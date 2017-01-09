def init(node, global_state):
    def tick(value):
        return {"result": value["a"] * value["b"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Mult"
    node["inputs"]["a"] = "Number"
    node["inputs"]["b"] = "Number"
    node["outputs"]["result"] = "Number"
    node["desc"] = "a * b"
