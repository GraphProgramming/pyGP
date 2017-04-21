import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.matrix(value["val"]).T}

    node["tick"] = tick

def spec(node):
    node["name"] = "toMatrix"
    node["inputs"]["val"] = "Vector"
    node["outputs"]["result"] = "Matrix"
    node["desc"] = "Converts a vector to a matrix."
