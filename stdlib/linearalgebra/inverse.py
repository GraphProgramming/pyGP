import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Invert",
    inputs=dict(val="Matrix"),
    outputs=dict(result="Matrix"))
def init(node, global_state) -> Callable:
    """
    Invert a matrix.
    """
    def tick(val):
        return {"result": np.linalg.inv(val)}
    return tick
