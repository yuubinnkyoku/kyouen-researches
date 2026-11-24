---
id: K1290
title: "pre-diag 双生児 z5/z6 の全称確定: T-PDT5/T-BDT5・T-PDT6/T-BDT6 (R 例外層 2·[R odd] の厚み 6・偶数 cell は z6 で主則と一致)・L-BU5G/L-BU6G・sharpened C-PSF′ (w=0..6 で全称確定・z7/z8 は OBS 登録) — K1289 O8 完全解決・69,553 点公式監査 bad 0・4 走 byte-identical"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins extended to plane 5 and plane 6, universal. Pair positions H(R;(m,m+g);z) on the pre-diagonal band k<=0 and beds b_z(j) := H(2m+j;(m,m);z), j<=0, with delta := R-2m. The exception layers are R-CONSTANT values claimed in the same packet (K1288's innovation, third generation): T-PDT5 (z5 band): H = 2*[R odd] (R<6, thickness L(5)=2*ceil(5/2)=6, the even cells genuinely override the main law g1(delta-4)=1); g1(delta-4) (R>=6). T-BDT5 (z5 bed): 2*[R odd] (R<6); g1(j-4) (R>=6). T-PDT6 (z6 band): 2*[R odd] (R<6, of which the even cells already coincide with the main law f0(delta-6)=0); f0(delta-6) (R>=6). T-BDT6 (z6 bed): 2*[R odd] (R<6); f0(j-6) (R>=6). None of the values depend on m or g. New uniformity lemmas from the K0832 closed form: L-BU5G: v(w,6,t) = 2*[t odd] (t<6); g1(t-4) (6<=t<=w) — the single token at plane 6 inherits the plane-5 law; L-BU6G: v(w,7,t) = 2*[t odd] (t<6); f0(t-6) (6<=t<=w) — plane-6 law; both machine-checked vs closed form AND both engines for w<=30 (D9(a)/(b))."
  - "THE PROOFS (typed child mex, hand-written in the declaration note SS2.0-SS2.6, well-founded single R strong induction over the joint packet {T-PDT5, T-BDT5, T-PDT6, T-BDT6}): all engine children sit at budget R-1; children are classified as fall (m>=2, delta+1) / B (m=1 -> single token w=g+1 at plane z+1, valued by the K0832 closed form through L-BU5G/L-BU6G without induction) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1) / C (1 XOR, plane z-1, same budget R-1). Cross-plane reads: z5's C child reads T-PDT4 (K1289, unconditional all-R); z6's C child reads T-PDT5 (same packet, budget R-1). The B-exit reproduces the fall-child table on plane 5 (g1(delta-3)) and plane 6 (f0(delta-5)); the corner child equals the compress child. Mex closure tables (note SS2.1-SS2.4): for z5 the option set {g1(delta-1), g1(delta-5), 1 XOR f0(delta-5)} closes to g1(delta-4) for all delta parities, with nucleation columns delta=5 ({0,1}->2=g1(1)) and the C-core delta=6 ({1,2,3}->0=g1(2)); for z6 {f0(delta-5), f0(delta-7), 1 XOR g1(delta-5)} closes to f0(delta-6) with nucleation columns delta=7 ({1,0}->2=f0(1)), the C-core delta=6 ({2,1,3}->0=f0(0)) and the compress-core delta=8 ({0,2}->1=f0(2)=1 main-law value at a nucleation cell). The exception layers close on constant child reads with the W-INDEPENDENT mechanism (K1289 SS2.1, now third instance): R=1 {0,1}->2; R=2 {2,3}->0; R=3 {0,1}->2; R=4 {2,3}->0; R=5 {0,1}->2 — the same mex{0,1}=2/mex{2,3}=0 pair as z3 in spite of the thickness growing to 6; the seam R=6 closes with {0,2}->1 (z5) / {2,3}->0 (z6). Beds: fall (pair gap 1, same plane) + C (plane-1 bed) + B (m=1, w=1 edge values {0,2}); single-value mex tables close by j parity (SS2.2/SS2.4)."
  - "SUBSUMPTION: C1 RESOLVES K1289 O8 — the z5/z6 far-observation planes of the K1289 D11 are now the main law, universally, exception layers included. C2 EXTENDS the sharpened plane-shift family C-PSF': H(R;(m,m+g);w) = 2*[R odd] for R < 2*ceil(w/2); T_w(delta - 2*floor(w/2)) for R >= 2*ceil(w/2), with T_w = g1 (w odd) / f0 (w even); w=0 (K1286), w=1,2 (K1288), w=3,4 (K1289), w=5,6 (this item) are now all PROVED; the layer-thickness law L(w) = 2*ceil(w/2) holds universally for w<=6 and the OBS extends it through w=10 (new dedup sweep, 320 (R,delta) cells x planes 7..10, mixed 0, cpsf-bad 0). C3 completes SEVEN branches of the B-exit uniformity family: single token at plane z+1 inherits the plane-z law (L-BU0 plane-0 ... L-BU6G plane-6); the next branches (token planes 8/9, i.e. L-BU7G/L-BU8G) are discovered and registered as OBS (w<=40, engine == closed form == plane-7/8 law)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 88dd5370 (observed HEAD at start 68483d7d -> pre-push refetch 1e1578a2; intervening commits were Part DH takeover-2 / Part DM drive-1 adoption-lane bookkeeping, non-contact; K1290 vacancy verified: latest K item = K1289 at 518c4366, no competing declaration), then kit 048ae37c (verify_k1290.py sha256 b86cdaf9..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282..K1289; engine_block.py standalone 582c93c1..., byte-identical to the K1282-K1289 kits; explore_k1290.py + explore2_k1290.py with outputs; predry/ 4 byte-identical runs), fetch-back of the 15 published kit files (15/15 sha256 full match), THEN official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 e5359335... = predry = declared (fetchback cwd x2 PYTHONHASHSEED random/1 + isolated trees isoA/isoB built from fetch bytes, env -i PYTHONHASHSEED 99/7, ~7.3s/run). counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 30051, 1516, 15304] TOTAL 69,553 bad 0 (D1/D3 z5/z6 band censuses m<=14 g<=25 k>=-30; D2/D4 bed censuses m<=18 j in [-36..0]; D5-D8 typed slices/beds where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine; D9 anchors: L-BU5G/L-BU6G w<=30 vs closed form + engine 493+493, K1289 T-PDT3/T-BDT3/T-PDT4/T-BDT4 re-verification 4,690, K1288 T-PDT1/2 + T-BDT1/2 re-verification 4,690, K1286 T-PD0/T-B0 re-verification 2,345, sharpened C-PSF' identity sweep over the PROVED planes w=0..6 (cpsf == engine == plane claim) 16,415, T-TWIN identity 201, closed form vs both engines (x<=16, z in 2..7) 720, B-exit w=1 edges 4; D10 cross-engine canonical-vs-ordered z5/z6 1,516; D11 OBS: z7/z8 band 4,500x2 + beds 120x2 + far rows 216x2 + low-R hist probes {0:283,2:280}x2 (R<8) + L-BU7G/L-BU8G plane-token discovery sweeps (z=8,9, w<=30) 493x2 + dedup (R,delta) sweep z=0..10 3,520). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin; tamper_engine.info is 0 bytes by design), z5s D1 bad 8928 / z5b D2 bad 360 / z6s D3 bad 8928 / z6b D4 bad 360, all rc=1. Audit artifacts published at 3a62c705 (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries) with fetch-back verification: 18/18 non-empty sha256 match + tamper_engine.out sha match + the 0-byte tamper_engine.info verified by remote size 0."
relations:
- type: extends
  target: K1289
  note: "K1289 (pre-diag twins z3/z4) の O8 (T-PDT5/T-BDT5/T-PDT6/T-BDT6) を本項の 4 定理で完全解決し、sharpened C-PSF′ の全称実例化を w=5,6 に拡張。z3/z4 アンカー (T-PDT3/T-PDT4/T-BDT3/T-BDT4) は z5 の C 子として帰納で利用し D9(c) が再照合。z5 の typed 構文は K1288/K1289 の R 例外層込み packet 構文の直接拡張 (第 3 世代)。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU5G/L-BU6G (本項の新規補題・w≤30 で機体 D9(a)/(b) が閉形式×両 engine と照合) として fall 子の表を直接再生。床 m=1 の w=1 edge {0,2} も閉形式から (D9(i))。"
- type: depends_on
  target: K1286
  note: "z0 アンカー T-PD0/T-B0 (f0) を D9(e) が再照合 (f0 は本項の全 mex 表の基礎関数)。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1289 公開 block と同一 (startup sha ゲート)。engine_block.py 582c93c1… は K1282–K1289 kit と byte-identical。"
- type: related
  target: K1287
  note: "領域直交 (multi-c web F2 内面 k>0 vs ペア pre-diag k≤0)。K1287 O1 残部 ((i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化) は本項でも非着手 (宣言ノート §5 O13)。"
- type: related
  target: K1288
  note: "L-BUzG B-exit 均一性族の z1/z2 枝 (L-BU1G/L-BU2G) と z1/z2 アンカーを D9(d) が再照合。本項で族は 7 枝に出揃った。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z5z6-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 88dd5370・観測 HEAD 68483d7d〔着手時〕/ 1e1578a2〔push 直前再取得〕・K1290 空き・対抗宣言なし)。§1 主張一式 (T-PDT5/T-BDT5/T-PDT6/T-BDT6・L-BU5G/L-BU6G・C1 O8 解決・C2 sharpened C-PSF′ w=5,6・C3 L-BUzG 族 7 枝)・§2 typed 証明全文 (§2.0 子分類・§2.1–§2.2 z5 band/bed の mex 場合表・§2.3–§2.4 z6 band/bed・§2.5 閉形式からの補題導出・§2.6 well-founded 性・§2.7 honest 記述)・§3 宣言前探索 (X1–X7/Y1–Y8)・§4 機体宣言 (counts 69,553・変異電池期待値の事前宣言)・§5 open 登録 (O9′/O10′/O11/O12/O13)・§6 主張の区別。
- path: research/experiments/prediag-twins-z5z6-20261124/
  role: machine
  note: 実験キット一式 (出版 048ae37c・監査成果物出版 3a62c705): README・verify_k1290.py (sha256 b86cdaf9…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z5s/z5b/z6s/z6b)・engine_block.py (582c93c1…・K1282–K1289 kit と同一 bytes)・explore_k1290.py+.out・explore2_k1290.py+.out (宣言前 discovery + wide census + z7/z8 OBS + L-BU7G/L-BU8G 発現)・predry/ 宣言前 4 走 (byte-identical sha e5359335…)、公式監査成果物 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries)。
- path: research/log/2026-11-24-prediag-twins-z5z6.md
  role: report
  note: 実行 log (宣言→kit→fetch-back 15/15→公式 4 走→変異電池→成果物出版 3a62c705 と fetch-back 18/18→K item・README bullet の全記録・受入判定・次課題)。
---

## 概要

K1289（pre-diag 双生児 z3/z4）が open 登録した O8（z5/z6 typed 全称）を
解決し、双生児定理を平面 5・6 まで拡張した。

- **T-PDT5/T-BDT5**: z5 バンド・床は **2·[R odd] (R < 6) / g1(δ−4) (R ≥ 6)**
  （床は δ→j）。例外層は厚み 6 の R 定数層（偶数 cell は主則 1 を上書き）。
- **T-PDT6/T-BDT6**: z6 は **2·[R odd] (R < 6) / f0(δ−6) (R ≥ 6)**
  （偶数例外 cell R∈{0,2,4} は主則 0 と値が一致し層の実効は R∈{1,3,5}）。
- **L-BU5G/L-BU6G**: 単一 Token @ 平面 6/7 は plane-5/6 則を継承
  （K0832 閉形式から導出・w ≤ 30 で閉形式×両 engine 照合 bad 0）。
  B-exit 均一性族は L-BU0・L-BU1G/L-BU2G・L-BU3G/L-BU4G（既刊）+ 本項で
  7 枝が出揃った（token 平面 8/9 の L-BU7G/L-BU8G 相当は w ≤ 40 OBS 発見）。
- **C1（O8 解決）**: K1289 D11 が OBS として観測していた z5/z6 が全称定理化。
- **C2（sharpened C-PSF′）**: 全平面の統一形式
  H = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌋)。
  w=0（K1286）・w=1,2（K1288）・w=3,4（K1289）・w=5,6（本項）で全称証明済み。
  **w∈{7,8}は OBS（band 4,500×2・beds 120×2・far-row 216×2 bad 0・low-R
  hist {0:283,2:280}）に加え、dedup sweep で w=9,10 まで 320 cell × 11 面
  mixed 0・cpsf bad 0 に拡張**（全称主張なし）。
- 値はいずれも m・g を経由しない。

## 主張の区分（過大主張の防止）

- **定理（全称・宣言ノート §2 に手証明全文）**: T-PDT5・T-BDT5・T-PDT6・
  T-BDT6・L-BU5G・L-BU6G・C1・C3。well-founded な単一 R 強帰納
  （全子が予算 R−1・面間参照は下位予算のみ〔z6 の C 子は packet 内〕・
  B 子は閉形式で帰納外）。基底 R=0 = mex ∅ = 0。例外層 R<6 の閉鎖は
  mex{0,1}=2 / mex{2,3}=0 の w 非依存機構（z3 で確立・第 3 世代で再確認）。
- **corollary（既刊の言い換え・全称）**: C2 の w ≤ 6 部分。
  C-PSF′ の一般 w（層厚 L(w) の帰納）は**予想**（O9′・全称主張なし）。
- **有限観測（OBS・全称主張なし）**: z7/z8 の band・beds・far-row・low-R hist
  （D11・explore2 Y3–Y5）、L-BU7G/L-BU8G 発現（Y7・D11 z=8,9 sweep）、
  dedup (R,δ) sweep z=0..10。
- census 69,553 点は定理の実機照合であり、全称性の主張ではない。

## 11×11・規約への接続

- verdict 不消費・11×11 の UNKNOWN は不変・Part DH/DM/DN 等 adoption
  レーンと非接触。
- T-PD0（K1286）+ K1288 + K1289 + 本項で、ペア面 z∈{0..6} の対角下全域
  k ≤ 0 が R 例外層込みで O(1) 即値評価可能（band は (R,δ) 2 変数・床は 1 変数）。
  枝刈り格子の境界側拡張として巨大探索レーンへ記録（採用判断はオーナー）。

## 次課題（単一オーナー候補）

1. **T-PDT7/T-BDT7・T-PDT8/T-BDT8（O9′）**: z7/z8 の typed 全称証明。
   C 子は本項の z5/z6 定理（全 R・例外層込み）を参照するため同一構文で
   証明可能な見通し。障壁は層厚 L(7)=L(8)=8 の層定数管理
   （子に現れる層定数が w−1 面の層域 R<6 を跨ぐ）。sharpened C-PSF′ の
   w=8 まで全称化。
2. **C-PSF′ の w 帰納（O9′）**: 主則域の mex 恒等式は双子恒等式で閉じる
   見込み。主要障壁は例外層の厚み L(w)=2⌈w/2⌉ の帰納（層の子は面上
   の層定数を R−1 パリティで読む。本項で w=3,5 の奇数世代・w=4,6 の
   偶数世代の 2 世代ペアが確定し、一般 w の同時管理の見取りが得られた）。
3. **L-BUzG 族の全称形（O10′）**: 閉形式の region 計算で一般 w へ
   （L-BU7G/L-BU8G の w ≤ 40 OBS が入力）。
4. **K1287 O1 残部（K1291+ 候補）**: (i) SLB2/SLB3 単一層族・(ii) L/Am
   frontier の全称化（本項非着手）。
