---
id: K1319
title: "min>=9 クリティカルストリップ z=14 スライス (floor-9): H(m+15;X;14)=v(ΣX,14,m+15)（床付き floor-9 セル梯子 F14f9..A214f9 の 8 全称補題 + 自明吸収底 + 選択肢集合一致帰納の全称証明・K1317 ハンドオフ T-Z14 の完走・z=14 スライスの min>=9 全閉鎖・m=9 行は z∈{0..14} 確定で残余バンド内 z∈{15,16}）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=14 slice (floor-9, min>=9): for every m>=9 and every nonempty finite multiset X with min(X)=m, H(m+15;X;14)=v(sumX,14,m+15) (theorem T-Z14). With z*(m)=2m-2+(m mod 2) (K1268), z*(9)=17, so together with the published slice chain (low-min T-Z6..T-Z12 fixing z in {0..12}, T-Z13 fixing z=13 for min>=8 ⊇ 9) and T-Z14, the m=9 row is determined for ALL z in {0..14} (remaining in-band z in {15,16} open), and the z=14 slice is closed for ALL min>=9 (every m>=9 has z=14 in band since z*(m)>=17>14)."
  - "floor-9 cell ladder (all 8 lemmas proved universal, decomposition-independent = s-only; Cell_j(s):=H(j+15;{j}∪Y;14) with all Y tokens >=9, arity arbitrary, Y blank iff s=0, s in {0}∪{9..}): Lemma F14f9 (F14f9(s)=H(16;{1}∪Y;14) equals 1 at s=14 / v(s+1,14,16) otherwise including s=0: a SINGLE UP deviant 1>0 at s=14 and NO tail -- the F13f8 constant-2 tail (s>=14, K1317) is fully absorbed at this rung and the F-family tail shape returns to a single point: the FIFTH tail form after the z=10 death (K1279), z=11 rebirth (K1280), z=12 blister (K1316 chain), z=13 constant-2 (K1317)), Lemma G14f9 (0 at s=12, 2 at s=14, else v(s+2,14,17): DOWN 0<2 at s=12 plus UP 2>1 at s=14), Lemma E14f9 (1 at s=12, else v(s+3,14,18): single UP 1>0 at s=12 where the two deviant supply sources coalesce into one UP), Lemma D14f9 (0 at s=10, 2 at s=12, else v(s+4,14,19)), Lemma C14f9 (1 at s=10, else v(s+5,14,20): single UP), Lemma B14f9 (2 at s=10, else v(s+6,14,21): single UP 2>1), Lemma A14f9 (v(s+7,14,22) with NO deviants -- the FIRST full collapse of an A-rung cell in the ladder series, after z=13's A13f8 UP 2>0 at s=8), Lemma A214f9 (v(s+8,14,23) with NO deviants; small token 8 = one rank BELOW the published z=13 A cell; both supply sources (rung-below A14f9 and the C-hand T-Z13(8) line) are deviant-free so no case split is needed; corollary: at the min=8 z=14 claim position H(23;X;14) the value is v(sumX,14,23) whenever the second-smallest token is >=9 -- the predecl-observed out-of-band separation X=(8,8), sumX=16 (parent 2 vs single-token 1) is OUTSIDE this corollary (co-token 8<9), consistent with the z*(8)=14 frontier of K1268 C1)."
  - "proof technique (per-rung induction making every option s-only, extending the K1317 z=13 machinery to z=14): for each rung j with P_j=(j+15;{j}∪Y;14) the option set is exactly (i) an A-move on a Y-internal token a>=9: R_child=j+14=z+min exactly, so the K1264 stair (equality case) gives v(s+j-1,14,j+14), (ii) the A-move on the small token j landing on the NEXT-LOWER rung cell P_{j-1} at UNCHANGED s (bottom-up 8-rung induction; at j=1 the B-move removing the 1 gives v(s,15,15) universally, including s=0), and (iii) the C-move = the published z=13 min=j line (K1317 cell table F13f8..A13f8 for j=1..7 with the floor-8 domain {0}∪{8..} ⊇ the floor-9 points used here, and T-Z13(8)=v(s+8,13,22), no deviants, for j=8), so every Cell_j value depends only on s. DEATH-POINT DEACTIVATION (the structural simplification of this slice): every z=13 supply source positioned at s<9 (C13f8/B13f8/A13f8 at s=8) vanishes under the floor-9 domain (no valid Y with sumY<9), so the z=13 C/B/A-rank deviants never appear in the z=14 ladder; the K0832 case computation on the finitely many surviving supply positions closes each rung. Theorem T-Z14 base m=9 is TRIVIAL ABSORPTION: the a=9 child is exactly the A214f9 cell (Y=X minus one 9, all tokens >=9, sumY=S-9) which has NO deviants, so the option set is identically the stair value set for every S -- not a single excess option enters (K1274/K1275 typology, as opposed to the TOLERANT-ABSORPTION bases of T-Z12/T-Z13); the structural novelty is that as at T-Z13 the out-of-band base child forces the FULL ladder, now 8 rungs (the a=9 child is min=8 ON the frontier z*(8)=14, one rank beyond the published z=13 table), so the base typology is trivial-absorption PLUS full-ladder dependence -- the first base combining both. The m>=10 step is option-set identity: {v(S-1,14,m+14)} (a>m children at the stair edge R=z+min exactly, a=m child the induction hypothesis T-Z14(m-1) at R=m+14=(m-1)+15) and {1^v(S,13,m+14)} (C-move child, the published T-Z13 line at m>=9) matching the single-token side exactly."
  - "machine (publish-then-execute, every stage fetch-back byte-verified): pre-declaration exploration kit published FIRST (commit eec59fdd: engine_block.py sha256 582c93c1... same bytes as the K1282..K1317 chain with startup pin gate bd5f22e4..., frozen explore_z14pre.py 2890def6... / explore_z14pre.out 0d57e481..., kit README, predecl log acadb212...), declaration note 0a1163a5 (sha256 f6e0337f..., 549 lines, full paper proofs in sec.2 disclosed before machine execution), verify kit edbd3301 (verify_k1319.py 564ac761..., README extended), published official outputs eca93f76 (official_runs/run1..run4.out each e06315ae... byte-identical, detcheck.json OFFICIAL-PASS e9461543...). Declared battery 8,394 pts, all endpoint fail-closed (count mismatch itself FAILs): D1 cells 2,496 (8 cells x 312 exhaustive floor-9 shapes, s in {0}∪{9..40}, arity 0..4) / D2 strip 791 (m in {9..13}, S in m..m+39, Y parts >=m, arity(Y) <=3, engine vs v at the T-Z14 claim position) / D3 z13 anchors 297 (8 lines x 34 s-values in {0}∪{8..40} = 272 re-anchoring the embedded K1317 z=13 cell table against the engine + 25 T-Z13 C-hand anchors m in {9..13} -- the battery guarantees the z=13 table REGARDLESS of the z13 lane's official-verification state) / D4 stair anchors 256 (8 x 32 A-on-Y child stair positions) / D5 self 4,464 (single-token engine-vs-v grid 4,320 + empty-position anchors 144) / D6 deviant witnesses 13 / D7 extension 77 (tail spots s in {41..48} x 8 cells = 64, strip spots m in {14..17} = 12, m=9 base spot (24;(9,9);14)=0=v(18,14,24) = 1). Official 4 runs (PYTHONHASHSEED=random same-cwd / =1 same-cwd / 2x env -i isolated, all from PUBLISHED bytes fetched back and byte-verified) all rc 0, stdout byte-identical to the declared predry sha e06315ae..., overall_bad 0, declared totals matched exactly. Tamper battery 7/7 fail-closed from published bytes (--tamper-engine rc 2 engine gate, --tamper=cell/strip/anchor13/stair/deviant/ext rc 1 each contaminating exactly the declared single gate). Honest record (declaration sec.6): the initial local --tamper=cell mode flipped TWO points at once (G14f9 s=12 and s=14), caught by the fail-closed output D1 bad=2, corrected to a single-point flip (s=12 value 0->1) giving bad=1 and exactly the D1 gate flagged; all battery numbers and shas were measured before authoring the declaration note; paper option values were hand-computed from the K0832 closed form BEFORE machine cross-check (8 cells x representative s plus 55 supply points, 4-way agreement, 0 mismatches)."
relations:
- type: extends
  target: K1317
  note: "K1317 §5/§7 ハンドオフが指名した T-Z14 (min>=9・z=14・床は census 次第) を、floor-9 (= z−5) セル族の census 成功を受けて受け取り、z=13 で確立した床付きセル梯子機構を z=14 に拡張して全称証明した。梯子長は 7 段→8 段、底セル A214f9 の小トークン 8 は出版 z=13 A セルの 1 段下。K1317 の F13f8 恒常 2 尾が本項 F14f9 段で完全吸収され F 系尾形は第 5 形態 (単点回帰・尾なし) に。z=13 セル表 F13f8..A13f8 と T-Z13(8) は本項証明の C 手供給源として直接使用し、D3 battery が engine に対して独立再照合する。"
- type: related
  target: K1268
  note: "統合窓 sharpness 予想 C1。本項により min=9 行は z∈{0..14} が全確定 (残余バンド内 z∈{15,16})。z*(9)=17 は K1268 公式 (2m−2+(m mod 2)) の値であり、K1317 §7 にあった z*(9)=18 という記述は計算誤りとして本項宣言ノート §2.11 で訂正済み (K1317 の出版主張は z*(8)=14 のみを使用しており影響なし)。"
- type: related
  target: K1276
  note: "ストリップ定理の底構造分類への対照データ。T-Z14 の底 m=9 は過剰オプションが 1 つも入らない自明吸収型 (K1274/K1275 型) でありながら、底子 (min=8・z*(8)=14 前線上) が帯域外であるためフル 8 段梯子を要する — 自明吸収+フル梯子依存の組み合わせは初観測。底類型系列 (自明吸収→deviant 吸収→TOLERANT-ABSORPTION→自明吸収+フル梯子) の決定則は open。"
- type: depends_on
  target: K1264
  note: "階段定理 (空でない X・R=z+min(X) でちょうど H(R;X;z)=v(ΣX,z,R))。セル梯子の Y 内 A手子評価・T-Z14 母体の a>m 子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。セル梯子の全場合計算・T-Z14 単一側選択肢集合の算出基盤。宣言 §6: 本項は手計算を機械照合に先行して実施 (4 項照合 0 不一致)。"
- type: depends_on
  target: K1138
  note: "残余ゲーム H(R;X;z) の再帰・Z 座標系の定義 (engine 転写 chain pin bd5f22e4…・engine_block.py 582c93c1… は K1282..K1317 chain と同一 bytes)。"
- type: depends_on
  target: K1312
  note: "空位置・多トークン Σ tail 崩壊。セル梯子各段の白紙 A手子・s=0 列の評価に使用。"
- type: depends_on
  target: K1317
  note: "z=13 floor-8 セル表 (F13f8..A13f8・ただし s<9 deviant 位置は床上げで死点化) と T-Z13 (m>=8・C手子評価) を本項証明の供給源として直接引用。D3/D6 battery がこれらの転写を engine に独立再照合 (K1317 公式検証状態に非依存)。"
artifacts:
- path: research/log/2026-11-25-z14-predecl-exploration.md
  role: log
  commit: eec59fdd481f1e0cb809ebcd48e85ba3b3d7ffa6
  note: 宣言前探査 log (着手時 HEAD・対抗宣言不在の確認・floor-9 census 全数値・帯外分離 X=(8,8) の観測・宣言に先行する一次資料としての出版)。
- path: research/experiments/strip-z14-min9-20261125/explore_z14pre.py
  role: verifier
  commit: eec59fdd481f1e0cb809ebcd48e85ba3b3d7ffa6
  note: "凍結探索機体 (sha256 2890def6…・engine pin ゲート内蔵)。8 セル ×床付き全分解 census・tail spots・z=14 strip・帯外分離 witness を再現し宣言表と完全一致。"
- path: research/experiments/strip-z14-min9-20261125/explore_z14pre.out
  role: data
  commit: eec59fdd481f1e0cb809ebcd48e85ba3b3d7ffa6
  note: "凍結探索出力 (sha256 0d57e481…・multivalue 0 行の観測・宣言表と完全一致)。"
- path: research/experiments/strip-z14-min9-20261125/engine_block.py
  role: data
  commit: eec59fdd481f1e0cb809ebcd48e85ba3b3d7ffa6
  note: "engine ブロック単体 (sha256 582c93c1…・K1282..K1317 chain と同一 bytes・pin bd5f22e4… を explore/verify 両機体が startup ゲートで照合)。"
- path: research/experiments/strip-z14-min9-20261125/README.md
  role: log
  commit: eec59fdd481f1e0cb809ebcd48e85ba3b3d7ffa6
  note: "kit README (verify kit 出版時に検証機体セクション追記・commit edbd3301・sha256 19fdf50b…・battery/実行構成の説明・K1317 §7 ハンドオフの受領)。"
- path: research/log/2026-11-25-strip-z14-min9-single-owner-note.md
  role: declaration
  commit: 0a1163a5f1bfe781bced72b0afa8b1544b4077c3
  note: "単一オーナー宣言ノート (37,021 bytes・549 行・sha256 f6e0337fef4cbb6603e3baf01f560931585f5f504a2c87f8088c1bb00f788759)。§1 主張 (8 補題 + T-Z14 + 系 1/2)・§2 紙面証明全文 (機械実行前に先行開示・publish-then-execute)・§3 凍結探索・§4 宣言 battery 8,394 点 fail-closed + predry sha + 公式 4 走 protocol・§4.5 主張の区別・§5 open 登録・§6 宣言前探査の全開示 (honest)・§7 次レーンへの申し送り (T-Z15 floor-10)。"
- path: research/experiments/strip-z14-min9-20261125/verify_k1319.py
  role: verifier
  commit: edbd33014bd8be03cf342175fc4af6c70a153943
  note: "専用検証機体 (sha256 564ac761af0c520a43ad22c44981aa3f386c6233c3d02cfa93ee4b7493afd96c・engine pin bd5f22e4… startup ゲート・D1-D7 宣言 battery 8,394 点・変異 7 モード・点数過不足も即 FAIL)。"
- path: research/experiments/strip-z14-min9-20261125/published/official_runs/run1.out
  role: data
  commit: eca93f764571e7d72d50acbc368ea978c7b03958
  note: "公式 4 走の正本出力 (run1..run4 すべて sha256 e06315ae72ac99718615623c148145fcc7fbbf6c54a7e162b78eee73a37ed225 で byte-identical・rc 0・overall_bad 0・counts 8,394 = 宣言・出版 bytes から fetch-back 照合の上で実行)。"
- path: research/experiments/strip-z14-min9-20261125/published/detcheck.json
  role: data
  commit: eca93f764571e7d72d50acbc368ea978c7b03958
  note: "公式 deterministic check (OFFICIAL-PASS・predry/公式 4 走/tamper 7 種/kit fetch-back の全実測を記録)。"
- path: research/log/2026-11-25-strip-z14-min9.md
  role: log
  note: 完了 log (publish-then-execute チェーン eec59fdd→0a1163a5→edbd3301→公式実行→eca93f76→本 item/log commit・公式実行実測・誠実記録・次課題)。本 item と同一 commit で出版。
scope: >-
  残余ゲーム H(R;X;z) (K1138 再帰・K0832 単一トークン閉形式 v) について、すべての
  m>=9・min(X)=m を持つ空でない任意の有限多重集合 X (全形状・全アリティ) に対して
  H(m+15;X;14)=v(ΣX,14,m+15) が成立するという全称命題 (proved・床付き floor-9
  セル梯子 8 補題の K0832 場合計算 + 出版 z=13 表の引用 (s<9 deviant は床上げで
  死点化) + 底 m=9 の自明吸収 (A214f9 完全崩壊ゆえ過剰オプションなし・ただし
  フル 8 段梯子依存) + 選択肢集合一致 + m に関する帰納)。同一証明に含まれる
  数学的部品として Lemma F14f9 (s=14 単点 UP・尾なし = F 系第 5 尾形・全称)、
  Lemma G14f9 (s=12 下向き + s=14 上向き・全称)、Lemma E14f9 (s=12 上向き
  単一・全称)、Lemma D14f9 (s=10 下向き + s=12 上向き・全称)、Lemma C14f9
  (s=10 上向き単一・全称)、Lemma B14f9 (s=10 上向き単一・全称)、Lemma A14f9
  (完全崩壊 = A 段初の全称完全崩壊・全称)、Lemma A214f9 (完全崩壊・T-Z14 底セル・
  小トークン 8 = 出版表外 1 段・全称) と、A214f9 の言い換えである「min=8 の
  z=14 主張位置は第 2 小トークン >= 9 ならば v(ΣX,14,23) に崩壊」という限定文
  (co-token < 9 の帯外分離は適用外) も主張に含む。系として m=9 行の z∈{0..14}
  確定 (残余 {15,16}) と z=14 スライスの min>=9 全閉鎖が従う。min<=8 の
  z=14 セル (古典床) は本項の範囲外で open、T-Z15 (z=15・floor-10・底子が
  帯域内 m=9 に落ちる初のスライス候補)、「床 min(Y)>=z−5 が必要十分か」という
  一般床の問い (z=13 floor-8 に続き 2 つ目の肯定データ点)、F 系尾形の一般則
  (z=10 死 / z=11 再誕 / z=12 blister / z=13 恒常 2 尾 / z=14 尾なしの法則化)、
  死点化の法則化 (下位スライスの s<床 deviant が床上げで消滅する構造)、底類型
  (自明吸収+フル梯子) の決定則、m>=10 行の z∈{15..z*(m)−1} は open。11×11
  盤面のいかなる勝敗も本項の範囲外 (二石 root・S2・class 1/2/4 は全時点
  UNKNOWN・verdict 不消費)。

## 概要

K1317 (z=13 min>=8 スライス・T-Z13) の §5/§7 ハンドオフが指名した z=14 スライスを、
**床 min(Y)>=9 (floor-9 = z−5)** のセル族に限って選んだ構成で全称証明し出版した
(仮採番 K1319・publish-then-execute)。

- **T-Z14 (主定理)**: すべての m>=9・min(X)=m で H(m+15;X;14)=v(ΣX,14,m+15)。
  底 m=9 は**過剰オプションが 1 つも入らない自明吸収型** (底セル A214f9 が完全
  崩壊しているため)。構造的新事実: **自明吸収型でありながら底子 (min=8) が
  前線 z*(8)=14 上の帯域外であるためフル 8 段梯子を要する** (梯子長 7→8・
  自明吸収+フル梯子依存の組み合わせは底類型として初観測)。
- **セル梯子 8 補題 (全称・分解非依存)**: 各セルの値は ΣY=s のみで決まる。
  F14f9 は **s=14 の単点 UP で尾なし** — K1317 F13f8 の恒常 2 尾を本段で完全吸収
  し、F 系尾形は第 5 形態 (単点回帰) に。A14f9 は **A 段として系列初の完全崩壊**、
  A214f9 (小トークン 8・出版表の 1 段下) も供給源双方の deviant なしにより
  場合分け不要の完全崩壊。z=13 セルの s=8 deviant (C13f8/B13f8/A13f8) は
  床上げで**死点化**し梯子から消滅。
- **系 1**: z=14 スライスは min>=9 全域で Σ崩壊。**系 2**: min=9 行は
  z∈{0..14} 全確定 (残余バンド内 z∈{15,16}・z*(9)=17)。
- **機体**: 宣言 battery 8,394 点 fail-closed (D3 が埋込 z=13 表を engine に
  独立再照合し K1317 レーンの公式検証状態に非依存)・公式 4 走 byte-identical
  (stdout sha e06315ae…)・tamper 7/7 fail-closed・detcheck OFFICIAL-PASS 出版。

## 主張の区別 (定型)

§1 の 8 補題・T-Z14・系 1/2 は全称 (証明は宣言ノート §2 の紙面のみ)。battery と
census (multivalue 0 の観測・tail spots・帯外分離 witness) は独立の有限再照合・
観測資料であり、それ自体は全称性の証明でない。F 系尾形の一般則・死点化の
法則化・底類型の決定則・一般床の問いは open。11×11 空盤・二石 root・S2・
class 1/2/4 は全時点 UNKNOWN・verdict 不消費。
