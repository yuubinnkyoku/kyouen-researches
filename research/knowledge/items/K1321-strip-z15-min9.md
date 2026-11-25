---
id: K1321
title: "min>=9 クリティカルストリップ z=15 スライス (floor-9 = z−6): H(m+16;X;15)=v(ΣX,15,m+16)（床付き floor-9 セル梯子 F15f9..A315f9 の 9 全称補題 + co-token-9 行文 A315f9 = m=9 行 z=15 の全称解決 + 自明吸収底 + m>=10 は出版 T-Z15 継承・z=15 スライスの min>=9 全閉鎖・m=9 行は z∈{0..15} 確定で残余バンド内 z∈{16}・床非感受性 10→9 の全称確定・古典床 z−5 を下回る最初のスライス）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=15 slice (floor-9 = z-6, min>=9): for every m>=9 and every nonempty finite multiset X with min(X)=m, H(m+16;X;15)=v(sumX,15,m+16) (theorem T-Z15 min>=9 edition). With z*(m)=2m-2+(m mod 2) (K1268), z*(9)=17>15, so together with the published slice chain (low-min editions fixing z in {0..12}, T-Z13 fixing z=13 for min>=8, T-Z14 fixing z=14 for min>=9, published T-Z15 (K1320) fixing z=15 for min>=10) and this theorem, the m=9 row is determined for ALL z in {0..15} (remaining in-band z=16 and frontier z=17 open), and the z=15 slice is closed for ALL min>=9. The floor of the cell ladder is 9 = z-6, the FIRST slice of the series below the classical floor z-5, an affirmative universal data point on the general-floor question (sufficiency side extends below z-5 for the first time)."
  - "floor-9 cell ladder over co-token-9 domains (all 9 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+16;{j}∪Y;15) with all Y tokens >=9 INCLUDING co-token 9, arity arbitrary, Y blank iff s=0, s in {0}∪{9..}): every closed form is IDENTICAL to the published floor-10 table (K1320) -- floor-insensitivity 10->9 proved universally (no supply source sits below 9: z=14 deviant positions {10,12,14}, lower-rung deviants {10,12,14}, tail region s>=16, absorption-identity break s>=16; the newly admitted floor-entry level s=9 is supply-free in all 9 rungs). Lemma F15f9 (s=14 DOWN 1<2 / s=15 hole / CONSTANT 2 for ALL s>=16, the F-family SIXTH tail form; the absorption identity v(s,16,16)=v(s,15,16) holds for the EXTENDED range {0}∪{9..15} and breaks at s>=16 -- the below-band j=1 B-move child (16;Y;16)=v(s,16,16) (lemma BB-f9 = K1264 stair + K1312 empty) remains the live tail supply source), Lemma G15f9 (0 at s=14, F tail fully absorbed at the G rung, no own tail), Lemma E15f9 (1 at s=12, 2 at s=14), Lemma D15f9 (0 at s=12), Lemma C15f9 (1 at s=10, 2 at s=12), Lemma B15f9 (0 at s=10), Lemma A15f9 (2 at s=10), Lemma A215f9 (no deviants, full collapse -- the a=9 child), Lemma A315f9 (no deviants: A315f9(s)=v(s+9,15,25) over the FULL m=9-row claim position domain H(25;{9}∪Y;15) with co-token 9 allowed and arbitrary arity, SOLVING the K1320 sec.5 open (1) 'm=9-row z=15 line' in full: every nonempty X with min(X)=9 is {9}∪Y with Y tokens >=9, so H(25;X;15)=A315f9(S-9)=v(S,15,25))."
  - "proof technique (per-rung s-only induction copied structurally from K1320 with two new parts, both disclosed before machine execution): NEW PART 1 -- the co-token-9 A-move: for rungs j in {1..8} a Y-internal 9 decrements to 8 >= j so the child min stays j and the stair (equality case R=j+15=z+min) replicates v(s+j-1,15,j+15); at rung j=9 (and at the theorem bottom m=9) the a=9 child has min 8 and lands EXACTLY on the A215f9 cell position (child = (24;{9}∪Y∖{9}∪{8};15) = A215f9(s)), an EQUIVALENT REPLICATION of the stair value v(s+8,15,24) for all s because A215f9 has no deviants -- co-token existence never adds an excess option; NEW PART 2 -- floor-entry level s=9: neither the published z=14 lines nor any rung has a deviant at 9 (all supply locations are within {10,12,14}∪{16..}), so s=9 collapses in all 9 rungs with the alternating singleton option sets O={1} (odd j) / O={0} (even j) (representative hand computation F15f9(9): (i)=v(9,15,16)=1, (ii')=v(9,16,16)=1 by the s=9 case of the extended absorption identity, (iii)=1^v(10,14,16)=1, mex{1}=0=v(10,15,17)); the remaining supply-point cases s in {10,12,14,16..} are the K1320 evaluations verbatim (values depend only on s). Theorem bottom m=9 (new): (a>9) children = stair v(S-1,15,24); (a=9) children = A215f9(S-9)=v(S-1,15,24) (identical); (C) child = published T-Z14(9) line 1^v(S,14,24); the option set equals the single-token S-rec set of v(S,15,25) for every S, TRIVIAL ABSORPTION with no case analysis (K1274/K1275 typology, co-token variant); m>=10 inherited verbatim from published T-Z15 (K1320 sec.2.11)."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration exploration kit published FIRST by a parallel lane execution (commit 5ec6c35d: engine_block.py sha256 582c93c1... same bytes as the K1282..K1320 chain with startup pin gate bd5f22e4..., frozen explore_z15m9.py 00d15acb... / explore_z15m9.out 52a9808e... determinism 3 byte-identical runs, kit README db051467... extended to b6dc0392..., predecl log e09585a8...) plus an independent second-lane verification log (commit e386b59b: published-bytes re-run 3x byte-identical, shared 8-cell deviant tables fully agreeing, below-band floor-9 collapse 312 shapes agreeing, zero discrepancies), declaration note cfa1c6b0911da6dd81005ed9f842912ef7cbca1b (sha256 2dd9cd7a7723b842827629fdfe9abc9bd652ce211670520129fecaccd9678e62, 57,572 bytes, 812 lines, full paper proofs in sec.2 disclosed before machine execution), verify kit 65db46fd2b736611dfba4bd8979586bf569f0de0 (verify_k1321.py 9eb114c1547c3a348154055d39ebd34a6f233d49a05899d23d169f2533bf87da), published official outputs 24789e2af467d3884b9f739552857ccdd4ed3c2b (official_runs/run1..run4.out each c337e63b37f2f7fdc0b0e22f16b3210a37e3fd1d59abcacaec57195bdaf7d381 byte-identical, detcheck.json OFFICIAL-PASS 00e36be9b25c773f42ba792799816861a0ef34d4a01fbb8eda8e43d730d5ac88). Declared battery 10,532 pts, all endpoint fail-closed (count mismatch itself FAILs): D1 cells 2,808 (9 cells x 312 exhaustive floor-9 shapes, s in {0}∪{9..40}, arity 0..4) / D2 strip 859 (NEW m=9 claim positions 265 shapes + m in {10..14} re-measure 594) / D3 z14 anchors 294 (8 lines x 33 s-values = 264 + 30 T-Z14 C-hand anchors m in {9..14} -- INCLUDING m=9, i.e. the j=9 C-hand line, closing the D3 gap noted by the K1320 second-lane verification) / D4 stair anchors 288 (9 x 32 A-on-Y child stair positions, s in {9..40}) / D5 self 5,865 (same grid as K1320 incl. z=16 for lemma-BB-f9 evaluations + 153 empty-position anchors) / D6 deviant witnesses 20 (17 K1320 witnesses over the floor-9 domain + 3 NEW: F15f9 s=9 FLAT 0 floor-entry, A215f9 s=9 FLAT 1 floor-entry, A315f9 co-token (Y=(9,)) FLAT 0 = claim-position shape H(25;(9,9);15)=v(18,15,25)) / D7 extension 86 (tail spots 72, strip spots 12, NEW m=9 base spot (25;(9,9);15)=0=v(18,15,25), m=10 base spot continuity) / D8 below-band anchors 312 (lemma-BB-f9 supply source H(16;Y;16) vs v(s,16,16) over the FULL floor-9 decomposition sweep). First full machine run PASSed outright; predry 6 runs byte-identical; official 4 runs (PYTHONHASHSEED=random same-cwd / =1 same-cwd / 2x env -i isolated dirs, from published bytes cmp-verified) all rc 0, stdout sha = declared predry sha, overall_bad 0, declared totals matched exactly; tamper battery 8/8 fail-closed from published bytes. Honest record (declaration sec.6 + detcheck): the two env -i isolated official runs initially hit rc 2 with empty stdout because the fetched-back file had been copied under the name fb_verify.py inside the isolation dirs (python: cannot open file) -- fixed by renaming to verify_k1321.py and re-running, rc 0 byte-identical, machine bytes untouched, failed runs produced zero output."
relations:
- type: extends
  target: K1320
  note: "K1320 §5 open① (m=9 行 z=15 の行文) と §7 ハンドオフ (a) を受領。floor-10 セル梯子 (F15f10..A315f10) を床 9 に拡張して 9 補題を全称証明し、A315f9 を限定文 (co-token >= 10) から行文 (co-token 9 許容・全アリティ) に拡張して open を解決。閉形式表は floor-10 版と全域同一 (床非感受性 10→9 の全称確定・供給源位置はすべて 9 以上)。m>=10 段は出版 T-Z15 をそのまま継承して m>=9 の主張を合成。梯子長は 9 段のまま・帯域下供給源も継承。"
- type: depends_on
  target: K1319
  note: "z=14 floor-9 セル表 F14f9..A214f9 と T-Z14 定理線 (m>=9) を本項証明の C 手供給源として直接引用。floor-9 版では K1319 定義域 {0}∪{9..} が梯子の Y>=9 と厳密一致 (K1320 で必要だった部分集合引数を廃し定義域の非対称を解消)。D3 battery が 8 線の転写を engine に独立再照合し、さらに T-Z14 C 手位置アンカーを m∈{9..14} に広げて j=9 線 (= K1320 レーンで未 anchor だった箇所) を直接 anchor。"
- type: related
  target: K1268
  note: "統合窓 sharpness 予想 C1。本項により min=9 行は z∈{0..15} が全確定 (残余バンド内 z∈{16}・前線 z∈{17}=z*(9))。z*(9)=17 は K1268 公式の値。m=9 行 z=17 前線の観測 ((9,10) 単一分離・z16-min9 kit) と整合し、奇数 m 前線構造の全称候補が次課題。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z15 min>=9 版の底 m=9 は co-token-9 (a=9) 子が底子 A215f9 に正確に一致して階段値と恒等的同値になる自明吸収型 (K1274/K1275 型の co-token 変種)。底類型系列 (自明吸収→deviant 吸収→TOLERANT-ABSORPTION→自明吸収+フル梯子依存→自明吸収+帯域内底子 (K1320)→自明吸収+co-token 吸収 (本項)) の決定則は open。"
- type: depends_on
  target: K1264
  note: "階段定理。セル梯子の Y 内 A 手子評価 (R=j+15=z+min ちょうど・co-token 9 を含む全 a>=9 で窓端等号)・補題 BB-f9 ((16;Y;16) の R=16<=16+min(Y))・底 m=9 の (a>9) 子評価に使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。セル梯子の全場合計算 (floor 参加点 s=9 の場合を含む)・吸収恒等式拡張 ({0}∪{9..15})・T-Z15 単一側選択肢集合算出の基盤。宣言 §6: 本項は手計算を機械照合に先行して実施 (不一致 0・初回 full 実行 PASS)。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1320 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置・多トークン Σ tail 崩壊。セル梯子各段の白紙 A手子・s=0 列・帯域下子 (16;Y;16) の白紙位置評価に使用。"
artifacts:
- path: research/experiments/strip-z15-min9-20261125/explore_z15m9.py
  role: verifier
  commit: 5ec6c35d
  note: "凍結探索機体 (sha256 00d15acb…・engine pin ゲート内蔵・先行並走レーンの出版)。9 セル ×床付き全分解 census (312 形状/セル)・tail spots・strip m∈{9..14}・帯域下子 floor-9 census・m=9 行帯域内記録・名付き witness を再現し宣言表と完全一致。(publish 流程上の一次資料)"
- path: research/experiments/strip-z15-min9-20261125/explore_z15m9.out
  role: data
  commit: 5ec6c35d
  note: "凍結探索出力 (sha256 52a9808e…・決定性 3 走 byte-identical・multivalue 0 行の観測・宣言表と完全一致)。"
- path: research/log/2026-11-25-z15m9-predecl-exploration.md
  role: log
  commit: 5ec6c35d
  note: "宣言前探査 log (sha256 e09585a8…・先行出版・本項の受領)。9 セル census 全数値・床非感受性の観測・m=9 行 152 形状分離 0・宣言に先行する一次資料。"
- path: research/log/2026-11-25-z15m9-kit-second-lane-verification.md
  role: log
  commit: e386b59b
  note: "第二レーン独立検証 log (sha256 702b6f8e…・先行出版・本項の受領)。出版 kit bytes の 3 走再実行 byte-identical・共有 8 セル deviant 表完全一致・帯域下子 floor-9 崩壊 312 形状完全一致・不一致 0 件の二重測定。"
- path: research/experiments/strip-z15-min9-20261125/engine_block.py
  role: data
  commit: 5ec6c35d
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1320 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/experiments/strip-z15-min9-20261125/README.md
  role: log
  commit: 65db46fd2b736611dfba4bd8979586bf569f0de0
  note: "kit README (拡張前 sha256 db051467… で先行出版・検証機体出版時に機体セクション追記・拡張版 sha256 b6dc0392…・battery/実行構成の説明・K1320 ハンドオフの受領)。"
- path: research/log/2026-11-25-strip-z15-min9-single-owner-note.md
  role: declaration
  commit: cfa1c6b0911da6dd81005ed9f842912ef7cbca1b
  note: "単一オーナー宣言ノート (57,572 bytes・812 行・sha256 2dd9cd7a7723b842827629fdfe9abc9bd652ce211670520129fecaccd9678e62)。§1 主張 (9 補題 + T-Z15 min>=9 版 + 系 1/2/3)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute・co-token 9 の取扱いと床参加点 s=9 の場合計算を含む)・§3 凍結探索・§4 宣言 battery 10,532 点 fail-closed + predry sha + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録・§6 宣言前探査の全開示 (honest)・§7 次レーンへの申し送り。"
- path: research/experiments/strip-z15-min9-20261125/verify_k1321.py
  role: verifier
  commit: 65db46fd2b736611dfba4bd8979586bf569f0de0
  note: "専用検証機体 (sha256 9eb114c1547c3a348154055d39ebd34a6f233d49a05899d23d169f2533bf87da・engine pin bd5f22e4… startup ゲート・D1-D8 宣言 battery 10,532 点・変異 8 モード・点数過不足も即 FAIL・fetch-back byte 一致)。"
- path: research/experiments/strip-z15-min9-20261125/published/official_runs/run1.out
  role: data
  commit: 24789e2af467d3884b9f739552857ccdd4ed3c2b
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 c337e63b37f2f7fdc0b0e22f16b3210a37e3fd1d59abcacaec57195bdaf7d381 で byte-identical・rc 0・overall_bad 0・counts 10,532 = 宣言・出版 bytes から fetch-back cmp 照合の上で実行)。"
- path: research/experiments/strip-z15-min9-20261125/published/detcheck.json
  role: data
  commit: 24789e2af467d3884b9f739552857ccdd4ed3c2b
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 00e36be9…・predry 6 走/公式 4 走/tamper 8 種/kit fetch-back の全実測・タイミング走・honest 注記 (env -i 初回 rc 2 のファイル名事故と再実行) を記録)。"
- path: research/log/2026-11-25-strip-z15-min9.md
  role: log
  note: "完了 log (publish-then-execute chain 5ec6c35d→cfa1c6ba→65db46fd→24789e2a→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。"
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=9・min(X)=m を持つ空でない任意の有限多重集合 X (全形状・全アリティ・
  co-token 9 を含む) に対して H(m+16;X;15)=v(ΣX,15,m+16) が成立するという
  全称命題 (proved・床付き floor-9 (z−6) セル梯子 9 補題の K0832 場合計算 +
  出版 z=14 表の引用 (定義域厳密一致) + 補題 BB-f9 の帯域下子崩壊 (吸収恒等式
  の floor-9 拡張 {0}∪{9..15} と破れ s>=16 = F 尾供給源) + 底 m=9 の自明吸収
  (co-token-9 A 手子が A215f9 に正確一致で階段値と恒等的同値・過剰オプションなし) +
  選択肢集合一致 + m>=10 の出版 T-Z15 継承)。同一証明に含まれる数学的部品として
  Lemma F15f9 (s=14 下向き単点 + s=15 穴 + s>=16 恒常 2 尾 = F 系第 6 尾形・
  供給源は帯域下子・床 9 版でも全称)・G15f9 (F 尾の G 段完全吸収)・E15f9・
  D15f9・C15f9・B15f9・A15f9 (各下向き/上向き単点群)・A215f9 (完全崩壊)・
  A315f9 (完全崩壊 = m=9 行 z=15 行文そのもの・co-token 9 を含む全形状) と、
  床非感受性 (10→9) の全称帰結 (9 セルの閉形式が床低下で 1 点も変わらない)
  も主張に含む。系として z=15 スライスの min>=9 全閉鎖と m=9 行の z∈{0..15}
  確定が従う。z=15 スライスの min<=8 (古典床側・beyond-frontier で分離の観測
  あり) は本項の範囲外で open、m=9 行残余 z∈{16} (バンド内)・z∈{17} (前線)
  は open、床 7 z=15 の census、帯域下子の一般理論、F 系尾形の一般則、
  底類型 (co-token 吸収型) の決定則、m>=10 行の z∈{16..z*(m)−1} は open。
  11×11 盤面のいかなる勝敗も本項の範囲外 (二石 root・S2・class 1/2/4 は全時点
  UNKNOWN・verdict 不消費・battery 10,532 点は定理の実機照合であって証明の
  代替ではない)。

## 概要

K1320 (z=15 min>=10 スライス・T-Z15) の §5 open 登録と §7 ハンドオフが指名した
floor-9 z=15 スライスを、先行出版済み predecl kit (`5ec6c35d`) と第二環境検証 log
(`e386b59b`) を受領して全称証明し出版した (publish-then-execute)。

- **T-Z15「min>=9 版」(主定理)**: すべての m>=9・min(X)=m で
  H(m+16;X;15)=v(ΣX,15,m+16)。**床は z−6 = 9 で、ストリップ系列で初めて古典床
  z−5 = 10 を下回る** — 「一般床の問い (min(Y)>=z−5 は必要十分か)」への
  最初の z−5 を破る全称肯定的データ点 (必要性側の証拠はゼロのまま・z=15 の
  セル観測は床 8 でも s-only が継続しており下限はむしろ前線で決まるとの
  構造観測)。
- **底 m=9 (新規)**: (a=9) co-token の A 手子は min 8 に落ちるが位置として
  **A215f9 セルそのもの**に一致し A215f9(S−9) = v(S−1,15,24) = 階段値
  (全 S で恒等的同値) — co-token の存在が底に過剰オプションを 1 つも持ち
  込まない自明吸収型 (co-token 変種・K1274/K1275 型)。m>=10 は出版 T-Z15 を
  そのまま継承。
- **A315f9 = m=9 行 z=15 の行文そのもの**: Y>=9 (co-token 許容) の拡張により
  A315f9 は限定文ではなく H(25;X;15) の全 min=9 形状 (全アリティ・X=(9) 含む)
  を網羅する。K1320 系 3 の open は閉じた。
- **床非感受性 (10→9) の全称確定**: 供給源位置がすべて 9 以上 ({10,12,14}∪{16..})
  にあるため、9 セルの閉形式は床低下で 1 点も変わらない (先行探査の
  観測「位置・方向・値まで同一」の全称化)。
- **系**: z=15 スライスは min>=9 全閉鎖 (z*(m)>=z*(9)=17>15・K1268)。
  m=9 行は z∈{0..15} 全確定 (残余バンド内 z∈{16}・前線 z∈{17})。

機体と検証は publish-then-execute で完全出版: 宣言ノート (812 行・紙面証明全文
を機械実行前に先行開示) → 検証機体 verify_k1321.py (宣言 battery 10,532 点・
D3 は T-Z14 C 手アンカーに m=9 を含む j=9 線を直接 anchor・D6 に床参加点 2 点
と co-token 主張位置 1 点の新 witness・D8 帯域下子 floor-9 census 312 形状) →
公式 4 走 (出版 bytes fetch-back cmp 照合から byte-identical 全 rc 0・
overall_bad 0・点数過不足 fail-closed) + tamper 8/8 fail-closed → detcheck.json
OFFICIAL-PASS。手計算は機械照合に先行 (不一致 0・初回 full 実行 PASS)。
11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費
(battery 点数は定理の実機照合であって証明の代替ではない)。
