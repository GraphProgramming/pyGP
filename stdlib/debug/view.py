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
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="View",
    inputs=dict(val="Object"),
    outputs=dict(result="Object"))
def init(node, global_state, max_fps: float = 2, width: int = 160, height: int = 120) -> Callable:
    """
    Views and passes the object.
    """
    node["last_transmission"] = 0
    def tick(val):
        result = {"result": val}
        if not "debugger" in global_state.shared_dict:
            return result

        now = time.time()
        if now - node["last_transmission"] < 1.0 / max_fps:
            return result
        
        data_str = ""
        if type(val) is list or type(val) is dict or type(val) is str or type(val) is int:
            data_str = "json:" + json.dumps(val)
        elif type(val) == np.ndarray and (len(val.shape) != 2 or len(val[1]) != 3) and not (len(val.shape) == 3 and val.shape[2] == 3):
            data_str = "json:" + json.dumps(val.tolist())
        elif type(val) == np.ndarray:
            img = val
            img = cv2.resize(img.copy(), (width, height), 0, 0, cv2.INTER_CUBIC)
            cnt = cv2.imencode('.png', img)[1].tostring()
            b64 = str(base64.encodestring(cnt))[2:-1]
            data_str = ("img:" + b64).replace("\n", "").replace("\\n", "")
        else:
            data_str = "type:" + str(type(val))
        global_state.shared_dict["debugger"].send("data_" + node["node_uid"] + ":" + data_str)
        node["last_transmission"] = now
        return result
    return tick
