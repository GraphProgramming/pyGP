import os
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="(Serial) Execute",
    inputs=dict(cmd="String", trigger="Object"),
    outputs=dict(trigger="Object"))
def init(node, global_state) -> Callable:
    """
    Execute a system command.
    """
    def tick(cmd, trigger):
        os.system(cmd)
        return {"trigger": trigger}
    return tick
