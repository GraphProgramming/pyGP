def init(node, global_state):
    def tick(value):
        return {"1": value["val"],
                "2": value["val"],
                "3": value["val"],
                "4": value["val"],
                "5": value["val"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Splitflow 5"
    node["inputs"]["val"] = "Object"
    node["outputs"]["1"] = "Object"
    node["outputs"]["2"] = "Object"
    node["outputs"]["3"] = "Object"
    node["outputs"]["4"] = "Object"
    node["outputs"]["5"] = "Object"
    node["desc"] = "Split the flow into five."
