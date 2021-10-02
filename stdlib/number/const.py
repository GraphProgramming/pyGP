from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Number Const",
    inputs=dict(),
    outputs=dict(result="Number"))
def init(node, global_state, value: float = 0) -> Callable:
    """
    A constant number.
    """
    def tick():
        return {"result": value}
    return tick
