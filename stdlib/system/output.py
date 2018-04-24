def init(node, global_state):
    def tick(value):
        global_state.output_dict[node["args"]["outputname"]] = value["val"]
        return {}

    node["tick"] = tick

def spec(node):
    node["name"] = "Output"
    node["inputs"]["val"] = "Object"
    node["args"]["outputname"] = "test"
    node["desc"] = "Sets the output of the program"
