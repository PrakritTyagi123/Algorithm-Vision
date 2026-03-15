"""Chinese Remainder Theorem — find x such that x ≡ r_i (mod m_i) for all i."""


def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> list[dict]:
    steps = []

    if not remainders or not moduli or len(remainders) != len(moduli):
        steps.append({"step": 1, "description": "Invalid input: need equal-length remainder and moduli lists"})
        return steps

    steps.append({"step": len(steps) + 1,
                  "description": f"Solve: " + ", ".join(f"x ≡ {r} (mod {m})" for r, m in zip(remainders, moduli))})

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1

    # Compute product of all moduli
    M = 1
    for m in moduli:
        M *= m

    steps.append({"step": len(steps) + 1,
                  "table": [[M]],
                  "col_headers": ["M (product)"],
                  "description": f"M = product of all moduli = {M}"})

    x = 0
    for i, (r, m) in enumerate(zip(remainders, moduli)):
        Mi = M // m
        gcd, yi, _ = extended_gcd(Mi % m, m)

        if gcd != 1:
            steps.append({"step": len(steps) + 1,
                          "description": f"Moduli not coprime! GCD({Mi}, {m}) = {gcd}"})
            return steps

        yi = yi % m
        contribution = r * Mi * yi

        steps.append({
            "step": len(steps) + 1,
            "table": [[r, m, Mi, yi, contribution]],
            "col_headers": ["r_i", "m_i", "M_i", "y_i", "r_i·M_i·y_i"],
            "current": [0, 4],
            "description": f"Eq {i+1}: M_{i+1}={Mi}, y_{i+1}={yi}, contribution={contribution}",
        })

        x += contribution

    x = x % M

    steps.append({
        "step": len(steps) + 1,
        "description": f"Solution: x = {x} (mod {M})",
    })

    # Verify
    for r, m in zip(remainders, moduli):
        steps.append({
            "step": len(steps) + 1,
            "description": f"Verify: {x} mod {m} = {x % m} {'✓' if x % m == r else '✗'}",
        })

    return steps
