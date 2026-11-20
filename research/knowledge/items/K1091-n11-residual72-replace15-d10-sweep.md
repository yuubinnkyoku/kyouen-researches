---
id: K1091
title: 残余72行 代替15根 depth-10掃引: WIN8-D10 candidate 3根（主張10行）+ REFUTED-D10 fact 12根（主張30行）・30 probes完走・残余40行宇宙をK1085+K1086+K1089から独立再導入
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - depth-10 verdict sweep of the 15 round-2 replacement roots over the residual 40 rows (K1090 scope1 greedy selection, 30 probes, both AND orderings, cap 30M, pilot_d6 control)
  - 3 WIN8-D10 candidates (both orderings uncapped loss=true, gained 4/3/3, claimed 10 rows), cumulative WIN8 candidates now 13 roots claiming 42 rows
  - 12 REFUTED-D10 facts (claimed 30 rows) erode the round-3 re-solve pool to P-double-prime (120,433 roots)
relations:
- type: depends_on
  target: K1090
  note: 掃引対象の15根（scope1_refsolve_residual40.greedy_selection・残余40行leftover 0完全被覆）を正本（SHA-256 48af6810…）から引き継ぎ
- type: depends_on
  target: K1089
  note: 残余40行宇宙再導入の出典（WIN8 3根の主張9行と REFUTED 13根の主張40行の分割）
- type: depends_on
  target: K1086
  note: 残余49行宇宙再導入の出典（WIN8 7根の主張23行と REFUTED 16根の主張49行の分割）
- type: depends_on
  target: K1085
  note: 残余72行base state・add-two-stones censusの出典
artifacts:
- path: research/experiments/n11-residual72-replace15-d10-sweep-20261120/README.md
  role: document
  note: 実験README（15根成否表・WIN/REF分類・需要構造・解釈規約・次の一手）
- path: research/experiments/n11-residual72-replace15-d10-sweep-20261120/scripts/replace15_d10_sweep_20261120.py
  role: verifier
  note: 掃引機械（入力4正本SHA pin・残余49/40行宇宙独立再導入・resume-safe probe実行・全16 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json
  role: data
  note: 機械可読正本（SHA-256 edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25・全16 gate PASS・interpretation_guard 5文言同梱）
- path: research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/probe-records-replace15.jsonl
  role: data
  note: 逐次probe記録（30 probes・resume-safe・pilot_d6制御行同梱）
- path: research/experiments/n11-residual72-replace15-d10-sweep-20261120/runner_v17.ts
  role: verifier
  note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・掃引機械が実行毎にblob pinを検証）
- path: research/log/2026-11-20-n11-residual72-replace15-d10-sweep.md
  role: log
  note: 実行記録（宣言ノート参照・15根成否・決定性確認・次の一手）
scope: >-
  K1090正本の残余40行greedy代替15根に対する depth-10 verdict掃引（両AND順序30 probes・
  runner v17・cap 30M・pilot_d6制御）。行の閉鎖・receipt fold・証明書抽出は含まない。
evidence: >-
  （1）掃引: 30/30 probes完走・capped 0・error 0・順序間矛盾0・nodes総計
  7,383,022（平均約246K・最大1,054,873・terminal石数union [14,18]）。
  （2）分類: WIN8-D10 candidate 3根（両順序uncapped loss=true・gained 4/3/3・
  主張被覆10行）: `00000000000000801212000001009000`（nodes 192,365/229,502）,
  `00000000000000003800000008d10000`（564,695/673,870）,
  `00000000000000043800000008180010`（882,327/1,054,873）。
  REFUTED-D10 fact 12根（両順序uncapped loss=false・主張被覆30行）。
  WIN3主張10行とREF12主張30行は残余40行のdisjoint exactly-once分割
  （機械gate保証）。（3）独立再導入: 残余40行宇宙はK1085+K1086から残余49行を、
  さらにK1089のWIN3/REF13主張から40行を再計算（union==49・disjoint・
  exactly-once）。15根の被覆幾何（D4方位・部分集合・ちょうど1回・
  gains hist {4:2,3:9,2:1,1:3}・popcount 8・quadruple-free・D4 min-canonical）を
  整数幾何で再導入し全16 gate PASS。（4）決定性: probe再実行（WIN最大根両順序+
  REFUTED 1根）がnode-exact一致、assemble同一cwd複数回+別cwd別プロセス1回で
  正本JSON byte-identical（SHA-256 edd7ac84…）。ただしloss=trueはdepth-10内
  必敗のprobe事実で証明書ではなく、extract/fold/行閉鎖は別工程。REFUTED-D10は
  LOSS証明ではない。nodes数を勝敗として読まない。残余72行は1行も閉じていない:
  全行openのまま。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4はすべてUNKNOWNのまま。
---

## 詳細

単一オーナー宣言ノート（commit f1d78342・先行出版）の下で、K1090 README
「次の一手」第1項（代替15根のdepth-10 verdict掃引）を実施した。
**WIN8-D10 candidate 3根**（主張10行・累計WIN候補は13根・主張42行）、
**REFUTED-D10 fact 12根**（主張30行・第3ラウンド再解決pool P″は120,433根）を
確定した。行は1行も閉じていない。証明書抽出は別宣言
（1根抽出の宣言ノートは並走レーンが先行出版済み: commit 4496c888）。
詳細は[実験](../../experiments/n11-residual72-replace15-d10-sweep-20261120/README.md)・
[掃引正本](../../experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace15-d10-sweep.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
