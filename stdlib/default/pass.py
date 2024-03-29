from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Pass",
    inputs=dict(inp="Object"),
    outputs=dict(outp="Object"))
def init(node, global_state) -> Callable:
    """
    Pass an object. Does nothing.
    """
    def tick(inp):
        return {"outp": inp}
    return tick
