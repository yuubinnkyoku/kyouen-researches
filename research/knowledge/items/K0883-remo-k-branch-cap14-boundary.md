---
id: K0883
title: 3枝REMO決定性のサイズ境界cap≤14拡張（境界は13で閉じず30新キーが出現）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap14 size boundary]
relations:
- type: depends_on
  target: K0882
  note: 定理H13（cap≤13・r=3の22非坍縮キー）・r=3 packed出版レコード77,828件（D_13部分列位置で全件再現・sha256ピン付き照合）・検証器のverbatim供給（エンジン・列挙・mask twin・K0862 witness定数）
- type: depends_on
  target: K0876
  note: 監査JSONのr=3 22キー分割表（定理Hキーはcap≤14でも同値・sha256ピン付き照合）と検証器系譜（packed読み取り修復版）
- type: depends_on
  target: K0862
  note: 定理Hの22キー・出版44 witness（本項でもverbatim再検証）
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（非坍縮⇒剰余対{0,2}の必要条件観察のサイズ14へのアウトオブサンプル拡張・52キー全部で{0,2}）
- type: depends_on
  target: K0864
  note: 全称補題FL（可能第1敗者=={C_i mod r}）のcap≤14全プロファイルでの違反0拡張
artifacts:
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/report.md
  role: data
  note: 定理H14主張・Burnside対照表・K0882交差照合・置換対応の有限観察・限界
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/verify_remo_k_branch_cap14_boundary.py
  role: verifier
  note: committed packed records（part1of2/part2of2・per-part shaピン）照合・K0882出版レコード・K0876監査との交差照合・Python twin live checks・21機械チェック・assemble二重実行byte同一・stdlibのみ
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/mask_engine_fast.js
  role: solver
  note: 決定的JavaScript maskエンジン（K0876系譜・r=3・正準cap≤14列挙123,272プロファイル一括スイープ・324.6秒）
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/pack_records.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/output/js_cap14_r3.packed.jsonl.part1of2
  role: data
  note: r=3決定的sweepレコード前半61,636件（sha256 f627814d1c8b484d5aab36f6054005b757e49f3e53f491c141e5d9fa5dad5d5d）
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/output/js_cap14_r3.packed.jsonl.part2of2
  role: data
  note: r=3決定的sweepレコード後半61,636件（sha256 7848e20cfc142db1e3e8fbb754503c15405ef57af5f252f5c5fba009c833d6d0）。join byte正確でpacked blob（123,272件・sha256 710f328936340c2a2ab4316cde4316942a677207dd29ec1dc52af7c9cb786644）と一致
- path: research/experiments/remo-k-branch-cap14-boundary-20261116/output/remo_k_branch_cap14_boundary_audit.json
  role: data
  note: 21機械チェック・cap14センサス・52キー分割・剰余レンズ・K0882/K0876交差照合の全記録
scope: "3枝REMO、r=3、枝サイズ≤14（正準形123,272プロファイル・2,380キー）の有限完全列挙。r≥4で枝サイズ13以上を含むキーは本項では未走査。枝サイズ≥15は未走査。"
evidence: "決定的JavaScript maskエンジンで生成したコミット済みsweepレコード（123,272件・packed出版形式・part1of2/part2of2分割コミット・per-part sha256照合・検証器内で無損失再構成）を、出版済みK0882検証器からverbatim系譜のエンジン・列挙・Python mask twinで検証。21機械チェック（Burnside一致・レコード形式・センサス・52キー完全一致・H22残留・新キー全てサイズ14枝・per-key分割・ndet生存者集合・決定側一様P_1・FL違反0・剰余類計数・枝サイズ統計）に加え、正準列挙の順序保存部分列性を用いてK0882出版r=3レコード77,828件をD_13対応位置で全件再現（0不一致・sha256ピン付き）、K0876監査JSONの定理H 22キー分割表と突合（不変を確認）。live checkとしてcap≤7全域2,048 verdictsでverbatim==mask twin==committed、stride 32層化サンプル3,853 verdicts、K0862出版44 witnessをverbatimエンジンで再検証。assemble二重実行byte同一。"
---

## 主張

**定理H14（cap≤14・r=3・有限完全）**: 3枝点族で全枝サイズ C_i≤14・任意γ のとき、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**ちょうど52個**である: 定理H（cap≤10）の22個 + **30個の新キー**。

- サイズ境界を 10→12→13 へ広げても新規0だった安定化は**14で破れる**。30個の新キーはすべてサイズ14枝を含む（サイズ14枝を含む560キーのうち30個がmixed）。
- 新キーは9つのサイズ多重集合: (2,3,14),(2,9,14),(3,3,14),(3,8,14),(3,9,14),(3,14,14)×γ=0..1（12キー）と (8,9,14),(9,9,14),(9,14,14)×γ=0..5（18キー）。
- **有限観察（全称主張ではない）**: 9つの新多重集合はいずれも定理Hの7つの多重集合の{8,9}要素の1〜2個を14に置き換えた形で、γ範囲もsourceと一致する。ただし逆は成り立たない（候補11のうち(2,8,14),(8,8,14)は坍縮）。14 ≡ 8 ≡ 2 (mod 3)。
- 定理Hの22キーのper-key分割はcap≤14でも完全不変（K0876監査sweeps.r3.failing_partitionsと完全一致）。決定側生存者は52キーすべて一様P_1。非決定側可能生存者集合⊆{{1,2},{0,1,2}}。

付随する確定事実:

- 軌道数はcap 14で123,272（Burnside fix(id),fix(trans),fix(cyc)=(692,102, 15,638, 308)・直接正準化列挙と一致）。キー数2,380=一様決定349+一様非決定1,979+mixed 52。
- サイズ11枝550キー・サイズ12枝556キー・サイズ13枝559キーはすべて坍縮。
- 52キーすべて剰余対{0,2}。1剰余420キー・3剰余400キーはすべて坍縮。2剰余1,560キーの非坍縮は52個のみ。
- 補題FL（可能第1敗者=={C_i mod 3}）はcap≤14全123,272プロファイルで違反0。
- 最大状態数74,695（状態総数686,151,143）。
- 正準列挙の順序保存部分列性（D_13⊂D_14）によりK0882出版r=3 packedレコード77,828件をD_13対応位置で全件再現（0不一致）。

## 限界

r=3のみ。r≥4で枝サイズ13,14を含むキーは本項では未走査（K0876はr=4,5,6・cap≤12）。**枝サイズ≥15は未走査**で、サイズ15（≡0 (mod 3)・9と同剰余）でも同様の新キー族が出るかは次の検証課題。「サイズ8が失敗に必要」はサイズ≤13でのみ成立し、サイズ14で(2,3,14)等が反例（K0882 reportのguardどおり）。置換対応の有限観察は一般則ではない。「非坍縮⇒2剰余{0,2}」は必要条件の有限観察であり一般の証明ではない。本項の有限観察を全称定理へ昇格させない。11×11空盤はUNKNOWNのまま。
