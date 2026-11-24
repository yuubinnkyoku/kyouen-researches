---
id: K1286
title: "境界スライスと対角下バンドの全称確定: T-PD0（z0 対角下バンド一次元崩壊則・δ = R−2m のみで評価）・T-B0（z0 床）・T-Z1/T-B1（z1 境界 k∈{−1,0,1}・床 j∈{−1,0,1}）・T-Z2/T-B2（z2 境界 k∈{0,1,2}・床 j∈{0,1,2}）・系 C1–C5（K1285 OBS-D9 境界三角形 4 脚の全称昇格 = K1285 未来課題 F1 完了）（publish-then-execute・宣言ノートに証明全文収録・18,118 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the border-slices / pre-diagonal collapse. For a pair (m, m+g) define the diagonal coordinate k := R - 2m - g and the DELTA coordinate delta := R - 2m. T-PD0 (z0 pre-diagonal one-dimensional collapse law): for every m>=1, g>=1, 0 <= R <= 2m+g: H(R; (m, m+g); 0) = f0(R-2m) = f0(delta), where f0(d) = 2 if d==1; [d odd] if d<=0; [d even] if d>=2. The value passes NEITHER through m NOR g — the ENTIRE z0 band k in [-2m-g, 0] (diagonal and all the way down to R=0) collapses to the single integer delta. This solves at once the cascade K1285's future F1 thought necessary (z1-k0 -> z0-k(-1)): no per-k induction is needed because the whole band is delta-1D. T-B0 (z0 beds): b0(j) = f0(j) for every m>=1, j<=0, 2m+j>=0 (m-independent). T-Z1 (z1 border slices): for k in {-1,0,1}: Z1(-1,·): g=1->1, g=2->2, g>=3->[g even]; Z1(0,·): g=1->2, g>=2->[g odd]; Z1(1,·): g=1->1, g=2->2, g>=3->[g even]. T-B1 (z1 beds): b1(1)=0 (published front line, cross-listed for audit), b1(0)=1, b1(-1)=0 (m>=2) / 2 (m=1). T-Z2 (z2 border slices): for k in {0,1,2}: Z2(0,·)=Z2(2,·): g=1->1, g=2->0, g=3->2, g>=4->[g even]; Z2(1,·)=[g odd] (clean). T-B2 (z2 beds): b2(0)=0, b2(1)=2, b2(2)=0. Corollaries: C1 z0 diagonal leg = f0(g) (K1285 OBS-D9 P0 promoted); C2 z1 diagonal leg = Z1(1,g) (P1); C3 z2 diagonal leg = Z2(2,g) (P2); C4 z2-k1 clean = [g odd] (K1285 OBS promoted); C5 the NEW determined regions z1-k0/k(-1) and z2-k0 (no prior observation existed). After this item the pair z0/z1/z2 planes are undetermined ONLY in the far interior k >= 4/2/3."
  - "STRUCTURE (typed-children mex, note 2): EVERY option of a pair position falls into one of: fall (lower token, m>=2: row-(m-1) pair, g'=g+1, k unchanged, delta+1) / B (m=1: single token v(g+1, z+1, R-1) valued by the published K0832 closed form) / compress (upper token, g>=2: g'=g-1, k unchanged, delta-1) / corner (g=1: bed (m,m)@(R-1; z) with slice j=k) / C (z>=1: same pair at plane z-1, R-1, value 1 XOR). ALL children live on budget R-1, and inter-plane references always point DOWN one budget (z2 -> z1 tables and beds, z1 -> z0/T-PD0 and beds), so the whole claim packet (T-PD0/T-B0/T-Z1/T-B1/T-Z2/T-B2 on top of the published-K0832 closed form) is proved JOINTLY by strong induction on R (well-foundedness note 2.5; base R=0 = empty-option mex 0 = f0(-2m)). The B-uniformity lemmas L-BU0/1/2 show the m=1 B-children reproduce the exact fall-child tables (direct K0832 tail-branch computations, w<=30 machine-checked), which is what makes the m-split of the packet unnecessary on the claimed slices."
  - "PROOFS in full in the single-owner note (2.0-2.5). Key mechanism on the z0 band: H(P) = mex{f0(delta+1), f0(delta-1)} (fall/B below, compress/corner above), and the 8-row delta case table closes every class. On z1/z2 the mex tables run over {fall, upper/corner, C} values read off from the Z1/Z2/bed tables and the z-plane one below; all cases are enumerated in the note and the same mex arithmetic is machine-checked against BOTH engine values and the claim tables on wide finite ranges by the kit's typed batteries (D2/D3/D4/D5/D6, with the claims supplying child values and the engine only arbitrating)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at f6db3f33 (observed HEAD at start 405da370, re-fetched pre-push 5b9c6231 — all intervening commits are the Part DF/DG/DL/DJ solver/bookkeeping lanes, non-contact; K1286 vacancy re-verified directly against the items dir commits — latest K item = K1285 at 6703e506, no competing declaration), then kit ccf48d10 frozen (verify_k1286.py sha256 13ec8f7b..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282-K1285; engine_block.py standalone = 582c93c1..., byte-identical to the K1282-K1285 kit block), fetch-back of all 13 kit files with FULL sha256 byte-match on every file (verify 13ec8f7b... / engine_block 582c93c1... / explore_border.py 4aac4ebb... / explore_border.out 10e2c5c4... / dryrun1-4.out all ac7d104d... byte-identical / README d32e6668...), THEN official 4 runs from the verified bytes: rc=0 all, stdout byte-identical sha256 ac7d104d8a70b69c37ae354d98048fcc07c69ca836cb482166c22ba1864967e9 = declared exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated trees env -i x2 PYTHONHASHSEED 99/7, /usr/local/bin/python3 3.12, ~0.7-0.8 s/run). counts [6719, 3470, 882, 42, 882, 42, 152, 2910, 2353, 666] total 18,118 bad 0 (D1 T-PD0 z0 band m<=14 g<=21 k in [-26..0] / D2 typed z0 + beds + L-BU0/1/2 / D3 T-Z1 slices engine+typed / D4 T-B1 beds / D5 T-Z2 slices / D6 T-B2 beds / D7 T-B0 beds / D8 published anchors interior 7 families + T-ALM + T-Q + floors/EMPTY/singles vs both engines + C-PB2/C-PC / D9 cross-engine + K1285 OBS pattern-function identity P0/P1/P2/clean vs the now-proven tables + engine recheck / D10 observation registrations). Mutation battery 6/6 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80... != pin), --tamper=f0 -> D1 6719 + D7 152 bad / z1 -> D3 882 / z2 -> D5 882 / bed1 -> D4 42 / bed2 -> D6 42, all rc=1. Audit artifacts published at a92dcc12 (audit_run1-4.out+.info, tamper 12 record files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries)."
  - "OPEN registrations (finite observations only, NO universal claims; note 5): O1 z1 pre-diag (k<=-2) is NOT delta-1D — z1-k(-2) has an m=1,g=1 nucleation (value 2) and m>=2 rows 0,1,2,[g odd]; the typed proof needs the z1 beds j<=-2 which are m-SPLIT (j=-2: m=1->0, m>=2->1), so the z1 pre-diag law will be a two-stage construction over small-m bed families (future F1'). O2 z2-k(-1) rows appear m-uniform 0,1,0,2,[g odd] (g>=5) over m<=10 (378 cells D10/E6) and z2-k(-2) has a g=5 value-2 spike and an m=1/g=1 split — the z2 pre-diag collapse is the K1287 target (its C-children depend on O1). O3 the F2 spread web F_d/G_d (d in {1,2,3}) c>=2 columns are m-INDEPENDENT (288 OBS points, D10): F: (d=2, c>=2) -> 1 else 0; G: (d=1: c=2->0, c>=3->2; d=2: c>=2->1; d=3: c>=2->0) — input data for the spread theory (K1285 F2). O4 the z1 beds j<=-2 and z2 beds j<=-1 m-split structure (E3) is not claimed here; typed Beds extension is a K1287 candidate."
  - "CONNECTION to the 11x11 giant lanes: T-PD0 makes the ENTIRE pair z0 band (k<=0) an O(1) delta-lookup, extending the K1285 pruning lattice over the whole pre-diagonal region. Recorded for the giant-lane owners; no verdict consumed, 11x11 UNKNOWN unchanged, non-contact with the Part DF/DG/DL/DJ lanes."
relations:
- type: resolves
  target: K1285
  note: "K1285 open 登録（OBS-D9 境界三角形）の全称化、すなわち宣言ノート §5 未来課題 F1 を完了: z0-k0 = f0(g) / z1-k1 = Z1(1,g) / z2-k2 = Z2(2,g) / z2-k1 = [g odd] clean の 4 脚が T-PD0/T-Z1/T-Z2 の系として全称確定。F1 が想定した z1-k0 → z0-k(−1) カスケードは T-PD0 の δ 座標で一挙に解消（バンド全体が δ のみに落ちるため k=0 側からでも k<0 側でも同一則）。K1285 の残 open（multi-c web・C-PC1z1-d4 c>=2 半分）は本項では不完全のまま継承（O3 が spread 理論への新規入力データを供給）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。本項は B-uniformity 補題 L-BU0/1/2（m=1 の B 手子 v(g+1, z+1, R−1) が fall 子の表 Z1(k,·)/Z2(k,·)/f0 と一致すること）を閉形式の直接計算として使用。機体 D2c/d/e が w<=30 で閉形式・表・両 engine の三方照合。"
- type: depends_on
  target: K1282
  note: "公刊アンカーの再照合（D8: 内面 7 族 [g odd] 2,240 点・T-Q corner 20 点・T-ALM 120 点・floors/EMPTY/singles vs 両 engine 400 点・C-PB2/C-PC 130 点・T-PS0/1/2〔K1285 公刊〕族）。T-Q (m,m)@2m+1 z0 = 0 は T-B0 の j=1 境界外再掲ではなく床側独立アンカーとして照合。"
- type: depends_on
  target: K1283
  note: "T-E1・T-B1′(i)・engine pin 同一 block（bd5f22e4…・K1282-K1285 kit chain）。b1(1)=0 は K1281/K1283 前線（公示済み pure-c1 ラダー系）の再掲・照合用重複掲載。"
- type: related
  target: K1285
  note: "T-PS0/1/2（内面 k>=1・[g odd] 族）と本項（境界帯 k<=0・床）でペア z0/z1/z2 面の未確定領域は遠方内面 k>=4/2/3 のみ。typed 子 mex の構文は K1285 の族閉性証明の R 軸帰納を typed 化したもの（D9 は K1285 OBS パターン関数 P0/P1/P2/z2k1-clean と新定理表の関数同一性 800 点を照合・drift なし）。"
- type: related
  target: K1281
  note: "A手子の min 分類（fall/stair/compress）は K1281 §2.0 の規約に準拠。本項は境界帯で bed へ落ちる corner を分離し、予算 R−1 の型付き子解析（typed-children mex）で帰納を閉じる。"
artifacts:
- path: research/log/2026-11-24-border-slices-prediag-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 f6db3f33・観測 HEAD 5b9c6231〔着手時 405da370・いずれも長期レーンで非接触〕・K1286 空き確認・対抗宣言なし）。T-PD0/T-B0/T-Z1/T-B1/T-Z2/T-B2・L-BU0/1/2 の証明全文（§2.0-2.5・型付き子 mex case 表・well-founded 性）・宣言前探索実績（E1-E6）・機体宣言（sha・counts・変異表）・§5 open 登録 O1-O4 と K1287 ロードマップ・honest 記録を収録。証明の正本。
- path: research/experiments/border-slices-20261124/
  role: machine
  note: 実験キット一式（出版 ccf48d10・成果物 a92dcc12）: README・verify_k1286.py (sha256 13ec8f7b…・engine pin bd5f22e4… ゲート内蔵)・engine_block.py (582c93c1…・K1282-K1285 kit と同一 bytes)・exploration {explore_border.py, explore_border.out: E1-E6・E5/E6 は open 登録 census}・output dryrun1-4 (+.info・4 走 byte-identical) + 公式監査成果物（audit_run1-4.out+.info・tamper 12 ファイル・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries・全ファイル sha256 fetch-back 照合）。
- path: research/log/2026-11-24-border-slices-prediag.md
  role: report
  note: 実行 log（宣言→キット→fetch-back 照合→公式 4 走→変異電池→成果物出版→K item・README bullet の全記録・受入判定・次課題）。
---

## 概要

ペア (m, m+g) の z0 面で、対角下バンド全域（k ≤ 0・すなわち
0 ≤ R ≤ 2m+g）が **δ := R − 2m の一次元関数に崩壊**することを
全称証明した:

- **T-PD0**: H(R; (m, m+g); 0) = f0(δ)（f0(δ) = 2 (δ=1); [δ odd]
  (δ≤0); [δ even] (δ≥2)）。値は m・g を経由しない。
- **T-B0**: z0 床 b0(j) = f0(j)（j ≤ 0・m 非依存）。
- **T-Z1/T-B1**: z1 境界スライス k∈{−1,0,1}（Z1 表）と床
  j∈{−1,0,1}（b1(1)=0 は公刊前線の再掲）。
- **T-Z2/T-B2**: z2 境界スライス k∈{0,1,2}（Z2 表・k=1 は [g odd]
  clean）と床 j∈{0,1,2} → 0, 2, 0。
- **系 C1–C5**: K1285 OBS-D9 境界三角形 4 脚（z0-k0/z1-k1/z2-k2/
  z2-k1）の全称昇格 = **K1285 未来課題 F1 の完了**。z1-k0/k(−1)・
  z2-k0 は従来観測すらない新規確定領域。
- **ペア z0/z1/z2 面で未確定は遠方内面 k ≥ 4/2/3 のみ**となった。

構造の鍵は**型付き子 mex 解析**: fall/B/compress/corner/C の全子が
予算 R−1 に落ち、面間参照（z2→z1→z0）も常に下位予算。B-uniformity
補題 L-BU0/1/2（m=1 の B 子が K0832 閉形式から fall 子の表そのものを
再生）により、主張面上で m に関する場合分けが不要になる。全主張を
R に関する単一の強帰納で同時確定（§2.5 well-founded）。

## 主張の区分（過大主張の防止）

- 定理（全称証明・ノート §2 に証明全文）: T-PD0・T-B0・T-Z1・T-B1・
  T-Z2・T-B2・L-BU0/1/2。
- 予想・観測の解決: K1285 OBS-D9 境界三角形 4 脚 → 全称定理
  （C1–C4）。K1285 未来課題 F1 完了。
- open 登録（本項で新規・有限観測のみ）: O1 z1 pre-diag 非崩壊
  （m=1 核生成・z1 床 j≤−2 の m 分裂 → F1′）・O2 z2-k(−1)/(−2)
  （K1287 目標）・O3 F2 web c≥2 列 m 非依存（spread 理論への
  入力）・O4 床 m 分裂構造（typed Beds 拡張候補）。
- 継承 open: K1285 の multi-c web・C-PC1z1-d4 c≥2 半分・
  z2 pre-band・a-ladder・純カウントラダー等。
- census は証明ではない: D1–D10 の 18,118 点は定理の実機照合
  （bad 0）であり、定理の全称性は手証明（型付き子 mex の case
  analysis）によって成立する。typed 電池はその算術の有限機械照合。

## 公式監査（publish-then-execute・fetch-back 検証機体から走行）

- 宣言 f6db3f33（観測 HEAD 5b9c6231・着手時 405da370・K1286 空き
  〔最新 K item = K1285 6703e506〕・対抗宣言なし）→ 機体 ccf48d10
  → fetch-back 13 ファイル全 sha256 byte 一致 → 公式 4 走
  （同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2
  PYTHONHASHSEED=99/7）すべて rc=0・stdout byte-identical
  （sha256 ac7d104d… = 宣言想定）。~0.7-0.8s/走。
- counts `[6719, 3470, 882, 42, 882, 42, 152, 2910, 2353, 666]`・
  総計 18,118 点・bad 0・engine_gate PASS・D8 公刊アンカー再照合
  （2,910 点）・D9 交差エンジンと K1285 OBS パターン関数同一性照合。
- 変異電池 6/6 期待どおり fail-closed・rc-exact: engine rc=2
  （mutated sha 0ea47a80… ≠ pin）。f0 → D1 6719 + D7 152 bad・
  z1 → D3 882・z2 → D5 882・bed1 → D4 42・bed2 → D6 42
  （すべて rc=1・宣言値と一致）。
- 成果物出版 a92dcc12（audit_run1-4.out+.info・tamper 12 ファイル・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）。

## 11×11・規約への接続

- verdict 不消費・11×11 巨大探索の UNKNOWN は不変・Part DF/DG/DL/
  DJ レーンと完全非接触。
- T-PD0 によりペア z0 帯全域（k ≤ 0）が δ の O(1) 即値評価可能に
  なった（K1285 枝刈り格子の境界側への拡張）。巨大レーンへの接続は
  記録のみ（採用判断は巨大レーンオーナー）。

## 次課題（単一オーナー候補）

1. **z2 pre-diag 崩壊**（O2・K1287 本命）: z2-k(−1) の m 非依存候補
   表 (0,1,0,2,[g odd] g≥5) と z2-k(−2) の g=5 突起の typed 証明。
   C 子が z1-k(−2) を要求するため O1 に依存。
2. **z1 pre-diag の 2 段構え法則**（F1′）: z1 床 j ≤ −2 の m 分裂
   （小 m 床族）込みの構造確定。
3. **spread 理論**（K1285 F2）: O3 の c ≥ 2 列 m 非依存データ
   （F_d/G_d・288 点）を入力とした c 方向帰納。
4. **typed Beds 拡張**（O4）: z1/z2 床の負 j 側 m 分裂の全称化。
