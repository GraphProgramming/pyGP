from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Split",
    inputs=dict(val="String"),
    outputs=dict(result="Array"))
def init(node, global_state, sep: str = "/") -> Callable:
    """
    Split a string into an array of strings at the position of separator.
    """
    def tick(val):
        return {"result": val.split(sep)}
    return tick
