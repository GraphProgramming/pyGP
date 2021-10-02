import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="toVector",
    inputs=dict(val="Matrix"),
    outputs=dict(result="Vector"))
def init(node, global_state) -> Callable:
    """
    Convert Matrix to vector.
    """
    def tick(val):
        return {"result": np.squeeze(np.asarray(val.T))}
    return tick
