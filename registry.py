from inspect import signature

REGISTRY = {}

def register(local_registry, name, inputs, outputs):
    def __wrapper(fun):
        REGISTRY[name] = dict(
            name=name,
            inputs=inputs,
            outputs=outputs,
            args=_kwargs(fun),
            desc=_desc(fun),
            code=fun,
        )
        local_registry[name] = REGISTRY[name]
        return fun
    return __wrapper

def _kwargs(fun):
    sig =  signature(fun)
    return {p.name: p.default for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD and p.default != p.empty}

def _desc(fun):
    sig =  fun.__doc__.strip()
    return sig
