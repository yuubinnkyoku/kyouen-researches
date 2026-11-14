---
id: K0826
title: "7xm q=7 row-deficient witness band — witnesses 7x7..7x25 (M_{7,7} >= 26, upper 708 by K0318 substitution); first (7,7) family results (q=w diagonal)"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census + sequential-counter/maximality core used verbatim (sat.js/sat2.js); def-mode single clause is the complete encoding of 'total < 42 iff some row <= 5'"
- type: depends_on
  target: K0318
  note: "upper bound U_{7,7}=708 by curve-packing substitution (w7_upper_bounds.json of seven-row-inband-families-20261114)"
- type: depends_on
  target: K0825
  note: "same machinery and runner as the (7,8) search; rowY fixed-row split re-validated at q=7 (cracked the m=25 OR-instance wall); sat2.js is the only generator here since genfast.js requires q >= w+1"
artifacts:
- path: research/experiments/seven-row-q7-witness-search-20261114/report.md
  role: proof
  note: "claims, method (sat2.js all-triples census at q=w, rowY split), verification protocol (dual witness verification, m=24 bit-exact determinism re-run), results table, honest negatives, scope and limits"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/def-search/records.jsonl
  role: data
  note: "19 records: SAT m=7..25 witnesses dual-verified (m=7..14 deep deficiency 30..41 stones, m=15..24 single-deficiency 41 stones) + m=25 OR-instance INDET (2,478,476 conflicts at 240s cap — honest negative)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/row-split/records.jsonl
  role: data
  note: "m=25 rowY=0..3 fixed-row split: rowY=3 (central row) SAT at 756,785 conflicts (41-stone witness rows 6,6,6,5,6,6,6 dual-verified); rowY=0/1/2 INDET at 200s caps (961,944 / 970,708 / 1,130,645 conflicts — not absence claims)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/row-split/s7x25q7_rowY3.witness.json
  role: data
  note: "largest-width (7,7) witness (41 stones at 7x25, rows 6,6,6,5,6,6,6, found via the rowY=3 split); m=7..24 witnesses at output/def-search/s7xMq7_none.witness.json, all dual-verified (sat.js verifyConfig + Python Fraction)"
scope: "finite machine verification: kissat 4.0.4 (all instances); widths stated per family only; up to census completeness and solver correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction) + m=24 bit-exact determinism re-run (2,105,329 conflicts reproduced). See report.md."
---

# 7×m q=7 行欠損witness帯 — witness 7×7..7×25（M_{7,7} ≥ 26・上界708）・q=w 対角ファミリー初の結果

## 主張

1. **(7,7)（7×m・q=7・q点共円/共線禁止）**: 行欠損の極大安全配置が
   **m=7..25 の全幅で存在する**（本ファミリー初の結果。q=w の対角ケース）。
   - m=7..14 は深欠損（30, 32, 34, 37, 38, 39, 40, 41 石・deficiency 12..1。
     m=10..14 は上位6行が6石・最下段 1..5 石の構造系列）。
   - m=15..25 は単一欠損の **41石**（ある行のみ5石・他の6行は6石。
     満容量 42 = 7·6）。
   - すべて census 不使用 JS verifyConfig と Python Fraction 独立実装の
     2系統検証で safe + maximal + 行欠損 PASS。
2. よって witness 幅集合は {7..25} を含み **M_{7,7} ≥ 26**
   （M ∈ [26, 708]・上界 708 は K0318 曲線パッキング代入・U_{7,7}=708）。
3. **m=25 の解法**: def OR 実例は 240s cap で INDET（2,478,476 conflicts）だったが、
   欠損行固定の **rowY 分解（V 対称で 4 クラス）の rowY=3（中央行）で SAT**
   （756,785 conflicts）。rowY=0/1/2 は 200s cap で INDET（不在の主張ではない）。
   K0825 の (7,8) m=24 と同様、**行固定分解が OR 壁を突破**（q=7 でも再確認）。
4. **正直な負記録**: m=25 rowY=0/1/2 の INDET、m=26 以降は未走査。
   witness 探索の前線は **7×26**。
5. **観測（全称主張ではない）**: 7行族の単一欠損 witness 帯は
   (7,8) m=13..24 と (7,7) m=15..25 で同型（欠損行の位置は幅ごとに変わり、
   (7,7) m=25 では中央行）。def OR 実例の難化も同様
   （(7,7): m=23 SAT 119,071 → m=24 SAT 2,105,329 → m=25 OR INDET 2,478,476）。

## 手法と検証

符号化は K0810 の sat2.js を verbatim（genfast.js は q ≥ w+1 専用のため
不適用・全三つ組censusを n=7m ≤ 175 で使用）。def 単一節 ∨¬rowGe[y] は
「総石数 < 42 ⟺ ある行 ≤ 5」の完全符号化。制御: m=24 def OR 再実行で
conflicts 2,105,329 が bit-exact 再現（決定性）。sat2.js の符号化自体は
前回実験で fastsat/kissat 交差較正・cross-reset 決定性検証済みの同一コード。

## 範囲と限界

有限機械検証（census 完全性とソルバ正確性まで）。数論的証明ではない。
M_{7,7} の確定には 7×26..7×28（census 実用範囲）以降の評価と
上界 708 の改善（K0342 型 tail 評価）が残る。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
