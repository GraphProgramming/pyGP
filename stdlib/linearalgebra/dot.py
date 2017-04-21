import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.dot(value["a"], value["b"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Dot Product"
    node["inputs"]["a"] = "Vector"
    node["inputs"]["b"] = "Vector"
    node["outputs"]["result"] = "Number"
    node["desc"] = "Calculate the dot product of vectors."
