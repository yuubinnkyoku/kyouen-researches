---
id: K0827
title: "7xm q=4,5,6 row-deficient witness bands — witnesses 7x4..7x35 (q=4; 4..21 SAT, 22..35 constructive extension), 7x5..7x32 (q=5; 32 by row-split), 7x6..7x27 (q=6; 27 by row-split); M_{7,4} >= 36, M_{7,5} >= 33, M_{7,6} >= 28; first results for the three families"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census + sequential-counter/maximality core used verbatim (sat.js/sat2.js); def-mode single clause is the complete encoding of 'total < 7(q-1) iff some row <= q-2'"
- type: depends_on
  target: K0068
  note: "(7,4) upper bound T_7 = 3+2{C(19,3)-6} = 1929 by the general q=4 parity theorem (all maximals 3w stones, g=(3w-|S|) mod2 for m >= T_w); matches K0318 substitution U=1929"
- type: depends_on
  target: K0318
  note: "upper bounds U_{7,6}=862, U_{7,5}=1142 by curve-packing substitution (w7_upper_bounds.json of seven-row-inband-families-20261114)"
- type: depends_on
  target: K0826
  note: "same machinery and runner as the (7,7) search (same session, same binary); q <= w families confirmed to have continuous witness bands from m=q"
artifacts:
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/report.md
  role: proof
  note: "claims, per-family results tables, method (sat2.js all-triples census at q<=w, m>=q minimum width), dual verification protocol, honest unswept frontiers, scope and limits"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q6-def-search/records.jsonl
  role: data
  note: "21 records m=6..26 all SAT dual-verified: m=6..15 deep deficiency 20..33 stones, m=16..25 single-deficiency 34 stones, m=26 33 stones rows 5/5/5/5/5/3/5 (441,809 conflicts); raw kissat output for m=26 included"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q5-def-search/records.jsonl
  role: data
  note: "18 records m=5..22 all SAT dual-verified: deep deficiency 14..26 stones then single-deficiency 27 stones (m=20 has a 25-stone witness with a 1-stone row 4/1/4/4/4/4/4); raw kissat output for m=22 included"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q4-def-search/records.jsonl
  role: data
  note: "11 records m=4..14 all SAT dual-verified 0 conflicts: 8..15 stones, deficiency 13..6, [3,3,3,3,1,1,1]-type at m=12..14; raw kissat output for m=14 included"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q5-frontier-extension/records.jsonl
  role: data
  note: "9 records m=23..31 all SAT dual-verified single-deficiency 27 stones (except 25-stone 1-stone-row witnesses at m=25 and previously m=20); conflicts 1,200 / 2,029 / 7,730 / 3,257 / 23,195 / 48,433 / 116,669 / 220,814 / 31,000 (non-monotone dip at m=31); M_{7,5} >= 32"
- path: research/experiments/seven-row-q4-q6-witness-search-20261114/output/q4-frontier-extension/records.jsonl
  role: data
  note: "7 records m=15..21 all SAT dual-verified 0 conflicts: 16..18 stones, deficiency 6..3, [3,3,3,3,3,2,1]-type at m=20,21; M_{7,4} >= 22 (band extended constructively to m=35 in seven-row-q4-extension-band-20261114)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/ts-verify-cross-family.json
  role: data
  note: "third-system (pure TS/BigInt) cross-family record; q4/q5/q6 entries: (7,6) m=26 (33 stones rows 5/5/5/5/5/3/5, 5073 circles), (7,5) m=31 (27 stones rows 3/4/4/4/4/4/4, 2742 circles), (7,4) m=21 (18 stones rows 3/3/3/3/3/2/1, 799 circles) all PASS safe+maximal+row-deficient — triple-verified"
- path: research/experiments/seven-row-q4-extension-band-20261114/report.md
  role: proof
  note: "blocking-coverage extension lemma, constructive extension of the q=4 band to m=22..35 without SAT (free empty-column extension of the m=21 witness to 22; greedy adds + deterministic hill-climb to 23..35), exact per-width verification, honest scope (heuristic search; widths >= 36 unswept; M in [36,1929])"
- path: research/experiments/seven-row-q4-extension-band-20261114/output/verification.json
  role: data
  note: "per-width exact verification records m=22..35 (safe + maximal + row-deficient PASS, uncovered 0, maxCirc/maxLine 3), configs C22/CA/CB with contiguous coverage 22/31/35, curve counts, negative control (4-collinear correctly unsafe), provenance"
- path: research/experiments/seven-row-q4-extension-band-20261114/output/witnesses/s7x22q4_none.witness.json
  role: data
  note: "width-22 witness = the m=21 witness stones (free empty-column extension); s7x23..31q4_none.witness.json = 20-stone config CA (maxX=22, coverage 31, rows [3,3,3,3,3,3,2]); s7x32..35q4_none.witness.json = 20-stone config CB (maxX=26, coverage 35); all third-system verified (tsVerify); jsVerify/pyVerify re-verification complete (m=22..27 frontier-20261115 stone-identical, m=28..35 sat3-20261115 independent witnesses, constructive files themselves js+py re-verified 14/14 by seven-row-q5-q6-frontier-row-split-20261115)"
- path: research/experiments/seven-row-q4-extension-band-20261114/scripts/extend_band.ts
  role: verifier
  note: "pure TS/BigInt constructive extension + exact verification script (third independent system, no repo code, no SAT); regenerates and re-verifies the whole band 22..35 from the three configs"
- path: research/experiments/seven-row-q4-q6-witness-frontier-20261115/output/records.jsonl
  role: data
  note: "9 records: (7,4) m=22..27 all SAT 0 conflicts dual-verified (18 stones [3,3,3,3,3,2,1] at 22; 20 stones [3,3,3,3,3,3,2] at 23..27, matching the constructive free-extension and config CA) - completes the jsVerify/pyVerify re-verification of the constructive band for m=22..27; (7,5) m=23 SAT 1,200 conflicts bit-exact with the published record (calibration); (7,5) 7x32 INDET 329,844 conflicts / 200s and (7,6) 7x27 INDET 744,027 conflicts / 200s honest frontier negatives (not absence claims; both resolved SAT by seven-row-q5-q6-frontier-row-split-20261115 row-splits); sat2.js all-triples census OOM (rc 137, 2560MB heap) at 7x28 q=4 - SAT-based q4 extension blocked at m=28"
- path: research/experiments/seven-row-q4-extension-band-sat3-20261115/output/records.jsonl
  role: data
  note: "9 records: (7,4) m=28..35 all SAT (kissat 36-537 conflicts), decoded 20-stone witnesses dual-verified (js+py), row multiset {3,3,3,3,3,3,2} same as the constructive band but independently placed; m=35 lex=H,V,HV cross-encoding SAT (314 conflicts) dual-verified; sat3.js streaming census resolves the sat2.js 7x28 census OOM wall; output/calibration.jsonl: m=22..27 q4 reproduction (0 conflicts, witness stones 6/6 identical to the published records) + (7,5) m=23 kissat calibration 1,200 conflicts bit-exact"
- path: research/experiments/seven-row-q4-extension-band-sat3-20261115/scripts/sat3.js
  role: verifier
  note: "streaming all-triples census generator, DIMACS byte-identical to sat2.js (K0810 encode core verbatim: counter/totalizer/lexLeader/CLI): clause streaming to disk + first-encounter circle emission + O(w) row-quadratic point scan; unblocks q<=w SAT search at 7x28+ (gen ~3-5s per width at m=28..35, CNF 103MB at m=35); 9/9 control cmp MATCH vs sat2.js"
- path: research/experiments/seven-row-q5-q6-frontier-row-split-20261115/output/q5-m32-row-split/records.jsonl
  role: data
  note: "(7,5) m=32 rowY=0 rowfixed SAT 129,923 conflicts (250s cap), 27-stone single-deficiency witness rows [3,4,4,4,4,4,4] js+py dual-verified; resolves the 7x32 frontier negative (frontier-20261115: 200s OR INDET 329,844); M_{7,5} >= 33, frontier moves to 7x33"
- path: research/experiments/seven-row-q5-q6-frontier-row-split-20261115/output/q6-m27-row-split/records.jsonl
  role: data
  note: "(7,6) m=27: def-mode OR INDET 175s (703,590 conflicts), rowY=0/1/2 INDET 250s (989,735 / 1,078,304 / 1,074,595), rowY=3 SAT 230,973 conflicts - 34-stone single-deficiency witness rows [5,5,5,4,5,5,5] js+py dual-verified; resolves the 7x27 frontier negative (frontier-20261115: 200s OR INDET 744,027); M_{7,6} >= 28, frontier moves to 7x28; INDET entries are honest negatives (not absence claims)"
- path: research/experiments/seven-row-q5-q6-frontier-row-split-20261115/output/q4band-witness-dual-verification/records.jsonl
  role: data
  note: "jsVerify (sat.js verifyConfig) + pyVerify (Python Fraction) on the published constructive witness files s7x22..35q4_none.witness.json of seven-row-q4-extension-band-20261114: 14/14 PASS (m=22 18 stones [3,3,3,3,3,2,1], m=23..35 20 stones [3,3,3,3,3,3,2]) - completes the four-way verification of the constructive files themselves (independent of the sat3-20261115 SAT witnesses)"
- path: research/experiments/seven-row-q4-witness-band-36-40-20261115/output/records.jsonl
  role: data
  note: "5 records: (7,4) m=36..40 all SAT (kissat 117..402 conflicts, 200s cap, sat3-generated CNFs), decoded 20-stone witnesses dual-verified (js+py), row multiset {3,3,3,3,3,3,2}; extends the witness band beyond the constructive limit m=35; M_{7,4} lower bound 36 -> 41 (M in [41,1929]); frontier now 7x41 (untested, not an absence claim); sat3 dedup Set OOMs at m=50 generation (>=q-only key registration is the next fix, output-invariant)"
scope: "finite machine verification: kissat 4.0.4 for m=4..21; exact rational arithmetic (pure TS/BigInt) for m=22..35; SAT re-verification m=22..35 (22..27: seven-row-q4-q6-witness-frontier-20261115; 28..35: seven-row-q4-extension-band-sat3-20261115, sat3.js streaming census byte-identical to sat2.js); (7,5) m=5..32 and (7,6) m=6..27 all SAT dual-verified (m=32/27 via rowY fixed-row splits, seven-row-q5-q6-frontier-row-split-20261115); widths stated per family only; up to census completeness and solver/arithmetic correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction, all records jsVerify/pyVerify true) + third independent verification system (pure TS/BigInt, no repo code: verify_independent.ts of seven-row-q7-witness-search-20261114 — frontier witnesses (7,6) m=26, (7,5) m=31, (7,4) m=21 all PASS safe+maximal+row-deficient, record in seven-row-q7-witness-search-20261114/output/ts-verify-cross-family.json — triple-verified) + deterministic CNF regeneration from the calibrated sat2.js + cross-environment-reset bit-exact reproduction of the frontier records ((7,5) m=23..26 and (7,4) m=15 re-run after an environment reset with identical conflicts 1,200/2,029/7,730/3,257 and 0) + constructive extension band m=22..35 (seven-row-q4-extension-band-20261114): blocking-coverage lemma gives a free empty-column extension of the triple-verified m=21 witness to m=22; deterministic greedy adds + hill-climb (extend_band.ts, exact TS/BigInt, no SAT) produce 20-stone configs CA (maxX=22, coverage W=31, witnesses m=23..31) and CB (maxX=26, W=35, witnesses m=27..35, used for 32..35); all widths 22..35 verified safe+maximal+row-deficient by exact rational arithmetic (uncovered 0, negative control detected); M_{7,4} >= 36 (M in [36, 1929]); jsVerify/pyVerify re-verification of the extension-band witnesses: m=22..27 SAT re-confirmed and dual-verified by seven-row-q4-q6-witness-frontier-20261115 (kissat 0 conflicts, rows matching the constructive configs; four-way verified: kissat SAT + jsVerify + pyVerify + tsVerify), m=28..35 SAT re-confirmed and dual-verified by seven-row-q4-extension-band-sat3-20261115 (sat3.js streaming census, DIMACS byte-identical to sat2.js: 9 controls cmp MATCH, (7,5) m=23 kissat calibration 1,200 conflicts bit-exact, m=22..27 witness reproduction 6/6 stones identical; kissat 36-537 conflicts at m=28..35, all 200s cap; independent 20-stone witnesses with row multiset {3,3,3,3,3,3,2} matching the constructive configs; m=35 lex=H,V,HV cross-encoding SAT 314 conflicts) - the whole band m=4..35 is now four-way verified (kissat SAT + jsVerify + pyVerify + tsVerify), and the constructive files themselves are js+py re-verified 14/14 (seven-row-q5-q6-frontier-row-split-20261115). (7,5) m=32 and (7,6) m=27 resolved by rowY fixed-row splits (seven-row-q5-q6-frontier-row-split-20261115, rowsplit.sh, sat2.js --rowY=Y, kissat 4.0.4 sha256 21da5d98..., post-reset calibration (7,5) m=31 def-mode 31,000 conflicts bit-exact): (7,5) m=32 rowY=0 SAT 129,923 conflicts, 27-stone witness [3,4,4,4,4,4,4]; (7,6) m=27 rowY=3 SAT 230,973 conflicts, 34-stone witness [5,5,5,4,5,5,5]; both js+py dual-verified; M_{7,5} >= 33 (M in [33, 1142]), M_{7,6} >= 28 (M in [28, 862]). See report.md."
---

# 7xm q=4,5,6 行欠損witness帯 — 3ファミリー初の結果（M_{7,4} ≥ 36・M_{7,5} ≥ 33・M_{7,6} ≥ 28）

## 主張

1. **(7,6)**: 行欠損の極大安全配置が **m=6..27 の全幅で存在**
   （m=6..15 深欠損 20..33石・m=16..25 単一欠損34石・m=26 は33石
   rows 5/5/5/5/5/3/5・441,809 conflicts・m=27 は34石
   rows [5,5,5,4,5,5,5]・rowY=3 分割 230,973 conflicts）。
   **M_{7,6} ≥ 28**（上界 862・K0318 代入）。
2. **(7,5)**: **m=5..32 の全幅で存在**（m=16..31 は単一欠損27石を含む。
   m=20 と m=25 は25石・1石行の深欠損例。conflicts は 1,200..220,814 で
   単調ではなく m=31 は 31,000 と急落する。m=32 は rowY=0 分割で
   27石 rows [3,4,4,4,4,4,4]・129,923 conflicts）。
   **M_{7,5} ≥ 33**（上界 1142・K0318 代入）。
3. **(7,4)**: **m=4..35 の全幅で存在**。
   - m=4..21 は SAT 探索（8..18石・conflicts 全幅 0・m=20,21 は
     [3,3,3,3,3,2,1] 型18石・2系統検証、m=21 は3系統検証）。
   - m=22 は m=21 witness の**空列追加**（ブロック被覆が x=21 まで連続）。
   - m=23..31 は20石構成 CA・m=32..35 は20石構成 CB（いずれも
     rows [3,3,3,3,3,3,2]・構成的延伸・後述）。
   **M_{7,4} ≥ 36**。上界は **K0068 の一般 q=4 偶奇定理 T_7=1929**
   （K0318 代入 U=1929 と一致）。
4. 検証: m=4..21 は2系統検証（census 不使用 sat.js verifyConfig + Python Fraction）、
   m=21 は加えて第3系統（純TS/BigInt）で3系統検証。
   m=22..35 は4系統検証（tsVerify + SAT再確認 + 構成ファイル自体の js+py 再検証）。
   (7,5) m=32・(7,6) m=27 は2系統検証。

## 手法と検証

m=4..31 の SAT 探索は K0810 の sat2.js を verbatim（q ≤ w で genfast.js 不適用・
全三つ組census。census は m ≥ q を要求し、最小幅は m=q）。kissat 4.0.4 公式バイナリ。
決定性: 同一セッションの (7,7) 実験で m=24 conflicts bit-exact 再現を確認
（K0826）・本実験の全 CNF はスクリプトから決定的に再生成可能。

**構成的延伸（m=22..35）**: ブロック被覆補題 — セルがブロック済み ⟺ 3石を含む
円/直線上にある（追加すれば4石曲線＝違反）。ちょうど3石の行は行直線全体を
ブロックする。全7行が x が [0, W) で連続被覆され全石が x < W なら、maxX < w ≤ W の
すべての幅 w で witness になる。m=21 witness の被覆計算だけで m=22 が得られ
（空列追加）、貪欲追加2石＋決定的山登りで CA (W=31)・CB (W=35) に到達
（SATソルバ不使用・純TS/BigInt・乱数不使用）。

**rowY 固定分割**: def-mode OR（∃欠損行）を「欠損行 = rowY」で固定した
sat2.js --rowY=Y 符号化に分解する。(7,8) m=24（rowY=3）・(7,7) m=25/26
（rowY=3）に続き、(7,5) m=32（rowY=0）・(7,6) m=27（rowY=3）で
5例目・6例目の成功。OR が 200s cap で INDET の前線でも、
rowY 分割で数分以内に SAT する場合がある。

## 観測（全称主張ではない）

q ≤ w の 7行族（q=4,5,6,7）は m=q から継続的な witness 帯を持ち、
深欠損から単一欠損へ移行する。q > w の (7,8)..(7,10) では witness-free 帯が
出現するのと対照的。K0318/K0068 の上界は witness が有限幅で消えることを保証。
構成的延伸では行0..5 が各3石（行直線で自動ブロック）＋欠損行6が2石の構造で、
20石の場合の被覆容量（円 C(20,3)=1140 × 各欠損行 ≤2 ヒット ≈ 2280 セル/行）は
K0068 上界 1929 を下回らず、延伸余地は大きい（残る障害は交点の整数性）。

## 範囲と限界

有限機械検証。前線は 7×36 (q=4)・7×28 (q=6)・7×33 (q=5)。
m=22..35 の探索は決定的ヒューリスティック（全称不在証明ではない）。
sat2.js census の実用範囲（n=7m ≈ 200）を超える SAT 延長には
帯状censusの一般化（genfast の q ≤ w 版）が必要だが、sat3.js（streaming・
sat2 byte-identical）と構成的延伸の双方で継続可能。
M の確定には前線評価と上界改善（K0342 型 tail 評価）が残る。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。

## 追記 (2026-11-15 SATによる m=22..27 再検証と前線負記録)

`seven-row-q4-q6-witness-frontier-20261115`（(7,9)帯閉包レーンの後続バッチ）:

1. **(7,4) m=22..27 を SAT + 2系統検証で再確認**（sat2.js 完全符号化・kissat 4.0.4・
   全幅 0 conflicts・sat.js verifyConfig + Python Fraction とも PASS）。
   m=22 は 18石 [3,3,3,3,3,2,1]（構成的 free extension と一致）・
   m=23..27 は 20石 [3,3,3,3,3,3,2]（config CA と同一行構造）。
   よって構成的延伸帯のうち **m=22..27 は4系統検証済み**（kissat SAT + js + py + tsVerify）。
   m=28..35 は引き続き tsVerify のみ（再検証 pending）。
2. **前線負記録**: (7,5) 7×32 は 200s INDET（329,844 conflicts）・
   (7,6) 7×27 は 200s INDET（744,027 conflicts）。いずれも不在主張ではない
   （いずれも後続の row-split で SAT に解決・下記追記）。
3. **sat2.js census 壁**: 7×28 (q=4) の全三つ組census生成が node heap 2560MB で
   OOM (rc 137)。SAT による (7,4) 帯の直接延長は m=28 で停止。
   m ≥ 28 の SAT 探索には q ≤ w 版メモリ有界 census の開発が必要。
   前線は 7×36 のまま（M ∈ [36, 1929] 不変）。
4. 較正: (7,5) m=23 再実行 1,200 conflicts が本項目の公開 record と bit-exact。

## 追記 (2026-11-15 sat3 streaming census による m=28..35 の SAT 再検証)

`seven-row-q4-extension-band-sat3-20261115`（frontier レーンの後続）:

1. **sat2.js の 7×28 census メモリ壁（OOM rc 137）を sat3.js で解消**。
   変更は3点のみ（encode core は verbatim）: 節のストリーム出力（OOM 主因の
   `enc.clauses[]` 保持+`toDimacs()` GB 結合を廃止）・円の初遭遇処理（circMap
   挿入順 = 三つ組列挙順でその場 emit）・円の点走査 O(w) 化（行ごと2次方程式の
   整数根）。**DIMACS は sat2.js と byte-identical**（9対照 cmp MATCH、
   cap/seq・cap/tot・lex・rowY 全モード）。
   較正: (7,5) m=23 で 1,200 conflicts bit-exact・(7,4) m=22..27 の再実行は
   全幅 0 conflicts で **公開 witness と石配置 6/6 完全一致**
   （output/calibration.jsonl）。
2. **m=28..35 全幅 SAT・2系統検証 PASS**（kissat 36〜537 conflicts・生成3.1〜5.2s・
   m=35 は 5,510,073 clauses/CNF 103MB）。witness はいずれも **20石で行マルチセット
   {3,3,3,3,3,3,2}** — 構成的延伸（config CA/CB）と同一マルチセット・配置は独立。
   m=35 は lex=H,V,HV 別符号化でも SAT（314 conflicts・2系統検証 PASS）。
3. **結果: m=4..35 全帯が4系統検証済み**（m=4..21 SAT 2系統+K0827 既往、
   m=22..27 SAT+構成が石配置まで一致、m=28..35 SAT と構成が互いに独立の証明）。
   M_{7,4} ∈ [36, 1929] は不変。m ≥ 36 は未実施（不在主張ではない）。
   sat3 により (7,4) の SAT 探索は m=36 以降も生成 ~6s/幅で実行可能になった。

## 追記 (2026-11-15 rowY 固定分割による (7,5)/(7,6) 前線の解決)

`seven-row-q5-q6-frontier-row-split-20261115`:

1. **(7,5) m=32 SAT・2系統検証 PASS**（rowY=0 固定分割・129,923 conflicts・
   250s cap・27石 rows [3,4,4,4,4,4,4]）。前線負記録（frontier-20261115:
   200s OR INDET 329,844）を解決し、**witness帯は m=5..32 に拡大、
   M_{7,5} ≥ 33**（M ∈ [33, 1142]）。前線は 7×33。
2. **(7,6) m=27 SAT・2系統検証 PASS**（rowY=3 固定分割・230,973 conflicts・
   250s cap・34石 rows [5,5,5,4,5,5,5]・単一欠損）。OR は 175s INDET
   (703,590)・rowY=0/1/2 は 250s INDET（989,735/1,078,304/1,074,595）で
   いずれも不在主張ではない。**witness帯は m=6..27 に拡大、
   M_{7,6} ≥ 28**（M ∈ [28, 862]）。前線は 7×28。
3. 較正: 環境リセット後の再構築で (7,5) m=31 def-mode 再実行 31,000 conflicts
   bit-exact（公開 record と一致）・kissat は sha256 21da5d98… の同一公式バイナリ
   （rel-4.0.4）。rowY 分解は (7,8) m=24・(7,7) m=25/26 に続き
   5例目・6例目の成功。
4. **(7,4) 構成witnessファイルの2系統再検証**: seven-row-q4-extension-band-20261114
   の output/witnesses/s7x22..35q4_none.witness.json 全14幅が
   sat.js verifyConfig + Python Fraction で 14/14 PASS
   （output/q4band-witness-dual-verification）。sat3-20261115 の独立配置 SAT witness
   と合わせ、**構成ファイルそのものも4系統検証**となった。

## 追記 (2026-11-15 構成的限界35の先 — m=36..40 全幅 SAT・下界41)

`seven-row-q4-witness-band-36-40-20261115`（sat3 レーンの直接の続き）:

1. **witness 帯は m=35 で終わらない**: m=36..40 の全5幅で SAT witness が発見され
   （kissat 117..402 conflicts・生成6.0〜7.9s・m=40 は 8,101,031 clauses/CNF 155MB）、
   decode_verify.js + verify_witness.py の2系統検証 PASS。
   全 witness 20石・行マルチセット {3,3,3,3,3,3,2}（m=28..35 と同一）。
2. **M_{7,4} ∈ [41, 1929] に更新**（下界36→41・上界は K0068/K0318 のまま）。
   witness 探索の前線は 7×41（未実施・不在主張ではない）。
   上記 row-split 追記の「M_{7,4} ∈ [36,1929]」は sat3 時点の記録（当時正確）。
3. sat3 の dedup Set は m=50 生成で OOM（rc 137・全円キー保持のため）。
   ≥q点円のみ Set に登録する修正で出力を変えずに縮小可能
   （q点未満の円は三つ組が1つしかなく再遭遇しないため）— 次バッチの課題。
