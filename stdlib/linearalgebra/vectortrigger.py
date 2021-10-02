from time import sleep
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Vector Trigger",
    inputs=dict(),
    outputs=dict(result="Matrix"))
def init(node, global_state, value = [1, 0, 0], time = 1.0) -> Callable:
    """
    A simple vector.
    """
    def tick():
        global_state.publish(node, "result", value)
        sleep(time)
        global_state.shedule(node)
        return {}
    return tick
