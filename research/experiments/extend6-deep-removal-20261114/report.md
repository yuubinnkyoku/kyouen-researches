# 深除去列拡張列挙による下界更新 — M_{6,5} ≥ 31・M_{6,6} ≥ 24（2026-11-14）

固定幅 6×m の open 境界（(6,5)・(6,6)）の下界を、既知 witness プールに対する
**深除去列拡張列挙**（extend6.js）で更新した。すべての witness は
JS census 不使用検証器（verifyConfig）と Python 別実装独立検証器
（Fraction 厳密演算・石ペア直線・石3点組円の全列挙 = K0815 と同方式）の
2系統で safe + maximal PASS。

## 結果

- **M_{6,5} ≥ 31**（従来 ≥30）: 23石の欠損極大安全配置が **6×30** に 2件
  （行構成 4,4,4,4,3,4・いずれも 6×29 23石witness（K0815）から rem=4/add=4・off=1）。
  K0815 第1弾の「6×30 未決着」（kissat 260s・余剰0空列ブロック・r≤3+新規列追加では不発）
  を決着させ、M_{6,5}=30 の可能性を反証。境界は [31,658] に。
- **M_{6,6} ≥ 24**（従来 ≥23）: 29石の欠損極大が **6×23** に 8件
  （行構成 5,4,5,5,5,5・いずれも 6×22 29石witness（K0815）から rem=3/add=3・off=0 が4件・off=1 が4件）。
  K0815 の「6×23 kissat 260s 未決着」を決着。境界は [24,495] に。

## 手法: 深除去列拡張列挙（extend6.js）

既知witness（base・w×baseM）を off 列シフトし、r 石を除去（rmin≤r≤rmax）し、
未ブロック空セルへ追加 A（|kept|+|A| ≤ w(q−1)−1）した形の候補を
**決定的に全列挙**する（scripts/extend6.js・ヘッダに完全性議論）。

部分空間内の完全性（要旨）: 候補 C = (base シフト) − R + A が safe なら、
A の各石は kept 上で ≥q−1 石を載せる曲線に乗らない（さもなければ unsafe）ので
A は kept に対して未ブロックの空セルのみから選べる。逆にそのようなセルの
全部分集合を列挙し、各候補を census 不使用 verifyConfig で全検証する。
base footprint 内への追加はより小さい r で被覆される。off は 0..targetM−baseM の全水平位置。

効率化: 除去DFSで曲線ごとの kept 計数・セルごとの blocked 計数を増分管理、
追加列挙は U セル（空・未ブロック）の曲線バケット M1..M6 と
曲線×U の bitmask AND popcount で枝刈り。**文書化済みの不完備スキップ**:
u>24 または maxA>6 の葉は列挙を打ち切る（uOverflow に計上・下記の陰性結果の証拠力は
この分だけ弱い。陽性結果（witness）は影響を受けない）。

## 較正（既知witness再現）

- 6×28 22石（K0811・sa3）→ 6×29 r=0: K0815 の 23石witness（行 4,4,4,4,3,4）を off 0・1 で再現 ✓
- 6×21 29石（K0811/K0815）→ 6×22 r=0: K0815 の 29石witness（行 5,4,5,5,5,5）を再現 ✓

## 実行記録（raw = output/*.jsonl）

| task | r 範囲 | leaves/off | 結果 |
|---|---|---|---|
| 6×30 q=5 ← 29base 23石 | 4..4 | 8,855 (=C(23,4)) | off=0: 0件・off=1: **2件**（subsets 10,903・candPass 2・verifyPass 2・uOverflow 8,854/8,855） |
| 6×23 q=6 ← 22base 29石 | 0..3 | 4,090 (=C(29,≤3)) | rem=3/add=3 に **8 distinct**（off 0・1） |
| 6×23 q=6 ← 22base 29石 | 4..5 | 142,506 (=C(29,≤5)) | 追加の distinct 0件（rem=3 の再出現のみ） |
| 6×31 q=5 ← 30base 23石 | 0..5 | 44,552 (=C(23,≤5)) | 0件（candPass 0・**uOverflow 44,483〜44,485/44,552 ≈ 99.8%** — 証拠力は限定的） |
| 6×24 q=6 ← 23base 29石 | 0..4 | 27,841 (=C(29,≤4)) | 0件（candPass 0・subsets 657,334/588,073・**uOverflow ≈ 99%** — 証拠力は限定的） |
| 6×29 q=5 ← 28base 22石 | 0..0 | 1 | 較正: K0815 witness 再現 |
| 6×22 q=6 ← 21base 29石 | 0..0 | 1 | 較正: K0815 witness 再現 |

6×30 witness 2件・6×23 witness 8件は（元runに加え）リファクタ済み
repo 版 extend6.js での再実行でも distinct 2件・8件をbit-exactに再現した
（6×23 は off 重複込み26 WITNESS行・distinct 8）。Python 独立検証器での
再検証も ALL-PASS（scripts/verify_rowcase.py）。

witness の正本: [w65_30.json](output/w65_30.json)（2件）・[w66_23.json](output/w66_23.json)（8件）。
base witness プール（再現用コピー）: [witness-pool/](witness-pool/)。

## 解釈と残課題

- (6,5) の witness 前線は **6×31**、(6,6) の前線は **6×24** に移動。
  ただし新witnessをbaseとする直接拡張近傍（上表の r≤5 / r≤4）は
  uOverflow スキップが支配的で、限定非不在の証拠力は弱い。
  次の一手は (i) maxA 制限を上げた列挙（コスト増）、(ii) SA/kissat による
  6×31・6×24 直接探索、(iii) dm=2（2石欠損）witness の発見ルート。
- M_{6,5}=30・M_{6,6}=23 の可能性は反証された（6×30・6×23 にwitness実在）。
  上界 658・495（K0318 代入）は不変。
