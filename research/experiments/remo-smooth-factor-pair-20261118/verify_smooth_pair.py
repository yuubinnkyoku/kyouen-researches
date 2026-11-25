#!/usr/bin/env python3
"""K0952 audit: exact M-smooth cofactor reduction for the sigma_Z value-1 tail."""
from __future__ import annotations
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def sigma_E(P: int, alpha: int, beta: int) -> int:
    if alpha + beta <= 1:
        return 0
    frames = []
    k = alpha + beta
    while k > 1:
        q, r = divmod(P, k)
        frames.append((k, r))
        if r < alpha:
            P, alpha, beta = P + q, alpha - r - 1, beta + r
        else:
            P, alpha, beta = P + q + 1, beta + 2 * alpha - r - 1, r - alpha
        k -= 1
    sig = 0
    for k, r in reversed(frames):
        sig = (r + 1 + sig) % k
    return sig


def sigma_Z(M: int, K: int) -> int:
    if K <= 1:
        return 0
    q, r = divmod(M, K)
    return (r + 1 + sigma_E(M + q, K - 1 - r, r)) % K


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def primes_upto(n: int) -> list[int]:
    b = bytearray(b"\x01") * (n + 1)
    if n >= 0:
        b[0] = 0
    if n >= 1:
        b[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if b[p]:
            b[p*p:n+1:p] = b"\x00" * (((n-p*p)//p) + 1)
    return [i for i, v in enumerate(b) if v]


def smooth_part(n: int, M: int, primes: list[int]) -> tuple[int, int]:
    d, q = 1, n
    for p in primes:
        if p >= M:
            break
        while q % p == 0:
            q //= p
            d *= p
    return d, q


def tail_grid() -> dict:
    primes = primes_upto(100)
    prime_M = [m for m in primes if m <= 17]
    out = {
        "states": 0, "mismatch": 0, "live_states": 0, "live_hits": 0,
        "dead_states": 0, "dead_hits": 0, "smooth_mismatch": 0,
        "e_gt1": 0, "e_counts": {},
    }
    for M in prime_M:
        for kap in range(M - 1):
            live = math.gcd(kap + 1, M + 1) == 1
            C = math.gcd(M + 1, kap + 2)
            A = M * (M + 1) // C
            B = (M * (kap + 1) - 1) // C
            if math.gcd(A, B) != 1 or C > M - 1:
                out["smooth_mismatch"] += 1
            for t in range(max(M, 3), 101):
                Y = (M + 1) * t + kap + 1
                K = (M + 1) * t + kap
                k0 = M * t + kap - 1
                N = M * Y - 1
                Q = A * t + B
                D, P = smooth_part(N, M, primes)
                no_div_smooth = D < M and P > k0 and is_prime(P)
                no_div_direct = not any(N % d == 0 for d in range(M, k0 + 1))
                e = D // C
                no_div_union = any(
                    Q % d == 0 and is_prime(Q // d) and Q // d > k0
                    for d in range(1, M) if C * d < M
                )
                if (D % C != 0 or Q != N // C or Y == M * M or
                        no_div_smooth != no_div_direct or
                        no_div_smooth != no_div_union):
                    out["smooth_mismatch"] += 1
                actual = sigma_Z(M, K) == 1
                predicted = live and is_prime(Y) and no_div_smooth
                out["states"] += 1
                if actual != predicted:
                    out["mismatch"] += 1
                if live:
                    out["live_states"] += 1
                    if actual:
                        out["live_hits"] += 1
                        out["e_gt1"] += int(e > 1)
                        out["e_counts"][str(e)] = out["e_counts"].get(str(e), 0) + 1
                else:
                    out["dead_states"] += 1
                    out["dead_hits"] += int(actual)
    return out


def admissibility() -> dict:
    ps = primes_upto(1000)
    out = {
        "prime_M_le_97_count": 0, "live_residue_pairs": 0,
        "prime_modulus_checks": 0, "obstructions": 0,
    }
    for M in primes_upto(97):
        out["prime_M_le_97_count"] += 1
        for kap in range(M - 1):
            if math.gcd(kap + 1, M + 1) != 1:
                continue
            C = math.gcd(M + 1, kap + 2)
            a1, b1 = M + 1, kap + 1
            a2, b2 = M * (M + 1) // C, (M * (kap + 1) - 1) // C
            if (math.gcd(a1, b1) != 1 or math.gcd(a2, b2) != 1 or
                    a1 * b2 - a2 * b1 != -(M + 1) // C):
                out["obstructions"] += 1
            out["live_residue_pairs"] += 1
            for p in ps:
                out["prime_modulus_checks"] += 1
                if not any((a1*t+b1) % p and (a2*t+b2) % p for t in range(p)):
                    out["obstructions"] += 1
    return out


def build_audit() -> dict:
    g = tail_grid()
    a = admissibility()
    return {
        "experiment": "remo-smooth-factor-pair-20261118",
        "checks": {
            "EXACT_TAIL_GRID": {
                "prime_M": [2, 3, 5, 7, 11, 13, 17],
                "t_range": "max(M,3) <= t <= 100",
                "states": g["states"],
                "mismatches_vs_direct_sigma_Z": g["mismatch"],
                "live_states": g["live_states"],
                "live_hits": g["live_hits"],
                "dead_states": g["dead_states"],
                "dead_hits": g["dead_hits"],
                "smooth_part_vs_direct_divisor_mismatches": g["smooth_mismatch"],
                "e_gt_1_hit_count": g["e_gt1"],
                "finite_branch_counts_by_e": g["e_counts"],
                "ok": g["mismatch"] == 0 and g["smooth_mismatch"] == 0 and g["dead_hits"] == 0,
            },
            "LOCAL_ADMISSIBILITY": {
                "prime_M_le_97_count": a["prime_M_le_97_count"],
                "live_residue_pairs": a["live_residue_pairs"],
                "prime_moduli_le_1000": 1000,
                "prime_modulus_checks": a["prime_modulus_checks"],
                "obstructions": a["obstructions"],
                "ok": a["obstructions"] == 0,
            },
        },
        "all_ok": (g["mismatch"] == 0 and g["smooth_mismatch"] == 0 and
                   g["dead_hits"] == 0 and a["obstructions"] == 0),
    }


def main() -> None:
    payload = build_audit()
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    out = os.path.join(HERE, "output", "smooth_pair_audit.json")
    raw = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(raw)
    print("all_ok =", payload["all_ok"])
    print("audit_sha256 =", hashlib.sha256(raw.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
