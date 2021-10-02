import time

from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Delay",
    inputs=dict(val="Object"),
    outputs=dict(result="Object"))
def init(node, global_state, delay: float = 0.2) -> Callable:
    """
    Delay the execution.
    """
    def tick(value):
        time.sleep(delay)
        return {"delayed": value["val"]}
    return tick
