import os

def init(node, global_state):
    def tick(value):
        os.system(value["cmd"])
        return {"trigger": value["trigger"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "(Serial) Exec"
    node["inputs"]["cmd"] = "String"
    node["inputs"]["trigger"] = "Object"
    node["outputs"]["trigger"] = "Object"
    node["desc"] = "Execute a system command."
