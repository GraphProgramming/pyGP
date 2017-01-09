def init(node, global_state):
    def tick(value):
        return {"result": str(value["val"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "toString"
    node["inputs"]["val"] = "Object"
    node["outputs"]["result"] = "String"
    node["desc"] = "Converts to string"
