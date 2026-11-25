---
id: K0882
title: 3枝REMO決定性のサイズ境界cap≤13拡張（非坍縮キーは定理Hの22個のまま）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap13 size boundary]
relations:
- type: depends_on
  target: K0875
  note: 定理H12（cap≤12・r=3の22非坍縮キー）・Burnside/正準列挙機構・22キー構造定数
- type: depends_on
  target: K0876
  note: r=3 packed出版レコード47,595件（順序保存部分列位置で全件再現・sha256ピン付き照合）と監査JSONのr=3 22キー分割表、ならびに検証器のverbatim供給（エンジン・列挙・mask twin・K0862 witness定数）
- type: depends_on
  target: K0862
  note: 定理Hの22キー・出版44 witness（本項でもverbatim再検証）
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（非坍縮⇒2剰余の必要条件観察のサイズ13へのアウトオブサンプル拡張）
- type: depends_on
  target: K0864
  note: 全称補題FL（可能第1敗者=={C_i mod r}）のcap≤13全プロファイルでの違反0拡張
artifacts:
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/report.md
  role: data
  note: 定理H13主張・Burnside対照表・交差アーティファクト照合・限界
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/verify_remo_k_branch_cap13_boundary.py
  role: verifier
  note: committed packed records照合・K0876出版レコード・監査との交差照合・Python twin live checks・19機械チェック・assemble二重実行byte同一・stdlibのみ
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/mask_engine_fast.js
  role: solver
  note: 決定的JavaScript maskエンジン（K0876系譜・r=3・正準cap≤13列挙77,828プロファイル一括スイープ）
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/pack_records.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript（再実行でbyte同一を確認済み）
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/output/js_cap13_r3.packed.jsonl
  role: data
  note: r=3決定的sweepレコード77,828件・packed出版形式 [i, sv_mask, fl_mask, states]（sha256 47a5eb34f738dc60a74d4ef0c66e54032d7c79f2e3413b47c40dbc56c07df5fd・atomsは検証器内の正準列挙で無損失再構成）
- path: research/experiments/remo-k-branch-cap13-boundary-20261116/output/remo_k_branch_cap13_boundary_audit.json
  role: data
  note: 19機械チェック・cap13センサス・22キー分割・剰余レンズ・K0876交差照合の全記録
scope: "3枝REMO、r=3、枝サイズ≤13（正準形77,828プロファイル・1,820キー）の有限完全列挙。r≥4で枝サイズ11以上を含むキーは本項では未走査。枝サイズ≥14は未走査。"
evidence: "決定的JavaScript maskエンジンで生成したコミット済みsweepレコード（77,828件・packed出版形式・sha256照合・検証器内で無損失再構成）を、出版済みK0876検証器からverbatim抽出したエンジン・列挙・Python mask twinで検証。19機械チェック（Burnside一致・レコード形式・センサス・22キー分割・ndet生存者集合・決定側一様P_1・FL違反0・剰余類計数・枝サイズ統計）に加え、正準列挙の順序保存部分列性を用いてK0876出版r=3レコード47,595件をD_12対応位置で全件再現（0不一致・sha256ピン付き）、K0876監査JSONの22キー分割表と突合。live checkとしてcap≤7全域2,048 verdictsでverbatim==mask twin==committed、stride 32層化サンプル2,433 verdicts、K0862出版44 witnessをverbatimエンジンで再検証。assemble二重実行byte同一。"
---

## 主張

**定理H13（cap≤13・r=3・有限完全）**: 3枝点族で全枝サイズ C_i≤13・任意γ のとき、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**定理H（cap≤10）の22個と同一の集合**である。サイズ境界を 10→12→13 へ広げても非坍縮キーは0個増える。

付随する確定事実:

- 軌道数はcap 13で77,828（Burnside fix(id),fix(trans),fix(cyc)=(432,906, 11,186, 252)・直接正準化列挙と一致）。キー数1,820=一様決定313+一様非決定1,485+mixed 22。
- **サイズ13枝を含む455キーはすべて坍縮**（サイズ11枝451キー・サイズ12枝454キーもすべて坍縮）。
- 22キーの構造はcap≤10/12と完全不変: 決定側生存者一様P_1、非決定側可能生存者集合⊆{{1,2},{0,1,2}}、per-key分割はK0876監査sweeps.r3.failing_partitionsと完全一致、K0862出版44 witnessは本設定でも有効。
- 補題FL（可能第1敗者=={C_i mod 3}）はcap≤13全77,828プロファイルで違反0（cap≤12観察の拡張）。
- 剰余レンズ（K0872）: 22 mixedキーはすべて剰余対{0,2}。1剰余330キー・3剰余300キーはすべて坍縮。2剰余キー1,190個のうち非坍縮は同じ22個のみ。「非坍縮⇒|L_3|=2」の必要条件観察はサイズ13までアウトオブサンプルで無反例。
- 最大状態数48,256（状態総数294,553,171）。

## 限界

r=3のみ。r≥4で枝サイズ11,12,13を含むキーは本項では未走査（K0876はr=4,5,6・cap≤12、r=7,8は進行中の別作業）。**枝サイズ≥14は未走査**で「サイズ8が失敗に必要」はサイズ≤13でのみ確定。非坍縮22キーの構造的特徴づけ（なぜサイズ8か）は未解決のまま。「非坍縮⇒2剰余」は必要条件の有限観察であり一般の証明ではない。本項の有限観察を全称定理へ昇格させない。11×11空盤はUNKNOWNのまま。
