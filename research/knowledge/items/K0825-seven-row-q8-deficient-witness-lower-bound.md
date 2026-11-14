---
id: K0825
title: "7xm q=8 row-deficient witness band — witnesses 7x8..7x24 (M_{7,8} >= 25, upper 651 by K0318 substitution); first (7,8) family results"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census + sequential-counter/maximality core used verbatim (sat.js/sat2.js); def-mode single clause is the source experiment's sat2.js addition"
- type: depends_on
  target: K0796
  note: "2x8 q=4 SAT / 2x9 q=4 UNSAT def+lex controls (fastsat 121/535 conflicts bit-exact with the K0820 controls record; kissat agrees) — consistent with M_{2,4}=9"
- type: depends_on
  target: K0318
  note: "upper bound U_{7,8}=651 by curve-packing substitution (w7_upper_bounds.json of seven-row-inband-families-20261114)"
- type: depends_on
  target: K0820
  note: "genfast.js (memory-bounded CNF generator) reused; instance-identity calibration (7,10) m=46 def+lex regenerated, kissat 861 conflicts bit-exact with the q10-band record; genfast byte-identity to sat2.js re-validated for q=8 on 4 samples"
artifacts:
- path: research/experiments/seven-row-q8-witness-search-20261114/report.md
  role: proof
  note: "claims, method (def-mode completeness, genfast q=8 byte-identity, rowY split at the OR-instance wall), verification protocol (controls bit-exact, dual witness verification, instance-identity calibration, cross-reset determinism), results, honest negatives, scope and limits"
- path: research/experiments/seven-row-q8-witness-search-20261114/output/def-search/records.jsonl
  role: data
  note: "17 records: SAT m=8..23 (witnesses dual-verified) + m=24 INDET (def OR 3,829,302 conflicts and def+lex 3,710,480 conflicts at 240s caps — honest negatives)"
- path: research/experiments/seven-row-q8-witness-search-20261114/output/row-split/records.jsonl
  role: data
  note: "rowY=3 fixed-row split: m=24 SAT (641,005 conflicts, 48-stone witness rows 7,7,7,6,7,7,7 dual-verified) + m=25 INDET (3,534,747 conflicts at 250s, 3 other mirror row classes unswept)"
- path: research/experiments/seven-row-q8-witness-search-20261114/output/row-split/s7x24q8_rowY3.witness.json
  role: data
  note: "largest-width (7,8) witness (48 stones at 7x24, rows 7,7,7,6,7,7,7, found via the rowY=3 split); m=8..23 witnesses at output/def-search/s7xMq8_none.witness.json, all dual-verified (sat.js verifyConfig + Python Fraction)"
- path: research/experiments/seven-row-q8-witness-search-20261114/output/controls/records.jsonl
  role: data
  note: "2x8/2x9 q=4 def+lex controls (fastsat 121/535 bit-exact with K0820) + def-only variants (fastsat 81/2002, kissat 65/1268 agree) + (7,10) m=46 instance-identity calibration (kissat 861 conflicts bit-exact)"
- path: research/experiments/seven-row-q8-witness-search-20261114/output/controls/genfast_q8_byteidentity.json
  role: data
  note: "genfast.js vs sat2.js CNF md5-identical on 4 samples at q=8 (m=9,12, lex on/off)"
scope: "finite machine verification: kissat 4.0.4 (all instances) + fastsat control agreement; widths stated per family only; up to census completeness and solver correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction) + bit-exact controls and instance-identity calibration + cross-environment-reset determinism (m=8..22 conflicts reproduced bit-exact). See report.md."
---

# 7×m q=8 行欠損witness帯 — witness 7×8..7×24（M_{7,8} ≥ 25・上界651）

## 主張

1. **(7,8)（7×m・q=8・q点共円/共線禁止）**: 行欠損の極大安全配置が
   **m=8..24 の全幅で存在する**（本ファミリー初の結果）。
   - m=8, 9 は 38石（deficiency 11・行パターン 2,5,4,6,7,7,7 / 2,4,4,7,7,7,7）、
     m=10..12 は 45, 46, 47石、m=13..24 は単一欠損の **48石**
     （満容量 49 = 7·7・ある行が6石・他の行は7石）。
   - すべて census 不使用 JS verifyConfig と Python Fraction 独立実装の
     2系統検証で safe + maximal + 行欠損 PASS。
2. よって witness 幅集合は {8..24} を含み **M_{7,8} ≥ 25**
   （M ∈ [25, 651]・上界 651 は K0318 曲線パッキング代入・U_{7,8}=651）。
3. **m=24 の解法（方法論的成果）**: def 単一節（OR）実例は 240s cap で
   INDET（3,829,302 conflicts・def+lex=H,V,HV でも 3,710,480）だったが、
   欠損行を固定する rowY=3 分解（sat2.js --rowY）で kissat 4.0.4 が
   **641,005 conflicts（約41秒）で SAT**。以後の帯評価は行固定分解
   （V 対称で 4 クラス）が有効。
4. **正直な負記録**: m=25 は rowY=3 分解でも 250s cap で INDET
   （3,534,747 conflicts）。他の 3 行クラスは未走査。不在の主張ではない。
   witness 探索の前線は **7×25**。

## 手法と検証

符号化は K0810 の sat2.js を verbatim（def 単一節 ∨¬rowGe[y] は
「総石数 < 49 ⟺ ある行 ≤ 6」の完全符号化）。q=8 = w+1 のため
K0820 の genfast.js（半整数中心census）が適用可能で、q=8 で
sat2.js と CNF バイト一致を4サンプル（m=9,12・lex有無）で再検証。
制御: 2×8/2×9 q=4 def+lex が K0820 controls と fastsat conflicts
bit-exact（121 SAT / 535 UNSAT）・def 単独でも両ソルバ判定一致
（fastsat 81/2002・kissat 65/1268）。
インスタンス同一性較正: (7,10) m=46 def+lex 再生成CNFの kissat
conflicts 861 が K0820 q10-band records と bit-exact。
決定性: 実行環境リセット1回を挟み m=8..22 の全 conflicts が
bit-exact 再現（191, 824, 140, 292, 601, 4717, 49349, 49711, 681530, …）。

## 範囲と限界

有限機機検証（census 完全性とソルバ正確性まで）。数論的証明ではない。
M_{7,8} の確定には 7×25 以降の評価（前線 7×25・def OR 実例の難化が
顕著: m=23 SAT 1.3M → m=24 OR 3.8M INDET）と上界 651 の改善
（K0342 型 tail 評価）が残る。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
