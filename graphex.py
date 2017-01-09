import json
import sys
import time
from threading import Thread
from threading import Lock
import debugger
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
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

class GraphExState(object):
    def __init__(self):
        self.shared_dict = {}
        self.output_dict = {}
        self.restricted_mode = False
        self.graph = None
        self.publish = None
        self.output = None
        self.shutdown_hooks = []
        self.shutdown_blockers = 0

class GraphEx(object):
    def __init__(self, graph_path, state, verbose = False):
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
            try:
                codeName = node["code"]
                if self.verbose:
                    print("Importing %s" % codeName)
                module = __import__("%s" % codeName, fromlist=["init"])
            except ImportError:
                module = None
                raise ImportError("Cannot find implementation for node: " + node["code"])

            # Create node and add lists for connecting them.
            module.init(node, state)
            node["node_uid"] = node["name"]
            node["heat"] = 0
            node["main_thread"] = False
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
            inputNode["outs"][outputQualifier].append({"node":outputNode,"var":inputQualifier});
            outputNode["prevNodes"].append(inputNode)
            outputNode["ins"][inputQualifier] = {"var":outputQualifier}

    def shedule(self, node, queue):
        self.lock.acquire()
        queue.put(node)
        self.lock.release()

    def publish(self, node, topic, msg):
        if topic in node["outs"]:
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
                        if node["main_thread"] or self.serial_mode:
                            queue = self.queue_serial
                        self.shedule(next_node, queue)
        else:
            print("ERROR: Topic '" + str(topic) + "' is not an output of the node.")

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
            for x in self.input_nodes:
                self.shedule(self.input_nodes[x], self.queue_serial)

        # Execution
        self.dispatchLoop(self.queue_serial, False)

    def dispatchLoop(self, queue, start_threaded):
        while self.running and ((not queue.empty()) or self.state.shutdown_blockers > 2):
            elem = self.tryGetFromQueue(queue)
            if elem is None:
                time.sleep(0.01)
                continue

            inputs = {}
            for x in elem["input_buffer"]:
                # TODO correctly manage input buffer! (buffer policy implementation)
                inputs[x] = elem["input_buffer"][x].get()
            if start_threaded:
                self.thread_pool.submit(self.tickNode, elem, inputs)
            else:
                self.tickNode(elem, inputs)

    def tickNode(self, node, inputs):
        result = node["tick"](inputs)
        if result is not None:
            for x in result:
                self.publish(node, x, result[x])
        self.lock.acquire()
        del self.in_execution[node["name"]]
        self.lock.release()

if __name__ == "__main__":
    # Execute all graph paths passed as parameters.
    if len(sys.argv) < 2:
        print("Usage: python graphex.py <file.graph.json> [debug] [cluster] [args]")
    else:
        state = GraphExState()
        offset = 2
        if len(sys.argv) > offset and sys.argv[offset] == "debug":
            state.shared_dict["debugger"] = debugger.Debugger()
            offset += 1
        if len(sys.argv) > offset and sys.argv[offset] == "cluster":
            state.restricted_mode = True
            offset += 1
        if len(sys.argv) > offset:
            dbg = None
            if "debugger" in state.shared_dict:
                dbg = state.shared_dict["debugger"]
            state.shared_dict = json.loads(" ".join(sys.argv[offset:]))
            if dbg is not None:
                state.shared_dict["debugger"] = dbg
        state.shared_dict["kill"] = False
        gex = GraphEx(sys.argv[1], state)
        gex.executeThreaded()
        for hook in state.shutdown_hooks:
            hook()
        print(json.dumps(state.output_dict))
