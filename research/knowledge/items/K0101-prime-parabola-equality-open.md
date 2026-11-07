---
id: K0101
title: 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0097
  note: ''
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 禁止四点の完全対分類とNAE・原点節の厳密な分解。全素数の充足可能性は未証明
- path: research/experiments/frontier-geometry-2026-10-05/recovered-witnesses.json
  role: certificate
  note: 131..251拡張の追跡されていなかった証人を回復・保存
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-witnesses.json
  role: certificate
  note: 509,1009の追加有限等号証人
- path: research/experiments/parabola-equality-extension-20261016/README.md
  role: source
  note: 521..2000への有限拡張。全奇素数の等号は依然未証明
- path: research/experiments/parabola-equality-extension-20261016/output/witnesses_521_2000.json
  role: certificate
  note: 521..1999の全206素数の等号証人
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: certificate
  note: 2003..2477の64素数のうち63の等号証人。2207は深いd走査中
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit.txt
  role: data
  note: generic 4×4 Leibnizによる全63証人の独立検証出力（共円0件）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207_d_verdicts.json
  role: data
  note: p=2207の全1103 dのCNF UNSAT判定（反例候補。DRAT未検査）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/README.md
  role: source
  note: 反例候補の方法・全数照合・信頼境界
scope: 奇素数 p における等号 A(p)=(p+3)/2 の有限検証範囲と d=h 例外の記述。
evidence: finite computation; p=2207で等号証人が存在しない計算結果あり（K0693, needs-review）; それ以外の5..2477は証人あり; all-prime proof unknown
---

# 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定

Q_p内の一般上界は証明済みで、5..2000の全奇素数で安全証人が等号を達成する。
5..127の29素数は既存独立検算。131..251の23素数については追跡されていなかった証人を回復し、
generic 4×4 Leibniz展開で全選択四点を再検査した。257..439の31素数と443..503の11素数も、証明済み必要合同式で全候補を絞った後に直接整数行列式で独立検査した。521..1999の全206素数は
research/experiments/parabola-equality-extension-20261016 で構成し、同じ独立検証器で検査した
（必要合同式を満たす総計2,196,275,194,090四点組のうち1,385,691,858候補に直接整数行列式、共円0件）。
したがって5..2000は穴なく有限確認済み。1009を超える範囲の等号も有限に確認している。

**全奇素数に同じ達成構成があるかは未証明**。2000を超える反例素数も未発見。

K0334は、等号問題をある完全対dについてsigned NAE3/4と原点由来2/3リテラル節の
同時充足可能性へ正確に帰着した。その全称充足可能性も反例素数も未確定。
認証方式の上界や全盤K_pの既知下界とは別の問い。

## 2026-10-17 bounded advance

New finite evidence: `d=h` is sufficient for all primes 5..443 and (newly) 2003..2143, except `d=h-1` for 1087, 1091, 1367, 1523, 1847, 2027 and `d=h-66` for 1861; p=2027 independently verified with `verify_witnesses.cpp`. All 302 odd primes up to 2000 already had equality witnesses; new runs add independently checked witnesses for 2003..2053 and 2069..2143. No counterexample prime to equality found.

Scope clarification: K0101 is not resolved by the `d=h` construction alone; `d=h` works for most primes but has exceptions, so a uniform construction remains unknown.

Next steps: characterize the `d=h` exception pattern; extend finite verification beyond 2143; seek an all-prime proof. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
## 2026-11-07 有限証人の保存拡張（2003..2477）

`research/experiments/parabola-equality-extension-2143-2500-20261107` で 2003..2477 の奇素数 64 個を走査し、
63 個で等号証人を構成・保存した（`d=h-1` は 2027, 2399, 2477、他の 60 は `d=h`）。
2351 は既定設定の cadical がタイムアウトしたが SAT 向け設定（`--sat -L1000`）で `d=h` の解を得た。
証人は探索と独立な generic 4×4 Leibniz 検証器で全件監査済み（共円 0 件）。
これで **5..2203 の全奇素数**と **2213..2477** に証人が存在する。
2207 は `d=h..h-528` の走査で未発見であり（深い d を走査中）、等号不成立の証拠ではない。
2017 の記録が挙げた 2003..2143 の証人も本実験で再構成・保存した。

Scope clarification: 有限範囲の保存証人が 2203 まで延びただけで、全奇素数での等号は依然未解決。
`d=h` の例外分布（h-1 が多いが 1861 は h-66）の特徴づけも未解決。

## 2026-11-08 p=2207 の反例候補（要監査）

上記 2026-11-07 の走査を続けた結果、**p=2207 では d=1..1103 の全 `d` で CNF が UNSAT**
（UNSAT 1103・SAT 0・不明 0）となった。タイムアウトした 4 件（289, 297, 312, 324）は
衝突予算 2000 万で再判定済み。Glucose4 と Minisat22 も d=1,289,550,1103 で UNSAT。
実装の全数照合は p=5..23 の全安全集合列挙と全 `d` で一致（p=23 で 8,064 集合・d 集合一致）。

K0334 の等価（等号 ⟺ ある `d` で CNF 充足可能）とサイズ `h+2` の集合が一完全対構造を取ることから、
`A(2207) <= 1104 < 1105 = (2207+3)/2` が従う。**本問の「全奇素数で等号」は p=2207 で否定される**
（K0693, status needs-review）。ただし UNSAT の DRAT 証明は未取得・未検査であり、本項の status は
open のまま維持する。監査完了後に K0693 を確定し、本項を superseded にする予定。
続いて **p=2531 でも d=1..1265 の全数が UNSAT**（unknown 0）となり、2例目の等号不達成候補
`A(2531) <= 1266 < 1267` が得られた（K0702）。p=2207 では標本 21 d の DRAT 証明を独立チェッカーで
VERIFIED にしたが、p=2531 の監査は未実施。p=2539, 2543, 2549 も d=h..h-30 で証人未発見であり、
反例素数はさらに増える可能性がある。`A(2207)`, `A(2531)` の正確な値は未確定。
