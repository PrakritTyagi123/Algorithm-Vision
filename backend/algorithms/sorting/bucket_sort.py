"""Bucket Sort — O(n+k) avg time, O(n) space, Stable"""


def bucket_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []

    if not a:
        return steps

    max_val = max(a) + 1
    bucket_count = max(1, n // 3)
    buckets = [[] for _ in range(bucket_count)]

    # Distribution phase
    for i in range(n):
        idx = min(a[i] * bucket_count // max_val, bucket_count - 1)
        buckets[idx].append(a[i])
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "current": i,
            "active": [i],
            "description": f"Distribute {a[i]} → bucket {idx} (now {buckets[idx]})",
        })

    # Sort each bucket and collect
    pos = 0
    sorted_so_far = []
    for bi, bucket in enumerate(buckets):
        bucket.sort()
        if bucket:
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "description": f"Sort bucket {bi}: {bucket}",
            })
        for val in bucket:
            old_val = a[pos]
            a[pos] = val
            sorted_so_far.append(pos)
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "swap": [pos] if old_val != val else [],
                "active": [pos],
                "sorted": list(sorted_so_far),
                "description": f"Collect: place {val} at index {pos}",
            })
            pos += 1

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
