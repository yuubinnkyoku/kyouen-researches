---
id: K1308
title: "上半畳み込みの全称確定: T-UH（ペア上半 tail = [g odd]・真の安定化長 k ≥ z+1）・T-DU'（床 k ≥ z → 0・閾値正確）・Z-DIAG（対角行 3 分岐則・全 plane・被包: K1286 C1–C3 の全 z 昇格)・L-SB（単一トークン tail 読み）でペア・床の面 z ≤ 2 が全 k で閉鎖（K1303 O-G4 far above-diagonal 完了・窓偶奇交互予想は 29 反例で棄却・publish-then-execute・宣言ノートに証明全文収録・20,588 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the upper-half collapse. Diagonal coordinate k := R - 2m - g (pairs) / k := R - 2a (beds). T-UH (universal): for every z>=0, m>=1, g>=1, k>=z+1: H(2m+g+k; (m, m+g); z) = [g odd], independent of m, k, and z — the pair value stabilizes to the gap parity EXACTLY from k = z+1 (sharp: the k=z row differs by the Z-DIAG law). T-DU' (universal): for every z>=0, a>=1, k>=z: H(2a+k; (a,a); z) = 0; threshold sharp (z1-k0 row b1(0)=1 and z2-k1 row b2(1)=2, published K1286). Z-DIAG (universal, ALL planes — promotes the published z0/z1/z2 diagonal legs to every z at once): for k=z, H(2m+g+z; (m, m+g); z) = [g odd] (g<=z) / 2 (g=z+1) / [g even] (g>=z+2). L-SB (corollary of the published K0832 closed form): v(x, p, x+j) = x%2 for all x>=2, p>=1, j>=p, plus the B-exit boundary readings v(z+1, z+1, 2z+1)=2, v(z+2, z+1, 2z+2)=(z+1)%2, v(1, p, R)=1 (R>=2), v(1,1,1)=2 used by the proofs. LANDMARK: together with the published K1303 band (k<=0, all planes) and the K1286 z2-k1 row, the pair planes z=0,1,2 and the bed planes z=0,1,2 are now determined for EVERY k — the undetermined pair/bed region for z>=3 is only the transition window 1<=k<=z-1."
  - "STRUCTURE (typed children, joint budget induction — third vertex of the web after K1285's slices and K1286's border): every option of a pair cell at k>=z is one of fall (pair, g+1, k SAME, plane same) / compress (pair, g-1, k same) / corner (g=1 -> bed, k same, and k>=z keeps it inside T-DU') / B-exit (m=1 -> single token valued by the published closed form) / C (plane z-1, k-1: diagonal maps to diagonal, tail maps to tail). Key observations: A-children preserve k, C decrements k and z together, so the upper region closes on budget R-1 by strong induction over the JOINT packet {T-UH, Z-DU', T-DU'} with the K0832 closed form as instant base. Tail uniformity: ALL options of a T-UH cell evaluate to 1-[g odd], hence mex = [g odd] (machine-checked pointwise: set(children) == {1-claim}). Z-DIAG mex tables run over the three g-regions x m-split and close with the 2 exactly at g=z+1. T-DU' options are all in {1,2}. Well-foundedness + base cells (R<=3) hand-checked and re-checked by D2/D3 smallest cells."
  - "SUBSUMPTION (all published anchors re-checked identically in audit D6, 1,941 pts): K1285 T-PS0/1/2 slices are T-UH instances; K1285 T-ALM six allm-2 floors are T-DU' instances; K1282 T-Q corner is T-DU'; K1286 diagonals: Z1(1,.) = Z-DIAG z=1, Z2(2,.) = Z-DIAG z=2, T-B1 b1(1)=0 / T-B2 b2(2)=0 are T-DU', b1(0)=1 / b2(1)=2 are the sharpness sub-threshold exceptions, T-B0 rows are the published bed band re-checked with the domain guard 2m+j>=0 (two out-of-domain cells excluded as battery design error, honestly recorded — same class as K1303 SS2.7)."
  - "REFUTED + OBSERVATIONS (no universal claims): the pre-declaration transition-window parity-alternation conjecture ('rows k not congruent z mod 2 in 1<=k<=z-1 have the tail value [g odd]') FAILS from z=4: 29 counters on the frozen census (z3..8, m1..3, g1..12; distribution 5/2/8/4/10; z=3 clean; full list frozen in the audit obs). The SURVIVING half (congruent rows k=z-2, z-4, ... follow Z-DIAG(g,z)) is clean on a 1,296-pt census through z=13 (OBS-WC, unproved). Bed window row k=z-1 is 1/2 at z=1/2 (published) and 0 on the census for z>=3 (OBS-BW, unproved). C-SUM census conjecture (tail value = [token-sum S odd]) supports: singles [x odd]=L-SB, pairs [g odd]=T-UH, beds 0=T-DU', triples 1,344 pts, mixed triples 840 pts, quads 180 pts all bad 0; thresholds appear multiplicity-dependent (mixed look stable from k=z+1 — E6b, obs); generalization is future F1."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at eabcb742 (observed HEAD 295b9505 — Part DW lane, orthogonal; K1308 vacancy verified: latest K-item publish chain ends at K1305, K1306 declared by the SLB ladder lane 53d2d335 and K1307-provisional by the REMO sweep lane 4d2d506a — both orthogonal, non-contact), kit 28959626 frozen, fetch-back of all 13 kit files (byte/sha256 match 13/13 + full-text match of the note), THEN official 4 runs from the verified bytes: rc=0 all, stdout byte-identical sha256 d3e244f42f290db0cb0a28d15cd9dec482386e808fcc673db6e4995e16c88d25 = the declared predry sha exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated trees env -i x2 PYTHONHASHSEED 99/7, /usr/local/bin/python3 3.12, ~2.6 s/run). counts [5760, 972, 1260, 1512, 2623, 1941, 1440, 2364, 6, 1116, 1594] total 20,588 bad 0 (D1 T-UH census / D2 T-DU' census / D3 Z-DIAG census / D4 typed self-check: children built ONLY from the claim tables + K0832 closed form, tail uniformity set(children)=={1-claim} and bed no-0-child asserted pointwise / D5 L-SB closed form vs BOTH engines / D6 published anchors / D7 plane-closure census z0..2 all k=1..8 / D8 C-SUM census (conjecture, obs-labeled) / D9 REFUTED recheck with the 'z=3 clean, z>=4 counters' expectation and the full 29-counter list frozen in obs / D10 cross-engine canonical-vs-ordered / D11 stress: far-m rows m13..25, spot planes z<=24, far diagonal z<=13 g<=24, far L-SB). Mutation battery 9/9 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), uh 5760 / du 972 / zd 1260 / ty 1502 / sb 2623 / ps 1941 / cs 2364 / rw 6, all rc=1 (ty=1502 not 1512 is the honest pre-declared count: the 10 z=0 bed cells whose flipped typed children stay off 0 legitimately pass — recorded in note 2.6). Audit artifacts published at 30bbcbb5 (audit_run1-4.out+.info, tamper 9 record files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 27 entries)."
  - "OPEN registrations (note SS5): O1 the transition window 1<=k<=z-1 (z>=3) — alternation half REFUTED, congruent half clean census (OBS-WC), the true window law is open; O2 bed window rows k=z-1 (z>=3) census-zero, unproved; O3 C-SUM thresholds by multiplicity + three-token typed generalization (future F1); F2 11x11 connection: the ENTIRE pair upper triangle k>=z (and beds k>=z) is now O(1)-evaluable on every plane; with K1303 this closes the whole k-axis for z<=2 and leaves only the window — pruning-lattice widening recorded for the giant-search owners, adoption decision belongs to them, as since K1286. 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed."
relations:
- type: resolves
  target: K1303
  note: "K1303 open 登録 O-G4「far above-diagonal k > 0 (untouched)」を全称完了。O-G4 の領域（対角行 k=z と上半 tail k≥z+1・全 plane）を T-UH/Z-DIAG で確定し、残る未確定を遷移窓 1≤k≤z−1 (z≥3) のみに縮小。engine pin は同一 chain bytes（bd5f22e4…・埋込み block・単体 582c93c1…）。"
- type: extends
  target: K1285
  note: "T-PS0/1/2 スライス（z0 k1..3 / z1 k2..3 / z2 k3..4 = [g odd]）は T-UH の部分族、T-ALM 六床は T-DU′ の部分族として全称昇格（機体 D6 で 1,941 点アンカー照合・bad 0）。両者の境界三角形 OBS-D9 の対角 3 脚は K1286 経由で Z-DIAG の z=0/1/2 instance。"
- type: extends
  target: K1286
  note: "T-Z1(1,·)（z1-k1）・T-Z2(2,·)（z2-k2）は Z-DIAG の z=1/z=2 instance として全 z へ昇格。C4（z2-k1 = [g odd]）は境界アンカーとして使用・T-B1/T-B2 の b1(1)=0・b2(2)=0 は T-DU′ 側・b1(0)=1・b2(1)=2 は T-DU′ の閾値下シャープネス照合。T-B0 は定義域 2m+j≥0 ガード付きで再照合。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,p,R)。本項は L-SB（tail 分支読み）と B-exit 境界読み v(g+1, z+1, g+z+1)（3 分岐: [g even]/2/[g odd]）・v(z+1,z+1,2z+1)=2・v(z+2,z+1,2z+2)=(z+1)%2・v(1,p,R)=1 (R≥2) を閉形式からの直接導出として使用。機体 D5 が x≤20・p≤14 で閉形式・両 engine の三方照合（2,623 点 bad 0）。"
- type: depends_on
  target: K1282
  note: "T-Q corner (m,m)@2m+1 z0 = 0 は T-DU′ の k=1 instance として被包（K1302/K1303 kit 用の板（engine pin chain bd5f22e4…・単体 582c93c1…）と同一 bytes を使用）。"
- type: related
  target: K1287
  note: "z2 pre-band 崩壊（C-SPA）レーンとの接続: 本項で上半（k≥z）が確定したことで、z≥3 の残る未確定は窓 1≤k≤z−1 のみ。窓の合同行（k≡z mod 2）は census で Z-DIAG 追従（OBS-WC・z13 まで）・非合同行は 29 反例で交互予想棄却。窓 typed 解析は K1287 の s=0 スライス包含との併用が本命。"
- type: related
  target: K1281
  note: "A手子の min 分類（fall/stair/compress）は K1281 §2.0 の規約に準拠。本項の帰納は予算 R 軸の joint packet（T-UH + Z-DU′ + T-DU′）で、K1285/K1286 の構文の上半頂点にあたる。"
artifacts:
- path: research/log/2026-11-24-pair-upper-collapse-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 eabcb742・着手時/出版時 HEAD 295b9505〔Part DW レーン・非接触〕・K1308 空き確認・K1306 (SLB) / K1307仮 (REMO) レーンとの非接触明記）。§1 主張一式（T-UH・T-DU′・Z-DIAG・L-SB・被包関係・面 z≤2 全 k 閉包・C-SUM 予想・REFUTED・OBS-WC/OBS-BW）・§2 手証明全文（2.0 帰納パケットと well-founded 性・2.1 T-UH 均一化・2.2 Z-DIAG case 表・2.3 T-DU′・2.4 L-SB と B-exit 境界読み・2.5 基底部・2.6 honest 電池設計記録：b0 定義域ガードと ty=1,502 の事前宣言）・§3 宣言前探索（E1–E9 凍結数値）・§4 機体宣言（counts 20,588・変異表 9 種事前宣言・predry sha d3e244f4…）・§5 open 登録 O1–O3/F1/F2・§6 主張の区別。証明の正本。
- path: research/experiments/pair-upper-20261124/
  role: machine
  note: 実験キット一式（出版 28959626・成果物 30bbcbb5）: README・verify_k1308.py (sha256 973c97a5…・engine pin bd5f22e4… ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1305 chain と同一 bytes)・explore_upper.py / explore_upper.out (84df9a1b…・E1–E9 凍結)・output dryrun1-4 (+.info・byte-identical d3e244f4…) + 公式監査成果物（audit_run1-4.out+.info・tamper 9 ファイル・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 27 entries・13/13 fetch-back byte 照合）。
- path: research/log/2026-11-24-pair-upper-collapse.md
  role: report
  note: 実行 log（宣言→キット→fetch-back 照合→公式 4 走→変異電池→成果物出版→K item・README bullet の全記録・受入判定・次課題）。
---

## 概要

K1303 が O-G4 として残した上半領域（対角行 k=z と上半 tail k≥z+1・全 plane）を
**4 本の全称定理**で確定した:

- **T-UH**: ペア (m, m+g) は k ≥ z+1 で [g odd] に安定化し、閾値 k=z+1 は正確。
- **T-DU′**: 床 (a,a) は k ≥ z で 0。z≤2 の閾値下非零（b1(0)=1・b2(1)=2）は
  K1286 公刊どおり。
- **Z-DIAG**: 対角行 k=z は 3 分岐則（[g odd] / 2 at g=z+1 / [g even]）で
  **全 plane** で確定（K1286 C1–C3 の対角 3 脚を同時に昇格）。
- **L-SB**: 単一トークン tail 読み v(x,p,x+j)=x%2 と B-exit 境界読み。

到達点として、**ペア・床とも面 z=0,1,2 の全ての k（到達可能な全予算域）が確定**した
（K1303 帯域 k≤0 + K1286 境界行 + 本 package の上半）。z≥3 の未確定は遷移窓
1 ≤ k ≤ z−1 のみ。宣言前探索で窓の偶奇交互予想（非合同行 = [g odd]）は
**29 反例で棄却**し、生き残った合同行（k ≡ z mod 2 の Z-DIAG 追従）を
census 観測 OBS-WC として登録した。

構造の鍵は **A 手子は k 不変・C 手子は k と z を同時に −1** という観測で、
上半主張族（T-UH + Z-DU′ + T-DU′）が予算 R−1 上の joint 強帰納で閉じる。
T-UH cell の全選択肢が 1−[g odd] に均一化される点は機体 D4 が
set(children) == {1−claim} として点ごと機械検証している。

## 主張の区分（過大主張の防止）

- 定理（全称証明・宣言ノート §2 に証明全文）: T-UH・T-DU′・Z-DIAG・L-SB・
  B-exit 境界読み。
- census 予想（未証明・全称主張しない）: C-SUM（tail = [S odd]・
  3 重 1,344 点 / 混合 840 点 / 4 重 180 点 bad 0・閾値構造は open）。
- 反例（honest 棄却）: 窓偶奇交互予想の非合同行半分（29 反例・z≥4・
  機体 obs に全リスト凍結・z=3 は clean）。
- 観測登録（未証明）: OBS-WC（合同行 Z-DIAG 追従・z3..13・1,296 点 clean）・
  OBS-BW（床 k=z−1 行は z≥3 で census 0）・E6b 混合 3 重の早期安定化。
- census は証明ではない: 20,588 点は定理の実機照合（bad 0）であり、
  定理の全称性は手証明によって成立する。

## 公式監査（publish-then-execute）

- 宣言 eabcb742（HEAD 295b9505・K1308 空き・K1306/K1307仮レーンと非接触）→
  機体 28959626 → fetch-back 13 ファイル sha256 byte 照合 + ノート全文照合 →
  公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2
  PYTHONHASHSEED=99/7）すべて rc=0・stdout byte-identical
  （sha256 d3e244f4… = 宣言どおり）。約 2.6 秒/走。
- counts `[5760, 972, 1260, 1512, 2623, 1941, 1440, 2364, 6, 1116, 1594]`・
  総計 20,588 点・bad 0・engine_gate PASS・D4 typed（主張表+閉形式のみで子構成・
  tail 均一化・床 no-0-child 点検証）・D5 両 engine 三方照合・
  D10 cross-engine 一致。
- 変異電池 9/9 検出・宣言どおり: engine rc=2（0ea47a80…）・uh 5760・du 972・
  zd 1260・**ty 1502**（宣言ノート §2.6 の honest 事前宣言値・z=0 床 10 cell の
  正当通過を含む）・sb 2623・ps 1941・cs 2364・rw 6（すべて rc=1）。
- 成果物出版 30bbcbb5（audit_run1-4.out+.info・tamper 9 レコード・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 27 entries）。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は全時点 UNKNOWN。
- ペア上半三角（k ≥ z・全 plane）が O(1) 評価可能になった。K1303 帯域と合わせ
  z≤2 は全 k 軸・z≥3 は窓を除く全 k 軸が O(1)。枝刈り格子の上方拡張として
  巨大レーンオーナーに記録する（採用判断はオーナー側・Part DW レーンと非接触）。

## 次課題（単一オーナー候補）

1. **F1**: 3 トークン以上の typed 上半解析（C-SUM 予想の単一コピー 3 重
   a<b<c からの全称化）。
2. **O1**: 遷移窓 1≤k≤z−1（z≥3）の真の法則（合同行 Z-DIAG 追従の全称化が
   本命候補・非合同行の構造は未決着）。
3. **O2**: 床窓行 k=z−1（z≥3）の消滅則の証明。
