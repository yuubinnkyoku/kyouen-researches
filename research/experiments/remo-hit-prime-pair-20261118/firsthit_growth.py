#!/usr/bin/env python3
"""FIRSTHIT-GROWTH: P-KILL-TIGHT初回ヒット増大則の定量評価（決定的・監査外）。

入力はすべて本実験dirの出版済みoutputs（tier3 = 素数M<=199 x K<=1e7 per-kappa
first・tier4_slim = M in [211,997] x K<=2e5・tier5_slim = M in [1009,1999]
x K<=2e5・pkill_probe_deep.json = 打ち切り済み2クラスの深部プローブ）。
出力 output/firsthit_growth.json は純関数として再生成可能（乱数・時刻不使用）。

内容:
  F(M) := Mのlive κクラスの初回ヒット位置の最大値。
  - tier3（K<=1e7・46素数）は打ち切りなし完全データ。
  - tier4/5（K<=2e5）は missing 空なら完全・そうでなければ
    pkill_probe_deep.json の first_hits[0] で補完（(1367,682)=215458・
    (1741,648)=220140）。
  - log-log回帰 F ~ A * M^beta（tier3完全データ上）。
  - 包絡比 F/(M ln^2 M)・F/(M ln M) のM帯別最大値。
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, "output", name), encoding="utf-8") as f:
        return json.load(f)


def main():
    tier3 = load("pkill_tight_tier3.json")
    tier4 = load("pkill_tight_tier4_slim.json")
    tier5 = load("pkill_tight_tier5_slim.json")
    deep = load("pkill_probe_deep.json")

    # 深部プローブで解消済みの遅いクラス: (M, kappa) -> first hit
    deep_first = {(rec["M"], rec["kappa"]): rec["first_hits"][0] for rec in deep}

    per_M = []  # (M, Kmax, F, fully_resolved)
    censored_details = []
    for src in (tier3, tier4, tier5):
        for key, e in sorted(src.items(), key=lambda kv: int(kv[0])):
            M, Kmax = e["M"], e["Kmax"]
            if "first" in e:  # per-kappa (tier3)
                F = max(e["first"].values())
                missing = e.get("missing", [])
            else:
                F = e.get("max_first_K", 0)
                missing = e.get("missing", [])
            resolved = True
            if missing:
                # 打ち切りクラスを深部プローブの初回ヒットで補完
                deep_hits = [deep_first[(M, kap)] for kap in missing
                             if (M, kap) in deep_first]
                unres = [kap for kap in missing if (M, kap) not in deep_first]
                if deep_hits:
                    F = max(F, max(deep_hits))
                if unres:
                    resolved = False
                    censored_details.append(
                        {"M": M, "unresolved_kappa": unres, "Kmax": Kmax})
            per_M.append({"M": M, "Kmax": Kmax, "F": F, "resolved": resolved})

    for rec in per_M:
        M, F = rec["M"], rec["F"]
        lnM = math.log(M)
        rec["F_over_M"] = F / M
        rec["F_over_MlnM"] = F / (M * lnM)
        rec["F_over_Mln2M"] = F / (M * lnM * lnM)

    # log-log回帰は完全解決済みtier3（K<=1e7・打ち切りなし）上で
    t3 = [r for r in per_M if r["Kmax"] == 10000000 and r["resolved"]]
    xs = [math.log(r["M"]) for r in t3]
    ys = [math.log(r["F"]) for r in t3]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    beta = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))
    A = math.exp(my - beta * mx)
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (math.log(A) + beta * x)) ** 2 for x, y in zip(xs, ys))
    r2 = 1 - ss_res / ss_tot

    # 残差と ln M / ln^2 M の相関（冪則で十分かのチェック）
    resid = [y - (math.log(A) + beta * x) for x, y in zip(xs, ys)]

    def corr(a, b):
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        num = sum((u - ma) * (v - mb) for u, v in zip(a, b))
        den = math.sqrt(sum((u - ma) ** 2 for u in a)
                        * sum((v - mb) ** 2 for v in b))
        return num / den

    resid_lnM = corr(xs, resid)
    resid_ln2 = corr([x * x for x in xs], resid)

    # M帯別の包絡比最大値（完全解決済みデータのみ）
    bands = [
        ("M in [2,199] (K<=1e7, complete)", lambda M: M <= 199),
        ("M in [211,997] (K<=2e5)", lambda M: 211 <= M <= 997),
        ("M in [1009,1999] (K<=2e5)", lambda M: M >= 1009),
        ("M >= 100 (all resolved)", lambda M: M >= 100),
        ("M >= 1000 (all resolved)", lambda M: M >= 1000),
    ]
    band_stats = []
    resolved = [r for r in per_M if r["resolved"]]
    for label, pred in bands:
        sel = [r for r in resolved if pred(r["M"])]
        if not sel:
            continue
        w1 = max(sel, key=lambda r: r["F_over_Mln2M"])
        w2 = max(sel, key=lambda r: r["F_over_MlnM"])
        band_stats.append({
            "band": label, "n": len(sel),
            "max_F_over_Mln2M": round(w1["F_over_Mln2M"], 3),
            "argmax_M_Mln2M": w1["M"], "argmax_F_Mln2M": w1["F"],
            "max_F_over_MlnM": round(w2["F_over_MlnM"], 3),
            "argmax_M_MlnM": w2["M"], "argmax_F_MlnM": w2["F"],
        })

    # 遅い2クラスの包絡比（補完後）
    late = []
    for (M, kap), fh in sorted(deep_first.items()):
        if fh is None:
            continue
        lnM = math.log(M)
        late.append({
            "M": M, "kappa": kap, "first_hit": fh,
            "F_over_Mln2M": round(fh / (M * lnM * lnM), 3),
        })

    out = {
        "analysis": "FIRSTHIT-GROWTH: max over live kappa classes of first-hit position F(M)",
        "sources": ["pkill_tight_tier3.json", "pkill_tight_tier4_slim.json",
                    "pkill_tight_tier5_slim.json", "pkill_probe_deep.json"],
        "n_primes": len(per_M),
        "n_resolved": len(resolved),
        "censored_unresolved": censored_details,
        "loglog_fit_tier3_complete": {
            "model": "F ~ A * M^beta", "n": n, "A": round(A, 4),
            "beta": round(beta, 4), "R2": round(r2, 4),
            "corr_residual_lnM": round(resid_lnM, 4),
            "corr_residual_ln2M": round(resid_ln2, 4),
        },
        "band_envelope_stats": band_stats,
        "late_classes_from_deep_probe": late,
        "per_M": sorted(per_M, key=lambda r: r["M"]),
    }
    path = os.path.join(HERE, "output", "firsthit_growth.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", path)
    print(json.dumps(out["loglog_fit_tier3_complete"], ensure_ascii=False))
    for b in band_stats:
        print(json.dumps(b, ensure_ascii=False))
    print("late:", json.dumps(late, ensure_ascii=False))


if __name__ == "__main__":
    main()
