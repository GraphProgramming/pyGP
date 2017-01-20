'''
Debug View Module

This module renders a debug view.
'''

import json
import sys
try:
    import base64
    import numpy as np
    import cv2
except:
    pass # Well there cannot be any cv input, so there will not occur any error.

def init(node, global_state):
    def tick(value):
        result = {"result": value["val"]}
        if not "debugger" in global_state.shared_dict:
            return result
        
        data_str = ""
        if type(value["val"]) is list or type(value["val"]) is dict or type(value["val"]) is str or type(value["val"]) is unicode or type(value["val"]) is int:
            data_str = "json:" + json.dumps(value["val"])
        elif type(value["val"]) == np.ndarray:
            width = node["args"]["width"]
            height = node["args"]["height"]
            img = value["val"]
            if width == 0:
                width = 160
            if height == 0:
                height = int(width * 3 / 4)
            img = cv2.resize(img.copy(), (width, height), 0, 0, cv2.INTER_CUBIC)
            cnt = cv2.imencode('.png', img)[1]
            b64 = base64.encodestring(cnt)
            data_str = ("img:" + b64).replace("\n", "")
        else:
            data_str = "type:" + str(type(value["val"]))
        global_state.shared_dict["debugger"].send("data_" + node["node_uid"] + ":" + data_str)
            
        
        return result

    node["tick"] = tick

def spec(node):
    node["name"] = "View"
    node["inputs"]["val"] = "Object"
    node["outputs"]["result"] = "Object"
    node["args"]["width"] = 0
    node["args"]["height"] = 0
    node["desc"] = "Views and passes the object."
