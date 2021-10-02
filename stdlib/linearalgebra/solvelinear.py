import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Solve Mx = b",
    inputs=dict(M="Matrix", b="Vector"),
    outputs=dict(x="Vector"))
def init(node, global_state) -> Callable:
    """
    Solves Mx = b for x.
    """
    def tick(M, b):
        return {"x": np.linalg.solve(M, b)}
    return tick
