---
id: K0843
title: "8xm q=11 / q=12 row-deficient band closure — (8,11) witness band 11..20 + witness-free band 21..907 fully swept (M_{8,11} = 21 exact, first complete determination at w=8); (8,12) witness-free 17..230 swept (M_{8,12} in {17} union [231,883], sweep in flight)"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) + sequential-counter/maximality core reused verbatim via the sat2.js monkey-patch; def-mode single clause and lex as in K0820"
- type: depends_on
  target: K0318
  note: "upper bounds U_{8,11}=908 and U_{8,12}=883 by curve-packing substitution (w7_upper_bounds.json) - proved; excludes witnesses for all m >= 908 / 883"
- type: depends_on
  target: K0830
  note: "strip-classification machine ported to w=8 (eight-row-strip-classification-20261115): Theorem A + Corollary 4 - every in-board circle with >= 11 points is a placement member of the twelve-point F1 family for all m <= 984; band-wide soundness basis of the genfam12 family census"
artifacts:
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/README.md
  role: proof
  note: "claims, family-census soundness (dropping curves only removes constraints), CNF byte-identity calibration 21/21, dual witness verification protocol, cross-reset determinism, scope and limits, environment-incident record"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/sweep-q11.jsonl
  role: data
  note: "887 records m=21..907 ALL UNSAT (kissat 4.0.4 def-mode over the genfam12 family census; per-width conflicts, process-time, CNF md5, vars/clauses; INDET 0, SAT 0, no gaps): completes the (8,11) witness-free band 21..907"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/calibration-cnf-byteidentity.jsonl
  role: verifier
  note: "21/21 CNF byte-identity of genfam12 vs sat2.js all-triples census (8x11..16 q11/q12) and vs genfast.js chord-pair census (8x17/20/26/40/60 q11/q12); reproduced after a full environment rebuild"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses
  role: data
  note: "witness files on main: 8x17..20 q11 and 8x15..16 q12 (kissat SAT beyond the SA non-discovery record); 8x15/16 q11 pending upload from the local artifacts mount; all dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction; rows 2,5 full, single 9-stone deficient row; m=11 q11 witness is 78 stones 2-deficient)"
scope: "finite machine verification: kissat 4.0.4 def-mode UNSAT over the family census, sound band-wide for m <= 984 (Theorem A + Corollary 4; the q11 sweep stays within m <= 907) + constructive dual-verified witnesses + K0318 proved tail exclusion; up to census completeness and solver correctness; (8,12) sweep 231..882 in flight"
evidence: "complete-encoding UNSAT instances (def mode = 'exists a row-deficient maximal safe config' since safety caps every row at q-1) + constructive witnesses dual-verified by two independent systems + 21/21 CNF byte-identity against both predecessor census generators + bit-exact cross-reset determinism (m=21: 1,379,955 and m=26: 162,762 conflicts). See the experiment README."
---

# 8×m q=11 / q=12 行欠損帯閉包 — (8,11) は M=21 で完全決着（w=8 初）・(8,12) は掃引中

## 主張

1. **(8,11)**: 行欠損の極大安全配置が **m=11..20 の全幅に存在する**（m=11 は78石2欠損・
   m=12..20 は79石単一欠損・rows 2,5 full・欠損行は9石。m=12..15 は SA レーン
   （eight-row-q11-q12-sa-witnesses-20261115）・m=15..20 は kissat 4.0.4 def-mode SAT）。
2. **(8,11)**: **m=21..907 の全887幅で行欠損極大配置は存在しない**（族census 符号化・
   kissat 4.0.4 def-mode・conflicts は m=21 の 1,379,955 を最大に漸減・process-time ≤41s・
   INDET 0・SAT 0・欠落 0）。
3. **決着**: m ≥ 908 は K0318 substitution U_{8,11}=908（proved）で排除されるため
   **M_{8,11} = 21 が exact に決着**（w=8 で初の完全決着。w≥6 全体では M_{7,10}=19・
   M_{7,9}=24 に次ぐ3例目）。
4. **(8,12)**: witness 8×12..8×16（87石単一欠損・m=15..16 は kissat 新規）・
   witness-free 17..230（214幅 UNSAT・INDET 0）より **M_{8,12} ∈ {17} ∪ [231, 883]**。
   231..882 の掃引は継続中（resume-safe）。全幅 UNSAT なら M_{8,12}=17 exact。
5. **genfam12.js（族census 生成器）**: ≥11点円が F1 のみ（Theorem A + 系4・m≤984）を
   健全性の核に、「8行 + (m−7) 個の12点 F1 円（中心 (u, 7/2)、(2x−2u)²+(2y−7)²=50、
   rows {0,1,3,4,6,7}）」のみの O(m) census で CNF を生成（sat2.js の符号化を
   monkey-patch で verbatim 再利用・曲線順序は buildCensus と厳密一致）。
   **sat2.js 全三つ組census と 8×11..16（q11/q12）、genfast.js 弦対census と
   8×17/20/26/40/60（q11/q12）の計21対照で CNF byte-identity**。全三つ組census の
   生成コスト壁を回避し、887幅の帯掃引を可能にした。
6. SA の m=16..26（q11）/15,16（q12）「抵抗」はヒューリスティック非発見の記録であり、
   m=16..20・15..16 の witness 発見により解決済み。

## 手法と検証

符号化は sat2.js（K0810 census + sequential counter + 極大性）を verbatim 使用
（`S.buildCensus` のみ差し替え）。def 単一節（∨¬rowGe[y]）は「総石数 < w(q−1) ⟺
ある行 ≤ q−2」により行欠損存在の完全符号化。健全性: 族census は全census から曲線を
落としたものであり、制約を削るだけなので UNSAT は全census に遺伝する（q11/q12 の
掃引範囲 m ≤ 907 < 984 で Theorem A + 系4 が全 q点円の族を F1 に限る）。
SAT witness は sat.js verifyConfig（全census・census 不使用の独立実装）と
verify_witness.py（Python exact Fraction・別実装）の2系統で safe+maximal+行欠損を検証。
較正: 21対照 CNF byte-identity（sat2.js 全census・genfast.js 弦対census の両系統）。
決定性: m=21 (1,379,955)・m=26 (162,762) の conflicts が環境の完全リセット・再構築を
またいで bit-exact。

## 範囲と限界

有限機械検証（族census の完全性は Theorem A + 系4（m≤984）とソルバ正確性まで）。
数論的証明ではない。(8,12) の掃引 231..882 は未完で M_{8,12}=17 は候補にとどまる。
witness 探索前線は (8,11) では消滅（完全決着）、(8,12) では掃引完了後に消滅予定。
