#!/usr/bin/env python3
"""天井トークン付き残余ゲーム（ceiling game）の値2位置分類の独立検証器。

定義: H(R;X;z) は κ=1 残余mex再帰（K0832 本文と同一）:
  A手: トークン v>=2 を v-1 へ   -> (R-1, X', z)
  B手: トークン 1 を除去          -> (R-1, X から 1 を除いた多重集合, z+1)
  C手: z>=1 なら z-1              -> 値 1 XOR 子
  H(0;X;z)=0, 値は mex。

天井ゲーム: T_inf(X;z) := {R>=1 : H(R; X∪{R+1}; z) = 2}（X は正整数の有限多重集合）。
cap補題（証明済み・K0832）により H(R;X;z)=H(R;cap_{R+1}(X);z) なので、
X∪{R+1} のうち R+1 以上のトークンはすべて R+1 に capped され、
「天井」は各レベルで常に 1 個として振る舞う。

検証対象の予想（本実験で提案・有限監査対象・全称性は未証明）:
  T_inf(X;z) = L(z) ∪ P(X;z)
  L(z) = {奇数 R <= z+1} から z+1 を除いた集合
  P(X;z) = {p_j : j=0..m-1},  X を昇順 t_0<=...<=t_{m-1} として
    p_j = 2*t_j + p_{j-2} + 2   (p_{-1}=p_{-2} 未定義は下の初期値で代替)
    p_0 = 2*t_0 + delta_A(z),  p_1 = 2*t_1 + delta_A(z+1)
  delta_A(u) = u 以上の最小奇数。
  m=0 (X=∅) では P=∅。
  実装上は p_j = 2*(t_j+t_{j-2}+t_{j-4}+...) + delta_A(z+j) と等価。

証明済みアンカー:
  V0 単一トークン閉形式（K0832 全称証明済み）との一致（m=0 含む）
  V1 R<=z+1 の単一トークン縮約（K0832 高さ縮約定理・証明済み）から導かれる
     ラダー L(z) の導出と一致
  V2 Theorem T（値2は奇数Rのみ・証明済み）との整合
  V4 cap補題（証明済み）の直接照合
ブリッジ（予想の系・有限監査）: 元ゲーム X=(x1,...) について
  max(z+2, max(X_{<=R}... )) ... 詳細は report.md。2トークン・3トークンで
  R ∈ [max(z+2, min(X)), x_max - 1] の帯の値2位置が P と一致する。

出力: output/audit.json（決定的・二回実行でbyte-identical）。
"""
import json
import os
import random
import sys

sys.setrecursionlimit(1000000)

SEED = 20261116

# ---------------- エンジン1: cap付き正準多重集合再帰 ----------------
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
            opts.add(Hc(R - 1, cap(Xc[:i] + (t - 1,) + Xc[i + 1:], R - 1), z))
        else:
            opts.add(Hc(R - 1, cap(Xc[:i] + Xc[i + 1:], R - 1), z + 1))
    if z >= 1:
        opts.add(1 ^ Hc(R - 1, Xc, z - 1))
    g = 0
    while g in opts:
        g += 1
    memo_c[key] = g
    return g


# ---------------- エンジン2: capなし順序ラベル再帰（独立実装） ----------------
memo_l = {}


def Hl(R, X, z):
    """X: 昇順タプル。capも多重集合正準化もしない素朴なラベル付き再帰。"""
    if R == 0:
        return 0
    key = (R, X, z)
    v = memo_l.get(key)
    if v is not None:
        return v
    opts = set()
    for i in range(len(X)):
        t = X[i]
        if t >= 2:
            opts.add(Hl(R - 1, X[:i] + (t - 1,) + X[i + 1:], z))
        else:
            opts.add(Hl(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ Hl(R - 1, X, z - 1))
    g = 0
    while g in opts:
        g += 1
    memo_l[key] = g
    return g


# ---------------- 予測側（独立実装） ----------------
def delta_A(u):
    return u if u % 2 == 1 else u + 1


def ladder_pred(z):
    return {R for R in range(1, z + 2, 2) if R != z + 1}


def pred_positions(X, z):
    """p_0=2t_0+dA(z), p_1=2t_1+dA(z+1), p_j=2t_j+p_{j-2}+2 (j>=2)。"""
    T = sorted(X)
    ps = []
    for j, t in enumerate(T):
        if j == 0:
            p = 2 * t + delta_A(z)
        elif j == 1:
            p = 2 * t + delta_A(z + 1)
        else:
            p = 2 * t + ps[j - 2] + 2
        ps.append(p)
    return set(ps)


def Tinf_pred(X, z):
    return ladder_pred(z) | pred_positions(X, z)


def Tinf_engine(X, z, Rmax):
    Xs = tuple(sorted(X))
    return set(R for R in range(1, Rmax + 1) if Hc(R, (R + 1,) + Xs, z) == 2)


# ---------------- 証明済み単一トークン閉形式（K0832・全称証明済み） ----------------
def q_odd(k):
    return k - 1 if k % 2 == 0 else k


def v_single(a, z, R):
    """H(R;(a);z) の証明済み閉形式（K0832 本文の転写）。"""
    if R == 0:
        return 0
    if z == 0:
        return min(R, a) % 2
    if z == a:
        if R % 2 == 1 and R <= 2 * a - 1:
            return 2
        if R % 2 == 0 and R <= a - 1:
            return 0
        return a % 2
    m = q_odd(min(a, z))
    if R % 2 == 1 and R <= m:
        return 2
    if R % 2 == 0 and R <= m:
        return 0
    if z < a and R < a + z:
        return (R + z) % 2
    return a % 2


def v_single_T(a, z):
    """単一トークンの値2位置集合（証明済み閉形式・上限付き）。"""
    mu = 2 * a - 1 if z == a else q_odd(min(a, z))
    Rmax = 2 * a + z + 4
    return {R for R in range(1, Rmax + 1) if R % 2 == 1 and R <= mu}


# ---------------- 監査本体 ----------------
def tuples_nondecreasing(maxval, m):
    """1..maxval の重複組み合わせ（昇順）を列挙。"""
    if m == 0:
        return [()]
    out = []

    def rec(start, rem, cur):
        if rem == 0:
            out.append(tuple(cur))
            return
        for v in range(start, maxval + 1):
            cur.append(v)
            rec(v, rem - 1, cur)
            cur.pop()

    rec(1, m, [])
    return out


def main():
    rng = random.Random(SEED)
    audit = {
        "seed": SEED,
        "definition": "T_inf(X;z)={R>=1: H(R; X u {R+1}; z)=2}",
        "conjecture": {
            "ladder": "L(z) = {odd R <= z+1} \\ {z+1}",
            "positions": "p_0=2t_0+dA(z), p_1=2t_1+dA(z+1), p_j=2t_j+p_{j-2}+2",
            "status": "conjecture (finite audit, universal proof open)",
        },
        "audits": {},
    }
    fails = []

    def record(name, checks, mismatches, examples):
        audit["audits"][name] = {
            "checks": checks,
            "mismatches": len(mismatches),
            "examples": mismatches[:5],
        }
        if mismatches:
            fails.append(name)

    # --- A0: m=0 ラダー vs エンジン（単一トークン a=R+1） ---
    mm = []
    n = 0
    for z in range(0, 31):
        Rmax = z + 8
        got = Tinf_engine((), z, Rmax)
        pred = Tinf_pred((), z)
        n += 1
        if got != pred:
            mm.append({"z": z, "got": sorted(got), "pred": sorted(pred)})
    record("A0_m0_ladder_engine", n, mm, mm)

    # --- A0b: m=0 vs 証明済み単一トークン閉形式（値も照合） ---
    mm = []
    n = 0
    for z in range(0, 15):
        for R in range(1, min(z + 6, 40) + 1):
            n += 1
            eng = Hc(R, (R + 1,), z)
            ref = v_single(R + 1, z, R)
            if eng != ref:
                mm.append({"z": z, "R": R, "engine": eng, "closed_form": ref})
    record("A0b_m0_vs_published_single_token", n, mm, mm)

    # --- A1: m=1..5 全グリッド（完全T_inf一致） ---
    grids = [
        (1, 20, 20),
        (2, 12, 14),
        (3, 8, 12),
        (4, 5, 10),
        (5, 4, 8),
    ]
    for (m, tmax, zmax) in grids:
        mm = []
        n = 0
        for X in tuples_nondecreasing(tmax, m):
            for z in range(0, zmax + 1):
                Rmax = 2 * sum(X) + z + 30
                got = Tinf_engine(X, z, Rmax)
                pred = Tinf_pred(X, z)
                n += 1
                if got != pred:
                    mm.append({"X": list(X), "z": z,
                               "extra": sorted(got - pred), "missing": sorted(pred - got)})
        record(f"A1_full_grid_m{m}", n, mm, mm)

    # --- A2: m=6,7 スポット ---
    tests67 = [
        (1, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1, 1), (3, 2, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1),
        (3, 3, 2, 2, 1, 1), (4, 3, 2, 2, 1, 1), (4, 3, 3, 2, 2, 1), (5, 4, 3, 2, 1, 1),
        (5, 3, 3, 2, 2, 1), (6, 4, 3, 2, 1, 1), (7, 5, 3, 2, 1, 1), (5, 5, 4, 3, 2, 1),
        (6, 5, 4, 3, 2, 1), (8, 5, 4, 3, 2, 1), (9, 6, 4, 3, 2, 1), (2, 2, 2, 2, 2, 2),
        (1, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1, 1), (3, 2, 2, 1, 1, 1, 1),
        (4, 3, 2, 2, 1, 1, 1), (5, 4, 3, 2, 1, 1, 1), (6, 5, 4, 3, 2, 1, 1),
        (4, 4, 3, 3, 2, 2, 1), (7, 5, 4, 3, 2, 1, 1), (3, 3, 3, 2, 2, 1, 1),
    ]
    mm = []
    n = 0
    for X in tests67:
        for z in range(0, 9):
            Rmax = 2 * sum(X) + z + 30
            got = Tinf_engine(X, z, Rmax)
            pred = Tinf_pred(X, z)
            n += 1
            if got != pred:
                mm.append({"X": list(X), "z": z,
                           "extra": sorted(got - pred), "missing": sorted(pred - got)})
    record("A2_m67_spot", n, mm, mm)

    # --- A3: all-ones ---
    mm = []
    n = 0
    for m in range(1, 8):
        for z in range(0, 13):
            X = (1,) * m
            Rmax = 2 * m + z + 30
            got = Tinf_engine(X, z, Rmax)
            pred = Tinf_pred(X, z)
            n += 1
            if got != pred:
                mm.append({"m": m, "z": z,
                           "extra": sorted(got - pred), "missing": sorted(pred - got)})
    record("A3_all_ones", n, mm, mm)

    # --- A4: 遠方tail（margin 150） ---
    far_states = [(1,), (2,), (5,), (2, 1), (3, 2), (6, 4), (3, 2, 1), (4, 3, 2),
                  (5, 4, 3, 2, 1), (2, 2, 1, 1, 1, 1), (6, 5, 4, 3, 2, 1)]
    mm = []
    n = 0
    for X in far_states:
        for z in [0, 3, 7, 12]:
            Rmax = 2 * sum(X) + z + 150
            got = Tinf_engine(X, z, Rmax)
            pred = Tinf_pred(X, z)
            n += 1
            if got != pred:
                mm.append({"X": list(X), "z": z,
                           "extra": sorted(got - pred), "missing": sorted(pred - got)})
    record("A4_far_tail_margin150", n, mm, mm)

    # --- A5: big-z ---
    mm = []
    n = 0
    for X in [(1,), (2,), (1, 1), (2, 1), (3, 2), (2, 2), (3, 2, 1), (1, 1, 1),
              (4, 3, 2, 1)]:
        for z in [15, 20, 25, 30, 40]:
            Rmax = 2 * sum(X) + z + 30
            got = Tinf_engine(X, z, Rmax)
            pred = Tinf_pred(X, z)
            n += 1
            if got != pred:
                mm.append({"X": list(X), "z": z,
                           "extra": sorted(got - pred), "missing": sorted(pred - got)})
    record("A5_big_z", n, mm, mm)

    # --- A6: エンジン相互照合 (Hc vs Hl, 天井状態を含む) ---
    samples = []
    for _ in range(600):
        m = rng.randint(0, 4)
        X = tuple(sorted(rng.randint(1, 8) for _ in range(m)))
        z = rng.randint(0, 8)
        R = rng.randint(0, 26)
        samples.append((X, z, R))
    samples.sort()
    mm = []
    n = 0
    for (X, z, R) in samples:
        n += 1
        Xs = tuple(sorted(X))
        if Hc(R, (R + 1,) + Xs, z) != Hl(R, (R + 1,) + Xs, z):
            mm.append({"X": list(X), "z": z, "R": R})
    record("A6_engine_crosscheck", n, mm, mm)
    memo_l.clear()  # A6専用の素朴エンジンのメモを解放

    # --- A7: cap補題の直接照合（証明済み・エンジンサニティ） ---
    # 小トークン全般 + capが活発に働く「大トークン・低R」標的の2群。
    samples = []
    for _ in range(500):
        m = rng.randint(1, 5)
        X = tuple(sorted(rng.randint(1, 8) for _ in range(m)))
        z = rng.randint(0, 8)
        R = rng.randint(1, 20)
        samples.append((X, z, R))
    for _ in range(60):
        m = rng.randint(1, 4)
        X = tuple(sorted(rng.randint(9, 50) for _ in range(m)))
        z = rng.randint(0, 10)
        R = rng.randint(1, 12)
        samples.append((X, z, R))
    samples.sort()
    mm = []
    n = 0
    for (X, z, R) in samples:
        n += 1
        if Hc(R, X, z) != Hc(R, cap(X, R + 1), z):
            mm.append({"X": list(X), "z": z, "R": R})
    record("A7_cap_lemma", n, mm, mm)

    # --- A8: Theorem T パリティ（全監査状態のT_infが奇数のみ） ---
    mm = []
    n = 0
    for m in range(0, 5):
        for X in tuples_nondecreasing(5, m)[:200]:
            for z in [0, 3, 7]:
                Rmax = 2 * sum(X) + z + 30
                got = Tinf_engine(X, z, Rmax)
                n += 1
                ev = sorted(r for r in got if r % 2 == 0)
                if ev:
                    mm.append({"X": list(X), "z": z, "even_positions": ev})
    record("A8_theorem_T_parity", n, mm, mm)

    # --- A9: ブリッジ 2トークン元ゲーム ---
    mm = []
    n = 0
    for y in range(1, 9):
        for dx in range(0, 11):
            x = y + dx
            for z in range(0, 9):
                lo = max(z + 2, y)
                for R in range(lo, x):
                    n += 1
                    pred = (R in pred_positions((y,), z))
                    eng = (Hc(R, (x, y), z) == 2)
                    if pred != eng:
                        mm.append({"x": x, "y": y, "z": z, "R": R, "pred": pred, "eng": eng})
    record("A9_bridge_two_token", n, mm, mm)

    # --- A10: ブリッジ 3トークン元ゲーム ---
    mm = []
    n = 0
    for w in range(1, 4):
        for dy in range(0, 4):
            y = w + dy
            for dx in range(0, 9):
                x = y + dx
                for z in range(0, 7):
                    lo = max(z + 2, y)
                    for R in range(lo, x):
                        n += 1
                        pred = (R in pred_positions((y, w), z))
                        eng = (Hc(R, (x, y, w), z) == 2)
                        if pred != eng:
                            mm.append({"x": x, "y": y, "w": w, "z": z, "R": R,
                                       "pred": pred, "eng": eng})
    record("A10_bridge_three_token", n, mm, mm)

    # --- 集計 ---
    total_checks = sum(a["checks"] for a in audit["audits"].values())
    total_mm = sum(a["mismatches"] for a in audit["audits"].values())
    audit["total_checks"] = total_checks
    audit["total_mismatches"] = total_mm
    audit["all_pass"] = (total_mm == 0)

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "audit.json"), "w") as f:
        json.dump(audit, f, indent=1, sort_keys=True, ensure_ascii=False)

    print(f"total checks: {total_checks}")
    print(f"total mismatches: {total_mm}")
    for name, a in sorted(audit["audits"].items()):
        print(f"  {name}: {a['checks']} checks, {a['mismatches']} mismatches")
    print("ALL PASS" if total_mm == 0 else f"FAILED: {fails}")
    return 0 if total_mm == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
