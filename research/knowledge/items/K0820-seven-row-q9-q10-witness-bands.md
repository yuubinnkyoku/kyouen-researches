---
id: K0820
title: "7xm q=9 / q=10 row-deficient witness bands — (7,9) witnesses 9..23 and witness-free 24..60 (M_{7,9} = 24 or >= 61), (7,10) witness-free band 19..40 confirmed by kissat and extended to 60 (M_{7,10} = 19 or >= 61)"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) + sequential-counter/maximality core used verbatim (sat.js/sat2.js); the def-mode single clause and lex-leader constraints are the source experiment's sat2.js additions"
- type: depends_on
  target: K0796
  note: "2x8 q=4 5-stone SAT control and 2x9 q=4 UNSAT control (fastsat conflicts bit-exact with the source experiment; kissat agrees) — consistent with M_{2,4}=9"
- type: depends_on
  target: K0318
  note: "upper bounds U_{7,9}=613 and U_{7,10}=587 by curve-packing substitution (w7_upper_bounds.json of the source experiment)"
artifacts:
- path: research/experiments/seven-row-q9-q10-bands-20261114/report.md
  role: proof
  note: "claims, method (def-mode completeness, lex soundness on the (7,10) band), verification protocol (controls, bit-exact fastsat calibration, dual witness verification, lex cross-encoding, determinism across env resets), results, scope and limits"
- path: research/experiments/seven-row-q9-q10-bands-20261114/output/q9-witness-search/records.jsonl
  role: data
  note: "50 records: SAT m=15..23 (witnesses dual-verified) + UNSAT m=24..60 (kissat def-no-lex, complete encoding; m=34..45 lean1.sh/sat2.js, m=46..60 lean2.sh/genfast.js) + def+lex cross-checks at m=24/33/52/60"
- path: research/experiments/seven-row-q9-q10-bands-20261114/output/q9-witness-search/s7x23q9_none.witness.json
  role: data
  note: "largest-width (7,9) witness (55 stones at 7x23, rows 8,8,8,7,8,8,8); all 9 witnesses s7x15..23q9_none.witness.json dual-verified (sat.js verifyConfig + Python Fraction)"
- path: research/experiments/seven-row-q9-q10-bands-20261114/output/q10-band/records.jsonl
  role: data
  note: "44 records m=19..60 all UNSAT: fastsat calibration (bit-exact with seven-row-inband results.jsonl for m=19..40) + kissat 4.0.4 for m=19..51 (band1.sh, both solvers); m=52..60 kissat-only lean extension (lean2.sh/genfast.js) with def+lex cross-checks at 52/60"
- path: research/experiments/seven-row-q9-q10-bands-20261114/output/q10-band/summary.json
  role: data
  note: "aggregate: all 44 UNSAT, per-width conflicts of both solvers (m=19..51) and lean extension rows (m=52..60)"
- path: research/experiments/seven-row-q9-q10-bands-20261114/scripts/genfast.js
  role: code
  note: "memory-bounded CNF generator (half-integer-center census, monkey-patches S.buildCensus and reuses sat2.js verbatim); byte-identical to sat2.js on 12 validation samples; required for 7xm at m>=52 where the all-triples census OOMs"
- path: research/experiments/seven-row-q9-q10-bands-20261114/output/controls/records.jsonl
  role: data
  note: "2x8/2x9 q=4 controls (fastsat 121/535 conflicts bit-exact; kissat SAT 37 / UNSAT 316)"
- path: research/experiments/seven-row-inband-families-20261114/output/results.jsonl
  role: data
  note: "source experiment (unintegrated): (7,9) witnesses m=9..14 and (7,10) witnesses m=10..18 (dual-verified there) + fastsat def+lex UNSAT band m=19..40 that this K confirms and extends"
- path: research/experiments/seven-row-inband-families-20261114/output/w7_upper_bounds.json
  role: data
  note: "K0318 curve-packing substitution upper bounds U_{7,9}=613, U_{7,10}=587 (7 controls passed)"
scope: "finite machine verification: kissat 4.0.4 (all instances) + fastsat calibration/cross-check (the (7,10) band); widths stated per family only; up to census completeness and solver correctness"
evidence: "complete-encoding UNSAT instances (def mode is exactly 'exists row-deficient maximal safe config' since safety caps every row at q-1) + constructive dual-verified witnesses + bit-exact instance-identity calibration + second-encoding (def+lex) cross-checks at (7,9) 24/33 + determinism across environment resets. See report.md."
---

# 7×m q=9 / q=10 行欠損witness帯 — (7,9) witness 9..23・不在帯 24..33、(7,10) 不在帯 19..40 をkissatで確認し 51 まで延長

## 主張

1. **(7,9)（7×m・q=9・q点共円/共線禁止）**: 行欠損の極大安全配置が
   **m=15..23 に存在する**（満容量56石に対し55石・m=15のみ54石・すべて2系統独立検証
   PASS）。`seven-row-inband-families-20261114` の m=9..14 witness と合わせて
   witness 幅集合は **{9..23}** を含む。
2. **(7,9)**: **m=24..60 の各行で行欠損極大配置は存在しない**（def単一節符号化・
   lexなし = 「ある行が≤7石の極大安全配置が存在」の完全符号化・kissat 4.0.4 が
   全幅 UNSAT・m=24/33/52/60 は def+lex=H,V,HV の別符号化でも UNSAT。
   m=34..45 は sat2.js (lean1.sh)、m=46..60 は genfast.js (lean2.sh・CNFは
   sat2.js と12サンプルでバイト一致) で生成）。よって witness-free 帯は
   **{24..60}** を含み **M_{7,9} = 24 または M_{7,9} ≥ 61**
   （M ∈ {24} ∪ [61, 613]・上界613はK0318代入）。
3. **(7,10)**: `seven-row-inband-families-20261114` の fastsat UNSAT 帯 m=19..40
   （def+lex=H,V,HV）を **kissat 4.0.4 で独立確認**した（再生成CNFの fastsat
   conflicts が全22幅で bit-exact 一致により同一インスタンス性を保証）上で、
   **帯を m=60 まで延長**した（41..51 は fastsat・kissat 両UNSAT、52..60 は
   kissat 単独 (lean2.sh/genfast.js)・52/60 は lex 別符号化でも UNSAT）。
   witness 幅集合 {10..18}（同実験・2系統検証済み）と合わせ
   **M_{7,10} = 19 または M_{7,10} ≥ 61**（M ∈ {19} ∪ [61, 587]・上界587はK0318代入）。
4. **genfast.js（censusメモリ壁の解消）**: sat2.js の全三つ組円censusは
   7×52 (n=364・C(n,3)≈800万) でコンテナメモリ上限を超え OOM (rc 137) する
   （7×51 は通過・CNF自体は8k vars/29k節と微小）。**q ≥ w+1 のもとで全 q点円の
   中心x座標が半整数になる**（各行∩円 ≤ 2点ゆえ同一行ペアが存在し、その垂直
   二等分線が中心を通る）ことを用いた半整数中心censusに差し替え、符号化論理は
   sat2.js を monkey-patch で完全再利用（エンコードdriftゼロ）。曲線挿入順序を
   buildCensus と厳密に一致させ（線は最小2点順・円は最小3点順・線が円の前）、
   **12サンプルで sat2.js とバイト一致検証**（deficient / cap+totalizer / rowfixed・
   lex有無・w=5,6,7）。7×52 生成は 2.7 秒。m ≥ 52 の7行レーン全般（(7,8)・
   (7,9)・(7,10)・将来の帯延長）の実装障壁を除去。

## 手法と検証

符号化は `seven-row-inband-families-20261114/scripts/sat2.js`（K0810 census +
sequential counter + 極大性）を verbatim 使用。def 単一節（∨¬rowGe[y]）は
「総石数 < w(q−1) ⟺ ある行 ≤ q−2」により行欠損存在の**完全**符号化であり、
節は H/V/HV 不変なので (7,10) 帯の lex-leader は健全（orbit-min が全制約を満たす）。
(7,9) witness 探索は lex なし（K0815 第4弾の教訓: lex は SAT 側の探索を悪化させる）。
制御: 2×8 q=4 SAT / 2×9 q=4 UNSAT（fastsat conflicts が元実験と bit-exact・kissat 同意）。
全 SAT witness は census 不使用 JS verifyConfig と Python Fraction 別実装の
2系統で safe+maximal+行欠損 PASS。較正: (7,10) m=19..40 の再生成CNFで fastsat
conflicts が元実験 results.jsonl と全幅 bit-exact 一致。
**制限（正直な負記録）**: (7,9) 帯 m=24 の fastsat は 60秒 cap で TIMEOUT
（210k conflicts）であり、(7,9) 帯は kissat 単独 + 2幅の別符号化交差確認による。
決定性: 全記録数値は実行環境リセット2回を挟んで bit-exact 再現。

## 範囲と限界

有限機械検証（census 完全性 — m≤45 は sat2.js、m≥46 は12サンプルでバイト一致
検証済みの genfast.js — とソルバ正確性まで）。数論的証明ではない。
M_{7,9}=24 の確定には m=61..612 の持続性（または K0342 型 tail 評価）が残り、
M_{7,10}=19 の確定には m=61..586 が残る。witness 探索前線は **7×61 (q=9)** と
**7×61 (q=10)** に移動。上界 613/587（K0318 代入）は不変。

## 関連する未統合の源実験

`seven-row-inband-families-20261114`（results.jsonl・witnesses.json・
w7_upper_bounds.json・classification_q10.json）は本項目の主要な入力であるが、
K項目化は本項目が初めて（(7,9) witness m=9..14・(7,10) witness m=10..18・
fastsat UNSAT 帯 m=19..40・U_{7,q}/U_{8,q} 表・10点円2族分類）。
同実験の (7,10) UNSAT 帯の根拠は本項目の kissat 交叉確認により
「単一カスタムCDCL」から「2ソルバ一致」に強化された。

## 追記 (2026-11-14 同日 第2ラウンド: 帯延長 24..60 / 19..60 と genfast.js)

当初の本項目（kissat交叉確認 + (7,9) witness 15..23 + 不在帯 24..33 / 19..51・
3コミット 55750abd→1a2b87db→20a85748）から同日内にさらに:
(a) **(7,9) 不在帯を 24..60 に延長**（m=34..45 lean1.sh・m=46..60 lean2.sh・
全幅 kissat UNSAT・52/60 は lex別符号化でも UNSAT）、
(b) **(7,10) 帯を 19..60 に延長**（52..60 kissat単独・52/60 lex別符号化でも UNSAT）。
よって **M_{7,9} ∈ {24} ∪ [61,613]**・**M_{7,10} ∈ {19} ∪ [61,587]**。
(c) **genfast.js 開発**: sat2.js の全三つ組censusが7×52でOOMする壁を、
q ≥ w+1 なら全 q点円の中心x座標が半整数（同一行ペアの垂直二等分線）なる
ことに基づく半整数中心censusで解消。sat2.js の符号化論理を monkey-patch で
完全再利用し、曲線順序を厳密再現（線:最小2点順、円:最小3点順、線が先）して
**12サンプルで sat2.js と CNFバイト一致**（cmp・deficient/cap+totalizer/rowfixed・
lex有無・w=5,6,7）。7×52 生成 2.7 秒・メモリ O(n²)。
限界: q < w+1 では半整数中心保証が崩れるため assert で拒否（sat2.js を使う）。
m=61..612 / 61..586 の持続性または K0342 型 tail 評価が exact M 決着の残課題。
