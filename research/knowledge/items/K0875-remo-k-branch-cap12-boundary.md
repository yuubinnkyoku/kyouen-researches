---
id: K0875
title: 3枝REMO決定性のサイズ境界cap≤12拡張（非坍縮キーは定理Hの22個のまま）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap12 size boundary]
relations:
- type: depends_on
  target: K0861
  note: 定理E′（atomプロファイルへの軌道簡約・全称）でプロファイル判定が盤に転送される
- type: depends_on
  target: K0862
  note: エンジンverbatim供給・定理H（cap≤10の22非坍縮キー）・22×2最小witness・Burnside機構
- type: depends_on
  target: K0864
  note: r=3 (8,8,9)/(8,9,9)分割計数の出版定数
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（2剰余キー分類・r=3剰余対{0,2}）
artifacts:
- path: research/experiments/remo-k-branch-cap12-boundary-20261116/report.md
  role: data
  note: 定理H12主張・Burnside/直接列挙対照表・アンカー一覧・限界
- path: research/experiments/remo-k-branch-cap12-boundary-20261116/verify_remo_k_branch_cap12_boundary.py
  role: verifier
  note: cap≤12完全スイープ・出版定数埋込み・二重実行バイト同一・stdlibのみの検証器
- path: research/experiments/remo-k-branch-cap12-boundary-20261116/output/remo_k_branch_cap12_boundary_audit.json
  role: data
  note: 22キー分割・witness・新キーセンサス・det_map全記録と機械チェック19件
scope: "3枝REMO、r=3、枝サイズ≤12（正準形47,595プロファイル・1,365キー）の有限完全列挙。r≥4・枝サイズ11,12の組合せは未走査。枝サイズ≥13は未走査。"
evidence: "K0862検証器のエンジンをverbatim使用した単一検証器（stdlibのみ・決定的・main二重実行バイト同一）でcap≤12全域をスイープ。Burnside固定点計数と直接正準化列挙がcap 10/11/12すべてで一致し、プロファイル集合の入れ子D_10⊂D_11⊂D_12を確認。定理Hの22キー・K0862出版witness・K0864出版分割計数を機械抽出定数として再現。"
---

## 主張

**定理H12（cap≤12・r=3・有限完全）**: 3枝点族で全枝サイズC_i≤12・任意γのとき、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**定理H（cap≤10）の22個と同一の集合**である。サイズ境界を10→12へ広げても非坍縮キーは0個増える。

付随する確定事実:

- 軌道数はcap 10/11/12で15,863/28,065/47,595（Burnside固定点計数と直接正準化列挙の2通りで一致。fix(id),fix(trans),fix(cyc)=(84494,3478,125)/(152171,5299,161)/(261749,7805,203)）。キー数715/1,001/1,365。D_10⊂D_11⊂D_12。
- **サイズ11枝を含む363キー・サイズ12枝を含む364キー（和集合650）はすべて坍縮**。失敗キーでサイズ8枝を含まないものはない（22/22）。cap≤11でもサイズ11枝を含む286キーは全て坍縮。
- 2剰余キー（{C_i mod 3}がちょうど2種）は890個で、非坍縮は同じ22個のみ（K0872剰余対{0,2}）。
- 22キーの構造はcap≤10と完全不変: 決定側生存者一様P_1、非決定側可能生存者集合⊆{{1,2},{0,1,2}}、r=3分割計数はK0862/K0864出版表と一致、K0862出版witness 44組は有効最小witnessのまま。
- 補題FL（可能第1敗者=={C_i mod 3}）はcap≤12全プロファイルで違反0。Δ=0プロファイルはすべて定理D値で決定的。定理F′閉形式はmin C_i≥3・C_i≤12の全1,155 (family,γ)対で領域ゲームと完全一致。定理D再帰はK0859出版(C,r)表84エントリと完全一致。22キー最小witnessはセルレベル対局樹でも同一成果（定理E′アンカー）。

## 限界

r=3のみ。**r≥4で枝サイズ11,12を含むキーは未走査**（K0864/K0866/K0869のr=4..8境界はcap≤10上限）。枝サイズ≥13は未走査で「サイズ8が失敗に必要」はサイズ≤12でのみ確定。非坍縮22キーの構造的特徴づけ（なぜサイズ8か）は未解決で、本項は列挙であり特徴づけではない。非坍縮キー内でも非決定側の可能生存者集合はatom配分依存のまま。11×11空盤はUNKNOWNのまま。
