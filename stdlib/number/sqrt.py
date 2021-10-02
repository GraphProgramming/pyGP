import math
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="SQRT",
    inputs=dict(a="Number"),
    outputs=dict(result="Number"))
def init(node, global_state) -> Callable:
    """
    SQRT(a)
    """
    def tick(a):
        return {"result": math.sqrt(a)}
    return tick
