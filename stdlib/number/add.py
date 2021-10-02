from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Add",
    inputs=dict(a="Number", b="Number"),
    outputs=dict(result="Number"))
def init(node, global_state) -> Callable:
    """
    Add to floating point numbers.
    """
    def tick(a, b):
        return {"result": a + b}
    return tick
