---
id: K1294
title: "pre-diag 双生児 z7/z8 の全称確定: T-PDT7/T-BDT7・T-PDT8/T-BDT8 (R 例外層 2·[R odd] の厚み 8・偶数 cell は z8 で主則に一致)・L-BU7G/L-BU8G・sharpened C-PSF′ (w=0..8 で全称確定・z9/z10 は OBS 登録) — K1290 O9′ z7/z8 部分解決・80,059 点公式監査 bad 0・4 走 byte-identical・層域横断 2 型の初出"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pre-diagonal twins extended to plane 7 and plane 8, universal. Pair positions H(R;(m,m+g);z) on the pre-diagonal band k<=0 and beds b_z(j) := H(2m+j;(m,m);z), j<=0, with delta := R-2m. The exception layers are R-CONSTANT values (packet syntax, fourth generation): T-PDT7 (z7 band): H = 2*[R odd] (R<8, thickness L(7)=2*ceil(7/2)=8); g1(delta-6) (R>=8). T-BDT7 (z7 bed): 2*[R odd] (R<8); g1(j-6) (R>=8). T-PDT8 (z8 band): H = 2*[R odd] (R<8, of which the even cells already coincide with the main law f0(delta-8)=0); f0(delta-8) (R>=8). T-BDT8 (z8 bed): 2*[R odd] (R<8); f0(j-8) (R>=8). None of the values depend on m or g. New uniformity lemmas from the K0832 closed form: L-BU7G: v(w,8,t) = 2*[t odd] (t<8); g1(t-6) (8<=t<=w) — the single token at plane 8 inherits the plane-7 law; L-BU8G: v(w,9,t) = 2*[t odd] (t<8); f0(t-8) (8<=t<=w) — plane-8 law; both machine-checked vs closed form AND both engines for w<=30 (D9(a)/(b))."
  - "THE PROOFS (typed child mex, hand-written in the declaration note SS2.0-SS2.7, well-founded single R strong induction over the joint packet {T-PDT7, T-BDT7, T-PDT8, T-BDT8}): all engine children sit at budget R-1; children are classified as fall (m>=2, delta+1) / B (m=1 -> single token w=g+1 at plane z+1, valued by the K0832 closed form through L-BU7G/L-BU8G without induction) / compress (g>=2, delta-1) / corner (g=1 -> bed slide j=delta-1) / C (1 XOR, plane z-1, same budget R-1). Cross-plane reads: z7's C child reads T-PDT6 (K1290, unconditional all-R); z8's C child reads T-PDT7 (same packet, budget R-1). The B-exit reproduces the fall-child table on plane 7 (g1(delta-5)) and plane 8 (f0(delta-7)); the corner child equals the compress child. Mex closure tables (note SS2.1-SS2.4): for z7 the option set {g1(delta-5), g1(delta-7), 1 XOR f0(delta-7)} closes to g1(delta-6) for all delta parities (the K1290 z5 table shifted by 2 in delta: nucleation column delta=7 ({0,1}->2=g1(1)) and the C-core delta=8 ({1,2,3}->0=g1(2))); for z8 {f0(delta-7), f0(delta-9), 1 XOR g1(delta-7)} closes to f0(delta-8) with nucleation columns delta=9 ({1,0}->2=f0(1)), the C-core delta=8 ({2,1,3}->0=f0(0)) and the compress-core delta=10 ({0,2}->1=f0(2)). THE NEW STRUCTURE OF THE THICKNESS-8 GENERATION: (i) z7's exception layer at R=7 reads its C child at budget 6, which CROSSES OUT of z6's layer region (thickness 6) into z6's MAIN law f0(delta2-6) — the value falls to the constant 0 (hence C=1) through the fixed parity delta2 = 6-2m; the bed pair T-BDT7 R=7 does the same against b6's main law. This is the first layer-crossing generation (K1290 predicted this barrier). (ii) z8's exception layer needs NO crossing at all: its C children at budgets 0..7 all land inside z7's layer region (thicknesses of the twin planes coincide); the seam R=8 is the {2,3}->0 pattern of the z6 seam type (C child reads z7's LAYER value at budget 7). The w-independent exception mechanism (mex{0,1}=2 / mex{2,3}=0) survives its fourth generation unchanged."
  - "SUBSUMPTION: C1 RESOLVES the z7/z8 part of K1290 O9' — the K1290 D11/Y3-Y5 far-observation planes are now the main law, universally, exception layers included. C2 EXTENDS the sharpened plane-shift family C-PSF': H(R;(m,m+g);w) = 2*[R odd] for R < 2*ceil(w/2); T_w(delta - 2*floor(w/2)) for R >= 2*ceil(w/2), with T_w = g1 (w odd) / f0 (w even); w=0 (K1286), w=1,2 (K1288), w=3,4 (K1289), w=5,6 (K1290), w=7,8 (this item) are now all PROVED (D9(g) identity sweep over all 9 planes, 21,105 points); the layer-thickness law L(w) = 2*ceil(w/2) holds universally for w<=8 and the OBS extends it through w=12 (new dedup sweep, 320 (R,delta) cells x planes 9..12, mixed 0, cpsf-bad 0). C3 extends the B-exit uniformity family to NINE branches (L-BU0 ... L-BU8G); the next branches (token planes 10/11, i.e. L-BU9G/L-BU10G) are discovered and registered as OBS (w<=40, engine == closed form == plane-9/10 law)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 8dce7a3d (observed HEAD at start 739e8428 -> pre-push refetch a461445f [design-kyouen-witt lane evidence, orthogonal]; K1294 vacancy verified against the then-observed items tree: latest K item = K1293 739e8428 fix, no competing declaration visible — post hoc the moment lane's collision 2702e06a landed 21 s BEFORE this declaration push and was invisible at refetch time: see NUMBERING RESOLVED), then kit 9421cbc2 (verify_k1294.py sha256 b3974b63..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282..K1290; engine_block.py standalone 582c93c1..., byte-identical to the K1282-K1290 kits; explore_k1294.py + explore2_k1294.py with outputs incl. the pre-declaration typed self-check X8 (3,878+228 points bad 0); predry/ 4 byte-identical runs), fetch-back of the 15 published kit files (15/15 byte match), THEN official 4 runs from the fetch-back verified bytes: rc=0 all, stdout byte-identical sha256 c424a680... = predry = declared (fetchback cwd x2 PYTHONHASHSEED random/1 + isolated trees isoA/isoB built from fetch bytes, env -i PYTHONHASHSEED 99/7, ~10s/run). counts [8928, 360, 8928, 360, 1939, 114, 1939, 114, 39671, 1516, 16190] TOTAL 80,059 bad 0 (D1/D3 z7/z8 band censuses m<=14 g<=25 k>=-30; D2/D4 bed censuses m<=18 j in [-36..0]; D5-D8 typed slices/beds where children are built ONLY from the claim tables and the mex is checked against BOTH the claim and the engine; D9 anchors: L-BU7G/L-BU8G w<=30 vs closed form + engine 493+493, K1290 T-PDT5/T-BDT5/T-PDT6/T-BDT6 re-verification 4,690, K1289 T-PDT3/T-BDT3/T-PDT4/T-BDT4 re-verification 4,690, K1288 T-PDT1/2 + T-BDT1/2 re-verification 4,690, K1286 T-PD0/T-B0 re-verification 2,345, sharpened C-PSF' identity sweep over the PROVED planes w=0..8 (cpsf == engine == plane claim) 21,105, T-TWIN identity 201, closed form vs both engines (x<=16, z in 2..9) 960, B-exit w=1 edges 4; D10 cross-engine canonical-vs-ordered z7/z8 1,516; D11 OBS: z9/z10 band 4,500x2 + beds 120x2 + far rows 216x2 + low-R hist probes {0:346,2:340}x2 (R<10) + L-BU9G/L-BU10G plane-token discovery sweeps (z=10,11, w<=30) 493x2 + dedup (R,delta) sweep z=0..12 4,160). Mutation battery 5/5 fail-closed exactly as pre-declared BEFORE the runs: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin; tamper_engine.info is 0 bytes by design), z7s D1 bad 8928 / z7b D2 bad 360 / z8s D3 bad 8928 / z8b D4 bad 360, all rc=1. Audit artifacts published at 6be78993 (audit_run1-4.out+.info, tamper 5x2 files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries) with fetch-back verification: 20/20 sha256 match + tamper_engine.info remote size 0."
  - "NUMBERING RESOLVED (transient collision, resolved by the concurrent lane deferring): 21 s before our declaration push (8dce7a3d, 15:45:09Z) the moment lane published items K1293-second-moment-multiplier-s-arc-bounds.md and K1294-moment-relaxation-exact-lp-optimum.md (2702e06a, 15:44:48Z), double-booking the Witt lane's K1293 (7a1e183c, 15:25:20Z) and racing this package's provisional K1294 label; our pre-push vacancy refetch predated that commit and showed neither. At integration that lane resolved BOTH collisions itself (K1293/K1294 -> K1295/K1296 at 4a2ad69e 15:53:12Z -> K1296/K1297 at c6edfe14 15:55:36Z, moving above the then-current maximum because, in their words, other lanes had merged items numbered 1294 and 1295 while their work was in flight), deferring K1294 to this package. Items K1294/K1295 are vacant on main (verified by direct path probes and the items-tree commit history immediately before this push), so per AGENTS.md no renumber of this item is required: it publishes as K1294, matching the published declaration/kit/artifact labels end-to-end, and the kit filenames verify_k1294.py / explore_k1294.py / explore2_k1294.py are the genuine in-flight names (publish-then-execute chain intact by construction, not a rename). Contents are fully orthogonal: s-arc moment/LP bounds on inversive planes (K1296/K1297) vs pre-diagonal twins z7/z8 (this item)."

relations:
- type: extends
  target: K1290
  note: "K1290 (pre-diag twins z5/z6) の O9′ (z7/z8 typed 全称) を本項の 4 定理で解決し、sharpened C-PSF′ の全称実例化を w=7,8 に拡張。z5/z6 アンカー (T-PDT5/T-BDT5/T-PDT6/T-BDT6) は z7 の C 子として帰納で利用し D9(c) が再照合。z7 の typed 構文は K1288–K1290 の R 例外層込み packet 構文の第 4 世代で、層厚 8 世代の「層域横断」(z7 R=7 の C 子 budget 6 が z6 主則域を読む・定数落ち) と「横断ゼロ」(z8) の 2 型を初めて確定。"
- type: related
  target: K1296
  note: "採番レースの解決記録 (相手側 moment レーンが自 item を 4a2ad69e/c6edfe14 で K1296/K1297 に移動し K1294 を本項に明け渡し・K1297 は同 companion item)。内容は反転平面の s-弧 moment/LP 上界で、pre-diagonal twins とは完全直交。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。m=1 の B-exit が L-BU7G/L-BU8G (本項の新規補題・w≤30 で機体 D9(a)/(b) が閉形式×両 engine と照合) として fall 子の表を直接再生。床 m=1 の w=1 edge {0,2} も閉形式から (D9(j))。"
- type: depends_on
  target: K1286
  note: "z0 アンカー T-PD0/T-B0 (f0) を D9(f) が再照合 (f0 は本項の全 mex 表の基礎関数)。"
- type: depends_on
  target: K1282
  note: "engine pin bd5f22e4… は K1138/K1282–K1290 公開 block と同一 (startup sha ゲート)。engine_block.py 582c93c1… は K1282–K1290 kit と byte-identical。"
- type: related
  target: K1287
  note: "領域直交 (multi-c web F2 内面 k>0 vs ペア pre-diag k≤0)。K1287 O1 残部 ((i) SLB2/SLB3 単一層族・(ii) L/Am frontier 全称化) は本項でも非接触 (宣言ノート §5 O13)。"
- type: related
  target: K1289
  note: "z3/z4 アンカーを D9(d) が再照合。z7 例外層 R∈{1..6} の C 子は z6 層値読み (K1290 層域 R<6) で第 3 世代機構を継承、R=7 で初の層域横断。"
artifacts:
- path: research/log/2026-11-24-prediag-twins-z7z8-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 8dce7a3d・観測 HEAD 739e8428〔着手時〕/ a461445f〔push 直前再取得〕・当時観測で K1294 空き・対抗宣言なし〔統合時事後判明：宣言の 21 秒前に moment レーンの採番衝突 item 出版が走っており refetch 時点では不可視・相手側がその後自 item を K1296/K1297 へ再採番して解消〕)。§1 主張一式 (T-PDT7/T-BDT7/T-PDT8/T-BDT8・L-BU7G/L-BU8G・C1 K1290 O9′ z7/z8 部分解決・C2 sharpened C-PSF′ w=7,8・C3 L-BUzG 族 9 枝)・§2 typed 証明全文 (§2.0 子分類・§2.1–§2.2 z7 band/bed の mex 場合表・§2.3–§2.4 z8 band/bed・§2.5 閉形式からの補題導出・§2.6 well-founded 性・§2.7 honest 記述)・§3 宣言前探索 (X1–X8/Y1–Y8・typed self-check 宣言前検証)・§4 機体宣言 (counts 80,059・変異電池期待値の事前宣言)・§5 open 登録 (O9″/O10″/O11/O12/O13)・§6 主張の区別。
- path: research/experiments/prediag-twins-z7z8-20261124/
  role: machine
  note: 実験キット一式 (出版 9421cbc2・監査成果物出版 6be78993)。README・verify_k1294.py (sha256 b3974b63…・engine pin bd5f22e4… ゲート内蔵・--tamper-engine/--tamper=z7s/z7b/z8s/z8b)・engine_block.py (582c93c1…・K1282–K1290 kit と同一 bytes)・explore_k1294.py+.out・explore2_k1294.py+.out (宣言前 discovery + wide census + z9/z10 OBS + L-BU9G/L-BU10G 発現 + typed self-check)・predry/ 宣言前 4 走 (byte-identical sha c424a680…)、公式監査成果物 (audit_run1-4.out+.info・tamper 5 種×2・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries)。
- path: research/log/2026-11-24-prediag-twins-z7z8.md
  role: report
  note: 実行 log (宣言→kit→fetch-back 15/15→公式 4 走→変異電池→成果物出版 6be78993 と fetch-back 20/20→K item・README bullet の全記録・受入判定・次課題)。
---

## 概要

K1290（pre-diag 双生児 z5/z6）が open 登録した O9′ の z7/z8 部分を
解決し、双生児定理を平面 7・8 まで拡張した。

- **T-PDT7/T-BDT7**: z7 バンド・床は **2·[R odd] (R < 8) / g1(δ−6) (R ≥ 8)**
  （床は δ→j）。例外層は厚み 8 の R 定数層。
- **T-PDT8/T-BDT8**: z8 は **2·[R odd] (R < 8) / f0(δ−8) (R ≥ 8)**
  （偶数例外 cell R∈{0,2,4,6} は主則 0 と値が一致し層の実効は R∈{1,3,5,7}）。
- **L-BU7G/L-BU8G**: 単一 Token @ 平面 8/9 は plane-7/8 則を継承
  （K0832 閉形式から導出・w ≤ 30 で閉形式×両 engine 照合 bad 0）。
  B-exit 均一性族は 7 枝 → **9 枝**（token 平面 10/11 の L-BU9G/L-BU10G
  相当は w ≤ 40 OBS 発現）。
- **C1（K1290 O9′ z7/z8 部分解決）**: K1290 D11 が OBS として観測していた
  z7/z8 が全称定理化。
- **C2（sharpened C-PSF′）**: 全平面の統一形式
  H = 2·[R odd] (R < 2⌈w/2⌉); T_w(δ−2⌊w/2⌋) (R ≥ 2⌈w/2⌉)。
  w=0（K1286）・1,2（K1288）・3,4（K1289）・5,6（K1290）・**7,8（本項）**
  で全称証明済み（D9(g) が w=0..8 全 9 面で identity 照合 21,105 点）。
  **w∈{9,10}は OBS**（band 4,500×2・beds 120×2・far-row 216×2 bad 0・
  low-R hist {0:346,2:340}）に加え、**dedup sweep で w=11,12 まで 320 cell
  × 13 面 mixed 0・cpsf bad 0 に拡張**（全称主張なし）。
- **厚み 8 世代の新構造**: 層域横断 2 型を初めて確定 — (i) **横断型**
  z7 R=7（および床 R=7）の C 子 budget 6 が z6（層厚 6）の主則域
  f0(δ₂−6) を読むが、δ₂ = 6−2m の parity 固定で値は定数 0 に落ちる
  （K1290 が予告した障壁の実測・導出は宣言ノート §2.1–§2.2）。
  (ii) **横断ゼロ型** z8 は双対面との層厚一致 (8,8) により例外層 R∈{1..7}
  の全 C 子が z7 層域内に収まる（seam R=8 は z6 seam 型 {2,3}→0）。
  層核の w 非依存 mex{0,1}=2 / mex{2,3}=0 機構は第 4 世代も不変。
- 値はいずれも m・g を経由しない。
- **採番レースの解決**: 宣言 push の 21 秒前に moment レーンが
  K1293/K1294 を二重採番して出版 (2702e06a・Witt レーンの K1293 とも衝突)。
  統合時に対象レーンが自 item を K1295/K1296 → K1296/K1297 へ再採番して
  (4a2ad69e・c6edfe14) K1294 を本項に明け渡したため、main 上で K1294 は
  空きのまま確定し、AGENTS.md の統合時再採番規則は不発動。
  本項は出版 chain (宣言ノート・kit・audit 成果物、全て K1294 呼称) と
  端末間で整合する **K1294 のまま**出版する (詳細は aliases NUMBERING
  RESOLVED・run log 手順 8)。

## 主張の区分（過大主張の防止）

- **定理（全称・宣言ノート §2 に手証明全文）**: T-PDT7・T-BDT7・T-PDT8・
  T-BDT8・L-BU7G・L-BU8G・C1（O9′ z7/z8 部分解決の記述）・C2 の w ≤ 8 部分。
  well-founded な単一 R 強帰納（全子が予算 R−1・面間参照は下位予算のみ
  〔z8 の C 子は packet 内〕・B 子は閉形式で帰納外）。基底 R=0 = mex ∅ = 0。
  例外層 R<8 の閉鎖は mex{0,1}=2 / mex{2,3}=0 の w 非依存機構
  （z3 で確立・第 4 世代で再確認・横断 cell R=7 も C 値の parity 固定で
  定数読みに帰着）。
- **corollary（既刊の言い換え・全称）**: C2/C3 の既刊分の再表現。
  C-PSF′ の一般 w（層厚 L(w) の帰納）は**予想**（O9″・全称主張なし）。
- **有限観測（OBS・全称主張なし）**: z9/z10 の band・beds・far-row・low-R
  hist（D11・explore2 Y3–Y5）、L-BU9G/L-BU10G 発現（Y7・D11 z=10,11
  sweep）、dedup (R,δ) sweep z=0..12。
- census 80,059 点は定理の実機照合であり、全称性の主張ではない。

## 11×11・規約への接続

- verdict 不消費・11×11 の UNKNOWN は不変・Part DH/DM/DN 等 adoption
  レーン・moment-polynomial/Witt design レーン (K1291–K1293) と非接触。
- T-PD0（K1286）+ K1288 + K1289 + K1290 + 本項で、ペア面 z∈{0..8} の対角下
  全域 k ≤ 0 が R 例外層込みで O(1) 即値評価可能（band は (R,δ) 2 変数・
  床は 1 変数）。枝刈り格子の境界側拡張として巨大探索レーンへ記録
  （採用判断はオーナー）。

## 次課題（単一オーナー候補）

1. **T-PDT9/T-BDT9・T-PDT10/T-BDT10（O9″）**: z9/z10 の typed 全称証明。
   層厚 L(9)=L(10)=10。C 子は本項 z7/z8 定理（全 R・例外層込み）を参照。
   横断型の幅が広がる: z9 では C 子 budget 8,9 が z8 主則域 (R ≥ 8) を
   読む（2 列・うち budget 8 は z8 seam 直後の主則読み）・z10 は横断
   ゼロ型（層厚一致 (10,10)）。sharpened C-PSF′ の w=10 まで全称化。
2. **C-PSF′ の w 帰納（O9″ 主体）**: 層厚 L(w)=2⌈w/2⌉ の帰納ステップ。
   本項で「横断型」と「横断ゼロ型」の 2 型が確定したため、奇数世代
   (w=2j+1) は横断 1 列・偶数世代 (w=2j+2) は横断ゼロ、という w mod 2
   ペア交互の見取り（宣言ノート §2.6・§5 O11 の (w 偶奇) 分類）。
3. **L-BUzG 族の全称形（O10″）**: 閉形式の region 計算で一般 w へ
   （L-BU9G/L-BU10G の w ≤ 40 OBS が入力・境界一致 3 型の世代スキーム）。
4. **K1287 O1 残部（O13）**: (i) SLB2/SLB3 単一層族・(ii) L/Am frontier
   の全称化（本項非接触）。
