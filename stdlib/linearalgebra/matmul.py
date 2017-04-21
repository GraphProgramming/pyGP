import numpy as np

def init(node, global_state):
    def tick(value):
        return {"result": np.matmul(value["a"], value["b"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Matrix Product"
    node["inputs"]["a"] = "Matrix"
    node["inputs"]["b"] = "Matrix"
    node["outputs"]["result"] = "Number"
    node["desc"] = "Calculate the matrix multiplication of matrices."
