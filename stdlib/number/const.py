def init(node, global_state):
    def tick(value):
        return {"result": node["args"]["value"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Const"
    node["outputs"]["result"] = "Number"
    node["args"]["value"] = 0
    node["desc"] = "A constant number"
