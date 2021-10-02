from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Splitflow 2",
    inputs=dict(val="Object"),
    outputs=dict(a="Object", b="Object"))
def init(node, global_state) -> Callable:
    """
    Split the flow into two.
    """
    def tick(val):
        return {"a": val, "b": val}
    return tick
