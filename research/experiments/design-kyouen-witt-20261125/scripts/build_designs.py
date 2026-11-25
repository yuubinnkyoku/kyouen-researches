"""Build Steiner 3-design boards for the Kyouen game, from coding theory.

Boards (points 0..v-1, blocks = the design blocks):
  AG(3,2)  3-(8,4,1)     affine planes of F_2^3
  AG(4,2)  3-(16,4,1)    affine planes of F_2^4
  W_11     4-(11,5,1)    derived W_12 at a point
  W_12     5-(12,6,1)    supports of weight-6 words of the ternary Golay code
  W_22     3-(22,6,1)    derived W_23 at a point
  W_23     4-(23,7,1)    supports of weight-7 words of the binary Golay code
  W_24     5-(24,8,1)    supports of weight-8 words of the extended binary Golay code

All designs are verified from scratch (every t-subset in the right number of blocks).

Usage:
    python build_designs.py --out ../output
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent


# ---------------------------------------------------------------- F_2^11 ---
class GF2m:
    """GF(2^m) with the primitive polynomial given by its low-bit mask."""

    def __init__(self, m: int, poly: int):
        self.m = m
        self.mask = (1 << m) - 1
        self.poly = poly  # x^m + ... encoded as the low m bits

    def mul(self, a: int, b: int) -> int:
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if a & (1 << self.m):
                a ^= (1 << self.m) | self.poly
            a &= self.mask
        return r

    def pow(self, a: int, e: int) -> int:
        r = 1
        while e:
            if e & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            e >>= 1
        return r

    def order(self, a: int) -> int:
        q = (1 << self.m) - 1
        n = q
        for p in _prime_factors(n):
            while n % p == 0 and self.pow(a, n // p) == 1:
                n //= p
        return n


def _prime_factors(n: int) -> list[int]:
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def _poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] ^= x & y
    return out


# ---------------------------------------------------------------- GF(3^5) ---
class GF3m:
    def __init__(self, m: int, poly: list[int]):
        # poly = coefficients of x^m + ... (length m, low order first)
        self.m = m
        self.poly = poly
        self.q = 3 ** m

    def add(self, a: int, b: int) -> int:
        a0, a1 = a, b
        out = 0
        place = 1
        for _ in range(self.m):
            out += ((a0 % 3 + a1 % 3) % 3) * place
            a0 //= 3
            a1 //= 3
            place *= 3
        return out

    def sub(self, a: int, b: int) -> int:
        return self.add(a, self.neg(b))

    def neg(self, a: int) -> int:
        out, place = 0, 1
        for _ in range(self.m):
            out += ((-(a % 3)) % 3) * place
            a //= 3
            place *= 3
        return out

    def mul(self, a: int, b: int) -> int:
        da = [(a // 3 ** i) % 3 for i in range(self.m)]
        db = [(b // 3 ** i) % 3 for i in range(self.m)]
        prod = [0] * (2 * self.m - 1)
        for i in range(self.m):
            for j in range(self.m):
                prod[i + j] = (prod[i + j] + da[i] * db[j]) % 3
        # reduce modulo x^m + poly
        for i in range(2 * self.m - 2, self.m - 1, -1):
            c = prod[i]
            if c:
                prod[i] = 0
                for j, pj in enumerate(self.poly):
                    prod[i - self.m + j] = (prod[i - self.m + j] - c * pj) % 3
        out, place = 0, 1
        for i in range(self.m):
            out += prod[i] * place
            place *= 3
        return out

    def pow(self, a: int, e: int) -> int:
        r = 1
        while e:
            if e & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            e >>= 1
        return r

    def order(self, a: int) -> int:
        n = self.q - 1
        for p in _prime_factors(n):
            while n % p == 0 and self.pow(a, n // p) == 1:
                n //= p
        return n


def _int_to_field(x: int, m: int, p: int) -> list[int]:
    out = []
    for _ in range(m):
        out.append(x % p)
        x //= p
    return out


def cyclic_code_generator(F, n: int, qr: list[int], alpha: int, p: int):
    """Product over r in qr of (X - alpha^r), coefficients low->high.

    The arithmetic is performed IN the field F (field addition/subtraction and
    multiplication); because the root set is Frobenius-invariant, the final
    coefficients lie in the prime field and are returned as ints 0..p-1.
    """
    add = (lambda a, b: a ^ b) if p == 2 else F.add
    sub = (lambda a, b: a ^ b) if p == 2 else F.sub
    g = [1]  # field element 1
    for r in qr:
        root = F.pow(alpha, r)
        new = [0] * (len(g) + 1)
        for i, c in enumerate(g):
            new[i + 1] = add(new[i + 1], c)             # X * c X^i
            new[i] = sub(new[i], F.mul(c, root))        # -root * c X^i
        g = new
    out = []
    for c in g:
        assert c < p, (c, p)  # must lie in the prime field
        out.append(c)
    return out


def cyclic_words(g: list[int], n: int, k: int, p: int, F):
    """All p^k multiples of g modulo X^n - 1, as coefficient lists."""
    words = []
    for msg in range(p ** k):
        m = _int_to_field(msg, k, p)
        prod = [0] * (k + len(g) - 1)
        for i, a in enumerate(m):
            for j, b in enumerate(g):
                prod[i + j] = (prod[i + j] + a * b) % p
        # reduce modulo X^n - 1
        out = [0] * n
        for i, c in enumerate(prod):
            out[i % n] = (out[i % n] + c) % p
        words.append(out)
    return words


def weight_supports(words, w: int) -> list[frozenset[int]]:
    out = set()
    for word in words:
        nz = [i for i, c in enumerate(word) if c]
        if len(nz) == w:
            out.add(frozenset(nz))
    return sorted(out, key=lambda s: sorted(s))


def design_check(points: int, blocks: list[frozenset[int]], t: int, lam: int) -> dict:
    """Verify every t-subset lies in exactly lam blocks, and lambda_2, lambda_3."""
    counts = Counter()
    for B in blocks:
        for T in combinations(sorted(B), t):
            counts[T] += 1
    all_t = list(combinations(range(points), t))
    vals = {counts[T] for T in all_t}
    lam2 = None
    lam3 = None
    if t >= 2:
        c2 = Counter()
        for B in blocks:
            for T in combinations(sorted(B), 2):
                c2[T] += 1
        lam2 = sorted(set(c2.values()))
    if t >= 3:
        c3 = Counter()
        for B in blocks:
            for T in combinations(sorted(B), 3):
                c3[T] += 1
        lam3 = sorted(set(c3.values()))
    lam_by_t = {}
    for tt in range(2, min(5, len(blocks[0])) + 1):
        c = Counter()
        for B in blocks:
            for T in combinations(sorted(B), tt):
                c[T] += 1
        all_tt = list(combinations(range(points), tt))
        lam_by_t[tt] = sorted({c.get(T, 0) for T in all_tt})
    return {"v": points, "b": len(blocks), "k": len(blocks[0]),
            "t": t, "lambda_t": sorted(vals), "lambda_2": lam2, "lambda_3": lam3,
            "lambda_by_t": {str(k): v for k, v in lam_by_t.items()},
            "ok": vals == {lam}}


def ag_planes(d: int) -> tuple[int, list[frozenset[int]]]:
    v = 1 << d
    blocks = set()
    vecs = list(range(1, v))
    for a, b in combinations(vecs, 2):
        # directions a, b, a^b; skip if dependent (a==b or a^b==0 impossible)
        if a == b:
            continue
        proj = {0, a, b, a ^ b}
        if len(proj) != 4:
            continue
        # canonical direction space
        dirs = frozenset(proj)
        for x in range(v):
            blocks.add(frozenset(x ^ y for y in dirs))
    return v, sorted(blocks, key=lambda s: sorted(s))


def write_circle_file(path: Path, blocks, n: int) -> None:
    with path.open("w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(blocks)}\n")
        for B in blocks:
            fh.write(f"{len(B)} " + " ".join(str(x) for x in sorted(B)) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=EXP / "output")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    meta = {"experiment": "design-kyouen-witt-20261125", "designs": []}

    # ---- affine geometries ----
    for d, t, lam in [(3, 3, 1), (4, 3, 1)]:
        v, blocks = ag_planes(d)
        chk = design_check(v, blocks, t, lam)
        assert chk["ok"], chk
        write_circle_file(args.out / f"board_ag{d}2.txt", blocks, v)
        meta["designs"].append({"name": f"AG({d},2)", **chk,
                                "board": f"output/board_ag{d}2.txt"})

    # ---- binary Golay: W_23 and W_24 ----
    # GF(2^11), primitive polynomial x^11 + x^2 + 1 (mask 0b101)
    F2 = GF2m(11, 0b101)
    assert F2.order(2) == 2047, "x is not primitive"
    alpha23 = F2.pow(2, 89)  # order 23
    assert F2.order(alpha23) == 23
    qr23 = [1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18]
    g2 = cyclic_code_generator(F2, 23, qr23, alpha23, 2)  # length 12
    assert len(g2) == 12
    words23 = cyclic_words(g2, 23, 12, 2, F2)
    supports7 = weight_supports(words23, 7)
    assert len(supports7) == 253, len(supports7)
    chk23 = design_check(23, supports7, 4, 1)
    assert chk23["ok"] and chk23["lambda_3"] == [5], chk23
    write_circle_file(args.out / "board_w23.txt", supports7, 23)
    meta["designs"].append({"name": "W_23", **chk23, "board": "output/board_w23.txt"})

    # extended Golay: append parity bit
    ext = []
    for w in words23:
        ext.append(w + [sum(w) % 2])
    supports8 = []
    for w in ext:
        nz = [i for i, c in enumerate(w) if c]
        if len(nz) == 8:
            supports8.append(frozenset(nz))
    supports8 = sorted(set(supports8), key=lambda s: sorted(s))
    assert len(supports8) == 759, len(supports8)
    chk24 = design_check(24, supports8, 5, 1)
    assert chk24["ok"], chk24
    write_circle_file(args.out / "board_w24.txt", supports8, 24)
    meta["designs"].append({"name": "W_24", **chk24, "board": "output/board_w24.txt"})

    # W_22 = derived W_23 at point 22 (block containing 22, remove 22)
    derived22 = [frozenset(B - {22}) for B in supports7 if 22 in B]
    derived22 = sorted(set(derived22), key=lambda s: sorted(s))
    assert len(derived22) == 77, len(derived22)
    chk22 = design_check(22, derived22, 3, 1)
    assert chk22["ok"], chk22
    write_circle_file(args.out / "board_w22.txt", derived22, 22)
    meta["designs"].append({"name": "W_22", **chk22, "board": "output/board_w22.txt"})

    # ---- ternary Golay: W_12 ----
    # GF(3^5), primitive polynomial x^5 + 2x + 1 == x^5 + 2x + 1 (coeffs low->high)
    for poly in ([1, 2, 0, 0, 0], [1, 1, 0, 0, 0], [2, 1, 2, 2, 2], [1, 2, 2, 2, 2]):
        try:
            F3 = GF3m(5, poly)
            if F3.order(3) == 242:
                break
        except Exception:
            continue
    else:
        raise AssertionError("no primitive polynomial found")
    alpha11 = F3.pow(3, 22)  # order 11
    assert F3.order(alpha11) == 11
    qr11 = [1, 3, 4, 5, 9]
    g3 = cyclic_code_generator(F3, 11, qr11, alpha11, 3)
    assert len(g3) == 6, g3
    words11 = cyclic_words(g3, 11, 6, 3, F3)
    # extend to length 12 with the negated sum (self-dual ternary Golay)
    ext3 = []
    for w in words11:
        ext3.append(w + [(-sum(w)) % 3])
    supports6 = []
    for w in ext3:
        nz = [i for i, c in enumerate(w) if c]
        if len(nz) == 6:
            supports6.append(frozenset(nz))
    supports6 = sorted(set(supports6), key=lambda s: sorted(s))
    assert len(supports6) == 132, len(supports6)
    chk12 = design_check(12, supports6, 5, 1)
    assert chk12["ok"], chk12
    write_circle_file(args.out / "board_w12.txt", supports6, 12)
    meta["designs"].append({"name": "W_12", **chk12, "board": "output/board_w12.txt"})

    # W_11 = derived W_12 at point 11
    derived11 = [frozenset(B - {11}) for B in supports6 if 11 in B]
    derived11 = sorted(set(derived11), key=lambda s: sorted(s))
    assert len(derived11) == 66, len(derived11)
    chk11 = design_check(11, derived11, 4, 1)
    assert chk11["ok"], chk11
    write_circle_file(args.out / "board_w11.txt", derived11, 11)
    meta["designs"].append({"name": "W_11", **chk11, "board": "output/board_w11.txt"})

    (args.out / "designs_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    for d in meta["designs"]:
        print(f"{d['name']}: v={d['v']} b={d['b']} k={d['k']} "
              f"lambda2={d['lambda_2']} lambda3={d['lambda_3']} ok={d['ok']}")


if __name__ == "__main__":
    main()
