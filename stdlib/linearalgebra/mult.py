from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Multiply",
    inputs=dict(a="Matrix", b="Matrix"),
    outputs=dict(result="Matrix"))
def init(node, global_state) -> Callable:
    """
    Multiplies component wise.
    """
    def tick(a, b):
        return {"result": a * b}
    return tick
