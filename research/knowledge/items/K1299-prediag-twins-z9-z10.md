---
id: K1299
title: "pre-diag 双生児 z9/z10 の全称確定: T-PDT9/T-BDT9・T-PDT10/T-BDT10 (R 例外層 2·[R odd] の厚み 10・偶数 cell は z10 で主則に一致)・L-BU9G/L-BU10G・sharpened C-PSF′ (w=0..10 で全称確定・z11/z12 は OBS 登録) — K1294 O9″ z9/z10 部分解決・90,535 点公式監査 bad 0・4 走 byte-identical・層域横断 2 行と横断ゼロの厚み 10 世代"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins extended to plane 9 and plane 10, universal. Pair positions H(R;(m,m+g);z) on the pre-diagonal band k<=0 and beds b_z(j) := H(2m+j;(m,m);z), j<=0, with delta := R-2m. The exception layers are R-CONSTANT values (packet syntax, fifth generation): T-PDT9 (z9 band): H = 2*[R odd] (R<10, thickness L(9)=2*ceil(9/2)=10); g1(delta-8) (R>=10). T-BDT9 (z9 bed): 2*[R odd] (R<10); g1(j-8) (R>=10). T-PDT10 (z10 band): H = 2*[R odd] (R<10, of which the even cells already coincide with the main law f0(delta-10)=0); f0(delta-10) (R>=10). T-BDT10 (z10 bed): 2*[R odd] (R<10); f0(j-10) (R>=10). None of the values depend on m or g. New uniformity lemmas from the K0832 closed form: L-BU9G: v(w,10,t) = 2*[t odd] (t<10); g1(t-8) (10<=t<=w) — the single token at plane 10 inherits the plane-9 law; L-BU10G: v(w,11,t) = 2*[t odd] (t<10); f0(t-10) (10<=t<=w) — plane-10 law; both machine-checked vs closed form AND both engines for w<=30 (D9(a)/(b)) and probed at w<=40 (explore2 Y7)."
  - "THE PROOFS (typed child mex, hand-written in the declaration note SS2.0-SS2.7, well-founded single R strong induction over the joint packet {T-PDT9, T-BDT9, T-PDT10, T-BDT10}): all engine children sit at budget R-1; children are classified as fall (m>=2, delta+1) / B (m=1 -> single token w=g+1 at plane z+1=10/11, valued by the K0832 closed form through L-BU9G/L-BU10G without induction) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1) / C (1 XOR, plane z-1, same budget R-1). Cross-plane reads: z9's C child reads T-PDT8 (K1294, unconditional all-R); z10's C child reads T-PDT9 (same packet, budget R-1). The B-exit reproduces the fall-child table on plane 9 (g1(delta-7)) and plane 10 (f0(delta-9)); the corner child equals the compress child. Mex closure tables (note SS2.1-SS2.4): for z9 the option set {g1(delta-7), g1(delta-9), 1 XOR f0(delta-9)} closes to g1(delta-8) for all delta parities (the K1294 z7 table shifted by 2 in delta: nucleation column delta=9 ({0,1}->2=g1(1)) and the C-core delta=10 ({1,2,3}->0=g1(2))); for z10 {f0(delta-9), f0(delta-11), 1 XOR g1(delta-9)} closes to f0(delta-10) with nucleation columns delta=11 ({1,0}->2=f0(1)), the C-core delta=10 ({2,1,3}->0=f0(0)) and the compress-core delta=12 ({0,2}->1=f0(2)). THE THICKNESS-10 GENERATION: (i) z9's exception layer sprouts the layer-crossing at TWO rows: the in-layer final row R=9 (C child at budget 8 reads z8's MAIN law f0(delta2-8), delta2=8-2m even -> constant 0 -> C=1; the seam-adjacent main read, matching z7's R=7 against z6) AND the seam R=10 (C child at budget 9 reads z8's main law f0(odd)=1 -> C=0); the crossing values are parity-locked constants, the w-independent exception mechanism (mex{0,1}=2 / mex{2,3}=0) survives its fifth generation; the bed pair T-BDT9 does the same against b8's main law. (ii) z10 needs NO crossing at all: its C children at budgets 0..9 all land inside z9's layer region (thicknesses coincide at (10,10)); the seam R=10 is the {2,3}->0 pattern (C child reads z9's LAYER value 2 at budget 9 -> C=3), the K1290 z6 / K1294 z8 seam type."
  - "SUBSUMPTION: C1 RESOLVES the z9/z10 part of K1294 O9-prime-prime — the K1294 D11/Y3-Y5 far-observation planes are now the main law, universally, exception layers included. C2 EXTENDS the sharpened plane-shift family C-PSF': H(R;(m,m+g);w) = 2*[R odd] for R < 2*ceil(w/2); T_w(delta - 2*floor(w/2)) for R >= 2*ceil(w/2), with T_w = g1 (w odd) / f0 (w even); w=0 (K1286), w=1,2 (K1288), w=3,4 (K1289), w=5,6 (K1290), w=7,8 (K1294), w=9,10 (this item) are now all PROVED (D9(h) identity sweep over all 11 planes, 25,795 points); the layer-thickness law L(w) = 2*ceil(w/2) holds universally for w<=10 and the OBS extends it through w=14 (new dedup sweep, 320 (R,delta) cells x planes 0..14, mixed 0, cpsf-bad 0; K1294 reached plane 12). C3 extends the B-exit uniformity family to ELEVEN branches (L-BU0 ... L-BU10G); the next branches (token planes 12/13, i.e. L-BU11G: v(w,12,t) = 2*[t odd] (t<12)/g1(t-10) and L-BU12G: v(w,13,t) = 2*[t odd] (t<12)/f0(t-12)) are discovered and registered as OBS (verify w<=30, explore2 w<=40, engine == closed form == plane-11/12 law, bad 0)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 506a7d18 (observed HEAD at start 4377c987 -> pre-push refetch 4f731fb1 [round-4 commit-chain log, orthogonal]; K1299 vacancy verified by direct path probe against the then-observed max = K1298 74753b66, parity-graded lane, no competing declaration), then kit fc3f987f (verify_k1299.py sha256 0fa53559..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282..K1294; engine_block.py standalone 582c93c1..., byte-identical to the K1282-K1294 kits; explore_k1299.py + explore2_k1299.py with outputs incl. the pre-declaration typed self-check X8 (3,878+228 points bad 0); predry/ 4 byte-identical runs), fetch-back of the 15 published kit files (15/15 byte match), THEN official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 e9b3784a... = predry = declared (fetchback cwd x2 PYTHONHASHSEED random/1 + isolated trees isoA/isoB built from fetch bytes, env -i PYTHONHASHSEED 99/7, ~12.2-12.8s/run). counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 49291, 1516, 17046] TOTAL 90,535 bad 0 (D1/D3 z9/z10 band censuses m<=14 g<=25 k>=-30; D2/D4 bed censuses m<=18 j in [-36..0]; D5-D8 typed slices/beds where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine; D9 anchors: L-BU9G/L-BU10G w<=30 vs closed form + engine 493+493, K1294 T-PDT7/T-BDT7/T-PDT8/T-BDT8 re-verification 4,690, K1290 T-PDT5/T-BDT5/T-PDT6/T-BDT6 re-verification 4,690, K1289 T-PDT3/T-BDT3/T-PDT4/T-BDT4 re-verification 4,690, K1288 T-PDT1/2 + T-BDT1/2 re-verification 4,690, K1286 T-PD0/T-B0 re-verification 2,345, sharpened C-PSF' identity sweep over the PROVED planes w=0..10 (cpsf == engine == plane claim) 25,795, T-TWIN identity 201, closed form vs both engines (x<=16, z in 2..11) 1,200, B-exit w=1 edges 4; D10 cross-engine canonical-vs-ordered z9/z10 1,516; D11 OBS: z11/z12 band 4,500x2 + beds 120x2 + far rows 216x2 + low-R hist probes {0:402,2:392}x2 (R<12) + L-BU11G/L-BU12G plane-token discovery sweeps (z=12,13, w<=30) 493x2 + dedup (R,delta) sweep z=0..14 4,800). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin; tamper_engine.info is 0 bytes by design), z9s D1 bad 8928 / z9b D2 bad 360 / z10s D3 bad 8928 / z10b D4 bad 360, all rc=1. Audit artifacts published at f9afeadd (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries) with fetch-back verification: 20/20 sha256 match + tamper_engine.info remote size 0."
  - "NUMBERING (clean this time): the package reserved max+1 = K1299 by direct path probe before the declaration push; the observed maximum at integration time was K1298 (parity-graded-grundy lane, renumbered 74753b66 from its own colliding K1294 label, deferring to the K1294 fast-lane package); K1295/K1296/K1297 were in the intervening hours taken by the projective-blocking-kyouen (dfb38f6b) and moment lanes; no collision or race occurred at any point of this chain (the last concurrent-lane commits during the chain were Part DP adoption-lane outputs 8c3b77ae/7a5ee133, content-orthogonal)."

relations:
- type: extends
  target: K1294
  note: "K1294 (pre-diag twins z7/z8) の O9″ (z9/z10 typed 全称) を本項の 4 定理で解決し、sharpened C-PSF′ の全称実例化を w=9,10 に拡張。z7/z8 アンカー (T-PDT7/T-BDT7/T-PDT8/T-BDT8) は z9 の C 子として帰納で利用し D9(c) が再照合。z9 の typed 構文は K1288–K1294 の R 例外層込み packet 構文の第 5 世代で、層厚 10 世代の「層域横断 2 行」(z9 R=9/R=10 の C 子 budget 8/9 が z8 主則域を読む・値は parity 固定で定数) と「横断ゼロ」(z10) の 2 型が厚み 10 でも再現。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU9G/L-BU10G (本項の新規補題・w≤30 で機体 D9(a)/(b) が閉形式×両 engine と照合) として fall 子の表を直接再生。床 m=1 の w=1 edge {0,2} も閉形式から (D9(k))。"
- type: depends_on
  target: K1286
  note: "z0 アンカー T-PD0/T-B0 (f0) を D9(g) が再照合 (f0 は本項の全 mex 表の基礎関数)。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1294 公開 block と同一 (startup sha ゲート)。engine_block.py 582c93c1… は K1282–K1294 kit と byte-identical。"
- type: related
  target: K1290
  note: "z5/z6 アンカーを D9(d) が再照合。z9 例外層 R∈{1..8} の C 子は z8 層値読み (K1294 層域 R<8) で第 4 世代機構を継承、R=9 で層域横断・seam R=10 で 2 行目。"
- type: related
  target: K1289
  note: "z3/z4 アンカーを D9(e) が再照合 (アンカー系の積み上げは K1290/K1294 と同一構文)。"
- type: related
  target: K1287
  note: "領域直交 (multi-c web F2 内面 k>0 vs ペア pre-diag k≤0)。K1287 O1 残部 ((i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化) は本項でも非接触 (宣言ノート §5 O13)。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z9z10-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 506a7d18・観測 HEAD 4377c987〔着手時〕/ 4f731fb1〔push 直前再取得〕・直接 path probe で K1299 空き・対抗宣言なし)。§1 主張一式 (T-PDT9/T-BDT9/T-PDT10/T-BDT10・L-BU9G/L-BU10G・C1 K1294 O9″ z9/z10 部分解決・C2 sharpened C-PSF′ w=9,10・C3 L-BUzG 族 11 枝)・§2 typed 証明全文 (§2.0 子分類・§2.1–§2.2 z9 band/bed の mex 場合表〔層域横断 2 行の構造記述含む〕・§2.3–§2.4 z10 band/bed〔横断ゼロ〕・§2.5 閉形式からの補題導出・§2.6 well-founded 性・§2.7 honest 記述)・§3 宣言前探索 (X1–X8/Y1–Y8・typed self-check 宣言前検証 3,878+228 bad 0)・§4 機体宣言 (counts 90,535・変異電池期待値の事前宣言)・§5 open 登録 (O9‴/O10‴/O11/O12/O13)・§6 主張の区別。
- path: research/experiments/prediag-twins-z9z10-20261124/
  role: machine
  note: 実験キット一式 (出版 fc3f987f・監査成果物出版 f9afeadd)。README・verify_k1299.py (sha256 0fa53559…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z9s/z9b/z10s/z10b)・engine_block.py (582c93c1…・K1282–K1294 kit と同一 bytes)・explore_k1299.py+.out・explore2_k1299.py+.out (宣言前 discovery + wide census + z11/z12 OBS + L-BU11G/L-BU12G 発現 + typed self-check)・predry/ 宣言前 4 走 (byte-identical sha e9b3784a…)、公式監査成果物 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries)。
- path: research/log/2026-11-24-prediag-twins-z9z10.md
  role: report
  note: 実行 log (宣言→kit→fetch-back 15/15→公式 4 走→変異電池→成果物出版 f9afeadd と fetch-back 20/20→K item・README bullet の全記録・受入判定・次課題)。
---

## 概要

K1294（pre-diag 双生児 z7/z8）が open 登録した O9″ の z9/z10 部分を
解決し、双生児定理を平面 9・10 まで拡張した。

- **T-PDT9/T-BDT9**: z9 バンド・床は **2·[R odd] (R < 10) / g1(δ−8) (R ≥ 10)**
  （床は δ→j）。例外層は厚み 10 の R 定数層。
- **T-PDT10/T-BDT10**: z10 は **2·[R odd] (R < 10) / f0(δ−10) (R ≥ 10)**
  （偶数例外 cell R∈{0,2,4,6,8} は主則 0 と値が一致し層の実効は
  R∈{1,3,5,7,9}）。
- **L-BU9G/L-BU10G**: 単一 Token @ 平面 10/11 は plane-9/10 則を継承
  （K0832 閉形式から導出・w ≤ 30 で閉形式×両 engine 照合 bad 0・
  w ≤ 40 発現 probe）。B-exit 均一性族は 9 枝 → **11 枝**
  （token 平面 12/13 の L-BU11G/L-BU12G 相当は w ≤ 30/40 OBS 発現）。
- **sharpened C-PSF′ の w=9,10 全称化**: ペア面
  **H = 2·[R odd] (R < 2⌈w/2⌉) / T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**
  が w ∈ {0..10} 全 11 面で全称確定（D9(h) identity sweep 25,795 点）。
  z11/z12 は OBS（band 4,500×2・beds 120×2・far-row 216×2・
  low-R (R<12) hist {0:402,2:392}×2）、dedup sweep は **plane 14 まで拡張**
  （z=0..14・全 15 面 mixed 0・cpsf bad 0）。
- **層厚 10 世代の構造**: z9 の層域横断は **2 行**（層内最終行 R=9 の
  C 子 budget 8 が z8 seam 直後の主則 f0(−2m)=0 を読み C=1・継ぎ目
  R=10 の C 子 budget 9 が z8 主則 f0(odd)=1 を読み C=0・いずれも
  parity 固定で定数）。z10 は層厚一致 (10,10) で**横断ゼロ**（z8 型）。
  mex{0,1}=2 / mex{2,3}=0 の w 非依存機構は第 5 世代も不変。

## 証明構造

- 単一 packet {T-PDT9, T-BDT9, T-PDT10, T-BDT10} で R 強帰納。
  子は 5 型（fall / B-exit / compress / corner / C・床は 3 型）で全て
  budget R−1。z9 の C 子は z8（K1294 既刊・全 R 無条件）、z10 の C 子は
  z9（packet 内・下位 budget）。B 子は K0832 閉形式で帰納外。
- 帰納本体は宣言ノート §2 の mex 場合表（z9: δ→δ−2 平行移動表 +
  核 δ=9 / C 核 δ=10・z10: 核 δ=11 / C 核 δ=8+2 / comp 核 δ=10+2）。
- typed 子の mex 構文は宣言前 X8 self-check（申立テーブル + 閉形式のみで
  構成した子 mex = 申立値 = engine・3,878+228 点 bad 0）で事前検証済み。

## 公式監査（publish-then-execute）

1. 宣言ノート `506a7d18`（機体 counts 90,535・変異電池期待値を事前宣言）
2. キット `fc3f987f`（verify_k1299.py sha256 `0fa53559…`・engine pin
   `bd5f22e4…` ゲート内蔵・explore/explore2+.out・predry 4 走）→
   fetch-back 15/15 byte 一致
3. 公式 4 走（fetch-back bytes から）: rc=0・stdout byte-identical
   sha256 **`e9b3784a…`** ＝宣言＝predry（同一 cwd random/1 + 隔離 tree
   env -i 99/7・~12.3s/走）・counts
   `[8928,360,8928,360,1939,114,1939,114,49291,1516,17046]`
   **総計 90,535 bad 0**
4. 変異電池 5/5 fail-closed 宣言一致（engine rc2〔mutated sha
   `0ea47a80…`≠pin・tamper_engine.info は size 0〕・z9s 8,928 / z9b 360 /
   z10s 8,928 / z10b 360 全 rc1）
5. 成果物 `f9afeadd`（audit_run1-4.out+.info・tamper 5 種×2・
   detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）→
   fetch-back 20/20 byte 一致

census 90,535 点は定理の実機照合であって証明の代替ではない。
標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
全て UNKNOWN のまま・verdict 不消費。OBS（z11/z12 band/beds/far-row/
low-R・L-BU11G/L-BU12G・dedup sweep z=11..14）は全称主張なし。

## 次課題（resolved/open）

- resolves: K1294 §5 O9″ の z9/z10 部分（sharpened C-PSF′ w ∈ {0..10}）。
- open（本項 §5）: O9‴（z11/z12 typed・層厚 12・横断 2 行 /
  横断ゼロの予告構造込み・dedup/OBS 入力は本項 D11 に揃っている）、
  O10‴（L-BUzG 族の一般 w 全称形・L-BU11G/L-BU12G OBS が入力）、
  O11（例外定数層の一般理論・(w mod 2) 2 型分類）、O12（giant 枝刈り
  格子の境界側拡張 z∈{0..10}）、O13（K1287 O1 残部・非接触のまま）。
