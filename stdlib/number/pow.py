from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="POW",
    inputs=dict(a="Number", b="Number"),
    outputs=dict(result="Number"))
def init(node, global_state) -> Callable:
    """
    a ^ b
    """
    def tick(a, b):
        return {"result": a ** b}
    return tick
