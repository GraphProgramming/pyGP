def init(node, global_state):
    def tick(value):
        return {"result": value["a"] * value["b"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Mult"
    node["inputs"]["a"] = "Matrix"
    node["inputs"]["b"] = "Matrix"
    node["outputs"]["result"] = "Matrix"
    node["desc"] = "Multiplies component wise."
