from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="To String",
    inputs=dict(val="String"),
    outputs=dict(result="String"))
def init(node, global_state) -> Callable:
    """
    Convert something to a string.
    """
    def tick(val):
        return {"result": str(val)}
    return tick
