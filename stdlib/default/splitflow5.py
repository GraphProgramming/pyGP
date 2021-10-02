from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Splitflow 5",
    inputs=dict(val="Object"),
    outputs=dict(a="Object", b="Object", c="Object", d="Object", e="Object"))
def init(node, global_state) -> Callable:
    """
    Split the flow into five.
    """
    def tick(val):
        return {"a": val,
                "b": val,
                "c": val,
                "d": val,
                "e": val}
    return tick
