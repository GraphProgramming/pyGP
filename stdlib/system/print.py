import sys
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Print",
    inputs=dict(val="Object"),
    outputs=dict())
def init(node, global_state, value: str = "Hello World!") -> Callable:
    """
    Print on the screen.
    """
    def tick(val):
        print(val)
        sys.stdout.flush()
    return tick
