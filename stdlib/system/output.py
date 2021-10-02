from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Output",
    inputs=dict(val="Object"),
    outputs=dict(value="Object"))
def init(node, global_state, outputname: str = "test") -> Callable:
    """
    Sets the output of the program.
    """
    def tick(val):
        global_state.output_dict[outputname] = val
        return {}
    return tick
