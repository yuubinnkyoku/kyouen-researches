# five-row-q6-m22-witness-20261115

COMPLETE — 高速レーン。**5×22 q=6 に行欠損極大witnessが存在する**ことを
class-split SAT（kissat 4.0.4・class {0}・k×minpos 分解サブインスタンス）で発見。
**(5,6) のwitness帯は m=15..21 → m=15..22 に拡大・M_{5,6} ∈ [23, 249]・前線は 5×23。**

## 結果

- **5×22 class {0} krow=0:4 minpos=0 が SAT**: kissat 4.0.4・**3,126,820 conflicts / 194.87s**。
  witness は **24石・rows (4,5,5,5,5)**（単一欠損行 row 0 が4石・左端石 column 0）。
  前回の m22 class-split sweep（five-row-q6-m22-class-split-20261114）で 250s INDET
  だった class {0}（3,556,467）・{0}krow0:4 INDET（2,019,686）は、k×minpos 分解で
  **p0 サブインスタンスが witness 手前で打ち切りだった**ことが確定。
- **二系統検証 PASS**: (a) sat3.js decode → sat.js census-free verifyConfig
  （safe + maximal）・(b) 独立な純TS再実装（ペア直線・トリプル円・正準整数係数）で
  safe（1,824 石曲線すべて最大5石・unsafe 0）+ maximal（86/86 空セル遮断）。
- **陽性対照 5×21 {0} SAT 330,743** が m22 class-split レーンの対照記録と bit-exact
  （24石 rows (4,5,5,5,5)・verifyConfig PASS）。
- **m=23 は INDET（不在主張ではない）**: class {0} k4p0 **3,343,593**・k4p1
  **3,369,340**・k4p2 **3,686,541**（ここまでで最難）・k3p0 **3,276,028**
  conflicts（いずれも kissat --time=220 の壁時計打ち切り・
  時間打ち切り値は同一軌跡でも bit-exact ではない）。
  **k4p0 は 700s の深いキャップでも UNKNOWN（9,630,182 conflicts・3.2倍深い
  探索でも決着せず）** — m=23 は m=22（witness は 3.1M conflicts で出現）より
  質的に難しい。残る k4p3..p11・k3p1..・k2/k1/k0・他クラスは未走査。
- **witness 近傍 surgery の完全列挙（負記録）**: m=22 witness を 5×23 に移植すると
  safe かつ未遮断セルは (22,0) のみ（T曲線32本・seed最大カウント 4,3,3）。
  1石surgery **1,416構成 → 0件**・2石surgery（heavy-T曲線健全フィルタで完全）
  **552,000構成 → 0件**。よって 5×23 の24石witness（存在すれば）は本seedから
  **2石移動（対称差 ≤4 セル）以内にはない**。m=23 不在の主張ではない。

## 復旧・再現性

- witness 発見後に実行環境の完全リセットが発生。確立済みプロトコルで復旧:
  scripts を main から復元（blob sha 6c3262d6 / edfae1d2 / 6dfa7db3 照合）・
  kissat 4.0.4 を公式 rel-4.0.4 asset から再取得（md5 3a5eba830aa6008a604fcc9bbe99a325）・
  CNF 再生成 → 4インスタンス決定的再実行。**2つの SAT 実行は bit-exact**
  （330,743 / 3,126,820・witness 石配置も発見時と同一）。INDET 2件は同一軌跡の
  壁時計打ち切り（再実行値を生ログとして公開）。
- スコープ: witness の有限機械検証（census・符号化・kissat 4.0.4 まで）。
  m ≥ 23 の不在・存在は open。5×23 前線の残るサブインスタンス
  （class {0} k4p2..・k3p0..・class {1}.. など）は未走査。
