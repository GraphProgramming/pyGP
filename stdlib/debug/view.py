'''
Debug View Module

This module renders a debug view.
'''

import json
import sys
import time
try:
    import base64
    import numpy as np
    import cv2
except:
    pass # Well there cannot be any cv input, so there will not occur any error.

def init(node, global_state):
    node["last_transmission"] = 0
    def tick(value):
        result = {"result": value["val"]}
        if not "debugger" in global_state.shared_dict:
            return result

        now = time.time()
        if now - node["last_transmission"] < 1.0 / node["args"]["max_fps"]:
            return result
        
        data_str = ""
        if type(value["val"]) is list or type(value["val"]) is dict or type(value["val"]) is str or type(value["val"]) is int:
            data_str = "json:" + json.dumps(value["val"])
        elif type(value["val"]) == np.ndarray and (len(value["val"].shape) != 2 or len(value["val"][1]) != 3) and not (len(value["val"].shape) == 3 and value["val"].shape[2] == 3):
            data_str = "json:" + json.dumps(value["val"].tolist())
        elif type(value["val"]) == np.ndarray:
            width = node["args"]["width"]
            height = node["args"]["height"]
            img = value["val"]
            if width == 0:
                width = 160
            if height == 0:
                height = int(width * 3 / 4)
            img = cv2.resize(img.copy(), (width, height), 0, 0, cv2.INTER_CUBIC)
            cnt = cv2.imencode('.png', img)[1].tostring()
            b64 = str(base64.encodestring(cnt))[2:-1]
            data_str = ("img:" + b64).replace("\n", "").replace("\\n", "")
        else:
            data_str = "type:" + str(type(value["val"]))
        global_state.shared_dict["debugger"].send("data_" + node["node_uid"] + ":" + data_str)
        node["last_transmission"] = now
        
        return result

    node["tick"] = tick

def spec(node):
    node["name"] = "View"
    node["inputs"]["val"] = "Object"
    node["outputs"]["result"] = "Object"
    node["args"]["width"] = 0
    node["args"]["height"] = 0
    node["args"]["max_fps"] = 2
    node["desc"] = "Views and passes the object."
