from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="ArgNode",
    inputs=dict(),
    outputs=dict(value="Object"))
def init(node, global_state, argname: str = "verbose", default = True) -> Callable:
    """
    Arguments that are passed to the graph via call.
    """
    def tick():
        ret = default
        if argname in global_state.arguments:
            ret = global_state.arguments[argname]
        return {"value": ret}
    return tick
