import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.array(node["args"]["value"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Matrix"
    node["outputs"]["result"] = "Matrix"
    node["args"]["value"] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    node["desc"] = "A simple matrix"
