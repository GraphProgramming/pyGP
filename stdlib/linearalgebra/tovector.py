import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.squeeze(np.asarray(value["val"].T))}

    node["tick"] = tick

def spec(node):
    node["name"] = "toVector"
    node["inputs"]["val"] = "Matrix"
    node["outputs"]["result"] = "Vector"
    node["desc"] = "Convert Matrix to vector."
