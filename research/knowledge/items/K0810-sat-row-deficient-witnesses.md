---
id: K0810
title: SAT探索による行欠損極大witness — M_{6,5}≥23・M_{6,6}≥20・M_{6,8}≥18・M_{5,6}≥18（K0809候補予想4件の反証）
kind: proposition
status: proved
topics: [rectangles, variants]
aliases: []
relations:
- type: refines
  target: K0808
  note: 貪欲では発見できなかったm帯のwitnessをSATで発見し(6,5)/(6,6)/(6,8)下界を更新
- type: refines
  target: K0809
  note: 行capハンディキャップ貪欲の候補予想 M=22/17/12/16 を4件とも反証
- type: depends_on
  target: K0806
  note: 上界（K0318代入）は不変
artifacts:
- path: research/experiments/row-deficient-sat-witnesses-20261114/scripts/row_deficient_sat.js
  role: experiment
  note: census完全列挙・SAT符号化（sequential counter）・自作CDCL/DPLL・census不使用独立検証器
- path: research/experiments/row-deficient-sat-witnesses-20261114/output/sat_results.json
  role: data
  note: 全16実行・witness座標・独立検証詳細・制御・fuzz記録
- path: research/experiments/row-deficient-sat-witnesses-20261114/report.md
  role: proof
  note: 手法・制御・捕捉した実装バグ4件・未解決の区別
solution:
  board: 6×m・5×m（q=5,6,8・q=6）
  level: strong
  outcome: bounds-only
  classification: [deficient-maximal-witnesses]
  coverage: (6,5) m=22・(6,6) m=17,19・(6,8) m=12..17・(5,6) m=16,17 の各盤
  conditions: q点共円・共線禁止・標準整数格子
  verification: [exhaustive-search-SAT, independent-verification]
  certificate: SAT model（全witnessがcensus不使用独立検証で safe+maximal PASS）
  independent_check: 別プロセスでの再検証・2ソルバ相互検証・全列挙制御（2×8/2×9）・fuzz 800題
  note: 下界更新のみ。timeout した m（(6,8) m=18・(5,6) m=18,19・(5,7) m=19・(6,7) m=20・(6,6) m=18,20,21）は未解決であり不在証明ではない
---

# SAT探索による行欠損極大witness — 4組の下界更新（2026-11-14）

固定幅 w×m・q点共円・共線禁止盤において、欠損極大安全配置（ある行が q−2 石以下の極大安全配置）
の存在は M_{w,q} の下界を与える。K0808/K0809 の貪欲系探索が非発見とした m 帯に対し、
危険曲線censusの完全列挙（直線=全ペア・円=全3点組のCramer整数解）と
sequential counter によるSAT符号化（safety・blocking・行欠損）で自作CDCLを実行し、
以下の検証済みwitnessを発見した（すべてcensus不使用独立検証で safe+maximal PASS）。

- **M_{6,5} ≥ 23**: 23石@6×22（行構成 4,4,4,4,4,3）。
- **M_{6,6} ≥ 20**: 29石@6×17 と 29石@6×19（行構成 5,5,5,5,5,4 / 5,5,5,5,4,5）。
- **M_{6,8} ≥ 18**: 41石@6×12,6×13,6×14,6×15,6×16,6×17 の6盤連続（いずれも41石=満容量42−1）。
  さらに 6×12 には40石・**39石**の極大安全配置も存在する（cap=40・cap=39 SAT・
  行構成 7,7,7,7,5,7 / 5,7,7,7,6,7。いずれも独立検証 PASS。
  6×12 q=8 の最小極大サイズは ≤39 に更新。cap=38 は未解決・不在証明ではない）。
- **M_{5,6} ≥ 18**: 24石@5×16 と 24石@5×17（行構成 5,5,5,5,4 / 5,5,5,4,5）。

これにより K0809 の候補予想 M_{6,5}=22・M_{6,6}=17・M_{6,8}=12・M_{5,6}=16 は反証された
（ヒューリスティックな予想であり、貪欲系探索の非発見 m は実際の不在と系統的にズレる）。
(5,7) m=19・(6,7) m=20 はCDCL予算内で解けず未解決（不在証明ではない）。

現在の境界: M_{6,5} ∈ [23,658]・M_{6,6} ∈ [20,495]・M_{6,8} ∈ [18,371]・
M_{5,6} ∈ [18,249]・M_{5,7} ∈ [19,158]・M_{6,7} ∈ [20,402]。

制御: 6×12・q=8 census 92曲線（K0809と一致）・2×8 q=4 SAT（5石witness・K0796再発見）・
2×9 q=4 UNSAT（CDCL+DPLL+全列挙で M_{2,4}=9 制御）・2×8 全列挙（欠損極大16個・最小5石）・
乱数3-SAT 400題×2ソルバ vs 全列挙（800検査・不一致0）。

実装教訓（いずれも制御/fuzzが実際に捕捉）:
(a) sequential counterの S→Sp∨(x_i∧Spp) の2節分解は必須（1節圧縮で非極大偽witness）、
(b) DPLLの衝突時早期returnは計数のundo対称性を壊す、
(c) CDCLの決定レベルpush忘れは偽UNSAT、
(d) 円の整数係数は (det,−B,−C,−D) で d の符号に注意。
