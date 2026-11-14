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

## 現在の結果 (2026-11-14 claim 時点)

- `output/q10-band/records.jsonl`: 幅 60, 80, 100, 150, 200, 300, 500,
  700, 939 の 9 幅 UNSAT（difficulty probe と同一パイプライン・
  `raw-logs/` に per-width kissat log + meta）。
- 残り: m=26..59（難所帯）・60..939 の未掃引幅。

（難所帯 m=26..59 の掃引結果・帯内 SAT の有無は追記される）
