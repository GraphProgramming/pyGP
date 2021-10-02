import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Matrix",
    inputs=dict(),
    outputs=dict(value="Matrix"))
def init(node, global_state, value = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) -> Callable:
    """
    A simple matrix
    """
    def tick():
        return {"result": np.array(value)}
    return tick
