"""Comb Sort — O(n²) worst, O(n log n) avg time, O(1) space"""


def comb_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    gap = n
    shrink = 1.3
    sorted_flag = False

    while not sorted_flag:
        gap = max(1, int(gap / shrink))
        sorted_flag = gap == 1

        steps.append({"step": len(steps)+1, "array": list(a),
                      "description": f"Gap = {gap}"})

        for i in range(n - gap):
            steps.append({"step": len(steps)+1, "array": list(a), "compare": [i, i+gap],
                          "description": f"Compare index {i} and {i+gap}"})
            if a[i] > a[i + gap]:
                a[i], a[i+gap] = a[i+gap], a[i]
                sorted_flag = False
                steps.append({"step": len(steps)+1, "array": list(a), "swap": [i, i+gap],
                              "description": f"Swap {a[i+gap]} and {a[i]}"})

    steps.append({"step": len(steps)+1, "array": list(a), "sorted": list(range(n)),
                  "description": "Array is sorted!"})
    return steps
