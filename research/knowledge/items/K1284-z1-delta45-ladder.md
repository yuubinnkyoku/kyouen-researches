---
id: K1284
title: "z1 ラダー δ4/δ5 の確定: T-L4z1（z1-δ4 arm-1・max>=m+2 → 0）・L-Z5F（z1-δ5 ≠0・行内自己消費エンジン）・C-LS2/C-IIz1-2 の解決（(j,j+2)@δ3 = 2・クラスE@δ3 = 2 ちょうど）・T-ALPHA（z1-δ3 arm-1 完全分類: 2 ⟺ (m,m+2)・他 1）・床 G4z2/W411/BC5 パッケージ（publish-then-execute・宣言ノートに証明全文収録・13,120 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE package: the z1 ladder continues past delta-3 into delta-4/5 and closes both open conjectures left by K1283. Notation as in K1281-K1283 (m=min(X), mixed, arm-1 = mixed with mult(m)=1, class E = mixed with mult(m)>=2 and not arm-2; row-m band/diagonal/frontier/delta-k coordinates). T-L4z1 (main theorem, proved universally): for every j>=1 and every arm-1 mixed Y with max(Y)>=j+2: H(2j+4;Y;1)=0. This RESOLVES and STRENGTHENS the K1283 explore2 open candidate C-L4z1 ('high-gap arm-1 -> 0'): high-gap (no (j+1)-token) is a special case, and shapes carrying (j+1) plus a >=(j+2) token (class-II-type high rows) are ALSO 0, because the C-child probes the z0 plane where T-L3 gives 0 (high-gap, C-child 1) and T-II gives >=2 (class-II, C-child 1 XOR (>=2) which is never 0 since 1 XOR v = 0 iff v=1)."
  - "ENGINE (new structural mechanism, the core novelty): L-Z5F: for every m>=1 and U subset of [m+2,infty) nonempty with max(U)>=m+3: H(2m+5;(m,U);1) <> 0. The 0-witness of the z1-delta-5 node (2m+5, (m,U)) is a min-preserving move taking a token w>=m+3 to w-1>=m+2: the child IS a row-m z1-delta-4 arm-1 high node, which is 0 BY THE THEOREM OF THE SAME ROW (T-L4z1(m)). So the delta-5 nonzero region is fed by an IN-ROW self-consumption: T-L4z1(m) uses L-Z5F(m-1) (the fall child of the row-m delta-4 parent is exactly the row-(m-1) delta-5 shape (m-1, U') with U' subset [m+1,inf) = [(m-1)+2,inf) and max>=m+2=(m-1)+3), and L-Z5F(m) uses only T-L4z1(m). The induction ladder T-L4z1(1) -> L-Z5F(1) -> T-L4z1(2) -> ... is cycle-free (dependency graph in note 2.6/2.7); the fall information of row m is recycled into row m's own high-region value, in contrast to K1283's L-Z1F which consumed the PREVIOUS plane (z0) through the C-child. Row 1 base of T-L4z1: A-children = T-N0z1(1) != 0, B-children (token 1) = D@5z2 evaluated by the NEW floor BC5 (single: v(x,2,5)=1 for x>=3 and v(x,2,4)=0 for x>=2 via K0832 direct reading; multi min>=2: C-child 1 XOR F5 = 1 XOR 1 = 0 in opts, hence != 0), C-child = 1 XOR T-L3(1) = 1."
  - "RESOLUTIONS of the two open conjectures (both exactly): T-LS2: for every j>=1: H(2j+3;(j,j+2);1)=2 exactly — opts are {C: 1 XOR T-H1(j) = 0} U {stair (j,j+1)@2j+2 z1: T-H2(j) special = 1} U {fall (j-1,j+2)@2j+2 z1: row-(j-1) z1-delta-4 arm-1 with max = j+2 >= (j-1)+2, T-L4z1(j-1) = 0}; mex({0,1,0}) = 2. Row 1: fall absent (token 1), B-child (3,)@4z2 = v(3,2,4) = 0 (BC5-S), A-child (1,2)@4z1 = 1 (T-H2(1) special), C-child 1 XOR J1 = 0; mex({0,1,0}) = 2. C-LS2 CLOSED. T-IIz1-2: for every m>=2, class E at z1-delta-3: H = 2 exactly — opts are {C: 1 XOR T-E(m) = 1} U {stair child >= (m+2)-token: T-H2(m) generic = 0 since child mult(m)=q>=2 and sum >= 3m+1 >= 2m+2} U {compress child (m+1)->m: allm (m^{q+1}) -> T-E1(m) = 0, or mixed with mult>=3 -> T-H2 generic = 0} U {fall child (m-1, m^{q-1}, E')@2m+2 z1: row-(m-1) z1-delta-4 arm-1 with all E' tokens >= m+1 = (m-1)+2, T-L4z1(m-1) = 0}; opts = {0,1} with both present, mex = 2 exactly. C-IIz1-2 CLOSED. Note the fall child here needed the FULL max>=j+2 strength of T-L4z1 (class-E parents carry (m+1)-tokens, so a high-gap-only theorem would NOT close C-IIz1-2)."
  - "T-ALPHA (complete classification of the (alpha) class left open by K1283 observation (a)): for every m>=1, arm-1 mixed Y at (2m+3, z1): H = 2 iff Y = (m,m+2), else H = 1 (including (m,m+1)). Row-1: B-child U@4z2 = 0 either way (single: v(x,2,4)=0; multi min>=2: NEW floor G4z2 = 0), C-child = 1 XOR J1 = 0, compress child allm (1,1) = NEW floor W411 = 0, the ONLY 1-producing child is the stair (1,3)->(1,2) = T-H2(1) special; Y=(1,3): mex({0,0,1}) = 2, else mex({0}) = 1. Rows m>=2: C = 1 XOR T-H1(m) = 0, fall = T-L4z1(m-1) = 0 (all D tokens >= m+1 = (m-1)+2), min-preserving children = T-H2(m) generic 0 / allm child T-E1(m) = 0, and the (m,m+1) stair child is the ONLY 1 in the whole row; Y=(m,m+2): mex({0,0,1}) = 2, else mex({0}) = 1. This explains K1283's n0_hist {1:454, 2:196}: the arm-1 2-values come exactly from (m,m+2) shapes, the rest of the 2s from class E (-> T-IIz1-2) and arm-2 corners. Consistency: T-LS2 is the (m,m+2) branch of T-ALPHA plus the row-1 base; D3/D5 cross-check each other."
  - "NEW FLOORS (full proofs in note 2.1): G4z2 (budget-4 z2, multi min>=2 -> 0): A-children are G3z2-multi -> 1 (children stay multi, (1,1) impossible from a single 2), C-child = 1 XOR F4 = 1, opts {1}, mex 0. W411 (budget-4 z1, (1,1) -> 0): B-child (1,)@3z2 = v(1,2,3) = 1, C-child = 1 XOR F3((1^2)=0) = 1, opts {1}, mex 0. BC5 (budget-5 z2 row-1 B-children): single v(x,2,5)=1 (x>=3), v(x,2,4)=0 (x>=2); multi min>=2: C-child 1 XOR F5(multi z1 budget-4) = 1 XOR 1 = 0 in opts -> != 0. v-readings machine-checked (D6/D9 both engines) and against the independent reference implementation."
  - "OPEN registrations (finite observations, NOT claimed): C-Z5F1 (z1-delta-5 (m,U) value = 1 conjecture; census 480 points all 1; proving =1 needs the z0-delta-4 classification (C4b region, open); note claims only <> 0). C-PC1z1-d4 (z1-delta-4 pure-c1 family (j,(j+1)^c): census 30 points c=1 -> 1, c>=2 -> 0; proof blocked by the a-ladder (z1-delta-3 allm a=2 -> 0) and z0-delta-3 pure-c1 values (pure-count ladder, both open). z0-delta-4 arm-1 census (values {0,1} only, 2 ABSENT in 234 points; direct fall-child material for C-II2 (K1282 open); no claim made). Remaining opens inherited from K1282/K1283: z1-delta-3 arm-2 exact values, allm-delta-k ladder, z>=2 planes, F14b, C-II2."
  - "PROVENANCE (publish-then-execute, strongest form): single-owner declaration note published FIRST at 66f06ad2 (observed HEAD 70d79714, K1284 free, no competing declaration; first push attempt hit a fast-forward race with a parallel lane and was retried after re-fetching HEAD — honestly recorded), then a correction commit c5709b87 BEFORE any official run fixing a provenance typo: note section 3 quoted the pre-declaration exploration E1 hist as {0:860} where explore_k1284.out actually reads {0:812} (the 48 tall-giant points were outside the exploration script's histogram; bad array empty, all 860 points 0; the MACHINE declaration l4_hist {0:860} was always correct and unchanged — declared expectations 377acf93/70319949/counts [860,480,43,858,2506,683,420,463,4800,2007], total 13,120, bad 0). Machine kit frozen at 35706ae6, fetch-back verified byte-identical on all 13 kit files + the corrected note. Official runs executed AFTER publication from the FETCHED-BACK machine: 4 runs rc=0, stdout byte-identical sha256 703199490ea26659ab458d8498d94a9c3de45912d647451fadd6b93f2de0e64c = declared exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated trees /tmp with env -i x2 PYTHONHASHSEED 99/7, ~3.8 s/run). Declared totals matching measured EXACTLY: 13,120 comparisons / bad 0; l4_hist {0:860}, z5f_hist {1:480}, alpha_hist {1:2499, 2:7} (the 7 twos are exactly the (m,m+2) corners), ls2_val all 2 for j=1..11. Mutation battery 7/7 fail-closed exactly as pre-declared: --tamper-engine -> rc=2 (mutated sha 0ea47a80... != pin bd5f22e4...), l4/z5f/ls2/ii12/alpha/fl -> rc=1 bad=860/480/11/810/2506/322. Audit outputs + detcheck.json (OFFICIAL-PASS) + MANIFEST-sha256 (29 files, all fetch-back verified) published at 9c21ec47. Engine block byte-identical to the K1282/K1283 pinned block; pre-declaration cross-check of the standalone block against a freshly written independent reference implementation on 3,936 points bad 0."
relations:
- type: resolves
  target: K1283
  note: "K1283 が open 登録した予想2件を閉鎖: C-LS2 ((j,j+2)@z1-δ3 = 2 ちょうど → T-LS2) と C-IIz1-2 (クラスE@z1-δ3 = 2 ちょうど → T-IIz1-2。下界 >=2 から =2 へ精密化)。さらに open 観測 (a) (α) クラスの 1/2 混在構造を T-ALPHA として完全分類（2 ⟺ (m,m+2)・他は1・n0_hist {1:454,2:196} の 2 側を (m,m+2)+クラスE+arm-2 で説明）。explore2 open 候補 C-L4z1「high-gap arm-1 → 0」も T-L4z1 として解決・(j+1) トークン保持の高域形状まで拡張（max>=j+2）。"
- type: depends_on
  target: K1282
  note: "T-H1（T-LS2/T-ALPHA の C手子値 1 XOR 1 = 0）・T-L3・T-II（T-L4z1 の C手子追放: high-gap→0/C-II→>=2）・T-E（T-IIz1-2 の C手子 1 XOR 0 = 1）・F3/F4/F5（床 G4z2/W411/BC5-M の C手子計算）・J1（行1基底）・K0832 v 直読み（BC5-S）。"
- type: depends_on
  target: K1283
  note: "T-H2 generic/special（全定理の min 保持子・stair 子評価）・T-E1（compress 子 allm）・T-N0z1（T-L4z1 行1/帰納部の A手子非零）・床 G3z2/B2z3・行1基底 H2(1)/T-E1(1)。機体 header は K1283 kit と同一 engine block（pin bd5f22e4…）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)（BC5-S の v(x,2,5)=1・v(x,2,4)=0・W411 の v(1,2,3)=1・D6/D9 両 engine 照合）。"
- type: related
  target: K1270
  note: "z1 帯・窓定理の行底とならぶ δ 軸拡張。T-L4z1/L-Z5F により z1 面は δ2（完全分類）・δ3（mixed≠0 + arm-1 完全分類 + クラスE=2）・δ4（arm-1 高域=0）・δ5（(m,U) 高域≠0）まで O(1) 評価可能な列が揃い、窓から δ ラダーへの系統的延長が確立。"
- type: related
  target: K1254
  note: "z>=2 面・FR-X との接続面。床 G4z2 は z2 面に新しく加わり（multi min>=2 @4z2 → 0）、BC5 は z2 行1の B手子評価様式を与える。z=2 帯端シフトの一般形は open 継続。"
- type: related
  target: K1281
  note: "A手子 min 分類（保持/落下/stair/compress）は K1281 §2.0 の再掲をそのまま使用。T-B1′ 帯の外側（δ>=3）を本項が初めて系統的に確定。"
- type: related
  target: K1268
  note: "予想 C1（低 z 崩壊帯）の延長として、z=1 面の非崩壊領域（δ>=2）の値の構造が T-ALPHA により完全記述される（1 と 2 の分布則）。"
- type: related
  target: K1279
  note: "z10/z11 ストリップとは非接触（本項は z<=1）。C手子の直前 z 面消費（L-Z5F は行内自己消費という新机制）はストリップ梯子の B10/A10 と対比される構造観察。"
artifacts:
- path: research/log/2026-11-24-z1-delta45-ladder-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 66f06ad2・訂正 c5709b87〔E1 探査 hist 記載修正+push競合honest記録・宣言期待値は不変〕・観測 HEAD 70d79714・対抗宣言なし・K1284 空き確認済み）。定理 T-L4z1/T-LS2/T-IIz1-2/T-ALPHA・補題 L-Z5F・床 G4z2/W411/BC5-S/M・v 恒等の証明全文・依存グラフ（行ラダーの循環なし確認）・主張区分（C-Z5F1/C-PC1z1-d4/z0-δ4arm-1 census は open 登録）・protocol D1-D10・変異表・honest 記録を収録。証明の正本。
- path: research/experiments/z1-delta45-ladder-20261124/
  role: machine
  note: 実験キット一式（出版 35706ae6）: README・verify_k1284.py (sha256 377acf93... engine pin bd5f22e4... ゲート内蔵)・engine_block.py (582c93c1... K1283 kit と同一 bytes・独立参照実装 3,936 点突合 bad 0)・exploration {explore_k1284.py, explore_k1284.out: E1-E9・E7/E8 は open 登録 census}・output dryrun1-4 (+.info) + 公式監査成果物（出版 9c21ec47: audit_run1-4.json (+.info)・detcheck.json OFFICIAL-PASS・tamper 記録 7 ファイル・MANIFEST-sha256 29 files）。
- path: research/log/2026-11-24-z1-delta45-ladder.md
  role: report
  note: 実行 log（宣言→訂正→機体→fetch-back 公式監査→出版の全記録・fast-forward 競合の honest 記録・受入判定・次課題）。
---

## 概要

z1 ラダーを δ4/δ5 まで開拓し、K1283 が残した open 予想を2件とも
閉じた:

- **T-L4z1**: z1-δ4 の arm-1 高域（max>=m+2）は値 0 に全称確定。
  K1283 explore2 の open 候補 C-L4z1 の直接解決かつ強化
  （(j+1)-トークン保持の class-II 型高域まで含む）。
- **L-Z5F**: z1-δ5 の (m, U⊆[m+2,∞)) 高域は ≠0。0-witness が
  **同一行**の T-L4z1 を踏む「行内自己消費」構造で、落下情報が
  行 m 自己完結の高域値に回収される（K1283 L-Z1F の「C手子で
  直前 z 面を消費」と対比される新しい帰納エンジン）。
- **T-LS2 = C-LS2 解決**: (j,j+2)@z1-δ3 = **2 ちょうど**。
- **T-IIz1-2 = C-IIz1-2 解決**: クラスE@z1-δ3 = **2 ちょうど**。
  こちらは T-L4z1 の拡張形（max>=j+2）が本質的（high-gap のみでは
  落下子 (m−1, m^{q−1}, E′) の (m+1)-トークンを処理できない）。
- **T-ALPHA = K1283 open 観測 (a) の完全解決**: z1-δ3 arm-1 の値は
  **2 ⟺ (m,m+2)、他はすべて 1**。
- 新規床: G4z2（4z2 multi min>=2→0）・W411（(1,1)@4z1→0）・
  BC5（v(x,2,5)=1・v(x,2,4)=0・multi C手子=0 で非零）。

## 主張の区分（過大主張の防止）

- 定理（全称証明・ノート §2 に証明全文）: T-L4z1・L-Z5F・T-LS2・
  T-IIz1-2・T-ALPHA・G4z2・W411・BC5-S/M・v 恒等。
- 予想の解決（閉鎖）: C-LS2・C-IIz1-2・K1283 open 観測 (a)・
  explore2 候補 C-L4z1。
- open 登録（本項で新規）: C-Z5F1（δ5 値=1 予想・census 480 点全
  1・≠0 のみ主張）・C-PC1z1-d4（pure-c1@z1-δ4・c=1→1・c>=2→0
  観測・a-ladder と z0-δ3 pure-c1 が blockers）・z0-δ4 arm-1 census
  （値 {0,1} のみ・2 不在・C-II2 の fall 子資料・主張せず）。
- open 継承: z1-δ3 arm-2 精確値・allm-δk ラダー・z>=2 面・純カウント
  ラダー・F14b・C-II2。
- census は証明ではない: D1-D10 の 13,120 点は定理の実機照合
  （bad 0）であり、定理の全称性は証明によって成立する。

## 公式監査（publish-then-execute・fetch-back 機体から走行）

- 宣言 66f06ad2（+訂正 c5709b87・宣言期待値不変）→ 機体 35706ae6
  → fetch-back 13 ファイル byte 照合 → 公式 4 走（同一 cwd×2
  PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2 PYTHONHASHSEED=99/7）
  すべて rc=0・stdout byte-identical
  （sha256 70319949…= 宣言想定）。~3.8s/走。
- counts `[860, 480, 43, 858, 2506, 683, 420, 463, 4800, 2007]`・
  総計 13,120 点・bad 0・l4_hist {0:860}・z5f_hist {1:480}・
  alpha_hist {1:2499, 2:7}（2 側は (m,m+2) の7点のみ）・
  ls2_val j=1..11 全 2。
- 変異電池 7/7 検出（engine rc=2〔mutated sha 0ea47a80… ≠ pin〕・
  l4 860・z5f 480・ls2 11・ii12 810・alpha 2506・fl 322・
  すべて宣言どおり）。監査成果物は同一実験 dir に出版
  （commit 9c21ec47・detcheck.json OFFICIAL-PASS・
  MANIFEST-sha256 29 files・全 fetch-back byte 照合）。
- honest 記録: 初回宣言 push は並走レーンとの fast-forward 競合で
  失敗し HEAD 再取得後に成功（ノートに記録）・宣言ノート §3 の
  E1 探査 hist 記述 {0:860} が実出力 {0:812}（tall-giant 48点の
  hist 集計対象外）と不一致だったのを公式実行前に transparent な
  訂正コミット c5709b87 で修正（機体 D1 の宣言 l4_hist {0:860} は
  最初から正しく変更なし）。

## 11×11・規約への接続

- verdict 不消費・11×11 巨大探索の UNKNOWN は不変・Part CY/CP/
  DH/DA レーンと非接触。
- z1 部分木の O(1) 評価化が δ4/δ5 まで拡大（arm-1 δ4=0・
  (m,U) δ5≠0・δ3 は arm-1 とクラスE が精確値）。巨大レーンへの
  接続は記録のみ（採用判断は巨大レーンオーナー）。

## 次課題（単一オーナー候補）

1. **K1285 一次候補: z1-δ4 pure-c1 族 (j,(j+1)^c) の証明**
   （C-PC1z1-d4）。blockers: (j,j+1) の compress 子 =
   (j,j)@z1-δ3 allm a=2 → 0（a-ladder）と pure-c1 の C手子 z0-δ3
   値（z0-δ3-pure-c1 ≠1・純カウントラダー）。
2. C-Z5F1（δ5 値=1）: z0-δ4 分類（C4b 領域）が鍵。
3. z1-δ3 arm-2 の精確値・allm-δk ラダー・z>=2 面。
