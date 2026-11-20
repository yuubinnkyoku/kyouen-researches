---
id: K1097
title: 残余72行 safe8 pool 第4ラウンド再解決: REFUTED-D10 50根除外後の残余23行をgreedy 9根がleftover 0完全被覆・stranded 0・マッチング23・WIN8累計16根の内在被覆は主張を包含（K1095 3根目は主張+1行の初の余剰）
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - round-4 re-solve of the residual 23 rows over pool P-triple-prime (120,424 roots) after excluding the 50 REFUTED-D10 roots (K1086 sixteen + K1089 thirteen + K1091 twelve + K1095 nine)
  - 9 greedy replacement roots cover the residual 23 rows with leftover 0 (gains {3:6,2:2,1:1}, lower bound 6, bipartite maximum matching 23, stranded 0)
  - per-root intrinsic coverage of all 16 WIN8-D10 candidates contains their claims (K1086 seven = 23 rows, K1089 three = 9, K1091 three = 10, K1095 three = 7; the K1095 third root has exactly one extra intrinsic row, claimed by the K1096-certificated root 8003180; no residual-23 row inside win-intrinsic; scope1=scope2 identical selection)
relations:
- type: depends_on
  target: K1095
  note: 代替12根のverdict（WIN8 3根/REFUTED 9根）と主張被覆を正本（SHA-256 335eca5e…）から引き継ぎ、claimsをcanonical化して30行exactly-once分割を再検証
- type: depends_on
  target: K1094
  note: 再解決機械構造（Stage C3 claims canonical化・pool P″・scope1/scope2二段被覆計画・win13 footprints）を継承しStage C4（K1095 verdict join）を追加
- type: depends_on
  target: K1096
  note: K1095 3根目のintrinsic余剰行の帰属先はroot 8003180の主張行（当該rootの証明書がK1096で出版済み。余剰の記録は受動的でK1096の内容に依存しない）
- type: depends_on
  target: K1091
  note: verdict join（WIN8 3根/REFUTED 12根・両順序uncapped pin）と残余40行宇宙再導入の出典
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
- path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/README.md
  role: document
  note: 実験README（結果・9根選定・需要構造・解釈規約・次の一手）
- path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/scripts/safe8_refuted50_refsolve_20261120.py
  role: verifier
  note: 再解決機械（入力5正本SHA pin・universe82/safe8/greedy23の独立再導入・claims canonical化3段（replacement16/15/12）・pool P‴・全27 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json
  role: data
  note: 機械可読正本（SHA-256 2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40・全27 gate PASS・interpretation_guard 4文言同梱）
- path: research/log/2026-11-20-n11-residual72-safe8-refuted50-refsolve.md
  role: log
  note: 実行記録（宣言ノート参照・全数値・決定性確認・次の一手）
scope: >-
  REFUTED-D10 50根（K1086の16根+K1089の13根+K1091の12根+K1095の9根）を除外した
  pool P‴（120,424根）上での残余23行 greedy計画再解決と、WIN8-D10候補累計16根の
  内在被覆確認。新規probe・掃引・証明書抽出・receipt fold・行の閉鎖は含まない。
evidence: >-
  （1）プールと需要: safe8 120,474根から50 REFUTED根を除外した pool P‴
  （120,424根）上で残余23行（K1095 REFUTED-9根の主張被覆行・canonical化・
  残余30行の部分集合でWIN8-3根主張7行とdisjoint）の per-row demand は
  min 1,781 / max 2,934 / sum 50,670・23行に触れるprovider 45,219根・
  provider被覆hist {1:40,065, 2:4,857, 3:297}で**stranded行0**。
  （2）計画: **greedy 9根が残余23行をleftover 0で完全被覆**
  （gains {3:6, 2:2, 1:1}・情報論的下界ceil(23/4)=6に対し+3）。
  **二部最大マッチング23**（全23行に互いに異なる被覆根・每行1根のwitness）。
  代替9根は未掃引で、depth-10掃引には両AND順序18 probesを要する。
  （3）内在被覆: 累計16 WIN8-D10候補根のC(8,6)=28部分集合のcanonical再導入は
  主張を包含し、うち15根はintrinsic==主張で完全一致。**K1095 3根目
  `0000000800000000380000000810000a` は主張+1行のintrinsic余剰
  `00000000000000003800000008001080` を持ち、当該行は残余23行ではなく
  K1086 WIN根 `00000000000000003800000008003180`（証明書はK1096で出版済み）の
  主張行**（初の「余剰あり」WIN候補の機械記録・残余23行の需要構造には無影響）。
  **残余23行へのWIN候補intrinsic被覆は0行**: 将来のWIN8 receipt foldは残余23行の
  需要構造を変えない（scope1=scope2同一9根選定で機械保証）。
  （4）全 体計画: 16 WIN8候補根（主張49行）+ 9代替根（23行）= 25根で72行
  （候補根の簿記であり証明書ではない）。
  （5）決定性: 同一cwd2回+別cwd別プロセス1回の計3実行で正本JSON
  byte-identical（SHA-256 2896deb0…）・全27 gate PASS・stdlibのみ・乱数・時刻なし。
  本計算は行を1つも閉じない。REFUTED-D10はLOSS証明ではなく、nodes数・solved数を
  勝敗として読まない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて UNKNOWN のまま。
---

## 詳細

単一オーナー宣言ノート（commit 22d85b72・先行出版）の下で、K1095 README
「次の一手」第1項（pool P‴ 再解決）・第2項（WIN16の内在被覆確認）を実施した。
除外50根後の pool P‴（120,424根）上で残余23行は stranded 0・**greedy 9根が
leftover 0完全被覆**（下界6に対し+3）・マッチング23。WIN16のper-root内在被覆は
主張を包含し、K1095 3根目に初の余剰1行（K1096証明書根の主張行）を記録、
残余23行へのintrinsic被覆は0行。全体計画は16 WIN+9代替=25根で72行。
次の一手は代替9根のdepth-10掃引（18 probes）・残るWIN候補の証明書抽出
（root 8003180はK1096で出版済み・別1根は宣言済み: commit 4496c888）・
K1096証明書のreceipt fold。行は1行も閉じていない。
詳細は[実験](../../experiments/n11-residual72-safe8-refuted50-refsolve-20261120/README.md)・
[再解決正本](../../experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-safe8-refuted50-refsolve.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
