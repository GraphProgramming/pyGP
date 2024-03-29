from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Multiply",
    inputs=dict(a="Number", b="Number"),
    outputs=dict(result="Number"))
def init(node, global_state) -> Callable:
    """
    Multiply to floating point number.
    """
    def tick(a, b):
        return {"result": a * b}
    return tick
