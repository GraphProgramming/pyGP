from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Transpose",
    inputs=dict(val="Matrix"),
    outputs=dict(result="Matrix"))
def init(node, global_state) -> Callable:
    """
    Transpose a matrix
    """
    def tick(val):
        return {"result": val.T}
    return tick
