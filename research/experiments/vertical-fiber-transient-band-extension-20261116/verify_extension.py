#!/usr/bin/env python3
"""3トークン過渡帯の拡張検証器: 予想Uのk=4..8、対角線OK表のm=9/m=10、偶数統一形。

前報 verify_transient.py (m=2..8・k=1..3) の拡張として次を検査する。

G1: 予想U (k>=1) を k=4..8 に拡張した全グリッド双方向照合。
    予想U: 帯条件 (R>x, R>z+1, R<S+z+2) 内で
      H(R;(x,y,w);z)=2  <=>  (j=0,w=1: z>=2k) or (lo<=z<=lo+1, lo=2(k+1-j-w))

G2: 対角線OK表 m=9。予想: OK <=> rest[:7]==(1,)*(7) (z 任意)。
    広域抽出 tmax=4, zmax=9 の完全双方向 + 族の高z陽性 (z<=20)。

G3: 対角線OK表 m=10。予想:
      z=1: OK <=> rest[:8]==(1,)*(8)
      z=0: OK <=> (rest[:7]==(1^7)∧rest[7]==2) ∨ (rest[:6]==(1^6)∧rest[6]==2∧rest[7]==2)
      z>=2: OK なし
    抽出 tmax=4 (z=0,1)・tmax=3 (z=2..4) の完全双方向。

G4: 偶数統一形と既存OK表の同値性。m=2r>=6 について
      z=1:  OK <=> rest[:2r-2]==(1^{2r-2})
      z=0:  OK <=> (rest[:2r-3]==(1^{2r-3})∧rest[2r-3]==2)
                  ∨ (rest[:2r-4]==(1^{2r-4})∧rest[2r-4]==2∧rest[2r-3]==2)
                  [m==8 のみ追加特例 rest==(1^7)]
      z>=2: OK なし
    が m=6 (tmax=6, zmax=9)・m=8 (tmax=3, zmax=6) の既存OK表と全グリッドで同値、
    かつ m=10 (tmax=4) の実際のHと双方向一致すること。

2エンジン: cap付き正準多重集合 Hc と capなし順序ラベル Hn の相互照合 (前報と同一)。
決定的出力: output/audit.json (二回実行で byte-identical)。
"""
import json
import sys
from itertools import combinations_with_replacement

sys.setrecursionlimit(1000000)
sys.path.insert(0, sys.path[0] if __name__ != "__main__" else ".")


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


def pred_even_uniform(m, rest, z):
    """m=2r>=6 の統一形 (m=4,2 は含まない。m==8 のみ特例付き)。"""
    r = m // 2
    rest = tuple(rest)
    if z == 1:
        return rest[:2 * r - 2] == (1,) * (2 * r - 2)
    if z == 0:
        c1 = rest[:2 * r - 3] == (1,) * (2 * r - 3) and rest[2 * r - 3] == 2
        c2 = (rest[:2 * r - 4] == (1,) * (2 * r - 4) and rest[2 * r - 4] == 2
              and rest[2 * r - 3] == 2)
        ok = c1 or c2
        if m == 8:
            ok = ok or rest == (1,) * 7
        return ok
    return False


def pred_m9(rest, z):
    return tuple(rest)[:7] == (1,) * 7


def pred_m10(rest, z):
    rest = tuple(rest)
    if z == 1:
        return rest[:8] == (1,) * 8
    if z == 0:
        c1 = rest[:7] == (1,) * 7 and rest[7] == 2
        c2 = rest[:6] == (1,) * 6 and rest[6] == 2 and rest[7] == 2
        return c1 or c2
    return False


def main():
    audit = {"schema": "transient-band-extension-20261116-v1", "checks": []}

    def add(name, n, bad):
        audit["checks"].append({"name": name, "cases": n, "mismatches": bad})
        print(f"{name}: cases={n} mismatches={bad}", flush=True)

    # ---- G1: 予想U k=4..8 ----
    for K in range(4, 9):
        n = bad = 0
        for y in range(1, 14):
            for w in range(1, min(y, 6) + 1):
                for z in range(0, 16):
                    for j in range(0, 8):
                        x = y + w + z + j
                        R = 2 * x - (2 * K + 1)
                        if not band(R, x, (y, w), z):
                            continue
                        n += 1
                        h = H2(R, (x, y, w), z)
                        if pred_U(K, j, w, z) != (h == 2):
                            bad += 1
        add(f"G1:conjecture-U-k{K}", n, bad)

    # ---- G2: m=9 広域双方向 (tmax=4, zmax=9) ----
    n = bad = 0
    for rest in combinations_with_replacement(range(1, 5), 8):
        for z in range(0, 10):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            h = H2(R, (x,) + tuple(rest), z)
            if pred_m9(rest, z) != (h == 2):
                bad += 1
    add("G2:diag-m9-wide", n, bad)

    # 族の高z陽性 (z<=20)
    n2 = bad2 = 0
    for last in range(1, 5):
        rest = (1,) * 7 + (last,)
        for z in range(10, 21):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n2 += 1
            if H2(R, (x,) + rest, z) != 2:
                bad2 += 1
    add("G2b:diag-m9-highz-family", n2, bad2)

    # ---- G3: m=10 ----
    n = bad = 0
    for rest in combinations_with_replacement(range(1, 5), 9):
        for z in (0, 1):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            h = H2(R, (x,) + tuple(rest), z)
            if pred_m10(rest, z) != (h == 2):
                bad += 1
    add("G3:diag-m10-z01", n, bad)

    n2 = bad2 = 0
    for rest in combinations_with_replacement(range(1, 4), 9):
        for z in range(2, 5):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n2 += 1
            if H2(R, (x,) + tuple(rest), z) == 2:
                bad2 += 1
    add("G3b:diag-m10-z2-absence", n2, bad2)

    # ---- G4: 偶数統一形の双方向 (m=6,10) と既存表との同値性 (m=6,8) ----
    for m, tmax, zmax in ((6, 6, 9), (8, 3, 6)):
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
                if pred_even_uniform(m, rest, z) != (h == 2):
                    bad += 1
        add(f"G4:diag-m{m}-uniform", n, bad)

    # m=10 の統一形 vs pred_m10 同値性 (定義上同じだが転写検査)
    n = bad = 0
    for rest in combinations_with_replacement(range(1, 5), 9):
        for z in (0, 1):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if pred_even_uniform(10, rest, z) != pred_m10(rest, z):
                bad += 1
    add("G4b:m10-uniform-vs-table", n, bad)

    # ---- G5: エンジン相互照合 (決定的線形合同列・広いパラメータ) ----
    n = bad = 0
    r = 67890
    for _ in range(300):
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        m = 2 + (r % 9)  # m=2..10
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        tmax = 1 + (r % 4)
        rest = []
        for _ in range(m - 1):
            r = (r * 1103515245 + 12345) & 0x7FFFFFFF
            rest.append(1 + (r % tmax))
        rest = tuple(sorted(rest))
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        z = r % 12
        x = sum(rest) + z
        if x < rest[-1]:
            continue
        R = 2 * x - 1
        if not band(R, x, rest, z):
            continue
        n += 1
        a = Hc(R, (x,) + rest, z)
        b = Hn(R, tuple(reversed((x,) + rest)), z)
        b2 = Hn(R, ((x,) + rest), z)
        if a != b or a != b2:
            bad += 1
    add("G5:engine-cross-diagonal", n, bad)

    total_cases = sum(c["cases"] for c in audit["checks"])
    total_bad = sum(c["mismatches"] for c in audit["checks"])
    audit["total_cases"] = total_cases
    audit["total_mismatches"] = total_bad
    audit["status"] = "PASS" if total_bad == 0 else "FAIL"
    with open("output/audit.json", "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True)
    print(json.dumps({"total_cases": total_cases,
                      "total_mismatches": total_bad,
                      "status": audit["status"]}, indent=1))
    return 0 if total_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
