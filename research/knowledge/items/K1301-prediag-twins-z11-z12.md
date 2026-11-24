---
id: K1301
title: "pre-diag 双生児 z11/z12 の全称確定: T-PDT11/T-BDT11・T-PDT12/T-BDT12 (R 例外層 2·[R odd] の厚み 12・偶数 cell は z12 で主則に一致)・L-BU11G/L-BU12G・sharpened C-PSF′ (w=0..12 で全称確定・z13/z14 は OBS 登録) — K1299 O9‴ z11/z12 部分解決・101,503 点公式監査 bad 0・4 走 byte-identical・層域横断 2 行と横断ゼロの厚み 12 世代"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins extended to plane 11 and plane 12, universal. Pair positions H(R;(m,m+g);z) on the pre-diagonal band k<=0 and beds b_z(j) := H(2m+j;(m,m);z), j<=0, with delta := R-2m. The exception layers are R-CONSTANT values (packet syntax, sixth generation): T-PDT11 (z11 band): H = 2*[R odd] (R<12, thickness L(11)=2*ceil(11/2)=12); g1(delta-10) (R>=12). T-BDT11 (z11 bed): 2*[R odd] (R<12); g1(j-10) (R>=12). T-PDT12 (z12 band): H = 2*[R odd] (R<12, of which the even cells already coincide with the main law f0(delta-12) since delta even <= 10 gives delta-12 even <= -2 gives f0=0); f0(delta-12) (R>=12). T-BDT12 (z12 bed): 2*[R odd] (R<12); f0(j-12) (R>=12). None of the values depend on m or g. New uniformity lemmas from the K0832 closed form: L-BU11G: v(w,12,t) = 2*[t odd] (t<12); g1(t-10) (12<=t<=w) — the single token at plane 12 inherits the plane-11 law; L-BU12G: v(w,13,t) = 2*[t odd] (t<12); f0(t-12) (12<=t<=w) — plane-12 law; both machine-checked vs closed form AND both engines for w<=30 (D9(a)/(b)) and probed at w<=40 (explore2 Y7)."
  - "THE PROOFS (typed child mex, hand-written in the declaration note SS2.0-SS2.6, well-founded single R strong induction over the joint packet {T-PDT11, T-BDT11, T-PDT12, T-BDT12}): all engine children sit at budget R-1; children are classified as fall (m>=2, delta+1) / B (m=1 -> single token w=g+1 at plane z+1=12/13, valued by the K0832 closed form through L-BU11G/L-BU12G without induction) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1) / C (1 XOR, plane z-1, same budget R-1). Cross-plane reads: z11's C child reads T-PDT10 (K1299, unconditional all-R); z12's C child reads T-PDT11 (same packet, budget R-1). The B-exit reproduces the fall-child table on plane 11 (g1(delta-9)) and plane 12 (f0(delta-11)); the corner child equals the compress child. Mex closure tables (note SS2.1-SS2.4): for z11 the option set closes to g1(delta-10) for all delta parities (the K1299 z9 table shifted by 2 in delta: nucleation column delta=11 ({0,1}->2=g1(1)) and the C-core delta=12 ({1,2,3}->0=g1(2))); for z12 {f0(delta-11), f0(delta-13), 1 XOR g1(delta-11)} closes to f0(delta-12) with nucleation columns delta=13 ({1,0}->2=f0(1)), the C-core delta=12 ({2,1,3}->0=f0(0)) and the compress-core delta=14 ({0,2}->1=f0(2)). THE THICKNESS-12 GENERATION: (i) z11's exception layer sprouts the layer-crossing at TWO rows: the in-layer final row R=11 (C child at budget 10 reads z10's MAIN law f0(delta2-10), delta2=10-2m even -> constant 0 -> C=1) AND the seam R=12 (C child at budget 11 reads z10's main law f0(odd)=1 -> C=0); the crossing values are parity-locked constants, the w-independent exception mechanism (mex{0,1}=2 / mex{2,3}=0) survives its sixth generation; the bed pair T-BDT11 does the same against b10's main law. (ii) z12 needs NO crossing at all: its C children at budgets 0..11 all land inside z11's layer region (thicknesses coincide at (12,12)); the seam R=12 is the {2,3}->0 pattern (C child reads z11's LAYER value 2 at budget 11 -> C=3), the K1290 z6 / K1294 z8 / K1299 z10 seam type. The odd-plane (z11) crossing-2-rows / even-plane (z12) crossing-zero pair structure persists at thickness 12 (K1289/K1290/K1294/K1299 and now this item)."
  - "SUBSUMPTION: C1 RESOLVES the z11/z12 part of K1299 O9-triple-prime — the K1299 D11/Y3-Y5 far-observation planes are now the main law, universally, exception layers included. C2 EXTENDS the sharpened plane-shift family C-PSF': H(R;(m,m+g);w) = 2*[R odd] for R < 2*ceil(w/2); T_w(delta - 2*floor(w/2)) for R >= 2*ceil(w/2), with T_w = g1 (w odd) / f0 (w even); w=0 (K1286), w=1,2 (K1288), w=3,4 (K1289), w=5,6 (K1290), w=7,8 (K1294), w=9,10 (K1299), w=11,12 (this item) are now all PROVED (D9(i) identity sweep over all 13 planes, 30,485 points); the layer-thickness law L(w) = 2*ceil(w/2) holds universally for w<=12 and the OBS extends it through w=16 (dedup sweep, 320 (R,delta) cells x planes 0..16, mixed 0, cpsf-bad 0; K1299 reached plane 14). C3 extends the B-exit uniformity family to THIRTEEN branches (L-BU0 ... L-BU12G); the next branches (token planes 14/15, i.e. L-BU13G: v(w,14,t) = 2*[t odd] (t<14)/g1(t-12) and L-BU14G: v(w,15,t) = 2*[t odd] (t<14)/f0(t-14)) are discovered and registered as OBS (verify w<=30, explore2 w<=40, engine == closed form == plane-13/14 law, bad 0)."
  - "MACHINE (publish-then-execute, exact chain; TWO EXECUTIONS OF THE SAME HOURLY FAST LANE, honest split recorded in the continuation note 391cf512): the sibling hourly run declared FIRST: single-owner declaration note published at 6f4c524d (observed HEAD at start 90732788 [Part DQ kit wave C, orthogonal]; K1300 already taken by the s-parameter lane at a20b5e25, verified by direct path probe; K1301 reserved as max+1, no competing declaration), then kit eb045ea2 (verify_k1301.py sha256 6026e07f..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282..K1299; engine_block.py standalone 582c93c1..., byte-identical to the K1282-K1299 kits; explore_k1301.py + explore2_k1301.py with outputs incl. the pre-declaration typed self-check X8 (3,878+228 points bad 0); predry/ 4 byte-identical runs sha 70206d62...), fetch-back of the 15 published kit files at eb045ea2 (15/15 byte match) — THEN THE STALL: 1h39m with no audit outputs; this continuation run re-verified the fetch-back (15/15), published the continuation record 391cf512, and executed the official chain: official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 70206d62... = declared = predry (fetchback cwd x2 PYTHONHASHSEED random/1 + isolated trees isoA/isoB built from fetch bytes, env -i PYTHONHASHSEED 99/7, 15.7-16.7s/run). counts [8928,360,8928,360,1939,114,1939,114,58911,1516,18394] TOTAL 101,503 bad 0 (D1/D3 z11/z12 band censuses; D2/D4 bed censuses; D5-D8 typed slices/beds where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine; D9 anchors: L-BU11G/L-BU12G w<=30 vs closed form + engine 493+493, K1299 T-PDT9/T-BDT9/T-PDT10/T-BDT10 re-verification 4,690, K1294 anchors 4,690, K1290 anchors 4,690, K1289 anchors 4,690, K1288 anchors 4,690, K1286 T-PD0/T-B0 re-verification 2,345, sharpened C-PSF' identity sweep over the PROVED planes w=0..12 30,485, T-TWIN identity 201, closed form vs both engines (x<=16, z in 2..13) 1,440, B-exit w=1 edge values 4; D10 cross-engine canonical-vs-ordered z11/z12 1,516; D11 OBS: z13/z14 band 4,500x2 + beds 120x2 + far rows R>=14 215x2 (the R=13 in-layer cells excluded after an initial battery-design flaw caught pre-declaration, note SS2.7) + low-R (R<14) hist probes {0:582,2:567}x2 + L-BU13G/L-BU14G plane-token discovery sweeps (z=14,15, w<=30) 493x2 + dedup (R,delta) sweep z=0..16 5,440). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin; tamper_engine.info is 0 bytes by design), z11s D1 bad 8,928 / z11b D2 bad 360 / z12s D3 bad 8,928 / z12b D4 bad 360, all rc=1. Audit artifacts published at eef36f40 (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries) with fetch-back verification: 20/20 sha256 match + tamper_engine.info remote size 0."
  - "NUMBERING (clean): the sibling run reserved max+1 = K1301 by direct path probe before the declaration push (K1300 was already published by the sParameter lane at a20b5e25; observed maximum at declaration time K1300); no collision or race occurred at any point of the chain (intervening commits were batch-33 long-lane outputs, W-spectrum/moment-lane outputs and PG-family outputs, all content-orthogonal). The chain is honestly recorded as split across two executions of the same fast lane: declaration + kit (sibling), fetch-back re-verify + continuation record + official runs + artifacts + this item (continuation run) — see the continuation note research/log/2026-11-24-prediag-twins-z11z12-continuation-takeover.md at 391cf512; the abort clause (competing K1301 publication) never triggered."

relations:
- type: extends
  target: K1299
  note: "K1299 (pre-diag twins z9/z10) の §5 O9‴ (z11/z12 typed 全称) を本項の 4 定理で解決し、sharpened C-PSF′ の全称実例化を w=11,12 に拡張。z9/z10 アンカー (T-PDT9/T-BDT9/T-PDT10/T-BDT10) は z11 の C 子として帰納で利用し D9(c) が再照合。z11 の typed 構文は K1288–K1299 の R 例外層込み packet 構文の第 6 世代で、層厚 12 世代の「層域横断 2 行」(z11 R=11/R=12 の C 子 budget 10/11 が z10 主則域 (R ≥ 10) を読む・値は parity 固定で定数) と「横断ゼロ」(z12) の mod 2 ペア 2 型 (奇数世代=横断 2 行・偶数世代=横断ゼロ) が厚み 12 でも再現 (O11 で帰納候補として定式化)。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU11G/L-BU12G (本項の新規補題・w≤30 で機体 D9(a)/(b) が閉形式×両 engine と照合) として fall 子の表を直接再生。床 m=1 の w=1 edge {0,2} も閉形式から (D9(l))。"
- type: depends_on
  target: K1286
  note: "z0 アンカー T-PD0/T-B0 (f0) を D9(h) が再照合 (f0 は本項の全 mex 表の基礎関数)。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1299 公開 block と同一 (startup sha ゲート)。engine_block.py 582c93c1… は K1282–K1299 kit と byte-identical。"
- type: related
  target: K1294
  note: "z7/z8 アンカーを D9(d) が再照合。z11 例外層 R∈{1..10} の C 子は z10 層値読み (K1299 層域 R<10) で第 5 世代機構を継承、R=11 で層域横断・seam R=12 で 2 行目 (K1294 z7 の R=7/R=8 と同型の δ+2 平行移動)。"
- type: related
  target: K1290
  note: "z5/z6 アンカーを D9(e) が再照合 (アンカー系の積み上げは K1299/K1294 と同一構文)。"
- type: related
  target: K1287
  note: "領域直交 (multi-c web F2 内面 k>0 vs ペア pre-diag k≤0)。K1287 O1 残部 ((i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化) は本項でも非接触 (宣言ノート §5 O13)。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z11z12-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 6f4c524d・観測 HEAD 90732788〔着手時〕・直接 path probe で K1300 取得済みを確認し K1301 空き確保・対抗宣言なし)。§1 主張一式 (T-PDT11/T-BDT11/T-PDT12/T-BDT12・L-BU11G/L-BU12G・C1 K1299 O9‴ z11/z12 部分解決・C2 sharpened C-PSF′ w=11,12・C3 L-BUzG 族 13 枝)・§2 typed 証明全文 (§2.0 子分類・§2.1–§2.2 z11 band/bed の mex 場合表〔層域横断 2 行 R=11/R=12 の構造記述含む〕・§2.3–§2.4 z12 band/bed〔横断ゼロ (12,12)〕・§2.5 閉形式からの補題導出・§2.6 well-founded 性・§2.7 far-row 電池設計の誤りと宣言前修正の honest 記述)・§3 宣言前探索 (X1–X8/Y1–Y8・typed self-check 宣言前検証 3,878+228 bad 0)・§4 機体宣言 (counts 101,503・変異電池期待値の事前宣言・predry sha 70206d62…)・§5 open 登録 (O9⁗/O10⁗/O11/O12/O13)・§6 主張の区別。
- path: research/log/2026-11-24-prediag-twins-z11z12-continuation-takeover.md
  role: log
  note: continuation 記録 (出版 391cf512)。先行 hourly 実行の宣言+kit 出版 (17:19:17Z/17:19:58Z) 後 1 時間 39 分の audit 成果物停滞を記録し、宣言 bytes・kit bytes を一切変更せずに残工程 (公式 4 走・変異電池・成果物出版・K item・README bullet・run log) を継続した旨と競合時中止規約を先行出版 (publish-then-execute の実行側)。fetch-back 15/15 sha 照合を先に確認。
- path: research/experiments/prediag-twins-z11z12-20261124/
  role: machine
  note: 実験キット一式 (宣言出版 eb045ea2・監査成果物出版 eef36f40)。README・verify_k1301.py (sha256 6026e07f…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z11s/z11b/z12s/z12b)・engine_block.py (582c93c1…・K1282–K1299 kit と同一 bytes)・explore_k1301.py+.out・explore2_k1301.py+.out (宣言前 discovery + wide census + z13/z14 OBS + L-BU13G/L-BU14G 発現 + typed self-check)・predry/ 宣言前 4 走 (byte-identical sha 70206d62…)、公式監査成果物 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries)。fetch-back 15/15 + 20/20 byte 一致・tamper_engine.info 遠隔 size 0。
- path: research/log/2026-11-24-prediag-twins-z11z12.md
  role: report
  note: 実行 log (先行実行の宣言→kit、continuation 実行の記録 391cf512→fetch-back 再検証→公式 4 走→変異電池→成果物出版 eef36f40 と fetch-back 20/20→K item・README bullet の全記録・受入判定・次課題・2 実行分割の honest 記録)。
---

## 概要

K1299（pre-diag 双生児 z9/z10）が open 登録した O9‴ の z11/z12 部分を
解決し、双生児定理を平面 11・12 まで拡張した（第 6 世代・層厚 12）。

- **T-PDT11/T-BDT11**: z11 バンド・床は **2·[R odd] (R < 12) / g1(δ−10) (R ≥ 12)**
  （床は δ→j）。例外層は厚み 12 の R 定数層。
- **T-PDT12/T-BDT12**: z12 は **2·[R odd] (R < 12) / f0(δ−12) (R ≥ 12)**
  （偶数例外 cell R∈{0,2,...,10} は主則 f0(δ−12)=0 と値が一致し層の実効は
  R∈{1,3,...,11}）。
- **L-BU11G/L-BU12G**: 単一 Token @ 平面 12/13 は plane-11/12 則を継承
  （K0832 閉形式から導出・w ≤ 30 で閉形式×両 engine 照合 bad 0・
  w ≤ 40 発現 probe）。B-exit 均一性族は 11 枝 → **13 枝**
  （token 平面 14/15 の L-BU13G/L-BU14G 相当は w ≤ 30/40 OBS 発現）。
- **sharpened C-PSF′ の w=11,12 全称化**: ペア面
  **H = 2·[R odd] (R < 2⌈w/2⌉) / T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌉)**
  が w ∈ {0..12} 全 13 面で全称確定（D9(i) identity sweep 30,485 点）。
  z13/z14 は OBS（band 4,500×2・beds 120×2・far-row R≥14 215×2・
  low-R (R<14) hist {0:582,2:567}×2）、dedup sweep は **plane 16 まで拡張**
  （z=0..16・全 17 面 mixed 0・cpsf bad 0・K1299 の z≤14 から +2 面）。
- **層厚 12 世代の構造**: z11 の層域横断は **2 行**（層内最終行 R=11 の
  C 子 budget 10 が z10 seam 直後の主則 f0(δ₂−10)=0（δ₂=10−2m even）を
  読み C=1・継ぎ目 R=12 の C 子 budget 11 が z10 主則 f0(odd)=1 を読み
  C=0・いずれも parity 固定で定数）。z12 は層厚一致 (12,12) で**横断ゼロ**
  （z8/z10 型・seam R=12 は層値 2 を読み C=3 の {2,3}→0 型）。
  mex{0,1}=2 / mex{2,3}=0 の w 非依存機構は第 6 世代も不変。

## 証明構造

- 単一 packet {T-PDT11, T-BDT11, T-PDT12, T-BDT12} で R 強帰納。
  子は 5 型（fall / B-exit / compress / corner / C・床は 3 型）で全て
  budget R−1。z11 の C 子は z10（K1299 既刊・全 R 無条件）、z12 の C 子は
  z11（packet 内・下位 budget）。B 子は K0832 閉形式で帰納外。
- 帰納本体は宣言ノート §2 の mex 場合表（z11: K1299 z9 表の δ→δ−2
  平行移動・核 δ=11 / C 核 δ=12、z12: 核 δ=13 / C 核 δ=12 /
  comp 核 δ=14・beds は j parity 2 行表）。
- typed 子の mex 構文は宣言前 X8 self-check（申立テーブル + 閉形式のみで
  構成した子 mex = 申立値 = engine・3,878+228 点 bad 0）で事前検証済み。

## 公式監査（publish-then-execute）

1. 宣言ノート `6f4c524d`・キット `eb045ea2`（先行 hourly 実行・
  counts 101,503・変異電池期待値・predry sha `70206d62…` を事前宣言）→
  1 時間 39 分の停滞 → continuation 記録 `391cf512`（本実行・bytes 変更なし）
2. fetch-back 15/15 byte 一致（verify 6026e07f…・engine_block 582c93c1…・
  predry 4 走 70206d62…）の再検証
3. 公式 4 走（fetch-back bytes から）: rc=0・stdout byte-identical
  sha256 **`70206d62…`** ＝宣言＝predry（同一 cwd random/1 + 隔離 tree
  env -i 99/7・15.7–16.7s/走）・counts
  `[8928,360,8928,360,1939,114,1939,114,58911,1516,18394]`
  **総計 101,503 bad 0**
4. 変異電池 5/5 fail-closed 宣言一致（engine rc2〔mutated sha
  `0ea47a80…`≠pin・tamper_engine.info は size 0〕・z11s/z12s 8,928 /
  z11b/z12b 360 全 rc1）
5. 成果物 `eef36f40`（audit_run1-4.out+.info・tamper 5 種×2・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）→
  fetch-back 20/20 byte 一致

census 101,503 点は定理の実機照合であって証明の代替ではない。
標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
全て UNKNOWN のまま・verdict 不消費。OBS（z13/z14 band/beds/far-row/
low-R・L-BU13G/L-BU14G・dedup sweep z=13..16）は全称主張なし。

## 次課題（resolved/open）

- resolves: K1299 §5 O9‴ の z11/z12 部分（sharpened C-PSF′ w ∈ {0..12}）。
- open（本項 §5）: O9⁗（z13/z14 typed・層厚 L(13)=L(14)=14・横断 2 行 /
  横断ゼロの予告構造込み・dedup/OBS 入力は本項 D11/Y3–Y5/Y8 に揃っている）、
  O10⁗（L-BUzG 族の一般 w 全称形・境界一致 3 型スキームの一般 w 命題化）、
  O11（例外定数層の一般理論・横断型=奇数世代 / 横断ゼロ型=偶数世代の
  (w mod 2) 2 型分類で O9⁗ と統合）、O12（giant 枝刈り格子の境界側拡張
  z∈{0..12}）、O13（K1287 O1 残部・非接触のまま）。
