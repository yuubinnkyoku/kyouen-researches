---
id: K1320
title: "min>=10 クリティカルストリップ z=15 スライス (floor-10): H(m+16;X;15)=v(ΣX,15,m+16)（床付き floor-10 セル梯子 F15f10..A315f10 の 9 全称補題 + 自明吸収底 + 選択肢集合一致帰納の全称証明・T-Z14 ハンドオフ T-Z15 の完走・z=15 スライスの min>=10 全閉鎖・m=10 行は z∈{0..15} 確定で残余バンド内 z∈{16,17}・帯域内底子と帯域下供給源の初観測）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=15 slice (floor-10, min>=10): for every m>=10 and every nonempty finite multiset X with min(X)=m, H(m+16;X;15)=v(sumX,15,m+16) (theorem T-Z15). With z*(m)=2m-2+(m mod 2) (K1268), z*(10)=18, so together with the published slice chain (low-min T-Z6..T-Z12 fixing z in {0..12}, T-Z13 fixing z=13 for min>=8, T-Z14 fixing z=14 for min>=9, each covering 10) and T-Z15, the m=10 row is determined for ALL z in {0..15} (remaining in-band z in {16,17} open), and the z=15 slice is closed for ALL min>=10 (every m>=10 has z=15 in band since z*(m)>=z*(10)=18>15)."
  - "floor-10 cell ladder (all 9 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+16;{j}∪Y;15) with all Y tokens >=10, arity arbitrary, Y blank iff s=0, s in {0}∪{10..}): Lemma F15f10 (F15f10(s)=H(17;{1}∪Y;15) equals 2 at s=14 / v(s+1,15,17) otherwise including s=0 and s=15: the F-family SIXTH tail form -- CONSTANT 2 for ALL s>=16, with a clean HOLE at s=15 (tail gap) and a single DOWN 1<2 at s=14, the first tail whose supply source is the BELOW-BAND j=1 B-move child (16;Y;16)=v(s,16,16), i.e. a below-band position acting as a LIVE supply source of a ladder for the first time in the series), Lemma G15f10 (0 at s=14, else v(s+2,15,18): single DOWN 0<1 at s=14, and the F constant-2 tail (s>=16) is FULLY absorbed at this rung -- the G-rung absorption law K1317 sec.2.3 survives the supply-source handover), Lemma E15f10 (1 at s=12, 2 at s=14, else v(s+3,15,19)), Lemma D15f10 (0 at s=12, else v(s+4,15,20)), Lemma C15f10 (1 at s=10, 2 at s=12, else v(s+5,15,21)), Lemma B15f10 (0 at s=10, else v(s+6,15,22)), Lemma A15f10 (2 at s=10, else v(s+7,15,23); single UP 2>0 at s=10), Lemma A215f10 (v(s+8,15,24) with NO deviants, fully collapsed), Lemma A315f10 (v(s+9,15,25) with NO deviants, fully collapsed; small token 9 is the FIRST IN-BAND base child of the strip series (min=9 is in-band for z=15 since z*(9)=17>15, in contrast to the on-frontier bases of T-Z13 min=8 / T-Z14 min=9); corollary (rephrasing): at the min=9 z=15 claim position H(25;X;15) the value is v(sumX,15,25) whenever the second-smallest token is >=10 -- co-token-9 shapes are OUTSIDE this claim (the full min=9 row H(25;X;15)=v(sumX,15,25) is open; the predecl-observed 152 in-band m=9-row z=15 shapes with separation 0 are an observation, not a claim)."
  - "proof technique (per-rung induction making every option s-only, extending the K1319 z=14 machinery to z=15, ladder length 8 -> 9): for each rung j in {1..9} with P_j=(j+16;{j}∪Y;15) the option set is exactly (i) an A-move on a Y-internal token a>=10: R_child=j+15=z+min exactly, so the K1264 stair (equality case) gives v(s+j-1,15,j+15), (ii) the A-move on the small token j landing on the NEXT-LOWER rung cell P_{j-1} at UNCHANGED s (bottom-up 9-rung induction; at j=1 the B-move removing the 1 gives the below-band child H(16;Y;16)=v(s,16,16) universally, including s=0: Lemma BB = the (B3) stair at R=16<=16+min(Y) plus (B2) direct application, with the ABSORPTION IDENTITY v(s,16,16)=v(s,15,16) holding exactly for s in {0}∪{10..15} and BREAKING at s>=16 -- the break being the supply source of the F15f10 constant-2 tail, requiring no new mathematical part), and (iii) the C-move = the published z=14 min=j line (K1319 cells F14f9..A214f9 for j=1..8 with the floor-9 domain {0}∪{9..} covering the floor-10 points used here, and the T-Z14 theorem line at m>=9 for j=9 -- roughly 267 of the 9339-battery points), so every Cell_j value depends only on s. NO DEATH-POINT DEACTIVATION this slice: the z=14 supply sources sit at s in {10,12,14}, ALL at or above the floor 10, so every one of them survives (in contrast to z=14 where the z=13 sources at s=8 died under the floor); the K0832 case computation closes each rung. Theorem T-Z15 base m=10 is TRIVIAL ABSORPTION: the a=10 child is exactly the A315f10 cell which has NO deviants, so the option set is identically the stair value set for every S (K1274/K1275 typology) -- yet TWO structural novelties: (a) the base child (min=9) is IN-BAND for the first time, and (b) the ladder still requires the FULL 9 rungs because the universal proof of A315f10 itself references all lower rungs down to the below-band child; the last rung's live supply source is below-band for the first time. The m>=11 step is option-set identity: {v(S-1,15,m+15)} (a>m children at the stair edge R=z+min exactly, a=m child the induction hypothesis T-Z15(m-1) at R=m+15=(m-1)+16) and {1^v(S,14,m+15)} (C-move child, the published T-Z14 line at m>=10) matching the single-token side exactly."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration exploration kit published FIRST by a prior lane execution (commit f547c174: engine_block.py sha256 582c93c1... same bytes as the K1282..K1319 chain with startup pin gate bd5f22e4..., frozen explore_z15pre.py 3e2a8ab863212efc3806a6acb93caeb7c9020ead468e1afa9cb6ffd4c2714513 / explore_z15pre.out 2cf0a9664f46c2c1eff27e387a20d32b16eebb5cd45a19335f397bd9eb30dfe7 determinism 3 byte-identical runs, kit README a4628eb1..., predecl log 944fdf79c3590e3927ec3b5500e60b759ce13ace1e8f68f6bbe69795730da6f8), declaration note 671ca6babe32aa5f2718ca20d046d5d8ac1d0f60 (sha256 fbfb6bb999fae6f83754afa88c5c6874e26b53463c6e3512d38f2f819a26de24, 48,667 bytes, 701 lines, full paper proofs in sec.2 disclosed before machine execution), verify kit 8ee5330b00591010b6fbf67de5c2ad8d9d49fdb4 (verify_k1320.py 081fe719a3274c25719c8149beefdcf724e381b2cc025bc582e9d2e28936c7e4, kit README extended sha256 bb22f3041c11d0c9442d53b5add5318715916f90d842a3699fb484a6668de251), published official outputs 0e4bfab24a1419f829b8c1832cd91a651b229d4b (official_runs/run1..run4.out each a4ed7c21fb36d839576be508f1ae39c3e59b63ace2ee1751a4066453f1d41765 byte-identical, detcheck.json OFFICIAL-PASS c2c751914c21134d60e64c5a3b108b1e2aa0b8713dad01d2e713c79f57c61699). Declared battery 9,339 pts, all endpoint fail-closed (count mismatch itself FAILs): D1 cells 1,989 (9 cells x 221 exhaustive floor-10 shapes, s in {0}∪{10..40}, arity 0..4) / D2 strip 594 (m in {10..14}, S in m..m+39, Y parts >=m, arity(Y) <=3, engine vs v at the T-Z15 claim position) / D3 z14 anchors 289 (8 lines x 33 s-values in {0}∪{9..40} = 264 re-anchoring the published K1319 z=14 cell table against the engine + 25 T-Z14 C-hand anchors m in {10..14} -- the battery guarantees the z=14 table REGARDLESS of the z14 lane's official-verification state) / D4 stair anchors 279 (9 x 31 A-on-Y child stair positions) / D5 self 5,865 (single-token engine-vs-v grid incl. z=16 for the lemma-BB v(s,16,16) evaluations + empty-position anchors) / D6 deviant witnesses 17 / D7 extension 85 (tail spots s in {41..48} x 9 cells = 72, strip spots m in {15..18} = 12, m=10 base spot (26;(10,10);15)=1=v(20,15,26) = 1) / D8 below-band anchors 221 (NEW gate: (16;Y;16) census of the lemma-BB supply source vs v(s,16,16) over the full floor-10 decomposition sweep -- the battery independently secures the F-tail supply). Official 4 runs (PYTHONHASHSEED=random same-cwd / =1 same-cwd / 2x env -i isolated dir, all from PUBLISHED bytes fetched back and byte-verified via cmp) all rc 0, stdout byte-identical to the declared predry sha a4ed7c21..., overall_bad 0, declared totals matched exactly. Tamper battery 8/8 fail-closed from published bytes (--tamper-engine rc 2 engine gate, --tamper=cell/strip/anchor14/stair/deviant/ext/belowband rc 1 each contaminating exactly the declared single gate). Honest record (declaration sec.6): paper option values were hand-computed from the K0832 closed form BEFORE machine cross-check (0 mismatches, and the hand derivation independently noticed the lemma-BB collapse of the below-band child); the first full machine run PASSed outright (unlike K1319's initial two-point tamper slip), helped by the pre-published census; the predry env -i isolated runs initially hit rc 127 via /usr/bin/python3 (not installed at that path) and were re-run byte-identical with the actual /usr/local/bin/python3 (no determinism impact; failed runs produced zero output and left the machine untouched); D2 594 and D8 221 declared counts were cross-checked against the frozen exploration .out cumulative counters."
relations:
- type: extends
  target: K1319
  note: "K1319 §5/§7 のハンドオフ (T-Z15 指名・floor-10 セル族・先行出版済み predecl kit f547c174 の受領) を受け、z=14 で確立した床付きセル梯子機構を z=15 に拡張して全称証明した。梯子長は 8 段→9 段 (j=9 段 A315f10 の追加・小トークン 9 = 出版 z=14 A2 セルの 1 段下)。C 手供給源として z=14 セル表 F14f9..A214f9 と T-Z14 定理線を直接引用し、D3 battery が engine に対して独立再照合する (K1319 公式検証状態に非依存、相互独立の chain)。F 系尾形は z=14 の尾なし単点 (第 5 形態) から第 6 形態 (恒常 2 尾・供給源は帯域下子) に移行し、G 段吸収則が供給源交代後も成立することを再演した。"
- type: related
  target: K1268
  note: "統合窓 sharpness 予想 C1。本項により min=10 行は z∈{0..15} が全確定 (残余バンド内 z∈{16,17})。z*(10)=18 は K1268 公式 (2m−2+(m mod 2)) の値。底子 min=9 が z*(9)=17 > 15 より**帯域内**に落ちるのはストリップ系列で初めてであり (T-Z13/T-Z14 の底子は前線上・帯域外)、z*(m) 前線の役割が「梯子長の下限」から「底子の帯域内外」の分類軸に現れた観測データ点。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z15 の底 m=10 は過剰オプションが 1 つも入らない自明吸収型 (K1274/K1275 型) でありながら、底子が初めて帯域内 (min=9) に落ち、なおフル 9 段梯子を要する — 自明吸収+帯域内底子+フル梯子依存の組み合わせは初観測。底類型系列 (自明吸収→deviant 吸収→TOLERANT-ABSORPTION→自明吸収+帯域外フル梯子 (K1319)→自明吸収+帯域内フル梯子 (本項)) の決定則は open。"
- type: depends_on
  target: K1264
  note: "階段定理 (空でない X・R=z+min(X) でちょうど H(R;X;z)=v(ΣX,z,R))。セル梯子の Y 内 A手子評価 (R=j+15=z+min ちょうど)・T-Z15 母体の a>m 子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。セル梯子の全場合計算・T-Z15 単一側選択肢集合・補題 BB の吸収恒等式 (v(s,16,16) vs v(s,15,16)) 算出の基盤。宣言 §6: 本項は手計算を機械照合に先行して実施 (不一致 0)。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1319 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置・多トークン Σ tail 崩壊。セル梯子各段の白紙 A手子・s=0 列・帯域下子 (16;Y;16) の白紙位置評価に使用。"
- type: depends_on
  target: K1319
  note: "z=14 floor-9 セル表 F14f9..A214f9 (床 9 ⊆ 床 10 の全点を被覆) と T-Z14 定理線 (m>=9 ⊇ 10) を本項証明の C 手供給源として直接引用。D3 battery がこれらの転写を engine に独立再照合。本項は K1319 の下で「死点化なきスライス」の初事例 (z=14 供給源 s∈{10,12,14} がすべて床 10 以上で存活)。"
artifacts:
- path: research/log/2026-11-25-z15-predecl-exploration.md
  role: log
  commit: f547c174
  note: 宣言前探査 log (先行実行による出版・本項の受領。9 セル census 全数値・F15f10 第 6 尾形の観測・strip 594 形状・帯域内 m=9 行 z=15 の 152 形状分離 0・宣言に先行する一次資料。sha256 944fdf79…)
- path: research/experiments/strip-z15-min10-20261125/explore_z15pre.py
  role: verifier
  commit: f547c174
  note: "凍結探索機体 (sha256 3e2a8ab8…・engine pin ゲート内蔵)。9 セル ×床付き全分解 census・tail spots・z=15 strip・帯域下子 census・帯域内 m=9 行 z=15 記録を再現し宣言表と完全一致。"
- path: research/experiments/strip-z15-min10-20261125/explore_z15pre.out
  role: data
  commit: f547c174
  note: "凍結探索出力 (sha256 2cf0a966…・決定性 3 走 byte-identical・multivalue 0 行の観測・宣言表と完全一致)。"
- path: research/experiments/strip-z15-min10-20261125/engine_block.py
  role: data
  commit: f547c174
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1319 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/experiments/strip-z15-min10-20261125/README.md
  role: log
  commit: f547c174
  note: "kit README (仮 sha256 a4628eb1…で先行出版・検証機体出版時に機体セクション追記・commit 8ee5330b・拡張版 sha256 bb22f304…・battery/実行構成の説明・K1319 §7 ハンドオフの受領)。"
- path: research/log/2026-11-25-strip-z15-min10-single-owner-note.md
  role: declaration
  commit: 671ca6babe32aa5f2718ca20d046d5d8ac1d0f60
  note: "単一オーナー宣言ノート (48,667 bytes・701 行・sha256 fbfb6bb999fae6f83754afa88c5c6874e26b53463c6e3512d38f2f819a26de24)。§1 主張 (9 補題 + T-Z15 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute)・§3 凍結探索・§4 宣言 battery 9,339 点 fail-closed + predry sha + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録・§6 宣言前探査の全開示 (honest)・§7 次レーンへの申し送り。"
- path: research/experiments/strip-z15-min10-20261125/verify_k1320.py
  role: verifier
  commit: 8ee5330b00591010b6fbf67de5c2ad8d9d49fdb4
  note: "専用検証機体 (sha256 081fe719a3274c25719c8149beefdcf724e381b2cc025bc582e9d2e28936c7e4・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 9,339 点・変異 8 モード・点数過不足も即 FAIL・fetch-back byte 一致)。"
- path: research/experiments/strip-z15-min10-20261125/published/official_runs/run1.out
  role: data
  commit: 0e4bfab24a1419f829b8c1832cd91a651b229d4b
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 a4ed7c21fb36d839576be508f1ae39c3e59b63ace2ee1751a4066453f1d41765 で byte-identical・rc 0・overall_bad 0・counts 9,339 = 宣言・出版 bytes から fetch-back 照合の上で実行)。"
- path: research/experiments/strip-z15-min10-20261125/published/detcheck.json
  role: data
  commit: 0e4bfab24a1419f829b8c1832cd91a651b229d4b
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 c2c75191…・predry/公式 4 走/tamper 8 種/kit fetch-back の全実測を記録)。"
- path: research/log/2026-11-25-strip-z15-min10.md
  role: log
  note: 完了 log (publish-then-execute チェーン f547c174→671ca6ba→8ee5330b→公式実行→0e4bfab2→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=10・min(X)=m を持つ空でない任意の有限多重集合 X (全形状・全アリティ) に対して
  H(m+16;X;15)=v(ΣX,15,m+16) が成立するという全称命題 (proved・床付き floor-10
  セル梯子 9 補題の K0832 場合計算 + 出版 z=14 表の引用 (死点化なし・全供給源
  存活) + 補題 BB の帯域下子崩壊 (吸収恒等式の s>=16 の破れ = F 尾供給源) +
  底 m=10 の自明吸収 (A315f10 完全崩壊ゆえ過剰オプションなし・ただし帯域内
  底子かつフル 9 段梯子依存) + 選択肢集合一致 + m に関する帰納)。同一証明に
  含まれる数学的部品として Lemma F15f10 (s=14 下向き単点 + s=15 穴 + s>=16 恒常
  2 尾 = F 系第 6 尾形・供給源は帯域下子・全称)、Lemma G15f10 (s=14 下向き
  単点・F 尾の G 段完全吸収・全称)、Lemma E15f10 (s=12 下向き + s=14 上向き・
  全称)、Lemma D15f10 (s=12 下向き単点・全称)、Lemma C15f10 (s=10 下向き +
  s=12 上向き・全称)、Lemma B15f10 (s=10 下向き単点・全称)、Lemma A15f10
  (s=10 上向き単点・全称)、Lemma A215f10 (完全崩壊・全称)、Lemma A315f10
  (完全崩壊・帯域内底子・全称) と、A315f10 の言い換えである「min=9 の z=15
  主張位置は第 2 小トークン >= 10 ならば v(ΣX,15,25) に崩壊」という限定文
  (co-token 9 形状の行文は適用外で open・先行探査の 152 形状分離 0 は観測) も
  主張に含む。系として m=10 行の z∈{0..15} 確定 (残余 {16,17}) と z=15
  スライスの min>=10 全閉鎖が従う。min<=9 の z=15 セル (古典床) は本項の
  範囲外で open (m=9 行 z=15 の行文証明は申し送り課題)、帯域下子の一般理論
  ((16;Y;16) 型の崩壊と吸収恒等式の破れの法則化: 本項では j=1・z=16 の一点の
  みを BB として扱う)、F 系尾形の一般則 (z=10 死 / z=11 再誕 / z=12 blister /
  z=13 恒常 2 尾 / z=14 尾なし / z=15 供給源交代つき恒常 2 尾の法則化)、
  底類型 (自明吸収+帯域内底子+フル梯子) の決定則、m>=10 行の z∈{16..z*(m)−1}
  (行残余 z∈{16,17} を含む) は open。11×11 盤面のいかなる勝敗も本項の範囲外
  (二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費)。

## 概要

K1319 (z=14 min>=9 スライス・T-Z14) の §5/§7 ハンドオフが指名した z=15 スライスを、
**床 min(Y)>=10 (floor-10 = z−5)** のセル族に限って選んだ構成で全称証明し出版した
(publish-then-execute・先行出版済み predecl kit `f547c174` の受領)。

- **T-Z15 (主定理)**: すべての m>=10・min(X)=m で H(m+16;X;15)=v(ΣX,15,m+16)。
  底 m=10 は**過剰オプションが 1 つも入らない自明吸収型** (底セル A315f10 が完全
  崩壊しているため)。構造的新事実が 2 つ: **(a) 底子 (min=9) がストリップ系列で
  初めて帯域内 (z*(9)=17 > 15) に落ちる** (T-Z13/T-Z14 の底子は前線上・帯域外)。
  **(b) 梯子の最下段 (j=1 の B 手子 (16;Y;16)) が初めて帯域下 (z'=16 > z) の位置を
  活きた供給源として利用する** — それでいて底は自明吸収型であり、なおフル 9 段
  梯子を要する (梯子長 8→9)。
- **セル梯子 9 補題 (全称・分解非依存)**: 各セルの値は ΣY=s のみで決まる。
  F15f10 は **s=14 下向き単点 + s=15 穴 + s>=16 恒常 2 尾** — **F 系第 6 尾形**
  (恒常 2 尾の再々来・ただし供給源が帯域下子に交代・z=13 では (ii') が単一側の
  選択肢を忠実に複製するだけだったのと対照的)。G15f10 は s=14 下向き単点で
  **F 尾を G 段で完全吸収** (K1317 G 段吸収則が供給源交代後も成立)。
  A215f10・A315f10 は**完全崩壊** (A315f10 = 小トークン 9・出版 z=14 A2 の
  1 段下・**系列初の帯域内底子**)。**死点化なし**: z=14 側供給源 (s∈{10,12,14})
  はすべて床 10 以上で存活し、z=13/z=14 の死点化機構と対照をなす。
- **系 1**: z=15 スライスは min>=10 全域で Σ崩壊。**系 2**: min=10 行は
  z∈{0..15} 全確定 (残余バンド内 z∈{16,17}・z*(10)=18)。
- **機体**: 宣言 battery 9,339 点 fail-closed (D3 が出版 z=14 表を engine に
  独立再照合し K1319 レーンの公式検証状態に非依存・**D8 が帯域下子供給源
  H(16;Y;16) を独立に掃引**)・公式 4 走 byte-identical (stdout sha a4ed7c21…)・
  tamper 8/8 fail-closed・detcheck OFFICIAL-PASS 出版。

## 主張の区別 (定型)

§1 の 9 補題・T-Z15・系 1/2 は全称 (証明は宣言ノート §2 の紙面のみ)。battery と
census (multivalue 0 の観測・tail spots・帯域内 m=9 行 z=15 の 152 形状分離 0) は
独立の有限再照合・観測資料であり、それ自体は全称性の証明でない。F 系尾形の一般則・
帯域下子の一般理論・吸収の法則化・底類型の決定則・一般床の問い (min(Y)>=z−5 が
必要十分か・z=13/z=14 に続き 3 つ目の肯定データ点)・m=9 行 z=15 の行文は open。
11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。
