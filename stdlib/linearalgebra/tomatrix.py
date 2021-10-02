import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="toMatrix",
    inputs=dict(val="Vector"),
    outputs=dict(result="Matrix"))
def init(node, global_state) -> Callable:
    """
    Converts a vector to a matrix.
    """
    def tick(val):
        return {"result": np.matrix(val).T}
    return tick
