def init(node, global_state):
    def tick(value):
        argname = node["args"]["argname"]
        ret = node["args"]["default"]
        if argname in global_state.arguments:
            ret = global_state.arguments[argname]
        return {"value": ret}

    node["tick"] = tick

def spec(node):
    node["name"] = "ArgNode"
    node["outputs"]["value"] = "Object"
    node["args"]["argname"] = "verbose"
    node["args"]["default"] = True
    node["desc"] = "Arguments that are passed to the graph via call."
