---
id: K1288
title: "pre-diag 双生児バンド z1/z2 の全称確定: T-PDT1/T-BDT1（f0 の偶奇双生児 g1・R∈{0,1} 例外層込み typed 全称証明）+ T-PDT2/T-BDT2（δ−2 シフト・R=1 例外層）+ 系 C1–C4（K1286 open O1/O2/O4 完全解決・K1287 O1 blocker の床負域〔(iii)〕を供給）・30,440 点公式監査 bad 0・4 走 byte-identical・z3/z4 シフト族 OBS と C-PSF 予想登録（O5/O6/O7）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins, universal. Pair positions H(R;(m,m+g);z) with diagonal coordinate k := R-2m-g and delta coordinate delta := R-2m; target = the FULL pre-diagonal band k<=0 (the diagonal leg and everything below it, 0<=R<=2m+g) and the beds b_z(j) := H(2m+j;(m,m);z), j<=0. New twin of the published f0 (K1286): g1(d) := 2 at d=1; [d even] at d<=0; [d odd] at d>=2 (T-TWIN: g1 = 1 XOR f0 off d=1, g1(1)=f0(1)=2). FOUR UNIVERSAL THEOREMS (all m>=1, g>=1, all valid cells; values depend on NEITHER m NOR g — a one-dimensional collapse in delta): T-PDT1 (z1 band): H(R;(m,m+g);1) = 0 (R=0); 2 (R=1); g1(delta) (R>=2) — the FULL k<=0 region including the k<=-2 part K1286 T-Z1 could not reduce. T-BDT1 (z1 bed): b1(j) = 0 (R=0); 2 (R=1); g1(j) (R>=2). T-PDT2 (z2 band): H = 2 (R=1); f0(delta-2) otherwise (R=0 included since f0(-2m-2)=0). T-BDT2 (z2 bed): b2(j) = 2 (R=1); f0(j-2) otherwise. The delta-2 SHIFT is the z2 face of the structure law (T_w(delta - 2*floor(w/2)))."
  - "THE PROOFS (typed child mex, hand-written in the declaration note S2, well-founded single R-strong-induction): children fall (m>=2, delta+1) / B (m=1 -> single token w=g+1, value from the K0832 closed form) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1<=0; corner child = compress child by the same delta-1 and budget) / C (value 1 XOR, z->z-1), ALL at budget R-1; cross-plane references z2 -> z1 -> z0 are lower-budget only. THE KEY INNOVATION: the exception layers (z1: R=0 -> 0, R=1 -> 2; z2: R=1 -> 2) are claimed VALUES in the same packet, so child reads at R-1 in {0,1} also use the packet laws — everything K1286 misread as m-splits (its O1/O2/O4) turns out to be R-case layers of the child analysis. B-uniformity lemmas from the K0832 single-token closed form make the m=1 B-exit reproduce the fall child table without induction: L-BU1G (z1 face): v(w,2,t) = 0 (t=0); 2 (t=1); g1(t) (2<=t<=w), all w>=2. L-BU2G (z2 face): v(w,3,t) = 0 (t=0); 2 (t=1); f0(t-2) (2<=t<=w). The mex tables close by delta-parity: z1 R>=3 children {g1(delta+1), g1(delta-1), 1 XOR f0(delta-1)} = {g1(delta+1), g1(delta-1), g1(delta-1)} by T-TWIN (third child 3 only at delta=2, mex 0 = g1(2)); z2 R>=3 children reduce to {f0(d-1), f0(d-3)} at d=delta-2 which is exactly the K1286 8-row table, plus the delta=2 column {2,1,3} -> 0 = f0(0). Base R=0: mex of the empty set = 0 on all four theorems."
  - "SUBSUMPTION AND OPEN RESOLUTION (declaration note S1 C1-C4): C1 K1286 T-Z1 slices k in {-1,0} = g1(g+k) (always R>=2 there, never in the exception layer); T-Z1's k=1/z1-interior stays K1286-side. C2 T-B1 j in {-1,0} inside T-BDT1; the K1286 b1(-1) m-split IS the R=1 layer (m=1 -> R=1 -> 2; m>=2 -> R>=3 -> g1(-1)=0); b1(1)=0 (j>0) stays K1286/K1283-side. C3 T-Z2 k=0 = f0(g-2); T-B2 b2(0)=f0(-2)=0; k in {1,2}/b2(1),b2(2) stay K1286-side. C4 RESOLVES K1286 O1: the z1-k(-2) m=1,g=1 core (value 2) is the R=1 layer (R=2m+g+k=1) and the m>=2 rows 0,1,2,[g odd] are g1(g-2) regenerations — the 'two-stage law / small-m bed family' hypothesis was unnecessary, the whole band is a single twin law with an R-exception layer; O2: the z2-k(-1) m-independent candidate row (0,1,0,2,[g odd] g>=5) = f0(g-3); the z2-k(-2) g=5 spike (value 2) = f0(1)=2 and the m=1/g=1 splits are the R=1 layer; O4: the z1/z2 bed negative-j m-splits are fully explained by the R in {0,1} layers of T-BDT1/T-BDT2 (m-splits are just how the exception layers look). K1286 O3 (F2 spread web) was taken by K1287 (untouched here). After this package, the ONLY undetermined pair-z1/z2 territory is the interior k>=1."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 787f635c (observed HEAD at start 35394ac8, pre-push refetch 3074f6d9; intervening commits all K1287-lane + Part DH bookkeeping, non-contact; K1288 vacancy verified against the items dir commits — latest K item = K1287 at f16808ae, no competing declaration), then kit 3321c63a (verify_k1288.py sha256 25c6bdc7f0207b48de0c90e9d67a14b9001f0a09c1c79c710e86b0fb734f2fb5, startup sha gate on the embedded engine block, pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 = the SAME published block as K1138/K1282..K1287; engine_block.py standalone 582c93c1…, byte-identical to the K1282-K1287 kits; explore_k1288.py + explore2_k1288.py with outputs + predry/ 4 deterministic runs), fetch-back of 15 published files (remote == local, sha256 15/15 full match), THEN official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 6d19ef62ecb6cd4b6342569758f5f29e1ed16c9614e0061fe557659906f54d04 = declared exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated trees env -i PYTHONHASHSEED 99/7, ~1.4-1.5 s/run). counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 5720, 1318, 720] total 30,440 bad 0 (D1/D3 z1/z2 band censuses m<=14 g<=25 all k<=0, D1 split R0:206 / R1:218 / R>=2 delta<=0:3954 / R>=2 delta>0:4550; D2/D4 bed censuses m<=18 j in [-36..0]; D5-D8 typed slices where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine (m<=10, g<=14, k>=-14 slices; beds m<=10, j>=-16); D9 uniformity + published anchors: L-BU0/L-BU1G/L-BU2G (w<=30), T-PD0/T-B0 re-verification, K1286 table identities Z1(k in {-1,0})=g1(g+k) / Z2(k=0)=f0(g-2) / beds, single-token closed form vs both engines, T-TWIN algebraic identity; D10 cross-engine canonical-vs-ordered; D11 OBS registrations z3far/z4far 216+216 + z3 low-R exception probe 288). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80… != pin; the tamper_engine.info timing file is 0 bytes by design — the engine gate aborts before writing timing info), z1s D1 bad 8928 / z1b D2 bad 360 / z2s D3 bad 8928 / z2b D4 bad 360, all rc=1. Audit artifacts published at 27c71274 (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries), fetch-back 20/20 sha256 match (the empty tamper_engine.info verified byte-exact by the remote dir listing size 0 + the MANIFEST empty-sha entry e3b0c442…, since the MCP connector cannot return empty-file contents as text)."
  - "OPEN REGISTRATIONS (note S5; finite observation ONLY, no universal claims): O5 z3/z4 exception small-R layers unresolved: z3 = g1(delta-2) and z4 = f0(delta-4) hold with bad 0 on the wide m 3..12, g<=25, k<=0 boxes at R>=4 (6,250 cells each) and on the m=12 far rows (k in [-12..-1], g in [1..18], 216 points each), but the R in {2,3} rows produce delta-local value mixing (z3: even delta {0,1} / odd delta {0,2}; z4: odd delta {1,2}) and the low-R probe (R<=3, m 1..6, g<=12, 288 valid cells) sees only {0,1,2} (hist 0:144 / 2:144) — a typed z3 proof will need the T-PDT2 exception-layer laws through the z2->z3 C-reference. O6 C-PSF (plane-shift family CONJECTURE): the z_w pre-diag band k<=0 collapses to T_w(delta - 2*floor(w/2)) with T_w = g1 (w odd) / f0 (w even), plus an exception small-R layer; z1 (w=1, g1(delta)) and z2 (w=2, f0(delta-2)) are PROVED here, z3 (g1(delta-2)) / z4 (f0(delta-4)) are census-observed only; the general shape of the layer thickness (R>=2 for z1, R=1 for z2, R in {2,3} contamination for z3, R in {0..3} for z4) is undetermined. O7 next single-owner candidates: T-PDT3/T-BDT3 (z3) and T-PDT4/T-BDT4 (z4) typed universal proofs; the C-PSF induction in w; connection to the K1287 T-RC/F2 territory (interior side k>0 of the z>=3 planes; non-contact). NUMBERING NOTE (honest): the K1287 lane's own roadmap NAMED its O1 target 'K1288 target' — that is roadmap naming only, no commit had acquired a K item number for the SLB2/SLB3/L/Am territory; this K1288 takes the pre-diag twins territory (K1286 O1/O2/O4) and ADDITIONALLY SUPPLIES item (iii) (floor negative regions) of the K1287 O1 blocker diagnosis; the remaining blockers (i) single-layer SLB2/SLB3 and (ii) L/Am universalization stay open (K1289+ candidates). 11x11 connection: with T-PD0 (K1286) and this package, the ENTIRE pre-diagonal region k<=0 of the pair z0/z1/z2 planes is O(1) instantiable — recorded as a boundary-side extension of the pruning lattice for the giant-search lane; no verdict consumed, 11x11 UNKNOWN unchanged."
relations:
- type: extends
  target: K1286
  note: "K1286（境界スライス・T-PD0/T-B0/T-Z1/T-B1/T-Z2/T-B2）の open O1/O2/O4（pre-diag バンド k≤−2・z2 pre-diag・床負 j 側の m 分裂）を本項の 4 定理で完全解決し、T-Z1 の k∈{−1,0}・T-B1 の j∈{−1,0}・T-Z2 の k=0・T-B2 の b2(0) を R 例外層込みの双生児則に包含（申立 C1–C3・機体 D9(f) が表同一性を照合）。z0 アンカー（T-PD0/T-B0）は帰納の子読みで使用し D9(d)(e) が再照合。内面 k≥1 は K1286 側に残存（主張の重複なし）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU1G/L-BU2G（本項の新規補題・w≤30 で機体 D9(b)(c) が照合）として fall 子の表を直接再生。D9(g) が閉形式 vs 両 engine を照合。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1287 公開 block と同一（startup sha ゲート）。engine_block.py 582c93c1… は K1282–K1287 kit と byte-identical。"
- type: related
  target: K1287
  note: "領域直交（multi-c web F2 vs ペア pre-diag z1/z2）。K1287 O3（F2 spread）は同 lane 取得済み・本項非接触。本項が K1286 O1/O2/O4 を解決したことで K1287 O1 blocker 診断の (iii) 床負域が供給され、C-SP* 5 族全称化の残る blocker は (i) SLB2/SLB3 単一層族と (ii) L/Am frontier の全称化のみになった（K1289+ 候補）。本項と K1287 の targeted な子 mex 構文は同一 R 強帰納形式で互いに再利用可能。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z1z2-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 787f635c・観測 HEAD 35394ac8〔着手時〕/ 3074f6d9〔push 直前再取得〕・K1288 空き・対抗宣言なし）。§1 主張一式（T-TWIN・4 定理・C1–C4・K1286 open 解決登録・範囲の正確な記述）・§2 typed 証明全文（§2.0 型付き子解析と L-BU1G/L-BU2G・§2.1–§2.4 の mex case 表・§2.5 well-founded 性）・§3 宣言前探索実績（E1–E5・z3/z4 OBS）・§4 機体宣言（sha・counts 30,440・変異電池 5 走の期待値事前宣言）・§5 open 登録（O5/O6/O7・C-PSF・11×11 接続）・Honest 記録（D9(i) b1ov 演算子優先順位バグの宣言前修正）。
- path: research/experiments/prediag-twins-z1z2-20261124/
  role: machine
  note: 実験キット一式（出版 3321c63a・監査成果物出版 27c71274）: README・verify_k1288.py (sha256 25c6bdc7…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z1s/z1b/z2s/z2b)・engine_block.py (582c93c1…・K1282–K1287 kit と同一 bytes)・explore_k1288.py+.out・explore2_k1288.py+.out（宣言前広域照合 39,160×2+1,350+6,080 点 bad 0・z3/z4 OBS box）・predry/ 宣言前 4 走、公式監査成果物（audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）。
- path: research/log/2026-11-24-prediag-twins-z1z2.md
  role: report
  note: 実行 log（宣言→キット→fetch-back 15/15→公式 4 走→変異電池→監査成果物出版 27c71274 と fetch-back 20/20→K item・README bullet の全記録・受入判定・§2.2 推敲文言の honest 記録・空ファイル照合の技法記録・次課題）。
---

## 概要

K1286（境界スライス）が open 登録した O1/O2/O4（z1/z2 の pre-diag バンド
k ≤ −2 と床負 j 側の未確定・m 分裂）を、**f0 の偶奇双生児 g1** を導入して
例外小 R 層込みの typed 全称証明で完全解決した。

- **T-TWIN**: g1(d) = 1 ⊕ f0(d)（d ≠ 1）、g1(1) = f0(1) = 2。
  双生児は f0 の 0/1 領域を反転させ、例外値 2 を保存する。
- **T-PDT1/T-BDT1**: z1 バンド全域（k ≤ 0）と床は
  **0 (R=0); 2 (R=1); g1(δ) (R≥2)** / **0; 2; g1(j)**。
  K1286 T-Z1 が諦めた k ≤ −2 を含む全域が、R∈{0,1} 例外層付きの
  双生児 δ 一次元に落ちる。値は m も g も経由しない。
- **T-PDT2/T-BDT2**: z2 バンドと床は
  **2 (R=1); f0(δ−2) (他)** / **2 (R=1); f0(j−2) (他)**。
  δ−2 シフト・例外 1 層。
- **C1–C4**: K1286 の境界スライス表を包含し、O1（z1-k(−2) 核は
  2 段構え法則でなく R=1 例外層）・O2（z2-k(−1) 候補行 = f0(g−3)・
  g=5 突起 = f0(1)=2・分裂 = R=1 層）・O4（床の m 分裂 = 例外層の
  見え方）を解決登録。K1286 が m 分裂と誤認した現象は、子も
  含めた R の場合分けだった。
- **C-PSF 予想（O6・全称未証明）**: z_w バンド = T_w(δ − 2⌊w/2⌋)
  （T_w = g1〔w 奇数〕/ f0〔w 偶数〕）+ 例外小 R 層。z1/z2 は本項で
  全称証明、z3 = g1(δ−2)・z4 = f0(δ−4) は R≥4 広 box（各 6,250 cell）
  で bad 0 の OBS（O5 として例外層は未解決登録）。

## 主張の区分（過大主張の防止）

- **定理（全称・ノート §2 に手証明全文）**: T-TWIN・T-PDT1・T-BDT1・
  T-PDT2・T-BDT2・包含 C1–C3。well-founded な単一 R 強帰納
  （全子が予算 R−1・面間参照は下位予算のみ・B 子は K0832 閉形式から
  L-BU1G/L-BU2G で帰納外の直接計算）。
- **typed 電池（D5–D8・有限機械照合）**: 申立テーブル**のみ**から子を
  構成し mex を主張値と engine 値の双方と照合。**証明の算術の有限
  照合であって証明の代替ではない**。
- **有限観測（OBS・全称主張なし）**: z3/z4 の R≥4 box 一致・far 行・
  z3 例外層 probe。O5 に open 登録。
- **予想（CONJECTURE）**: C-PSF（O6）。O7 に次候補を登録。
- census 点数（D1–D11 の 30,440 点）は定理の実機照合であり、
  全称性の主張ではない。

## 公式監査（publish-then-execute・fetch-back 検証機体から走行）

- 宣言 787f635c（観測 HEAD 35394ac8 → push 直前再取得 3074f6d9・
  K1288 空き・対抗宣言なし・並走 K1287 lane/Part DH と非接触）→
  機体 3321c63a（15 ファイル）→ fetch-back sha256 15/15 byte 一致 →
  公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree×2
  env -i PYTHONHASHSEED=99/7・fetch-back 検証済み bytes から）
  すべて rc=0・stdout byte-identical
  （sha256 6d19ef62… = 宣言値）・~1.4–1.5s/走。
- counts `[8928, 360, 8928, 360, 1939, 114, 1939, 114, 5720, 1318,
  720]`・総計 30,440 点・bad 0・engine_gate PASS・D10 cross-engine
  （canonical vs ordered）一致・D9 公刊アンカー（T-PD0/T-B0・
  K1286 表同一性・単一トークン閉形式）整合。
- 変異電池 5/5 検出・宣言どおり（全て run 前に事前宣言）:
  engine rc=2（mutated sha 0ea47a80… ≠ pin・info は設計どおり
  0 バイト）・z1s D1 8928・z1b D2 360・z2s D3 8928・z2b D4 360
  （全 rc=1）。
- 成果物出版 27c71274（audit_run1-4.out+.info・tamper 5 種×2・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）・
  fetch-back 20/20 sha256 一致（空ファイル tamper_engine.info は
  遠隔 size 0 一覧 + MANIFEST の empty-sha で byte 照合）。

## 11×11・規約への接続

- verdict 不消費・11×11 の UNKNOWN は不変・Part DH 等 单独レーンと非接触。
- T-PD0（K1286）+ 本項でペア z0/z1/z2 面の対角下全域 k ≤ 0 が
  O(1) 即値評価可能。枝刈り格子の境界側拡張として巨大レーンへ
  記録（採用判断は巨大レーンオーナー）。

## 次課題（単一オーナー候補）

1. **T-PDT3/T-BDT3（z3 面・O5/O7）**: R∈{2,3} 例外層の確定込みの
   typed 全称証明。C 子は T-PDT2 例外層込み法則を参照
   （本項の構文の再利用）。
2. **T-PDT4/T-BDT4（z4 面）**: 同様。
3. **C-PSF の w 帰納（O6）**: 例外層の厚みの一般形
   （z1: R≥2 / z2: R=1 / z3: R∈{2,3} 汚染 / z4: R∈{0..3}）の定式化。
4. **K1287 O1 との合流（K1289+ 候補）**: SLB2/SLB3 単一層族と
   L/Am frontier の全称化（床負域〔(iii)〕は本項で供給済み）で
   C-SP* 5 族の全称化。
