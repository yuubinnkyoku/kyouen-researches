#!/usr/bin/env python3
"""2トークン族残余2位置集合閉形式（予想）の独立検証器。

対象: κ=1 残余ゲーム H(R;X;z)（K0832・全t最大値定理の再帰に従う）のうち
X=(x,y), x>=y>=1 の2位置集合 T(x,y,z) = {R : H(R;(x,y);z)=2} の閉形式。
閉形式は本体report.mdの予想1（ラダー・家族B・家族A）。

検証は有限監査であり、閉形式の全称性は主張しない。
エンジン3種（素朴・ラベル付き独立・cap付き）と発表済み定理
（全1族・系A、単一トークン閉形式、高余裕単一トークン縮約、tailレジーム）
との照合からなる。全てseed固定・決定的。
"""
import json
import random
import sys

sys.setrecursionlimit(100000)


# ---------- 基本エンジン1: 素朴（多重集合はソート済みタプル、z+Rでメモ） ----------
memo1 = {}
def H1(R, X, z):
    if R == 0:
        return 0
    X = tuple(sorted(X))
    key = (R, X, z)
    if key in memo1:
        return memo1[key]
    opts = set()
    for i, t in enumerate(X):
        if t >= 2:  # A手
            Y = list(X); Y[i] = t - 1
            opts.add(H1(R - 1, tuple(sorted(Y)), z))
        elif t == 1:  # B手
            Y = [u for j, u in enumerate(X) if j != i]
            opts.add(H1(R - 1, tuple(sorted(Y)), z + 1))
    if z >= 1:  # C手
        opts.add(1 ^ H1(R - 1, X, z - 1))
    v = mex(opts)
    memo1[key] = v
    return v


def mex(s):
    g = 0
    while g in s:
        g += 1
    return g


# ---------- エンジン2: ラベル付き独立（トークンを区別する別実装） ----------
memo2 = {}
def H2(R, X, z):
    if R == 0:
        return 0
    key = (R, X, z)  # X はラベル付き（ソートしない）
    if key in memo2:
        return memo2[key]
    opts = set()
    for i in range(len(X)):
        t = X[i]
        if t >= 2:
            opts.add(H2(R - 1, X[:i] + (t - 1,) + X[i + 1:], z))
        else:
            opts.add(H2(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H2(R - 1, X, z - 1))
    v = mex(opts)
    memo2[key] = v
    return v


# ---------- エンジン3: cap補題付き（トークン値をR+1にcap、高速） ----------
def cap(X, c):
    return tuple(sorted(min(t, c) for t in X))


memo3 = {}
def H3(R, X, z):
    X = cap(X, R + 1)
    return H3c(R, X, z)

def H3c(R, X, z):
    if R == 0:
        return 0
    key = (R, X, z)
    if key in memo3:
        return memo3[key]
    Xc = cap(X, R)  # 子レベルでのcap
    opts = set()
    for i, t in enumerate(Xc):
        if t >= 2:
            opts.add(H3c(R - 1, cap(Xc[:i] + (t - 1,) + Xc[i + 1:], R - 1), z))
        else:
            opts.add(H3c(R - 1, cap(Xc[:i] + Xc[i + 1:], R - 1), z + 1))
    if z >= 1:
        opts.add(1 ^ H3c(R - 1, Xc, z - 1))
    v = mex(opts)
    memo3[key] = v
    return v


# ---------- 発表済み定理の参照実装 ----------
def q_odd(k):
    """k以下最大の奇数。q(0)=0。"""
    return k - 1 if k % 2 == 0 else k


def T_all_ones(k, z):
    """全1族 X=(1^k) の2位置集合（K0832系A・全称証明済み）。"""
    if z == 0:
        return set()
    if z % 2 == 1:
        return set(range(1, q_odd(k) + 1, 2))
    s = set(range(1, q_odd(min(k, z)) + 1, 2))
    e = 2 * k - z + 1
    if e >= 1:
        s.add(e)
    return s


# ---------- 予想閉形式（本体report.md・予想1） ----------
def smin(d):
    return d + 1 if d % 2 == 0 else d + 2


def T_closed(x, y, z):
    """2トークン族 X=(x,y) の2位置集合の予想閉形式。"""
    if x < y:
        x, y = y, x
    S = x + y
    d = x - y
    out = set(range(1, q_odd(min(S, z)) + 1, 2))  # ラダー
    if d % 2 == z % 2 and d <= z:  # 家族B
        ystar = (z - d) // 2
        lo = smin(d)
        hi = 2 * ((z + d + 3) // 4) - 1
        if y == ystar and ystar >= 1 and hi >= lo:
            out.update(2 * y + dd for dd in range(lo, hi + 1, 2))  # PT角
        if (z + d) % 4 == 2 and y >= ystar:  # EXT
            out.add(2 * y + (z + d) // 2)
    if d == z + 1:  # 家族A: ラン
        da = z + 1 if z % 2 == 0 else z
        out.update(2 * y + dd for dd in range(da, 2 * z + 2, 2))
    elif d >= z + 2:  # 家族A: 定常
        out.add(2 * y + (z + 1 if z % 2 == 0 else z))
    return out


# ---------- 窓とT集合計算 ----------
def T_engine(x, y, z):
    X = tuple(sorted((x, y)))
    L = x + y + 2 + z
    return {R for R in range(0, L + 4) if H3(R, X, z) == 2}


def main():
    rng = random.Random(20261116)
    results = {}

    # V0a: 素朴 vs ラベル付き独立エンジン（小状態・全R走査）
    bad = 0; n = 0
    for _ in range(120):
        x = rng.randint(1, 7); y = rng.randint(1, x); z = rng.randint(0, 5)
        L = x + y + z + 2
        for R in range(0, L + 2):
            n += 1
            if H1(R, (x, y), z) != H2(R, (max(x, y), min(y, x)), z):
                bad += 1
                if bad <= 5:
                    print(f"V0a MISMATCH x={x} y={y} z={z} R={R}")
    results['V0a_naive_vs_labeled'] = {'checks': n, 'mismatches': bad}

    # V0b: cap付き vs 素朴（cap補題の適用確認・中状態）
    bad = 0; n = 0
    for _ in range(120):
        x = rng.randint(1, 10); y = rng.randint(1, x); z = rng.randint(0, 6)
        L = x + y + z + 2
        for R in range(0, min(L + 2, 16)):
            n += 1
            if H3(R, (x, y), z) != H1(R, (max(x, y), min(x, y)), z):
                bad += 1
                if bad <= 5:
                    print(f"V0b MISMATCH x={x} y={y} z={z} R={R}")
    results['V0b_capped_vs_naive'] = {'checks': n, 'mismatches': bad}

    # V1: 閉形式 vs cap付きエンジン・全グリッド
    bad = 0; n = 0; samples = []
    for z in range(0, 17):
        for y in range(1, 27):
            for d in range(0, 19):
                x = y + d
                Te = T_engine(x, y, z)
                Tc = T_closed(x, y, z)
                n += 1
                if Te != Tc:
                    bad += 1
                    if len(samples) < 10:
                        samples.append({'x': x, 'y': y, 'z': z, 'engine': sorted(Te), 'closed': sorted(Tc)})
    results['V1_grid_z0_16_y1_26_d0_18'] = {'checks': n, 'mismatches': bad, 'samples': samples}

    # V2: 大規模ランダム＋法則の境界標的スポット
    bad = 0; n = 0; samples = []
    cases = [(rng.randint(1, 60), rng.randint(1, 60), rng.randint(0, 40)) for _ in range(220)]
    for z in range(0, 41):
        for d in [z - 2, z - 1, z, z + 1, z + 2, z + 3, max(z - 4, 0)]:
            if d < 0:
                continue
            for y in [1, 2, (z - d) // 2 if (z - d) % 2 == 0 and (z - d) // 2 >= 1 else 1, 25, 40]:
                cases.append((y + d, y, z))
    for (x, y, z) in cases:
        x2, y2 = max(x, y), min(x, y)
        if x2 > 62 or y2 > 62 or z > 40:
            continue
        Te = T_engine(x2, y2, z)
        Tc = T_closed(x2, y2, z)
        n += 1
        if Te != Tc:
            bad += 1
            if len(samples) < 10:
                samples.append({'x': x2, 'y': y2, 'z': z, 'engine': sorted(Te), 'closed': sorted(Tc)})
    results['V2_random_and_boundary'] = {'checks': n, 'mismatches': bad, 'samples': samples}

    # V3: x=y=1（全1族k=2）と証明済み系Aの照合
    bad = 0; n = 0; samples = []
    for z in range(0, 41):
        Ta = T_all_ones(2, z)
        Tc = T_closed(1, 1, z)
        Te = T_engine(1, 1, z)
        n += 2
        if Tc != Ta:
            bad += 1; samples.append({'z': z, 'corollaryA': sorted(Ta), 'closed': sorted(Tc)})
        if Te != Ta:
            bad += 1; samples.append({'z': z, 'corollaryA': sorted(Ta), 'engine': sorted(Te)})
    results['V3_all_ones_k2_vs_corollaryA'] = {'checks': n, 'mismatches': bad, 'samples': samples}

    # V4a: 証明済み高余裕単一トークン縮約との記号的一貫性
    # z >= S+R-1（R<=z-S+1）の帯では2位置は奇数R<=q_o(S)に限る（定理・K0832）。
    bad = 0; n = 0
    for x in range(1, 21):
        for y in range(1, x + 1):
            S = x + y
            for z in range(S, 61):
                lim = z - S + 1
                if lim < 1:
                    continue
                expect = set(range(1, min(q_odd(S), lim) + 1, 2))
                got = {R for R in T_closed(x, y, z) if R <= lim}
                n += 1
                if got != expect:
                    bad += 1
                    if bad <= 5:
                        print(f"V4a MISMATCH x={x} y={y} z={z}")
    results['V4a_highz_band_consistency'] = {'checks': n, 'mismatches': bad}

    # V4b: 証明済みtailレジームとの一貫性（R >= S+2+z-1 = S+z+1 は2位置でない）
    bad = 0; n = 0
    for x in range(1, 21):
        for y in range(1, x + 1):
            S = x + y
            for z in range(0, 41):
                Tc = T_closed(x, y, z)
                n += 1
                if any(R >= S + z + 1 for R in Tc):
                    bad += 1
                    if bad <= 5:
                        print(f"V4b MISMATCH x={x} y={y} z={z} T={sorted(Tc)}")
    results['V4b_tail_regime_consistency'] = {'checks': n, 'mismatches': bad}

    # V5: Theorem T一貫性（2位置は奇数Rのみ）
    bad = 0; n = 0
    for x in range(1, 30):
        for y in range(1, x + 1):
            for z in range(0, 30):
                n += 1
                if any(R % 2 == 0 for R in T_closed(x, y, z)):
                    bad += 1
    results['V5_parity_consistency'] = {'checks': n, 'mismatches': bad}

    audit = {
        'date': '2026-11-16',
        'subject': 'two-token residual 2-position closed form (conjecture)',
        'engine_basis': ['naive multiset memo', 'labeled independent memo', 'cap-lemma capped memo'],
        'results': results,
        'total_checks': sum(r['checks'] for r in results.values()),
        'total_mismatches': sum(r['mismatches'] for r in results.values()),
    }
    with open('output/audit.json', 'w') as f:
        json.dump(audit, f, indent=1, sort_keys=True)
    for k, r in results.items():
        print(f"{k}: checks={r['checks']} mismatches={r['mismatches']}")
    print(f"TOTAL checks={audit['total_checks']} mismatches={audit['total_mismatches']}")
    print("PASS" if audit['total_mismatches'] == 0 else "FAIL")


if __name__ == '__main__':
    main()
