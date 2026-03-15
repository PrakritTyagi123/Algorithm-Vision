"""Radix Sort — O(d·n) time, O(n+k) space, Stable"""


def radix_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []

    if not a:
        return steps

    max_val = max(a)
    exp = 1
    digit_pos = 1

    while max_val // exp > 0:
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "description": f"Pass {digit_pos}: sorting by {'ones' if exp == 1 else 'tens' if exp == 10 else 'hundreds' if exp == 100 else f'10^{len(str(exp))-1}'} digit",
        })

        output = [0] * n
        count = [0] * 10

        # Count digits
        for i in range(n):
            digit = (a[i] // exp) % 10
            count[digit] += 1
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "current": i,
                "active": [i],
                "description": f"Element {a[i]}: digit = {digit}",
            })

        # Cumulative count
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build output (show each placement)
        for i in range(n - 1, -1, -1):
            digit = (a[i] // exp) % 10
            count[digit] -= 1
            pos = count[digit]
            output[pos] = a[i]

        # Show the rearranged result
        old_a = list(a)
        for i in range(n):
            a[i] = output[i]

        # Highlight positions that changed
        changed = [i for i in range(n) if old_a[i] != a[i]]
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "swap": changed[:2] if len(changed) >= 2 else changed,
            "active": changed,
            "description": f"After pass {digit_pos}: {list(a)}",
        })

        exp *= 10
        digit_pos += 1

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
