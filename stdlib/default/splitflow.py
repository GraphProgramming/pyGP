def init(node, global_state):
    def tick(value):
        return {"left": value["val"], "right": value["val"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Splitflow 2"
    node["inputs"]["val"] = "Object"
    node["outputs"]["left"] = "Object"
    node["outputs"]["right"] = "Object"
    node["desc"] = "Split the flow into two."
