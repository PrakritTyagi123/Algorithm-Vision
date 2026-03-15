"""Fixed combinations with final summary message."""


def combinations_fixed(values: list[int], k: int) -> list[dict]:
    steps = []
    n = len(values)
    results = []

    def combine(start, combo):
        if len(combo) == k:
            result = [values[i] for i in combo]
            results.append(result)
            steps.append({
                "step": len(steps) + 1,
                "array": values,
                "active": list(combo),
                "found": list(combo),
                "description": f"Combination found: {result}",
            })
            return
        for i in range(start, n):
            combo.append(i)
            steps.append({
                "step": len(steps) + 1,
                "array": values,
                "active": list(combo),
                "current": i,
                "description": f"Add {values[i]}",
            })
            combine(i + 1, combo)
            combo.pop()

    combine(0, [])
    steps.append({
        "step": len(steps) + 1,
        "array": values,
        "description": f"Done! Found {len(results)} combinations of size {k}",
    })
    return steps
