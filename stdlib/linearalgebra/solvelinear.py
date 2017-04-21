import numpy as np

def init(node, global_state):
    def tick(value):
        return {"x": np.linalg.solve(value["M"], value["b"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Solve Mx = b"
    node["inputs"]["M"] = "Matrix"
    node["inputs"]["b"] = "Vector"
    node["outputs"]["x"] = "Vector"
    node["desc"] = "Solves Mx = b for x."
