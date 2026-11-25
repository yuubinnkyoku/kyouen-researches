---
id: K1309
title: "遷移窓合同行の全称崩壊: T-WC（窓合同ペア行 = D(g,z)・k・m 非依存）・T-WBC（窓合同床行 = 0）・L-BE/L-C 導出表（K1308 O1 合同半分の解決・OBS-WC 全称昇格・publish-then-execute・宣言ノートに証明全文収録・40,412 点公式監査 bad 0・4 走 byte-identical・ペア・床とも全 k 軸の未確定は非合同窓行のみに縮小）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the window congruent-row collapse. Coordinates: pair k := R - 2m - g, bed k := R - 2a, window 1 <= k <= z-1, congruent means k = z (mod 2), z >= 3. T-WC (universal): for every z >= 3, m >= 1, g >= 1 and every window-congruent k in [1, z-1]: H(2m+g+k; (m, m+g); z) = D(g, z) = [g odd] (g <= z) / 2 (g = z+1) / [g even] (g >= z+2) — the K1308 Z-DIAG diagonal law value, INDEPENDENT of k and m, so every window congruent row carries the diagonal row's value. T-WBC (universal): for every z >= 3, a >= 1 and window-congruent k: H(2a+k; (a, a); z) = 0 (the bed window congruent rows vanish; the non-congruent bed row k = z-1 of OBS-BW stays open). Together with the published K1303 band (k <= 0, all planes) and K1308 upper half (k >= z), the UNDETERMINED region for pairs and beds is now EXACTLY the non-congruent window rows 1 <= k <= z-1, k not= z (mod 2), z >= 3 — a full k-axis classification with a value law on every congruent row and O(1) evaluation everywhere else. L-BE (derived from the published K0832 closed form): the m=1 B-exit single token v(g+1, z+1, g+k+1) = [g even] (g <= z-1) / 2 (g = z) / [z even] (g = z+1) / [g odd] (g >= z+2), window-k independent. L-C (derived from the published K1303 band laws): the window pair C-child reads D(g, z-1) (always for k >= 2, and for k = 1 when 2m+g >= z-1); the ONLY exception cells (k=1 and 2m+g <= z-2) read 2*[g odd]; the window bed C-child reads 0 on both branches."
  - "STRUCTURE (typed children, joint budget induction — the window sibling of the K1308 upper-half packet): every option of a window-congruent pair cell is EXACTLY one of fall (pair, g+1, k and z SAME) / compress (pair, g-1, k same) / corner (g=1 -> bed, k same: stays inside T-WBC by congruence since k=z-1 from k=z congruence step, or bigger) / B-exit (m=1 -> single token, L-BE) / C (window-congruent pair at (k-1, z-1) for k >= 2 — congruence is preserved because both k and z flip parity — or the k=0 band row on plane z-1 for k=1, read by the published K1303 band). Bed options: A -> window-congruent pair gap 1, B(a=1) -> v(1, z+1, k+1), C -> window-congruent bed (k-1, z-1) or the k=0 band bed. Congruence invariance: A-children preserve (k, z), C-children decrement BOTH, so the packet {T-WC, T-WBC} closes on budget R-1 by strong induction with the K0832 closed form and the K1303 band as instant bases (neither induction hypothesis needs the non-congruent rows — this is why the window CONGRUENT half closes while the non-congruent half, whose C-children land on non-congruent rows, is genuinely blocked). Hand proof by region tables: A (g <= z-2) / A2 (g = z-1) / B (g = z) / C (g = z+1) / D1 (g = z+2) / D2 (g >= z+3), split m >= 2 vs m = 1, exception vs normal cells; mex tables close pointwise; the 2 appears exactly at the region boundary g = z (B-exit) and the D1 normal-row fall = 0 = 1 - D pattern."
  - "SUBSUMPTION: K1308 OBS-WC (congruent rows follow Z-DIAG, z3..13 census, 1,296 pts) is promoted from observation to the T-WC instances (machine D-checked via the K1308 E4b box re-run, 1,296 pts mismatch 0). K1308 O1 (transition window law, open) — the CONGRUENT half is now proved (this package); the remaining open is re-registered as O1' = the non-congruent window rows only (pairs and beds). K1308 anchors re-checked in D8 (2,600 pts): Z-DIAG k=z rows z3..10, T-DU' beds z0..6 k=z..z+3, T-UH z0..6 k=z+1..z+3 all bad 0. The frozen non-congruent value-distribution census (OBS-NCW, 35 rows, z3..12 m1..3 g1..12, 12,960 cells) is an OBSERVATION registration with NO claim, re-frozen identically by the machine D10: deep non-congruent rows take only {0,1} split by gap parity (consistent with [g odd]), but the shallow rows k in {1,2,3} spawn 2s at positions structured by the k-z difference — the true non-congruent law is open."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 7041fd07 (observed HEAD 42cb2abc; K1309 vacancy verified; K1306 SLB-ladder and K1307-provisional REMO lanes orthogonal, non-contact), kit 3c11a737 (12 files: README.md, verify_k1309.py, engine_block.py, explore_wc.py, explore_wc.out X1..X8 frozen, predry/dryrun1-4 (+.info), 4 runs byte-identical sha256 3b5aa0b153569026d1e3312d5e1a1a6ffb46a6046417e388fdd5f0c0049cc8dd), fetch-back byte-identical 12/12 (kit README.md needed one raw-CDN 404 retry, size 3879 confirmed, sha 3be4982b...), THEN official 4 runs from the verified bytes: same cwd x2 (PYTHONHASHSEED random/1) + isolated tree env -i x2 (PYTHONHASHSEED 99/7), all rc=0, stdout byte-identical to the declared predry sha exactly (~1.3 s/run, python 3.12). verify_k1309.py sha256 cd1328e37acb445d67e8525877582814ee39ef61508689c9e7542657a5bd3414, embedded engine block startup sha gate pin bd5f22e4... (K1138/K1282..K1308 chain identical embedded bytes; standalone engine_block.py 582c93c1... identical to the K1282..K1308 kits). counts [10752, 3456, 3840, 888, 8736, 1344, 3740, 2600, 341, 35, 4680] total 40,412 bad 0 (D1 T-WC census / D2 T-WC far z{18,20,22} / D3 T-WC m-distance to m=20 / D4 T-WBC census / D5 typed self-check: children built ONLY from the hand tables T-WC/T-WBC/L-BE/L-C + published closed forms, mex == claim == engine pointwise / D6 L-BE vs transcribed closed form vs BOTH engines (window box 1,344) / D7 band + L-C engine gate (k=0 pair band w2..15, k=0 bed band w2..15, k=1 C-child L-BE hand table) / D8 published anchors 2,600 / D9 cross-engine canonical-vs-ordered 341 / D10 OBS-NCW frozen 35-row table reproduction (observation reproducibility, NOT a law claim) / D11 k=1 row stress z odd 3..27 m<=12 g<=30 including the 650 exception cells 4,680). Mutation battery 12/12 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), wc1 [D1=10752, D5=672] total 11,424 / wc2 4,128 / wc3 4,512 / bw 888 / ty 8,736 / be 1,344 / cp 3,740 / ps 2,600 / xg 341 / rw 1 / ex 4,680, all rc=1 (wc1/wc2/wc3 also flip the D5 typed table = +672 honest cross-count as pre-declared; rw flips exactly 1 frozen-table row). Audit artifacts published at 7c0d311f (audit_run1-4.out+.info, tamper 12 record files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 33 entries), fetch-back 33/33 sha256 match."
  - "OPEN registrations (note SS5): O1' the non-congruent window rows 1 <= k <= z-1 (k not= z mod 2, z >= 3) for pairs AND beds — the typed packet cannot close here because C-children of non-congruent rows are again non-congruent rows (self-referential block); the D10 frozen table is the input data (deep rows {0,1} by gap parity, shallow rows k in {1,2,3} spawn structured 2s). O2 bed non-congruent rows incl. the k=z-1 OBS-BW row share the same blocker. F1 the C-SUM three-token typed generalization unchanged (untouched). F2 11x11 connection: with this package the O(1)-evaluable rows on EVERY plane are now the band k <= 0, the upper half k >= z, the diagonal k = z, AND the window congruent rows — the only non-instant-evaluable region of the whole pair/bed k-axis is the non-congruent window rows; pruning-lattice widening recorded for the giant-search owners, adoption decision belongs to them, as since K1286. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed."
relations:
- type: resolves
  target: K1308
  note: "K1308 open 登録 O1（遷移窓 1≤k≤z−1・z≥3 の真の法則）のうち**合同半分**を T-WC/T-WBC で全称解決。OBS-WC（合同行 Z-DIAG 追従・z3..13・1,296 点 census）は観測から T-WC の実例へ昇格（機体 D8/D9 前後の E4b box 再現 1,296 点 mismatch 0・公刊アンカー 2,600 点 bad 0）。残る O1′ = 非合同窓行のみとして再登録。engine pin は同一 chain bytes（bd5f22e4…・埋込み・単体 582c93c1…）。"
- type: extends
  target: K1308
  note: "K1308 の上半パッケージ（T-UH/T-DU′/Z-DIAG/L-SB）に対し、窓合同行を同一の typed 子構文（A 手子は k・z 不変・C 手子は k・z 同時 −1 で合同性保存）で補完。合同性の保存が帰納 packet {T-WC, T-WBC} の閉性の核で、非合同行は C 子が非合同行に落ちるため同 packet では本質的に閉じない（= O1′ blocker の構造的理由）。"
- type: depends_on
  target: K1303
  note: "K1303 一般帯域則 T-GEPSF/T-GEBED（k≤0・全 w）を L-C の k=1 C 子（帯域 k=0 行・plane z−1）と床の k=1 C 子の両分岐で直接使用。D7 が帯域 engine ゲート（k=0 ペア帯域 w2..15 m1..6 g1..20・k=0 床帯域 w2..15 a1..10）で照合。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,p,R)。L-BE は m=1 窓 B-exit v(g+1, z+1, g+k+1) の窓 box 全域での値表を閉形式から直接導出（D6 が転写閉形式・両 engine の三方照合 1,344 点）。"
- type: related
  target: K1282
  note: "engine block pin chain（bd5f22e4…・単体 582c93c1…）は K1282..K1308 kit と同一 bytes を使用。"
- type: related
  target: K1303
  note: "F2 接続: 11×11 枝刈り格子の O(1) 行が「帯域 k≤0・上半 k≥z・対角 k=z・窓合同行」まで拡大（残る非即値域は非合同窓行のみ）。巨大探索レーンオーナーへの記録のみ。"
artifacts:
- path: research/log/2026-11-24-window-congruent-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 7041fd07・着手時 HEAD 42cb2abc・K1309 空き確認後に push・証明の正本）。§1 主張一式（T-WC・T-WBC・L-BE・L-C・位置恒等式・被包・OBS-NCW）・§2 手証明全文（2.0 packet と well-founded 性・2.1 L-BE・2.2 L-C・2.3 T-WBC・2.4 T-WC 区域表〔A/A2/B/C/D1/D2 × m≥2/m=1 × 例外/通常〕）・§3 宣言前探索 X1..X8 凍結・§4 機体宣言（counts 40,412・変異表 12 種事前宣言・predry sha 3b5aa0b1…）・§4.5 主張の区別・§5 open 登録 O1′/O2/F1/F2・§6 honest 構築経緯（engine sha gate による初回 block 誤り即時検出・§2.4 D1 表の初回誤算と宣言前是正）。
- path: research/experiments/window-congruent-20261124/
  role: machine
  note: 実験キット一式（出版 3c11a737・成果物 7c0d311f）: README.md・verify_k1309.py (sha256 cd1328e3…・engine pin bd5f22e4… ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1308 chain と同一 bytes)・explore_wc.py / explore_wc.out (0c253020…/7e57e2e4…・X1..X8 凍結)・predry/dryrun1-4 (+.info・byte-identical 3b5aa0b1…) + 公式監査成果物（output/audit_run1-4.out+.info・tamper レコード 12 ファイル・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 33 entries・fetch-back 33/33 sha 一致）。
- path: research/log/2026-11-24-window-congruent-collapse.md
  role: report
  note: 実行 log（宣言 7041fd07 → kit 3c11a737 → fetch-back 12/12〔宣言ノート byte 一致 c18b9f9c…・README 404 retry 記録付き〕→ 公式 4 走 → 変異電池 12/12 → 成果物 7c0d311f → K item・README bullet の全記録・受入判定・次課題）。
---

## 概要

K1308 が O1（遷移窓 1 ≤ k ≤ z−1・z ≥ 3）の観測 OBS-WC として残していた
**合同半分**を、2 本の全称定理で確定した:

- **T-WC**: 窓合同ペア行（k ≡ z mod 2）はすべて **対角行と同じ値 D(g,z)** をとり、
  値は k・m に非依存（[g odd] (g≤z) / 2 (g=z+1) / [g even] (g≥z+2)）。
- **T-WBC**: 窓合同床行はすべて **0**（T-DU′ の k≥z 領域を窓の合同行まで拡張。
  床の非合同行 k=z−1〔OBS-BW〕は含まず・open のまま）。

導出補題として **L-BE**（m=1 B-exit 単一トークンの窓 box 値表・k 非依存）と
**L-C**（窓ペア C 子の値 = D(g, z−1)・例外 cell〔k=1 かつ 2m+g ≤ z−2〕のみ
2·[g odd]・床 C 子 = 0）が published 閉形式（K0832・K1303）から直接導かれる。

到達点として、ペア・床とも **全 k 軸のうち未確定は非合同窓行のみ**になった
（K1303 帯域 k≤0 + K1308 対角/上半 k≥z + 本定理の窓合同行の和集合が残り全部）。
非合同行は D10 凍結表（35 行・OBS-NCW）として観測登録のみ（深い行は {0,1} の
g 奇偶分割だが、浅い行 k ∈ {1,2,3} に構造化した 2 が発生・法則は open）。

構造の鍵は **A 手子は (k,z) 不変・C 手子は k と z を同時に −1（偶奇両反転で
合同性保存）** という位置恒等式で、帰納 packet {T-WC, T-WBC} が予算 R−1 上の
強帰納で閉じる。非合同行では C 子が再び非合同行に落ちるため、この packet では
本質的に閉じない——これが O1′ blocker の構造的理由であり、領域分割の誠実な
意味での「残り」である。

## 主張の区分（過大主張の防止）

- 定理（全称証明・宣言ノート §2 に証明全文）: T-WC・T-WBC。
- 導出補題（published からの直接導出・証明 §2.1/§2.2）: L-BE・L-C。
- 代数定理（engine-free 位置恒等式・§2.0）: 子の型閉包。
- 観測登録（未証明・主張なし）: OBS-NCW の D10 凍結表（35 行・値分布の
  再現性は観測の照合であって法則主張ではない）。
- census は証明ではない: 40,412 点は定理・手表の実機照合（bad 0）であり、
  定理の全称性は手証明によって成立する。

## 公式監査（publish-then-execute）

- 宣言 7041fd07（着手時 HEAD 42cb2abc・K1309 空き・K1306/K1307仮レーンと非接触）→
  機体 3c11a737（12 ファイル）→ fetch-back 12/12 byte 一致（kit README は
  raw CDN 404 を 1 度 retry して照合成立・honest 記録）→ 公式 4 走
  （同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2 99/7）すべて rc=0・
  stdout byte-identical sha256 3b5aa0b1…（宣言・predry と同一）。約 1.3 秒/走。
- counts `[10752, 3456, 3840, 888, 8736, 1344, 3740, 2600, 341, 35, 4680]`・
  総計 40,412 点・bad 0・engine_gate PASS。D5 typed（手表のみで子構成・
  mex == 申立 == engine の三点一致）・D6 L-BE 三方照合・D7 帯域 engine ゲート・
  D8 公刊アンカー 2,600・D10 非合同行凍結表再現・D11 k=1 例外 cell 650 個込み stress。
- 変異電池 12/12 検出・宣言どおり: engine rc=2（0ea47a80…）・wc1 11,424
  〔D1+D5〕・wc2 4,128・wc3 4,512・bw 888・ty 8,736・be 1,344・cp 3,740・
  ps 2,600・xg 341・rw 1・ex 4,680（すべて rc=1）。
- 成果物出版 7c0d311f（audit_run1-4.out+.info・tamper レコード 12・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 33 entries・fetch-back 33/33）。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は全時点 UNKNOWN。
- 全 plane で O(1) 評価可能な行が「帯域 k≤0・上半 k≥z・対角 k=z・窓合同行」に
  なり、非即値域は非合同窓行のみ。枝刈り格子の拡大として巨大レーンオーナーに
  記録する（採用判断はオーナー側・Part DH など 11×11 レーンと非接触）。

## 次課題（単一オーナー候補）

1. **O1′**: 非合同窓行 1 ≤ k ≤ z−1（k ≢ z mod 2・z≥3）の真の法則。
   D10 凍結表が入力データ。typed packet の自己参照 blocker の解除が本体
   （非合同行の値そのものの問題に帰着）。
2. **O2**: 床非合同行（k=z−1 の OBS-BW 含む）。同一 blocker。
3. **F1**（K1308 から不変）: C-SUM 3 トークン typed 化。
