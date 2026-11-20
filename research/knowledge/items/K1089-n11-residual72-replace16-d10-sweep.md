---
id: K1089
title: 残余72行 代替16根の depth-10 掃引: WIN8-D10 candidate 3根（被覆9行）と REFUTED-D10 fact 13根・32 probes完全完走（capped 0・順序整合）と残余49行宇宙・被覆幾何の独立再導入
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - depth-10 verdict sweep of the 16 replacement eight-stone roots for the residual 49 rows
  - 3 WIN8-D10 candidates (both orderings uncapped loss=true, claimed coverage 9 of the residual 49 rows) and 13 REFUTED-D10 facts
  - 32/32 probes completed, capped 0, error 0, in-order conflicts 0, nodes total 6,339,079 (avg 198K nodes/probe)
  - independent re-derivation of the residual-49 universe from K1085+K1086 and of the replacement-16 coverage geometry (D4 orientation, subsetting, exactly-once 49-row coverage, gains hist, popcount, quadruple-free, D4-min-canonical) via exact integer geometry
relations:
- type: depends_on
  target: K1088
  note: 代替16根（scope1_refsolve_residual49.greedy_selection）を正本（SHA-256 16b38d04…）から引き継ぎ、49行被覆幾何を独立再導入してgate化
- type: depends_on
  target: K1086
  note: 掃引protocol（runner v17・両AND順序・cap 30M・pilot_d6制御）と残余49行再導入の出典（per-root主張被覆の23+49 disjoint exactly-once分割）・WIN8 7根の累計簿記
- type: depends_on
  target: K1085
  note: 残余72行 base state（residual_row_hex）を正本（SHA-256 5fdd342d…）から引く
artifacts:
- path: research/experiments/n11-residual72-replace16-d10-sweep-20261120/README.md
  role: document
  note: 実験README（per-root表・主張被覆行・解釈規約・次の一手）
- path: research/experiments/n11-residual72-replace16-d10-sweep-20261120/scripts/replace16_d10_sweep_20261120.py
  role: verifier
  note: verdict掃引機械（入力3正本SHA pin・runner blob pin・残余49行のK1085+K1086からの独立再導入・32 probes resume-safe・assemble全13 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-replace16-d10-sweep-20261120/runner_v17.ts
  role: verifier
  note: runner v17 repo原本固定コピー（git blob c132cc64…）
- path: research/experiments/n11-residual72-replace16-d10-sweep-20261120/output/probe-records-replace16.jsonl
  role: data
  note: 生probe記録32行（assembleの唯一の入力・resume-safe掃引の実行痕跡）
- path: research/experiments/n11-residual72-replace16-d10-sweep-20261120/output/replace16-d10-sweep-20261120.json
  role: data
  note: 機械可読正本（SHA-256 808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc・全13 gate PASS・interpretation_guard 5文言同梱）
- path: research/log/2026-11-20-n11-residual72-replace16-d10-sweep.md
  role: log
  note: 実行記録（宣言ノート参照・全数値・決定性確認・次の一手）
scope: >-
  K1088が選定した残余49行完全被覆 greedy 代替16根に対する depth-10 verdict
  掃引。各根の両AND順序probe（32 probes・runner v17・cap 30M・pilot_d6制御）
  の事実記録と、残余49行宇宙（K1085+K1086から再導入）・代替16根被覆幾何の
  独立再導入。行の閉鎖・証明書抽出・receipt fold・8石receipt被覆幾何の設計は含まない。
evidence: >-
  （1）掃引: 32/32 probes完走・capped 0・error 0・順序間矛盾0・nodes総計
  6,339,079・平均約198K nodes/probe・最大probe 878,391・terminal石数union [12,18]。
  WIN8-D10 candidate 3根（両順序 loss=true・uncapped・gained 3×3・主張被覆行
  3+3+3=残余49行のうち9行）・REFUTED-D10 fact 13根（両順序 loss=false・uncapped・
  主張被覆40行）。（2）独立再導入: 残余49行宇宙をK1085残余72行×K1086 per-root
  主張から（K1088に頼らず）再導入し WIN8 23行+REFUTED 49行の disjoint・
  exactly-once・union==72 分割を確認。代替16根の49対主張すべて「行hexは再導入49行
  のD4方位」かつ「行石集合 ⊆ rootのいずれかのD4像」・49行ちょうど1回被覆・
  gains hist {4:3,3:11,2:2}・16根すべて popcount 8・quadruple-free・D4 orbit最小hex
  を再導入し全13 gate PASS。（3）決定性: pilot_d6制御が全32 probe記録で nodes 3,402・
  loss=false・capped=false。probe再実行（WIN 1根両順序+REFUTED 1根1順序）が
  nodes/loss/capped/terminalで記録と完全一致。assembleは同一cwd複数回＋別cwd別
  プロセス2回で正本JSON byte-identical（SHA-256 808fbda1…）。（4）解釈: loss=trueは
  WIN8-D10 certificate再構築の対象候補にすぎず、抽出・独立二重検証・8石receipt
  foldの意味論は本項では確定しない。loss=falseはREFUTED-D10 factでありLOSS証明
  ではない。行の閉鎖は一切行っていない: 累計計画は K1086 7根（23行）+本項3根（9行）
  のWIN8-D10候補被覆32行が増えたが、残余72行は全行openのまま。nodes数・solved数を
  勝敗として読まない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit 7e038004・先行出版）の下で、K1088 README
「次の一手」第1項の代替16根 depth-10 掃引を実施した。**WIN8-D10 candidate 3根**
が両順序 uncapped で発見され（主張被覆9行・証明書抽出には別の単一オーナー宣言を要する）、
**REFUTED-D10 fact 13根**（主張被覆40行）を得た。32 probes は capped 0・error 0・
順序間矛盾0 で完走し、残余49行宇宙はK1085+K1086から（K1088に頼らず）独立再導入・
代替16根の被覆幾何は整数幾何で再導入して全13 gate PASS、正本は決定性確認済み。
次の一手は pool P′（120,445根）での残余40行再解決と新WIN8-3根の内在被覆確認。
詳細は[実験](../../experiments/n11-residual72-replace16-d10-sweep-20261120/README.md)・
[掃引正本](../../experiments/n11-residual72-replace16-d10-sweep-20261120/output/replace16-d10-sweep-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace16-d10-sweep.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
