import argparse
import json
import sys
import time
from threading import Thread
from threading import Lock
from threading import Event
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
try:
    from queue import Queue
except:
    from Queue import Queue

import traceback
try:
    import rospy
except:
    pass

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import gpm.pyGP.debugger as debugger


class GraphExState(object):
    def __init__(self, restricted_mode=False):
        self.arguments = {}
        self.shared_dict = {}
        self.output_dict = {}
        self.restricted_mode = restricted_mode
        self.graph = None
        self.publish = None
        self.shedule = None
        self.output = None
        self.parent = None
        self.shutdown_hooks = []
        self.shutdown_blockers = 0

    def create_child_state(self):
        state = GraphExState()
        if "debugger" in self.shared_dict:
            state.shared_dict["debugger"] = self.shared_dict["debugger"]
        state.restricted_mode = self.restricted_mode
        state.parent = self
        return state

class GraphEx(object):
    def __init__(self, graph_path, state, verbose = False):
        self.eventSerial = Event()
        self.eventThreaded = Event()
        self.running = True
        self.state = state
        self.serial_mode = False
        self.nodes = {}
        self.queue_parallel = Queue()
        self.queue_serial = Queue()
        self.in_execution = {}
        self.lock = Lock()
        self.input_nodes = {}
        self.thread_pool = None

        # Open the graph and parse it as json.
        data = open(graph_path, 'r').read()
        self.verbose = verbose
        self.raw_graph = json.loads(data)

        # Now build a graph that we can work with efficiently.
        self.findAndCreateNodes(self.raw_graph["nodes"])
        self.findAndCreateConnections(self.raw_graph["connections"])

    def findAndCreateNodes(self, nodelist):
        # Empty nodes and input nodes list.
        self.nodes = {}
        self.state.graph = self.nodes
        self.input_nodes = {}

        # Load all nodes.
        for node in nodelist:
            if node["name"] in self.nodes:
                raise Exception("Invalid Graph: Duplicate node name. All node names must be unique!")

            # Try to import the code required for a node.
            codeName, nodeName = node["code"].split(":")
            try:
                if self.verbose:
                    print("Importing %s" % codeName)
                module = __import__("%s" % codeName, fromlist=["NODES"])
            except ImportError:
                module = None
            if module is None:
                # Try to import the code required for a node.
                try:
                    codeName = "gpm.pyGP." + codeName
                    if self.verbose:
                        print("Importing %s" % codeName)
                    module = __import__("%s" % codeName, fromlist=["NODES"])
                except ImportError:
                    module = None
                    raise ImportError("Cannot find implementation for node: " + node["code"])

            # Create node and add lists for connecting them.
            try:
                node["tick"] = module.NODES[nodeName]["code"](node, self.state, **node["args"])
            except Exception as e:
                raise RuntimeError(node["code"]) from e
            node["node_uid"] = node["name"]
            node["heat"] = 0
            if not ("main_thread" in node):
                node["main_thread"] = False
            if not ("buffer_policy" in node):
                node["buffer_policy"] = "undefined"
            if not ("buffer_size" in node):
                node["buffer_size"] = -1
            node["nextNodes"] = []
            node["prevNodes"] = []
            node["ins"] = {}
            node["outs"] = {}
            node["input_buffer"] = {}

            # Add the node to the internal lists for inputs and all nodes.
            self.nodes[node["name"]] = node
            if len(self.nodes[node["name"]]["inputs"]) == 0:
                self.input_nodes[node["name"]] = self.nodes[node["name"]]

    def findAndCreateConnections(self, connectionlist):
        self.connections = {}
        for conn in connectionlist:
            # Find all nodes and outputs as well as inputs.
            inputNode = self.nodes[conn["input"]["node"]]
            outputNode = self.nodes[conn["output"]["node"]]
            outputQualifier = conn["input"]["output"]
            inputQualifier = conn["output"]["input"]

            # Link the nodes together
            inputNode["nextNodes"].append(outputNode)
            if outputQualifier not in inputNode["outs"]:
                inputNode["outs"][outputQualifier] = []
            inputNode["outs"][outputQualifier].append({"node":outputNode,"var":inputQualifier})
            outputNode["prevNodes"].append(inputNode)
            outputNode["ins"][inputQualifier] = {"var":outputQualifier}

    def shedule(self, node, queue):
        self.lock.acquire()
        queue.put(node)
        self.eventSerial.set()
        self.eventThreaded.set()
        self.lock.release()

    def shedule_automatic(self, node):
        queue = self.queue_parallel
        if node["main_thread"] or self.serial_mode:
            queue = self.queue_serial
        self.shedule(node, queue)

    def publish(self, node, topic, msg):
        if topic in node["outputs"]:
            for next_node in node["nextNodes"]:
                for conn in node["outs"][topic]:
                    if next_node["name"] == conn["node"]["name"]:
                        # TODO check is there really a lock required?
                        self.lock.acquire()
                        if not conn["var"] in next_node["input_buffer"]:
                            next_node["input_buffer"][conn["var"]] = Queue()
                        next_node["input_buffer"][conn["var"]].put(msg)
                        self.lock.release()
                        queue = self.queue_parallel
                        if next_node["main_thread"] or self.serial_mode:
                            queue = self.queue_serial
                        self.shedule(next_node, queue)
        else:
            print("ERROR: Topic '" + str(topic) + "' is not an output of the node '" + str(node["name"]) + "' (" + str(node["code"]) + ").")

    def tryGetFromQueue(self, queue):
        elem = None
        self.lock.acquire()
        if not queue.empty():
            elem = queue.get()
            # Check if element can be executed
            if elem["name"] in self.in_execution:
                queue.put(elem)
                elem = None
            else:
                for x in elem["ins"]:
                    if (not x in elem["input_buffer"]) or elem["input_buffer"][x].empty():
                        elem = None
                        break
        if not elem is None:
            self.in_execution[elem["name"]] = elem
        self.lock.release()
        return elem

    def executeThreaded(self, initialization_required=True):
        # Initialisation
        if initialization_required:
            self.state.publish = self.publish
            self.state.shedule = self.shedule_automatic
            n = multiprocessing.cpu_count()
            self.thread_pool = ThreadPoolExecutor(n * 16)
            for x in self.input_nodes:
                queue = self.queue_parallel
                if self.input_nodes[x]["main_thread"]:
                    queue = self.queue_serial
                self.shedule(self.input_nodes[x], queue)

        # Execution
        t = Thread(target=self.dispatchLoop, args=(self.queue_parallel, True))
        t.setDaemon(True)
        t.start()
        self.executeSerial(initialization_required=False)

    def executeSerial(self, initialization_required=True):
        # Initialisation
        if initialization_required:
            self.serial_mode = True
            self.state.publish = self.publish
            self.state.shedule = self.shedule_automatic
            for x in self.input_nodes:
                self.shedule(self.input_nodes[x], self.queue_serial)

        # Execution
        self.dispatchLoop(self.queue_serial, False)

    def dispatchLoop(self, queue, start_threaded):
        while self.is_running() and ((not self.queue_serial.empty()) or (not self.queue_parallel.empty()) or self.state.shutdown_blockers > 0 or len(self.in_execution) > 0):
            elem = self.tryGetFromQueue(queue)
            if elem is None:
                if start_threaded:
                    self.eventThreaded.wait()
                    self.eventThreaded.clear()
                else:
                    self.eventSerial.wait()
                    self.eventSerial.clear()
                continue

            inputs = {}
            for x in elem["input_buffer"]:
                while 0 < elem["buffer_size"] and elem["input_buffer"][x].qsize() > elem["buffer_size"]:
                    elem["input_buffer"][x].get()
                inputs[x] = elem["input_buffer"][x].get()
                if elem["buffer_policy"] == "keep":
                    elem["input_buffer"][x].put(inputs[x])
            if start_threaded:
                self.thread_pool.submit(self.tickNode, elem, inputs)
            else:
                self.tickNode(elem, inputs)

    def is_running(self):
        running = self.running
        try:
            running = running and not rospy.is_shutdown()
        except:
            pass
        return running

    def kill(self):
        self.running = False

    def tickNode(self, node, inputs):
        try:
            if "debugger" in self.state.shared_dict:
                node["heat"] += 1
                dat = {"state": True, "heat": node["heat"]}
                data_str = "running:" + json.dumps(dat)
                self.state.shared_dict["debugger"].send("data_" + node["node_uid"] + ":" + data_str)
            result = node["tick"](**inputs)
            sys.stdout.flush()
            if "debugger" in self.state.shared_dict:
                dat = {"state": False, "heat": node["heat"]}
                data_str = "running:" + json.dumps(dat)
                self.state.shared_dict["debugger"].send("data_" + node["node_uid"] + ":" + data_str)
            if result is not None:
                for x in result:
                    self.publish(node, x, result[x])
        except:
            print("ERROR: " + str(sys.exc_info()[0]))
            print(traceback.format_exc())
            sys.stdout.flush()
        self.lock.acquire()
        del self.in_execution[node["name"]]
        self.eventThreaded.set()
        self.eventSerial.set()
        self.lock.release()

    def run(self, args=None):
        self.state.shared_dict["kill"] = False
        if args is not None:
            self.state.arguments = args
        self.executeThreaded()
        self.kill()
        for hook in self.state.shutdown_hooks:
            hook()
        return self.state.output_dict

def main(argv):
    parser = argparse.ArgumentParser(description='Graph Programming Manager')
    parser.add_argument("--debug", required=False, action="store_true", help="Debug mode.")
    parser.add_argument("--restricted", required=False, action="store_true", help="If running in restricted mode.")
    parser.add_argument("file", type=str, help="Run an extension")
    args, other_args = parser.parse_known_args(argv)

    state = GraphExState(restricted_mode=args.restricted)
    if args.debug:
        state.shared_dict["debugger"] = debugger.Debugger()
    gex = GraphEx(args.file, state)
    try:
        run_args = json.loads(" ".join(other_args))
    except:
        run_args = {}
    if args.debug:
        while not state.shared_dict["debugger"].has_clients():
            time.sleep(0.2)
    result = gex.run(run_args)
    print(json.dumps(result))


if __name__ == "__main__":
    main(sys.argv[1:])
