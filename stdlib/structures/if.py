from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="If",
    inputs=dict(condition="Boolean", val="Object"),
    outputs=dict(true="Object", false="Object"))
def init(node, global_state) -> Callable:
    """
    Pass val based on condition.
    """
    def tick(condition, val):
        if condition:
            return {"true": val}
        else:
            return {"false": val}

    node["tick"] = tick
