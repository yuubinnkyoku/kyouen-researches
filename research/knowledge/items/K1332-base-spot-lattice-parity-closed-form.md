---
id: K1332
title: "base-spot 格子パリティ補題: すべての z>=11 で v(2z−10; z; 2z−4) ≡ z (mod 2)（K0832 単一トークン閉形式の中間枝による 3 行 engine-free 証明・機械照合 z∈{11..200} 全 190 行で枝不変量 4 種成立・出版 base-spot 観測列 0/1/0/1/0/1 (z=16..21) は崩壊側パリティと全点一致・証明済みスライス T-Z15..T-Z19 では base-spot 値そのものが corollary に格上げされ z=15 値 1 を系として新規確定・z=20/21/22 は census 観測 (z=22 の値 0 は同日出版の z22 kit 実測で補題予言と一致)・予測 z=23→1・z=24→0〔K番号は仮・統合時再採番予定〕）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "Base-spot lattice parity lemma: for every z >= 11, v(2z-10; z; 2z-4) = z (mod 2), where (R;X;z) = (2z-4; (z-5,z-5); z) is the base-spot lattice position of slice z (T-Zz numbering R=m+z+1 at m=z-5, sum(X)=2z-10). Proof engine-free from the published K0832 single-token closed form: with x=2z-10, (i) 1 <= z <= x-1=2z-11 holds iff z>=11 (middle regime); (ii) q_odd(z) <= z < R=2z-4 for z>4; (iii) R < x+z=3z-10 iff z>6; hence the middle branch applies and v=(R+z)%2=(3z-4)%2=z (mod 2). COROLLARY (proved slices): for each z in {15..19} the published strip theorem T-Zz (K1320 z=15 min>=10, K1322 z=16 min>=11, K1325 z=17 min>=12, K1328 z=18 min>=13, K1330 z=19 min>=14; universal claim H(m+z+1;X;z)=v(sumX;z,m+z+1) at min(X)=m>=z-5) covers X=(z-5,z-5), so the base-spot value is a THEOREM COROLLARY (z=15..19 values 1,0,1,0,1): four points (z=16..19) of the published base-spot z-parity sequence are promoted from observations to corollaries and the z=15 point (=1) is newly fixed as a corollary. The z=20/21 points (0, 1) agree on the collapse side; absorption (base-spot H = collapse) at z=20/21 is a census observation pair (cross-run verified 2026-11-25: both published census kits vs an independent re-measurement kit, full-row agreement), to become a corollary once T-Z20/T-Z21 are declared. The same-day z22-min17 census kit (commit 115c0bb9) measured H(40;(17,17);22)=0=v(34,22,40), the seventh observation point, matching the lemma prediction. Predictions: z=23 base spot 1, z=24 base spot 0 (collapse side closed-form for all z>=11; absorption side conditional on the slice proofs)."
relations:
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)・q_odd・中間枝 (R+z)%2 が本項の全基盤。z>=11 では x=2z−10 に対し 1<=z<=x−1 剛好を満たし (z<=2z−11)、m=q_odd(z)<=z<2z−4=R、R<x+z=3z−10 (z>6) により中間枝が確定することを機械照合 (z∈{11..200}) と手計算の両面で確認。"
- type: depends_on
  target: K1320
  note: "系の z=15 側: T-Z15 (min>=10) の全称主張が base-spot 位置 X=(10,10), R=26 を含み、H(26;(10,10);15)=1 (=15 mod 2) が corollary として確定。"
- type: depends_on
  target: K1322
  note: "系の z=16 側: T-Z16 (min>=11) が X=(11,11), R=28 を含み H=0 が corollary。"
- type: depends_on
  target: K1325
  note: "系の z=17 側: T-Z17 (min>=12) が X=(12,12), R=30 を含み H=1 が corollary。"
- type: depends_on
  target: K1328
  note: "系の z=18 側: T-Z18 (min>=13) が X=(13,13), R=32 を含み H=0 が corollary。"
- type: depends_on
  target: K1330
  note: "系の z=19 側: T-Z19 (min>=14) が X=(14,14), R=34 を含み H=1 が corollary。z=20/21 の base-spot 観測 (0, 1) は同日 cross-run 検証 (本項 artifacts) で再確認済み。"
- type: related
  target: K1138
  note: "残余ゲーム H(R;X;z) 再帰と Z 座標系。本項の主張は崩壊値 v に対する閉形式系であり、H 値との一致 (吸収) は系の z∈{15..19} と z=20/21 の観測に限る。"
- type: related
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2) とは独立 (本項は z* を使わない)。base-spot 格子位置 R=2z−4=m+z+1 は各スライスの帯域内領域に属する点の対照記録として関連。"
artifacts:
- path: research/experiments/crossrun-z20-z21-verification-20261125/verify_z21_indep.py
  role: verifier
  note: "z=21 独立再測定機体 (sha256 43aa03b2…・本レーン自前 z20 explorer ← 出版 z19 kit 機体の子孫・出版 z20/z21 機体からは非派生・engine pin bd5f22e4… startup ゲート内蔵)。section (h) が本項の機械照合 (z∈{11..200}・枝不変量 4 種の全行記録) を収録。決定性 4 走 byte-identical。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/verify_z21_indep.out
  role: data
  note: "凍結出力 (sha256 07ef7cd4…・engine_gate PASS を含む・section (h) の 190 行照合・mismatches=[]・6 観測点 z=16..21 の崩壊値 0/1/0/1/0/1 を収録)。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/compare_z21.py
  role: verifier
  note: "出版 z21 凍結出力との全値行比較スクリプト (330 行 / 436 項目 / 不一致 0)。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/compare_z20.py
  role: verifier
  note: "出版 z20 凍結出力との全値行比較スクリプト (242 行 / 335 項目 / 不一致 0・共有 s-域 {0}∪{12..56} の恒等式比較を含む)。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/z20_crossrun/explore_z20f15.py
  role: data
  note: "本レーン自前の z=20 探索機体 (sha256 d4df9769…・出版 z20 kit 機体 d4648301… とは別派生・重複のため未出版のまま検証資産化)。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/z20_crossrun/z20_run1.out
  role: data
  note: "本レーンの z=20 凍結出力 (sha256 3576d0d7…・5 走 byte-identical・ordered-engine 一致済み)。"
- path: research/experiments/crossrun-z20-z21-verification-20261125/engine_block.py
  role: data
  note: "出版 chain engine 単体 (sha256 582c93c1…・startup pin bd5f22e4…)。"
- path: research/experiments/strip-z21-min16-20261125/explore_z21f16.out
  role: data
  commit: 8a106233
  note: "出版 z21 census 凍結出力 (sha256 10f94100…・本項の系・観測点 z=21 (1) の一次出典・cross-run 全行一致検証の比較対象)。"
- path: research/experiments/strip-z20-min15-20261125/explore_z20f15.out
  role: data
  commit: 2cc16d34
  note: "出版 z20 census 凍結出力 (sha256 09e9026a…・観測点 z=20 (0) の一次出典・cross-run 全行一致検証の比較対象)。"
- path: research/log/2026-11-25-z20-z21-crossrun-verification.md
  role: log
  note: "本項の一次記録 (衝突回避記録・z20/z21 全行一致 330/436/0 と 242/335/0・補題証明と corollary の帰結表・事前調査 (repo 全域探索で parity 閉形式証明の先行なし)・K番号仮の開示を含む)。"
---

# K1332: base-spot 格子パリティ補題 (engine-free)

## 主張

- **補題 (全称・z>=11)**: v(2z−10; z; 2z−4) ≡ z (mod 2)。
  ここに (2z−4; (z−5,z−5); z) はスライス z の base-spot 格子位置
  (T-Zz 番号 R=m+z+1 の底 m=z−5、ΣX=2z−10)。v は K0832 単一
  トークン閉形式 (崩壊値)。
- **系 (証明済みスライス z=15..19)**: T-Zz (K1320/K1322/K1325/
  K1328/K1330) の全称主張は min(X)=m>=z−5 を含むので、各 z∈{15..19}
  に対し H(2z−4; (z−5,z−5); z) = z (mod 2) が定理系として確定する
  (値列 z=15..19: 1, 0, 1, 0, 1)。出版 base-spot z-parity 観測列
  (0/1/0/1/0/1 at z=16..21) のうち z=16..19 の 4 点は観測から系へ
  格上げされ、z=15 (値 1) が新規に系として確定する。

## 証明

x=2z−10, R=2z−4 とおく。z>=11 のとき:

1. 1 <= z <= x−1 = 2z−11 (z>=11 と同値) — K0832 の中間領域。
2. m=q_odd(z) <= z < 2z−4 = R (z>4)。
3. R < x+z = 3z−10 ⟺ z>6。

よって中間枝 (m<R<x+z) が選ばれ
v = (R+z)%2 = (3z−4)%2 = z (mod 2) (4 は偶数)。∎

系の証明: T-Zz の主張位置 R=m+z+1・min(X)=m>=z−5 において X=(z−5,z−5)
は min(X)=z−5⊆定義域、ΣX=2z−10、R=2z−4 なので補題の閉形式値と
H 値が一致し、その閉形式値 ≡ z (mod 2)。∎

(z<=10 では条件 1 が崩れ本補題の範囲外。z=20/21 の base-spot は
T-Z20/T-Z21 の宣言待ちで現時点では観測。)

## 機械照合

z∈{11..200} 全 190 行: 各行で value == z%2 と枝不変量 4 種
(z<=x−1 / z>=1 / q_odd(z)<R / R<x+z) を全行照合、不一致 0
(kit verify_z21_indep.py section (h)、engine recursion 不使用の
純閉形式照合・凍結出力に全記録)。出版観測点 z=16..21 の崩壊値
0/1/0/1/0/1 は補題の予言と全点一致。

## 観測との整合

- z=16..19: 本系により証明済み (出版観測は corollary と重複)。
- z=20 (0), z=21 (1): 吸収 (base-spot H 値 = 崩壊値) は census
  観測。2026-11-25 の cross-run 検証 (出版 2 kit vs 本レーン独立
  再測定 kit、全行一致 242/335/0 と 330/436/0) で再確認。
  T-Z20/T-Z21 宣言後に corollary へ格上げ予定。
- z=22 (0): 本項の執筆時点と同日に出版された z22-min17 census kit
  (commit 115c0bb9) が base spot H(40;(17,17);22)=0=v(34,22,40) を
  実測し、本補題の崩壊側予言 (22 mod 2 = 0) と一致した (7 観測点目)。
- 予測: z=23 → 1, z=24 → 0, ... (崩壊側は z>=11 全確定。吸収側は
  各スライス証明の条件付き)。

## 限界

- 本項の全称範囲は崩壊値 v に対するもの。H 値 (engine 値) への
  主張は系の z∈{15..19} に限り、z>=20 の base-spot の H=崩壊は
  吸収証明太原の観測。
- K0832 閉形式自体の妥当性は K0832 が担う (本項はその系)。
- 盤面 verdict とは無関係 (11×11 空盤・二石 root・S2・class 1/2/4
  すべて UNKNOWN のまま・verdict 不消費)。

## honest 記録

- **K 番号 1332 は仮** (並走レーン運用のため。items/ には既に
  K1330 の二重採番が存在: K1330-strip-z19-min14.md と
  K1330-pg2q8-pgammal-cap-orbits.md)。統合時に再採番予定。
- **採番の経緯 (索引遅延の教訓)**: 当初 K1331 を採番したが、push
  直前の実パス確認で research/knowledge/items/
  K1331-pg2q9-cap-structure.md (PG(2,9) レーン・19:11Z 出版) が
  発見され、番号を K1332 に変更した。数分前の repo 全域 code search
  (GitHub 索引) は K1331 を 0 件と返しており、索引遅延が原因。
  並走レーン運用では K 番号の空き確認に code search だけでなく
  items/ の実パス・直近 commit の直接確認が必要。
- **事前調査**: 2026-11-25 時点で repo 全域 code search により
  base-spot パリティの閉形式証明項目は未発見。出版 z20/z21 census
  log は base-spot 列を「SIX data points (z=22 candidate: 0)」と
  観測として記録しており閉形式証明を含まない — 本項が初出。
- cross-run 検証は同一 engine bytes・同一サンドボックスクラスでの
  別セッション再測定であり第三者機関検証ではない (kit README
  caveats 参照)。
