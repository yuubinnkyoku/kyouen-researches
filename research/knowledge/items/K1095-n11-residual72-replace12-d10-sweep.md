---
id: K1095
title: "残余72行 代替12根 depth-10掃引: WIN8-D10 candidate 3根（主張7行）+ REFUTED-D10 fact 9根（主張23行）・24 probes完走・残余30行宇宙をK1085+K1086+K1089+K1091から独立再導入"
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - round-3 depth-10 verdict sweep of the 12 greedy replacement roots covering the residual 30 rows over pool P-double-prime (K1094 scope1), 24 probes both AND orderings, runner v17, cap 30M
  - 3 new WIN8-D10 candidates (both orderings loss=true uncapped, gained 3/3/1, claimed 7 rows) and 9 REFUTED-D10 facts (claimed 23 rows; round-4 re-solve pool 120,424)
  - cumulative WIN8-D10 candidates now 16 roots claiming 49 of the 72 residual rows (all candidate bookkeeping, no row closure)
relations:
- type: depends_on
  target: K1094
  note: 12代替根と残余30行宇宙の出典（scope1_refsolve_residual30.greedy_selection・正本SHA-256 e1924490…）。掃引機械は残30行宇宙をK1094から取らず独立再導入で一致検証
- type: depends_on
  target: K1091
  note: 残余40行宇宙のWIN3/REF12主張分割（残30行再導入の最上流）を正本（SHA-256 edd7ac84…）から引き継ぎ
- type: depends_on
  target: K1089
  note: 残余49行宇宙のWIN3/REF13主張分割の再導入の出典
- type: depends_on
  target: K1086
  note: 残余72行×主張23/49行のverdict joinと残余49行再導入の出典
- type: depends_on
  target: K1085
  note: 残余72行base state・add-two-stones censusを正本（SHA-256 5fdd342d…）から引き継ぎ
artifacts:
- path: research/experiments/n11-residual72-replace12-d10-sweep-20261120/README.md
  role: document
  note: 実験README（12根verdict表・主張被覆・解釈規約・次の一手）
- path: research/experiments/n11-residual72-replace12-d10-sweep-20261120/scripts/replace12_d10_sweep_20261120.py
  role: verifier
  note: 掃引機械（入力5正本SHA pin・残49/40/30行宇宙の独立再導入・被覆幾何D4+Bareiss再導入・pilot_d6制御・全18 gate fail-closed・stdlib+node runnerのみ）
- path: research/experiments/n11-residual72-replace12-d10-sweep-20261120/runner_v17.ts
  role: code
  note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59）
- path: research/experiments/n11-residual72-replace12-d10-sweep-20261120/output/replace12-d10-sweep-20261120.json
  role: data
  note: 機械可読正本（SHA-256 335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707・全18 gate PASS・interpretation_guard 5文言同梱）
- path: research/experiments/n11-residual72-replace12-d10-sweep-20261120/output/probe-records-replace12.jsonl
  role: data
  note: 24 probesの生記録（pilot_d6制御・cap・child hex・nodes/loss/capped/terminalStoneRange・resume-safe JSONL）
- path: research/log/2026-11-20-n11-residual72-replace12-d10-sweep.md
  role: log
  note: 実行記録（宣言ノート参照・verdict表・再現性・次の一手）
scope: >-
  K1094 scope1 greedy 代替12根（残余30行leftover 0完全被覆・pool P″上の計画根）
  の depth-10 verdict掃引（両AND順序24 probes）。行の閉鎖claim・receipt fold・
  証明書抽出は含まない。
evidence: >-
  （1）verdict: 24/24 probes完走・capped 0・error 0・順序間矛盾0
  （nodes総計5,700,222・平均約238K/probe・最大1,416,679・terminal石数union [12,18]）。
  **WIN8-D10 candidate 3根**（`00000000000000801202000000901010` nodes 198,622/240,848・
  `00000000000000801202000022081000` nodes 126,683/137,565・
  `0000000800000000380000000810000a` nodes 1,226,804/1,416,679・両順序loss=true・
  uncapped・gained 3/3/1・主張被覆7行）、**REFUTED-D10 fact 9根**（両順序loss=false・
  uncapped・主張被覆23行→pool P‴ = 120,433 − 9 = 120,424根での第4ラウンド再解決を要する）。
  （2）独立再導入: 残余30行宇宙はK1094正本から取らずK1085+K1086+K1089+K1091から
  再導入（win11 claims 10行 + ref12 claims 30行・disjoint・exactly-once・union==40）、
  12根の30対主張・ちょうど1回被覆・gains hist {3:8,2:2,1:2}・popcount 8・
  quadruple-free・D4 min-canonicalを整数幾何（Bareiss 4x4行列式）で再導入して
  全18 gate PASS（K1094帳簿の残30行一致はcrosscheck gate）。（3）再現性:
  probe再実行（WIN最大根両順序+REFUTED 1根1順序）がnode-exact一致・
  assemble同一cwd複数回+別cwd別プロセス1回でbyte-identical
  （正本SHA-256 335eca5e…）。（4）解釈: loss=true uncappedはWIN8-D10
  certificate再構築の対象候補にすぎず、抽出・独立二重検証・8石receipt fold・
  行閉鎖は別工程。REFUTED-D10はLOSS証明ではなくpool浸食のみ。nodes数・solved数を
  勝敗として読まない。累計WIN8候補16根（主張49行）はすべて候補簿記であり
  行閉鎖ではない: 残余72行は全行openのまま。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit 71536f20・先行出版）の下で、K1094 README
「次の一手」第1項（代替12根の depth-10 verdict掃引）を実施した。
24 probes すべて完走し **WIN8-D10 candidate 3根（主張7行）・REFUTED-D10 fact 9根（主張23行）**
を確定した。WIN8候補は累計16根・主張49行（72行の簿記上の過半。ただし候補であり
行閉鎖ではない）。次の一手は第4ラウンド再解決（pool P‴ 120,424根・残余23行）と
新3根の内在被覆確認・証明書抽出（別宣言）。行は1行も閉じていない。
詳細は[実験](../../experiments/n11-residual72-replace12-d10-sweep-20261120/README.md)・
[掃引正本](../../experiments/n11-residual72-replace12-d10-sweep-20261120/output/replace12-d10-sweep-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace12-d10-sweep.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
