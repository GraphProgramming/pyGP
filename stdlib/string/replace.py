from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Replace",
    inputs=dict(val="String"),
    outputs=dict(result="String"))
def init(node, global_state, search: str = "a", replace: str = "b") -> Callable:
    """
    Replace all occurances of "search" with "replace".
    """
    def tick(val):
        return {"result": val.replace(search, replace)}
    return tick
