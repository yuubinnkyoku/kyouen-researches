---
id: K1289
title: "pre-diag 双生児 z3/z4 の全称確定: T-PDT3/T-BDT3・T-PDT4/T-BDT4 (R 例外層 2·[R odd] の厚み 4 / 実効 {1,3})・L-BU3G/L-BU4G・sharpened C-PSF′ (w=0..4 で全称確定・z5/z6 は OBS 登録) — K1288 O5 完全解決・55,159 点公式監査 bad 0・4 走 byte-identical"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins extended to plane 3 and plane 4, universal. Pair positions H(R;(m,m+g);z) on the pre-diagonal band k<=0 and beds b_z(j) := H(2m+j;(m,m);z), j<=0, with delta := R-2m. The exception layers are R-CONSTANT values claimed in the same packet (K1288's key innovation, extended): T-PDT3 (z3 band): H = 2*[R odd] (R<=3, thickness 4); g1(delta-2) (R>=4). T-BDT3 (z3 bed): 2*[R odd] (R<=3); g1(j-2) (R>=4). T-PDT4 (z4 band): 2*[R odd] (R<4, of which the even cells R=0,2 already coincide with the main law); f0(delta-4) (R>=4). T-BDT4 (z4 bed): 2*[R odd] (R<4); f0(j-4) (R>=4). None of the values depend on m or g. New uniformity lemmas from the K0832 closed form: L-BU3G: v(w,4,t) = 2*[t odd] (t<=3); g1(t-2) (4<=t<=w) — the single token at plane 4 inherits the plane-3 law; L-BU4G: v(w,5,t) = 2*[t odd] (t<4); f0(t-4) (4<=t<=w) — plane-4 law; both machine-checked vs closed form AND both engines for w<=30 (D9(a)/(b))."
  - "THE PROOFS (typed child mex, hand-written in the declaration note SS2.0-SS2.6, well-founded single R strong induction over the joint packet {T-PDT3, T-BDT3, T-PDT4, T-BDT4}): all engine children sit at budget R-1; children are classified as fall (m>=2, delta+1) / B (m=1 -> single token w=g+1 at plane z+1, valued by the K0832 closed form through L-BU3G/L-BU4G without induction) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1) / C (1 XOR, plane z-1, same budget R-1). Cross-plane reads: z3's C child reads T-PDT2 (K1288, unconditional all-R); z4's C child reads T-PDT3 (same packet, budget R-1). The B-exit reproduces the fall-child table on plane 3 (g1(delta-1)) and plane 4 (f0(delta-3)); the corner child equals the compress child. Mex closure tables (note SS2.1-SS2.4): for z3 the option set {g1(delta-1), g1(delta-3), 1 XOR f0(delta-3)} has mex g1(delta-2) for all delta parities, with nucleation columns delta=3 ({0,1}->2=g1(1)) and delta=4 ({1,2,3}->0=g1(2)); for z4 {f0(delta-3), f0(delta-5), 1 XOR g1(delta-3)} closes to f0(delta-4) with nucleation columns delta=4 ({2,1,3}->0=f0(0)) and delta=5 ({1,0}->2=f0(1)). The exception layers close on constant child reads: R=1 {0,1}->2; R=2 {2,3}->0; R=3 {0,1}->2 (z3) and R=4 {2,3}->0 / R=2 {2,3}->0 seam to the main law (SS2.3). Beds: fall (pair gap 1, same plane) + C (plane-1 bed) + B (m=1, w=1 edge values {0,2}); single-value mex tables close by j parity (SS2.2/SS2.4)."
  - "SUBSUMPTION: C1 RESOLVES K1288 O5 — the reported 'z3 R in {2,3} delta-local value mixing' and 'z4 odd-delta {1,2}' were constant R-layers seen on delta-fixed rows; the (R,delta) plane has ZERO mixed cells (exploration X1/X3) and the layer is 2*[R odd] on R<=3 (z3) / R in {1,3} (z4). K1288's z3/z4 R>=4 far observations are now the main law, universally. C2 SHARPENS K1288 O6 into C-PSF': H(R;(m,m+g);w) = 2*[R odd] for R < 2*ceil(w/2); T_w(delta - 2*floor(w/2)) for R >= 2*ceil(w/2), with T_w = g1 (w odd) / f0 (w even); w=0 (K1286 T-PD0, layer thickness 0), w=1,2 (K1288), w=3,4 (this item) are now all PROVED; the layer-thickness law L(w) = 2*ceil(w/2) is confirmed for w<=4 and observed for w in {5,6} (OBS). C3 completes five branches of the B-exit uniformity family: single token at plane z+1 inherits the plane-z law (L-BU0 plane-0, L-BU1G plane-1, L-BU2G plane-2, L-BU3G plane-3, L-BU4G plane-4; plane-5/6 sweeps are OBS in the exploration)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 0e7a23d6 (observed HEAD at start 6a6e3a34 -> pre-push refetch 402d481f; intervening commits were Part DN/DK/DM adoption-lane bookkeeping, non-contact; K1289 vacancy verified: latest K item = K1288 at dbc59af1, code search 'K1289' 0 hits, no competing declaration), then kit a54bc4f2 (verify_k1289.py sha256 f8d86f9e..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282..K1288; engine_block.py standalone 582c93c1..., byte-identical to the K1282-K1288 kits; explore_k1289.py + explore2_k1289.py with outputs; predry/ 4 byte-identical runs), fetch-back of the 15 published kit files (15/15 sha256 full match), THEN official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 a9f0dabc... = predry = declared (fetchback cwd x2 PYTHONHASHSEED random/1 + isolated trees isoA/isoB built from fetch bytes, env -i PYTHONHASHSEED 99/7, ~3.6s/run). counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 20431, 1516, 10530] TOTAL 55,159 bad 0 (D1/D3 z3/z4 band censuses m<=14 g<=25 k>=-30; D2/D4 bed censuses m<=18 j in [-36..0]; D5-D8 typed slices/beds where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine; D9 anchors: L-BU3G/L-BU4G w<=30 vs closed form + engine 493+493, K1288 T-PDT1/2 + T-BDT1/2 re-verification 4,690, K1286 T-PD0/T-B0 re-verification 2,345, sharpened C-PSF' identity sweep over the PROVED planes w=0..4 (cpsf == engine == plane claim) 11,725, T-TWIN identity 201, closed form vs both engines 480, B-exit w=1 edges 4; D10 cross-engine canonical-vs-ordered z3/z4 1,516; D11 OBS: z5/z6 band 4,500x2 + beds 120x2 + far rows 216x2 + low-R hist probes {0:215,2:214}x2). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin; tamper_engine.info is 0 bytes by design), z3s D1 bad 8928 / z3b D2 bad 360 / z4s D3 bad 8928 / z4b D4 bad 360, all rc=1. Audit artifacts published at 7acdfd46 (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries) with fetch-back verification: 20/20 sha256 match (33 manifest entries verified against fetched bytes + the 0-byte tamper_engine.info verified by the remote size-0 listing)."
relations:
- type: extends
  target: K1288
  note: "K1288 (pre-diag twins z1/z2) の O5 (z3/z4 例外小 R 層未確定) を本項の 4 定理で完全解決し、O6 (C-PSF) を sharpened C-PSF′ (層厚 L(w)=2⌈w/2⌉・主則 T_w(δ−2⌊w/2⌋)) に精密化して w=3,4 を全称実例化。z1/z2 アンカー (T-PDT1/T-PDT2/T-BDT1/T-BDT2) は z3 の C 子として帰納で利用し D9(c) が再照合。z3 の typed 構文は K1288 の R 例外層込み packet 構文の直接拡張。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU3G/L-BU4G (本項の新規補題・w≤30 で機体 D9(a)/(b) が閉形式×engine 双方と照合) として fall 子の表を直接再生。床 m=1 の w=1 edge {0,2} も閉形式から (D9(h))。"
- type: depends_on
  target: K1286
  note: "z0 アンカー T-PD0/T-B0 (f0) を D9(d) が再照合 (f0 は本項の全 mex 表の基礎関数)。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1288 公開 block と同一 (startup sha ゲート)。engine_block.py 582c93c1… は K1282–K1288 kit と byte-identical。"
- type: related
  target: K1287
  note: "領域直交 (multi-c web F2 内面 k>0 vs ペア pre-diag k≤0)。本項の z5/z6 OBS は C-PSF′ 予想の w 方向の観測支援。K1287 O1 残部 ((i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化) は本項では非着手 (K1290+ 候補)。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z3z4-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 0e7a23d6・観測 HEAD 6a6e3a34〔着手時〕/ 402d481f〔push 直前再取得〕・K1289 空き・対抗宣言なし)。§1 主張一式 (T-PDT3/T-BDT3/T-PDT4/T-BDT4・L-BU3G/L-BU4G・C1 O5 解決・C2 sharpened C-PSF′・C3 L-BUzG 族)・§2 typed 証明全文 (§2.0 子分類・§2.1–§2.2 z3 band/bed の mex 場合表・§2.3–§2.4 z4 band/bed・§2.5 閉形式からの冪題導出・§2.6 well-founded 性・§2.7 honest 記述)・§3 宣言前探索 (X1–X7/Y1–Y8)・§4 機体宣言 (counts 55,159・変異電池期待値の事前宣言)・§5 open 登録 (O8–O12)・§6 主張の区別。
- path: research/experiments/prediag-twins-z3z4-20261124/
  role: machine
  note: 実験キット一式 (出版 a54bc4f2・監査成果物出版 7acdfd46): README・verify_k1289.py (sha256 f8d86f9e…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z3s/z3b/z4s/z4b)・engine_block.py (582c93c1…・K1282–K1288 kit と同一 bytes)・explore_k1289.py+.out・explore2_k1289.py+.out (宣言前 discovery + wide census + z5/z6 OBS)・predry/ 宣言前 4 走 (byte-identical sha a9f0dabc…)、公式監査成果物 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries)。
- path: research/log/2026-11-24-prediag-twins-z3z4.md
  role: report
  note: 実行 log (宣言→kit→fetch-back 15/15→公式 4 走→変異電池→成果物出版 7acdfd46 と fetch-back 20/20→K item・README bullet の全記録・受入判定・§4 宣言ノート推敲文言の honest 記録・空ファイル照合の技法記録・次課題)。
---

## 概要

K1288（pre-diag 双生児 z1/z2）が open 登録した O5（z3/z4 の例外小 R 層）を
解決し、双生児定理を平面 3・4 まで拡張した。

- **T-PDT3/T-BDT3**: z3 バンド・床は **2·[R odd] (R ≤ 3) / g1(δ−2) (R ≥ 4)**
  （床は δ→j）。例外層は厚み 4 の R 定数層。
- **T-PDT4/T-BDT4**: z4 は **2·[R odd] (R < 4) / f0(δ−4) (R ≥ 4)**
  （偶数例外 cell は主則と値が一致するため層の実効は R∈{1,3}）。
- **L-BU3G/L-BU4G**: 単一 Token @ 平面 4/5 は plane-3/4 則を継承
  （K0832 閉形式から導出・w ≤ 30 で閉形式×両 engine 照合 bad 0）。
  B-exit 均一性族は L-BU0/L-BU1G/L-BU2G（既刊）+ 本項で 5 枝が出揃った。
- **C1（O5 解決）**: K1288 が δ-local な value mixing と報告した z3 R∈{2,3}
  の層は (R,δ) 平面では R 定数層 0/2 に一意化（mixed cell 0）。
- **C2（sharpened C-PSF′）**: 全平面の統一形式
  H = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌋)。
  w=0（K1286）・w=1,2（K1288）・w=3,4（本項）で全称証明済み。
  w∈{5,6} は有限 OBS（D11・全称主張なし）。
- 値はいずれも m・g を経由しない。

## 主張の区分（過大主張の防止）

- **定理（全称・宣言ノート §2 に手証明全文）**: T-PDT3・T-BDT3・T-PDT4・
  T-BDT4・L-BU3G・L-BU4G・C1・C3。well-founded な単一 R 強帰納
  （全子が予算 R−1・面間参照は下位予算のみ〔z4 の C 子は packet 内〕・
  B 子は閉形式で帰納外）。基底 R=0 = mex ∅ = 0。
- **corollary（既刊の言い換え・全称）**: C2 の w ≤ 4 部分。
  C-PSF′ の一般 w（層厚 L(w) の帰納）は**予想**（O9・全称主張なし）。
- **有限観測（OBS・全称主張なし）**: z5/z6 の band・beds・far-row・low-R hist
  （D11・explore2 Y3–Y5/Y7 の z=6,7 sweep）。
- census 55,159 点は定理の実機照合であり、全称性の主張ではない。

## 公式監査（publish-then-execute・fetch-back 検証機体から走行）

- 宣言 0e7a23d6（観測 HEAD 6a6e3a34 → push 直前再取得 402d481f・
  K1289 空き・対抗宣言なし・並走 Part DN/DK/DM と非接触）→
  機体 a54bc4f2（15 ファイル）→ fetch-back sha256 15/15 byte 一致 →
  公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree×2〔fetch-back
  bytes から再構成・sha 再検証〕env -i PYTHONHASHSEED=99/7）すべて rc=0・
  stdout byte-identical（sha256 `a9f0dabcc88c99063a5539163226b56bc46e145537c5c1e4e0f4044c7e748b376`
  以下省略）= 宣言・predry と同一。
- counts `[8928, 360, 8928, 360, 1939, 114, 1939, 114, 20431, 1516, 10530]`・
  総計 55,159 点・bad 0・engine_gate PASS・D10 cross-engine 一致・
  D9 公刊アンカー（K1286 T-PD0/T-B0・K1288 T-PDT1/2・T-BDT1/2・T-TWIN・
  閉形式 vs 両 engine・sharpened C-PSF′ identity w=0..4）整合。
- 変異電池 5/5 検出・宣言どおり（全て run 前に事前宣言）:
  engine rc=2（mutated sha `0ea47a80…` ≠ pin・info は設計どおり 0 バイト）・
  z3s 8928・z3b 360・z4s 8928・z4b 360（全 rc=1）。
- 成果物出版 7acdfd46・fetch-back 20/20 sha 一致
  （空ファイル tamper_engine.info は遠隔 size 0 一覧 + MANIFEST の
  empty-sha `e3b0c442…` で byte 照合・MANIFEST 34 entries 全件掃除）。

## 11×11・規約への接続

- verdict 不消費・11×11 の UNKNOWN は不変・Part DN/DK/DM 等 adoption
  レーンと非接触。
- T-PD0（K1286）+ K1288 + 本項で、ペア面 z∈{0,1,2,3,4} の対角下全域
  k ≤ 0 が R 例外層込みで O(1) 即値評価可能（band は (R,δ) 2 変数・床は 1 変数）。
  枝刈り格子の境界側拡張として巨大探索レーンへ記録（採用判断はオーナー）。

## 次課題（単一オーナー候補）

1. **T-PDT5/T-BDT5・T-PDT6/T-BDT6（O8）**: z5/z6 の typed 全称証明。
   C 子は本項の z3/z4 定理（全 R・例外層込み）を参照するため同一構文で
   証明可能な見通し。sharpened C-PSF′ の w=6 まで全称化。
2. **C-PSF′ の w 帰納（O9）**: 主則域の mex 恒等式は双子恒等式で閉じる
   見込み。主要障壁は例外層の厚み L(w)=2⌈w/2⌉ の帰納（層の子は他面の
   層定数を読む。z3 の証明では z2 の層 {1} のみが必要だった）。
3. **L-BUzG 族の全称形（O10）**: 閉形式の region 計算で一般 w へ。
4. **K1287 O1 残部（K1290+ 候補）**: (i) SLB2/SLB3 単一層族・(ii) L/Am
   frontier の全称化（本項非着手・床負域 (iii) は K1288 供給済み）。
