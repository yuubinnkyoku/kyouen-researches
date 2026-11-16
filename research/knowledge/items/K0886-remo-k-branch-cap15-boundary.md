---
id: K0886
title: 3枝REMO決定性のサイズ境界cap≤15拡張（15世代も新キー族は続き58新キー・γ窓0..9とndet生存者{0,1}の初出現）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap15 size boundary]
relations:
- type: depends_on
  target: K0883
  note: 定理H14（cap≤14・r=3の52非坍縮キー）・r=3 packed出版レコード123,272件（D_14部分列位置で全件再現・sha256ピン付き照合）・検証器のverbatim供給（エンジン・列挙・mask twin・K0862 witness定数）
- type: depends_on
  target: K0876
  note: 監査JSONのr=3 22キー分割表（定理Hキーはcap≤15でも同値・sha256ピン付き照合）と検証器系譜（packed読み取り修復版）
- type: depends_on
  target: K0862
  note: 定理Hの22キー・出版44 witness（本項でもverbatim再検証）
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（非坍縮⇒剰余対{0,2}の必要条件観察のサイズ15へのアウトオブサンプル拡張・110キー全部で{0,2}）
- type: depends_on
  target: K0864
  note: 全称補題FL（可能第1敗者=={C_i mod r}）のcap≤15全プロファイルでの違反0拡張
artifacts:
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/report.md
  role: data
  note: 定理H15主張・Burnside対照表・K0883交差照合・置換対応とγ窓拡張の有限観察・限界
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/verify_remo_k_branch_cap15_boundary.py
  role: verifier
  note: committed packed records（part1of3/part2of3/part3of3・per-part shaピン）照合・K0883出版レコード・K0876/K0883監査との交差照合・Python twin live checks・24機械チェック・assemble二重実行byte同一・stdlibのみ
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/mask_engine_fast.js
  role: solver
  note: 決定的JavaScript maskエンジン（K0876系譜・main出版K0883実験とsha同一・r=3・正準cap≤15列挙189,864プロファイル一括スイープ）
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/pack_records.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript（行境界3分割付き）
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/output/js_cap15_r3.packed.jsonl.part1of3
  role: data
  note: r=3決定的sweepレコード第1部63,288件（sha256 ddda26c93cfc7bc6830f0f6f8a338f854e0cd7b25b6bc598489a8662381b1b34）
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/output/js_cap15_r3.packed.jsonl.part2of3
  role: data
  note: r=3決定的sweepレコード第2部63,288件（sha256 2c30fe0bcf39330b1112deea71b913c5bcf79e2eaa16c0525ca67b3bea44a2d7）
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/output/js_cap15_r3.packed.jsonl.part3of3
  role: data
  note: r=3決定的sweepレコード第3部63,288件（sha256 efa6b55d113378bf7c5ae454882612749b160565ee184a9bfe12c3cabfce1e1f）。3部join byte正確でpacked blob（189,864件・sha256 7c44da46cc65fbc9a88b93c2e26b2a18531738a7da5e5fcce084d5966c002db4）と一致
- path: research/experiments/remo-k-branch-cap15-boundary-20261116/output/remo_k_branch_cap15_boundary_audit.json
  role: data
  note: 24機械チェック・cap15センサス・110キー構造・ndet生存者集合・剰余レンズ・K0883/K0876交差照合の全記録
scope: "3枝REMO、r=3、枝サイズ≤15（正準形189,864プロファイル・3,060キー）の有限完全列挙。r≥4で枝サイズ13以上を含むキーは本項では未走査。枝サイズ≥16は未走査。"
evidence: "決定的JavaScript maskエンジンで生成したコミット済みsweepレコード（189,864件・packed出版形式・3部分割コミット・per-part sha256照合・検証器内で無損失再構成）を、出版済みK0883検証器からverbatim系譜のエンジン・列挙・Python mask twinで検証。24機械チェック（Burnside一致・レコード形式・センサス・110キー完全一致・H22/H14 52残留・新キー全てサイズ15枝・per-key分割・ndet生存者集合・決定側一様P_1・FL違反0・剰余類計数・枝サイズ統計）に加え、正準列挙の順序保存部分列性を用いてK0883出版r=3レコード123,272件をD_14対応位置で全件再現（0不一致・sha256ピン付き）、K0876監査JSONの定理H 22キー分割表とK0883監査JSONの52キー分割表を突合（いずれもsha256ピン付き・完全不変を確認）。live checkとしてcap≤7全域2,048 verdictsでverbatim==mask twin==committed、stride 32層化サンプル5,934 verdicts、K0862出版44 witnessをverbatimエンジンで再検証。assemble二重実行byte同一・別プロセス2回実行でも監査JSON byte同一。スイープレコードは独立環境からの再生成でも記録済みshaピン4点（joined+3部）とbyte一致。"
---

## 主張

**定理H15（cap≤15・r=3・有限完全）**: 3枝点族で全枝サイズ C_i≤15・任意γ のとき、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**ちょうど110個**である: 定理H14（cap≤14）の52個 + **58個の新キー**。

- サイズ境界を 10→12→13 へ広げても新規0だった安定化は14で破れ（H14の30新キー）、**サイズ15（≡0 (mod 3)・9と同剰余）でもさらに58個の新キーが出続ける**。58個すべてサイズ15枝を含む（サイズ15枝を含む680キーのうち58個がmixed）。
- 新キーは11のサイズ多重集合: (14,14,15),(14,15,15)×γ=0..9（20キー）と (2,8,15),(2,14,15),(3,8,15),(3,14,15)×γ=0..1（8キー）と (8,8,15),(8,9,15),(8,14,15),(8,15,15),(9,14,15)×γ=0..5（30キー）。
- **γ窓の初の拡張**: (14,14,15)/(14,15,15) の失敗γ範囲は0..9で、従来の失敗キー族のγ窓（すべて≤5）を初めて破る。残り9多重集合のγ窓はsourceのキーと一致。
- **有限観察（全称主張ではない）**: 定理H14の52キーの{8,9,14}要素の1〜2個を15に置き換えた候補74キーのうち50個がmixed・24個が坍縮・不在0。58新キーのうち50個はこの置換で得られ、残る8個は(14,14,15)/(14,15,15)のγ=6..9（sourceのγ窓の外側）。
- **もう一つの有限観察**: 新mixed多重集合はすべてサイズ8枝またはサイズ14枝を15と併せ持ち、8も14も持たない置換候補（(2,3,15),(2,9,15),(3,3,15),(3,9,15),(9,9,15),(2,15,15),(3,15,15),(9,15,15)）はすべて坍縮する。
- **ndet生存者集合{0,1}の初出現**: (2,8,15),(3,8,15),(8,8,15),(8,9,15),(8,14,15),(8,15,15) の6多重集合（28キー）で非決定側の可能生存者集合に{0,1}が現れる（cap≤14では可能生存者集合は{{1,2},{0,1,2}}内だった）。6多重集合とも8と15を併せ持つ。
- 110キーすべて剰余対{0,2}・決定側生存者は一様P_1・定理H14の52キーのper-key分割は完全不変（K0883監査mixed_partition・K0876監査のH22分割とも完全一致）。

付随する確定事実:

- 軌道数はcap 15で189,864（Burnside fix(id),fix(trans),fix(cyc)=(1,074,198, 21,414, 372)・直接正準化列挙と一致）。キー数3,060=一様決定399+一様非決定2,551+mixed 110。
- サイズ11枝660キー・サイズ12枝670キー・サイズ13枝676キーはすべて坍縮（境界13までの観察の再確認）。
- 1剰余525キー・3剰余525キーはすべて坍縮。2剰余2,010キーの非坍縮は110個のみ（「非坍縮⇒2剰余{0,2}」必要条件観察はサイズ15まで無反例）。
- 補題FL（可能第1敗者=={C_i mod 3}）はcap≤15全189,864プロファイルで違反0。
- 最大状態数120,202（状態総数1,545,731,088）。
- 正準列挙の順序保存部分列性（D_14⊂D_15）によりK0883出版r=3 packedレコード123,272件をD_14対応位置で全件再現（0不一致）。

## 限界

r=3のみ。r≥4で枝サイズ13,14,15を含むキーは本項では未走査（K0876はr=4,5,6・cap≤12）。**枝サイズ≥16は未走査**。16≡1 (mod 3)で、これまで未観察の剰余での新キー族の出現は次の検証課題。置換対応・「8/14併有」・γ窓拡張・ndet生存者{0,1}の有限観察は一般則ではない（H14の置換観察が15で部分的に伸びたのと同様に扱う）。「非坍縮⇒2剰余{0,2}」は必要条件の有限観察であり一般の証明ではない。本項の有限観察を全称定理へ昇格させない。11×11空盤はUNKNOWNのまま。順位決定性は本項で扱わない。
