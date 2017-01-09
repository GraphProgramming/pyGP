import sys

def init(node, global_state):
    def tick(value):
        print(value["val"])
        sys.stdout.flush()

    node["tick"] = tick

def spec(node):
    node["name"] = "Print"
    node["inputs"]["val"] = "Object"
    node["desc"] = "Print on the screen."
