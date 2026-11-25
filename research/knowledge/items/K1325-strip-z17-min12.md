---
id: K1325
title: "min>=12 クリティカルストリップ z=17 スライス (floor-12 = z−5): H(m+18;X;17)=v(ΣX,17,m+18)（床付き floor-12 セル梯子 F17f12..A517f12 の 11 全称補題 + T-Z17 + z=17 スライスの min>=12 全閉鎖・m=12 行は z∈{0..17} 確定で残余バンド内 z∈{18..21}・F 系第 8 尾形 (恒常 2 尾の再誕・+2 シフト)・吸収恒等式の s>=18 全域一様破れ = 恒常尾の供給源・死点化なし遷移 (初事象)・A RANK 4 段崩壊連鎖の破れ・第 3 連続帯域内底子 A517f12）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=17 slice (floor-12 = z-5, min>=12): for every m>=12 and every nonempty finite multiset X with min(X)=m, H(m+18;X;17)=v(sumX,17,m+18) (theorem T-Z17). With z*(m)=2m-2+(m mod 2) (K1268), z*(12)=22>17, so together with the published slice chain (low-min editions fixing z in {0..12}, T-Z13 z=13 min>=8, T-Z14 z=14 min>=9, T-Z15 z=15 min>=10, T-Z16 z=16 min>=11) and this theorem, the m=12 row is determined for ALL z in {0..17} (remaining in-band z in {18..21}, frontier z=22 open), and the z=17 slice is closed for ALL min>=12. The claim position offset is 18 = z+1 (same lattice as T-Z16's 17 and T-Z15's 16); the bottom m=12 is a trivial-absorption base whose a=12 child lands EXACTLY on the eleventh cell A517f12 (deviant-free, hence identically equal to the stair value v(S-1,17,29) for all S, supply-free collapse at the bottom), and all C-hand children land on published lines: rungs j in {1..10} on the K1322 z=16 cells (co-floor 11 ⊆ 12 subset argument) and the j=11 C-hand child (28;{11}∪Y;16) on the published T-Z16 m=11-row claim position R=11+16 EXACTLY -- and the K1320 out-of-domain D3 anchor issue is absent here because the j=11 dependency is itself re-anchored by the D3 m=11 column."
  - "floor-12 cell ladder (all 11 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+18;{j}∪Y;17) with all Y tokens >= 12, arity arbitrary, Y blank iff s=0, s in {0}∪{12..}): Lemma F17f12 = 1 at s=16 / 2 for all s>=18 / v(s+1,17,19) elsewhere including s=0 -- the F-family EIGHTH tail typology: a SINGLE below-collapse DOWN point at s=16 (1 < 2), a HOLE at s=17 (agreeing with collapse), and the constant-2 UP tail REBORN for all s>=18 (2 > 0); the s-profile is the exact +2 shift of the z=15 sixth form (DOWN at z-1 / hole at z / tail from z+1). The supply is NEW: the j=1 below-band B-move child H(18;Y;18)=v(s,18,18) (lemma BB', R=18<=18+min(Y)) whose absorption identity v(s,18,18)=v(s,17,18) holds on {0}∪{12..17} and BREAKS UNIFORMLY for all s>=18 (v(s,17,18)=1 vs v(s,18,18)=0, both constants) -- the break region's expression mode alternates across three consecutive slices (z=15: single-point break -> single deviant; z=16: uniform break absorbed at mex level; z=17: uniform break EXPRESSED at mex level as the constant tail = tail-supply alternation). The s=16 DOWN point is the mex-level inversion of the published F16f11 s=16 UP deviant (value 1 unchanged, direction flipped by the changed option multiset). Lemma G17f12 = 0 at s=16 DOWN only (the F-tail fully FLAT-absorbed at this rung; the published G16f11 s=14 DOWN supply also FLAT-exits), Lemma E17f12 (1 at s=14 DOWN / 2 at s=16 UP, two points), Lemma D17f12 (0 at s=14 DOWN only; the inherited s=12 DOWN class is FLAT-absorbed here -- a 4-slice lifespan from its z=14 birth in D14f9 through D15f10/D16f11), Lemma C17f12 (1 at s=12 DOWN -- the z=16 UP class direction-flipped / 2 at s=14 UP), Lemma B17f12 (0 at s=12 DOWN -- B16f11's UP:2 direction switch), Lemma A17f12 (2 at s=12 UP -- BREAKS the z=13..16 four-slice A-rank full-collapse chain; a structurally new ladder head), A217f12 = v(s+8,17,26), A317f12 = v(s+9,17,27), A417f12 = v(s+10,17,28), A517f12 = v(s+11,17,29) (FOUR consecutive full collapses; A517f12 is the T-Z17 absorption bottom and, at position (min=11, z=17) with z*(11)=21>17, the THIRD consecutive in-band base child after K1320 A315f10 and K1322 A416f11)."
  - "transition z=16 -> z=17 is the FIRST no-death transition of the series: the z=16 deviant positions {12,14,16} all lie at-or-above the new floor 12, so nothing dies by domain containment (death events #1 z=13->14 at s=8 and #2 z=15->16 at s=10 both killed below-floor positions); instead every surviving class restructures along the two supply laws visible in the ladder: an UP climb chain A@12 -> C@14 -> E@16 -> F-tail (s>=18) and a DOWN spread chain B@12 -> D@14 -> G@16. Census observations (declaration note sec.3, frozen bytes): the constant F-tail passes beyond the census window (tail spots s in {43..50}: exactly 8 F-row mismatches vs collapse, all engine==declared==2), in-band m=11 / m=10 rows at z=17 show 0 separations in 110 / 130 shapes (row statements still open), the m=8-row beyond separation set at z=17 is EXACTLY one point X=(8,10) DOWN at S=18 -- the first SHRINK event of the beyond series {z14:(8,8)UP} -> {z15:(8,8)DOWN} -> {z16:(8,8)DOWN+(8,10)UP} -> {z17:(8,10)DOWN} with UP/DOWN alternation (observation only), and the m=12 base spot value is 1 = v(24,17,30), differing from z=16's 0 (bottom-child token dependence, observation). The F-tail typology across z=10..17 is now 8 forms (death / rebirth / blister / constant / single / constant / single / constant) with strengthened alternation; the general classification law is open."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration exploration kit published FIRST by a parallel lane execution (commit 2c74f1c6: engine_block.py sha256 582c93c1... same bytes as the K1282..K1322 chain with startup pin gate bd5f22e4..., frozen explore_z17m12.py 410fea31... / explore_z17m12.out f3579f0d... determinism 3 byte-identical runs, re-verified locally from the published bytes, kit README 7,268 bytes, predecl log sha256 f8f8eef8...), declaration note de7b3065 (52,672 bytes, 751 lines, published sha256 ea500eb5..., full paper proofs in sec.2 disclosed before machine execution), verify machine 5a3c17f4 (verify_k1325.py sha256 17efe50098a4bd4d491978380d9118de6218365252f0f5ebd29488f29a6b4953, structural copy of verify_k1322.py with all diffs disclosed; kit README machine section appended), official outputs e5cc9f8e (official_runs/run1..run4.out each byte-identical sha256 571403b128cf7e391f6b5151bda819d40c2f5d5b0ef9839f4fc6f17e42f7219f = declared predry sha, detcheck.json OFFICIAL-PASS sha256 c7ff0854...). Declared battery 15,173 pts, all endpoints fail-closed (count mismatch itself FAILs): D1 cells 1,705 (11 cells x 155 exhaustive floor-12 shapes, s in {0}∪{12..42}, arity 0..4) / D2 strip 358 (m in {12..16}, census-mirroring sweep, cumulative counts 107/191/259/314/358 cross-checked against the frozen .out) / D3 z16 anchors 350 (10 published K1322 line transcriptions x 32 s-values on the K1322 floor-11 domain + 30 T-Z16 C-hand anchors m in {11..16}) / D4 stair anchors 341 / D5 self anchors 12,141 (single-token grid x in {1..30}, z in {0..18} INCLUDING z=18 for the (ii') v(s,18,18) evaluations and the tail-region constant pair v(s,17,18)/v(s,18,18), 21 R-points per pair + 171 empty anchors) / D6 deviant/collapse witnesses 22 (values, collapse targets AND directions, incl. the eighth-form hole and tail-birth witnesses) / D7 extension 101 (tail spots s in {43..50} x 11 cells with the 8 F-row entries DECLARED as engine==collapse-mismatch==2 pairs + 12 strip spots m in {17..20} + the m=12 base spot 1) / D8 below-band 155 (lemma-BB' supply source H(18;Y;18) vs v(s,18,18) over the full floor-12 census domain). First full machine run PASSed outright; predry 7 runs byte-identical (default, PYTHONHASHSEED=random/1/0 same cwd, 3x env -i isolated); official 4 runs all rc 0 byte-identical to the declared sha; tamper battery 8/8 fail-closed from the published bytes (engine rc 2 mutated sha != pin; cell/strip/anchor16/stair/deviant/ext/belowband rc 1 each flagging exactly the single declared gate). Honest record (declaration sec.6): this lane returned to HAND-CALCULATION-FIRST phase ordering (closed-form candidates derived on paper from K0832 branch computations BEFORE any machine cross-check -- the K1320/K1321 style, the inverse of K1322's drafting-support-first; the drafting-support script check_k1325_cases.py, 1,705 census shapes + 3,069 extended shapes s in {43..60} + 549 T-Z17 claim-position shapes m in {12..25} all 0 mismatch, was run AFTER the paper derivation); the env -i runs used /usr/local/bin/python3 explicitly from the first attempt (the K1322 rc-127 lesson) and no incidents occurred."
relations:
- type: depends_on
  target: K1322
  note: "z=16 floor-11 セル表 F16f11..A416f11 と定理 T-Z16 (min(X)=m>=11・主張位置 R=m+17) を本項証明の C 手供給源として直接引用 (co-floor 11 ⊆ 12 の部分集合引数)。j=11 段の C 手子 (28;{11}∪Y;16) は unpublished ではなく出版 T-Z16 の m=11 行主張位置そのもの (=v(s+11,16,28))。D3 battery が 10 線の転写 + T-Z16 C 手位置 (m ∈ {11..16}) を engine に独立再照合するため K1322 公式検証の状態は本項の妥当性に影響しない (K1320 で問題になった D3 域外依存は本機体では存在しない)。F16f11 の s=16 UP deviant の mex 反転 (s=16 DOWN)・A416f11 崩壊の j=10 段供給も引用。"
- type: depends_on
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2)。z*(12)=22>17 (系 1・閉鎖)・z*(11)=21>17 (A517f12 帯域内底子 = 第 3 連続) の判定と系 2 の残余バンド z∈{18..21}・前線 z=22 の特定に使用。"
- type: depends_on
  target: K1264
  note: "階段定理。セル梯子の Y 内 A 手子評価 (R子=j+17=z+min ちょうど)・補題 BB' ((18;Y;18) の R=18<=18+min(Y))・T-Z17 の (a>m) 子評価 (R=m+17=z+min 等号) に使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・(R+z)%2 中間枝。セル梯子の全場合計算・吸収恒等式 (s ∈ {0}∪{12..17} で成立・s>=18 で一様破れ v(s,17,18)=1 vs v(s,18,18)=0 = F17f12 恒常 2 尾の供給源)・s=16 単点 DOWN (F16f11 UP の mex 反転) の基盤。宣言 §6: 本レーンは手計算先行に回帰 (K1322 の drafting 支援先行との位相差を開示)。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1322 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置 H(R;();z)=0。補題 s0・s=0 列・帯域下子 (18;Y;18) の白紙位置評価・D5 の空位置アンカー 171 点に使用。"
- type: related
  target: K1320
  note: "F 系第 6 尾形 (恒常 2 尾・z=15) の +2 シフトが本項第 8 形態 (DOWN@z−1・穴@z・尾@z+1 の全構造一致)。ストリップ定理縦糸 T-Z13..T-Z17 の z=15 項。帯域内底子系列の第 1 項 A315f10 (min=9・z=15) も K1320。"
- type: related
  target: K1321
  note: "本レーン手計算先行型の直接の先行実例 (K1320/K1321 型・K1322 は drafting 支援先行)。z=15 で証明された床非感受性との対照: 本項は床 12 のみ主張し、floor-11 の z=17 観測は並走 z17-min11 kit (82f98ef4) として別出版 (A5 セル崩壊・本項§5 の m=11 行観測と非矛盾)。"
- type: related
  target: K1319
  note: "s=12 DOWN クラスの出生スライス (D14f9 表出) → D15f10/D16f11 継承 → 本項 D17f12 で FLAT 吸収の寿命 4 スライス。deviant クラスの段階寿命の一般則は open。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z17 の底 m=12 は自明吸収型 (a=12 子が帯域内底子 A517f12 に一致し deviant ゼロゆえ階段値と恒等的同値)。底類型系列の帯域内底子連鎖 (K1320 A315f10 → K1322 A416f11 → 本項 A517f12 の 3 連続) の決定則は open。"
artifacts:
- path: research/experiments/strip-z17-min12-20261125/explore_z17m12.py
  role: verifier
  commit: 2c74f1c6
  note: "凍結探索機体 (sha256 410fea31…・engine pin ゲート内蔵・先行並走レーンの出版)。11 セル census (155 形状/セル)・tail spots・strip m∈{12..16}・IN-BAND m=11/m=10 行 z=17 記録・m=8 beyond 記録・帯域下子 census・m=12 base spot を再現し宣言表と完全一致 (publish-then-execute の一次資料)。"
- path: research/experiments/strip-z17-min12-20261125/explore_z17m12.out
  role: data
  commit: 2c74f1c6
  note: "凍結探索出力 (sha256 f3579f0d…・決定性 3 走 byte-identical・multivalue 0 行・deviant 表が宣言どおり・本環境で出版 bytes から再実行し再確認)。"
- path: research/log/2026-11-25-z17m12-predecl-exploration.md
  role: log
  commit: 2c74f1c6
  note: "宣言前探査 log (sha256 f8f8eef8…・先行出版・本項の受領)。census 全数値・ハンドオフ宣言 (全依存出版済み・K スロット未主張) を含む。"
- path: research/experiments/strip-z17-min12-20261125/engine_block.py
  role: data
  commit: 2c74f1c6
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1322 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/experiments/strip-z17-min12-20261125/README.md
  role: log
  commit: 5a3c17f4
  note: "kit README (拡張前 7,268 bytes で先行出版 2c74f1c6・検証機体出版時に機体セクション追記・拡張版は 5a3c17f4 fetch-back 検証・census 記録と climb/spread 2 供給鎖の説明)。"
- path: research/log/2026-11-25-strip-z17-min12-single-owner-note.md
  role: declaration
  commit: de7b3065
  note: "単一オーナー宣言ノート (52,672 bytes・751 行・出版 sha256 ea500eb5…)。§1 主張 (11 補題 + T-Z17 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute・吸収恒等式破れの供給機構・mex 反転・死点化なし・A RANK break を含む)・§3 凍結探索・§4 宣言 battery 15,173 点 fail-closed + predry sha + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録 (z=18 第 9 尾形予測問題ほか)・§6 宣言前探査の全開示 (手計算先行の位相・小事象なし)・§7 次レーンへの申し送り。"
- path: research/experiments/strip-z17-min12-20261125/verify_k1325.py
  role: verifier
  commit: 5a3c17f4
  note: "専用検証機体 (sha256 17efe500…・verify_k1322.py の構造写し・差分全開示・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 15,173 点・変異 8 モード・点数過不足も即 FAIL・fetch-back byte 一致)。"
- path: research/experiments/strip-z17-min12-20261125/official_runs/run1.out
  role: data
  commit: e5cc9f8e
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 571403b1… で byte-identical・rc 0・overall_bad 0・battery 15,173 = 宣言・出版 bytes から fetch-back cmp 照合の上で実行)。"
- path: research/experiments/strip-z17-min12-20261125/detcheck.json
  role: data
  commit: e5cc9f8e
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 c7ff0854…・predry 7 走・公式 4 走・tamper 8 種・kit fetch-back の全実測と honest 注記〔手計算先行・公式 env -i は初回成功〕を記録)。"
- path: research/log/2026-11-25-strip-z17-min12.md
  role: log
  note: "完了 log (publish-then-execute chain 2c74f1c6→de7b3065→5a3c17f4→e5cc9f8e→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。"
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=12・min(X)=m を持つ空でない任意の有限多重集合 X に対して
  H(m+18;X;17)=v(ΣX,17,m+18) が成立するという全称命題 (proved・床付き floor-12
  (z−5) セル梯子 11 補題の K0832 場合計算 + 出版 z=16 表 (K1322) の引用
  (co-floor 11 ⊆ 12 部分集合引数・j=11 の C 手子 = 出版 T-Z16 m=11 行) +
  補題 BB' の帯域下子崩壊 (吸収恒等式 {0}∪{12..17} 成立・s>=18 全域一様破れ =
  F17f12 恒常 2 尾の供給源) + 死点化なし遷移 (z=16 deviant 位置 {12,14,16} ⊇
  床 12) + 底 m=12 の自明吸収 (第 3 連続帯域内底子 A517f12・deviant ゼロ) +
  選択肢集合一致帰納)。同一証明に含まれる数学的部品として Lemma F17f12
  (s=16 DOWN 1<2・s=17 穴・s>=18 恒常 UP 2>0 = F 系第 8 尾形・恒常尾の再誕
  ・z=15 第 6 形態の +2 シフト)・G17f12 (16 DOWN・F 尾の完全吸収)・E17f12
  (14 DOWN・16 UP)・D17f12 (14 DOWN・s=12 クラスの FLAT 吸収)・C17f12
  (12 DOWN 方向反転・14 UP)・B17f12 (12 DOWN 方向転換)・A17f12 (12 UP =
  A RANK 4 段崩壊連鎖の破れ)・A217f12/A317f12/A417f12/A517f12 (完全崩壊
  4 連続・A517f12 = 第 3 連続帯域内底子) も主張に含む。系として z=17 スライス
  の min>=12 全閉鎖と m=12 行の z∈{0..17} 確定が従う。m=11 行残余
  z∈{17..20} (floor-11 z=17 edition が open・IN-BAND m=11 行 110 形状 0 分離
  の観測のみ)、m=10 行 z=17 (floor-10 edition が open・130 形状 0 分離の
  観測のみ)、m>=13 行の z∈{18..z*(m)−1}、床の必要十分性、帯域下子の一般
  理論、F 系尾形の一般法則、死点化の発生条件、A RANK break の一般則、beyond
  分離集合の交代構造は open。11×11 盤面のいかなる勝敗も本項の範囲外 (二石
  root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費・battery 15,173 点は
  定理の実機照合であって証明の代替ではない)。

## 概要

K1322 (z=16 min>=11 スライス) の縦糸後継: z=17 min>=12 スライスを、先行出版済み
predecl kit (`2c74f1c6`) を受領して全称証明し出版した (publish-then-execute)。
K1322 とは逆に手計算先行 (K1320/K1321 型) に戻し、drafting 支援機械照合は
紙面誘導の後段に回した (§6 開示)。

- **T-Z17 (主定理)**: すべての m>=12・min(X)=m で H(m+18;X;17)=v(ΣX,17,m+18)。
  主張位置の lattice は T-Z15 (offset 16)・T-Z16 (offset 17) に続き offset 18
  (=z+1)。底 m=12 は自明吸収型 (a=12 子 = A517f12・deviant ゼロ)・m>=13 は
  選択肢集合一致帰納。
- **A517f12 = 第 3 連続帯域内底子**: 小トークン 11 (z*(11)=21>17) の 11 段目
  セルが完全崩壊し、T-Z17 の底の子として階段値と恒等的同値になる (K1320
  A315f10・K1322 A416f11 に続き)。11 段梯子はストリップ系列最長を更新。
- **F 系第 8 尾形 (恒常 2 尾の再誕)**: deviant は s=16 DOWN 単点 (F16f11 UP の
  mex 反転)・s=17 穴・s>=18 恒常 UP 2 尾。供給源は補題 BB' (帯域下子
  v(s,18,18)) の吸収恒等式の s>=18 全域一様破れ (1 vs 0) が mex レベルで表出
  — 破れ領域の表出様式は z=15 (1 点表出)・z=16 (mex 吸収)・z=17 (全表出) と
  3 スライス連続で交替 (尾の供給源交替則・open)。
- **死点化なし遷移 (初事象) **: z=16 deviant 位置 {12,14,16} はいずれも床 12
  以上で域包含死なし。代わりに全クラスが再構成し、UP climb 鎖 (A@12→C@14→
  E@16→F 尾) と DOWN spread 鎖 (B@12→D@14→G@16) の 2 供給法則が梯子全体に
  観測される。**A17f12 UP:2 は z=13..16 の A RANK 4 段完全崩壊連鎖を破る**
  (構造的に新しい梯子頭)。
- **系**: z=17 スライス min>=12 全閉鎖 (z*(12)=22>17)。m=12 行 z∈{0..17}
  確定・残余バンド内 z∈{18..21}・前線 z=22。

機体と検証は publish-then-execute で完全出版: 宣言ノート (751 行・紙面証明全文
を機械実行前に先行開示) → 検証機体 verify_k1325.py (宣言 battery 15,173 点・
D8 帯域下子 gate が補題 BB' の供給源を独立担保) → 公式 4 走 (出版 bytes
fetch-back cmp 照合から byte-identical 全 rc 0・overall_bad 0・点数過不足
fail-closed) + tamper 8/8 fail-closed → detcheck.json OFFICIAL-PASS。
手計算先行への回帰 (drafting 支援 check_k1325_cases.py を紙面誘導後・
1,705+3,069+549 形状 0 不一致) を §6 に誠実開示。11×11 空盤・二石 root・
S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費 (battery 点数は定理の実機
照合であって証明の代替ではない)。
