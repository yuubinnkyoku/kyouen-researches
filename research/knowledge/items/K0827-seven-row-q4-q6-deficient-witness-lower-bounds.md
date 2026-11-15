---
id: K0827
title: "7xm q=4,5,6 row-deficient witness bands — q=4: 7x4..7x59, q=5: 7x5..7x37, q=6: 7x6..7x31; M_{7,4} >= 60, M_{7,5} >= 38, M_{7,6} >= 32"
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
- path: research/experiments/seven-row-q4-band-42-56-20261115/README.md
  role: proof
  note: "7x42..7x56 の20石行欠損極大安全配置、M_{7,4}>=57 の有限証拠と探索限界"
- path: research/experiments/seven-row-q4-band-42-56-20261115/output/witnesses.json
  role: data
  note: "m=42,44,45,47,50,53 の6基礎配置"
- path: research/experiments/seven-row-q4-band-42-56-20261115/output/records.jsonl
  role: data
  note: "m=42..56 の15幅の配置再利用関係と検証状態"
- path: research/experiments/seven-row-q4-band-42-56-20261115/output/verification.json
  role: data
  note: "全15幅の安全性・極大性・行欠損を整数演算で独立検査"
- path: research/experiments/seven-row-q4-band-42-56-20261115/output/search_runs.json
  role: data
  note: "6つのseeded SA探索とm=57の未発見試行"
- path: research/experiments/seven-row-q4-band-42-56-20261115/scripts/search_seeded.js
  role: source
  note: "既存witnessを種にした決定的な貪欲極大化・焼きなまし探索"
- path: research/experiments/seven-row-q4-band-42-56-20261115/scripts/verify_witnesses.py
  role: verifier
  note: "探索censusを使わないPython任意精度整数による安全性・極大性検証"
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
- path: research/experiments/seven-row-q4-band-41-20261115/output/records.jsonl
  role: data
  note: "3 records: (7,4) m=41 SAT dual-verified (281 conflicts, 8.7M clauses, 20-stone witness rows [3,3,3,3,3,3,2]) - M_{7,4} lower bound 41 -> 42, frontier 7x42; m=42 and m=50 honest kissat OOM negatives (solver RAM wall ~9M clauses in the 2026-11-15 container, generation succeeded - not absence claims); includes the sat3 >=q-only dedup fix (output-invariant, byte-identity re-validated incl. preserved m=28/m=40 CNFs)"
- path: research/experiments/seven-row-q5-q8-sat-frontier-20261115/README.md
  role: proof
  note: "(7,6) m=28 rowY=3 SAT (442,479 conflicts) + m=29 free-column extension -> M_{7,6} >= 30; (7,5) m=33 rowY=0 SAT at 900s cap (655,159 conflicts) -> M_{7,5} >= 34; (7,7) m=27 and (7,8) m=25 all-4-mirror-class 250s INDET sweeps (honest negatives); sat3/sat2 rowfixed q5 CNF byte-identity calibration 2/2"
- path: research/experiments/seven-row-q5-q8-sat-frontier-20261115/output/q6-m28-row-split/records.jsonl
  role: data
  note: "(7,6) m=28 rowY=3 SAT 442,479 conflicts (cap 250), 34-stone single-deficiency witness rows [5,5,5,4,5,5,5] js+py dual-verified; the same 34 stones verify on the 7x29 board (output/freecol-extensions/s7x29q6.witness.json) giving M_{7,6} >= 30; m=30 free-column extension fails (cell (29,3))"
- path: research/experiments/seven-row-q5-q8-sat-frontier-20261115/output/q5-m33-rowY0-900s/records.jsonl
  role: data
  note: "(7,5) m=33 rowY=0 SAT at 900s cap, 655,159 conflicts, 27-stone single-deficiency witness rows [3,4,4,4,4,4,4] js+py dual-verified; resolves the 250s 4-class INDET negatives 345k..399k; M_{7,5} >= 34; m=34 free-column extension fails (cell (33,0))"
- path: research/experiments/seven-row-q5-q8-sat-frontier-20261115/output/q6-m30-rowY3-900s/records.jsonl
  role: data
  note: "(7,6) m=30 rowY=3 900s cap INDET 1,569,306 conflicts (honest negative, not absence; earlier 250s/280s negatives in output/q6-m30-row-split and output/q6-m30-rowY3)"
- path: research/experiments/seven-row-q5-q8-sat-frontier-20261115/output/ts-verify-batch2-crosscheck.json
  role: verifier
  note: "third-system (pure TS exact integer arithmetic, no repo code, no census, no SAT) crosscheck: (7,5) m=32/33, (7,6) m=27/28/29 all PASS safe+maximal+row-deficient (triple-verified); free-column negatives reproduced exactly (m=34 cell (33,0), m=30 cell (29,3)); 5 self-test controls pass"
- path: research/experiments/seven-row-q4-band-42-56-20261115/output/ts-verify-crosscheck.json
  role: verifier
  note: "second independent verification system (pure TS exact integer arithmetic, no repo code, no census, no SA): all 6 base configs PASS safe+maximal+row-deficient at their free-column chain maxima (43/44/46/49/52/56), covering all 15 widths m=42..56 by monotonicity; the SA band is dual-verified (Python + TS); 3 controls pass"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/README.md
  role: proof
  note: "幅53の20石証人の2-for-2近傍を完全列挙し、7x57の2証人と7x59の行欠損極大証人を構成。M_{7,4}>=60"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/scripts/audit_two_swap.cpp
  role: source
  note: "整数行列式と包除原理で2-for-2候補を完全列挙するC++実装"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/scripts/verify_witness.py
  role: verifier
  note: "正規化整数直線・円方程式による独立Python検証器。7x57/7x59の安全性と極大性を再検査"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/output/two_swap_audit.json
  role: data
  note: "3つの基礎配置・幅の2-for-2近傍全列挙結果"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/output/verification.json
  role: verifier
  note: "発見した2配置の独立検証結果"
- path: research/experiments/seven-row-q4-width59-two-swap-20261115/output/witness_7x59.json
  role: data
  note: "7x59の20石証人、57個の欠損行セルの遮断確認、右端2セルの具体的曲線"
- path: research/experiments/seven-row-q5-witness-surgery-20261115/README.md
  role: proof
  note: "(7,5) m=34 witness by witness surgery (2-stone relocation of the m=33 witness targeting the unique uncovered cell (33,0)), depth-1/depth-2 relocation search, TS-exhaustive verification, M_{7,5} >= 35"
- path: research/experiments/seven-row-q5-witness-surgery-20261115/output/witness-7x34.json
  role: data
  note: "both 7x34 witnesses (winA/winB, 27 stones rows [3,4,4,4,4,4,4]) with exhaustive verification records and the 7x35 coverage profile"
- path: research/experiments/seven-row-q5-witness-surgery-20261115/scripts/witness_surgery.ts
  role: source
  note: "pure TS surgery search (inventory-based incremental pruning + brute re-verification) and the independent exhaustive verifier (5-subset enumeration safety + per-cell maximality)"
- path: research/experiments/seven-row-q5-m37-surgery-20261115/README.md
  role: proof
  note: "(7,5) m=35..37 witnesses by complete two-edit surgery enumeration of the m=34 witness (final-state case split targeting T=(34,0)); M_{7,5} >= 38; fresh independent pure-TS re-verification"
- path: research/experiments/seven-row-q5-m37-surgery-20261115/output/witness-7x37.json
  role: data
  note: "winC 27 stones rows [3,4,4,4,4,4,4], surgery description, chain profile 7x33..7x38, verification record"
- path: research/experiments/seven-row-q5-m37-surgery-20261115/scripts/verify_and_campaign.ts
  role: verifier
  note: "fresh independent pure-TS machine (no repo code/census/SAT): winC safety+maximality+profile, seed profiles, surgery cases A/F/b/b2a1 complete re-enumeration (unique witness winC)"
- path: research/experiments/seven-row-q6-m30-surgery-negative-20261115/README.md
  role: proof
  note: "initial partial record of the m=29 seed surgery; the 1,667,250-candidate line-based gap and all listed local classes were rerun in seven-row-q6-m30-surgery-completion-20261115: 1,781,021 unique candidates, 126,730 safe, 0 maximal (local only)"
- path: research/experiments/seven-row-q6-m30-surgery-negative-20261115/output/seed-verification.json
  role: verifier
  note: "fresh pure-TS re-verification of the s7x29q6 seed (safe, maximal on 7x29, only (29,3) uncovered on 7x30), T-curve census, all session case counts re-derived, and the completeness gap quantified"
- path: research/experiments/seven-row-q6-m30-surgery-completion-20261115/README.md
  role: proof
  note: "(7,6) m=29 seed to 7x30: complete disjoint classification of all <=2-removal/<=2-addition T-repairs with final size <=34; 1,781,021 unique candidates, 126,730 safe, 0 maximal; local negative only"
- path: research/experiments/seven-row-q6-m30-surgery-completion-20261115/scripts/verify_surgery.py
  role: verifier
  note: "independent exact Fraction circumcentre verifier for all six surgery families, seed curve census, safety and maximality"
- path: research/experiments/seven-row-q6-m30-surgery-completion-20261115/scripts/crosscheck_gap_cases.cpp
  role: verifier
  note: "independent normalized-integer line/circle crosscheck of the two formerly omitted line-based families (1,667,250 candidates)"
- path: research/experiments/seven-row-q6-m30-surgery-completion-20261115/output/audit.json
  role: data
  note: "six disjoint family counts, seed/T curve census, completeness scope and exact result"
- path: research/experiments/seven-row-q6-m30-surgery-completion-20261115/output/cpp_gap_crosscheck.json
  role: data
  note: "C++ crosscheck: gap-A 1,631,250 / gap-B 36,000 candidates, 103,923 safe, 0 maximal"
- path: research/experiments/seven-row-q5-m38-surgery-negative-20261115/README.md
  role: proof
  note: "(7,5) m=38 complete two-edit surgery of winC (T'=(37,0)): six final-state cases, 0 witnesses (local negative, not absence); exact U-set pruning with ground-truth audits"
- path: research/experiments/seven-row-q5-m38-surgery-negative-20261115/output/surgery-m38-summary.json
  role: data
  note: "census (no 4-stone T-curve; only the row-0 line y=0 has empty cells among the three 3-stone T-curves), six case counts, m35 case-b replica control, U validation 15/15, 20 ground-truth audit units all 0 maximal"
- path: research/experiments/seven-row-q5-m38-surgery-negative-20261115/scripts/verify_surgery_m38.ts
  role: verifier
  note: "pure TS machine (no repo code/census/SAT): all six cases with exact U-set pruning, m35 replica control, U validation, and skip audits in one script"

- path: research/experiments/seven-row-q6-m30-class-split-20261115/README.md
  role: proof
  note: "(7,6) m=30 witness by class {3} class-split SAT 2,670,296 conflicts/497.0s; 71 row-mirror canonical deficiency classes enumerated; (7,29,6) class {3} positive control SAT decoding a second distinct m=29 witness; M_{7,6} >= 31, frontier 7x31"
- path: research/experiments/seven-row-q6-m30-class-split-20261115/output/records.jsonl
  role: data
  note: "per-instance records: (7,29,6) class {3} control SAT 3,074,703 conflicts/545.5s; (7,30,6) class {3} SAT 2,670,296 conflicts/497.0s (cap 600, cnf md5 09e969b9461e413551f61f76bff817ce)"
- path: research/experiments/seven-row-q6-m30-class-split-20261115/output/c3.witness.json
  role: data
  note: "34-stone single-deficiency m=30 witness rows [5,5,5,4,5,5,5] row 3 cols [12,23,27,29]; c3.perturbed.json negative control (stone (12,3) removed -> not-maximal) and c3.pyverify.json Fraction verification included"
- path: research/experiments/seven-row-q6-m30-class-split-20261115/scripts/verify_witness_det.js
  role: verifier
  note: "third verification system: pure-integer 4x4-determinant line/circle test with built-in self-tests, no repo code; PASS on the m=30 witness (maxLine 5, maxCircle 5, uncovered 0) and not-maximal on the perturbation control"
- path: research/experiments/seven-row-q6-m31-frontier-20261115/README.md
  role: proof
  note: "(7,6) m=31 witness by complete two-edit surgery of the m=30 witness (unique 2-stone relocation among 2,140,633 candidates); M_{7,6} >= 32, frontier 7x32"
- path: research/experiments/seven-row-q6-m31-frontier-20261115/scripts/surgery_m31.py
  role: source
  note: "deterministic complete enumeration of final states S' = seed - R + A (removals <=2, additions <=2, final size <=34, T occupied or blocked); exact Fraction arithmetic with self-tests"
- path: research/experiments/seven-row-q6-m31-frontier-20261115/output/surgery-m31.json
  role: data
  note: "witness record R={(19,2),(25,4)} A={(27,2),(29,4)}, 34 stones rows [5,5,5,4,5,5,5]; T-curve census c4=2 c3=11; candidates 2,140,633, safe 1"
- path: research/experiments/seven-row-q6-m31-frontier-20261115/output/m31.detverify.json
  role: data
  note: "pure-integer 4x4-determinant verification: maxLine 5, maxCircle 5, uncovered 0; Fraction pyverify and the perturbed negative-control JSON alongside"

scope: "finite machine verification: current q4 witness band m=4..59 (M_{7,4}>=60; m=42..56 exact integer verification, m=57..59 verified by 2-for-2 exchange plus exact independent integer line/circle checks); kissat 4.0.4 for m=4..21; exact rational arithmetic (pure TS/BigInt) for m=22..35; SAT re-verification m=22..35 (22..27: seven-row-q4-q6-witness-frontier-20261115; 28..35: seven-row-q4-extension-band-sat3-20261115, sat3.js streaming census byte-identical to sat2.js); (7,5) m=5..37 and (7,6) m=6..31 all SAT dual-verified (m=30 additionally third-system verified; m=31 additionally surgery-constructed solver-free), free-column extended, or surgery-extended (m=35..37 by complete two-edit surgery enumeration of the m=34 witness, fresh pure-TS re-verified, seven-row-q5-m37-surgery-20261115; m=34 by 2-stone relocation surgery of the m=33 witness, TS-exhaustive verified only, js/py cross-check pending, seven-row-q5-witness-surgery-20261115) (m=32/33 via rowY=0 and m=27/28 via rowY=3 fixed-row splits; m=29 free-column extension of the m=28 witness; m=30 by class {3} class-split SAT triple-verified, seven-row-q6-m30-class-split-20261115; m=31 by complete two-edit surgery of the m=30 witness, triple-verified, seven-row-q6-m31-frontier-20261115; seven-row-q5-q6-frontier-row-split-20261115 and seven-row-q5-q8-sat-frontier-20261115); widths stated per family only; up to census completeness and solver/arithmetic correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction, all records jsVerify/pyVerify true) + third independent verification system (pure TS/BigInt, no repo code: verify_independent.ts of seven-row-q7-witness-search-20261114 — frontier witnesses (7,6) m=26, (7,5) m=31, (7,4) m=21 all PASS safe+maximal+row-deficient, record in seven-row-q7-witness-search-20261114/output/ts-verify-cross-family.json — triple-verified) + deterministic CNF regeneration from the calibrated sat2.js + cross-environment-reset bit-exact reproduction of the frontier records ((7,5) m=23..26 and (7,4) m=15 re-run after an environment reset with identical conflicts 1,200/2,029/7,730/3,257 and 0) + constructive extension band m=22..35 (seven-row-q4-extension-band-20261114): blocking-coverage lemma gives a free empty-column extension of the triple-verified m=21 witness to m=22; deterministic greedy adds + hill-climb (extend_band.ts, exact TS/BigInt, no SAT) produce 20-stone configs CA (maxX=22, coverage W=31, witnesses m=23..31) and CB (maxX=26, W=35, witnesses m=27..35, used for 32..35); all widths 22..35 verified safe+maximal+row-deficient by exact rational arithmetic (uncovered 0, negative control detected); M_{7,4} >= 36 (M in [36, 1929]); jsVerify/pyVerify re-verification of the extension-band witnesses: m=22..27 SAT re-confirmed and dual-verified by seven-row-q4-q6-witness-frontier-20261115 (kissat 0 conflicts, rows matching the constructive configs; four-way verified: kissat SAT + jsVerify + pyVerify + tsVerify), m=28..35 SAT re-confirmed and dual-verified by seven-row-q4-extension-band-sat3-20261115 (sat3.js streaming census, DIMACS byte-identical to sat2.js: 9 controls cmp MATCH, (7,5) m=23 kissat calibration 1,200 conflicts bit-exact, m=22..27 witness reproduction 6/6 stones identical; kissat 36-537 conflicts at m=28..35, all 200s cap; independent 20-stone witnesses with row multiset {3,3,3,3,3,3,2} matching the constructive configs; m=35 lex=H,V,HV cross-encoding SAT 314 conflicts) - the whole band m=4..35 is now four-way verified (kissat SAT + jsVerify + pyVerify + tsVerify), and the constructive files themselves are js+py re-verified 14/14 (seven-row-q5-q6-frontier-row-split-20261115). (7,5) m=32 and (7,6) m=27 resolved by rowY fixed-row splits (seven-row-q5-q6-frontier-row-split-20261115, rowsplit.sh, sat2.js --rowY=Y, kissat 4.0.4 sha256 21da5d98..., post-reset calibration (7,5) m=31 def-mode 31,000 conflicts bit-exact): (7,5) m=32 rowY=0 SAT 129,923 conflicts, 27-stone witness [3,4,4,4,4,4,4]; (7,6) m=27 rowY=3 SAT 230,973 conflicts, 34-stone witness [5,5,5,4,5,5,5]; both js+py dual-verified; M_{7,5} >= 33 (M in [33, 1142]), M_{7,6} >= 28 (M in [28, 862]). seven-row-q5-q8-sat-frontier-20261115 (sat3 streaming census + kissat 4.0.4, sat3/sat2 rowfixed q5 CNF byte-identity calibration 2/2, 900s background caps): (7,6) m=28 rowY=3 SAT 442,479 conflicts, 34-stone witness [5,5,5,4,5,5,5], plus m=29 free-column extension of the same 34 stones, both js+py dual-verified (M_{7,6} >= 30, M in [30, 862]); (7,5) m=33 rowY=0 SAT at 900s cap 655,159 conflicts, 27-stone witness [3,4,4,4,4,4,4], js+py dual-verified (M_{7,5} >= 34, M in [34, 1142]); m=34 free-column extension fails (cell (33,0)); (7,6) m=30 all-4-class cap negatives incl. rowY=3 900s INDET 1,569,306; (7,7) m=27 and (7,8) m=25 all-4-mirror-class 250s INDET sweeps. seven-row-q5-witness-surgery-20261115: (7,5) m=34 by 2-stone relocation surgery of the triple-verified m=33 witness ((25,5)->(8,5),(20,4)->(2,4); second witness with (23,5) instead of (8,5)); 27 stones rows [3,4,4,4,4,4,4]; TS-exhaustive verified (C(27,5)=80,730 subset-enumeration safety + per-cell 4-stone-curve maximality over all 211 empty cells, pure integer arithmetic, no repo code/census/SAT); js/py cross-check pending; M_{7,5} >= 35 (M in [35,1142]); 7x35 profile of the new witness: only cell (34,0) uncovered. See report.md. Latest q4 result: m=57..59 witnesses from seven-row-q4-width59-two-swap-20261115; M_{7,4}>=60 (M in [60,1929]); the width-60 searches are local 2-for-2 neighborhoods only. Latest surgery results: (7,5) m=37 witness winC (27 stones rows [3,4,4,4,4,4,4]) found as the unique case-b witness of the complete two-edit surgery enumeration of the m=34 witness targeting T=(34,0) on the 7x35 board (2-stone T-curves 333, sp-pairs 49, candidates 17,199; T-blocking curve the integer line x+2y-34=0); fresh independent pure-TS machine re-verification (no repo code/census/SAT): safe (max curve 4), all empty cells of 7x33..7x37 blocked by 61 four-stone curves, 7x38 fails only at (37,0); M_{7,5} >= 38 (M in [38,1142]); light cases A 1,053 / F 13,689 / b 17,199 / b2a1 36,432 freshly re-enumerated (complete) with the same unique witness; heavy cases E 76,167 and case-a 671,398+623,644 remain session records (0 witnesses, not re-enumerated). (7,6) m=30: two-edit surgery of the m=29 seed (T=(29,3)); session-enumerated cases T-occupancy 98,175 / one-swap 884 / two-remove-one-add 14,586 / case-b 561, total 114,206 candidates, 0 witnesses (session record; local negative); seed profile and T-curve census freshly re-verified and all four case counts re-derived by an independent pure-TS machine; the m=29 seed local surgery is now complete for at most two removals/additions and final size <=34: six disjoint classes, 1,781,021 unique candidates, 126,730 safe, 0 safe-maximal; exact Fraction Python audit plus independent integer-coefficient C++ crosscheck of gap-A/B (1,667,250 candidates); local negative only, no 7x30 global absence claim; M_{7,6} stays in [30,862], frontier 7x30 (seven-row-q6-m30-surgery-completion-20261115). Third system (pure TS, no-bash lane, session record in research/log/2026-11-15-seven-row-q5-witness-surgery.md): complete re-enumeration of the same (<=2,<=2) surgery space with a corrected machine agreeing on every per-case candidate and safe count (case-b 561/25 decomposing exactly into the 435/20 gap-A overlap plus the 126/5 independent slot; convention-inclusive totals 1,781,456 candidates / 126,750 safe) and 0 safe-maximal, brute cross-checked by direct final-config construction - the (7,6) m=30 (<=2,<=2) local negative is confirmed by three independent implementations (Python Fraction twice, integer-coefficient C++, pure TS). Latest surgery negative: (7,5) m=38 two-edit surgery of winC (T'=(37,0), q=5) - complete six-case final-state enumeration (c1a 378 / c1b 10,200 / c2c 40,392 / c2d 22,500 direct; c2a 83,538-eq and c2b 1,914,336-eq via exact U-set pruning: 312 pairs + 8,160 combos skipped by empty intersection, 378 + 11,219 candidates actually checked, all rejected at safety; 20 ground-truth audit units fully re-enumerated 0 maximal; m35 case-b replica control bit-exact rediscovering winC), 0 witnesses (local negative, not absence); M_{7,5} stays in [38,1142], frontier 7x38 (seven-row-q5-m38-surgery-negative-20261115). Latest: (7,6) m=30 witness by class-split (seven-row-q6-m30-class-split-20261115): class {3} sat3.js kissat 4.0.4 SAT 2,670,296 conflicts/497.0s (cap 600), 34-stone single-deficiency witness rows [5,5,5,4,5,5,5] row 3 cols [12,23,27,29], triple-verified (sat.js verifyConfig census + verify_witness.py Python Fraction + verify_witness_det.js pure-integer 4x4-determinant third system with built-in self-tests), negative control PASS (perturbation -> not-maximal in both independent verifiers); positive control (7,29,6) class {3} SAT 3,074,703 conflicts decoding a second distinct m=29 witness row 3 cols [4,12,26,28] dual-verified; M_{7,6} >= 31 (M in [31,862]); the m=30 rowY=0/1/2 250s and rowY=3 280/900s INDET negatives are reclassified as pre-witness cuts, not absence; witness band m=6..30, frontier 7x31. Latest: (7,6) m=31 witness by complete two-edit surgery of the m=30 witness on the 7x31 board (seven-row-q6-m31-frontier-20261115): unique 2-stone relocation R={(19,2),(25,4)}->A={(27,2),(29,4)} among 2,140,633 unique final-state candidates (complete final-state case split, removals <=2, additions <=2, final size <=34), exactly one safe-maximal in the <=2-edit neighborhood vs 0 at m=29->30; 34 stones rows [5,5,5,4,5,5,5]; triple-verified (verify_witness.py Python Fraction + verify_witness_det.js pure-integer 4x4-determinant + probe_free_column.py third Fraction system, all with self-tests), negative control PASS; solver-free construction, second solver-free witness beyond the SAT frontier after the (6,4) m=46 column-append; free-column extension of the m=31 witness fails at cell (31,3) one-stone-short; M_{7,6} >= 32 (M in [32,862]); witness band m=6..31, frontier 7x32."
---

# 7xm q=4,5,6 行欠損witness帯 — q=4 は m=4..56、M_{7,4} ≥ 57（q=5/6 は従来どおり）

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
3. **(7,4)**: **m=4..56 の全幅で存在**（m=36..41 はSAT、m=42..56 は本項目末尾の seeded SA + 空列延伸）。
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

## 追記 (2026-11-15 m=41 SAT・下界42・ソルバRAM壁)

`seven-row-q4-band-41-20261115`:

1. **m=41 SAT**（281 conflicts・39.0s・8,704,218 clauses・20石
   rows [3,3,3,3,3,3,2]・2系統検証 PASS）→ **M_{7,4} ∈ [42, 1929]**・前線 7×42。
2. sat3 の ≥q円のみ dedup 登録の修正（出力不変・byte-identity 再検証済み）で
   m=50 生成が可能になった（446,731 curves・15.5M clauses・11.6s・CNF 305MB）。
   一方 **kissat は ~9M clauses で本コンテナRAMにより OOM kill**（m=42・m=50・
   いずれも正直な負記録・不在主張ではない）。以降は大メモリ環境・節削減符号化・
   または構造論証が必要。


## 追記 (2026-11-15 m=42..56 seeded SA + 空列延伸 — 下界57)

seven-row-q4-band-42-56-20261115 により、**m=42..56 の全15幅で20石の行欠損極大安全配置**を得た。q=4・7行盤の満容量は21石なので、各配置は一行2石・残り六行3石である。

- 基礎配置を探索した幅: m=42,44,45,47,50,53（既存7×41 witnessを種にした決定的seeded SA）。
- 空列延伸: 42→43、45→46、47→49、50→52、53→56。各追加列の7セルは、既存の3石直線または3石円で全て遮断される。
- 独立検証: Python任意精度整数で15/15幅を再検査。最大直線点数・最大円点数はいずれも3、全空きセルの未遮断数0、石数20。安全性・極大性・行欠損すべてPASS。
- よって **M_{7,4} ≥ 57**、既存上界1929と合わせて M_{7,4}∈[57,1929]。これは有限witnessによる下界であり、閾値の確定ではない。
- m=57 は別seedで30秒・20秒のSAを試し、最良21石にとどまった。これは未発見記録であり、不存在証明ではない。前線は7×57。
- 追記 (2026-11-15): 6基礎配置を純TS完全整数演算の第2系統（repo コード不使用・
  census不使用・4点部分集合全列挙+全空セルの3石曲線被覆）で再検証し 6/6 PASS
  （`output/ts-verify-crosscheck.json`・各 chain max 43/44/46/49/52/56 で検証し
  単調性により全15幅を被覆・制御3件 PASS）。**m=42..56 の SA band は二系統検証済み**
（Python 任意精度整数 + TS）。

## 追記 (2026-11-15 (7,6) m=28 SAT + m=29 空列延伸・(7,5) m=33 900s SAT — M_{7,6} ≥ 30・M_{7,5} ≥ 34)

`seven-row-q5-q8-sat-frontier-20261115`（sat3 streaming census + kissat 4.0.4・
sat3/sat2 rowfixed q5 は CNF バイト一致較正 2/2（(7,23,5) def 1,200 conflicts
bit-exact・(7,32,5) rowY=0 129,923 conflicts bit-exact））:

1. **(7,6) m=28 SAT**（rowY=3 分割・442,479 conflicts・137.0s・cap 250）:
   **34石単一欠損 witness rows [5,5,5,4,5,5,5]**・js+py 2系統検証 PASS。
   **m=29 は同一34石の空列延伸**（追加列 x=28 の全7セルが既存の5石直線/円で
   遮断）で js+py 2系統検証 PASS。**witness帯は m=6..29、M_{7,6} ∈ [30, 862]**
   （上界 K0318 U=862 不変）。m=29→30 の空列延伸は cell (29,3) 未遮断で失敗。
2. **(7,6) m=30 honest negatives**: rowY=0/1/2 は cap 250s INDET
   （796,125 / 822,483 / 847,765 conflicts）・rowY=3 は 280s INDET 929,785 に続き
   **900s cap でも INDET（1,569,306 conflicts）**。全4クラス cap 内未解決・
   不在主張ではない。前線は 7×30。
3. **(7,5) m=33 SAT**（rowY=0 分割・**655,159 conflicts・835.7s・cap 900**）:
   **27石単一欠損 witness rows [3,4,4,4,4,4,4]**・js+py 2系統検証 PASS。
   全4ミラークラスの 250s INDET（399,206/399,144/344,970/345,432・クラス間抵抗
   ほぼ一様）は **cap 250s→900s の延長で SAT に解決** — クラス間抵抗がほぼ
   一様な前線でも cap 延長が有効になり得る観測（k×minpos 分解の前に試す価値）。
   **witness帯は m=5..33、M_{7,5} ∈ [34, 1142]**（上界 K0318 U=1142 不変）。
   m=34 への空列延伸は cell (33,0) 未遮断（not-maximal）で失敗。前線は 7×34。
4. **(7,7)/(7,8) 前線の全クラス走査（honest negatives）**: (7,7) 7×27 は
   rowY=0/1/2 が 250s INDET（2,186,370/2,243,432/2,095,752）・既存 rowY=3
   （262s・2,242,940）と合わせ全4クラス cap 内未解決。(7,8) 7×25 は
   rowY=0/1/2 が 250s INDET（3,613,768/3,717,333/3,678,867）・既存 rowY=3
   （250s・3,534,747）と合わせ全4クラス cap 内未解決。いずれも不在主張ではない。
5. **空列延伸の全系負記録（前線 witness からの直接延伸）**: (7,5) m=32→33・
   (7,6) m=27→28・(7,7) m=26→27・(7,8) m=24→25 は1幅も延伸せず
   （(7,6) m=28 SAT witness の m=29 が唯一の例外）。(7,4) SA base m=53→54..56 は
   PASS・57 で失敗（SA lane と一致）。
6. **第3系統検証（tsVerify・純TS完全整数演算・repo コード不使用・census不使用）**:
   `output/ts-verify-batch2-crosscheck.json` — 制御5件（5共線・5共円の検出、同一5点は
   q=6 では非違反、孤立3石の全空セル未遮断、4共線の非検出）全 PASS。
   (7,5) m=32/33・(7,6) m=27/28/29 の全5 witness が safe（q点部分集合の全列挙・
   完全整数演算）+ maximal（全空セルの q-1 石曲線被覆）+ 行欠損で PASS —
   **5 witness は triple-verified**。空列延伸の負記録（m=34 cell (33,0)・
   m=30 cell (29,3)）も第三系統で同一セルを再現。


## 追記 (2026-11-15 2石交換で7×59の行欠損極大配置)

seven-row-q4-width59-two-swap-20261115 により、幅53の20石証人から2石を除き2石を加える近傍を完全列挙した。

1. **7×57で2つの安全・行欠損極大配置を発見**。行容量3以下を保つ候補1,436,643件を全列挙し、安全候補60,921件のうち極大なものは2件。両方を独立Python検証器で再確認した。
2. そのうち一つは、(28,2),(36,4) を除き (56,2),(7,4) を加える。20石・行占有数 [3,3,3,3,3,3,2] のまま、空列延伸で **7×59** まで成立する。
3. 7×59証人は最大共線点数3・最大共円点数3。行0〜5は各3石の水平直線で塞がり、欠損行の57空セル x=0..58 は全て整数直線または円で遮断される。特に (57,6) は x-6y-21=0、(58,6) は 3(x²+y²)-307x+611y+3940=0 で遮断される。
4. (59,6) はこの配置では未遮断なので、同じ証人の単純な空列延伸は幅60で止まる。
5. したがって **M_{7,4}≥60**。既存上界1929と合わせて 60≤M_{7,4}≤1929。これは幅59の有限証人による下界であり、幅60の不存在や安定化長の確定ではない。
6. 幅60では、幅53の元証人と新しい幅59証人それぞれの2-for-2近傍を完全列挙したが、安全かつ行欠損極大な候補は0件。これは二つの局所近傍に限る結果で、7×60全体の不存在を意味しない。

## 追記 (2026-11-15 witness surgery による (7,5) m=34 — M_{7,5} ≥ 35)

`seven-row-q5-witness-surgery-20261115`（純TS・SAT不使用・bash環境不通時の代替レーン）:

1. **(7,5) m=34 witness を witness surgery で発見**: m=33 の triple-verified witness
   （27石 rows [3,4,4,4,4,4,4]）から 7×34 盤の唯一の未遮断セル (33,0) を遮断する
   2石移動を探索し、**2つの 27石単一欠損 witness** を得た:
   winA = base −(25,5) −(20,4) +(8,5) +(2,4)・
   winB = base −(25,5) −(20,4) +(23,5) +(2,4)。いずれも rows [3,4,4,4,4,4,4]。
2. **検証**: 純TS完全整数演算の独立実装（repo コード・census・SAT 不使用）で
   C(27,5)=80,730 部分集合全列挙の安全性と全211空セルの q−1=4 石曲線被覆
   （極大性）を確認し、winA/winB とも PASS。**js/py 交叉検証は pending**
   （bash 不通のため・正直な検証状態）。
3. **M_{7,5} ∈ [35, 1142]**（上界 K0318 U=1142 不変）。7×35 の不在主張ではない。
   新 witness の 7×35 profile は cell (34,0) のみ未遮断で、surgery 反復の出発点。
4. 手法メモ: depth-1 列挙は完全（T 未遮断 ⟹ T を通る曲線はすべて ≤3石 ⟹
   遮断曲線は「ちょうど3石曲線 + 移動石」に限る・939候補・106安全）。
   depth-2 は「どちらかの move が単独で T を遮断する」場合を網羅
   （必要条件フィルタで5,673組み評価・両新石が同一2石 T-曲線に乗るケースは
   未探索・不在主張なし）。増分 U 計算は高速化専用で、採用 witness は
   総当たり検験のみに依存。


## 追記 (2026-11-15 2編集surgery完全列挙による (7,5) m=35..37 witness — M_{7,5} ≥ 38)

seven-row-q5-m37-surgery-20261115（純TS・SAT不使用）:

1. (7,5) m=35..37 の単一欠損witnessを2編集surgeryの完全場合分けで発見。
   m=34 witness winA（7×35 で唯一の未遮断セル T=(34,0)）を種に、T を遮断する
   2編集の最終状態を場合分け: T-占有 / case-a（3石T-曲線+新石1つ）/
   case-b（2石T-曲線+両新石）/ b2a1（3石T-曲線+両新石+曲線上の除去1つ）。
   case-b（333曲線・49 spペア・17,199候補）の安全かつ極大な witness は
   winC = winA −(8,5) −(16,6) +(24,5) +(22,6)・27石 rows [3,4,4,4,4,4,4] のみ。
   T 遮断曲線は整数直線 x+2y−34=0。
2. 新規独立検証（純TS・完全整数演算・repoコード/census/SAT不使用）: winC は安全
   （最大曲線石数4）・7×33..7×37 の全空セル遮断（61本の4石曲線）・7×38 で (37,0) のみ
   未遮断。種 profile（base33・winA）再検証・制御4件 PASS。
   よって witness 帯は m=5..37・M_{7,5} ∈ [38, 1142]（上界不変）・前線 7×38。
3. 軽量ケースの新規再列挙（完全）: A 1,053（safe 173・0）・F 13,689（3,723・0）・
   b 17,199（594・winC を再発見）・b2a1 36,432（3,247・0）— セッション記録と完全一致。
   重い case E（76,167・0）と case-a（safe 671,398+unsafe中間 623,644・0・交叉検査300件
   一致）はセッション記録として保持（未再列挙）。下界 M_{7,5} ≥ 38 自体は winC の
   検証のみに依存し確定。

## 追記 (2026-11-15 (7,6) m=30 2編集surgery負記録と完全性ギャップ)

seven-row-q6-m30-surgery-negative-20261115（純TS・局所負記録・不在主張ではない）:

1. (7,6) m=29 seed（s7x29q6.witness.json・34石）の 7×30 における唯一の未遮断セル
   T=(29,3) を遮断する2編集surgeryのうち、セッションが列挙した4ケース:
   T-占有 98,175 / 1スワップ 884 / 2除去1追加 14,586 / case-b 561・計 114,206候補で
   0 witness（セッション記録）。
2. seed の新規独立検証（純TS）: 安全（最大曲線5）・7×29 極大・7×30 で (29,3) のみ
   未遮断・7×31 で (29,3),(30,3)。T センサス: 4石T-曲線は直線 y=3 のみ（空セル26）・
   3石T-曲線8本・2石T-曲線531本・T を含まない k3 spペアは ((1,3),(5,5)) の1組。
   全ケース数は独立再導出と一致（98,175=175×561・884=26×34・14,586=26×561・561=1×561）。
3. 完全性ギャップの新規特定: (2,2) で T ∉ 追加石のとき、T を通る4石T-曲線
   （直線 y=3）に新石1つを置くケース（25×150×C(30,2)=1,631,250候補）と同直線に
   両新石+線上の除去1つ（C(25,2)×4×30=36,000候補）がセッション列挙に含まれて
   いない（(7,5) の case-a に対応）。合計 1,667,250 候補の走査が最優先課題。
   両新石+除去0（4+2=6=q で安全違反）・新石1つ+線上除去（4<5）・k3+新石1つ（4<5）は
   構造的に排除済み。
4. M_{7,6} ∈ [30, 862] 不変・前線 7×30 のまま。SAT 全4クラス INDET
   （rowY=3 900s・1,569,306）と surgery 既走査分 0 件はいずれも局所的負記録。


## 追記 (2026-11-15 (7,5) 7×38 two-edit surgery 完全負記録)

seven-row-q5-m38-surgery-negative-20261115（純TS・局所負記録・不在主張ではない）:

1. m=37 witness winC（7×38 で唯一の未遮断セル T'=(37,0)）を種にした2編集surgeryの
   完全最終状態場合分け6ケース（T'占有 c1a / 3石T'-曲線+新石1 c1b・c2b /
   3石T'-曲線+両新石+曲線上除去1 c2c / 2石T'-曲線+両新石 c2d / T'+z2 c2a）で
   **0 witness**。c1a 378・c1b 10,200・c2c 40,392・c2d 22,500 は直接全列挙、
   c2a（83,538相当）と c2b（1,914,336相当）は厳密 U 集合剪定で実チェック
   378+11,219候補（312ペア+8,160コンボは交差空で全棄却・残りは safeCheck 段階で全棄却）。
2. T' センサス: 4石T'-曲線0本・3石T'-曲線3本（空セルを持つのは直線 y=0 のみ・
   34個・基底石 (8,0),(18,0),(30,0)・残る円2本は空セル0）・2石T'-曲線342本・
   spペア75組。q=5 では基底に4石T'-曲線が存在しないため (7,6) 型の線ベースcaseも
   c1b/c2b に自然に含まれ、6ケースで (2,2) 以下の編集空間を尽くす。
3. 機械の健全性検証: m=35 case-b レプリカが spペア49・17,199候補・safe 594・
   maximal 1・witness winC を完全再現（end-to-end陽性対照）・U(Rm) 導出が15ペアで
   直接全列挙と完全一致・剪定スキップ単位20件（c2b 14コンボはz2全204候補・
   c2a 6ペアはz2全238候補を無剪定で再列挙）がすべて maximal 0。
4. M_{7,5} ∈ [38, 1142] 不変・前線 7×38 のまま。次の枝: (7,6) ギャップ
   1,667,250 候補への同一手法の適用・3編集surgery・sat3 による 7×38 直接評価。


## 追記 (2026-11-15 (7,6) m=30 seed surgery の完全列挙)

seven-row-q6-m30-surgery-completion-20261115 により、m=29 の34石seedからの局所手術を完了した。

1. seedは7×29で安全・極大、7×30では T=(29,3) のみ未遮断。seed三つ組から定まる5,273曲線を有理数外心で独立再構成し、最大曲線点数5・7×29の未遮断0・7×30の未遮断1を確認。
2. Tを通るseed曲線の点数分布は2点531本・3点8本・4点1本。4点曲線は直線 y=3 のみ。3点T曲線上の空セル対は4組で、Tを含まない唯一の対は ((1,3),(5,5))。
3. 除去2個以下・追加2個以下・最終34石以下でTを占有または遮断する全候補を6互いに素な場合に分類。T占有98,175・1 swap 884・2除去1追加14,586・3点T曲線の追加枠126・4点線gap-A 1,631,250・gap-B 36,000。case-b 561のうち435はgap-Aと重複するため除き、**重複なし合計1,781,021候補**。
4. **安全126,730・安全かつ極大0**。Python Fractionの全6ケース検査を2回実行し、同じ出力を再現。C++の正規化整数係数実装で、従来未走査だったgap-A/gap-B 1,667,250候補を独立交差検証し、候補数・安全数・極大数が一致。
5. これは当該seedの編集数制限付き局所近傍に関する有限完全負記録であり、7×30全体の不在証明ではない。SAT全4欠損行クラスは依然INDET、M_{7,6}∈[30,862] は不変。次の候補は3編集手術・別seed・欠損行クラス分割SAT。
6. 第3系統の合意（純TS・bash不通レーンの独立再列挙・セッション記録）: 曲線正規化キー
   欠落の機械バグを対照実験で検出・修正した純TS機械による完全再列挙で、全ケースの
   候補数・安全数が完全一致（case-b 561/25 は gap-A 重複枠 435/20 と独立枠 126/5 に
   一致分解・重複を除かない合計 1,781,456候補/126,750安全 = 一意合計
   1,781,021+435/126,730+20）し、極大0も合意（brute交差検査・独立の S' 直接構成で
   不一致0）。よって「(≤2,≤2) 改装で witness なし」は3つの独立実装（Python
   Fraction・C++・純TS）で合意した有限完全負記録となった（セッション詳細は
   research/log/2026-11-15-seven-row-q5-witness-surgery.md 第4セッション）。


## 追記 (2026-11-15 class-split による (7,6) m=30 witness — M_{7,6} ≥ 31)

`seven-row-q6-m30-class-split-20261115`（sat3.js class-split・行ミラー V 正準欠損クラス 71 個・
kissat 4.0.4・cap 600s・resumable）:

1. **(7,6) m=30 を class {3}（row 3 のみ欠損）の SAT で解決**: **SAT 2,670,296 conflicts / 497.0s**。
   **34石単一欠損 witness rows [5,5,5,4,5,5,5]・row 3 の石は列 [12,23,27,29]**。
   3系統検証 PASS: sat.js verifyConfig（census）・verify_witness.py（Python Fraction・
   census 不使用）・verify_witness_det.js（純整数 4×4 行列式・自己テスト 3 件組み込み・
   repo コード不使用）。**負対照 PASS**: 石 (12,3) 除去の摂動配置を py/det 両系統が
   not-maximal と検出。
2. **対照 PASS**: (7,29,6) class {3} SAT 3,074,703 conflicts — row 3 石 [4,12,26,28] の
   **m=29 第二witness**（既刊の空列延伸 witness [3,8,11,27] と別配置）を復号・
   二系統検証 PASS。class-split 符号化・decode 鎖の (7,6) 家族での実地検証。
   同幅 rowfixed rowY=3 SAT 442,479 conflicts に対し class {3} instance は約 7 倍深い
   （6 行を exactly 5 に固定すると探索がむしろ難化する観測）。
3. **witness 帯は m=6..30 に延伸し M_{7,6} ∈ [31, 862]**（上界 K0318 U=862 不変）。
   前線は **7×31**。既存の 7×30 rowY=0/1/2 250s INDET（796,125/822,483/847,765）・
   rowY=3 280s/900s INDET（929,785/1,569,306）は **witness 手前の打ち切り
   （pre-witness cut）** だったことが確定 — INDET は cap 到達であって不在主張では
   ないという解釈境界の実例。2石 surgery 完全列挙負（1,781,021 候補 0 safe-maximal）
   は「m=29 seed の近傍に限れば」の局所負であったことが裏付けられた
   （新 witness は seed から ≥3 石移動の位置にある）。
4. **不在主張なし**: c3 の SAT により残る 70 クラスは不実施。driver v2 は SAT を
   検出して掃引を即時打ち切った（v1 の abort 判定は対照 record にも反応する bug で
   m=30 レコードに限定して修正済み）。
5. toolchain 備考: sat3.js decode は >65k 変数モデルで `Math.max(...lits)` の spread が
   RangeError（m=30 は ~128k 変数）。モデル解析は独立 Python パーサで実施
   （sat3.js blob は不変・他レーンの較正に影響しない）。


## 追記 (2026-11-15 2編集surgery完全列挙による (7,6) m=31 witness — M_{7,6} ≥ 32)

`seven-row-q6-m31-frontier-20261115`（2編集 surgery・決定的完全列挙・repo コード不使用）:

1. **着手時点**: witness 帯 m=6..30・前線 7×31。m=30 witness（34石 rows [5,5,5,4,5,5,5]）の
   空列延伸 probe は 7×31 で唯一の未遮断セル T=(30,3)（one-stone-short）。さらに probe 初版の
   外心 uy 公式に転写 bug（a² 項が (cx−bx) のべき所で (cy−by)）があり m=30 極大性と矛盾する
   偽の未遮断 15 セルを報告したが、組み込み自己テストで検出・修正（m=30 極大性を再現し det
   検証器と一致）。**幾何ルーチンには回帰自己テスト必須**の再確認。
2. **2編集 surgery 完全列挙**（m=30 witness を種に T=(30,3) を占有または遮断）:
   最終状態場合分けは T 占有 / c4・t=0 の 1 追加 / c4・t=1 と c3 の 2 追加で完全
   （c5 の T 曲線は存在しない・除去は遮断曲線を作らない）。**2,140,633 一意候補**、
   **safe かつ maximal はちょうど 1 件**: R={(19,2),(25,4)} → A={(27,2),(29,4)}
   （34石・rows [5,5,5,4,5,5,5] のまま単一欠損）。m=29→30 では 0 件だったのと対照的で、
   ≤2 編集近傍における witness の疎分布の例。
3. T=(30,3) の曲線センサス: c4=2（直線 y=3 と円 {(22,2),(23,3),(25,4),(28,4)}）・c3=11。
   遮断曲線は (27,2),(29,4) を含む c3 円（3 seed 石 + 両追加石）経由。
4. **3系統検証 PASS**（すべて自己テスト組み込み）: verify_witness.py（Python Fraction）・
   verify_witness_det.js（純整数 4×4 行列式: maxLine 5 / maxCircle 5 / uncovered 0）・
   probe_free_column.py（第三 Fraction 実装: 7×31 unblocked 0）。**負対照 PASS**:
   (29,4) 除去の摂動配置を py・det 両系統が検出。
5. **solver-free 構成**: SAT を使わず SAT 前線の先の witness を構成した 2 例目
   （(6,4) m=46 空列追加に次ぐ）。class {3} (7,31,6) SAT は並走実行中で、結果の如何に
   よらず surgery 構成の正当性は独立。witness の空列延伸は 7×32 で (31,3) 未遮断
   （one-stone-short）。**witness 帯 m=6..31・M_{7,6} ∈ [32, 862]・前線 7×32**。
6. script 開発中の 2 bug（両方修正・README 備考に記録）: (1) 除去石セルの再遮断と移動
   re-add の扱いが非統一 → 曲線を「盤上全セル」表現で |C∩S'| = |st_on−R| + |A∩full| に統一。
   (2) 直線キーの gcd 正規化漏れで同一幾何直線が重複（census 表示のみ影響・候補数
   2,140,633 は修正前後で同一・列挙の完全性に無影響）。
