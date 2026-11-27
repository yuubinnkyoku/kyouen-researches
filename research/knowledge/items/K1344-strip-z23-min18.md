---
id: K1344
title: "min>=18 クリティカルストリップ z=23 スライス (floor-18 = z−5): H(m+24;X;23)=v(ΣX,23,m+24)（床付き floor-18 セル梯子 F23f18..A1123f18 の 17 全称補題 + T-Z23 + z=23 スライスの min>=18 全閉鎖・m=18 行は z∈{0..23} 全確定・残余バンド内 z∈{24..33}・前線 z=34=z*(18)・F 系第 14 尾形 = 奇数 z HOLE+TAIL 形 (s=22=z−1 単点 DOWN 1v2・s=23=z 適合 HOLE・s>=24 恒常尾 UP 2v0・typology 交互則 9 連続スライス z15..z23 で成立・偶数形 4/4・奇数形 5/5)・吸収恒等式 v(s,24,24)=v(s,23,24) の {0}∪{12..23} 成立・s>=24 一様 0v1 破れ = K1334 定理 A の k=23 奇数インスタンス (奇数 4 形態のうち第 15 尾 k=25 まで前計算済み)・恒常尾再生機構 (奇数 k 形では (ii')=0 が留まり続けて尾を開く・偶数 k 形と鏡像)・A23f18 = A RANK BREAK REBIRTH 出生位置 s=18=z−5 UP 2v0 で奇数 z 出生 4/4 (偶数 z 全滅 5/5 と合わせ A RANK 完全偶奇分裂 9 スライス確定・出生位置 s=z−5 が偶数 z で奇数 s になることが全滅の機構候補)・定義域除外の非事象 (z=22→23 で deviant 位置集合 {18,20,22} 全生存・(偶, 直後奇) 位置ペア則 4/4・偶→奇の非除外 3/3)・station 値割当の偶奇鏡像則 (奇数形トリプレット {DOWN 1v2, DOWN 0v1, UP 2v0}: s=18 で {C,B,A}・s=20 で {E,D,C}・s=22 で {F,G,E}・census 4/4 確認)・第 9 連続帯域内底子 A1123f18 z*(17)=33>23)〔採番 K1344 は kit 構築時点で code 検索 0 件・push 直前に再 probe・対抗 T-Z23 宣言は最後まで不存在・改名 事故なし (drafting verify_tz23.py → verify_k1344.py はラベル/docstring bytes のみ・battery byte 同一)〕"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=23 slice (floor-18 = z-5, min>=18): for every m>=18 and every nonempty finite multiset X with min(X)=m, H(m+24;X;23)=v(sumX,23,m+24) (theorem T-Z23). With z*(m)=2m-2+(m mod 2) (K1268), z*(18)=34>23, so the z=23 slice is closed for ALL min>=18 (corollary 1), and the min=18 row is determined for ALL z in {0..23} by the published slice chain (low-min editions T-Z6..T-Z12 (z=6..12), T-Z13..T-Z22 (z=13..22, floors 8..17), low z by K1270/K1272/K1278) plus T-Z23 for z=23 (corollary 2): remaining in-band z for the min=18 row in {24..33}, frontier z=34=z*(18). The claim position offset is 24=z+1; the bottom m=18 is a trivial-absorption base whose a=18 child (41;{17}uY;23) lands EXACTLY on the seventeenth cell A1123f18's domain (small token 17, Y tokens >=18; deviant-free over the whole domain, NINTH consecutive in-band base child, z*(17)=33>23, its (iii) C-hand child (40;{17}uY;22) is the published T-Z22 m=17-row claim position itself), and all C-hand children land on published lines: rungs j in {1..16} on the K1339 z=22 cells (co-floor 17 subset argument: the C-hand child (j+23;{j}uY;22) has Y tokens >=18 >= 17 within the K1339 published lemma domain) and the j=17 C-hand child (40;{17}uY;22) on the published T-Z22 m=17-row claim position R=17+23 EXACTLY."
  - "floor-18 cell ladder (all 17 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+24;{j}uY;23) with all Y tokens >= 18, arity arbitrary, Y blank iff s=0, s in {0}u{18..}): Lemma F23f18 = 1 at s=22=z-1 (single point DOWN 1v2; conforming HOLE at s=23=z -- collapse value 0 matches the identity, supplying nothing) / 2 at s>=24 (persistent tail UP 2v0) / v(s+1,23,25) elsewhere including s=0 -- the F-family FOURTEENTH tail typology: the odd-z HOLE+TAIL form (z=19 K1330 and z=21 K1337 profile-identical), z-relative profile {s=z-1 single DOWN} / {s=z hole} / {s>=z+1 tail UP 2v0}: single@(even z) / hole+tail@(odd z) alternation now NINE consecutive consistent slices (z15..z23; even-z single form 4/4, odd-z hole+tail form 5/5; the general law remains open). DOUBLE supply mechanism (odd-z-form native, both sides published): (1) the single point is supplied NOT by an identity break but by the C-hand (iii) published F22f17 single point (s=22: 1): 1^1=0 removes 1 from the option set and drops the mex from 2 to 1 exactly at s=z-1; (2) the persistent tail comes from the j=1 below-band B-move child H(24;Y;24)=v(s,24,24) (lemma BB7, stair application R=24<=24+min(Y)) whose absorption identity v(s,24,24)=v(s,23,24) holds on {0}u{12..23} (K1334 theorem A, k=23 ODD instance: uniform (0,1) break for all s>=24): for s>=24 the broken (ii')=0 keeps injecting the mex minimum 0 into the option set next to (i)=1, pushing the mex to 2 -- at odd k the (ii') STAYS 0 so the tail regenerates (mirror image of the even-k mechanism where (ii') stands up to 2 and no tail is born). Lemma G23f18 = 0 at s=22 DOWN / v(s+2,23,26) elsewhere (the s=22 assignment is DOWN 0 in the odd form, contrasting the published G22f17 UP 2 at s=22), Lemma E23f18 = 1 at s=20 DOWN + 2 at s=22 UP / v(s+3,23,27), Lemma D23f18 = 0 at s=20 DOWN / v(s+4,23,28), Lemma C23f18 = 1 at s=18 DOWN + 2 at s=20 UP / v(s+5,23,29), Lemma B23f18 = 0 at s=18 DOWN / v(s+6,23,30), Lemma A23f18 = 2 at s=18 UP (A RANK BREAK REBIRTH at s=18=z-5, odd-z birth 4/4: z=17 s=12, z=19 s=14, z=21 s=16, z=23 s=18, always EVEN s UP 2v0) / v(s+7,23,31) -- the COMPLETE parity split of the A rank is settled across NINE slices (even-z annihilation 5/5: z=14,16,18,20,22; odd-z rebirth 4/4; the mechanism candidate: the birth position s=z-5 is ODD s exactly when z is even, and an odd-s deviant class has never been observed in any of the fourteen typologies or any station of the full history). Then A223f18 absorbs the s=18 REBIRTH class (full collapse), A323f18..A1023f18 deductively free collapse, A1123f18 the NINTH consecutive in-band base child (small token 17, z*(17)=33>23; its (iii) C-hand child is the published T-Z22 m=17-row claim position itself). Observed deviant position set {18,20,22} = the z=22 set {18,20,22} FULLY SURVIVING the floor 17->18 raise: the definition-domain EXCLUSION NON-EVENT THIRD-CONSECUTIVE (odd-arrival non-exclusions: z=18->19, z=20->21, z=22->23 = 3/3; the (even, following-odd) position-pair rule is settled 4/4 with pairs {(12,14,16)},{(14,16,18)},{(16,18,20)},{(18,20,22)}; the odd->even oldest-station deaths stay 2/2 (z=19->20 s=14, z=21->22 s=16)). Deviant station profile (odd-z form): {C:1 DOWN, B:0 DOWN, A:2 UP}@18 and {E:1 DOWN, D:0 DOWN, C:2 UP}@20 and {F:1 DOWN, G:0 DOWN, E:2 UP}@22 -- the value multiset {DOWN 1v2, DOWN 0v1, UP 2v0} of the odd form, the EXACT parity mirror of the even-form triplet values {DOWN 0v2, UP 1v0, UP 2v1} (station value-assignment parity-mirror rule, census 4/4 across nine slices)."
  - "transition z=22 -> z=23 and the odd machine (publish-then-execute, every stage fetch-back byte-verified): the published z=22 deviant positions {18,20,22} ALL survive the floor raise (exclusion non-event; no newborn, no death). Below-band supply identity pair v(s,24,24) vs v(s,23,24): holds on {0}u{12..23}, uniform (0,1) break for ALL s>=24 = the odd-k identity shape, K1334 theorem A instantiates it universally -- the below-band collapse H(24;Y;24)=v(s,24,24) (lemma BB7, stair application R=24<=24+min(Y)) plus theorem A closes the supply side of the whole slice without any new computation. Census observations (frozen bytes, NOT theorem content): m=17-row z=23 record 32+31 shapes 0 separations (K1339 residual band first entry candidate, row claim stays open), m=16-row 40/0 (K1337 band second entry), m=15-row 50/0 (K1335 band), m=14-row 62/0 (K1330 band), m=13-row 76/0 (K1328 band), strip m in {18..22} 108/0, m=18 base spot H(42;(18,18);23)=v(36,23,42)=1 (ninth base-spot parity point, continuing 0,1,0,1,0,1,0,1; z=24 predicted 0). Machine chain (publish-then-execute, all fetch-back verified): pre-declaration census kit 25522d56 (explore_z23f18.py eddd5e90... / explore_z23f18.out bb456e85... determinism 6 byte-identical runs ~29 s each; ordered-engine crosscheck of ALL rows 0 mismatches (1,377 cell + 136 tail + 108 strip + 32+31+40+50+62+76 record + 12 spots + base spot + 81 below-band + identity rows); SIXTEENTH-tail k=25 identity pre-computation included = the z=25 supply datum; predecl log 4142dfd9... (sha256). SHA-256 pins: engine_block.py 582c93c1... (identical bytes to the K1282..K1339 chain, pin bd5f22e4...)), declaration note 66ac2775 (60,208 bytes, sha256 795dc552..., full paper proofs in sec.2 disclosed before machine execution; single-owner slot claim K1344; NO numbering incident this time: K1344 probed free at kit-build (code search 0 hits) and re-probed at push; no rival T-Z23 declaration existed (path probed); the drafting machine was named verify_tz23.py and renamed verify_k1344.py before publication -- label/docstring bytes only, battery byte-identical, disclosed in sec.4/sec.6), verify machine b75e373e (verify_k1344.py sha256 8c0077a1ea4fd354ffdccfe9bc6c301e9cc0571869e67ffe6cb06897bd8c0b8f, 25,084 bytes, git blob sha1 019b3970c459ea899e48060471cd4ac64459f366; structural copy of verify_k1339.py with all diffs disclosed in the machine docstring; drafting bytes verify_tz23.py sha256 2b22acec... with its predry stdout 670 bytes disclosed; kit README machine section appended, README blob sha1 30ea773d...), official outputs e0b092ff (official_runs/run1..run4.out each 671 bytes byte-identical sha256 6d920fa11340d69f08cc2144aa4496c42bb423ddc2f3b1bce520fffd5617a2c5 = the post-rename predry sha of 8 runs: default x2, PYTHONHASHSEED=random/1/0 same cwd, env -i isolated x3 via /usr/local/bin/python3; tamper battery 8/8 fail-closed re-executed from the published bytes; detcheck.json OFFICIAL-PASS with machine_publication_commit b75e373e and declaration_note_commit 66ac2775). Declared battery 19,532 pts, all endpoints fail-closed (count mismatch itself FAILs): D1 cells 1,377 (17 cells x 81 exhaustive floor-18 shapes, s in {0}u{18..48}, arity 0..4) / D2 strip 108 (m in {18..22}, census-mirroring sweep, cumulative 28/51/71/90/108) / D3 z22 anchors 542 (16 published K1339 line transcriptions x 32 s-values on the K1339 floor-17 domain {0}u{17..47} = 512 + 30 T-Z22 C-hand anchors m in {17..22}) / D4 stair anchors 527 (17 x 31, s in {18..48}) / D5 self anchors 16,725 (single-token grid x in {1..30} x z in {0..24} INCLUDING z=24 for the below-band identity pair evaluations, 22 R-points = 16,500 + 225 empty anchors R in {0..8} x z in {0..24}) / D6 deviant/collapse witnesses 23 (literal values, collapse targets AND directions, incl. the fourteenth-form single point s=22=z-1 DOWN 1v2, the HOLE s=23 FLAT witness, the tail-opening s=24 UP 2v0 and the far tail spot s=52, the G/E/D/C/B/A station reconstructions, the A23f18 REBIRTH witness s=18=z-5 UP 2v0, the A1123f18 in-band base-child spots; the D6 literals were engine-measured FIRST (build_literals.py, unpublished) and the sec.2 paper derivation was checked against them -- both pre-freeze drafting errors (a j=4 s=22 R-argument misalignment and 4 witness direction labels analogized from the even form) were caught and corrected BEFORE any byte was frozen, disclosed in the note sec.6) / D7 extension 149 (tail spots s in {49..56} x 17 cells = 136 -- the F cell 8 spots ALL read the declared tail value 2 (odd-form signature, contrasting z=22's ALL-conforming even form) + 12 strip spots m in {23..26} + the m=18 base spot H(42;(18,18);23)=1) / D8 belowband 81 (H(24;Y;24) vs v(s,24,24) over the full floor-18 census domain, lemma BB7 machine cross-check)."
relations:
- type: depends_on
  target: K1339
  note: "z=22 floor-17 セル表 F22f17..A1022f17 (16 全称補題) と定理 T-Z22 (min(X)=m>=17・主張位置 R=m+23) を本項証明の C 手供給源として直接引用 (co-floor 17 ⊆ 18 の部分集合引数: C 手子 (j+23;{j}∪Y;22) の Y トークン 18 以上は出版補題領域内)。j=17 段の C 手子 (40;{17}∪Y;22) は出版 T-Z22 の m=17 行主張位置そのもの (A1123f18 の (iii) 供給源)。F23f18 の単点 s=22 は出版 F22f17 単点 (s=22: 1) の C 手 (iii) 供給として機構組込み (1^1=0 が mex を 2→1 に落とす)。D3 battery が 16 線の転写 + T-Z22 C 手位置 (m ∈ {17..22}) を engine に独立再照合するため K1339 公式検証の状態は本項の妥当性に影響しない。z=22→23 の遷移記録 (位置集合 {18,20,22} 全生存 = 除外非事象 3 連続) も本項が担う。"
- type: depends_on
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2)。z*(17)=33>23 (A1123f18 帯域内底子 = 第 9 連続)・z*(18)=34 (系 1・系 2 の残余バンド z∈{24..33}・前線 z=34=z*(18) の特定)。z=23 (奇数 z) < z*(18)=34 を宣言段階で公式と突合してから出版 (本項に算術誤りなし・erratum 不要)。"
- type: depends_on
  target: K1264
  note: "階段定理。セル梯子の Y 内 A 手子評価 (R子=j+23=z+min(z=23) ちょうど)・帯域下子 (24;Y;24) の適用範囲評価 (R=24 <= 24+min(Y) = 補題 BB7 (z=19/BB'''・z=21/BB'''''・z=22/BB6 と同じ骨格))・T-Z23 の (a>m) 子評価 (R=m+23=z_child+min 等号) に使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・(R+z)%2 中間枝。セル梯子の全場合計算・吸収恒等式 v(s,24,24)=v(s,23,24) の K1334 定理 A (k=23) に基づく直接確認 ({0}∪{12..23} 成立・s>=24 一様破れ (0,1))・第 16 尾 (k=25) 恒等式の継続前計算の基盤。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1344 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置 H(R;();z)=0。補題 s0・s=0 列・D5 の空位置アンカー 225 点に使用。"
- type: depends_on
  target: K1334
  note: "供給恒等式族閉形式 (定理 A)。本スライスの恒常尾供給源である j=1 帯域下 B 手子の吸収恒等式 v(s,24,24)=v(s,23,24) は定理 A の k=23 (奇数) インスタンスとして全称確定済み (成立域 [0..k−1]=[0..22]∪{0}・s>=24 一様破れ (0,1)・奇数 k 形は s>=k+1 で (ii')=0 が留まり続ける = 恒常尾再生機構・偶数 k 形 (0v2→2v1) と鏡像)。K1334 出版により本項の供給側計算は一切の新計算不要。単点 s=z−1 は定理 A でなく出版 F22f17 C 手から供給される点が K1339 (偶数側) との対照。"
- type: related
  target: K1337
  note: "A RANK 出生系列の直前奇数データ (z=21 s=16 出生・K1337 A RANK BREAK クラス) と残余バンド受領 (m=16 行 z=23: 40 形状 0 分離 = K1337 バンド z=23 エントリ・R=40)。A RANK 完全偶奇分裂 9 スライス確定 (偶数全滅 5/5 vs 奇数出生 4/4) の系列データ。"
- type: related
  target: K1335
  note: "残余バンド行記録 (m=15 行 z=23: 50 形状 0 分離 = K1335 バンドの z=23 エントリ・R=39) の受領。F 系尾形の偶数側データ (z=20 単点第 11 形) と奇形鏡像の対照データ。"
- type: related
  target: K1330
  note: "残余バンド行記録 (m=14 行 z=23: 62 形状 0 分離 = K1330 バンドの z=23 エントリ・R=38) の受領。F 系第 9 形態 (z=19 HOLE+TAIL) の奇数形先例で本項第 14 形の z-relative 同一プロファイル源。"
- type: related
  target: K1328
  note: "残余バンド行記録 (m=13 行 z=23: 76 形状 0 分離 = K1328 バンドの z=23 エントリ・R=37) の受領。帯域内底子 9 連鎖の途中データ (A618f13) と F 単点偶数形系列。"
- type: related
  target: K1322
  note: "F 系尾形 typology 交互則 (single@偶数 z / hole+tail@奇数 z) の 9 連続スライス z15..z23 成立。帯域内底子連鎖 (A416f11) と z=15..17 の奇数形先例。min=17 行 z=23..32 (K1339 残余バンド) は本項底子バンドとして open 継承・z=23 エントリ 32+31/0 記録済み。"
- type: related
  target: K1325
  note: "F 系第 10 形 (z=17 恒常 2 尾) の奇数形データ。本項第 14 形は z=19/z=21 (第 9/12 形) と z-relative プロファイル同一で奇数 z 形 5/5 の第 5 データ点。帯域内底子連鎖 (A517f12)。"
- type: related
  target: K1320
  note: "帯域内底子 9 連鎖の起点 (A315f10)。A1123f18 は第 9 連続 (K1320・K1322・K1325・K1328・K1330・K1335・K1337・K1339 に続き)。連鎖の決定則は open のまま。"
artifacts:
- path: research/experiments/strip-z23-min18-20261125/explore_z23f18.py
  role: verifier
  commit: 25522d56
  note: "凍結探索機体 (sha256 eddd5e90…・engine pin ゲート内蔵・先行実行出版・出版 explore_z22f17.py の z 22→23 差分全開示・仮 17 段ラベル A11 は本項で A1123f18 に正式化)。17 セル census (81 形状/セル)・tail spots 136 行・strip m∈{18..22}・m=17/16/15/14/13 行 z=23 記録 (32+31/40/50/62/76 形状 0 分離)・帯域下子 census 81 形状・m=18 base spot・engine-free 恒等式前計算 (第 14/15 尾再照合・第 16 尾 k=25 NEW 前計算 = z=25 スライスの供給データ) を含む。"
- path: research/experiments/strip-z23-min18-20261125/explore_z23f18.out
  role: data
  commit: 25522d56
  note: "凍結探索出力 (sha256 bb456e85…・決定性 6 走 byte-identical 各 ~29 s・multivalue 0・deviant 表が宣言どおり {0}∪{18..48} 上 {18,20,22})。"
- path: research/experiments/strip-z23-min18-20261125/engine_block.py
  role: data
  commit: 25522d56
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1344 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/log/2026-11-25-z23m18-predecl-exploration.md
  role: log
  commit: 25522d56
  note: "宣言前探査 log (先行出版・sha256 4142dfd9…)。census 全数値・恒等式前計算・ハンドオフ宣言 (全依頼出版済み・K スロット未主張)・ordered-engine 独立クロスチェック結果 (全行不一致 0) を含む。"
- path: research/log/2026-11-25-strip-z23-min18-single-owner-note.md
  role: declaration
  commit: 66ac2775
  note: "単一オーナー宣言ノート (60,208 bytes・sha256 795dc552…§0 採番 probe 手順・§1 主張 (17 補題 + T-Z23 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・BB7 帯域下子崩壊・K1334 定理 A k=23 による恒常尾再生機構の全称化・C 手出版 F22f17 単点による mex 2→1 単点機構・第 14 尾形 HOLE+TAIL・A RANK 完全偶奇分裂 9 スライス確定・A1123f18 第 9 連続帯域内底子・位置集合全生存 = 除外非事象)・§4 宣言 battery 19,532 点 fail-closed + predry/tamper sha (drafting 期を含む全部)・§4.5 主張の区別 (m=17 行 z=23 は行主張でない)・§5 open 登録 (T-Z24 など)・§6 宣言前探査の全開示 (D6 literal 実測先行・紙面導出中の誤り 2 件の開示)・§7 申し送り。K1344 採番事故なし・対抗 T-Z23 宣言なし。"
- path: research/experiments/strip-z23-min18-20261125/verify_k1344.py
  role: verifier
  commit: b75e373e
  note: "専用検証機体 (sha256 8c0077a1ea4fd354ffdccfe9bc6c301e9cc0571869e67ffe6cb06897bd8c0b8f・25,084 bytes・blob sha1 019b3970c459ea899e48060471cd4ac64459f366・verify_k1339.py の構造写し・差分全開示 (17 段・床 18・R 予算 j+24・D3 = K1339 z22 線転写 + T-Z22 C 手アンカー・D5 z-grid を z=24 まで拡張・D6/D7 保証 witness は奇数形署名に更新)・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 19,532 点・変異 8 モード・点数過不足も即 FAIL・drafting 機体 verify_tz23.py sha256 2b22acec… (24,970 bytes・未出版) との差分は機体ラベル 1 か所と docstring 行のみ (battery byte 同一)。改名後 bytes の predry 8 走 byte-identical (stdout 671 bytes・sha256 6d920fa1…)・tamper 8 モード再実測 fail-closed。"
- path: research/experiments/strip-z23-min18-20261125/README.md
  role: log
  commit: b75e373e
  note: "kit README (先行出版・機体出版時に verification machine セクション追記 (## Verify machine)・改名 (verify_tz23.py → verify_k1344.py) ・宣言 chain の要約と publish-then-execute 状態を記載・blob sha1 30ea773d…)。"
- path: research/experiments/strip-z23-min18-20261125/official_runs/run1.out
  role: data
  commit: e0b092ff
  note: "公式 4 走の正本出力 (run1..run4 すべて 671 bytes・sha256 6d920fa1… で byte-identical・blob sha1 9719cc10…・rc 0・overall_bad 0・battery 19,532 = 宣言・出版 bytes (blob sha1 019b3970… fetch-back 一致) から実行)。"
- path: research/experiments/strip-z23-min18-20261125/official_runs/detcheck.json
  role: data
  commit: e0b092ff
  note: "公式 deterministic check (OFFICIAL-PASS・公式 4 走 (既定/PYTHONHASHSEED=random 同一 cwd・env -i 隔離 ×2〔/usr/local/bin/python3〕)・tamper 8 種を出版 bytes から再実測 (8/8 fail-closed)・検証 chain commit (66ac2775/b75e373e) の全実測・claims_scope と主張の区別 (有限観測と全称証明の分離)・honest run record (r3/r4 初回 cp スリップ rc 2 空 out を即座に検出・出力凍結前にやり直し) を記録・blob sha1 c0457f1d…)。"
---

# K1344: z=23 min>=18 (floor-18) クリティカルストリップスライス

## 主張 (すべて全称・紙面証明は宣言ノート §2)

- **T-Z23**: すべての m>=18・min(X)=m で H(m+24;X;23)=v(ΣX,23,m+24)。
  底 m=18 は a=18 子 (41;{17}∪Y;23) が第 9 連続帯域内底子 A1123f18
  (z*(17)=33>23) の定義域そのもの (小トークン 17・Y は 18 以上・
  deviant ゼロゆえ階段側値 v(S−1,23,41) と恒等的同値) に落ちる自明吸収型。
  m>=19 は選択肢集合一致帰納: a=m 子 = T-Z23(m−1) の主張位置・
  a>m 子 = K1264 階段 (R=m+23=z_child+min・z=23 で min 不変)・
  C 手子 = 出版 T-Z22 の m>=17 行 (j=1..16 段は K1339 z=22 セルの
  co-floor 17⊆18 部分・j=17 段は T-Z22 m=17 行そのもの) で option set
  が単一側と完全一致。T-Z23 により z=23 スライスは min>=18 の全域で
  Σ崩壊が確定。系 1: z*(18)=34>23 で z=23 スライス min>=18 全閉鎖。
  系 2: min=18 行は出版 slice chain + T-Z23 を合わせて z∈{0..23} 全セル
  確定 (残余バンド内 z∈{24..33}・前線 z=34=z*(18) は open)。
- **17 セル閉形式 (全称・s-only)**: F23f18(s)=1 (s=22 単点 DOWN 1v2) /
  2 (s>=24 恒常尾 UP 2v0) / v(s+1,23,25) (他・s=0・s=23 適合 HOLE を含む) —
  第 14 尾形 = 奇数 z HOLE+TAIL 形 (z=19/z=21 型と z-relative 同一)。
  G23f18(s)=0 (s=22 DOWN) / v(s+2,23,26) (他)・E23f18(s)=1 (s=20 DOWN) /
  2 (s=22 UP) / v(s+3,23,27) (他)・D23f18(s)=0 (s=20 DOWN) / v(s+4,23,28)
  (他)・C23f18(s)=1 (s=18 DOWN) / 2 (s=20 UP) / v(s+5,23,29) (他)・
  B23f18(s)=0 (s=18 DOWN) / v(s+6,23,30) (他)・**A23f18(s)=2 (s=18
  UP = A RANK BREAK REBIRTH・出生位置 s=18=z−5・奇数 z 出生 4/4)** /
  v(s+7,23,31) (他)・A223f18=v(s+8,23,32) (REBIRTH クラス吸収の完全
  崩壊)・A323f18..A1023f18=v(s+j,23,j+23) (演繹自由崩壊)・
  A1123f18=v(s+17,23,41) (**第 9 連続帯域内底子**)。床 18・Y 全トークン
  >= 18・アリティ任意。観測 deviant 位置集合 {18,20,22} = z=22 の
  集合が床 17→18 の引き上げを全生存 (定義域除外の非事象・出生も
  死亡もなし)。
- **構造記録 (証明内で全称確定)**: 二重供給機構。恒常尾側 = 補題 BB7 型
  帯域下子 (24;Y;24)=v(s,24,24) (床 18 census 81 形状完全崩壊) の吸収
  恒等式 v(s,24,24)=v(s,23,24) が {0}∪{12..23} で成立し・s>=24 で
  一様 (0,1) で破れたまま (K1334 定理 A の k=23 奇数インスタンス)。
  破れ後 (ii')=0 が留まり続けて mex 最小値 0 を注入し続け (i)=1 と
  ともに **恒常尾 2 を s>=24 全域で再生** (奇数 k 形の固有機構・偶数 k
  形では (ii') が 2 に立ち上がって尾が再生しない K1339 機構と鏡像)。
  単点側 = C 手 (iii) の出版 F22f17 単点 (s=22: 1) から 1^1=0 が
  選択肢集合の 1 を除去して **mex を 2→1 に落とし・単点 1 を s=22=z−1
  ちょうどに生む** (定理 A でなく出版 C 手線から供給される点が K1339
  (偶数側・破れ第 1 点からの 0 注入) との対照)。F 系尾形 typology
  交互則 (single@偶数 z / hole+tail@奇数 z) は 9 連続スライス z15..z23
  で成立 (一般法則 open・偶数形 4/4・奇数形 5/5)。A RANK の完全偶奇
  分裂が 9 スライスで確定 (偶数 z 全滅 5/5 (z=14/16/18/20/22) vs
  奇数 z 出生 4/4 (z=17/19/21/23・いずれも UP 2v0・出生位置 s=z−5 は
  常に偶数 s)・偶数 z では出生位置 s=z−5 が奇数 s になることが全滅の
  機構候補・奇数 s 位置の deviant クラスは F 系 14 形態・station 全履歴
  で一度も観測されていない)。定義域除外の発生則: 偶→奇の非除外は
  3/3 (z=18→19・z=20→21・z=22→23) で位置集合不動を確認・
  (偶, 直後奇) ペア則は 4/4 (={(12,14,16)}・{(14,16,18)}・{(16,18,20)}・
  {(18,20,22)})・奇→偶の最古 station 死亡は 2/2 のまま (z=19→20 s=14・
  z=21→22 s=16)。station 値割当の偶奇鏡像則: 奇数形トリプレット
  {DOWN 1v2, DOWN 0v1, UP 2v0} が s=18 で {C,B,A}・s=20 で {E,D,C}・
  s=22 で {F,G,E} (census 4/4・偶数形 {DOWN 0v2, UP 1v0, UP 2v1}
  の鏡像・値割当は奇数形は j=23−s の C 側から {1,0,2})。
- **残余バンド行観測 (有限観測・本定理の一部でない)**: m=17 行 z=23
  (R=41) 32+31 形状 0 分離 (K1339 残余バンド第 1 エントリ候補・行主張
  open)・m=16 行 40/0 (K1337 バンド)・m=15 行 50/0 (K1335 バンド)・
  m=14 行 62/0 (K1330 バンド)・m=13 行 76/0 (K1328 バンド)・strip
  m∈{18..22} 108/0。m=18 base spot H(42;(18,18);23)=v(36,23,42)=1
  (基底 spot パリティ点第 9 点・0,1,0,1,0,1,0,1 に続き z=24 は 0 予想)。
  第 16 尾恒等式 (k=25・hold {0}∪{12..25}・s>=26 一様 0v1) は kit 出版
  済みの有限観測 + K1334 定理 A による全称確定 (= z=25 スライスの
  供給データ)。

機体と検証は publish-then-execute で完全出版: 宣言ノート (紙面証明全文を
機械実行前に先行開示・K1344 単一オーナー・対抗 T-Z23 宣言なし・採番
事故なし (K1344 は kit 構築時と push 直前の両方で空きを probe・drafting
機体名 verify_tz23.py → verify_k1344.py 改名はラベル/docstring bytes
のみで battery byte 同一・§4/§6 に開示)) → 検証機体 verify_k1344.py
(宣言 battery 19,532 点・D8 帯域下子 gate が BB7 を独立担保) →
公式 4 走 (出版 bytes fetch-back 検証から byte-identical・rc 0・
battery 19,532 = 宣言) + detcheck.json (tamper 8/8 出版 bytes から
fail-closed・honest run record 付き)。標準 11×11 盤の全局面は
UNKNOWN 不変・verdict 不消費 (§4.5 主張の区別どおり)。
