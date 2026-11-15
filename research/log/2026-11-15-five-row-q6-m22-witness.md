# 2026-11-15 five-row q=6 m=22 witness 発見（高速レーン・環境リセット復旧込み・M_{5,6} ∈ [23,249]）

## 概要

(5,6) 前線の 5×22 を解決。**class {0} krow=0:4 minpos=0 が SAT**
（kissat 4.0.4・3,126,820 conflicts / 194.87s）で **24石欠損極大witness
を発見**（rows (4,5,5,5,5)・単一欠損行 row 0 が4石）。
**(5,6) witness帯 m=15..21 → m=15..22・M_{5,6} ∈ [23, 249]・前線 5×23。** K0852。
発見後に実行環境完全リセット → 確立済み復旧プロトコルで raw ログを
決定的再実行により再構築し公開（SAT 2件 bit-exact・INDET 2件同一軌跡）。

## 実施

- 着手前の最新 main 確認: (4,4) m=35・(4,5) m=21 は four-row レーンの
  IN FLIGHT claim 中（譲り）。**five-row-q6-m22-class-split-20261114 の
  report がレジュームで「K0821 方式の k×minpos 完全分解」を明示推奨**しており、
  同レーンの新規 IN FLIGHT claim（e2750cb3・未掃引11クラスの250s sweep）は
  class {0} を含まないため対象が独立 → 5×22 class {0} k×minpos 分解に着手。
- 5×22 class {0} k=4 minpos=0 が **SAT 3,126,820 / 202.43s**（当環境では
  195s前後）。witness 24石 rows (4,5,5,5,5)。前回 sweep の {0} 250s INDET
  3,556,467・{0}krow0:4 INDET 2,019,686 は witness 手前の打ち切りと確定。
- **二系統検証 PASS**: (a) sat3.js decode → sat.js verifyConfig、
  (b) 独立純TS再実装（ペア直線・トリプル円・整数係数）safe
  （1,824石曲線・最大5石・unsafe 0）+ maximal（86/86 遮断）。
  **陽性対照 5×21 {0} SAT 330,743** は前回 m22 sweep レーンの記録と bit-exact。
- **m=23 プローブ（honest negative）**: {0} k4p0 **INDET 3,343,593**・
  k4p1 **INDET 3,369,340**（220s 壁時計・時間打ち切り値は bit-exactでない）。
- **witness surgery（完全列挙・負記録）**: 5×23 移植で未遮断は (22,0) のみ
  （T曲線32本・seedカウント 4,3,3,…）。1石surgery 1,416構成 0件・
  2石surgery（heavy-T健全フィルタ・552,000構成）0件 → 5×23 witness は
  本seedから2石移動以上離れている（不在主張ではない）。
- **環境リセット復旧**: ローカル全喪失後、(1) scripts を main から復元
  （blob sha 6c3262d6 / edfae1d2 / 6dfa7db3 照合）、(2) kissat 4.0.4 を
  公式 rel-4.0.4 asset から再取得（バイナリ md5 3a5eba830aa6008a604fcc9bbe99a325）、
  (3) 4 CNF 再生成+決定的再実行。**対照 330,743・witness 3,126,820 は
  bit-exact（石配置も発見時と同一）**・INDET 2件は同一軌跡の壁時計打ち切り
  （再実行値 3,343,593 / 3,369,340 を生ログとして公開）。
- 実験dir一式（README COMPLETE・report・records 4件・summary・scripts 5本・
  raw 6件）+ K0852 item + 本 log + CSV (5,6) 行更新 + fwreadme 2箇所 +
  workflow トリガー行を push。

## 境界の更新

- (5,6): 22..249 → **23..249**（下界 23・上界 249〔K0318 代入〕不変）。
  witness帯 5×15..5×22（15..21 は従来〔K0723・K0810・K0811・K0815〕+5×22 本項）。
- 前線は **5×23**（class {0} k4p0/k4p1 のみ INDET・他サブインスタンス未走査）。

## 備考・レジューム

- **5×23 の未走査サブインスタンス**: class {0} k4p2..p10（minpos 健全上限は
  floor((23−1)/2)=11）・k3p0..・k2/k1/k0・class {1} k×minpos・他クラスの
  krow 分解。m=22 witness が k4p0 にあったことから、m=23 も同型
  （単一欠損行・k=4・左端寄り minpos）に出る可能性が相対的に高い。
- **surgery 拡張案**: 3石surgery（remove 3/add 3）は本seed近傍では
  構成数が爆発するため、seedからではなく m=23 用の新規分解（k×minpos）
  を直接走らせる方が情報価値が高い。
- m22 class-split レーンの IN FLIGHT claim（未掃引11クラス 250s sweep・
  e2750cb3）とは対象独立。同レーンの sweep が別クラスで witness を
  発見した場合も本項（class {0} witness・帯拡大）とは独立な証拠追加。
- **INDET 値の再現性の扱い**: 時間打ち切り INDET の conflicts は
  bit-exact でない旨を records/summary に明記した（生ログは再実行値）。
  SAT 実行のみ bit-exact 主張可。
- **K項目を push したら必ず workflow トリガー行も push**（今回は
  refresh-knowledge-generated.yml に K0852 行を追加）。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class2・class4は
  いずれもUNKNOWN**。
