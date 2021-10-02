from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Concat",
    inputs=dict(a="String", b="String"),
    outputs=dict(result="String"))
def init(node, global_state) -> Callable:
    """
    a + b
    """
    def tick(a, b):
        return {"result": a + b}
    return tick
