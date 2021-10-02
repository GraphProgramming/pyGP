import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Vector",
    inputs=dict(),
    outputs=dict(result="Vector"))
def init(node, global_state, value = [1, 0, 0]) -> Callable:
    """
    A simple vector.
    """
    def tick():
        return {"result": np.array(value)}
    return tick
