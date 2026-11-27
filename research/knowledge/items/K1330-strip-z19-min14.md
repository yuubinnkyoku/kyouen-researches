---
id: K1330
title: "min>=14 クリティカルストリップ z=19 スライス (floor-14 = z−5): H(m+20;X;19)=v(ΣX,19,m+20)（床付き floor-14 セル梯子 F19f14..A719f14 の 13 全称補題 + T-Z19 + z=19 スライスの min>=14 全閉鎖・m=14 行は z∈{0..19} 確定・残余バンド内 z∈{20..25}・前線 z=26=z*(14)〔初出の系算術誤り 28 は erratum 修復済み〕・F 系第 10 尾形 HOLE+TAIL (奇数 z 形への回帰・typology 交互則 5 連続)・吸収恒等式 v(s,20,20)=v(s,19,20) の一様 0v1@20+ = 恒常尾の供給源・4 回連続床シフトではじめて定義域除外が非発生・A RANK 再誕生 (s=14=z−5 単点 UP・odd-z A-break 観測 2/2) の直後 6 段完全崩壊・第 5 連続帯域内底子 A719f14 (z*(13)=25>19))"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=19 slice (floor-14 = z-5, min>=14): for every m>=14 and every nonempty finite multiset X with min(X)=m, H(m+20;X;19)=v(sumX,19,m+20) (theorem T-Z19). With z*(m)=2m-2+(m mod 2) (K1268), z*(14)=26>19, so together with the published slice chain (low-min editions fixing z in {0..12}, T-Z13 z=13 min>=8, T-Z14 z=14 min>=9, T-Z15 z=15 min>=10 (both floor editions), T-Z16 z=16 min>=11, T-Z17 z=17 min>=12, T-Z18 z=18 min>=13) and this theorem, the m=14 row is determined for ALL z in {0..19} (remaining in-band z in {20..25}, frontier z=26=z*(14); the declaration note's original corollary wrote 28 by arithmetic slip, repaired by erratum commit 46c0efbe with conclusions unchanged), and the z=19 slice is closed for ALL min>=14. The claim position offset is 20 = z+1 (same lattice as T-Z18's 19); the bottom m=14 is a trivial-absorption base whose a=14 child (33;{13}uY;19) lands EXACTLY on the thirteenth cell A719f14's domain (small token 13, Y tokens >= 14; deviant-free, hence identically equal to the stair-side closed form v(S-1,19,33) for all S), and all C-hand children land on published lines: rungs j in {1..12} on the K1328 z=18 cells (co-floor 13 subset argument: the C-hand child (j+19;{j}uY;18) has Y tokens >= 14 >= 13 within the K1328 published lemma domain) and the j=13 C-hand child (32;{13}uY;18) on the published T-Z18 m=13-row claim position R=13+19 EXACTLY."
  - "floor-14 cell ladder (all 13 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+20;{j}uY;19) with all Y tokens >= 14, arity arbitrary, Y blank iff s=0, s in {0}u{14..}): Lemma F19f14 = 1 at s=18 DOWN (collapse 2) / 2 for all s>=20 UP (collapse 0) / v(s+1,19,21) elsewhere including the s=19 HOLE (equals its collapse 0) -- the F-family TENTH tail typology: HOLE+TAIL {z-1 DOWN 1v2, z HOLE, z+1+ persistent UP 2v0}, the z-relative profile IDENTICAL to the z=15 (sixth) and z=17 (eighth) forms: single@(even z) / hole+tail@(odd z) now FIVE consecutive consistent slices and the odd-z profile 3/3. NEW supply source: the j=1 below-band B-move child H(20;Y;20)=v(s,20,20) whose absorption identity v(s,20,20)=v(s,19,20) holds on {0}u{12..19} and breaks UNIFORMLY 0-vs-1 for ALL s>=20 (published as the z19 probe statement and rechecked engine-free over s in {0}u{12..56} as census kit section g1 BEFORE the declaration; contrast the z=18 two-stage break): the s=20 first break point injects the mex minimum 0 into the option set supplying the persistent UP 2 tail, and the identity's final hold point s=19 (=z) is exactly the HOLE -- supply-to-deviant alignment exact, same as z=18. Lemma G19f14 = 0 at s=18 DOWN (mirror of the F s=18 DOWN supply; v(s+2,19,22) elsewhere incl. s=0), Lemma E19f14 = 1 at s=16 DOWN + 2 at s=18 UP, Lemma D19f14 = 0 at s=16 DOWN, Lemma C19f14 = 1 at s=14 DOWN + 2 at s=16 UP, Lemma B19f14 = 0 at s=14 DOWN, Lemma A19f14 = 2 at s=14 UP -- the FIRST A-rank deviant since z=17 (A17f12 {12 UP:2}), sitting at s=14=z-5, exactly the z-5 relative position of the z=17 A break (odd-z A-break observation 2/2; the even-slice A18f13 produced no trough at z-5), then A219f14..A719f14 = v(s+j,19,j+20) -- SIX consecutive full collapses after the single break (series-record tie with z=18's six). A719f14 (j=13, min=13, z=19, Y>=14) is the T-Z19 absorption bottom and the FIFTH consecutive in-band base child after K1320 A315f10, K1322 A416f11, K1325 A517f12 and K1328 A618f13 (z*(13)=25>19; its (iii) C-hand child (32;{13}uY;18) is the published T-Z18 m=13-row claim position itself). Per-position deviant content: a repeating {DOWN:1, DOWN:0, UP:2} triplet at positions 14/16/18 (position 14 = {C,B,A}, 16 = {E,D,C}, 18 = {F,G,E}), one rank LOWER per position than the z=18 climb, with value multiset EXACTLY the z=17 base-position triplet {A17 DOWN:1, B17 DOWN:0, C17 UP:2}-pattern -- the odd-z ladder base triplet repeats (2/2 odd slices, observation)."
  - "transition z=18 -> z=19: the WHOLE published z=18 deviant position set {14,16,18} survives the floor shift (all >= 14) -- the FOURTH consecutive floor shift and the FIRST recorded non-event of the definition-domain-exclusion mechanism (after the three recorded events; z-transitions do not kill classes, floors re-admit or exclude them by domain -- here no class fell below floor 14). Below-band supply identity pair v(s,20,20) vs v(s,19,20) holds on {0}u{12..19} and breaks uniformly 0v1 for s>=20 (odd-z uniform full-expression form, z=17-type); the z=20 slice's ELEVENTH-tail identity pre-computation (census kit section g2, engine-free): v(s,21,21) vs v(s,20,21) holds on {0}u{12..19}, breaks {0v2 at s=20, uniform 2v1 for s>=21} = the exact z=18 even-z identity shape -- the even/odd supply-identity parity structure 2+2 consistent with the F-tail typology alternation. Census observations (frozen bytes, NOT theorem content): m=13-row z=19 record 76+75 shapes 0 separations (K1328 residual band first entry, row claim stays open), m=12-row 92/0 (K1325 band second entry), m=11-row 110/0 (K1322 band third entry); m=14 base spot H(34;(14,14);19)=1=v(28,19,34) -- base-spot z-parity alternation 0/1/0/1 across floors (probe crosscheck)."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration census kit published FIRST by this lane's earlier execution (commit 6a6832ce: engine_block.py sha256 582c93c1... same bytes as the K1282..K1328 chain with startup pin bd5f22e4..., frozen explore_z19f14.py e41138e2... / explore_z19f14.out 3354dfc6... determinism 5 byte-identical runs, kit README 8,945B + predecl log), z20 probe kit 0906ff21 (beyond/frontier z=20-side data + g2 identity; published earlier), declaration note e07d8f3d (50,262 bytes, 719 lines, published sha256 eb352b257156d98c1504a61af95a94de15702e621a31751d825be2b95708077f, full paper proofs in sec.2 disclosed before machine execution; single-owner slot claim K1330, no competing T-Z19 declaration existed; erratum repair 46c0efbe later fixed ONLY the corollary arithmetic z*(14)=28->26, repaired sha256 d6cf1287...), verify machine ca6d12bc (verify_k1330.py sha256 dda8e6278d3f60baf94f362f6465fddd78dc6847a354551e1491c4dcb5f2dc83, structural copy of verify_k1328.py with all diffs disclosed in the machine docstring; kit README machine section appended, extended README sha256 22db50a0...), official outputs 25aafd1a (official_runs/run1..run4.out each byte-identical sha256 a925af7dde945931473dfd3df2c2b775b36bdd8973dd49f7fb968566d04e30e8 = the predry sha, detcheck.json OFFICIAL-PASS sha256 a2ad4982...). Declared battery 16,267 pts, all endpoints fail-closed (count mismatch itself FAILs): D1 cells 1,521 (13 cells x 117 exhaustive floor-14 shapes, s in {0}u{14..44}, arity 0..4) / D2 strip 230 (m in {14..18}, census-mirroring sweep, cumulative 68/123/167/202/230) / D3 z18 anchors 438 (12 published K1328 line transcriptions x 34 s-values on the K1328 floor-13 domain {0}u{13..45} + 30 T-Z18 C-hand anchors m in {13..18}) / D4 stair anchors 403 (13 x 31, s in {14..44}) / D5 self anchors 13,419 (single-token grid x in {1..30}, z in {0..20} INCLUDING z=20 for the below-band identity pair evaluations, 21 R-points per pair = 13,230 + 189 empty anchors) / D6 deviant/collapse witnesses 22 (values, collapse targets AND directions, incl. the tenth-form DOWN point s=18, the s=19 HOLE flat, the s=20/s=52 persistent-tail points, the A19f14 A-rank rebirth witness and the in-band base child A719f14 spots) / D7 extension 117 (tail spots s in {45..52} x 13 cells -- F tail persistent 8/8, other 96 rows FLAT -- + 12 strip spots m in {19..22} + the m=14 base spot 1) / D8 belowband 117 (H(20;Y;20) vs v(s,20,20) supply-source collapse over the full floor-14 census domain). First full machine run PASSed outright; predry 8 runs byte-identical (default x2, PYTHONHASHSEED=random/1/0 same cwd, env -i isolated x3 with explicit /usr/local/bin/python3); official 4 runs all rc 0 byte-identical to the declared sha executed from the published bytes (fetch-back byte-identity via the disclosed deterministic chunk-artifact-invariant reconstruction + MSLResource read-back); tamper battery 8/8 fail-closed from the published bytes (engine rc 2; cell/strip/anchor18/stair/deviant/ext/belowband rc 1 each flagging exactly the single declared gate). Honest record: hand-calculation-first phase ordering (closed-form candidates derived on paper from K0832 branch computations BEFORE the machine cross-check); the scratch drafting-support machines check_z19_cases.py/check_z19_more.py (cell transcriptions, identity pair, triplet ladder, strip/tail witnesses) were run after the paper derivation and before publication, and were published as declaration note sec.6 attachments."
relations:
- type: depends_on
  target: K1328
  note: "z=18 floor-13 セル表 F18f13..A618f13 (12 全称補題) と定理 T-Z18 (min(X)=m>=13・主張位置 R=m+19) を本項証明の C 手供給源として直接引用 (co-floor 13 ⊆ 14 の部分集合引数: C 手子 (j+19;{j}∪Y;18) の Y トークン 14 以上は出版補題領域内)。j=13 段の C 手子 (32;{13}∪Y;18) は出版 T-Z18 の m=13 行主張位置そのもの。D3 battery が 12 線の転写 + T-Z18 C 手位置 (m ∈ {13..18}) を engine に独立再照合するため K1328 公式検証の状態は本項の妥当性に影響しない。z=18→19 の遷移記録 (位置集合 {14,16,18} の床 14 での全生存・定義域除外の初の非発生) も本項が担う。"
- type: depends_on
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2)。z*(13)=25>19 (A719f14 帯域内底子 = 第 5 連続)・z*(14)=26 (系 1・系 2 の z=19<z*(14) と残余バンド z∈{20..25}・前線 z=26 の特定)。honest: 宣言ノート初出の系は算術誤り 28 を含み・項目執筆時の K1268 公式照合で検出し erratum commit 46c0efbe で修復 (結論は不变・定理本文と battery は無影響)。"
- type: depends_on
  target: K1264
  note: "階段定理。セル梯子の Y 内 A 手子評価 (R子=j+20=z+min(z=19) ちょうど)・帯域下子 (20;Y;20) の ill 位置評価・T-Z19 の (a>m) 子評価 (R=m+19=z_child+min 等号) に使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・(R+z)%2 中間枝。セル梯子の全場合計算・吸収恒等式 v(s,20,20)=v(s,19,20) ({0}∪{12..19} 成立・s>=20 一様 0v1 = F19f14 恒常尾の供給源・engine-free 前計算は z19 probe + census kit section g1)・第 11 尾恒等式 v(s,21,21)=v(s,20,21) の g2 前計算 (z=20 スライスの単点供給 datum) の基盤。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1328 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置 H(R;();z)=0。補題 s0・s=0 列・D5 の空位置アンカー 189 点に使用。"
- type: related
  target: K1325
  note: "F 系尾形の奇数 z ペア (z=17 第 8 形・本項第 10 形 = 同一 z-relative プロファイル {z−1 DOWN, z HOLE, z+1+ 恒常尾}) と A RANK 再誕生の先例 (A17f12 s=12=z−5 -> A19f14 s=14=z−5・odd-z A-break 観測 2/2)。z=17 体形の値トリプレット {C17,B17,A17}={DOWN:1,DOWN:0,UP:2} が z=19 の位置 14/16/18 に反復する観測 (2/2 odd slices)。"
- type: related
  target: K1320
  note: "破れ表出様式系列の 偶数側起点 (z=15 単点表出) と・帯域内底子系列第 1 項 A315f10 -> K1322 A416f11 -> K1325 A517f12 -> K1328 A618f13 -> 本項 A719f14 の 5 連鎖。棒供給恒等式の一様全表出形 (z=17 型) の z=19 での再訪。"
- type: related
  target: K1322
  note: "単点@偶数 z の直接対 (z=16 第 7 形 vs 本項 z=19 第 10 形は hole+tail)。typology 交互則の 5 データ点 z16/z19 両端を担う。第 11 尾前計算 (供給恒等式 even-z 形 {0v2@z+1, 2v1@z+2+}) は z=20 スライスでこの対を再訪する予告 datum。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z19 の底 m=14 は自明吸収型 (a=14 子が第 5 連続帯域内底子 A719f14 領域に一致し deviant ゼロゆえ階段側閉形式と恒等的同値)。底類型の帯域内底子連鎖 5 連続の決定則は open。"
artifacts:
- path: research/experiments/strip-z19-min14-20261125/explore_z19f14.py
  role: verifier
  commit: 6a6832ce
  note: "凍結探索機体 (sha256 e41138e2…・engine pin ゲート内蔵・先行実行出版・verify_k1328 テンプレからの z 18→19 差分全開示)。13 セル census (117 形状/セル)・tail spots 104 行・strip m∈{14..18}・m=13/12/11 行 z=19 記録・帯域下子 census・m=14 base spot・engine-free 恒等式前計算 section g1/g2 を含む。"
- path: research/experiments/strip-z19-min14-20261125/explore_z19f14.out
  role: data
  commit: 6a6832ce
  note: "凍結探索出力 (sha256 3354dfc6…・決定性 5 走 byte-identical・multivalue 0・deviant 表が宣言どおり)。"
- path: research/experiments/strip-z19-min14-20261125/engine_block.py
  role: data
  commit: 6a6832ce
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1328 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/log/2026-11-25-z19m14-predecl-exploration.md
  role: log
  commit: 6a6832ce
  note: "宣言前探査 log (先行出版)。census 全数値・恒等式前計算・ハンドオフ宣言 (全依存出版済み・K スロット未主張) を含む。"
- path: research/experiments/strip-z19-min14-20261125/README.md
  role: log
  commit: ca6d12bc
  note: "kit README (先行出版 8,945 bytes・census 記録・機体出版時に verification machine セクション追記・拡張版 sha256 22db50a0…・宣言 chain の要約と publish-then-execute 状態を記載)。"
- path: research/log/2026-11-25-strip-z19-min14-single-owner-note.md
  role: declaration
  commit: 46c0efbe
  note: "単一オーナー宣言ノート (初出出版 e07d8f3d・50,262 bytes・719 行・出版 sha256 eb352b25…。§1 主張 (13 補題 + T-Z19 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・吸収恒等式一様 0v1@20+ の恒常尾供給機構・s=19 HOLE = 恒等式最終成立点・A RANK 再誕生・A719f14 帯域内底子を含む)・§4 宣言 battery 16,267 点 fail-closed + predry sha・§5 open 登録 (z=20/floor-15 ほか)・§6 宣言前探査の全開示 (手計算先行・scratch check 機体の添付)・§7 申し送り。erratum repair 46c0efbe は系 1/2・§2.13・§5 の z*(14)=28→26・残余バンド {20..27}→{20..25}・前線 28→26 の同一長 5 か所置換のみで・定理本文・補題・battery・機体に無影響 (修復後 sha256 d6cf1287…・修復検出の経緯は completion log に開示)。"
- path: research/experiments/strip-z19-min14-20261125/verify_k1330.py
  role: verifier
  commit: ca6d12bc
  note: "専用検証機体 (sha256 dda8627…・verify_k1328.py の構造写し・差分全開示 (13 段・床 14・R 予算 j+20・D3 = z18 線転写 + T-Z18 C 手アンカー・D5 z-grid を z=20 まで拡張)・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 16,267 点・変異 8 モード・点数過不足も即 FAIL・fetch-back byte 一致)。"
- path: research/experiments/strip-z19-min14-20261125/official_runs/run1.out
  role: data
  commit: 25aafd1a
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 a925af7d… で byte-identical・rc 0・overall_bad 0・battery 16,267 = 宣言・出版 bytes から fetch-back 照合の上で実行)。"
- path: research/experiments/strip-z19-min14-20261125/detcheck.json
  role: data
  commit: 25aafd1a
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 a2ad4982…・predry 8 走・公式 4 走・tamper 8 種・検証 chain commit の全実測・fetch-back 手続の開示を記録)。"
---

# K1330: z=19 min>=14 (floor-14) クリティカルストリップスライス

## 主張 (すべて全称・紙面証明は宣言ノート §2)

- **T-Z19**: すべての m>=14・min(X)=m で H(m+20;X;19)=v(ΣX,19,m+20)。
  底 m=14 は a=14 子 (33;{13}∪Y;19) が第 5 連続帯域内底子 A719f14
  (z*(13)=25>19) の定義域そのもの (小トークン 13・Y は 14 以上・
  deviant ゼロゆえ階段側閉形式と恒等的同値) に落ちる自明吸収型。
  m>=15 は選択肢集合一致帰納: a=m 子 = T-Z19(m−1) の主張位置・
  a>m 子 = K1264 階段 (R=m+19=z_child+min 等号)・C 手子 = 出版 T-Z18 の
  m>=13 行 (j=1..12 段は K1328 z=18 セルの co-floor 13⊆14 部分・j=13 段は
  T-Z18 m=13 行そのもの)。z=19 スライス min>=14 全閉鎖・m=14 行は
  z∈{0..19} 全確定 (残余バンド内 z∈{20..25}・前線 z=26=z*(14) —
  初出の系算術誤り 28 は erratum 46c0efbe で修復・結論不変)。
- **13 セル閉形式 (全称・s-only)**: F19f14(s)=1 (s=18) / 2 (s>=20) /
  v(s+1,19,21) (他・s=19 HOLE=崩壊値 0 含む)・G19f14=0 (18) /
  v(s+2,19,22)・E19f14=1 (16) / 2 (18) / v(s+3,19,23)・D19f14=0 (16) /
  v(s+4,19,24)・C19f14=1 (14) / 2 (16) / v(s+5,19,25)・B19f14=0 (14) /
  v(s+6,19,26)・A19f14=2 (14) / v(s+7,19,27)・A219f14..A719f14=
  v(s+j,19,j+20) (単一 A break の直後 6 段完全崩壊 = 系列タイ記録)。
  床 14・Y 全トークン >= 14・アリティ任意。
- **構造記録 (証明内で全称確定)**: F 系第 10 尾形 = HOLE+TAIL
  {s=18 DOWN 1v2・s=19 HOLE・s>=20 恒常 UP 2v0 尾} = 奇数 z 形への回帰
  (single@(偶数 z) / hole+tail@(奇数 z) の交互則 5 連続・odd-z プロファイル
  3/3)。供給源 = 補題 BB'' 型帯域下子 (20;Y;20)=v(s,20,20) の吸収恒等式
  v(s,20,20)=v(s,19,20) が {0}∪{12..19} で成立し s>=20 で一様 0v1 で破れる
  一様全表出形 (z=17 型): s=20 の破れ第 1 点が mex 最小値 0 を注入して
  恒常尾 2 を生み・恒等式最終成立点 s=19 (=z) が HOLE として正確に整列
  (supply-to-deviant alignment は z=18 と同一に正確)。A RANK 再誕生:
  A19f14 s=14=z−5 単点 UP 2v0 (z=17 の s=12=z−5 と同一相対位置・
  odd-z A-break 観測 2/2) の直後 A2..A7 が 6 段完全崩壊。位置
  トリプレット {DOWN:1, DOWN:0, UP:2} が s=14/16/18 で
  {C,B,A}/{E,D,C}/{F,G,E} に反復 (z=18 の climb 構造と対をなす周年構造・
  値多重集合は z=17 base トリプレットと一致)。定義域除外機構は 4 回連続
  床シフトではじめて非発生 (z=18 の位置集合 {14,16,18} 全生存・3 事象後の
  初の非事象)。

機体と検証は publish-then-execute で完全出版: 宣言ノート (719 行・紙面証明
全文を機械実行前に先行開示・K1330 単一オーナー・対抗 T-Z19 宣言なし) →
検証機体 verify_k1330.py (宣言 battery 16,267 点・D8 帯域下子 gate が
供給源を独立担保) → 公式 4 走 (出版 bytes fetch-back 照合から
byte-identical 全 rc 0・overall_bad 0・点数過不足 fail-closed) + tamper
8/8 fail-closed → detcheck.json OFFICIAL-PASS。手計算先行 (drafting 支援
scratch check 機体 2 本を紙面誘導後に実行・宣言 §6 に全開示)。系の算術
誤り (z*(14)=28) は項目執筆時の K1268 公式照合で検出し erratum
46c0efbe で修復 (定理・補題・battery・機体は無影響・completion log に
開示)。11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict
不消費 (battery 点数は定理の実機照合であって証明の代替ではない)。
