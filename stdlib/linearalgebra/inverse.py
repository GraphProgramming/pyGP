import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.linalg.inv(value["val"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Invert"
    node["inputs"]["val"] = "Matrix"
    node["outputs"]["result"] = "Matrix"
    node["desc"] = "Calculate the inverse for a matrix."
