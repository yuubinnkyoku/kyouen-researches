---
id: K1287
title: "multi-c web F2 スプレッド法則表: C-SPW/D/E/A'/A（5 族 × 3 面 × d<=8 の値法則・census-verified conjecture）・T-RC 子恒等式 I1-I11（族の閉性・代数定理）・mex 不動点機械証明書（K1286 O3 の F2 入力を継承拡張・11,743 点公式監査 bad 0・4 走 byte-identical・E 族旧法則 bad=96 の反例検出と修正を含む）"
kind: conjecture
status: conjecture
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the multi-c web F2 spread-law tables. Five web families in the min-gap band, planes z in {0,1,2}: W(d,c,m) = {m,(m+d)^c}@(2m+d+2+z) / D(d,c,m) = {m,m+d-1,(m+d)^(c-1)}@(2m+d+1+z) / E(d,c,m) = {m,m+d-2,(m+d)^(c-1)}@(2m+d+z), d>=3 / A'(d,c,m) = {m,(m+d-1)^2,(m+d)^(c-2)}@(2m+d+z) / A(m,s) = {m^2,(m+1)^s}@(2m+2+z); frontier families Am(m,h>=2,s) = {m^2,(m+h)^s}@(2m+2+z) / SLB2 (x^c)@(x+3) z2 / SLB3 (x^c)@(x+4) z3 / L(zp,d,s) = {d,(d+1)^s}@(d+2+zp) plane zp+1. LAWS (all CENSUS-VERIFIED CONJECTURES, not theorems; census boxes: W z3 x d1..8 c2..6 m1..10 [1200] / D d2..8 [1050] / E d3..8 m1..9 [810] / A' d2..8 c3..7 [945] / A s0..6 m1..12 [252] / Am 576 + SLB2 88 + SLB3 88 + L 80 [D6 832], plus a WIDER pre-declaration explore box reaching c<=7, m<=12): C-SPW: z1 face = [d even] with NO exceptions (the c>=2 HALF of the K1284 open registration C-PC1z1-d4 solved on census; d=1 row is 0); z0/z2 faces: d>=2 = [d even], d=1 = (m=1,z=2 -> 2; z0 m=1 c=2 -> 0 else 2; m>=2: c=2 -> 0, c>=3 -> 2). C-SPD: z1 = [d odd] (= the c=1 pair-slice law of K1285); z0/z2: d=2 -> 2 (except (z2,m=1,c=2) -> 0), d>=3 = [d odd]. C-SPE: d even -> 1; d=3 -> (z1 -> 0, z0/z2 -> 2); odd d >= 5 -> 0 (the naive 'odd d -> 2' reading was REFUTED by the wide census with bad=96, all odd d>=5 — honest history recorded). C-SPA': H = [d even] on all three faces, no exceptions. C-SPA: z0 = [s=1]; z2 = (m=1 -> 0, m>=2 -> [s=1]); z1 = (s=0 -> 0, m=1 s>=1 -> 2, m>=2: s=1 -> 1, s>=2 -> 2). Frontier OBS tables: OBS-F1 Am z0 -> 0, z1 -> (s=0 -> 0, s>=1 -> 2), z2 -> all 0 EXCEPT the single-point anomaly (m=1,h=2,s=1) -> 1; OBS-F2/F3 SLB2/SLB3 = (c=1: [x odd], c>=2: [x even]) with x=2 exception rows; OBS-F4 L: zp=0 d=1 -> 2, zp=0 d>=2 = [d even], zp=1 d=1 = (s=1 -> 1, s>=2 -> 0), zp=1 d>=2 = [d even]. Universal claims stay OPEN (no proof beyond the boxes)."
  - "THE THEOREM PART (algebraic, universal, machine-checked engine-free): the T-RC child identities I1-I11 show the web families are CLOSED under their own options: I1 A-top(W) = D (drop m+d by A -> exactly the D family); I2 A-min(W) = W(d+1,c,m-1) (the Episcopal m-direction: the row index drops while the gap grows by 1, SAME web); I3/I6/I7/I8/I9 C-children = the same family one plane down; I4 A-mid(D) = E; I5 A-top(D) = A'; I10 B-min(D,d,1) = the L frontier point; I11 B-min(W,d,1) = a single-layer frontier point ((d+1)^c)@((d+1)+2+z) plane z+1 (z=0 -> published C-PB2 family, z=1/2 -> SLB2/SLB3 one plane up). Each is a one-line multiset+budget equality; the machine checks 3,132 identity instances at declared coordinates (gate D8, bad 0). Consequence (blocker diagnosis, note S5 O1): the universal proof of the five value laws would close by typed-child R-strong-induction EXACTLY as in K1285 S2, PROVIDED the m=1 B-exits are universalized: (i) single-layer families (x^c)@(x+2+z) plane z+1 (z=0 published C-PB2; z=1/2 = SLB2/SLB3 conjectures), (ii) L and Am frontier conjectures, (iii) the floor negative regions (K1286 O1/O2/O4)."
  - "STRUCTURE (web topology): the five families are the full min-gap band of the spread web future F2 (take-over of the K1286 S5 O3 input registration, d in {1,2,3} / 288 points OBS extended to d<=8 / 5 families / 3 planes / c>=2). W is the top spread row; A-exits walk DOWN the band (W -> D -> E or W -> D -> A'), B-exits at m=1 leave the web to the frontier (L for D, single-layer for W), C-exits descend the planes z -> z-1. The c-direction is invariant across the census (c up to 7): no law change in c within the boxes (O3 open registration: 'c-invariant spread' conjecture)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 40f945b8 (observed HEAD at start 5b9c6231, pre-push refetch 076e05c1; all intervening commits are the rival K1286 lane f6db3f33..9336611a + README repair e56c8cce + Part DH a4e00aa3/076e05c1 bookkeeping, non-contact; K1287 vacancy verified against the items dir commits — latest K item = K1286 at 9336611a, no competing declaration for K1287 or the multic-web-f2 territory), then kit 35394ac8 (verify_k1287.py sha256 52e7eea70090ef41095d19b33de177793a80d7b3a5619ff7708d12ae851fe434, startup sha gate on the embedded engine block, pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 = the SAME published block as K1138/K1282..K1286; engine_block.py standalone 582c93c1…, byte-identical to the K1282..K1286 kits; explore_k1287.py wide census explorer with stage z0|z1|z2|frontier, deterministic stdout), fetch-back of 12 published files (remote == local byte-exact 12/12), isolated trees k1287_iso / k1287_iso2 written FROM THE FETCHED BYTES (machine sha re-verified in both trees), THEN official 4 runs from the fetched-back machines: rc=0 all, stdout byte-identical sha256 9e3a61f524af7bdcf7f32a31ceb465b3a63e69e0d86ae25ccee4243f0f8d7594 = declared exactly (same cwd x2 PYTHONHASHSEED unset/1 + isolated tree env -i PYTHONHASHSEED 99 / PYTHONHASHSEED 7, ~28 s/run). counts [1200, 1050, 810, 945, 252, 832, 702, 3132, 1458, 18, 1344] total 11,743 bad 0 (D1 W-law / D2 D-law / D3 E-law / D4 A'-law / D5 A-law / D6 frontier Am+SLB2+SLB3+L / D7 published anchors: pure-c1 ladders [d odd] + D-c1 pair slices [g odd] + T-ALM six floors + C-PC/C-PB2 / D8 identities I1-I11 engine-free / D9 mex fixed-point certificates / D10 cross-engine canonical-vs-ordered / D11 K0832 single-token closed form vs both engines). Mutation battery 9/9 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80…), wlaw 544 (D1 400 + D9 144) / dlaw 792 (D2 600 + D9 192) / elaw 387 (D3 315 + D9 72) / aplaw 1215 (D4 945 + D9 270) / alaw 144 (D5 84 + D9 60) / amlaw 160 (D6 only) / identity 336 (D8 only) / mex 175 (D9 only), all rc=1 with per-gate counts matching the declaration to the point. Audit artifacts published at 16bd8d12 (audit_run1-4.out+.info, tamper 9 x 2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 54 entries)."
  - "HONEST HISTORY (failure recorded): the E-family law was first read as 'odd d -> 2 on z0/z2'; the pre-declaration WIDE census refuted exactly that reading with bad=96 (all cells odd d>=5), and the corrected table EL(z,d): d even -> 1; d=3 -> (z1 -> 0, z0/z2 -> 2); odd d>=5 -> 0 was frozen before any declaration. The wrong-law lawcheck outputs are preserved in the kit as exploration primary sources. The D9 mex fixed-point gate re-derives each law value as mex(engine child values) inside the boxes — a machine certificate that the census laws are true mex fixed points, NOT just table coincidences; tamper=mex (children restricted to the first child) yields exactly 175 bad, delta-declaring what the certificate pins."
  - "OPEN registrations (note S5): O1 census -> universal blocker diagnosis (single-layer SLB2/SLB3 + L + Am universalization + floor negative regions K1286 O1/O2/O4; K1288 target). O2 C-PC1z1-d4 c>=2 half: C-SPW z1 d=1 row census-solved ({m,(m+1)^c}@(2m+4,1) = 0, c 2..6 x m 1..12 bad 0; universal waits on O1). O3 c-direction invariance (census c<=7, no law change in c; spread-theory conjecture). O4 Am z2 single-point anomaly (m=1,h=2,s=1) -> 1 with no structural explanation (K1289 candidate). 11x11 connection: the law tables are directly usable as O(1) value-lookup for multi-c low-z pruning lattices inside the census boxes; recorded only, no verdict consumed, 11x11 UNKNOWN unchanged."
relations:
- type: extends
  target: K1286
  note: "対抗 fast-lane K1286（ペア境界スライス・border-slices pre-diag collapse）の §5 O3 が登録した『F2 spread 理論への入力』（F_d/G_d・d∈{1,2,3}・288 点 OBS）を継承し、d<=8 × 5 族 × 3 面 × c>=2 に拡張して法則表・例外構造・frontier・子恒等式を確定。重複した全称主張なし（K1286 の定理群はペア c=1 側・本項は multi-c 側）。K1286 O1/O2/O4 の床負域には非接触（K1288 以降候補・O1 blocker 診断に引用のみ）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。機体 D11 が両 engine と照合（x 2..9, z 0..3, R 1..21・1,344 点・bad 0）。m=1 行の B-exit 評価の全称化で O1 blocker の一部になる。"
- type: depends_on
  target: K1285
  note: "純 c1 ラダー [d odd]・D-c1 ペアスライス [g odd]（T-PS 再添字 g=d-1）・T-ALM 六床・C-PB2/C-PC を機体 D7 が出版アンカーとして再照合（702 点・bad 0）。multi-c web の c=1 境界列と出版定理の整合を機械確認。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282-K1286 公開 block と同一（startup sha ゲート）。engine_block.py 582c93c1… は K1282-K1286 kit と byte-identical。C-PC 帯底は T-B0′(i) の instance（D7 で照合）。"
- type: related
  target: K1284
  note: "open 登録 C-PC1z1-d4 の c>=2 半分: C-SPW の z=1, d=1 行（{m,(m+1)^c}@(2m+4,1) = 0）が c 2..6 × m 1..12 で bad=0。census 上の解決として O2 に登録（全称は O1 待ち）。"
- type: related
  target: K1286
  note: "非接触領域の明示: 本項は multi-c 値法則（conjecture）と子恒等式（代数定理）のみ。K1286 の T-PD0/T-B0/T-Z1/T-B1/T-Z2/T-B2（床負域・pre-diag 分裂・z1/z2 床の m 分裂）には触れない。O1 blocker 診断で『typical な子 mex 解析には床負域の全称化が要る』と K1286 O1/O2/O4 を引用する only。"
artifacts:
- path: research/log/2026-11-24-multic-web-f2-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 40f945b8・観測 HEAD 5b9c6231〔着手時〕/ 076e05c1〔push 直前再取得〕・K1287 空き・対抗 K1286 との非重複明記）。§1 法則表 C-SPW/D/E/A'/A・OBS-F1..F4（census 箱の正確な記述）・§2 T-RC 子恒等式 I1-I11（代数定理・証明本文）・§3 宣言前探索実績（E 族旧法則 bad=96 反例検出の honest 記録を含む）・§4 機体宣言（sha・counts 11,743・変異電池 9 走の期待値事前宣言）・§5 open 登録（O1-O4・K1288 ロードマップ・11×11 接続記録）。
- path: research/experiments/multic-web-f2-20261124/
  role: machine
  note: 実験キット一式（出版 35394ac8・成果物 16bd8d12）: README・verify_k1287.py (sha256 52e7eea7…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=8 法則)・engine_block.py (582c93c1…・K1282-K1286 kit と同一 bytes)・explore_k1287.py (stage z0|z1|z2|frontier)・output/ explore 出版走 4 組 + 公式監査成果物（audit_run1-4.out+.info・tamper 9 法則×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 54 entries）・predry/ 宣言前ローカル dryrun 3 走 + 変異 9 走。
- path: research/log/2026-11-24-multic-web-f2.md
  role: report
  note: 実行 log（宣言→キット→fetch-back 照合→公式 4 走→変異電池→成果物出版→K item・README bullet の全記録・E 族旧法則の失敗と修正の発見順を含む・受入判定・次課題）。
---

## 概要

K1286（対抗 fast-lane・ペア境界スライス）の §5 O3 が「F2 spread 理論への
入力」として登録した multi-c web を、**d ≤ 8 × 5 族（W/D/E/A'/A）×
3 面（z ∈ {0,1,2}）× c ≥ 2** に拡張し、値法則表・例外構造・frontier
（Am/SLB2/SLB3/L）・**T-RC 子恒等式 I1–I11**（族の閉性・代数定理）・
mex 不動点機械証明書を確定した。

- **C-SPW/D/E/A'/A**: 5 族の値法則。**有限全数 census で bad=0 の
  conjecture**（機体コア箱 4,257 点 + explore 広域箱。全称主張は
  しない）。C-SPW の z=1 面は例外なしの [d even] で、**K1284 open
  登録 C-PC1z1-d4 の c≥2 半分を census 上で解決**（O2 登録）。
- **T-RC I1–I11**: W/D/E/A'/A の全ての手が「同 web 族点・frontier
  点」に予算 R−1 で落ちることを multiset 等式で示す**代数定理**。
  機体 D8 が 3,132 点を engine-free で照合。
- **D9 mex 不動点**: 法則値 = mex(engine 子値) を箱内で機械証明
  （1,458 点）。census 法則が mex の不動点であること直接的担保。
- **E 族旧法則の反例検出（honest）**: 旧読み「奇 d → 2（z0/z2）」は
  広域 census で bad=96（奇 d≥5 の全 cell）として反例検出され、
  修正表（d=3 のみ例外的に 2・奇 d≥5 は 0）を宣言前に確定。

## 主張の区分（過大主張の防止）

- **定理（代数・全称・ノート §2 に証明全文）**: 恒等式 I1–I11 のみ。
  自明の multiset・予算等式で、一行で証明される。
- **conjecture（census-verified）**: C-SPW/D/E/A'/A・OBS-F1..F4。
  有限箱内で bad=0。**箱の外では未検証**。
- **機械証明書（箱内有限）**: D9 mex 不動点。全称ではない。
- **open 登録（本項で新規）**: O1 全称化 blocker 診断（SLB2/SLB3・L・
  Am の全称化 + K1286 O1/O2/O4 床負域が blocker・K1288 目標）・
  O2 C-PC1z1-d4 c≥2 半分（census 解決・全称は O1 待ち）・
  O3 c 方向不変性（census c≤7・spread 予想）・O4 Am z2 の
  (m=1,h=2,s=1) 単点異常（K1289 候補）。
- census は証明ではない: D1-D11 の 11,743 点は法則の実機照合
  （bad 0）であり、法則の全称性は主張しない。

## 公式監査（publish-then-execute・fetch-back 検証機体から走行）

- 宣言 40f945b8（観測 HEAD 5b9c6231 → push 直前再取得 076e05c1・
  K1287 空き・対抗宣言なし）→ 機体 35394ac8 → fetch-back 12 ファイル
  byte 照合（remote == local・12/12）→ 隔離 tree 2 箇所に fetch した
  bytes から機体書き出し（sha 再検証）→ 公式 4 走（同一 cwd×2
  PYTHONHASHSEED 未設定/1 + 隔離 tree×2 env -i PYTHONHASHSEED=99 /
  PYTHONHASHSEED=7）すべて rc=0・stdout byte-identical
  （sha256 9e3a61f5… = 宣言想定）。~28s/走。
- counts `[1200, 1050, 810, 945, 252, 832, 702, 3132, 1458, 18, 1344]`・
  総計 11,743 点・bad 0・engine_gate PASS・D10 cross-engine
  （canonical vs ordered）一致・D11 公刊単一トークン閉形式 vs
  両 engine 一致・D7 公刊アンカー（K1285 ラダー・T-PS・T-ALM・
  C-PB2/C-PC）整合。
- 変異電池 9/9 検出・宣言どおり（全て run 前に事前宣言）:
  engine rc=2（mutated sha 0ea47a80…）・wlaw 544（D1 400 + D9 144）・
  dlaw 792（D2 600 + D9 192）・elaw 387（D3 315 + D9 72）・
  aplaw 1215（D4 945 + D9 270）・alaw 144（D5 84 + D9 60）・
  amlaw 160（D6 のみ）・identity 336（D8 のみ）・mex 175（D9 のみ）。
- 成果物出版 16bd8d12（audit_run1-4.out+.info・tamper 9 法則×2・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 54 entries）。

## 11×11・規約への接続

- verdict 不消費・11×11 巨大探索の UNKNOWN は不変・Part DF/DG/DL/DH
  レーン（b28/b31 solver 系 bookkeeping）と対象直交・非接触。
- 法則表は census 箱内で multi-c 低 z 面の枝刈り格子の評価表として
  O(1) 即値参照可能。巨大レーンへの接続は記録のみ（採用判断は
  巨大レーンオーナー）。

## 次課題（単一オーナー候補）

1. **K1288 目標（O1）**: SLB2/SLB3/L の typed 全称証明
   （C 子は SLB 自身・A 子は L/Am 族で web 閉包するかの判定）。
   床負域（K1286 O1/O2/O4）との合流で C-SP* の全称化を狙う。
2. **K1289 候補（O4）**: Am z2 の (m=1,h=2,s=1) 単点異常の構造説明。
3. **F3 系（O2/O3）**: C-PC1z1-d4 c≥2 半分の全称化・c 方向不変性
   （spread 理論・c 方向帰納）の定式化。
