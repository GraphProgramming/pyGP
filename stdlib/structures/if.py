def init(node, global_state):
    def tick(value):
        if value["condition"]:
            return {"true": value["val"]}
        else:
            return {"false": value["val"]}

    node["tick"] = tick

def spec(node):
  node["name"] = "If"
  node["inputs"]["val"] = "Object"
  node["inputs"]["condition"] = "Boolean"
  node["outputs"]["true"] = "Object"
  node["outputs"]["false"] = "Object"
  node["desc"] = "Pass val based on condition."
