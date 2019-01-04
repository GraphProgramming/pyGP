from gpm.pyGP.__main__ import GraphExState, GraphEx

def init(node, global_state):
    def tick(value):
        gex = GraphEx(node["args"]["graphname"], global_state.create_child_state())
        return {"ret": gex.run(value["val"])}

    node["tick"] = tick

def spec(node):
    node["name"] = "Subgraph"
    node["inputs"]["val"] = "Object"
    node["outputs"]["ret"] = "Object"
    node["args"]["graphname"] = "Default.graph.json"
    node["desc"] = "Call a graph."
