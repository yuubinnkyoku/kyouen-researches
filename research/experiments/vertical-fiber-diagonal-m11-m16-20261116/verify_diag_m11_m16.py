#!/usr/bin/env python3
"""対角線OK表の m=11..16 外挿検証器: 奇数族・偶数統一形（mod 4修正）・all-ones族プロファイル。

前報 verify_transient.py (m=2..8)・verify_extension.py (m=9,10・偶数統一形) の拡張として次を検査する。

D1: m=11 奇数族。予想: OK <=> rest[:9]==(1^9) (z 任意)。
    広域抽出 tmax=4, zmax=9 の完全双方向。
D1b: m=11 高z。族 (1^9,t) の陽性 (z=10..20)・族外 (1^8,2,2)/(1^7,2,2,2) の陰性。
D2: m=12 偶数。修正統一形: z=1: rest[:10]==(1^10)、
    z=0: c1=(rest[:9]==(1^9)∧rest[9]==2) ∨ c2=(rest[:8]==(1^8)∧rest[8]==2∧rest[9]==2)
          ∨ [m≡0 (mod 4) で rest==(1^11)]、z>=2: なし。tmax=4 の完全双方向。
D2b: m=12 z>=2 不在 (tmax=3, z=2..4) + 族形状 (1^10,t) の z=5..8 陰性。
D3: m=13 奇数族。OK <=> rest[:11]==(1^11)。tmax=4, zmax=9 の完全双方向。
D3b: m=13 高z陽性・族外陰性。
D4: m=14 偶数 (m≡2 mod 4 → all-ones特例なし)。tmax=4, z=0,1 の完全双方向。
D4b: m=14 z>=2 不在 (tmax=3, z=2..4) + 族形状 z=5..8 陰性。
D5: m=15 奇数族。OK <=> rest[:13]==(1^13)。tmax=3, zmax=6 の完全双方向 + 高z。
D6: m=16 偶数 (m≡0 mod 4 → all-ones特例あり)。tmax=3, z=0..2 の完全双方向。
D7: all-ones単一族プロファイル。H(2k−1;(k,1^k);0) は k=1..25 で
    k≡1 (mod 4) のとき 1、それ以外で 2（値2 ⟺ k≢1 (mod 4)）。
D8: 修正統一形の既存点の再監査。m=6 (tmax=6,z<=9)・m=8 (tmax=3,z<=6)・
    m=10 (tmax=4,z=0,1) を修正統一形で完全双方向。
D9: エンジン相互照合 (決定的線形合同列・m=11..16 の対角線・120件)。

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


def clear_memos():
    """グループ間でメモを解放する（値に影響しない・メモリ上限対策）。"""
    memo_c.clear()
    memo_n.clear()


def H2(R, X, z):
    a = Hc(R, X, z)
    b = Hn(R, tuple(sorted(X)), z)
    if a != b:
        raise AssertionError(f"engine mismatch R={R} X={X} z={z}: {a} vs {b}")
    return a


def band(R, x, rest, z):
    S = x + sum(rest)
    return R > x and R > z + 1 and R < S + z + 2


def pred_odd(m, rest, z):
    """奇数族予想: OK <=> rest[:m-2]==(1^{m-2}) (z 任意)。"""
    return tuple(rest)[:m - 2] == (1,) * (m - 2)


def pred_even_refined(m, rest, z):
    """偶数修正統一形 (m=2r>=6):
    z=1: rest[:2r-2]==(1^{2r-2})、
    z=0: c1 ∨ c2 ∨ [m≡0 (mod 4) かつ rest==(1^{2r-1})]、
    z>=2: なし。
    旧統一形の m==8 ハードコード特例を m≡0 (mod 4) に一般化したもの。
    """
    r = m // 2
    rest = tuple(rest)
    if z == 1:
        return rest[:2 * r - 2] == (1,) * (2 * r - 2)
    if z == 0:
        c1 = rest[:2 * r - 3] == (1,) * (2 * r - 3) and rest[2 * r - 3] == 2
        c2 = (rest[:2 * r - 4] == (1,) * (2 * r - 4) and rest[2 * r - 4] == 2
              and rest[2 * r - 3] == 2)
        ok = c1 or c2
        if m % 4 == 0:
            ok = ok or rest == (1,) * (m - 1)
        return ok
    return False


def diag_bidirectional(m, tmax, zvals, pred, name, audit, verbose_positives=False):
    """対角線 R=2x−1・x=sum(rest)+z の全グリッド双方向照合。"""
    n = bad = 0
    for rest in combinations_with_replacement(range(1, tmax + 1), m - 1):
        for z in zvals:
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            h = H2(R, (x,) + tuple(rest), z)
            if (h == 2) != pred(m, rest, z):
                bad += 1
                print(f"VIOLATION {name}: rest={rest} z={z} h={h}", flush=True)
    return n, bad


def add(audit, name, n, bad):
    audit["checks"].append({"name": name, "cases": n, "mismatches": bad})
    print(f"{name}: cases={n} mismatches={bad}", flush=True)


def main():
    audit = {"schema": "diagonal-m11-m16-20261116-v1", "checks": []}

    zr = lambda lo, hi: range(lo, hi + 1)

    clear_memos()
    # ---- D1/D1b: m=11 奇数族 ----
    n, bad = diag_bidirectional(11, 4, zr(0, 9), pred_odd, "D1", audit)
    add(audit, "D1:diag-m11-odd-wide", n, bad)

    n = bad = 0
    for t in range(1, 5):
        rest = (1,) * 9 + (t,)
        for z in zr(10, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) != 2:
                bad += 1
                print(f"m11 highz family negative: t={t} z={z}", flush=True)
    add(audit, "D1b:diag-m11-highz-family", n, bad)

    n = bad = 0
    for rest in [(1,) * 8 + (2, 2), (1,) * 7 + (2, 2, 2)]:
        for z in zr(10, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) == 2:
                bad += 1
                print(f"m11 highz negative positive: {rest[-1]} z={z}", flush=True)
    add(audit, "D1b:diag-m11-highz-negatives", n, bad)

    clear_memos()
    # ---- D2/D2b: m=12 偶数 (m≡0 mod 4 → all-ones特例) ----
    n, bad = diag_bidirectional(12, 4, (0, 1), pred_even_refined, "D2", audit)
    add(audit, "D2:diag-m12-even-z01", n, bad)

    n = bad = 0
    for rest in combinations_with_replacement(range(1, 4), 11):
        for z in zr(2, 4):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + tuple(rest), z) == 2:
                bad += 1
                print(f"m12 z>=2 positive: {rest} z={z}", flush=True)
    add(audit, "D2b:diag-m12-z2-absence", n, bad)

    n = bad = 0
    for t in range(1, 4):
        rest = (1,) * 10 + (t,)
        for z in zr(5, 8):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) == 2:
                bad += 1
                print(f"m12 family-shape z>=5 positive: t={t} z={z}", flush=True)
    add(audit, "D2b:diag-m12-family-z5-8-negative", n, bad)

    clear_memos()
    # ---- D3/D3b: m=13 奇数族 ----
    n, bad = diag_bidirectional(13, 4, zr(0, 9), pred_odd, "D3", audit)
    add(audit, "D3:diag-m13-odd-wide", n, bad)

    n = bad = 0
    for t in range(1, 5):
        rest = (1,) * 11 + (t,)
        for z in zr(10, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) != 2:
                bad += 1
                print(f"m13 highz family negative: t={t} z={z}", flush=True)
    add(audit, "D3b:diag-m13-highz-family", n, bad)

    n = bad = 0
    for rest in [(1,) * 10 + (2, 2), (1,) * 9 + (2, 2, 2)]:
        for z in zr(10, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) == 2:
                bad += 1
                print(f"m13 highz negative positive: z={z}", flush=True)
    add(audit, "D3b:diag-m13-highz-negatives", n, bad)

    clear_memos()
    # ---- D4/D4b: m=14 偶数 (m≡2 mod 4 → 特例なし) ----
    n, bad = diag_bidirectional(14, 4, (0, 1), pred_even_refined, "D4", audit)
    add(audit, "D4:diag-m14-even-z01", n, bad)

    n = bad = 0
    for rest in combinations_with_replacement(range(1, 4), 13):
        for z in zr(2, 4):
            x = sum(rest) + z
            if x < rest[-1]:
                continue
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + tuple(rest), z) == 2:
                bad += 1
                print(f"m14 z>=2 positive: {rest} z={z}", flush=True)
    add(audit, "D4b:diag-m14-z2-absence", n, bad)

    n = bad = 0
    for t in range(1, 4):
        rest = (1,) * 12 + (t,)
        for z in zr(5, 8):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) == 2:
                bad += 1
                print(f"m14 family-shape z>=5 positive: t={t} z={z}", flush=True)
    add(audit, "D4b:diag-m14-family-z5-8-negative", n, bad)

    clear_memos()
    # ---- D5: m=15 奇数族 (tmax=3, z<=6 + 高z) ----
    n, bad = diag_bidirectional(15, 3, zr(0, 6), pred_odd, "D5", audit)
    add(audit, "D5:diag-m15-odd-wide", n, bad)

    n = bad = 0
    for t in range(1, 4):
        rest = (1,) * 13 + (t,)
        for z in zr(7, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) != 2:
                bad += 1
                print(f"m15 highz family negative: t={t} z={z}", flush=True)
    add(audit, "D5b:diag-m15-highz-family", n, bad)

    n = bad = 0
    for rest in [(1,) * 12 + (2, 2), (1,) * 11 + (2, 2, 2)]:
        for z in zr(7, 20):
            x = sum(rest) + z
            R = 2 * x - 1
            if not band(R, x, rest, z):
                continue
            n += 1
            if H2(R, (x,) + rest, z) == 2:
                bad += 1
                print(f"m15 highz negative positive: z={z}", flush=True)
    add(audit, "D5b:diag-m15-highz-negatives", n, bad)

    clear_memos()
    # ---- D6: m=16 偶数 (m≡0 mod 4 → all-ones特例) tmax=3, z=0..2 ----
    n, bad = diag_bidirectional(16, 3, zr(0, 2), pred_even_refined, "D6", audit)
    add(audit, "D6:diag-m16-even-z012", n, bad)

    clear_memos()
    # ---- D7: all-ones単一族プロファイル ----
    n = bad = 0
    for k in range(1, 26):
        R = 2 * k - 1
        h = H2(R, (k,) + (1,) * k, 0)
        n += 1
        want = 1 if k % 4 == 1 else 2
        if h != want:
            bad += 1
            print(f"all-ones family profile mismatch: k={k} h={h} want={want}",
                  flush=True)
    add(audit, "D7:all-ones-family-profile-k1-25", n, bad)

    clear_memos()
    # ---- D8: 修正統一形の既存点の再監査 (m=6,8,10) ----
    for m, tmax, zvals in ((6, 6, zr(0, 9)), (8, 3, zr(0, 6)), (10, 4, (0, 1))):
        clear_memos()
        n, bad = diag_bidirectional(m, tmax, zvals, pred_even_refined,
                                    f"D8-m{m}", audit)
        add(audit, f"D8:diag-m{m}-refined-uniform-reaudit", n, bad)

    clear_memos()
    # ---- D9: エンジン相互照合 (決定的線形合同列・m=11..16 対角線) ----
    n = bad = 0
    r = 13571113
    for _ in range(120):
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        m = 11 + (r % 6)  # m=11..16
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        tmax = 1 + (r % 2)
        rest = []
        for _ in range(m - 1):
            r = (r * 1103515245 + 12345) & 0x7FFFFFFF
            rest.append(1 + (r % tmax))
        rest = tuple(sorted(rest))
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        z = r % 7
        x = sum(rest) + z
        if x < rest[-1]:
            continue
        R = 2 * x - 1
        if not band(R, x, rest, z):
            continue
        n += 1
        a = Hc(R, (x,) + rest, z)
        b = Hn(R, tuple(reversed((x,) + rest)), z)
        b2 = Hn(R, (x,) + rest, z)
        if a != b or a != b2:
            bad += 1
    add(audit, "D9:engine-cross-diagonal-m11-16", n, bad)

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
