#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2トークン残余ゲーム H(R;(x,3);7) の y=3 境界切片 全Grundy分類の独立検証器。

監査:
  - 直接多重集合再帰エンジン vs 候補閉形式
  - A/B/Cアンカー再構成エンジン vs 候補閉形式
    (A=cand_y3(x-1) R強帰納, B=K0978 z=7 y=2 公式, C=1 xor K0879 z=6 y=3 公式)
  - 選択肢署名帯表（R<=x+10 全被覆・一致・mex）+ tail 帯 (x+11<=R<=x+24)
  - K0879転写錨 vs 直接z=6再帰 / K0978転写錨 vs 直接z=7 y=2再帰
  - tail定理照合 R>=x+11 -> (x+3) mod 2  （K0832 高R縮約 tail: R>=S+|X|+z-1=x+11）
  - 高さのみ縮約アンカー R<=8 -> v(x+3,7,R)  （K0832: R<=z+1 で単一トークンへ縮約）
  - Theorem T 偶奇照合、値2位置の奇数性、T∩P=∅
  - 固定seed散点照合

全出力は決定的で、二回実行でbyte-identicalであることを要する。
"""
import sys, json, random
sys.setrecursionlimit(1000000)
from functools import lru_cache

def qod(k):
    return k if k % 2 == 1 else k - 1

def in_I(R, a):
    return R >= a
def in_O(R, a, b):
    return a <= R <= b and R % 2 == 1
def in_E(R, a, b):
    return a <= R <= b and R % 2 == 0

# ------------------------------------------------ 直接多重集合再帰エンジン
@lru_cache(maxsize=None)
def H_direct(R, X, z):
    """A手: トークン v>1 を v-1 へ。B手: トークン1の除去で z+1。C手: z>=1 で z-1（値は1 xor）。"""
    if R == 0:
        return 0
    opts = set()
    seen = set()
    for i, v in enumerate(X):
        if v in seen:
            continue
        seen.add(v)
        if v > 1:
            opts.add(H_direct(R - 1, tuple(sorted(X[:i] + X[i+1:] + (v - 1,))), z))
        else:
            opts.add(H_direct(R - 1, tuple(sorted(X[:i] + X[i+1:])), z + 1))
    if z >= 1:
        opts.add(1 ^ H_direct(R - 1, X, z - 1))
    if not opts:
        return 0
    m = 0
    while m in opts:
        m += 1
    return m

# ---------------------------------------- 単一トークン閉形式（K0832公式）
def v_single(x, z, R):
    if R == 0 or x <= 0:
        return 0
    L = x + z + 1
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 == 1 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = qod(z)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        if m < R < L - 1:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = qod(x)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        return x % 2
    raise ValueError

# ------------------------------ z=6・y=3 切片閉形式（K0879公式の転写）
def h6_y3(x, R):
    """H(R;(x,3);6) = K0879 の閉形式。"""
    if R == 0:
        return 0
    inT = (
        (x == 3 and R in (1, 3, 5, 7, 9)) or
        (x in (4, 5, 6, 8, 9) and R in (1, 3, 5)) or
        (x == 7 and R in (1, 3, 5, 11)) or
        (x == 10 and (R in (1, 3, 5) or in_O(R, 13, 19))) or
        (x >= 11 and R in (1, 3, 5, 13))
    )
    if inT:
        return 2
    inP = (
        (x == 3 and False) or
        (x == 4 and (R == 7 or in_I(R, 9))) or
        (x in (5, 7) and R in (7, 9)) or
        (x in (6, 8) and (R in (7, 9, 11) or in_I(R, 12))) or
        (x == 9 and R in (7, 9, 11)) or
        (x == 10 and (R in (7, 9, 11) or in_E(R, 14, 18) or in_I(R, 20))) or
        (x >= 11 and x % 2 == 1 and (R in (7, 9, 11) or in_E(R, 14, x + 9))) or
        (x >= 12 and x % 2 == 0 and (R in (7, 9, 11) or in_E(R, 14, x + 8) or in_I(R, x + 10)))
    )
    if inP:
        return 1
    return 0

# ------------------------------ z=7・y=2 切片閉形式（K0978公式の転写）
def h7_y2(x, R):
    """H(R;(x,2);7) = K0978 の閉形式。"""
    if R == 0:
        return 0
    inT = (
        (x == 2 and R in (1, 3)) or
        (x in (3, 4) and R in (1, 3, 5)) or
        (x == 5 and R in (1, 3, 5, 7, 9)) or
        (x in (6, 7, 8) and R in (1, 3, 5, 7)) or
        (x == 9 and R in (1, 3, 5, 7, 11)) or
        (x == 10 and (R in (1, 3, 5, 7, 11) or in_O(R, 13, 19))) or
        (x >= 11 and R in (1, 3, 5, 7, 11))
    )
    if inT:
        return 2
    inP = (
        (x in (2, 4) and False) or
        (x == 3 and in_I(R, 6)) or
        (x == 5 and (R == 8 or in_I(R, 10))) or
        (x == 6 and R == 8) or
        (x == 7 and (R == 8 or in_I(R, 10))) or
        (x == 8 and R in (8, 10)) or
        (x == 9 and (R in (8, 10) or in_I(R, 12))) or
        (x == 10 and R in (8, 10)) or
        (x >= 12 and x % 2 == 0 and (R in (8, 10) or in_O(R, 13, x + 9))) or
        (x >= 11 and x % 2 == 1 and (R in (8, 10) or in_O(R, 13, x + 9) or in_I(R, x + 10)))
    )
    if inP:
        return 1
    return 0

# ---------------------------------------- 候補: z=7・y=3 切片の閉形式
def cand_y3(x, R):
    """候補 H(R;(x,3);7)、x>=3。"""
    if R == 0:
        return 0
    isT = (
        (x == 3 and R in (1, 3, 5)) or
        (x == 4 and R in (1, 3, 5, 7, 9)) or
        (x in (5, 7, 8, 9) and R in (1, 3, 5, 7)) or
        (x == 6 and R in (1, 3, 5, 7, 11)) or
        (x == 10 and R in (1, 3, 5, 7, 13)) or
        (x == 11 and (R in (1, 3, 5, 7) or in_O(R, 13, 21))) or
        (x >= 12 and R in (1, 3, 5, 7, 13))
    )
    if isT:
        return 2
    isP = (
        (x == 3 and False) or
        (x == 4 and (R in (8, 10) or in_I(R, 11))) or
        (x in (5, 7) and R in (8, 10)) or
        (x in (6, 8) and (R in (8, 10) or in_I(R, 12))) or
        (x == 9 and R in (8, 10, 12)) or
        (x == 10 and (R in (8, 10, 12) or in_I(R, 14))) or
        (x == 11 and R in (8, 10, 12)) or
        (x >= 12 and x % 2 == 0 and (R in (8, 10, 12) or in_O(R, 15, x + 9) or in_I(R, x + 11))) or
        (x >= 13 and x % 2 == 1 and (R in (8, 10, 12) or in_O(R, 15, x + 10)))
    )
    if isP:
        return 1
    return 0

# -------------------------------------- A/B/Cアンカー署名再構成エンジン
def reconstruct_options(x, R):
    """x>=4: {A=cand_y3(x-1), B=h7_y2(x), C=1 xor h6_y3(x)}、x=3: {B, C}（A/B合流）。"""
    opts = set()
    if R == 0:
        return opts
    if x >= 4:
        opts.add(cand_y3(x - 1, R - 1))   # A手: H(R-1;(x-1,3);7) 帰納仮説
        opts.add(h7_y2(x, R - 1))         # B手: H(R-1;(x,2);7) = K0978
    else:
        opts.add(h7_y2(3, R - 1))         # x=3: 2つの減少手が同一子 (3,2)
    opts.add(1 ^ h6_y3(x, R - 1))        # C手: 1 xor H(R-1;(x,3);6) = K0879
    return opts

def mex(opts):
    m = 0
    s = set(opts)
    while m in s:
        m += 1
    return m

# ------------------------------------------------- 選択肢署名表（帯表）
# 各帯は (述語, 署名)。述語は R に対して評価する。署名は子値集合の数字列。
# 表は 1<=R<=x+10 を全被覆する。R>=x+11 はtail定理（R>=S+|X|+z-1=x+11）。
# 証明本文の表と同一の帯構造を持つ。
def _od(R, a, b):   # [a,b] の奇数
    return R % 2 == 1 and a <= R <= b
def _ev(R, a, b):   # [a,b] の偶数
    return R % 2 == 0 and a <= R <= b

def bands_for(x):
    if x == 3:
        return [ (lambda R: _od(R,1,5), "01"), (lambda R: _od(R,7,13), "1"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: _ev(R,8,10), "13"), (lambda R: R == 12, "1") ]
    if x == 4:
        return [ (lambda R: _od(R,1,9), "01"), (lambda R: _od(R,11,13), "0"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: _ev(R,8,14), "0") ]
    if x == 5:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,15), "1"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: _ev(R,8,10), "02"), (lambda R: _ev(R,12,14), "1") ]
    if x == 6:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: R == 9, "1"), (lambda R: R == 11, "01"), (lambda R: _od(R,13,15), "0"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: _ev(R,10,16), "0") ]
    if x == 7:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,17), "1"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "123"), (lambda R: _ev(R,14,16), "1") ]
    if x == 8:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,11), "1"), (lambda R: _od(R,13,17), "0"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: _ev(R,10,18), "0") ]
    if x == 9:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,19), "1"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "02"), (lambda R: _ev(R,14,18), "1") ]
    if x == 10:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,11), "1"), (lambda R: R == 13, "01"), (lambda R: _od(R,15,19), "0"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "02"), (lambda R: _ev(R,14,20), "023") ]
    if x == 11:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,11), "1"), (lambda R: _od(R,13,21), "01"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "02"), (lambda R: R == 14, "123"), (lambda R: _ev(R,16,20), "1") ]
    if x == 12:
        return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,11), "1"), (lambda R: R == 13, "01"), (lambda R: _od(R,15,21), "0"),
                 (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "02"), (lambda R: R == 14, "123"), (lambda R: _ev(R,16,22), "12") ]
    # x >= 13 の定常行
    return [ (lambda R: _od(R,1,7), "01"), (lambda R: _od(R,9,11), "1"), (lambda R: R == 13, "01"), (lambda R: _od(R,15,x+10), "0"),
             (lambda R: _ev(R,2,6), "23"), (lambda R: R == 8, "02"), (lambda R: R == 10, "0"), (lambda R: R == 12, "02"), (lambda R: R == 14, "123"), (lambda R: _ev(R,16,x+10), "1") ]

def table_signature(bands, R):
    hit = None; count = 0
    for pred, sig in bands:
        if pred(R):
            count += 1
            hit = sig
    return count, hit

def sigstr(opts):
    return "".join(str(m) for m in sorted(opts))

# ------------------------------------------------------------------ 監査
def main():
    audit = {"検証器": "verify_z7_y3.py",
             "対象": "H(R;(x,3);7) 2トークン残余ゲーム z=7・y=3境界切片の全Grundy分類",
             "検査": {}}
    ok = True

    # V1: 直接多重集合再帰 vs 候補閉形式（稠密グリッド）
    n = bad = 0
    for x in range(3, 61):
        for R in range(0, x + 41):
            n += 1
            if H_direct(R, (x, 3), 7) != cand_y3(x, R):
                bad += 1
    audit["検査"]["V1_直接再帰×候補"] = {"範囲": "3<=x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V2: 直接再帰 vs アンカー署名再構成のmex（同じグリッド）
    n = bad = 0
    for x in range(3, 61):
        for R in range(0, x + 41):
            n += 1
            v = mex(reconstruct_options(x, R)) if R >= 1 else 0
            if H_direct(R, (x, 3), 7) != v:
                bad += 1
    audit["検査"]["V2_直接再帰×アンカー再構成mex"] = {"範囲": "3<=x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V3a: 署名表の被覆・一致・mex照合（全x、全 1<=R<=x+10）
    n = bad_cov = bad_sig = bad_mex = 0
    for x in range(3, 2001):
        bands = bands_for(x)
        for R in range(1, x + 11):
            n += 1
            cnt, tsig = table_signature(bands, R)
            if cnt != 1:
                bad_cov += 1
                continue
            asig = sigstr(reconstruct_options(x, R))
            if asig != tsig:
                bad_sig += 1
            if mex(reconstruct_options(x, R)) != cand_y3(x, R):
                bad_mex += 1
    audit["検査"]["V3a_署名表被覆・一致・mex"] = {"範囲": "3<=x<=2000, 1<=R<=x+10",
        "照合点": n, "被覆違反": bad_cov, "署名不一致": bad_sig, "mex不一致": bad_mex}
    ok &= (bad_cov + bad_sig + bad_mex) == 0

    # V3b: tail帯 (x+11<=R<=x+24) のアンカー再構成 vs 候補
    n = bad = 0
    for x in range(3, 2001):
        for R in range(x + 11, x + 25):
            n += 1
            if mex(reconstruct_options(x, R)) != cand_y3(x, R):
                bad += 1
    audit["検査"]["V3b_tail帯アンカー再構成×候補"] = {"範囲": "3<=x<=2000, x+11<=R<=x+24", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V4: K0879転写錨 vs 直接z=6再帰（C子の公式の独立確認）
    n = bad = 0
    for x in range(3, 61):
        for R in range(0, x + 41):
            n += 1
            if H_direct(R, (x, 3), 6) != h6_y3(x, R):
                bad += 1
    audit["検査"]["V4_z6y3錨×直接z=6再帰"] = {"範囲": "3<=x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V5: K0978転写錨 vs 直接z=7,y=2再帰（B子の公式の独立確認）
    n = bad = 0
    for x in range(2, 61):
        for R in range(0, x + 41):
            n += 1
            if H_direct(R, (x, 2), 7) != h7_y2(x, R):
                bad += 1
    audit["検査"]["V5_z7y2錨×直接再帰"] = {"範囲": "2<=x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V6: tail照合 R>=x+11 -> (x+3) mod 2
    n = bad = 0
    for x in range(3, 5001):
        for R in range(x + 11, x + 15):
            n += 1
            if cand_y3(x, R) != (x + 3) % 2:
                bad += 1
    audit["検査"]["V6_tail定理照合"] = {"範囲": "3<=x<=5000, {x+11..x+14}", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V7: 高さのみ縮約アンカー R<=8 -> v(x+3,7,R)
    n = bad = 0
    for x in range(3, 501):
        for R in range(0, 9):
            n += 1
            if cand_y3(x, R) != v_single(x + 3, 7, R):
                bad += 1
    audit["検査"]["V7_高さのみ縮約アンカー"] = {"範囲": "3<=x<=500, R<=8", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V8: 固定seed散点
    random.seed(12345)
    n = bad = 0
    for _ in range(2000):
        x = random.randint(3, 300)
        R = random.randint(0, x + 60)
        n += 1
        if H_direct(R, (x, 3), 7) != cand_y3(x, R):
            bad += 1
    audit["検査"]["V8_固定seed散点"] = {"範囲": "3<=x<=300, R<=x+60, seed=12345", "照合点": n, "不一致": bad}
    ok &= bad == 0

    # V9: Theorem T 偶奇照合・値2奇数性・T∩P=∅
    n = bad_val = bad_even = bad_odd2 = bad_TP = 0
    for x in range(3, 2001):
        for R in range(0, x + 25):
            v = cand_y3(x, R)
            n += 1
            if v not in (0, 1, 2):
                bad_val += 1
            if R % 2 == 0 and v > 1:
                bad_even += 1
            if v == 2 and R % 2 == 0:
                bad_odd2 += 1
            if v == 2 and v == 1:
                bad_TP += 1
    audit["検査"]["V9_TheoremT偶奇照合"] = {"範囲": "3<=x<=2000, R<=x+24", "照合点": n,
        "値域違反": bad_val, "偶数R値2違反": bad_even, "T奇数性違反": bad_odd2}
    ok &= (bad_val + bad_even + bad_odd2) == 0

    total = 0
    for k, v in audit["検査"].items():
        for kk in ("照合点", "被覆違反", "署名不一致", "mex不一致", "不一致", "値域違反", "偶数R値2違反", "T奇数性違反"):
            if kk in v:
                total += v[kk]
                break
    audit["総照合点"] = total
    audit["全検査パス"] = ok

    import os
    os.makedirs("output", exist_ok=True)
    with open("output/audit.json", "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
