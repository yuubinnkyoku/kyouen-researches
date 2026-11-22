---
id: K0843
title: "8xm q=11 / q=12 row-deficient band closure — (8,11) witness band 11..20 + witness-free band 21..907 fully swept (M_{8,11} = 21 exact, first complete determination at w=8); (8,12) witness band 12..16 + witness-free band 17..882 fully swept (M_{8,12} = 17 exact, second complete determination at w=8)"
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
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/sweep-q12-shard1-m17-316.jsonl
  role: data
  note: "q12 sweep shard 1 of 3 (m=17..316, 300 widths): 866-width band m=17..882 ALL UNSAT (kissat 4.0.4 def-mode; conflicts min 679 at m=51, max 6,653 at m=17, median 1,655.5, p90 2,868 nearest-rank, sum 1,598,748; INDET 0, SAT 0, no gaps); md5 2ffc285045d40230cb72e5e86db2c0f4; together with shards 2-3 byte-exact against the canonical records/sweep-q12.jsonl (866 lines, md5 9c628f8e25ca541d82491e322743789a)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/sweep-q12-shard2-m317-616.jsonl
  role: data
  note: "q12 sweep shard 2 of 3 (m=317..616, 300 widths); md5 898b981feafbadaef4bcdbb5695c1a48; fetched back from main and md5-verified against records/sweep-q12.checksums"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/sweep-q12-shard3-m617-882.jsonl
  role: data
  note: "q12 sweep shard 3 of 3 (m=617..882, 266 widths); md5 6e86b860cd39603da89a64bbdb0436a2; fetched back from main and md5-verified against records/sweep-q12.checksums"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/sweep-q12.checksums
  role: verifier
  note: "md5 manifest of the three q12 sweep shards plus the canonical sweep-q12.jsonl (sha256 8e29576d0fe3fe037fbf9a08eaa293f19d7f78576255614a4cdc39bed2d195c2); every published shard fetched back and byte-verified"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/calibration-takeover-20261122.jsonl
  role: verifier
  note: "29/29 takeover calibration PASS: (A) 11/11 CNF byte-identity vs sat2.js all-triples census at 8x11..16 q11/q12, (B) 10/10 vs genfast.js chord-pair census at 8x17/20/26/40/60 q11/q12, (C) 8/8 CNF md5/vars/clauses match vs published records/sweep-q11.jsonl at m=21,26,40,100,300,500,700,907"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/records/rerun-sample-20261122.jsonl
  role: verifier
  note: "8-width sampled rerun rebuilt only from published artifacts (scripts/genfam12.js + sat2.js from seven-row-inband-families-20261114) and a fresh official kissat 4.0.4 download (binary md5 3a5eba830aa6008a604fcc9bbe99a325, bit-identical to the sweep binary): m=17,51,231,316,317,616,617,882 all regenerate the published CNF md5/vars/clauses byte-exactly and re-solve UNSAT with bit-exact conflicts (6653, 679, 2097, 1835, 1668, 1869, 1731, 1996); same execution environment, so an independent-environment full re-run remains future work"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/scripts/genfam12.js
  role: solver
  note: "family-census CNF generator (8 rows + m-7 twelve-point F1 circles); published and byte-verified against the kit copy"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/scripts/sweep-q12.sh
  role: solver
  note: "resume-safe sweep driver for the q12 band; published and byte-verified against the kit copy"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x15q12.json
  role: data
  note: "87-stone single-deficiency witness at 8x15 q12, kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x16q12.json
  role: data
  note: "87-stone single-deficiency witness at 8x16 q12, kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x17q11.json
  role: data
  note: "79-stone single-deficiency witness at 8x17 q11 (rows 2,5 full, single 9-stone deficient row), kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x18q11.json
  role: data
  note: "79-stone single-deficiency witness at 8x18 q11 (rows 2,5 full, single 9-stone deficient row), kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x19q11.json
  role: data
  note: "79-stone single-deficiency witness at 8x19 q11 (rows 2,5 full, single 9-stone deficient row), kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction)"
- path: research/experiments/eight-row-q11-q12-band-closure-20261115/witnesses/witness-8x20q11.json
  role: data
  note: "79-stone single-deficiency witness at 8x20 q11 (rows 2,5 full, single 9-stone deficient row), kissat def-mode SAT beyond the SA non-discovery record; dual-verified (sat.js verifyConfig + verify_witness.py exact Fraction); the m=12..15 SA-lane witnesses, the m=11 78-stone 2-deficient q11 witness and the 8x15/16 q11 witnesses are in the SA-lane experiment dirs and the local artifacts mount pending upload"

scope: "finite machine verification: kissat 4.0.4 def-mode UNSAT over the family census, sound band-wide for m <= 984 (Theorem A + Corollary 4; the q11 sweep stays within m <= 907, the q12 sweep within m <= 882) + constructive dual-verified witnesses + K0318 proved tail exclusion; up to census completeness and solver correctness; both bands complete"
evidence: "complete-encoding UNSAT instances (def mode = 'exists a row-deficient maximal safe config' since safety caps every row at q-1) + constructive witnesses dual-verified by two independent systems + 21/21 CNF byte-identity against both predecessor census generators + bit-exact cross-reset determinism (m=21: 1,379,955 and m=26: 162,762 conflicts) + q12: 866 widths m=17..882 ALL UNSAT published as three md5-verified shards with a 29/29 takeover calibration. See the experiment README."
---

# 8×m q=11 / q=12 行欠損帯閉包 — (8,11) は M=21・(8,12) は M=17 でともに完全決着（w=8）

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
   **witness-free 17..882 完走（全866幅 UNSAT・INDET 0・SAT 0・欠落 0・conflicts min 679（m=51）・
   max 6,653（m=17）・median 1,655.5・p90 2,868（nearest-rank）・総計 1,598,748・2026-11-22 完了・
   記録は3シャードで公開し checksums + fetch-back で md5 検証済み）**より、尾部 m ≥ 883 の排除
   （U_{8,12}=883・K0318 proved）と合わせて **M_{8,12} = 17 が exact に決着**
   （w=8 で2例目の完全決着）。
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
較正: 21対照 CNF byte-identity（sat2.js 全census・genfast.js 弦対census の両系統）+
接管較正 29/29（2026-11-22・(A)(B) の CNF byte-identity 再現に加え (C) 公開済み
sweep-q11 記録の CNF md5/vars/clauses 再現 8幅を含む）。
決定性: m=21 (1,379,955)・m=26 (162,762) の conflicts が環境の完全リセット・再構築を
またいで bit-exact。

## 範囲と限界

有限機械検証（族census の完全性は Theorem A + 系4（m≤984）とソルバ正確性まで）。
数論的証明ではない。両帯の掃引は完了し、(8,11)・(8,12) とも witness 探索前線は消滅
（完全決着）。
