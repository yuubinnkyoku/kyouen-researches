# eight-row-q10-band-closure-20261115

IN FLIGHT (claim)。(8,10) の現在の境界は **M_{8,10} ∈ [26, 940]**
（下界: `eight-row-bands-20261114` witness 帯 m=10..25 全 SAT・
71石単一欠損・m=25 は 1,221,994 conflicts; 上界: K0318 substitution
U_{8,10}=940・`seven-row-inband-families-20261114/output/w7_upper_bounds.json`
w=8 行）。本実験は残る幅 **m=26..939** を def-mode UNSAT 掃引で閉包し、
**M_{8,10} の完全決着**（全幅 UNSAT なら M=26・w=8 で初の完全決着、
M_{7,9}=24・M_{7,10}=19 に次ぐ w≥6 で3例目）または帯内 SAT witness の
発見（その場合は下界更新と witness dual-verify）を目指す。

前提となる難度プロファイル（`output/controls/difficulty-probe.json`）:
難所は **m ∈ [26,59] に集中**（m=26 は 230s/5.48M conflicts で4符号化すべて
INDET・m=27..30/40/50 は 60s cap で 1.69M..1.78M conflicts INDET）。
**m ≥ 60 はすべて cap 内で UNSAT**（m=60: 54s/1.53M → m=939: 42s/116k。
m=939 の直接 UNSAT と U=940 で上限側は既に閉じている）。難所帯を先に掃引し、
易幅帯（m ≥ 60）を batch runner で順次埋める。

## 手法

- 生成器: `genfast3.js`（chord-pair abstract-circle census・q ≥ w+2 限定。
  `seven-row-q9-band-extension-201-612-20261114/scripts/genfast3.js`
  md5 `12c2bd9cb3b24887fc3896f7ea9bcadf` を再利用。w=8, q=10 は
  10 ≥ 10 で要件を満たす）。
- ソルバ: kissat 4.0.4 official prebuilt・def 単一節符号化
  （「ある行が q-1 石以下の欠損極大安全配置が存在」の完全符号化・
  K0820 と同一）・幅ごとに cap を調整。
- スクリプト: `scripts/leanband8.sh`（1 幅: genfast3 生成 + kissat +
  JSONL record + SAT 時 decode/dual-verify・cap は第5引数）・
  `scripts/batchband8.sh`（wall-clock guard 付き連続実行）。
  genfast3.js / decode_verify.js / sat.js / sat2.js は隣接 experiment から
  再利用（commit しない・md5 上記）。

## 較正（`output/controls/calibration.json`）

- **CNF byte-identity vs genfast.js（w=8 版）**: (8,26,10) def /
  (8,40,10) def / (8,60,10) def の 3 サンプルすべて **MATCH**
  （511,123 / 1,065,862 / 1,869,915 bytes）。
- **instance-identity**: (8,25,10) def 再実行 SAT **1,221,994 conflicts
  bit-exact**（`eight-row-bands-20261114` w8q10 records.jsonl・4c8c441c と一致）。
- **陰性対照**: (7,10) m=200 def **UNSAT 2,941 conflicts bit-exact**
  （vars 36,315 / clauses 132,264 / curves 393・
  `seven-row-q10-band-closure-201-586-20261115` の instance-identity
  control と同一）。

## スコープ

有限機械検証（genfast3 census 完全性: q ≥ w+2 で全 q 点円は二重行 2 つから
u 非依存に決まる弦対列挙・CNF byte-identity で確認、とソルバ正確性）まで。
m=26..939 の各幅の UNSAT はその幅の「ある行が q-1 石以下の極大安全配置」
非存在の完全証明。INDET は honest negative として記録し non-absence とは
読まない。全幅 UNSAT の場合、witness 帯 {10..25}
（`eight-row-bands-20261114`）・witness-free 26..939（本実験）・
m ≥ 940 の持続性（K0318 substitution U=940・proved）と合わせ
**M_{8,10} = 26 が exact に決着**する。

## 現在の結果 (2026-11-15 01:20Z 更新)

### 帯掃引 (def-mode 直接・kissat 4.0.4)

- **43..59 全幅 UNSAT** (cap 250/110/90 秒: 43-45 は 250s cap・
  4.21M-5.00M conflicts・46-50 は 104-147s・51-59 は 55-82s・60 は 54s)。
  m=46-50 は env reset 後の再実行で bit-exact 再現 (決定性確認)。
- **難所帯 honest negatives (def-mode)**: m=27/28 (270s・3.45M/3.61M),
  m=29 (250s・6.01M), m=31 (240s・5.87M), m=41 (250s・6.44M),
  m=42 (250s・6.31M)。いずれも INDET であり non-absence ではない。
- **サンプル UNSAT**: 60, 80, 100, 150, 200, 300, 500, 700, 939
  (m=939 42s/116,323 conflicts; 上限側は U_{8,10}=940 で閉じている)。

### class-split 突破 — m=40, 41, 42 完全決着 (UNSAT)

def-mode OR 実例が抵抗した幅を **sat3.js class-split** (row-mirror 正準欠損行
クラス分割・six-row-q8-m19-class-split-20261114/scripts/sat3.js md5
d03f908e 再利用 + classfast.js = genfast3 に S.buildCensus を patch する
wrapper・byte-identity 確認済み) で分解すると全部解けた:

- **各幅 135/135 クラス UNSAT・0 INDET・0 SAT** → def-mode UNSAT 確定。
- m=41: 難クラス {3} 1,798,460 conflicts (def-mode 250s INDET 6.44M
  superseded)。詳細 output/q10-band/class-splits/classes-8x41q10.jsonl。
- m=42: 難クラス {3} 1.79M / {3,4} 1.76M。
- m=40: 難クラス {3} 2.22M / {3,4} 1.70M。
- runner: scripts/classsweep.sh (resume-safe・per-class log + JSONL)。

これで **witness-free 連続帯は 40..138** (61..138 は並走
eight-row-q10-band-closure-26-939-20261115 が掃引済み・53..60 は
クロスレーン conflicts bit-exact 検証済み)。残る難所は **26..39**
(26: 4符号化 INDET・27-31: プローブ INDET・30, 32..39: 未掃引または
def INDET → class-split 予定)。

### 進行中 (IN FLIGHT)

- m=32..39 を classsweep.sh で掃引中 (cap 100-280s)。
- 並走レーンが 139..500 (laneA) / 514..938 (laneB) を掃引中。
- 全幅閉包後: M_{8,10} = 26 exact 決着として K item + CSV exact-threshold 行化予定。
