import os
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Execute",
    inputs=dict(cmd="String"),
    outputs=dict())
def init(node, global_state) -> Callable:
    """
    Execute a system command.
    """
    def tick(cmd):
        os.system(cmd)
        return {}
    return tick
