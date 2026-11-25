---
id: K1322
title: "min>=11 クリティカルストリップ z=16 スライス (floor-11 = z−5): H(m+17;X;16)=v(ΣX,16,m+17)（床付き floor-11 セル梯子 F16f11..A416f11 の 10 全称補題 + T-Z16 + z=16 スライスの min>=11 全閉鎖・m=11 行は z∈{0..16} 確定で残余バンド内 z∈{17..20}・F 系第 7 尾形 (単点 UP・尾の完全消滅)・死点化第 2 事象の域包含論証・第 2 連続帯域内底子 A416f11）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=16 slice (floor-11 = z-5, min>=11): for every m>=11 and every nonempty finite multiset X with min(X)=m, H(m+17;X;16)=v(sumX,16,m+17) (theorem T-Z16). With z*(m)=2m-2+(m mod 2) (K1268), z*(11)=21>16, so together with the published slice chain (low-min editions fixing z in {0..12}, T-Z13 fixing z=13 for min>=8, T-Z14 fixing z=14 for min>=9, T-Z15 fixing z=15 for min>=10) and this theorem, the m=11 row is determined for ALL z in {0..16} (remaining in-band z in {17..20}, frontier z=21 open), and the z=16 slice is closed for ALL min>=11. The claim position offset is 17 = z+1 (same lattice as T-Z15's 16 and T-Z14's 15); the bottom m=11 is a trivial-absorption base whose a=11 child lands on the SECOND consecutive in-band base child A416f11 (min=10, z*(10)=18>16, fully collapsing), and all C-hand children land on published lines: rungs j in {1..9} on the K1320 z=15 cells (co-floor 10 superset argument) and the j=10 / row-m C-hand on the published T-Z15 claim position R=m+16 EXACTLY -- the dependency recheck (offset m+16 vs m+15 confusion, resolved by re-reading K1320 sec.2.11) is honestly recorded in the declaration note sec.6."
  - "floor-11 cell ladder (all 10 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+17;{j}∪Y;16) with all Y tokens >=11, arity arbitrary, Y blank iff s=0, s in {0}∪{11..}): Lemma F16f11 = 1 at s=16 and v(s+1,16,18) elsewhere -- the F-family SEVENTH tail typology: a SINGLE above-floor UP point and NO tail at all; the z=15 sixth-form constant-2 tail is fully absorbed in the uniform region s>=17 (options constants {1,2,3}, mex 0 = W), the supply being the lemma-BB below-band j=1 B-move child H(17;Y;17)=v(s,17,17) whose absorption identity v(s,17,17)=v(s,16,17) holds on {0}∪{11..15} and BREAKS at s=16 (v(16,16,17)=2 vs v(16,17,17)=0) in collision with the z=15 F-tail value 2 (option 3). Lemma G16f11 (0 at s=14 DOWN -- the published G15f10 DOWN survives the floor raise; 2 at s=16 UP -- the F16f11 UP propagates), Lemma E16f11 (1 at s=14 UP only -- the E15f10 s=12 DOWN supply is absorbed, restructured), Lemma D16f11 (0 at s=12 DOWN, 2 at s=14 UP NEW), Lemma C16f11 (1 at s=12 UP -- C15f10's s=10 DOWN class dies but its s=12 UP survives), Lemma B16f11 (2 at s=12 UP -- B15f10's dead s=10 DOWN class replaced, direction switch), Lemma A16f11/A216f11/A316f11/A416f11 (NO deviants, FOUR consecutive full collapses; A416f11 = v(s+10,16,27) is the second consecutive in-band base child and the T-Z16 absorption bottom)."
  - "death event #2 (second of the series) proved by domain containment: every z=15 source position s=10 (C15f10/B15f10/A15f10) lies below the new floor 11 and NEVER appears anywhere in the z=16 slice (the z=13->z=14 s=8 event was the first); the s in {12,14} sources survive restructured and a NEW s=16 deviant class enters (F/G only) -- supplied by the below-band absorption break, a mechanism no prior slice had (at z=15 the below-band child faithfully replicated the stair on its whole in-domain range). The general floor question (is min(Y)>=z-5 necessary and sufficient) gains its 4th affirmative sufficiency data point (z=13..16 at floors z-5), with the parallel z15-min8 kit (commit 232385bd) providing the below-classical-floor side data; z=16 F-form deviant structure {s=16 UP:1} is floor-INSENSITIVE across floors 9 (parallel z16-min9 kit observation, commit 5b2212cb) and 11 (this item), mirroring the floor-insensitivity proved at z=15 (K1321)."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration exploration kit published FIRST by a parallel lane execution (commit e0ca8d75: engine_block.py sha256 582c93c1... same bytes as the K1282..K1321 chain with startup pin gate bd5f22e4..., frozen explore_z16pre.py 87f3bb71... / explore_z16pre.out 16b10d0b... determinism 3 byte-identical runs, kit README extended sha 900c983f..., predecl log 30810222...), declaration note fd760f346ebe6eaff089b23c2dcba8ffc09e6d1c (published note sha256 e735e2d84dd60786a5d683e07fab43ac0ec8198cae827752b947e830142e5ab2, 47,024 bytes, 679 lines, full paper proofs in sec.2 disclosed before machine execution), verify machine cb105a1b (verify_k1322.py sha256 27e37152896a67798ab7cdf13e08fd2d5b80b4960bbceb7ea00025e87a96097c), official outputs 70c7322d (official_runs/run1..run4.out each byte-identical sha256 e0c6559f523f768204e7704e5e9ce42022d694d680bb059fef515f6d34bbad04 = declared predry sha, detcheck.json OFFICIAL-PASS sha256 fe3af36f...). Declared battery 13,293 pts, all endpoint fail-closed (count mismatch itself FAILs): D1 cells 1,830 (10 cells x 183 exhaustive floor-11 shapes, s in {0}∪{11..41}, arity 0..4) / D2 strip 456 (m in {11..15}, census-mirroring sweep) / D3 z15 anchors 322 (9 published K1320 line transcriptions x 33 s-values + 25 T-Z15 C-hand anchors m in {11..15}) / D4 stair anchors 310 / D5 self anchors 10,080 (single-token grid x in {1..29}, z in {0..17} incl. z=17 for the (ii') evaluations, 19 R-points per pair + 162 empty anchors) / D6 deviant/collapse witnesses 19 (values, collapse targets AND directions) / D7 extension 93 (tail spots x 10 cells + strip spots m in {16..19} + m=11 base spot) / D8 below-band 183 (lemma-BB supply source H(17;Y;17) vs v(s,17,17) over the full floor-11 census domain). First full machine run PASSed outright; predry 7 runs byte-identical (default, PYTHONHASHSEED=random/1/0 same cwd, 3x env -i isolated); official 4 runs all rc 0 byte-identical to declared; tamper battery 8/8 fail-closed from published bytes (engine rc 2; cell/strip/anchor15/stair/deviant/ext/belowband rc 1 each flagging exactly the single declared gate). Honest record (declaration sec.6): this lane used UNPUBLISHED drafting-support scripts (check_k1322_cases.py: closed-form-vs-engine over all 1,830 census shapes, 0 mismatches; cases_table.py: option-value tables transcribed into sec.2; sweep_tz16.py: T-Z16 claim-position sweep m in {16..25}, 235 shapes, 0 violations) BEFORE writing the paper proofs -- the derivation-first vs machine-first phase difference from K1320/K1321 is explicitly disclosed; the T-Z15 claim-offset (R=m+16) mid-drafting confusion and its resolution is recorded; the predry env -i runs initially targeted /usr/bin/python3 (rc 127, empty output) and were corrected to /usr/local/bin/python3 (official runs used the correct path from the start)."
relations:
- type: depends_on
  target: K1320
  note: "z=15 floor-10 セル表 F15f10..A315f10 と定理 T-Z15 (min>=10・主張位置 R=m+16) を本項証明の C 手供給源として直接引用 (co-floor 10 ⊆ 11 の部分集合引数・床不感受性は不要)。§7 ハンドオフ由来の predecl census kit を並走レーンが先行出版 (e0ca8d75) し本項が受領。本項は z=14 表 (K1319) は直接使わず (K1320 が z=14 表を使ったのと同型に K1320 表を使う)。D3 battery が 9 線の転写を engine に独立再照合するため K1320 公式検証の状態は本項の妥当性に影響しない。"
- type: depends_on
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2)。z*(11)=21>16・z*(10)=18>16 (第 2 連続帯域内底子) の判定と系 1/2 の残余 z∈{17..20} の特定に使用。"
- type: depends_on
  target: K1264
  note: "階段定理。セル梯子の Y 内 A 手子評価 (R=j+16=z+min ちょうど)・補題 BB ((17;Y;17) の R=17<=17+min(Y))・T-Z16 の (a>m) 子評価 (R=m+16=z+min 等号) に使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。セル梯子の全場合計算・吸収恒等式 ({0}∪{11..15} で成立・s=16 で破れ)・T-Z16 単一側選択肢集合算出の基盤。宣言 §6: 本レーンは drafting 支援機械照合を整文に先行 (K1320/K1321 の手計算先行との位相差を開示)。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1321 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置 H(R;();z)=0。補題 s0・s=0 列・帯域下子 (17;Y;17) の白紙位置評価・D5 の空位置アンカーに使用。"
- type: related
  target: K1321
  note: "F 系尾形の床非感受性の対照。z=15 では床 10/9 で第 6 形態 (恒常 2 尾) が不変 (K1321 証明)・z=16 では床 11 (本項) と床 9 (z16-min9 kit 観測) で第 7 形態 {s=16 UP} が一致 — 2 スライス連続の床非感受性観測。死点化の域包含論証は本項が 2 例目 (z=13→14 の s=8 に続き z=15→16 の s=10)。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z16 の底 m=11 は自明吸収型 (a=11 子が帯域内底子 A416f11 に一致し deviant ゼロゆえ階段値と恒等的同値)。底類型系列 (自明吸収→deviant 吸収→TOLERANT-ABSORPTION→自明吸収+フル梯子依存→同+帯域内底子 (K1320)→同+第 2 連続帯域内底子 (本項)) の決定則は open。"
artifacts:
- path: research/experiments/strip-z16-min11-20261125/explore_z16pre.py
  role: verifier
  commit: e0ca8d75
  note: "凍結探索機体 (sha256 87f3bb71…・explore_z15pre.py からの開示 diff 適用・engine pin ゲート内蔵・先行並走レーンの出版)。10 セル census (183 形状/セル)・tail spots・strip m∈{11..15}・帯域内 m=10 行 z=16 記録・帯域下子 census・m=11 base spot を再現し宣言表と完全一致。(publish-then-execute の一次資料)"
- path: research/experiments/strip-z16-min11-20261125/explore_z16pre.out
  role: data
  commit: e0ca8d75
  note: "凍結探索出力 (sha256 16b10d0b…・決定性 3 走 byte-identical・multivalue 0 行・deviant 表が宣言どおり)。"
- path: research/log/2026-11-25-z16-predecl-exploration.md
  role: log
  commit: e0ca8d75
  note: "宣言前探査 log (sha256 30810222…・先行出版・本項の受領)。census 全数値・honest note (docstring の s=12 死点予測の誤りを凍結前に訂正) を含む。"
- path: research/experiments/strip-z16-min11-20261125/engine_block.py
  role: data
  commit: e0ca8d75
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1321 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/experiments/strip-z16-min11-20261125/README.md
  role: log
  commit: cb105a1b
  note: "kit README (拡張前 sha256 c1e63235… で先行出版・検証機体出版時に機体セクション追記・拡張版 sha256 900c983f…・census 記録と battery/実行構成の説明)。"
- path: research/log/2026-11-25-strip-z16-min11-single-owner-note.md
  role: declaration
  commit: fd760f34
  note: "単一オーナー宣言ノート (47,024 bytes・679 行・出版 sha256 e735e2d8…)。§1 主張 (10 補題 + T-Z16 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute)・§3 凍結探索・§4 宣言 battery 13,293 点 fail-closed + predry sha + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録・§6 宣言前探査の全開示 (honest)・§7 次レーンへの申し送り。"
- path: research/experiments/strip-z16-min11-20261125/verify_k1322.py
  role: verifier
  commit: cb105a1b
  note: "専用検証機体 (sha256 27e37152…・verify_k1320.py の構造写し・差分全開示・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 13,293 点・変異 8 モード・点数過不足も即 FAIL・fetch-back byte 一致)。"
- path: research/experiments/strip-z16-min11-20261125/official_runs/run1.out
  role: data
  commit: 70c7322d
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 e0c6559f… で byte-identical・rc 0・overall_bad 0・counts 13,293 = 宣言・出版 bytes から fetch-back cmp 照合の上で実行)。"
- path: research/experiments/strip-z16-min11-20261125/detcheck.json
  role: data
  commit: 70c7322d
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 fe3af36f…・predry 7 走/公式 4 走/tamper 8 種/kit fetch-back の全実測・honest 注記 (predry env -i の python パス事故と訂正) を記録)。"
- path: research/log/2026-11-25-strip-z16-min11.md
  role: log
  note: "完了 log (publish-then-execute chain e0ca8d75→fd760f34→cb105a1b→70c7322d→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。"
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=11・min(X)=m を持つ空でない任意の有限多重集合 X に対して
  H(m+17;X;16)=v(ΣX,16,m+17) が成立するという全称命題 (proved・床付き floor-11
  (z−5) セル梯子 10 補題の K0832 場合計算 + 出版 z=15 表 (K1320) の引用
  (co-floor 部分集合引数) + 補題 BB の帯域下子崩壊 (吸収恒等式 {0}∪{11..15}
  と s=16 破れ = F16f11 単点 UP の供給源) + 死点化第 2 事象の域包含論証 +
  底 m=11 の自明吸収 (帯域内底子 A416f11・deviant ゼロ) + 選択肢集合一致帰納)。
  同一証明に含まれる数学的部品として Lemma F16f11 (s=16 単点 UP のみ =
  F 系第 7 尾形・恒常尾の完全消滅・s>=17 一様吸収)・G16f11 (14 DOWN・16 UP)・
  E16f11 (14 UP・s=12 DOWN の新吸収による再構成)・D16f11 (12 DOWN・14 UP 新規)・
  C16f11 (12 UP)・B16f11 (12 UP・方向転換)・A16f11/A216f11/A316f11/A416f11
  (完全崩壊 4 連続・A416f11 = 第 2 連続帯域内底子) も主張に含む。系として
  z=16 スライスの min>=11 全閉鎖と m=11 行の z∈{0..16} 確定が従う。
  m=10 行残余 z∈{16..17} (z*(10)=18; z=16 行文は floor-10 edition が open)、
  m=9 行 z=16 (floor-9 edition が open・census 5b2212cb 出版済み)、
  m>=12 行の z∈{17..z*(m)−1}、床の必要十分性、帯域下子の一般理論、
  F 系尾形の一般則、死点化の発生条件、底類型の決定則は open。
  11×11 盤面のいかなる勝敗も本項の範囲外 (二石 root・S2・class 1/2/4 は全時点
  UNKNOWN・verdict 不消費・battery 13,293 点は定理の実機照合であって証明の
  代替ではない)。

## 概要

K1320 (z=15 min>=10 スライス) の縦糸後継: z=16 min>=11 スライスを、先行出版済み
predecl kit (`e0ca8d75`) を受領して全称証明し出版した (publish-then-execute)。

- **T-Z16 (主定理)**: すべての m>=11・min(X)=m で H(m+17;X;16)=v(ΣX,16,m+17)。
  主張位置の lattice は T-Z14 (offset 15)・T-Z15 (offset 16) に続き offset 17
  (=z+1)。底 m=11 は自明吸収型・m>=12 は選択肢集合一致帰納。
- **A416f11 = 第 2 連続帯域内底子**: 小トークン 10 (z*(10)=18>16) の 10 段目
  セルが完全崩壊し、T-Z16 の底の子として階段値と恒等的同値になる (K1320 の
  A315f10 に続き 2 スライス連続)。10 段梯子はストリップ系列最長。
- **F 系第 7 尾形 (単点 UP・尾の完全消滅)**: deviant は s=16 の 1 点のみ。
  z=15 の恒常 2 尾は s>=17 全域で一様に吸収される (options {1,2,3} → mex 0)。
  供給源は補題 BB (帯域下子 (17;Y;17)=v(s,17,17)) の吸収恒等式の破れ
  (s=16) と z=15 F 尾の mex レベル衝突 — 帯域下子が「単点」を生む初の事例
  (z=15 では恒常尾を生んだ)。
- **死点化第 2 事象**: z=15 の s=10 供給クラス (C15/B15/A15) は床 11 の定義域
  外で全滅 (域包含の全称論証・z=13→14 の s=8 に続き 2 例目)。s∈{12,14} は
  存続しつつ再構成 (E の s=12 DOWN は吸収消滅・D に s=14 UP 新規・B は
  DOWN→UP 方向転換)。
- **系**: z=16 スライス min>=11 全閉鎖 (z*(11)=21>16)。m=11 行 z∈{0..16}
  確定・残余バンド内 z∈{17..20}・前線 z=21。

機体と検証は publish-then-execute で完全出版: 宣言ノート (679 行・紙面証明全文
を機械実行前に先行開示) → 検証機体 verify_k1322.py (宣言 battery 13,293 点・
D8 帯域下子 gate が補題 BB の供給源を独立担保) → 公式 4 走 (出版 bytes
fetch-back cmp 照合から byte-identical 全 rc 0・overall_bad 0・点数過不足
fail-closed) + tamper 8/8 fail-closed → detcheck.json OFFICIAL-PASS。
drafting 支援機械照合 (1,830 census 形状・0 不一致) を整文に先行させて使った
こと (K1320/K1321 の手計算先行との位相差) と T-Z15 主張位置の再確認を §6 に
誠実開示。11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict
不消費 (battery 点数は定理の実機照合であって証明の代替ではない)。
