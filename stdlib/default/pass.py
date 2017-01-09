def init(node, global_spec):
    def tick(value):
        return {}
    node["tick"] = tick

def spec(node):
    node["name"] = "Pass"
    node["inputs"]["in"] = "Object"
    node["outputs"]["out"] = "Object"
    node["desc"] = "Pass an object. Does nothing."
