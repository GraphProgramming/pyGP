import time

def init(node, global_state):
    def tick(value):
        time.sleep(node["args"]["delay"])
        return {"delayed": value["val"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "Delay"
    node["inputs"]["val"] = "Object"
    node["outputs"]["delayed"] = "Object"
    node["args"]["delay"] = 0.2
    node["desc"] = "Delay the execution."
