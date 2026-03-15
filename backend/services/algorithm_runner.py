"""Service: Algorithm Runner — delegates to algorithm modules."""


class AlgorithmRunner:
    """Central dispatcher for running algorithms by category/name."""

    def __init__(self):
        self._registry = {}

    def register(self, category: str, name: str, func):
        key = f"{category}/{name}"
        self._registry[key] = func

    def run(self, category: str, name: str, **kwargs):
        key = f"{category}/{name}"
        func = self._registry.get(key)
        if not func:
            raise ValueError(f"Unknown algorithm: {key}")
        return func(**kwargs)

    def list_algorithms(self, category: str = None):
        if category:
            return [k.split("/")[1] for k in self._registry if k.startswith(category + "/")]
        return list(self._registry.keys())
