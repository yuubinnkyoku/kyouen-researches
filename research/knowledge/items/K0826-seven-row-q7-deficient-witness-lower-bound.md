---
id: K0826
title: "7xm q=7 row-deficient witness band — witnesses 7x7..7x26 (M_{7,7} >= 27, upper 708 by K0318 substitution); first (7,7) family results (q=w diagonal)"
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
  note: "claims, method (sat2.js all-triples census at q=w, rowY split), verification protocol (dual witness verification + third-system pure-TS/BigInt confirmation, m=24 bit-exact determinism re-run), results table, honest negatives, scope and limits"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/def-search/records.jsonl
  role: data
  note: "19 records: SAT m=7..25 witnesses dual-verified (m=7..14 deep deficiency 30..41 stones, m=15..24 single-deficiency 41 stones) + m=25 OR-instance INDET (2,478,476 conflicts at 240s cap — honest negative)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/row-split/records.jsonl
  role: data
  note: "m=25 rowY=0..3 fixed-row split: rowY=3 (central row) SAT at 756,785 conflicts (41-stone witness rows 6,6,6,5,6,6,6 dual-verified); rowY=0/1/2 INDET at 200s caps (961,944 / 970,708 / 1,130,645 conflicts — not absence claims)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/row-split/s7x25q7_rowY3.witness.json
  role: data
  note: "largest-width (7,7) witness (41 stones at 7x25, rows 6,6,6,5,6,6,6, found via the rowY=3 split); m=7..24 witnesses at output/def-search/s7xMq7_none.witness.json, all dual-verified (sat.js verifyConfig + Python Fraction)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/results.jsonl
  role: data
  note: "parallel-lane independent-run records: SAT m=8..26 with raw kissat logs m=8..21; conflicts bit-exact with the def-search/row-split records on shared instances (m=24 def OR 2,105,329; m=25 rowY=3 756,785); m=26 record: rowY=3 SAT, 1,951,966 conflicts, 41 stones rows 6,6,6,5,6,6,6, dual-verified"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/w7q7_7x26q7_rowY3.witness.json
  role: data
  note: "m=26 witness (41 stones, rows 6,6,6,5,6,6,6) extends the band to 7x26: M_{7,7} >= 27, frontier 7x27; raw log at output/w7q7_7x26q7_rowY3.kissat.txt; m=27 rowY=3 262s-cap INDET log at output/w7q7_7x27q7_rowY3.kissat.txt (2,242,940 conflicts, honest negative)"
- path: research/experiments/seven-row-q7-witness-search-20261114/scripts/verify_independent.ts
  role: verifier
  note: "third verification system, independent of all repo code: pure TypeScript + BigInt exact arithmetic; circle identity by exact rational keys from stone triples (bijective reparameterization of the center), membership re-tested by the 4x4 cocircularity determinant; lines by canonical (a,b,c)"
- path: research/experiments/seven-row-q7-witness-search-20261114/output/ts-verify.json
  role: data
  note: "third-system records: m=25/m=26 rowY=3 witnesses both safe (9,477/9,407 circles, all curves and lines <= 6 stones), maximal (0 uncovered cells), row-deficient (rows 6,6,6,5,6,6,6); 7-collinear negative control correctly unsafe; m=26 hence triple-verified"
- path: research/experiments/seven-row-q7-m27-surgery-20261115/README.md
  role: proof
  note: "7x27 frontier surgery complete case-split from the 7x26 rowY3 seed: one-stone-short census (unique uncovered cell (26,3), sole 5-stone T-curve = line y=3, no 4-stone T-curves), blocking lemma (A meets {T} union lineEmpty), exact-iff prefilters (single-addition okZ gate, shared eff>=5 pair gate, eff5+1/eff4+2 coverage), canonical counts for all enumerated sub-spaces incl. the complete (2,3) case split (r3_on blocking analysis), 559/559 targeted controls, open sub-spaces listed, and the discovery that the first ad-hoc (1,3)/(3,3) runs had a dead-gate effOf defect (verdict superseded by the verified consolidated machine)"
- path: research/experiments/seven-row-q7-m27-surgery-20261115/output/surgery_results.json
  role: data
  note: "verified consolidated machine outputs: twoEdit singles 18,942 (13,725 okZ + 5,217 coverage) + pairs 99,326 (15,654 shared + 83,672 coverage) -> 0; (1,3) line-addition 149,940 (90,540 safety-gate + 59,400 coverage, gate 60/60 direct-brute UNSAFE confirm) + T-addition 10,660 -> 0; line-triple (3,3) 554,400 total (550,320 okZ-gated) -> 4,080 valid (1,430 shared + 2,650 coverage) -> 0; coverage targeted agreement 150/150 + 80/80 + 80/80 + 100/100; (2,3) complete: 10,660 R -> 0 witnesses (370 r3>=2 blocking-lemma rejects, 3,150 r3=1 forced-line-pair coverage wholesale, 115 wholesale + 4,320 HardU-intersection R rejects + 14,948 z-okZ + 55,638 per-z coverage-intersection rejects, 0 pairs through coverage; targeted cov 36/36 + zok 30/30 + line 23/23; machine script scripts/m27_surgery_two_add_three_remove.ts)"
scope: "finite machine verification: kissat 4.0.4 (all instances); widths stated per family only; up to census completeness and solver correctness"
evidence: "complete-encoding SAT instances (def mode is exactly 'exists row-deficient maximal safe config') + constructive dual-verified witnesses (census-free sat.js verifyConfig + Python Fraction) + third independent verification system (pure TS/BigInt, no repo code: scripts/verify_independent.ts + output/ts-verify.json — m=25/m=26 rowY=3 witnesses PASS, 7-collinear negative control unsafe, m=26 triple-verified) + m=24 bit-exact determinism re-run (2,105,329 conflicts reproduced; cross-lane independent-run bit-exact reproduction on shared instances m=24/m=25 rowY=3: 2,105,329 / 756,785). See report.md."
---

# 7×m q=7 行欠損witness帯 — witness 7×7..7×26（M_{7,7} ≥ 27・上界708）・q=w 対角ファミリー初の結果

## 主張

1. **(7,7)（7×m・q=7・q点共円/共線禁止）**: 行欠損の極大安全配置が
   **m=7..26 の全幅で存在する**（本ファミリー初の結果。q=w の対角ケース）。
   - m=7..14 は深欠損（30, 32, 34, 37, 38, 39, 40, 41 石・deficiency 12..1。
     m=10..14 は上位6行が6石・最下段 1..5 石の構造系列）。
   - m=15..26 は単一欠損の **41石**（ある行のみ5石・他の6行は6石。
     満容量 42 = 7·6）。
   - すべて census 不使用 JS verifyConfig と Python Fraction 独立実装の
     2系統検証で safe + maximal + 行欠損 PASS。
2. よって witness 幅集合は {7..26} を含み **M_{7,7} ≥ 27**
   （M ∈ [27, 708]・上界 708 は K0318 曲線パッキング代入・U_{7,7}=708）。
3. **m=25 の解法**: def OR 実例は 240s cap で INDET（2,478,476 conflicts）だったが、
   欠損行固定の **rowY 分解（V 対称で 4 クラス）の rowY=3（中央行）で SAT**
   （756,785 conflicts）。rowY=0/1/2 は 200s cap で INDET（不在の主張ではない）。
   K0825 の (7,8) m=24 と同様、**行固定分解が OR 壁を突破**（q=7 でも再確認）。
4. **正直な負記録**: m=25 rowY=0/1/2 の INDET、m=27 rowY=3 は 262s cap で INDET（2,242,940 conflicts・不在の主張ではない）。
   witness 探索の前線は **7×27**。m=26 は rowY=3 固定分解で SAT（1,951,966 conflicts・41石 rows 6,6,6,5,6,6,6・並走独立run・2系統検証 PASS）。
5. **観測（全称主張ではない）**: 7行族の単一欠損 witness 帯は
   (7,8) m=13..24 と (7,7) m=15..26 で同型（欠損行の位置は幅ごとに変わり、
   (7,7) m=25 では中央行）。def OR 実例の難化も同様
   （(7,7): m=23 SAT 119,071 → m=24 SAT 2,105,329 → m=25 OR INDET 2,478,476 → m=26 rowY=3 SAT 1,951,966 → m=27 rowY=3 INDET 2,242,940@262s）。
6. **第3検証系（純TS・BigInt・repoコード不使用）**: m=25 rowY=3・m=26 rowY=3
   の両 witness を独立実装（円は有理 (cx, cy, r²) キー + 4×4 共円行列式・
   直線は正規化 (a,b,c)）で検証し、いずれも safe + maximal + 行欠損 PASS
   （m=25: 円 9,477・m=26: 円 9,407・全曲線・全直線 ≤ 6 石・未覆空点 0）。
   負対照（7点共線）は正しく unsafe。**m=26 witness は3系統検証**となり、
   M_{7,7} ≥ 27 の構成要素は3つの独立実装系で確認済み。


7. **7×27 前線 surgery 完全負（既知 m=26 witness rowY3 族近傍・全 833,868 + (2,3) 34,103,980 形式候補・2026-11-15）**:
   m=26 rowY3 witness（既知の唯一の m=26 witness・4ミラー像を含む。surgery の可否は盤面対称性で不変）からの
   7×27 延伸を編集 S' = S − R + A（|R| ≥ |A|・A は空セル・行欠損要件）で探すと、
   - 2編集 (|A|,|R|) ∈ {(1,1),(1,2),(2,2)}: 18,942 + 99,326 候補 → **0 witness**
   - (1,3) 追加1・除去3: 直線追加型 149,940（単追加安全 gate 90,540 + 被覆棄却 59,400）・
     T 追加型 10,660 → **0**
   - (3,3) 直線3追加型（r_on=2 で直線 5−2+3=6 が成立する完全部分空間）:
     554,400（okZ gate 550,320）→ 有効 4,080（shared 1,430 + 被覆 2,650）→ **0**
   - (2,3) 追加2・除去3（2026-11-15 完全列挙）: 形式的 34,103,980 候補
     （10,660 R × 3,203 ペア）→ r3_on ≥ 2 は T-blocking 不可能で 370 R 即棄却・
     r3_on = 1 は追加2つが直線上に強制され Ux 直線対被覆 wholesale で 3,150 R 全滅・
     r3_on = 0 は wholesale 115 + HardU 交集 4,320 R + z級 okZ 14,948 + 被覆交集 55,638
     全棄却（coverage 通過ペア 0）→ **0**
   のすべてで safe-maximal witness なし（完全列挙・正規化機械で再検証済み）。
   seed は一石不足構造: 7×27 の未遮断セルは T=(26,3) のみ・T の5石曲線は直線 y=3 のみ・
   4石T-曲線は存在せず、blocking の場合分けが完全に閉じる。
   検証: 標的直接検証 559/559（被覆 410 + safety 直接brute 60 + (2,3) 89: coverage 36・z-okZ 30・line 23）・CTL2 摂動棄却 PASS・
   twoEdit は独立2実装で全計数一致。初回 ad-hoc 実行の (1,3)/(3,3) は effOf 欠陥
   （gate 不動作）で棄却根拠が無効だったため、検証済み consolidated 機械の結果に差し替え。
   **7×27 全配置の不在主張ではない**（open: (3,3) 一般・3石T-曲線上の3追加・
   |R| ≥ 4・seed から離れた fresh 配置 — m=27 の INDET 記録・前線 7×27 は不変）。

## 手法と検証

符号化は K0810 の sat2.js を verbatim（genfast.js は q ≥ w+1 専用のため
不適用・全三つ組censusを n=7m ≤ 175 で使用）。def 単一節 ∨¬rowGe[y] は
「総石数 < 42 ⟺ ある行 ≤ 5」の完全符号化。制御: m=24 def OR 再実行で
conflicts 2,105,329 が bit-exact 再現（決定性）。sat2.js の符号化自体は
前回実験で fastsat/kissat 交差較正・cross-reset 決定性検証済みの同一コード。

## 範囲と限界

有限機械検証（census 完全性とソルバ正確性まで）。数論的証明ではない。
M_{7,7} の確定には 7×27..7×28（census 実用範囲）以降の評価と
上界 708 の改善（K0342 型 tail 評価）が残る。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
