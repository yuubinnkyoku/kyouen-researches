---
id: K1285
title: "ペア対角スライス理論と pure-c1 ラダーの全称確定: T-PS0/1/2（z0-k1..3・z1-k2..3・z2-k3..4 ペアスライス = [g odd]）・T-L1/L2/L3（pure-c1 ラダー 3 面全て = [d odd]・C-PC1z1-d4 の c=1 半分を解決）・T-ALM（allm-2 六床 = 0）・C-PB2/C-PC（pre-band 単層族・既刊帯定理の直接实例）（publish-then-execute・宣言ノートに証明全文収録・9,794 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the pair-diagonal slice theory. For a pair (m, m+g) define the diagonal coordinate k := R - 2m - g. T-PS0: for every m>=1, g>=1, k in {1,2,3}: H(2m+g+k; (m, m+g); 0) = [g odd]. T-PS1: same for z=1, k in {2,3}. T-PS2: same for z=2, k in {3,4}. The z2 rows are the first systematic values in territory that was open at the close of K1283/K1284. T-L1/L2/L3: immediate reindexing corollaries = the pure-c1 ladder in ALL three low planes: H(2m+d+2; (m, m+d); 0) = H(2m+d+3; (m,m+d); 1) = H(2m+d+4; (m,m+d); 2) = [d odd], for every d>=1, m>=1. The d=1 z1 row (j, j+1)@2j+4 z1 = 1 for all j resolves the c=1 HALF of the K1284 open registration C-PC1z1-d4 (the c>=2 half stays open). T-ALM: the six allm-2 floors (m,m)@2m+2 z0 / 2m+3 z0 / 2m+2 z1 (= published T-E1 instance, cross-listed for audit) / 2m+3 z1 / 2m+3 z2 / 2m+4 z2 are ALL 0. C-PB2/C-PC: pre-band single-layer corollaries (x^c)@x+2 z1 and (x^c)@x+1 z0 have value (c=1: [x odd], c>=2: [x even]) — direct instances of the published band bottoms T-B1'(i) (K1283) / T-B0'(i) (K1282)."
  - "STRUCTURE (why the family closes): EVERY option of a pair position (R; (m, m+g); z) with R = 2m+g+k is one of: (i) min-fall: row-(m-1) pair with g'=g+1, k unchanged (m=1: the same hand is the B-hand leaving the SINGLE token v(g+1, z+1, g+k+1) whose closed-form reading is [g even] on all involved slices); (ii) upper-drop: pair with g'=g-1, k unchanged, and g=1 lands exactly on the allm-2 floor (m,m)@2m+k at the same plane; (iii) C-child: the same pair at plane z-1 with k'=k-1. So slices feed slices one plane down one k down, corners feed allm-2 floors, allm-2 floors feed g=1 slices — a closed dependency web on budget R-1, proved jointly by strong induction on R (well-foundedness argued in note 2.8; base = published single-token closed form v (K0832), hand-proved floors L-EMPTY / L-11z0 / L-1s, and the published T-Q / T-E1 corners)."
  - "PROOFS in full in the single-owner note (2.0-2.9). Key mechanism: for g odd the fall child (or the row-1 B child) is the 0-witness and every other child is shown NOT 1 (upper-drop parity flip, allm-2 corners 0, C-child 1 XOR [g odd] = 0); for g even ALL options are 1 hence mex = 0. The single-token B-child readings v(g+1, z, g+k+1) = [g even] for the three planes and k-ranges are direct closed-form computations (K0832 tail branch, note 2.9)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 2114a771 (observed HEAD 81ae89f1 — all intervening commits are the Part CP/DJ exploration lanes, non-contact; K1285 vacancy re-verified directly against the items dir commits — latest K item = K1284 at 7abca71f, no competing declaration), then kit 2c70a1b6 frozen (verify_k1285.py sha256 a4165f68..., startup sha gate on the embedded engine block, pin bd5f22e4... = the SAME published block as K1138/K1282/K1283/K1284; engine_block.py standalone = 582c93c1..., byte-identical to the K1282/K1283/K1284 kit block), fetch-back of all 13 kit files (size match 13/13 + full-text match of the note / verify_k1285.py / engine_block.py), THEN official 4 runs from the verified bytes: rc=0 all, stdout byte-identical sha256 41762e1b986d08494f4afd0ab4d8f1eb5a406e3608bc8696991b2019df735730 = declared exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated trees env -i x2 PYTHONHASHSEED 99/7, /usr/local/bin/python3 3.12, ~3-4 s/run). counts [1296, 864, 864, 768, 180, 400, 130, 4200, 560, 532] total 9,794 bad 0 (D1 z0-slices / D2 z1 / D3 z2 / D4 ladders / D5 allm-2 / D6 floors+singles-v-both-engines / D7 PB2-PC / D8 wide census all 7 families m<=30 g<=20 / D9 cross-engine canonical-vs-ordered / D10 observation censuses). Mutation battery 8/8 fail-closed exactly as pre-declared: --tamper-engine rc=2, zz0 1296 / zz1 864 / zz2 864 / lad 768 / alm 180 / fl 5 / pb 130, all rc=1. Audit artifacts published at c4b66682 (audit_run1-4 + .info, tamper 8 record files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 31 entries)."
  - "OPEN registrations (finite observations only, NO universal claims; note 5): OBS-D9 border triangle pattern tables z0-k0 = [2,1,0,[g even]] / z1-k1 = [1,2,0,[g even]] / z2-k2 = [1,0,2,[g even]] / z2-k1 = [g odd] (clean observation, 560 pts D9-adjacent census) — proof needs a z1-k0 -> z0-k(-1) cascade, i.e. a k<0 extension of the coordinate system (future F1). OBS-D10 multi-c web: F(1,c>=2)@z1-d4 = 0, G(1,2)@z0-d3 = 0, G(1,c>=3) = 2, a-ladder a>=3 nontrivial, G(d,c>=2)/Y-family spread (532 pts) — c>=2 row structure lies OUTSIDE the pair theory; the spread theory (induction in c) is the prime candidate (future F2). C-PC1z1-d4 c>=2 half: waiting on the spread theory (future F3). z2 pre-band (x^c)@(x+3) z2: blocked by the z2 band collapse. Inherited opens: z1-delta-3 arm-2 exact values, allm-delta-k ladder, pure-count ladder, F14b, C-II2."
  - "CONNECTION to the 11x11 giant lanes: the pair diagonal slices are directly usable as a pruning lattice (children of pair positions all land in known families, enabling O(1) value lookup). Recorded for the giant-lane owners; no verdict consumed, 11x11 UNKNOWN unchanged, non-contact with the Part CY/CP/DH/DA/DJ exploration lanes."
relations:
- type: resolves
  target: K1284
  note: "K1284 open 登録 C-PC1z1-d4（z1-δ4 pure-c1 族 (j,(j+1)^c) の値）のうち c=1 半分を全称解決: T-L2 の d=1 行として (j,j+1)@2j+4 z1 = 1 ∀j。c>=2 半分（census c>=2→0）は open 継続（K1284 が挙げた blockers のうち a-ladder・純カウントラダーに代わる spread 理論の開発が本命）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)（スライス行1の B 手子・allm-2 床の B 手子・C-PB2/C-PC の帯底評価。z∈{1,2,3} の tail 分岐読み v(g+1,z,g+k+1)=[g even] を機体 D6 が両 engine で照合）。"
- type: depends_on
  target: K1282
  note: "T-Q（z0-k1 g=1 compress 角 (m,m)@2m+1 = 0・m>=2 担保）・T-B0′(i)（C-PC の帯底 instance・min(R,Σ)%2 評価）。D8 で公刊定理との衝突検査（4,200 点・bad 0）。"
- type: depends_on
  target: K1283
  note: "T-E1（z1-k2 g=1 compress 角 (m,m)@2m+2 z1 = 0 = T-ALM (2,1) 項と同一局面・重複掲載は照合用）・T-B1′(i)（C-PB2 の帯底 instance・v(Σ,1,x+2) 評価）。engine pin は K1283/K1284 kit と同一 block（bd5f22e4…）。"
- type: related
  target: K1281
  note: "A手子の min 分類（fall/stair/compress）は K1281 §2.0 の規約に準拠（本項は upper-drop を stair・compress 併称で『compress 子』に統一）。ペア族の閉性による予算帰納は、K1282-K1284 の行帰納（T-H1/T-H2/T-L4z1）とは独立の軸（R 方向）で閉じる構文。"
- type: related
  target: K1284
  note: "非解決側の接続: z1-δ4 pure-c1 の c>=2 と K1284 の床 BC5/G4z2 は z2 面以降の帯評価で再利用される。境界三角形 z2-k1 = [g odd] clean 観測（OBS-D9）は z2-δ 系の次の目標。"
- type: related
  target: K1278
  note: "低 z banded 窓定理の『R−2m−g 消費』構造のペア版。スライス族 k∈{1..4} は窓定理の帯域外（k 小域）を値で埋め、両者の接続（k<0 座標）が未来課題 F1。"
- type: related
  target: K1254
  note: "z>=2 面の初の体系的値域（T-PS2）。z=2 帯端シフト・FR-X との対応は open 継続。"
artifacts:
- path: research/log/2026-11-24-pair-slices-pure-c1-ladders-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 2114a771・観測 HEAD 81ae89f1〔着手時 0b113ef3・いずれも探査レーンで非接触〕・K1285 空き確認・対抗宣言なし）。T-PS0/1/2・T-L1/L2/L3・T-ALM・L-EMPTY/L-11z0/L-1s・C-PB2/C-PC の証明全文（§2.0-2.9・手分類と予算帰納の well-founded 性・v readings）・宣言前探索実績・機体宣言（sha・counts・変異表）・open 登録と未来課題 F1-F3・honest 記録を収録。証明の正本。
- path: research/experiments/pair-slices-20261124/
  role: machine
  note: 実験キット一式（出版 2c70a1b6・成果物 c4b66682）: README・verify_k1285.py (sha256 a4165f68…・engine pin bd5f22e4… ゲート内蔵)・engine_block.py (582c93c1…・K1282/K1283/K1284 kit と同一 bytes)・exploration {explore_k1285.py, explore_k1285.out: E1-E6・E5/E6 は open 登録 census}・output dryrun1-4 (+.info) + 公式監査成果物（audit_run1-4.out+.info・tamper 8 ファイル・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 31 entries・全 size/full-text 照合）。
- path: research/log/2026-11-24-pair-slices-pure-c1-ladders.md
  role: report
  note: 実行 log（宣言→キット→fetch-back 照合→公式 4 走→変異電池→成果物出版→K item・README bullet の全記録・受入判定・次課題）。
---

## 概要

ペア (m, m+g) に対角座標 k := R − 2m − g を導入し、3 つの低 z 面で
スライス族を**全称確定**した:

- **T-PS0/1/2**: z0 k∈{1,2,3}・z1 k∈{2,3}・z2 k∈{3,4} で
  H(2m+g+k; (m, m+g); z) = [g odd]（∀m>=1, g>=1）。z2 面は
  K1283/K1284 時点で open だった領域の最初の体系的確定。
- **T-L1/L2/L3**: pure-c1 ラダーが再添字で即時従属し、3 面すべてで
  [d odd]。**d=1 の z1 行は K1284 open 登録 C-PC1z1-d4 の c=1 半分の
  全称解決**。
- **T-ALM**: allm-2 族 6 床 = 0（T-E1 instance を含む照合用重複）。
- **C-PB2/C-PC**: pre-band 単層族 = (c=1: [x odd], c>=2: [x even])
  （公刊 T-B1′/T-B0′ 帯底の直接实例）。
- 床: L-EMPTY・L-11z0・L-1s（手証明）。

構造の鍵は**族の閉性**: ペア局面の手がすべて「同族ペア（k 不変・
g ±1 または行 m−1）/ allm-2 床 / z−1 面の k−1 スライス / 行1 B手子の
単一トークン」に落ち、予算 R−1 の全ての子が既知族。g odd は fall 子
（または B 子）= 0 を 0-witness に mex = 1、g even は全子 = 1 で
mex = 0、c/o 子の z 面カスケード（1 XOR [g odd]）で 3 面が連結する。
全主張を予算 R に関する強帰納で同時に確定（well-founded・§2.8）。

## 主張の区分（過大主張の防止）

- 定理（全称証明・ノート §2 に証明全文）: T-PS0/1/2・T-L1/L2/L3・
  T-ALM・L-EMPTY・L-11z0・L-1s・C-PB2・C-PC。
- 予想の解決（閉鎖）: C-PC1z1-d4 の c=1 半分。
- open 登録（本項で新規・有限観測のみ）: 境界三角形法則
  （z0-k0/z1-k1/z2-k2 = 3 値前置 + [g even] tail・z2-k1 = [g odd]
  clean・k<0 カスケードが blocker・未来課題 F1）・multi-c web
  （F(1,c>=2)=0・G(1,c>=2)・a-ladder a>=3・spread 理論が本命・
  未来課題 F2）・C-PC1z1-d4 の c>=2 半分（F3）・z2 pre-band
  （z2-band 崩壊が鍵）。
- open 継承: z1-δ3 arm-2 精確値・allm-δk ラダー・純カウントラダー・
  F14b・C-II2・z>=2 面の帯構造。
- census は証明ではない: D1-D10 の 9,794 点は定理の実機照合（bad 0）
  であり、定理の全称性は証明によって成立する。

## 公式監査（publish-then-execute・fetch-back 検証機体から走行）

- 宣言 2114a771（観測 HEAD 81ae89f1・K1285 空き・対抗宣言なし）→
  機体 2c70a1b6 → fetch-back 13 ファイル size 照合 + ノート・
  verify・engine_block 全文照合 → 公式 4 走（同一 cwd×2
  PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2 PYTHONHASHSEED=99/7）
  すべて rc=0・stdout byte-identical
  （sha256 41762e1b…= 宣言想定）。~3-4s/走。
- counts `[1296, 864, 864, 768, 180, 400, 130, 4200, 560, 532]`・
  総計 9,794 点・bad 0・engine_gate PASS・D6 singles-vs-v 両 engine
  照合・D9 cross-engine（canonical vs ordered）一致。
- 変異電池 8/8 検出・宣言どおり: engine rc=2・zz0 1296・zz1 864・
  zz2 864・lad 768・alm 180・fl 5・pb 130（すべて rc=1）。
- 成果物出版 c4b66682（audit_run1-4.out+.info・tamper 8 ファイル・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 31 entries）。

## 11×11・規約への接続

- verdict 不消費・11×11 巨大探索の UNKNOWN は不変・Part CY/CP/DH/
  DA/DJ レーンと非接触。
- ペア対角スライスは枝刈り格子としてそのまま利用可能（ペア局面の
  子が全て既知族に落ちるため値即値評価が可能）。巨大レーンへの
  接続は記録のみ（採用判断は巨大レーンオーナー）。

## 次課題（単一オーナー候補）

1. **F1**: 境界三角形法則の全称化（z1-k0 → z0-k(−1) カスケード・
   k<0 座標系の拡張）。
2. **F2**: multi-c web の spread 理論（c 方向帰納）: F(1,c>=2)=0・
   G(1,c>=3)=2・G(d,c>=2)・Y族。
3. **F3**: C-PC1z1-d4 の c>=2 半分（spread 理論待ち）。
