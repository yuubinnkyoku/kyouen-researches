---
id: K0827
title: "7xm q=4,5,6 row-deficient witness bands — witnesses 7x4..7x35 (q=4; 4..21 SAT, 22..35 constructive extension), 7x5..7x31 (q=5), 7x6..7x26 (q=6); M_{7,4} >= 36, M_{7,5} >= 32, M_{7,6} >= 27; first results for the three families"
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
  note: "width-22 witness = the m=21 witness stones (free empty-column extension); s7x23..31q4_none.witness.json = 20-stone config CA (maxX=22, coverage 31, rows [3,3,3,3,3,3,2]); s7x32..35q4_none.witness.json = 20-stone config CB (maxX=26, coverage 35); all third-system verified (tsVerify), jsVerify/pyVerify re-verification pending"
- path: research/experiments/seven-row-q4-extension-band-20261114/scripts/extend_band.ts
  role: code
  note: "pure TS/BigInt constructive extension + exact verification script (third independent system, no repo code, no SAT); regenerates and re-verifies the whole band 22..35 from the three configs"
- path: research/experiments/seven-row-q4-q6-witness-frontier-20261115/output/records.jsonl
  role: data
  note: "9 records: (7,4) m=22..27 all SAT 0 conflicts dual-verified (18 stones [3,3,3,3,3,2,1] at 22; 20 stones [3,3,3,3,3,3,2] at 23..27, matching the constructive free-extension and config CA) - completes the jsVerify/pyVerify re-verification of the constructive band for m=22..27; (7,5) m=23 SAT 1,200 conflicts bit-exact with the published record (calibration); (7,5) 7x32 INDET 329,844 conflicts / 200s and (7,6) 7x27 INDET 744,027 conflicts / 200s honest frontier negatives (not absence claims); sat2.js all-triples census OOM (rc 137, 2560MB heap) at 7x28 q=4 - SAT-based q4 extension blocked at m=28"
scope: "finite machine verification: kissat 4.0.4 for m=4..21; exact rational arithmetic (pure TS/BigInt) for m=22..35; widths stated per family only; up to census completeness and solver/arithmetic correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction, all records jsVerify/pyVerify true) + third independent verification system (pure TS/BigInt, no repo code: verify_independent.ts of seven-row-q7-witness-search-20261114 — frontier witnesses (7,6) m=26, (7,5) m=31, (7,4) m=21 all PASS safe+maximal+row-deficient, record in seven-row-q7-witness-search-20261114/output/ts-verify-cross-family.json — triple-verified) + deterministic CNF regeneration from the calibrated sat2.js + cross-environment-reset bit-exact reproduction of the frontier records ((7,5) m=23..26 and (7,4) m=15 re-run after an environment reset with identical conflicts 1,200/2,029/7,730/3,257 and 0) + constructive extension band m=22..35 (seven-row-q4-extension-band-20261114): blocking-coverage lemma gives a free empty-column extension of the triple-verified m=21 witness to m=22; deterministic greedy adds + hill-climb (extend_band.ts, exact TS/BigInt, no SAT) produce 20-stone configs CA (maxX=22, coverage W=31, witnesses m=23..31) and CB (maxX=26, W=35, witnesses m=27..35, used for 32..35); all widths 22..35 verified safe+maximal+row-deficient by exact rational arithmetic (uncovered 0, negative control detected); M_{7,4} >= 36 (M in [36, 1929]); jsVerify/pyVerify re-verification of the extension-band witnesses: m=22..27 SAT re-confirmed and dual-verified by seven-row-q4-q6-witness-frontier-20261115 (kissat 0 conflicts, rows matching the constructive configs; four-way verified: kissat SAT + jsVerify + pyVerify + tsVerify), m=28..35 still tsVerify-only pending. See report.md."
---

# 7xm q=4,5,6 行欠損witness帯 — 3ファミリー初の結果（M_{7,4} ≥ 36・M_{7,5} ≥ 32・M_{7,6} ≥ 27）

## 主張

1. **(7,6)**: 行欠損の極大安全配置が **m=6..26 の全幅で存在**
   （m=6..15 深欠損 20..33石・m=16..25 単一欠損34石・m=26 は33石
   rows 5/5/5/5/5/3/5・441,809 conflicts）。
   **M_{7,6} ≥ 27**（上界 862・K0318 代入）。
2. **(7,5)**: **m=5..31 の全幅で存在**（m=16..31 は単一欠損27石を含む。
   m=20 と m=25 は25石・1石行の深欠損例。conflicts は 1,200..220,814 で
   単調ではなく m=31 は 31,000 と急落する）。
   **M_{7,5} ≥ 32**（上界 1142・K0318 代入）。
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
   m=22..35 は第3検証系（純TS/BigInt 厳密計算・seven-row-q4-extension-band-20261114）
   で safe + maximal + 行欠損 PASS（jsVerify/pyVerify による再検証は今後のrunで追加）。

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

## 観測（全称主張ではない）

q ≤ w の 7行族（q=4,5,6,7）は m=q から継続的な witness 帯を持ち、
深欠損から単一欠損へ移行する。q > w の (7,8)..(7,10) では witness-free 帯が
出現するのと対照的。K0318/K0068 の上界は witness が有限幅で消えることを保証。
構成的延伸では行0..5 が各3石（行直線で自動ブロック）＋欠損行6が2石の構造で、
20石の場合の被覆容量（円 C(20,3)=1140 × 各欠損行 ≤2 ヒット ≈ 2280 セル/行）は
K0068 上界 1929 を下回らず、延伸余地は大きい（残る障害は交点の整数性）。

## 範囲と限界

有限機械検証。前線は 7×36 (q=4)・7×27 (q=6)・7×32 (q=5)。
m=22..35 の探索は決定的ヒューリスティック（全称不在証明ではない）。
sat2.js census の実用範囲（n=7m ≈ 200）を超える SAT 延長には
帯状censusの一般化（genfast の q ≤ w 版）が必要だが、構成的延伸は
census 不要でいくらでも継続可能。M の確定には
前線評価と上界改善（K0342 型 tail 評価）が残る。

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
   (7,6) 7×27 は 200s INDET（744,027 conflicts）。いずれも不在主張ではない。
3. **sat2.js census 壁**: 7×28 (q=4) の全三つ組census生成が node heap 2560MB で
   OOM (rc 137)。SAT による (7,4) 帯の直接延長は m=28 で停止。
   m ≥ 28 の SAT 探索には q ≤ w 版メモリ有界 census の開発が必要。
   前線は 7×36 のまま（M ∈ [36, 1929] 不変）。
4. 較正: (7,5) m=23 再実行 1,200 conflicts が本項目の公開 record と bit-exact。
