---
id: K1090
title: 残余72行 safe8 pool 第2ラウンド再解決: REFUTED-D10 29根除外後の残余40行をgreedy 15根がleftover 0完全被覆・stranded 0・マッチング40・WIN8累計10根の内在被覆は主張と一致
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - round-2 re-solve of the residual 40 rows over pool P-prime (120,445 roots) after excluding the 29 REFUTED-D10 roots (K1086 sixteen + K1089 thirteen)
  - 15 greedy replacement roots cover the residual 40 rows with leftover 0 (gains {4:2,3:9,2:1,1:3}, lower bound 10, bipartite maximum matching 40, stranded 0)
  - per-root intrinsic coverage of all 10 WIN8-D10 candidates equals their claims exactly (K1086 seven = 23 rows, K1089 three = 9 rows, no surplus to the residual-40 rows; scope1=scope2 identical selection)
relations:
- type: depends_on
  target: K1089
  note: 代替16根のverdict（WIN8 3根/REFUTED 13根）と主張被覆を正本（SHA-256 808fbda1…）から引き継ぎ、claimsをcanonical化して49行exactly-once分割を再検証
- type: depends_on
  target: K1086
  note: verdict join（7 WIN8/16 REFUTED・両順序uncapped pin）と残余49行宇宙の再導入の出典
- type: depends_on
  target: K1088
  note: 第1ラウンド再解決の機械構造（Stage B/C/D等の設計・scope1/scope2二段被覆計画）を継承（入力pinは使用せずK1085+K1086+K1089から再導入）
- type: depends_on
  target: K1085
  note: 残余72行base state・add-two-stones census・greedy23計画を正本（SHA-256 5fdd342d…）から引き継ぎ
artifacts:
- path: research/experiments/n11-residual72-safe8-refuted29-refsolve-20261120/README.md
  role: document
  note: 実験README（結果・15根選定・需要構造・解釈規約・次の一手）
- path: research/experiments/n11-residual72-safe8-refuted29-refsolve-20261120/scripts/safe8_refuted29_refsolve_20261120.py
  role: verifier
  note: 再解決機械（入力3正本SHA pin・universe82/safe8/greedy23の独立再導入・claims canonical化・pool P′・全20 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-safe8-refuted29-refsolve-20261120/output/safe8-refuted29-refsolve-20261120.json
  role: data
  note: 機械可読正本（SHA-256 48af6810173060eb769eb52b1fd50ceb81222c07ba7738c8a15832f8c552d3f5・全20 gate PASS・interpretation_guard 4文言同梱）
- path: research/log/2026-11-20-n11-residual72-safe8-refuted29-refsolve.md
  role: log
  note: 実行記録（宣言ノート参照・全数値・決定性確認・次の一手）
scope: >-
  REFUTED-D10 29根（K1086の16根+K1089の13根）を除外した pool P′
  （120,445根）上での残余40行 greedy計画再解決と、WIN8-D10候補累計10根の
  内在被覆確認。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖は含まない。
evidence: >-
  （1）プールと需要: safe8 120,474根から29 REFUTED根を除外した pool P′
  120,445根での残余40行（K1089 REFUTED-13根の主張40行・canonical化で
  exactly-once・WIN8-3根の主張9行とdisjoint）のper-row demandは
  min 1,783 / max 2,942 / sum 89,467、provider 75,738根触達、stranded行0。
  （2）再解決: greedy 15根が40行をleftover 0で完全被覆
  （gains {4:2,3:9,2:1,1:3}・下界ceil(40/4)=10に対し+5）、二部最大マッチング40
  （全行に互いに異なる被覆根）。全体計画は10 WIN8候補根（主張32行）+
  15代替根（40行）=25根で72行。（3）内在被覆: 累計10 WIN8-D10候補根の
  per-root intrinsic coverage（C(8,6)=28部分集合canonical再導入）は
  K1086の7根=23行・K1089の3根=9行の主張とper-root完全一致で主張外余剰なし、
  残余40行へのWIN候補intrinsic被覆は0行: 将来のWIN8 receipt foldは
  残余40行の需要構造を変えない（scope1=scope2同一15根選定で機械保証）。
  （4）独立再導入: universe82（generation witness 471,960 events→380,098根・
  safe8 120,474・unsafe8 259,624）・coverage hist・demand・greedy23根計画
  （根順序・主張被覆行とも）・residual49分割・replacement16 claims
  canonical化を入力実験から独立に再現し全20 gate PASS。（5）決定性: stdlibのみ・
  同一cwd2回+別cwd別プロセス1回の3実行で正本JSON byte-identical
  （SHA-256 48af6810…）。ただしgreedy/witness選定は条件付き計画であり
  証明書ではない。REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗と
  して読まない。行の閉鎖は一切行っていない: 残余72行は全行openのまま。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit c5dee3de・先行出版）の下で、K1089 README
「次の一手」第1項・第2項（pool P′再解決・WIN8-3根の内在被覆確認）を実施した。
K1089 REFUTED-13根をさらに除外した pool P′（120,445根）上で
**残余40行のstranded行0・greedy 15根leftover 0完全被覆・二部最大マッチング40**、
**累計10 WIN8候補根の内在被覆はper-root主張と完全一致で残余40行への余剰なし**
（scope1=scope2同一選定で機械保証）を確定した。代替15根は未掃引であり、
次の一手は30 probes掃引と証明書抽出（別宣言）。行は1行も閉じていない。
詳細は[実験](../../experiments/n11-residual72-safe8-refuted29-refsolve-20261120/README.md)・
[再解決正本](../../experiments/n11-residual72-safe8-refuted29-refsolve-20261120/output/safe8-refuted29-refsolve-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-safe8-refuted29-refsolve.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
