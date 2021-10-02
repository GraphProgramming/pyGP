import numpy as np
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Matrix Product",
    inputs=dict(a="Matrix", b="Matrix"),
    outputs=dict(result="Matrix"))
def init(node, global_state) -> Callable:
    """
    Calculate the matrix multiplication of matrices.
    """
    def tick(a, b):
        return {"result": np.matmul(a, b)}
    return tick
