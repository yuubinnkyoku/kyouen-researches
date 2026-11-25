---
id: K1317
title: "min>=8 クリティカルストリップ z=13 スライス (floor-8): H(m+14;X;13)=v(ΣX,13,m+14)（床付き floor-8 セル梯子 F13f8..A13f8 の 7 全称補題 + TOLERANT-ABSORPTION 底 + 選択肢集合一致帰納の全称証明・K1268 予想 C1 バンド m=8 行の完走・z=13 スライスの min>=8 全閉鎖・完全走破行は m=7 行 (K1316 chain) に続き 2 本目）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=13 slice (floor-8, min>=8): for every m>=8 and every nonempty finite multiset X with min(X)=m, H(m+14;X;13)=v(sumX,13,m+14). With z*(m)=2m-2+(m mod 2) (K1268), z*(8)=14, so together with the published chain (T-Z6..T-Z12 slices fixing z in {0..12} for the m=8 row) this CLOSES the m=8 row of the K1268 Conjecture C1 band completely (band z<z*(8): all z in {0..13} determined, zero residue), the second fully-completed row after m=7 (T-Z12, the z=12 lane's declaration chain); and the z=13 slice is closed for ALL min>=8 (every m>=8 has z=13 in band since z*(m)>=14>13)."
  - "floor-8 cell ladder (all 7 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+14;{j}∪Y;13) with all Y tokens >=8, arity arbitrary, Y blank iff s=0): Lemma F13f8 (F13f8(s)=H(15;{1}∪Y;13) equals 2 for s>=14 / 1 at s=12 / v(s+1,13,15) otherwise including s=0: deviants are exactly the s=12 DOWN 1<2 and the s>=14 UP constant-2 tail vs the collapse value 0 -- the CONSTANT-2 tail, a FOURTH tail shape for the F family after the z=10 death (K1279), the z=11 rebirth (K1280), and the z=12 blister (K1316 note)), Lemma G13f8 (G13f8(s)=H(16;{2}∪Y;13) equals 0 at s=12, otherwise v(s+2,13,16): single DOWN deviant), Lemma E13f8 (1 at s=10 / 2 at s=12 / else collapse: DOWN 1<2 at s=10 plus first spurious-2 UP 2>0 at s=12), Lemma D13f8 (0 at s=10 / else collapse: single DOWN 0<1 at s=10, same position as z=12's D12 with the role shrunk to a downward point), Lemma C13f8 (1 at s=8 / 2 at s=10 / else collapse), Lemma B13f8 (0 at s=8 / else collapse: single DOWN 0<1 at s=8 = the position of the published out-of-band witness (6,8)@z=12, s=8 remaining the center at z=13 floor-8, recorded as an observation), Lemma A13f8 (2 at s=8 / else v(s+7,13,21): single UP 2>0 deviant at s=8 -- the universal confirmation of the K1316 census preview 'A13 first A-rank break [[8],8,2,0]')."
  - "proof technique (per-rung induction making every option s-only): for the base rung the small-token A-move child is (14;Y;14)=v(s,14,14) at the blank-position stair (K1312 empty tail) and for rungs j=2..7 the option set is exactly (i) an A-move inside Y lands at the stair edge exactly (child budget j+13 = z+min of the child = 13+j, the K1264 window-edge equality, giving v(s+j-1,13,j+13)), (ii) the A-move on the small token j lands on the NEXT-LOWER rung cell at UNCHANGED s (one rung down the ladder; this is what forces the bottom-up 7-rung induction), (iii) the C-move = the published z=12 line at min=j (T-Z12(7) for j=7 and the K1316 z=12 cell table for j=1..6; the floors 3..7 are all >= the moat requirement 8>=8), so every Cell_j value depends only on s; the K0832 case computation on v then closes each rung to a finitely deviant closed form. Theorem T-Z13 base m=8 is TOLERANT-ABSORPTION: the a=8 child is the A13f8 cell at s=S-8, and ONLY at S-8=8 (i.e. sumX=16) does the excess option A13f8(8)=2 enter the option set, which is TOLERATED because mex{0,2,0}=1=mex{0}=v(16,13,22) (mex invariance) -- the same typology as the T-Z12 base (K1316 note); the structural novelty is that unlike T-Z12 whose base needed a single cell (B12), the T-Z13 base needs the FULL 7-rung floor-8 ladder because the a=8 child is the min=7 cell A13f8 and m=7 is OUT of band at z=13 (z*(7)=13), so A13f8 itself must be proved from F13f8..B13f8 (the first strip-theorem base depending on a full cell ladder). The m>=9 step is option-set identity: {v(S-1,13,m+13)} (a>m children at the stair edge R=z+min exactly, a=m child the induction hypothesis T-Z13(m-1) at R=m+13=(m-1)+14) and {1^v(S,12,m+13)} (C-move child, the published T-Z12 line at m>=8), matching the single-token side exactly."
  - "machine (publish-then-execute, all fetch-back byte-verified): pre-declaration exploration kit published FIRST (commit 2d10d0a8: engine_block.py sha256 582c93c1... same bytes as the K1282..K1315 chain with startup pin gate bd5f22e4..., frozen explore_k1317.py 182ec937... / explore_k1317.out 3fbdd1e8... , predecl log), declaration note cd47356e (sha256 3158057a... full paper proofs in sec.2 disclosed before machine execution), verify kit d90f94a6 (verify_k1317.py b2394c87...), published official outputs 570d3bdb (official_runs/run1..run4.out each 92cfd293... byte-identical, detcheck.json OFFICIAL-PASS d49a2e8e...). Declared battery 8,631 pts, all endpoint fail-closed (count mismatch itself FAILs): D1 cells 3,220 (7 cells x 460 floored shapes, s in {0}∪{8..40}, arity 0..4) / D2 strip 1,069 (m in {8..12}, engine vs v at the T-Z13 claim position) / D3 z=12 anchors 263 (independent re-verification of the embedded z=12 cell table and T-Z12 C-hand anchors against the engine -- the battery guarantees the z=12 table REGARDLESS of the K1316 lane's official-verification state) / D4 stair 231 / D5 self 3,766 / D6 deviant witnesses 13 / D7 extension 69 (tail spots s in {41..48}, strip spots m in {13..16}, and the m=8 sumX=16 TOLERANT-ABSORPTION witness H(22;(8,8);13)=1=v(16,13,22)). Official 4 runs (PYTHONHASHSEED=random same-cwd / =1 same-cwd / 2x env -i isolated) all rc 0, stdout byte-identical to the declared predry sha 92cfd293..., overall_bad 0, declared totals matched exactly. Tamper battery 7/7 fail-closed (--tamper-engine rc 2 engine gate, --tamper=cell/strip/anchor12/stair/deviant/ext rc 1 each contaminating exactly the declared single gate). explore machine deterministic 2 runs byte-identical. Honest record (declaration sec.6): the first local census run shared one 6M engine cache across all cells and was OOM-killed (rc 137, after F13f8 completed, no wrong value emitted); rebuilt with per-cell cache_clear (engine bytes unchanged, values and determinism unaffected); a declared D3 point-count typo (312, correctly 238+25=263) was caught by the fail-closed predry count check and fixed before the final predry; all battery numbers and shas were measured before authoring the declaration note."
relations:
- type: extends
  target: K1280
  note: "クリティカルストリップ系列 (T-Z6 K1274・T-Z7 K1275・T-Z8 K1276・T-Z9 K1277・T-Z10 K1279・T-Z11 K1280) の延長として、z=13 スライスを床付き floor-8 族で全称確定した。直前の z=12 スライス (T-Z12・仮採番 K1316) は z12 レーンの宣言ノートで紙面全文出版済み (出版 commit d182fcfb) であり本項証明の C手子評価・D3 battery で直接使用するが、同レーンの K item は出版時点で未出版のため relation target からは除外し prose のみで言及する (target 実在性のため)。F 系尾形の系列観測 (z=10 死 K1279・z=11 再誕 K1280・z=12 blister・z=13 floor-8 恒常 2 尾・ただし F13f8 は floor-8 族で F13 古典族とは別族) の接続点。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1 の m=8 行をバンド内で完走 (z*(8)=14・z∈{0..12} は出版 chain T-Z6..T-Z12・z=13 が本項)。完全走破行としては m=7 行 (K1316 chain) に続き 2 本目。残部 m>=9 の z∈{14..z*(m)−1} は open。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z13 の底 m=8 は過剰オプション (A13f8(8)=2) が mex を破壊しない位置でのみ入る TOLERANT-ABSORPTION 型 (mex{0,2}=1=mex{0}) で T-Z12 (K1316 note) と同類型・K1274/K1275 の自明吸収型・K1276/K1277 の deviant 吸収型との対比で 3 分類＋T-Z13 の構造的新事実 (底が全セル梯子に依存: T-Z12 の単一セル (B12) 底との差) を与える。"
- type: depends_on
  target: K1264
  note: "階段定理 (空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R))。セル梯子の Y 内 A手子評価 (i)・T-Z13 母体の a>m 子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。セル梯子の全場合計算・T-Z13 単一側選択肢集合の算出基盤。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1315 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置・多トークン Σ tail 崩壊。セル梯子底段の白紙 A手子 (14;Y;14)=v(s,14,14)・各セル s=0 列の評価に使用。"
artifacts:
- path: research/log/2026-11-25-z13-predecl-exploration.md
  role: log
  commit: 2d10d0a86953b60b0c4fd087b8670408441a9682
  note: 宣言前探査 log (着手時 HEAD・対抗宣言不在の確認・紙面誘導の予測構造・予備 census の OOM と再構成・census 全数値・手計算との一致・正式機体の凍結と先行出版)。
- path: research/experiments/strip-z13-min8-20261125/explore_k1317.py
  role: verifier
  commit: 2d10d0a86953b60b0c4fd087b8670408441a9682
  note: "凍結探索機体 (sha256 182ec937122d3a1f0a6fd379cce38279d80f6386ab7c9fdd2443ceb2303bfaf8・engine pin ゲート内蔵・決定性 2 走バイト同一)。census 7 セル ×床付き全分解・tail spots・z=13 strip 1,069 形状・T-Z13 m=8 S=16 witness を再現。"
- path: research/experiments/strip-z13-min8-20261125/explore_k1317.out
  role: data
  commit: 2d10d0a86953b60b0c4fd087b8670408441a9682
  note: "凍結探索出力 (sha256 3fbdd1e8e1340c9cb097b5d5acdedc1854901c216845d22d4688e64a2f39c712・3,220 形状 multivalue 行 0 の観測・宣言表と完全一致)。"
- path: research/experiments/strip-z13-min8-20261125/README.md
  role: log
  commit: 2d10d0a86953b60b0c4fd087b8670408441a9682
  note: "kit README (sha256 d75a3d95…・battery/実行構成の説明・K1316 §7 ハンドオフの受領)。"
- path: research/experiments/strip-z13-min8-20261125/engine_block.py
  role: data
  commit: 2d10d0a86953b60b0c4fd087b8670408441a9682
  note: "engine ブロック単体 (sha256 582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0・K1282..K1315 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/log/2026-11-25-strip-z13-min8-single-owner-note.md
  role: declaration
  commit: cd47356ea1c56c1840b3f5a86de78e2f251400af
  note: "単一オーナー宣言ノート (32,079 bytes・sha256 3158057aefe69dc585eeed87da09e7d493ef809bb934a2ee18bc3bc30828bd4d)。§1 主張 (7 補題 + T-Z13 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute)・§3 凍結探索・§4 宣言 battery 8,631 点 fail-closed + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録・§6 宣言前探査の全開示 (honest)・§7 次レーンへの申し送り (T-Z14 floor-9)。",
- path: research/experiments/strip-z13-min8-20261125/verify_k1317.py
  role: verifier
  commit: d90f94a67f1b0be8d42527be10f235973190d94f
  note: "専用検証機体 (sha256 b2394c87abb0a0e07c43c433409f4a0c9098e75443245948d439b961b647d728・engine pin bd5f22e4… startup ゲート・D1-D7 宣言 battery 8,631 点・変異 7 モード・点数過不足も即 FAIL)。"
- path: research/experiments/strip-z13-min8-20261125/published/official_runs/run1.out
  role: data
  commit: 570d3bdb3c9e597529a28e9d883fa8e40c884ccf
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 92cfd293bb7f063a576a96d2df5328973206ebf9fccd2bc88d65a1a32cf96269 で byte-identical・rc 0・overall_bad 0・counts 8,631 = 宣言)。"
- path: research/experiments/strip-z13-min8-20261125/published/detcheck.json
  role: data
  commit: 570d3bdb3c9e597529a28e9d883fa8e40c884ccf
  note: "公式 deterministic check (OFFICIAL-PASS・sha256 d49a2e8ed459047b8c9668d87459a4524dc59fdb149e7d857a47a6a8e1321bb1・predry/公式 4 走/tamper 7 種/kit fetch-back の全実測を記録)。"
- path: research/log/2026-11-25-strip-z13-min8.md
  role: log
  note: 完了 log (publish-then-execute チェーン 2d10d0a8→cd47356e→d90f94a6→570d3bdb→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=8・min(X)=m を持つ空でない任意の有限多重集合 X (全形状・全アリティ) に対して
  H(m+14;X;13)=v(ΣX,13,m+14) が成立するという全称命題 (proved・床付き floor-8
  セル梯子 7 補題の K0832 場合計算 + 出版 z=12 表の引用 + 底 m=8 の
  TOLERANT-ABSORPTION (mex 不変) + 選択肢集合一致 + m に関する帰納)。同一証明に
  含まれる数学的部品として Lemma F13f8 (F セル z=13 床 8 閉形式表・分解非依存・
  s>=14 恒常 2 尾を含む・全称)、Lemma G13f8 (単一下向き s=12・全称)、Lemma E13f8
  (s=10 下向き + s=12 上向き 2 deviant・全称)、Lemma D13f8 (s=10 下向き 1 点・全称)、
  Lemma C13f8 (s=8 下向き + s=10 上向き・全称)、Lemma B13f8 (s=8 下向き 1 点・全称)、
  Lemma A13f8 (s=8 上向き 1 点 = K1316 census 予告の全称確定・全称) も主張に含む。
  系として K1268 予想 C1 の m=8 行バンド内完走 (z∈{0..13} 全確定・残部ゼロ) と
  z=13 スライスの min>=8 全閉鎖が従う。min∈{1..7} の z=13 セル (古典床) は
  F13 ndev 298 の爆発 (K1316 §1(c) census) により本項の範囲外で open、「床
  min(Y)>=z−5 が必要十分か」という一般床の問い、T-Z14 (min>=9・z=14・床 >= 9
  セル族・底 a=9 子は min=8・z*(9)=18 で帯域内)、F 系尾形の一般則 (恒常尾の G 段
  吸収の一般条件)、m>=9 行の z∈{14..z*(m)−1}、K1316 §7 (1)-(6) の観測系 open
  (TOLERANT-ABSORPTION 底の 2 スライス連続の法則化) は open。11×11 盤面のいかなる
  勝敗も本項の範囲外 (二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費)。

## 概要

K1316 (z=12 min>=7 スライス・T-Z12) の §7 ハンドオフが指名した z=13 スライスを、
**床 min(Y)>=8 (floor-8)** のセル族に限って選んだ構成で全称証明し出版した
(仮採番 K1317・publish-then-execute)。

- **T-Z13 (主定理)**: すべての m>=8・min(X)=m で H(m+14;X;13)=v(ΣX,13,m+14)。
  底 m=8 は**過剰オプションが mex を破壊しない TOLERANT-ABSORPTION 型**
  (ΣX=16 の 1 点だけで A13f8(8)=2 が選択肢に入るが mex{0,2}=1=v(16,13,22))。
  構造的新事実: **T-Z12 の底は単一セル (B12) で足りたが、T-Z13 の底は a=8 子が
  帯域外の min=7 セル A13f8 であるため F13f8..A13f8 の全 7 段梯子を必要とする**
  (ストリップ定理の底が初めて「全セル梯子」に依存)。
- **セル梯子 7 補題 (全称・分解非依存)**: 各セルの値は ΣY=s のみで決まり、
  deviant 線形は G13f8{s=12 下向き}・E13f8{s=10 下向き, s=12 上向き}・
  D13f8{s=10 下向き}・C13f8{s=8 下向き, s=10 上向き}・B13f8{s=8 下向き}・
  A13f8{s=8 上向き} の少数点に固定。F13f8 は **s>=14 の恒常 2 尾** (F 系第 4 の
  尾形: z=10 死・z=11 再誕・z=12 blister に続き)。
- **系 1**: K1268 C1 予想の m=8 行がバンド内完走 (z*(8)=14・出版 z∈{0..12} chain
  + 本項 z=13)。**系 2**: z=13 スライスは min>=8 全域で Σ崩壊。
- **機体**: 宣言 battery 8,631 点 fail-closed (D3 が埋込 z=12 表を engine に独立
  再照合し K1316 公式検証状態に非依存)・公式 4 走 byte-identical (stdout sha
  92cfd293…)・tamper 7/7 fail-closed・detcheck OFFICIAL-PASS 出版。

## 主張の区別 (定型)

§1 の 7 補題・T-Z13・系 1/2 は全称 (証明は宣言ノート §2 の紙面のみ)。battery と
census (multivalue 0 の観測・tail spots) は独立の有限再照合・観測資料であり、
それ自体は全称性の証明でない。F 系尾形の一般則・吸収の単調則・一般床の問いは
open。11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。
