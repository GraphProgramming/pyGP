from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="String Const",
    inputs=dict(),
    outputs=dict(result="Boolean"))
def init(global_state, value: str = "Hello World!") -> Callable:
    """
    Return a const string.
    """
    def tick():
        return {"result": value}
    return tick
