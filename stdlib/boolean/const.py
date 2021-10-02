from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Bool Const",
    inputs=dict(),
    outputs=dict(result="Boolean"))
def init(node, global_state, value: bool = True) -> Callable:
    """
    Return a const boolean.
    """
    def tick():
        return {"result": value}
    return tick
