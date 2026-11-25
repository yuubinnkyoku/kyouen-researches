# 2026-11-14 高速レーン第9回: (7,8) 7×25 row クラス完走（負）+ (7,9)/(7,10) 帯 101 以降延長開始

## 開始時の確認

- 最新 main: b80c2bbc → 並走は class2-lane merged recompute（69e v2 baseline 1023 + 70c/60b-warm/71b 23 receipts → 73f8b5d8）、
  eight-row-bands レーン（(8,9) witness 8×28 SAT / (8,10) 8×26 4符号化 INDET、w8q9/w8q10 records push 済み）、
  K0825 (7,8) witnesses 7×8..7×24 完了直後。本レーンは (8,9)/(8,10)（並走所有）と n11 class2 を回避し、
  K0825 の明示的残作業（7×25 残り3鏡映クラス）と K0820 レジュームの帯延長（m=101..200）を選定。

## 成果1: 7×25 q=8 row クラス {0,1,2} — 全 INDET（正直な負記録）

- 較正: (7,24,8) rowY=3 再生成 kissat SAT 641,005 conflicts = K0825 record と bit-exact（instance identity 確認）。
- rowY ∈ {0,1,2}: 3,440,713 / 3,541,875 / 3,577,791 conflicts、240s cap 全 INDET。
  rowY=3（K0825, 3,534,747）と合わせ**全4鏡映クラスが短予算で未決着**・クラス間でほぼ一様な抵抗。
  不在の主張ではない。→ `research/experiments/seven-row-q8-m25-rowclasses-20261114/`

## 成果2: (7,9)/(7,10) witness-free 帯の m=101 延長（進行中）

- 較正: (7,100,10) 再生成 UNSAT 2,388 conflicts = q10-band record と bit-exact。
- (7,9): m=101..118 全 UNSAT（11.5k..27.5k conflicts）。(7,10): m=101..110 全 UNSAT（1.5k..3.7k）。
- バッチごとに本ログと records を更新して継続。目標: m=200 まで（予算が許す限り）。
- 帰結（本コミット時点）: M_{7,9} ∈ {24} ∪ [119,613] / M_{7,10} ∈ {19} ∪ [111,587]。

## 構造観察（記録用・未昇格）

q=10 の ≥10点円は 7×m でちょうど 2m−14 本・すべて行 {0,3,6} を通る・m=30 では全円がちょうど10点
（rowcov.js による census 計測・m=30/60/100）。カバレッジ反証は不成立（行1,2,4,5の被覆も m 近くまで埋まる）。
带延長と合わせて q点円の分類が tail bound 手掛かりになる可能性。要追加調査。

## 運用

- batchband.sh の wall guard（~235s）でコンテナ hard stop 回避・GUARD_STOP/PROJ_STOP 後も records は幅単位で永続。
- push_files 前に最新 main を再取得して CSV/K項目の並走更新を確認する。

## 成果2 続き（第2バッチ・genfast2 切替）: (7,9) m=119..184 全 UNSAT

- **genfast2.js**: genfast.js の (v,ρ) 正規化（文字列Map + 二重gcd）をgcdなし正準整数キー
  (N480,RHO)=(480v, 921600ρ²)・typed-array open addressing に置換した高速版。
  4サンプル（7×25 q8 --rowY=2 / 7×101 q9 / 7×110 q10 --lex / 8×26 q9）で **CNF バイト一致検証**
  （`scripts/controls_byteid.json`）。~10.7x 高速（m=101: 21.4s → 2.0s）。
  初回実装は D=8(ya−yb)<0 の負号を抜いていたが 7×25 q8 サンプルの曲線数 121 vs 656 で捕捉・修正。
- (7,9): m=119..184 **全幅 UNSAT**（6.9k..26.8k conflicts・全幅 200s cap 内完走・INDET なし）。
  m=159/160 は 7.1k/6.9k と極端に軽い幅もあるが、m の非単調性は通常観察。
- (7,10) m=101..108 は並走コミット 699a0110 と重複（双方 UNSAT・無害）。q10 は並走に譲り本レーンは q9 に集中。
- 帰結: **M_{7,9} ∈ {24} ∪ [185,613]**（q9-band records 101..184）。目標 m=200 まで継続。

## 成果2 完了: (7,9) m=185..200 全 UNSAT — 帯 24..200 確定

- (7,9): m=185..200 **全幅 UNSAT**（19.8k..29.8k conflicts・200s cap 内完走）。q9-band records 101..200（100幅）。
- **帰結: M_{7,9} ∈ {24} ∪ [201,613]**。101..200 帯は本実験の目標幅に到達。以降の延長は後続レーン。
