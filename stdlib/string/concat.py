def init(node, global_state):
    def tick(value):
        return {"result": value["left"] + value["right"]}
    node["tick"] = tick

def spec(node):
    node["name"] = "String Concat"
    node["inputs"]["left"] = "String"
    node["inputs"]["right"] = "String"
    node["outputs"]["result"] = "String"
    node["desc"] = "Concat left and right."
