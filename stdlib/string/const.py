def init(node, global_state):
    def tick(value):
        return {"result": node["args"]["value"]}

    node["tick"] = tick

def spec(node):
    node["name"] = "String Const"
    node["outputs"]["result"] = "String"
    node["args"]["value"] = "Hello World!"
    node["desc"] = "Returns the arg on the output."
