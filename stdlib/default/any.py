def init(node, global_state):
    def tick(value):
        return {"result": value["val"]}

    node["tick"] = tick

def spec(node):
   node["name"] = "Accept any inputs"
   node["inputs"]["val"] = "Object"
   node["outputs"]["result"] = "Object"
   node["desc"] = "Accept any input"
