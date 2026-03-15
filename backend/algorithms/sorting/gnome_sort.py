"""Gnome Sort — O(n²) time, O(1) space, Stable"""


def gnome_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    i = 0

    while i < n:
        if i == 0 or a[i] >= a[i - 1]:
            i += 1
        else:
            steps.append({"step": len(steps)+1, "array": list(a), "compare": [i-1, i],
                          "description": f"Compare {a[i-1]} and {a[i]}"})
            a[i], a[i-1] = a[i-1], a[i]
            steps.append({"step": len(steps)+1, "array": list(a), "swap": [i-1, i],
                          "description": f"Swap and step back"})
            i -= 1

    steps.append({"step": len(steps)+1, "array": list(a), "sorted": list(range(n)),
                  "description": "Array is sorted!"})
    return steps
