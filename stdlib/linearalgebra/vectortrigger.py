import time
import sys

def init(node, global_state):
    def tick(value):
        global_state.publish(node, "result", node["args"]["value"])
        time.sleep(node["args"]["time"])
        global_state.shedule(node)
        return {}

    node["tick"] = tick

def spec(node):
    node["name"] = "Vector Trigger"
    node["outputs"]["result"] = "Vector"
    node["args"]["value"] = [1, 0, 0]
    node["args"]["time"] = 1.0
    node["desc"] = "A simple vector"
