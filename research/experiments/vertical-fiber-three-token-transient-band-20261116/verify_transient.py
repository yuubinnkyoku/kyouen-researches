#!/usr/bin/env python3
"""3トークン過渡帯 (c = R-2x <= -1 スライス) と対角線 OK 表の独立検証器。

K0832 残余ゲーム H(R;X;z) (κ=1) の2つの有限族について値2位置を検査する。

A. 3トークン族 X=(x,y,w)、x = y+w+z+j、R = 2x-(2k+1) の過渡帯スライス。

   予想U (k>=1): 帯条件 (R > x, R > z+1, R < S+z+2) 内で
     H(R;(x,y,w);z) = 2  <=>
       (j=0, w=1):  z >= 2k
       (その他):     2(k+1-j-w) <= z <= 2(k+1-j-w)+1   (下端負なら不成立)

   予想A/B/C (k=0, R=2x-1):
     A: j=0 (x=y+w+z)   -> 帯内で常に値2
     B: j=2 (x=y+w+z+2) -> 帯内で常に値2
     C: j=1 -> z=0 のみ値2、z>=1 は帯内で全fail、j>=3 は帯内に存在しない

B. 対角線 2*x_max = S+z、R = 2*x_max-1 における OK 表 (m=|X|)。
   X = (x_max,) + rest、x_max = sum(rest)+z と置いたとき:
     m=2: OK <=> z == 1
     m=3: OK <=> True (全OK)
     m=4: OK <=> (z==0 ∧ (rest[:2]≠(1,1) ∨ rest==(1,1,1))) ∨ (z==1 ∧ rest[:2]==(1,1))
     m=5: OK <=> rest[:3]==(1,1,1)
     m=6: OK <=> (z==1 ∧ rest[:4]==(1,1,1,1)) ∨
               (z==0 ∧ rest[:2]==(1,1) ∧ ((rest[:3]==(1,1,1) ∧ rest[3]==2) ∨ (rest[2]==2 ∧ rest[3]==2)))
     m=7: OK <=> rest[:5]==(1,1,1,1,1)
     m=8: OK <=> (rest==(1,)*7 ∧ z∈{0,1}) ∨ (z==1 ∧ rest[:6]==(1,)*6) ∨
               (z==0 ∧ ((rest[:5]==(1,)*5 ∧ rest[5]==2) ∨ (rest[:4]==(1,)*4 ∧ rest[4]==2 ∧ rest[5]==2)))
   これらは抽出範囲内の有限観察(全称予想としての一般化はレポート参照)。

2エンジン: cap付き正準多重集合 Hc と capなし順序ラベル Hn の相互照合。
決定的出力: output/audit.json (二回実行で byte-identical)。
"""
import json
import sys
from itertools import combinations_with_replacement

sys.setrecursionlimit(1000000)

# ---- engine A: cap付き正準多重集合 ----
memo_c = {}


def cap(X, c):
    return tuple(sorted(min(t, c) for t in X))


def Hc(R, X, z):
    if R == 0:
        return 0
    X = cap(X, R + 1)
    key = (R, X, z)
    v = memo_c.get(key)
    if v is not None:
        return v
    Xc = cap(X, R)
    opts = set()
    seen = set()
    for i, t in enumerate(Xc):
        if t in seen:
            continue
        seen.add(t)
        if t >= 2:
            child = Xc[:i] + (t - 1,) + Xc[i + 1:]
            opts.add(Hc(R - 1, cap(child, R - 1), z))
        else:
            child = Xc[:i] + Xc[i + 1:]
            opts.add(Hc(R - 1, cap(child, R - 1), z + 1))
    if z >= 1:
        opts.add(1 ^ Hc(R - 1, Xc, z - 1))
    g = 0
    while g in opts:
        g += 1
    memo_c[key] = g
    return g


# ---- engine B: capなし順序ラベル (独立実装) ----
memo_n = {}


def Hn(R, X, z):
    """X はラベル付き tuple。同一値の手は同一の子値を与えるため1回だけ展開。"""
    if R == 0:
        return 0
    key = (R, X, z)
    v = memo_n.get(key)
    if v is not None:
        return v
    opts = set()
    prev = None
    for i, t in enumerate(X):
        if t == prev:
            continue
        prev = t
        if t >= 2:
            opts.add(Hn(R - 1, X[:i] + (t - 1,) + X[i + 1:], z))
        else:
            opts.add(Hn(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ Hn(R - 1, X, z - 1))
    g = 0
    while g in opts:
        g += 1
    memo_n[key] = g
    return g


def H2(R, X, z):
    """2エンジン照合付きの値。不一致なら例外。"""
    a = Hc(R, X, z)
    b = Hn(R, tuple(sorted(X)), z)
    if a != b:
        raise AssertionError(f"engine mismatch R={R} X={X} z={z}: {a} vs {b}")
    return a


def band(R, x, rest, z):
    S = x + sum(rest)
    return R > x and R > z + 1 and R < S + z + 2


def pred_U(k, j, w, z):
    if j == 0 and w == 1:
        return z >= 2 * k
    lo = 2 * (k + 1 - j - w)
    return lo <= z <= lo + 1


def pred_diag(m, rest, z):
    rest = tuple(rest)
    if m == 2:
        return z == 1
    if m == 3:
        return True
    if m == 4:
        if z == 0:
            return rest[:2] != (1, 1) or rest == (1, 1, 1)
        if z == 1:
            return rest[:2] == (1, 1)
        return False
    if m == 5:
        return rest[:3] == (1, 1, 1)
    if m == 6:
        if z == 1:
            return rest[:4] == (1, 1, 1, 1)
        if z == 0:
            return rest[:2] == (1, 1) and (
                (rest[:3] == (1, 1, 1) and rest[3] == 2) or (rest[2] == 2 and rest[3] == 2))
        return False
    if m == 7:
        return rest[:5] == (1, 1, 1, 1, 1)
    if m == 8:
        if rest == (1,) * 7:
            return z in (0, 1)
        if z == 1:
            return rest[:6] == (1,) * 6
        if z == 0:
            return (rest[:5] == (1,) * 5 and rest[5] == 2) or (
                rest[:4] == (1,) * 4 and rest[4] == 2 and rest[5] == 2)
        return False
    return None


def main():
    audit = {"schema": "three-token-transient-band-20261116-v1", "checks": []}

    def add(name, n, bad):
        audit["checks"].append({"name": name, "cases": n, "mismatches": bad})

    # ---- E1: 予想U 双方向 (k=1,2,3) ----
    for K in (1, 2, 3):
        n = bad = 0
        for y in range(1, 14):
            for w in range(1, min(y, 6) + 1):
                for z in range(0, 16):
                    for j in range(0, 8):
                        x = y + w + z + j
                        if x < y:
                            continue
                        R = 2 * x - (2 * K + 1)
                        if not band(R, x, (y, w), z):
                            continue
                        n += 1
                        h = H2(R, (x, y, w), z)
                        if pred_U(K, j, w, z) != (h == 2):
                            bad += 1
        add(f"E1:conjecture-U-k{K}", n, bad)

    # ---- E2: 予想A/B/C (k=0) ----
    n = bad = 0
    for y in range(1, 18):
        for w in range(1, min(y, 12) + 1):
            for z in range(0, 20):
                base = y + w + z
                for j in ([0, 2] if z > 0 else [0, 1, 2]):
                    x = base + j
                    if x < y:
                        continue
                    R = 2 * x - 1
                    if not band(R, x, (y, w), z):
                        continue
                    n += 1
                    h = H2(R, (x, y, w), z)
                    pred = (j in (0, 2)) or (j == 1 and z == 0)
                    if pred != (h == 2):
                        bad += 1
    add("E2:conjecture-ABC-k0", n, bad)

    n2 = bad2 = 0
    for y in range(1, 14):
        for w in range(1, y + 1):
            for z in range(1, 14):
                x = y + w + z + 1
                if x < y:
                    continue
                R = 2 * x - 1
                if not band(R, x, (y, w), z):
                    continue
                n2 += 1
                if H2(R, (x, y, w), z) == 2:
                    bad2 += 1
    add("E2b:conjecture-C-negative", n2, bad2)

    n3 = 0
    for y in range(1, 10):
        for w in range(1, y + 1):
            for z in range(0, 10):
                for j in (3, 4):
                    x = y + w + z + j
                    R = 2 * x - 1
                    if band(R, x, (y, w), z):
                        n3 += 1
    add("E2c:k0-band-above-e2-empty", n3, n3)

    # ---- E3: 対角線 OK 表 m=2..8 双方向 ----
    grids = (
        (2, 7, 9), (3, 7, 9), (4, 7, 9), (5, 7, 9),
        (6, 6, 9), (7, 4, 9), (8, 3, 6),
    )
    for m, tmax, zmax in grids:
        n = bad = 0
        for rest in combinations_with_replacement(range(1, tmax + 1), m - 1):
            for z in range(0, zmax + 1):
                x = sum(rest) + z
                if x < rest[-1]:
                    continue
                R = 2 * x - 1
                if not band(R, x, rest, z):
                    continue
                n += 1
                h = H2(R, (x,) + tuple(rest), z)
                if pred_diag(m, rest, z) != (h == 2):
                    bad += 1
        add(f"E3:diag-m{m}", n, bad)

    # ---- E4: m=3 全OK (別グリッド・広い) ----
    n = bad = 0
    for y in range(1, 18):
        for w in range(1, min(y, 12) + 1):
            for z in range(0, 20):
                x = y + w + z
                if x < y:
                    continue
                R = 2 * x - 1
                if not band(R, x, (y, w), z):
                    continue
                n += 1
                if H2(R, (x, y, w), z) != 2:
                    bad += 1
    add("E4:m3-always-OK", n, bad)

    # ---- E5: エンジン相互照合 (決定的線形合同列) ----
    n = bad = 0
    r = 12345
    for _ in range(400):
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        y = 1 + (r % 16)
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        w = 1 + (r % y)
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        z = (r % 18)
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        j = (r % 8) - 2
        x = max(y, y + w + z + j)
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        k = (r % 4)
        R = 2 * x - (2 * k + 1)
        if R < 0:
            continue
        n += 1
        a = Hc(R, (x, y, w), z)
        b = Hn(R, (w, y, x), z)  # 逆順ラベルでも同一値
        b2 = Hn(R, tuple(sorted((x, y, w))), z)
        if a != b or a != b2:
            bad += 1
    add("E5:engine-cross", n, bad)

    # ---- E6: 正規化エッジ (トークン順序に依らない予想U) ----
    n = bad = 0
    for (X, z) in (((4, 2, 1), 1), ((4, 2, 1), 2), ((4, 2, 1), 3),
                   ((5, 2, 1), 1), ((5, 2, 1), 2), ((6, 3, 1), 2), ((7, 4, 1), 3)):
        x, y, w = X
        j = x - (y + w + z)
        if j < 0:
            continue
        R = 2 * x - 3
        if not band(R, x, (y, w), z):
            continue
        n += 1
        h = H2(R, X, z)
        if pred_U(1, j, w, z) != (h == 2):
            bad += 1
    add("E6:normalization-edge", n, bad)

    total_cases = sum(c["cases"] for c in audit["checks"])
    total_bad = sum(c["mismatches"] for c in audit["checks"])
    audit["total_cases"] = total_cases
    audit["total_mismatches"] = total_bad
    audit["status"] = "PASS" if total_bad == 0 else "FAIL"
    with open("output/audit.json", "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
    print(json.dumps(audit, indent=1, sort_keys=True))
    return 0 if total_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
