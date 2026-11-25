---
id: K1230
title: 7×7安全局面サイズ分布Z_7(λ)の15係数完全確定とλ=14のD4軌道センサス
kind: proposition
status: computed
topics:
- safe-subset
- size-histogram
- finite-complete-enumeration
- independent-verification
- geometry
aliases: ["Z_7 histogram", "n7 safe subset spectrum", "Z_7(4)=C(49,4)-F_7", "safe 14-sets D4 census n7"]
relations:
- type: depends_on
  target: K0005
  note: 総数179,810,350の独立アンカー (Round28 C++層別DP + 逆順再帰監査・和の厳密一致ゲート)
- type: depends_on
  target: K1228
  note: Z_3..Z_6係数較正 (33係数全一致) とレジューム項目「n7のsafe行サイズ別分布」の直接後継
- type: depends_on
  target: K0057
  note: F_7=6364 (collinear 660 + circle 5704) アンカー・Z_7(4)恒等式に使用
- type: depends_on
  target: K1224
  note: pinned census.mjs / forbidgen.py の幾何正本 (byte同一照合)
- type: consistent_with
  target: K1229
  note: λ≥15零は同項のn7 ge15 UNSAT×2と抄合・Z_7(14)=16>0はk=14行非空虚と抄合
artifacts:
- path: research/experiments/n7-safe-size-hist-20261122/README.md
  role: source
  note: 主張・3実装・受入条件・trust boundary
- path: research/experiments/n7-safe-size-hist-20261122/output/Z7_safe_hist.json
  role: data
  note: 正本15係数+検証データ
- path: research/log/2026-11-22-n7-safe-size-histogram-single-owner-note.md
  role: source
  note: 単一オーナー宣言 (HEAD 17e3619f観測)
- path: research/log/2026-11-22-n7-safe-size-hist-session-log.md
  role: source
  note: 発見順の実行記録
---

# 7×7安全局面サイズ分布Z_7(λ)の完全確定

標準共円盤 (q=4) 7×7の**安全部分集合** (禁止四点組を1つも含まない石配置・極大でないものも含む) のサイズ別個数Z_7(λ)を有限完全列挙で確定した。

## 確定した値

Z_7(0..14) = 1, 49, 1176, 18424, 205512, 1633048, 8796600, 29688640, 56927728, 55173324, 23478868, 3707028, 177760, 2176, 16。**総和は179,810,350でK0005出版の全安全局面数 (Round28 C++層別DP+独立逆順再帰監査) と厳密一致**。λ≥15は零。最大サイズ14。

- 付随: **λ=14の安全14集合は計16個で、D4の2つの自由軌道 (サイズ8, 8・安定群自明) に分解**。代表2個の明示は実験正本JSON。
- 数学的小核: **Z_7(4) = C(49,4) − F_7 = 211,876 − 6,364 = 205,512** (4点集合が安全⟺禁止四点組でない)。Z_7(1..3)=C(49,1..3)。この恒等式はn=3..6のZ_n(4)でも成立 (112/1626/11824/56414を全数検証)。
- K_7=14 (K0029既知値) と最大安全サイズが一致。K1228の自動極大補題によりZ_7(14)=16はn7 k=14極大行の完全個数でもある (K1225/K1229は行の非空を主張、**行の個数としての16は本項が初出**)。

## 検証方式 (3独立実装 × 分散union × 独立総数アンカー)

1. cov/stInF増分法 (safehist_n7.mjs): 全走行2回byte同一 + 初手セル7分割シャード並走unionが全係数一致。
2. マスク法 (safehist_mask.mjs): cov機構を持たない独立到達判定 (禁止トリプルマスク包含) でn7完全走行・全15係数一致。
3. Python複製実装 (dfs_py.py --safehist): n=3..6の33係数がK1228出版スペクトルと全桁一致。n7のPython完全走行は本環境の実行時間制約で実施せず (推定~1時間)、n7値の主張根拠には含めない。
4. 幾何はforbidgen.py (整数4×4行列式全列挙) ⇔ pinned census.mjs (K1224正本) のカタログがn=3..7でbyte同一、F_7=6364はK0057と一致。
5. 決定性: 全出力は乱数/時刻を含まず再実行byte同一。

## 非主張

- **Z_8 (8×8) 以降は未着手** (推定~6.7B局面で本環境の範囲外・次回レジューム)。
- サイズ別の**Grundy層** (round28_n7_layers.json) とは別物: 本項は「安全非別」のサイズ別カウントでありGrundy値の分布ではない。層別JSONはGit非管理のまま再出版していない。
- λ=14の16配置の構造分析 (円弧/直線の重ね合わせ) は行っていない。
- 有限盤の機械計算・形式証明ではない。実装・カタログ・アンカーのtrust boundaryは実験README。
- 標準11×11空盤・二石root・S2・closure classは非接触 (UNKNOWNのまま)。
