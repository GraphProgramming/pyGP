import os

def init(node, global_state):
    def tick(value):
        os.system(value["cmd"])
        return {}

    node["tick"] = tick

def spec(node):
    node["name"] = "Exec"
    node["inputs"]["cmd"] = "String"
    node["desc"] = "Execute a system command."
