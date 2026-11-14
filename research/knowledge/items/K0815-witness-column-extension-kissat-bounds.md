---
id: K0815
title: 列追加拡張と外部SATソルバによる下界更新 — M_{6,5}≥30・M_{6,6}≥23・6×12 q=8最小極大≤37
kind: proposition
status: proved
topics: [rectangles, variants]
aliases: []
relations:
- type: generalizes
  target: K0811
  note: SA抵抗帯6×29/6×22に欠損極大witnessが実在することを拡張列挙で示し下界を更新。M_{6,5}=29可能性（6×29 UNSAT）は反証
- type: depends_on
  target: K0810
  note: encode()/toDimacs 符号化をverbatim使用しDIMACSをkissat 4.0.4に投入。6×12 q=8 cap=38/37（自作CDCLのtimeout×2帯）がSAT
- type: depends_on
  target: K0796
  note: 2×8 q=4 5石witnessの制御再現
- type: depends_on
  target: K0806
  note: 上界（K0318代入）は不変
artifacts:
- path: research/experiments/witness-extension-kissat-20261114/scripts/extend.js
  role: source
  note: 列追加拡張の決定的完全列挙（既知witnessの平行移動+新規列部分集合・verifyConfigで検証）
- path: research/experiments/witness-extension-kissat-20261114/scripts/verify_py.py
  role: source
  note: 別実装Python独立検証器（Fraction厳密演算・石ペア直線/石3点組円全列挙）— 初版の÷2バグをJS検証器との矛盾で捕捉し修正
- path: research/experiments/witness-extension-kissat-20261114/scripts/dump.js
  role: source
  note: K0810符号化からDIMACSを吐出
- path: research/experiments/witness-extension-kissat-20261114/output/extended.json
  role: data
  note: 拡張witness 4件（6×29 q=5 23石・6×22 q=6 29石・6×19/6×21 q=6 29石）の座標と2系統検証結果
- path: research/experiments/witness-extension-kissat-20261114/output/w37.json
  role: data
  note: 6×12 q=8 37石witness（行構成 7,7,7,2,7,7）・2系統検証PASS
- path: research/experiments/witness-extension-kissat-20261114/output/kissat_runs.json
  role: data
  note: kissat実行記録（制御・timeout記録込み）
- path: research/experiments/witness-extension-kissat-20261114/report.md
  role: proof
  note: 手法・拡張列挙の完全性根拠・制御・未解決の記録
solution:
  board: 6×m（q=5,6）・6×12（q=8）
  level: weak
  outcome: conditional
  classification: [root]
  coverage: (6,5) 6×29・(6,6) 6×22 の各盤の欠損極大witness・6×12 q=8 の37石極大安全配置
  conditions: q点共円・共線禁止・標準整数格子
  verification: [independent-enumeration]
  certificate: witness座標（全witnessがJS census不使用独立検証器とPython別実装検証器の2系統で safe+maximal PASS）
  independent_check: 別言語・別アルゴリズム（石ペア直線・石3点組円の全列挙・Fraction厳密演算）による直接判定の一致
  note: 下界更新のみ。6×30 (q=5)・6×23 (q=6)・6×12 q=8 cap=36 は未決着であり不在証明ではない
---

# 列追加拡張とkissatによる下界更新（2026-11-14）

2つの手法で固定幅のopen境界を更新した。すべてのwitnessは2系統の独立検証器
（JS census不使用・Python別実装）で safe+maximal PASS。

- **M_{6,5} ≥ 30**: 23石の欠損極大安全配置が 6×29 に存在（行構成 4,4,4,4,3,4）。
  K0811 が最優先レジュームとした「6×29 UNSAT ⟹ M_{6,5}=29」は反証。
  SA 8 run が非発見だった盤であり、非発見は不在を意味しない教訓の最も直接的な再実証。
- **M_{6,6} ≥ 23**: 29石の欠損極大が 6×22 に存在（行構成 5,4,5,5,5,5）。SA 7 run 非発見帯。
- **6×12 q=8 の最小極大サイズ ≤ 37**: 37石極大安全配置（行構成 7,7,7,2,7,7）。
  K0810 の cap=38 は自作CDCLで2回timeoutだったが、kissat 4.0.4 では cap=38 が0 conflict で SAT、
  cap=37 が994,597 conflicts・38秒で SAT。cap=36 は255秒・4.92M conflicts で未決着。

## 列追加拡張（決定的完全列挙）

曲線は座標のみで決まるため、w×m 上の極大安全配置 S は w×m'（m'>m）上でも
安全かつ旧セルに対して極大のまま平行移動で置ける。拡張の可否は「新規列（k=m'−m列）
の各空セルが ≥q−1 石の曲線でブロックされるか石で埋まるか」のみに帰着し、
新規列セルの部分集合（|S|+追加 ≤ w(q−1)−1）の全列挙で完全に判定できる。
22石@6×28（K0811）→ 6×29 23石、29石@6×21（q=6）→ 6×22 29石 がこの列挙で発見された。
拡張の反復（新witnessをプールに追加）で新たな m は得られず、6×29→6×30 は
余剰0の空列ブロック・除去r≤3+新規列追加の列挙空間では未発見（非不在）。

## 外部SATソルバ

K0810 の encode()/toDimacs をそのまま使い DIMACS を kissat 4.0.4（公式linux-amd64
リリースバイナリ）に投入。制御: 2×9 q=4 UNSAT（M_{2,4}=9）・2×8 q=4 SAT（K0796 5石再現）。
拡張符号化（全体石数計数器 ≤ w(q−1)−1 + 欠損行は上半分とする行対称性条項・水平反転で健全）
は 6×28 cap=23 で 23石witness（行4,3,4,4,4,4）を出し整合。
6×29 q=5（素・拡張とも270秒未決着）は拡張列挙で決着、6×30 q=5・6×23 q=6 は未決着。

## 検証プロトコルの教訓

Python独立検証器の初版は円の3点組Cramer解の定数項に誤った÷2を含み、
JS検証器と矛盾する判定（6×29 witness を非極大と誤判定）を出した。2系統独立検証が
実際にバグを捕捉した事例（K0808・K0810 に続き3例目）。修正後、拡張witness 4件・
既知witness制御3件（2×8 q=4・6×22 q=5・6×28 q=5）すべて一致。

現在の境界: M_{6,5} ∈ [30,658]・M_{6,6} ∈ [23,495]・M_{6,8} ∈ [18,371]・
M_{5,6} ∈ [19,249]・M_{5,7} ∈ [19,158]・M_{6,7} ∈ [20,402]（上界は不変）。
