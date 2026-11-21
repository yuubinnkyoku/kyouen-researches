---
id: K1094
title: "残余72行 safe8 pool 第3ラウンド再解決: REFUTED-D10 41根除外後の残余30行をgreedy 12根がleftover 0完全被覆・stranded 0・マッチング30・WIN8累計13根の内在被覆は主張と一致"
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - round-3 re-solve of the residual 30 rows over pool P-double-prime (120,433 roots) after excluding the 41 REFUTED-D10 roots (K1086 sixteen + K1089 thirteen + K1091 twelve)
  - 12 greedy replacement roots cover the residual 30 rows with leftover 0 (gains {3:8,2:2,1:2}, lower bound 8, bipartite maximum matching 30, stranded 0)
  - per-root intrinsic coverage of all 13 WIN8-D10 candidates equals their claims exactly (K1086 seven = 23 rows, K1089 three = 9 rows, K1091 three = 10 rows, no surplus to the residual-30 rows; scope1=scope2 identical selection)
relations:
- type: depends_on
  target: K1091
  note: 代替15根のverdict（WIN8 3根/REFUTED 12根）と主張被覆を正本（SHA-256 edd7ac84…）から引き継ぎ、claimsをcanonical化して40行exactly-once分割を再検証
- type: depends_on
  target: K1090
  note: 第2ラウンド再解決の機械構造（Stage C2 claims canonical化・scope1/scope2二段被覆計画）を継承しStage C3（K1091 verdict join）を追加
- type: depends_on
  target: K1089
  note: verdict join（WIN8 3根/REFUTED 13根・両順序uncapped pin）と残余49行宇宙再導入の出典
- type: depends_on
  target: K1086
  note: verdict join（7 WIN8/16 REFUTED・両順序uncapped pin）と残余72行base universe再導入の出典
- type: depends_on
  target: K1085
  note: 残余72行base state・add-two-stones census・greedy23計画を正本（SHA-256 5fdd342d…）から引き継ぎ
artifacts:
- path: research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/README.md
  role: document
  note: 実験README（結果・12根選定・需要構造・解釈規約・次の一手）
- path: research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/scripts/safe8_refuted41_refsolve_20261120.py
  role: verifier
  note: 再解決機械（入力4正本SHA pin・universe82/safe8/greedy23の独立再導入・claims canonical化2段（replacement16/replacement15）・pool P″・全23 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-safe8-refuted41-refsolve-20261120/output/safe8-refuted41-refsolve-20261120.json
  role: data
  note: 機械可読正本（SHA-256 e19244904779d906853de603d42c07903e08ab80008aeeb621913669a249baa8・全23 gate PASS・interpretation_guard 4文言同梱）
- path: research/log/2026-11-20-n11-residual72-safe8-refuted41-refsolve.md
  role: log
  note: 実行記録（宣言ノート参照・全数値・決定性確認・次の一手）
scope: >-
  REFUTED-D10 41根（K1086の16根+K1089の13根+K1091の12根）を除外した pool P″
  （120,433根）上での残余30行 greedy計画再解決と、WIN8-D10候補累計13根の
  内在被覆確認。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖は含まない。
evidence: >-
  （1）プールと需要: safe8 120,474根から41 REFUTED根を除外した pool P″
  120,433根での残余30行（K1091 REFUTED-12根の主張30行・canonical化で
  exactly-once・WIN8-3根の主張10行とdisjoint・残余40行の部分集合）の
  per-row demandはmin 1,782 / max 2,935 / sum 65,952、provider 58,259根触達
  （被覆ヒストグラム {1: 50,956, 2: 6,913, 3: 390}）、stranded行0。
  （2）再解決: greedy 12根が30行をleftover 0で完全被覆
  （gains {3:8, 2:2, 1:2}・下界ceil(30/4)=8に対し+4）、二部最大マッチング30
  （全行に互いに異なる被覆根）。全体計画は13 WIN8候補根（主張42行）+
  12代替根（30行）=25根で72行。（3）内在被覆: 累計13 WIN8-D10候補根の
  per-root intrinsic coverage（C(8,6)=28部分集合canonical再導入）は
  K1086の7根=23行・K1089の3根=9行・K1091の3根=10行の主張とper-root完全一致で
  主張外余剰なし（K1091の3根は本実験で初めて機械検証）、残余30行へのWIN候補
  intrinsic被覆は0行: 将来のWIN8 receipt foldは残余30行の需要構造を変えない
  （scope1=scope2同一12根選定で機械保証）。（4）独立再導入: universe82
  （generation witness→380,098根・safe8 120,474・unsafe8 259,624）・
  greedy23根計画（根順序・主張被覆行とも完全再現）・residual49分割・
  replacement16/replacement15 claims canonical化（49行/40行exactly-once・
  claims ⊆ generation-witness被覆）を入力実験から独立に再現し全23 gate PASS。
  （5）決定性: stdlibのみ・計5実行（同一cwd4回＋別cwd別プロセス1回・実行環境
  リセットを跨いだ機械再構築を含む）で正本JSON byte-identical
  （SHA-256 e1924490…）。ただしgreedy/witness選定は条件付き計画であり
  証明書ではない。REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗と
  して読まない。行の閉鎖は一切行っていない: 残余72行は全行openのまま。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit 934a4ceb・先行出版）の下で、K1091 README
「次の一手」第1項・第2項（pool P″再解決・WIN8累計13根の内在被覆確認）を実施した。
K1091 REFUTED-12根をさらに除外した pool P″（120,433根）上で
**残余30行のstranded行0・greedy 12根leftover 0完全被覆・二部最大マッチング30**、
**累計13 WIN8候補根の内在被覆はper-root主張と完全一致で残余30行への余剰なし**
（scope1=scope2同一選定で機械保証）を確定した。代替12根は未掃引であり、
次の一手は24 probes掃引と証明書抽出（別宣言）。行は1行も閉じていない。
詳細は[実験](../../experiments/n11-residual72-safe8-refuted41-refsolve-20261120/README.md)・
[再解決正本](../../experiments/n11-residual72-safe8-refuted41-refsolve-20261120/output/safe8-refuted41-refsolve-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-safe8-refuted41-refsolve.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
