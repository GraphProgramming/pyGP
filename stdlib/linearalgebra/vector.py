def init(node, global_state):
    def tick(value):
        return {"result": node["args"]["value"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Vector"
    node["outputs"]["result"] = "Vector"
    node["args"]["value"] = [1, 0, 0]
    node["desc"] = "A simple vector"
