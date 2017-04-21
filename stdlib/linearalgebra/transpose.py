import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": value["val"].T}

    node["tick"] = tick

def spec(node):
    node["name"] = "Transpose"
    node["inputs"]["val"] = "Matrix"
    node["outputs"]["result"] = "Matrix"
    node["desc"] = "Transpose a matrix"
