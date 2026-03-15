"""Suffix Array — O(n log n) construction with step visualization."""


def suffix_array(text: str) -> list[dict]:
    steps = []
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]

    steps.append({"step": len(steps) + 1,
                  "description": f"All suffixes of '{text}':"})

    # Sort suffixes
    suffixes.sort()
    sa = [idx for _, idx in suffixes]

    for rank, (suffix, idx) in enumerate(suffixes):
        steps.append({
            "step": len(steps) + 1,
            "current": [0, rank],
            "description": f"SA[{rank}] = {idx}: '{suffix}'",
        })

    # Build LCP array
    lcp = [0] * n
    inv_sa = [0] * n
    for i in range(n):
        inv_sa[sa[i]] = i

    k = 0
    for i in range(n):
        if inv_sa[i] == 0:
            k = 0
            continue
        j = sa[inv_sa[i] - 1]
        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1
        lcp[inv_sa[i]] = k
        if k:
            k -= 1

    steps.append({
        "step": len(steps) + 1,
        "table": [sa, lcp],
        "row_headers": ["SA", "LCP"],
        "description": f"Suffix Array: {sa}, LCP: {lcp}",
    })

    return steps
