---
id: K1086
title: "残余72行 add-two greedy 23根の depth-10 掃引: WIN8-D10 candidate 7根（被覆23行）と REFUTED-D10 fact 16根・46 probes完全完走（capped 0・順序整合）と greedy計画幾何の独立再導入"
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - depth-10 verdict sweep of the 23 greedy eight-stone add-two candidate roots for the residual 72 rows
  - 7 WIN8-D10 candidates (both orderings uncapped loss=true, claimed coverage 23 of the 72 rows) and 16 REFUTED-D10 facts
  - 46/46 probes completed, capped 0, error 0, in-order conflicts 0, nodes total 18,032,471 (about 1/5.7 of the per-probe cost of the published 7-stone depth-10 sweeps)
  - independent re-derivation of the K1085 greedy plan geometry (72 claimed pairs, D4 orientation, subsetting, exactly-once coverage, gains hist, quadruple-free) via exact integer geometry
relations:
- type: depends_on
  target: K1085
  note: greedy 23根・残余72行base stateを正本（SHA-256 5fdd342d…）から引き継ぎ、pool/greedy計画幾何を独立再導入してgate化
- type: depends_on
  target: K1069
  note: 掃引protocol（runner v17・両AND順序・cap 30M・pilot_d6制御）と7石掃引のnode費用参照（sweep39live 169,615,508 nodes）
artifacts:
- path: research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/README.md
  role: document
  note: 実験README（per-root表・主張被覆行・解釈規約・次の一手）
- path: research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/scripts/addtwo_greedy23_d10_sweep_20261120.py
  role: verifier
  note: verdict掃引機械（K1085 sha pin・runner blob pin・greedy幾何の独立再導入・46 probes resume-safe・assemble全11 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/probe-records-add2greedy23.jsonl
  role: data
  note: 生probe記録46行（assembleの唯一の入力・resume-safe掃引の実行痕跡）
- path: research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json
  role: data
  note: 機械可読正本（SHA-256 3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced・全11 gate PASS・interpretation_guard 5文言同梱）
- path: research/log/2026-11-20-n11-residual72-addtwo-greedy23-d10-sweep.md
  role: log
  note: 実行記録（宣言ノート参照・全数値・決定性確認・次の一手）
scope: >-
  K1085が確定した add-two 8石候補 greedy set cover 23根に対する depth-10
  verdict 掃引。各根の両AND順序probe（46 probes・runner v17・cap 30M・
  pilot_d6制御）の事実記録と、greedy計画幾何の独立再導入。行の閉鎖・
  証明書抽出・receipt fold・8石receipt被覆幾何の設計は含まない。
evidence: >-
  （1）掃引: 46/46 probes完走・capped 0・error 0・順序間矛盾0・nodes総計
  18,032,471・terminal石数union [12,18]。WIN8-D10 candidate 7根（両順序
  loss=true・uncapped・greedy計画上の主張被覆行4+4+4+3+3+3+2=23行）・
  REFUTED-D10 fact 16根（両順序 loss=false・uncapped）。8石probeの節点費用は
  同protocolの7石掃引（sweep39live・平均約2.2M nodes/probe）に対して平均約
  392K nodes/probe（約1/5.7・23根の観察で一般化ではない）。（2）独立再導入:
  greedy計画のclaimed 72対すべて「行hexは残余72行のいずれかのD4方位」かつ
  「行石集合 ⊆ rootのいずれかのD4像」・残余72行はちょうど1根で被覆
  （covered union == residual rows・72 unique）・gains hist {4:7,3:13,2:2,1:1}・
  23根と72行すべて quadruple-free（4点共円/共線の4x4行列式・Bareiss・
  整数演算のみ）をK1085実験と独立に再導入し全gate PASS。（3）決定性:
  pilot_d6制御が全46 probe記録で nodes 3,402・loss=false・capped=false。
  probe再実行（WIN2本両順序+REFUTED1本）が nodes/loss/capped/terminal
  で記録と完全一致。assembleは同一cwd2回＋別cwd別プロセス1回で正本JSON
  byte-identical（SHA-256 3045e152…）。（4）解釈: loss=trueはWIN8-D10
  certificate再構築の対象候補にすぎず、抽出・独立二重検証・8石receipt
  fold（「8 D4像×2石除去」join）の意味論は本項では確定しない。loss=falseは
  REFUTED-D10 factでありLOSS証明ではない。行の閉鎖は一切行っていない:
  残余72行は全行openのまま。nodes数・solved数を勝敗として読まない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit b943a20875・先行出版）の下で、K1085 README
「次の一手」第1項の add-two greedy 23根 depth-10 掃引を実施した。
**WIN8-D10 candidate 7根**が両順序 uncapped で発見され（greedy計画上の
主張被覆23行・証明書抽出は別の単一オーナー宣言を要する）、**REFUTED-D10 fact
16根**を得た。46 probes は capped 0・error 0・順序間矛盾0 で完走し、
greedy計画幾何は整数幾何で独立再導入・全gate PASS、正本は決定性確認済み。
詳細は[実験](../../experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/README.md)・
[掃引正本](../../experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-addtwo-greedy23-d10-sweep.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
