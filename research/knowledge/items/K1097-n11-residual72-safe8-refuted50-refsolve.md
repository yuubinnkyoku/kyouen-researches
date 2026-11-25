---
id: K1097
title: "残余72行 safe8 第4ラウンド: REFUTED-D10 50根除外後の残余23行をgreedy9根で被覆・下界8から判定で最小被覆9が確定（8根被覆はUNSAT・数え上げ証明書つき）"
kind: computation
status: computed
topics: [search-methods, certificates, geometry]
aliases:
  - round-4 re-solve of the residual 23 rows over pool P-triple-prime (120,424 roots) after excluding the 50 REFUTED-D10 roots (K1086 sixteen + K1089 thirteen + K1091 twelve + K1095 nine)
  - 9 greedy replacement roots cover the residual 23 rows with leftover 0 (gains {3:6,2:2,1:1}, strengthened lower bound 8, bipartite maximum matching 23, stranded 0)
  - "the minimum provider-cover size over P''' is exactly 9: the eight-root cover decision is UNSAT (three rows have zero 3-row providers on P'''; counting certificate k_min=2 > k_max=3*8-23=1; exhaustive two-shape search over 100 pair patterns and 351 duplicate-row triple pairs agrees; the greedy 9-root plan is therefore provably minimal in root count on P''')"
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
- path: research/experiments/n11-residual23-cover-lower-bound-strengthening-20261120/README.md
  role: source
  note: P'''上の最大被覆3行から残余23行の必要根数下界を8へ強化し、8根被覆の形とILP縮約を導出
- path: research/experiments/n11-residual23-cover-lower-bound-strengthening-20261120/scripts/audit_lower_bound.py
  role: verifier
  note: K1097/K1102のSHA-256 pin・provider histogram一致・ceil(23/3)・最大550 pattern変数をfail-closed検査
- path: research/experiments/n11-residual23-cover-lower-bound-strengthening-20261120/output/residual23-cover-lower-bound-strengthening-20261120.json
  role: data
  note: 下界8・greedy9・8根被覆の必要形・最大550 pattern変数を記録（SHA-256 1310ef74…）
- path: research/log/2026-11-20-n11-residual23-cover-lower-bound-strengthening.md
  role: log
  note: 下界強化の発見順・計算・限界
- path: research/experiments/n11-residual23-eight-root-cover-decision-20261120/README.md
  role: document
  note: 8根被覆判定の実験README（数え上げ証明書・2形完全探索・独立第二実装・決定性・次の一手）
- path: research/experiments/n11-residual23-eight-root-cover-decision-20261120/scripts/eight_root_cover_decision_20261120.py
  role: verifier
  note: 判定機械（K1097/K1102/監査の3正本SHA pin・触れる宇宙137,959根の全数2述語safe8判定・28部分集合内在被覆100%全数・数え上げ証明書ゲート・Shape A/B完全探索・全18 gate fail-closed・stdlibのみ）
- path: research/experiments/n11-residual23-eight-root-cover-decision-20261120/output/residual23-eight-root-cover-decision-20261120.json
  role: data
  note: 判定正本（SHA-256 c5aaf83e…・minimum_cover_size_over_P3 = 9・interval [8,9]→[9,9]・UNSAT（witnessなし）・全18 gate PASS・interpretation_guard 5文言同梱）
- path: research/log/2026-11-20-n11-residual23-eight-root-cover-decision.md
  role: log
  note: 判定の実行記録（宣言ノート参照・発見順・独立第二実装・決定性確認・次回への引継ぎ）
scope: >-
  REFUTED-D10 50根（K1086の16根+K1089の13根+K1091の12根+K1095の9根）を除外した
  pool P‴（120,424根）上での残余23行 greedy計画再解決と、WIN8-D10候補累計16根の
  内在被覆確認。後続監査でprovider-cover下界を8へ強化し、8根被覆ILPを最大550 patternへ
  縮約した。判定実験で8根被覆を厳密に判定してUNSATとし、P‴上の最小被覆9を
  確定した（数え上げ証明書+2形完全探索）。新規probe・掃引・証明書抽出・
  receipt fold・行の閉鎖は含まない。
evidence: >-
  （1）プールと需要: safe8 120,474根から50 REFUTED根を除外した pool P‴
  （120,424根）上で残余23行（K1095 REFUTED-9根の主張被覆行・canonical化・
  残余30行の部分集合でWIN8-3根主張7行とdisjoint）の per-row demand は
  min 1,781 / max 2,934 / sum 50,670・23行に触れるprovider 45,219根・
  provider被覆hist {1:40,065, 2:4,857, 3:297}で**stranded行0**。
  （2）計画: **greedy 9根が残余23行をleftover 0で完全被覆**
  （gains {3:6, 2:2, 1:1}・当時の粗い下界ceil(23/4)=6に対し+3。後続監査でP'''の最大被覆3行から下界8へ強化）。
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
  （6）下界強化: K1097とK1102の独立正本はP'''上のprovider histogram
  {1:40,065, 2:4,857, 3:297}で一致し、最大被覆は3行。よって必要根数は
  ceil(23/3)=8。greedy9根と合わせて最小値は8または9。8根被覆では1行providerを
  使えず、2行providerは高々1根。候補は8 triple（重複1行）または7 triple+1 pair
  （重複なし）に限られる。2行patternは最大253種、3行providerは297根以下なので、
  被覆pattern変数は最大550。scope2もWIN16の残余23行intrinsic hitが0のため同じ。
  詳細は[下界強化監査](../../experiments/n11-residual23-cover-lower-bound-strengthening-20261120/README.md)・[研究ログ](../../log/2026-11-20-n11-residual23-cover-lower-bound-strengthening.md)を参照する。
  （7）8根被覆判定: 判定機が入力3正本（K1097=`2896deb0…`、K1102=`d0b5d845…`、
  監査=`1310ef74…`・pin連鎖検査つき）から23行×C(115,2)=150,765生成事象で触れる
  宇宙137,959根をD4正準形で再導入し、safe8/unsafe8をK1097交替和形式とK1102アンカー
  並進3×3形式の2独立述語で全数判定（不一致0）・C(8,6)=28部分集合の内在被覆==
  生成witnessを100%全数で確認・providers 45,219根・hist・per-row demand・
  drop 4・greedy9根完全再現・K1102 matching witness 23根を再被覆検証
  （全18 gate fail-closed PASS）。判定は**UNSAT・最小被覆9**。
  **数え上げ証明書**: 3行（`00000000000000003800000008002010`・
  `0000000000000000380000000a080000`・`00000000020000801202000000100000`）は
  P‴上に3行providerを1本も持たず、これらに触れる根は2行以下しか被覆できない。
  8根のうちk根がこの3行を被覆するとk≥2が必要な一方、被覆枠の算術は
  k ≤ 3·8−23 = 1 を要求して矛盾（手計算検証可能）。
  **2形の完全探索も同一結論**: Shape B（7 triple+1 pair・pair pattern重複除き100種）・
  Shape A（8 triple・重複1行・全dで351組の対）をメモ化exact coverで完全探索して
  不成立、独立第二実装（新規幾何・メモなし・分岐順不同）も同一列挙空間でUNSAT。
  有界8の下界は任意の宇宙で有効なまま、9はP‴に特有の確定である。
  interval [8,9]は[9,9]へ崩壊し、**greedy 9根代替掃引計画（18 probes）はP‴上で
  候補根数最小**。3回実行byte-identical（機械SHA-256 da51063c…・正本
  SHA-256 c5aaf83e…・約41秒/run）。
  詳細は[判定実験](../../experiments/n11-residual23-eight-root-cover-decision-20261120/README.md)・[判定正本](../../experiments/n11-residual23-eight-root-cover-decision-20261120/output/residual23-eight-root-cover-decision-20261120.json)・[研究ログ](../../log/2026-11-20-n11-residual23-eight-root-cover-decision.md)を参照する。

---

## 詳細

単一オーナー宣言ノート（commit 22d85b72・先行出版）の下で、K1095 README
「次の一手」第1項（pool P‴ 再解決）・第2項（WIN16の内在被覆確認）を実施した。
除外50根後の pool P‴（120,424根）上で残余23行は stranded 0・**greedy 9根が
leftover 0完全被覆**（下界6に対し+3）・マッチング23。WIN16のper-root内在被覆は
主張を包含し、K1095 3根目に初の余剰1行（K1096証明書根の主張行）を記録、
残余23行へのintrinsic被覆は0行。全体計画は16 WIN+9代替=25根で72行。
後続監査で下界を8に強化し、さらに判定実験の単一オーナー宣言（commit cb31752551）の下で
8根被覆を厳密に判定して**UNSAT・最小被覆9を確定**した（3行の3行provider零による
数え上げ証明書+2形完全探索+独立第二実装の三重確認）。
次の一手は代替9根のdepth-10掃引（18 probes・P‴上で計画は最小確定済み）・
残るWIN候補の証明書抽出（root 8003180はK1096で出版済み・別1根は宣言済み: commit 4496c888）・
K1096証明書のreceipt fold。行は1行も閉じていない。
詳細は[実験](../../experiments/n11-residual72-safe8-refuted50-refsolve-20261120/README.md)・
[再解決正本](../../experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json)・
[判定実験](../../experiments/n11-residual23-eight-root-cover-decision-20261120/README.md)・
[研究ログ](../../log/2026-11-20-n11-residual72-safe8-refuted50-refsolve.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
