from gpm.pyGP.__main__ import GraphEx
from typing import Callable
from gpm.pyGP.registry import register
NODES = {}

@register(NODES,
    name="Subgraph",
    inputs=dict(val="Object"),
    outputs=dict(ret="Object"))
def init(node, global_state, graphname: str = "Default.graph.json") -> Callable:
    """
    Call a graph.
    """
    def tick(val):
        gex = GraphEx(graphname, global_state.create_child_state())
        return {"ret": gex.run(val)}
    return tick
