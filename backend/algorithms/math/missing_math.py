"""Missing Mathematical Algorithms with step-by-step visualization."""
import random


def extended_euclidean(a: int, b: int) -> list[dict]:
    steps = []
    steps.append({"step": len(steps) + 1,
                  "description": f"Extended Euclidean: find gcd({a}, {b}) and coefficients x, y"})

    def ext_gcd(a, b):
        if a == 0:
            steps.append({"step": len(steps) + 1,
                          "table": [[a, b, b, 0, 1]],
                          "col_headers": ["a", "b", "gcd", "x", "y"],
                          "description": f"Base: gcd=b={b}, x=0, y=1"})
            return b, 0, 1

        gcd, x1, y1 = ext_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1

        steps.append({"step": len(steps) + 1,
                      "table": [[a, b, gcd, x, y]],
                      "col_headers": ["a", "b", "gcd", "x", "y"],
                      "description": f"ext_gcd({a}, {b}): x={x}, y={y}"})
        return gcd, x, y

    gcd, x, y = ext_gcd(a, b)
    steps.append({"step": len(steps) + 1,
                  "description": f"gcd({a}, {b}) = {gcd}, {a}·({x}) + {b}·({y}) = {a*x + b*y}"})
    return steps


def euler_totient(n: int) -> list[dict]:
    steps = []
    steps.append({"step": len(steps) + 1,
                  "description": f"Compute Euler's totient φ({n})"})

    result = n
    temp = n
    p = 2

    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
            steps.append({"step": len(steps) + 1,
                          "table": [[p, result]],
                          "col_headers": ["prime factor", "φ so far"],
                          "description": f"Factor {p}: φ = {result} (multiply by (1 - 1/{p}))"})
        p += 1

    if temp > 1:
        result -= result // temp
        steps.append({"step": len(steps) + 1,
                      "table": [[temp, result]],
                      "col_headers": ["prime factor", "φ so far"],
                      "description": f"Factor {temp}: φ = {result}"})

    # Show coprime numbers as table if small
    coprimes = [i for i in range(1, min(n + 1, 200)) if _gcd(i, n) == 1]
    if n <= 50:
        steps.append({"step": len(steps) + 1,
                      "table": [coprimes],
                      "col_headers": [str(x) for x in coprimes],
                      "description": f"Coprimes of {n}: {len(coprimes)} numbers"})

    steps.append({"step": len(steps) + 1,
                  "table": [[n, result]],
                  "col_headers": ["n", "φ(n)"],
                  "description": f"φ({n}) = {result}"})

    return steps


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def miller_rabin(n: int, k: int = 10) -> list[dict]:
    steps = []
    steps.append({"step": len(steps) + 1,
                  "table": [[n, k]],
                  "col_headers": ["n", "rounds"],
                  "description": f"Miller-Rabin primality test for n={n} with {k} rounds"})

    if n < 2:
        steps.append({"step": len(steps) + 1, "table": [[n, "No"]], "col_headers": ["n", "prime?"],
                      "description": f"{n} is not prime"})
        return steps
    if n == 2 or n == 3:
        steps.append({"step": len(steps) + 1, "table": [[n, "Yes"]], "col_headers": ["n", "prime?"],
                      "description": f"{n} is prime"})
        return steps
    if n % 2 == 0:
        steps.append({"step": len(steps) + 1, "table": [[n, "No"]], "col_headers": ["n", "prime?"],
                      "description": f"{n} is even — not prime"})
        return steps

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    steps.append({"step": len(steps) + 1,
                  "table": [[n - 1, r, d]],
                  "col_headers": ["n-1", "r", "d"],
                  "description": f"n-1 = {n-1} = 2^{r} · {d}"})

    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        steps.append({"step": len(steps) + 1,
                      "table": [[i + 1, a, x]],
                      "col_headers": ["round", "witness", "a^d mod n"],
                      "description": f"Round {i+1}: a={a}, a^d mod n = {x}"})

        if x == 1 or x == n - 1:
            steps.append({"step": len(steps) + 1,
                          "table": [[i + 1, a, x, "pass"]],
                          "col_headers": ["round", "a", "x", "result"],
                          "description": f"  → Probably prime (x={x})"})
            continue

        composite = True
        for j in range(r - 1):
            x = pow(x, 2, n)
            steps.append({"step": len(steps) + 1,
                          "table": [[i + 1, a, x, f"sq{j+1}"]],
                          "col_headers": ["round", "a", "x", "op"],
                          "description": f"  Squaring: x = {x}"})
            if x == n - 1:
                composite = False
                steps.append({"step": len(steps) + 1,
                              "table": [[i + 1, a, x, "pass"]],
                              "col_headers": ["round", "a", "x", "result"],
                              "description": f"  → Probably prime"})
                break

        if composite:
            steps.append({"step": len(steps) + 1,
                          "table": [[n, "COMPOSITE", a]],
                          "col_headers": ["n", "result", "witness"],
                          "description": f"{n} is COMPOSITE (witness: {a})"})
            return steps

    steps.append({"step": len(steps) + 1,
                  "table": [[n, "PRIME", k]],
                  "col_headers": ["n", "result", "rounds"],
                  "description": f"{n} is probably PRIME (passed {k} rounds)"})
    return steps
