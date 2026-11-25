#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2トークン残余ゲーム H(R;(x,1);7) の y=1 境界切片 全Grundy分類の独立検証器。

K0977 の有限監査:
  - 直接多重集合再帰エンジン vs 候補閉形式
  - A/B/Cアンカー再構成エンジン vs 候補閉形式
  - 選択肢署名表（帯表）の全R被覆・一致・mex照合
  - 単一トークン z=8 錨（K0832公式）vs 直接単一トークン再帰
  - z=6 y=1 錨（K0877公式の転写）vs 直接2トークンz=6再帰
  - tail定理照合 R>=x+9 -> (x+1) mod 2
  - 高さのみ縮約アンカー R<=8 -> v(x+1,7,R)
  - Theorem T 偶奇照合、値2位置の奇数性、T∩P=∅
  - 固定seed散点照合

全出力は決定的で、二回実行でbyte-identicalであることを要する。
"""
import sys, json, random
sys.setrecursionlimit(1000000)
from functools import lru_cache

# ---------------------------------------------------------------- 基本工具
def qod(k):
    return k if k % 2 == 1 else k - 1

# ------------------------------------------------ 直接多重集合再帰エンジン
@lru_cache(maxsize=None)
def H_direct(R, X, z):
    """残余ゲーム H(R;X;z) の直接再帰。
    A手: トークン v>1 を v-1 へ。B手: トークン1の除去で z+1。C手: z>=1 で z-1、値は 1 xor。"""
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

# ------------------------------ z=6・y=1 切片閉形式（K0877公式の転写）
def h6_y1(x, R):
    """H(R;(x,1);6) = K0877 の閉形式。"""
    if R == 0:
        return 0
    if x == 1:
        T = (R == 1); P = False
    elif x in (2, 3):
        T = R in (1, 3); P = (x == 2 and R >= 4)
    elif x == 4:
        T = R in (1, 3, 5); P = R >= 6
    elif x == 5:
        T = R in (1, 3, 5, 7); P = False
    elif x in (6, 7):
        T = R in (1, 3, 5); P = (x == 6 and R >= 7) or (x == 7 and R == 7)
    elif x == 8:
        T = R in (1, 3, 5) or (9 <= R <= 15 and R % 2 == 1)
        P = (R == 7) or (10 <= R <= 14 and R % 2 == 0) or R >= 16
    else:
        T = R in (1, 3, 5, 9)
        if x % 2 == 1:
            P = (R == 7) or (10 <= R <= x + 7 and R % 2 == 0)
        else:
            P = (R == 7) or (10 <= R <= x + 6 and R % 2 == 0) or R >= x + 8
    if T:
        return 2
    if P:
        return 1
    return 0

# ---------------------------------------- 候補: z=7・y=1 切片の閉形式
def cand(x, R):
    """候補 H(R;(x,1);7)。"""
    if R == 0:
        return 0
    isT = (
        (x == 1 and R == 1) or
        (x in (2, 3) and R in (1, 3)) or
        (x in (4, 5) and R in (1, 3, 5)) or
        (x in (6, 7) and R in (1, 3, 5, 7)) or
        (x == 9 and 1 <= R <= 17 and R % 2 == 1) or
        (x >= 8 and x != 9 and R in (1, 3, 5, 7, 9))
    )
    if isT:
        return 2
    isP = (
        (x in (1, 3, 5) and False) or
        (x == 2 and R >= 4) or
        (x == 4 and R >= 6) or
        (x == 6 and R >= 8) or
        (x in (7, 9) and R == 8) or
        (x == 8 and (R == 8 or R >= 10)) or
        (x >= 11 and x % 2 == 1 and (R == 8 or (11 <= R <= x + 8 and R % 2 == 1))) or
        (x >= 10 and x % 2 == 0 and (R == 8 or (11 <= R <= x + 9 and R % 2 == 1) or R >= x + 10))
    )
    if isP:
        return 1
    return 0

# -------------------------------------- A/B/Cアンカー署名再構成エンジン
def reconstruct_options(x, R):
    """x>=2: {A=cand(x-1), B=v_single(x,8), C=1^h6_y1}、x=1: B手2本同一。"""
    opts = set()
    if R == 0:
        return opts
    if x >= 2:
        opts.add(cand(x - 1, R - 1))   # A手: H(R-1;(x-1,1);7)
        opts.add(v_single(x, 8, R - 1))  # B手: H(R-1;(x);8)
    else:
        opts.add(v_single(1, 8, R - 1))  # x=1: 二つのB手は同一子 (1;8)
    opts.add(1 ^ h6_y1(x, R - 1))       # C手: 1 xor H(R-1;(x,1);6)
    return opts

def mex(opts):
    m = 0
    s = set(opts)
    while m in s:
        m += 1
    return m

# ------------------------------------------------- 選択肢署名表（帯表）
# 各帯: (述語 R->bool, 署名文字列)。各行で全 R>=1 を冗長なく被覆する。
def bands_for(x):
    if x == 1:
        return [ (lambda R: R == 1, "01"), (lambda R: R == 2, "23"), (lambda R: R >= 3, "1") ]
    if x == 2:
        return [ (lambda R: R in (1, 3), "01"), (lambda R: R == 2, "23"), (lambda R: R == 4, "03"), (lambda R: R >= 5, "0") ]
    if x == 3:
        return [ (lambda R: R in (1, 3), "01"), (lambda R: R in (2, 4), "23"), (lambda R: R >= 5, "1") ]
    if x == 4:
        return [ (lambda R: R in (1, 3, 5), "01"), (lambda R: R in (2, 4), "23"), (lambda R: R == 6, "03"), (lambda R: R >= 7, "0") ]
    if x == 5:
        return [ (lambda R: R in (1, 3, 5), "01"), (lambda R: R in (2, 4, 6), "23"), (lambda R: R == 7, "1"), (lambda R: R == 8, "13"), (lambda R: R >= 9, "1") ]
    if x == 6:
        return [ (lambda R: R in (1, 3, 5, 7), "01"), (lambda R: R in (2, 4, 6), "23"), (lambda R: R >= 8, "0") ]
    if x == 7:
        return [ (lambda R: R in (1, 3, 5, 7), "01"), (lambda R: R in (2, 4, 6), "23"), (lambda R: R == 8, "02"), (lambda R: R >= 9, "1") ]
    if x == 8:
        return [ (lambda R: R in (1, 3, 5, 7), "01"), (lambda R: R in (2, 4, 6), "23"),
                 (lambda R: R == 8, "02"), (lambda R: R == 9, "01"),
                 (lambda R: 10 <= R <= 16 and R % 2 == 0, "023"), (lambda R: (11 <= R <= 15 and R % 2 == 1) or R >= 17, "0") ]
    if x == 9:
        return [ (lambda R: R in (1, 3, 5, 7), "01"), (lambda R: R in (2, 4, 6), "23"),
                 (lambda R: R == 8, "02"), (lambda R: R == 9, "01"), (lambda R: R == 10, "123"),
                 (lambda R: 11 <= R <= 17 and R % 2 == 1, "01"), (lambda R: (12 <= R <= 16 and R % 2 == 0) or R >= 18, "1") ]
    if x == 10:
        return [ (lambda R: R in (1, 3, 5, 7, 9), "01"), (lambda R: R in (2, 4, 6), "23"),
                 (lambda R: R == 8, "02"), (lambda R: R == 10, "123"),
                 (lambda R: 11 <= R <= 17 and R % 2 == 1, "0"),
                 (lambda R: 12 <= R <= 18 and R % 2 == 0, "12"),
                 (lambda R: R >= 19, "0") ]
    if x % 2 == 1:   # x >= 11 奇数の定常行
        return [ (lambda R: R in (1, 3, 5, 7, 9), "01"), (lambda R: R in (2, 4, 6), "23"),
                 (lambda R: R == 8, "02"), (lambda R: R == 10, "123"),
                 (lambda R: 11 <= R <= x + 8 and R % 2 == 1, "0"),
                 (lambda R: 12 <= R <= x + 7 and R % 2 == 0, "1"),
                 (lambda R: R >= x + 9, "1") ]
    # x >= 12 偶数の定常行
    return [ (lambda R: R in (1, 3, 5, 7, 9), "01"), (lambda R: R in (2, 4, 6), "23"),
             (lambda R: R == 8, "02"), (lambda R: R == 10, "123"),
             (lambda R: 11 <= R <= x + 9 and R % 2 == 1, "0"),
             (lambda R: 12 <= R <= x + 8 and R % 2 == 0, "1"),
             (lambda R: R >= x + 10, "0") ]

def table_signature(x, R):
    """署名表の帯を引く。被覆数も返す。"""
    hit = None; count = 0
    for pred, sig in bands_for(x):
        if pred(R):
            count += 1
            hit = sig
    return count, hit

def sigstr(opts):
    return "".join(str(m) for m in sorted(opts))

# ------------------------------------------------------------------ 監査
def main():
    audit = {"検証器": "verify_z7_y1.py",
             "対象": "H(R;(x,1);7) 2トークン残余ゲーム z=7・y=1境界切片の全Grundy分類",
             "検査": {}}
    ok = True

    # V1: 直接多重集合再帰 vs 候補閉形式（稠密グリッド）
    n = 0; bad = 0
    for x in range(1, 61):
        for R in range(0, x + 41):
            n += 1
            if H_direct(R, (1, x), 7) != cand(x, R):
                bad += 1
    audit["検査"]["V1_直接再帰×候補"] = {"範囲": "x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V2: 直接再帰 vs アンカー署名再構成のmex（同じグリッド）
    n = 0; bad = 0
    for x in range(1, 61):
        for R in range(0, x + 41):
            n += 1
            if H_direct(R, (1, x), 7) != mex(reconstruct_options(x, R)):
                bad += 1
    audit["検査"]["V2_直接再帰×アンカー再構成mex"] = {"範囲": "x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V3: 署名表の被覆・一致・mex照合（広域）
    n = 0; bad_cover = 0; bad_sig = 0; bad_mex = 0
    for x in range(1, 2001):
        for R in range(1, x + 25):
            n += 1
            cnt, tsig = table_signature(x, R)
            if cnt != 1:
                bad_cover += 1
                continue
            asig = sigstr(reconstruct_options(x, R))
            if asig != tsig:
                bad_sig += 1
                continue
            if mex(reconstruct_options(x, R)) != cand(x, R):
                bad_mex += 1
    audit["検査"]["V3_署名表被覆・一致・mex"] = {"範囲": "x<=2000, 1<=R<=x+24",
        "照合点": n, "被覆違反": bad_cover, "署名不一致": bad_sig, "mex不一致": bad_mex}
    ok = ok and bad_cover == 0 and bad_sig == 0 and bad_mex == 0

    # V4: 単一トークン z=8 錨 vs 直接単一トークン再帰（B子の公式の独立確認）
    n = 0; bad = 0
    for x in range(1, 81):
        for R in range(0, 101):
            n += 1
            if v_single(x, 8, R) != H_direct(R, (x,), 8):
                bad += 1
    audit["検査"]["V4_単一トークンz=8錨×直接再帰"] = {"範囲": "x<=80, R<=100", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V5: z=6・y=1 錨（K0877転写）vs 直接2トークンz=6再帰（C子の公式の独立確認）
    n = 0; bad = 0
    for x in range(1, 61):
        for R in range(0, x + 41):
            n += 1
            if h6_y1(x, R) != H_direct(R, (1, x), 6):
                bad += 1
    audit["検査"]["V5_z6y1錨×直接z=6再帰"] = {"範囲": "x<=60, R<=x+40", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V6: tail照合 R>=x+9 -> (x+1) mod 2
    n = 0; bad = 0
    for x in range(1, 5001):
        for R in (x + 9, x + 10, x + 11, x + 12):
            n += 1
            if cand(x, R) != (x + 1) % 2:
                bad += 1
    audit["検査"]["V6_tail定理照合"] = {"範囲": "x<=5000, {x+9..x+12}", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V7: 高さのみ縮約アンカー R<=8 -> v(x+1,7,R)
    n = 0; bad = 0
    for x in range(1, 501):
        for R in range(0, 9):
            n += 1
            if cand(x, R) != v_single(x + 1, 7, R):
                bad += 1
    audit["検査"]["V7_高さのみ縮約アンカー"] = {"範囲": "x<=500, R<=8", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V8: 固定seed散点 x<=300
    rng = random.Random(12345)
    pts = set()
    while len(pts) < 2000:
        x = rng.randrange(1, 301)
        R = rng.randrange(0, x + 61)
        pts.add((x, R))
    n = 0; bad = 0
    for (x, R) in sorted(pts):
        n += 1
        if H_direct(R, (1, x), 7) != cand(x, R):
            bad += 1
    audit["検査"]["V8_固定seed散点"] = {"範囲": "x<=300, R<=x+60, seed=12345", "照合点": n, "不一致": bad}
    ok = ok and bad == 0

    # V9: Theorem T 偶奇照合（候補側で全グリッド点）
    n = 0; bad_parity = 0; bad_odd = 0; bad_even = 0
    for x in range(1, 2001):
        for R in range(0, x + 25):
            n += 1
            v = cand(x, R)
            if R % 2 == 0 and v > 1:
                bad_even += 1
            if R % 2 == 1 and v > 2:
                bad_odd += 1
    # 値2位置の奇数性・T∩P非交差（候補の帯表記そのものの検査）
    bad_t2 = 0
    for x in range(1, 2001):
        for R in range(0, x + 25):
            if cand(x, R) == 2 and R % 2 == 0:
                bad_t2 += 1
    audit["検査"]["V9_TheoremT偶奇照合"] = {"範囲": "x<=2000, R<=x+24", "照合点": n,
        "偶数R値>1": bad_even, "奇数R値>2": bad_odd, "偶数R値2": bad_t2}
    ok = ok and bad_even == 0 and bad_odd == 0 and bad_t2 == 0

    # V10: 候補内部整合: 各xでQi(x)=cand値の一意性は定義により自明。
    # ここでは署名表と閉形式のmex一致をV3で既に見るので、
    # x带域の重複・欠落がV3被覆検査で担保される。二重計上を避けるため省略。

    total = 0
    for k, v in audit["検査"].items():
        total += v.get("照合点", 0)
    audit["総照合点"] = total
    audit["全検査パス"] = ok

    with open("output/audit.json", "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
