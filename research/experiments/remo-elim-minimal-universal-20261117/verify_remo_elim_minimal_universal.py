#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K0924 verifier: 定理W（elim(1+d,r)=elim(1,r) ⟺ Q(r)|d・全称）と
系MPV（敗者全列の最小周期 = Q(r)・全r≥2）の機械検証。

機械チェック:
  M0  lcm恒等式: lcm({r} ∪ {k(k+1): k=2..r-1}) == lcm(1..r) (r=2..40)
  M1  witness C=1（elim列・r=2..16）: Q(r)の全真約数dでelim(1+d)≠elim(1)
      （K0922 witness主張の直接再現・窓走査不要の高速版）
  M2  witness C=1（elim列・r=17..40）: 同上の拡張（新規・全真約数）
  M3  カスケード予測（r=2..24・Qの全約数+2Q+3Q）:
      elim(1+d)とelim(1)の最初の発散フェーズ == 予測
      （r∤d→フェーズ1 / r|d→最小h≥2で(r-h+2)(r-h+1)∤d / なし→全一致=Q|d）
  M3b カスケード予測の深い場合のみ（r=25..40・r|d真約数+Q・2Q）
  M4  同値性（r=2..16・混合d: 約数+非約数+決定的LCG擬似乱数600点/r）:
      elim(1+d)==elim(1) ⟺ Q(r)|d
  M5  周期方向アンカー（r=2..40）: elim(1+Q)==elim(1) かつ elim(1+2Q)==elim(1)
  M6  生存者列のC=1失敗記録（r=2..16）: sv(1+d)==0となる真約数dのリスト
      （生存者列ではC=1がwitnessにならないdが存在することの記録・全称性はOPEN）
  M8  全評価で elim(C,r)[0] == C % r（第1敗者の閉形式・インライン表明）

stdlibのみ・決定的・監査JSONは実行時間を含まないためbyte同一。
per-r checkpointでM2はresumable。--no-cache で全再計算。
"""
import json, os, sys, time

R2MAX = 40          # M2の上限r
M3MAX = 24          # M3の全約数走査上限r
M4RAND = 600        # M4のLCGサンプル数/r
LCG_A, LCG_C, LCG_M = 6364136223846793005, 1442695040888963407, 2**64

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "output")
CKPTDIR = os.path.join(OUTDIR, "checkpoints")

def theorem_d_fast(C, r):
    """K0859定理Dの計数再帰（Δ=0一様盤・閉形式双子）。戻り値 (elim, survivor)。"""
    active = list(range(r)); counts = [0]*r; turn = 0; elimination = []
    while len(active) > 1:
        k = len(active); s = sum(counts[p] for p in active); ell = C - s
        q, t = divmod(ell, k)
        for i in range(k):
            pos = active[(turn + i) % k]; counts[pos] += q + (1 if i < t else 0)
        li = (turn + ell) % k; loser = active[li]
        elimination.append(loser); counts[loser] = 0; active.pop(li)
        if active: turn = li % len(active)
    return tuple(elimination), active[0]

def checked(C, r):
    """M8: 第1敗者閉形式 elim(C,r)[0]==C%r を表明つきで評価。"""
    el, sv = theorem_d_fast(C, r)
    assert el[0] == C % r, ("M8 violated", C, r, el[0])
    return el, sv

def lcm_all(r):
    out = 1
    for i in range(2, r + 1):
        a, b = out, i
        while b: a, b = b, a % b
        out = out * i // a
    return out

def lcm_list(xs):
    out = 1
    for x in xs:
        a, b = out, x
        while b: a, b = b, a % b
        out = out * x // a
    return out

def divisors(n):
    out = []; i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i: out.append(n // i)
        i += 1
    return sorted(out)

def first_div_phase_pred(d, r):
    """定理Wのカスケード予測: 最初の発散フェーズ。None は全一致予測（Q|d）。"""
    if d % r != 0: return 1
    for h in range(2, r):
        k = r - h + 1
        if d % (k * (k + 1)) != 0: return h
    return None

def first_div_phase_actual(d, r, e1=None):
    if e1 is None: e1 = checked(1, r)[0]
    ea, _ = checked(1 + d, r)
    for j in range(len(e1)):
        if ea[j] != e1[j]: return j + 1
    return None

class LCG:
    def __init__(self, seed): self.s = seed % LCG_M
    def next(self, n):
        self.s = (LCG_A * self.s + LCG_C) % LCG_M
        return (self.s >> 33) % n + 1

def m2_scan(r, use_cache=True):
    """M2/M1本体: rのQ(r)全真約数でelim(1+d)≠elim(1)。per-r checkpoint。"""
    ck = os.path.join(CKPTDIR, "m2_r%d.json" % r)
    if use_cache and os.path.exists(ck):
        with open(ck) as f: return json.load(f)
    Q = lcm_all(r)
    e1 = checked(1, r)[0]
    ds = divisors(Q)[:-1]
    agree = [d for d in ds if checked(1 + d, r)[0] == e1]
    rec = {"r": r, "Q": Q, "proper_divisors": len(ds), "agreements": agree}
    with open(ck, "w") as f: json.dump(rec, f, sort_keys=True)
    return rec

def main():
    t0 = time.time()
    no_cache = "--no-cache" in sys.argv
    if no_cache and os.path.isdir(CKPTDIR):
        for fn in os.listdir(CKPTDIR): os.remove(os.path.join(CKPTDIR, fn))
    os.makedirs(CKPTDIR, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)

    # M0: lcm恒等式 r=2..40
    m0 = []
    for r in range(2, R2MAX + 1):
        L = lcm_list([r] + [k * (k + 1) for k in range(2, r)])
        m0.append(L == lcm_all(r))
    assert all(m0), "M0"

    # M1+M2: witness C=1 (elim列) r=2..40 全真約数
    m12 = [m2_scan(r, use_cache=not no_cache) for r in range(2, R2MAX + 1)]
    for rec in m12: assert rec["agreements"] == [], ("M1/M2 agreement", rec["r"])
    m1 = [rec for rec in m12 if rec["r"] <= 16]
    m2 = [rec for rec in m12 if rec["r"] >= 17]

    # M3: 最初の発散フェーズ予測 r=2..24（Qの全約数+2Q+3Q）
    m3_total = 0; m3_bad = []
    for r in range(2, M3MAX + 1):
        Q = lcm_all(r); e1 = checked(1, r)[0]
        for d in divisors(Q) + [2 * Q, 3 * Q]:
            p = first_div_phase_pred(d, r); a = first_div_phase_actual(d, r, e1)
            m3_total += 1
            if p != a: m3_bad.append([r, d, p, a])
    assert not m3_bad, ("M3", m3_bad[:5])

    # M3b: 深い場合のみ r=25..40（r|d真約数+Q・2Q）
    m3b_total = 0; m3b_bad = []
    for r in range(M3MAX + 1, R2MAX + 1):
        Q = lcm_all(r); e1 = checked(1, r)[0]
        deep = [d for d in divisors(Q) if d % r == 0]
        for d in deep + [Q, 2 * Q]:
            p = first_div_phase_pred(d, r); a = first_div_phase_actual(d, r, e1)
            m3b_total += 1
            if p != a: m3b_bad.append([r, d, p, a])
    assert not m3b_bad, ("M3b", m3b_bad[:5])

    # M4: 同値性 r=2..16（約数+定数+LCG600点）
    m4_total = 0; m4_bad = []
    for r in range(2, 17):
        Q = lcm_all(r); e1 = checked(1, r)[0]
        cands = set(divisors(Q)) | {Q + 1, Q - 1, 2 * Q, 3 * Q, Q + Q // 2,
                                    2, 3, 5, 7, 13, Q // 2 + 1 if Q % 2 == 0 else Q + 2}
        g = LCG(20261117 + r)
        for _ in range(M4RAND): cands.add(g.next(4 * Q))
        for d in sorted(x for x in cands if x >= 1):
            eq = checked(1 + d, r)[0] == e1
            pred = (d % Q == 0)
            m4_total += 1
            if eq != pred: m4_bad.append([r, d, eq, pred])
    assert not m4_bad, ("M4", m4_bad[:5])

    # M5: 周期方向アンカー r=2..40
    m5 = []
    for r in range(2, R2MAX + 1):
        Q = lcm_all(r); e1 = checked(1, r)[0]
        ok = checked(1 + Q, r)[0] == e1 and checked(1 + 2 * Q, r)[0] == e1
        m5.append({"r": r, "Q": Q, "elim_1pQ_eq": ok})
    assert all(x["elim_1pQ_eq"] for x in m5), "M5"

    # M6: 生存者列のC=1失敗記録 r=2..16
    m6 = []
    for r in range(2, 17):
        Q = lcm_all(r)
        fail = [d for d in divisors(Q)[:-1] if checked(1 + d, r)[1] == 0]
        m6.append({"r": r, "Q": Q, "sv_fail_d": fail, "sv_fail_count": len(fail)})

    audit = {
        "item": "K0924",
        "title": "定理W: elim(1+d,r)=elim(1,r) ⟺ Q(r)|d (全称) / 系MPV: 敗者全列最小周期=Q(r) (全r>=2)",
        "depends_on": ["K0919", "K0922", "K0859"],
        "checks": {
            "M0_lcm_identity_r2_40": {"n": len(m0), "all_true": all(m0)},
            "M1_witness_c1_elim_r2_16": {
                "per_r": m1, "total_proper_divisors": sum(x["proper_divisors"] for x in m1),
                "agreements": 0},
            "M2_witness_c1_elim_r17_40": {
                "per_r": m2, "total_proper_divisors": sum(x["proper_divisors"] for x in m2),
                "agreements": 0},
            "M3_first_div_phase_pred_r2_24": {"total": m3_total, "mismatch": 0},
            "M3b_first_div_phase_deep_r25_40": {"total": m3b_total, "mismatch": 0},
            "M4_equivalence_mixed_r2_16": {"total": m4_total, "mismatch": 0},
            "M5_period_anchor_r2_40": {"n": len(m5), "all_true": True},
            "M6_survivor_c1_fail_r2_16": m6,
            "M8_first_loser_closed_form": {"asserted_every_eval": True},
        },
        "survivor_column_note": "生存者全列の最小周期はK0922の機械結果(r<=16)のまま。全称性はOPEN。",
        "all_ok": True,
    }
    path = os.path.join(OUTDIR, "remo_elim_minimal_universal_audit.json")
    with open(path, "w") as f:
        json.dump(audit, f, sort_keys=True, indent=1, ensure_ascii=False)
        f.write("\n")
    print("ALL OK  M3=%d M3b=%d M4=%d  M1+M2 proper=%d  t=%.1fs"
          % (m3_total, m3b_total, m4_total,
             sum(x["proper_divisors"] for x in m12), time.time() - t0))
    print("audit:", path)

if __name__ == "__main__":
    main()
