import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Dot Product",
    inputs=dict(a="Vector", b="Vector"),
    outputs=dict(result="Number"))
def init(node, global_state) -> Callable:
    """
    Calculate the dot product of vectors.
    """
    def tick(a, b):
        return {"result": np.dot(a, b)}
    return tick
