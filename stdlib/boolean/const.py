def init(node, global_state):
    def tick(value):
        return {"result": node["args"]["value"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Const"
    node["outputs"]["result"] = "Boolean"
    node["args"]["value"] = True
    node["desc"] = "Return a const boolean"
