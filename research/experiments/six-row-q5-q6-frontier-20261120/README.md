# six-row-q5-q6-frontier-20261120

IN FLIGHT (claim) → 成果出版（2026-11-20）— 高速レーン（単一オーナー宣言・2026-11-20 13:25Z・commit 796cbb46）。
repo検索時点で (6,5)/(6,6) のSAT前線掃引は未着手・未宣言であった。

## 結果（2026-11-20 出版）

生成 sat2.js（md5 282ae832efa0080127c6c153e65e1c3c・K0810 完全符号化）・
ソルバ kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）・
SAT witness は全て decode 後 **3系統検証**（sat.js verifyConfig〔census不使用〕・verify_witness.py
〔純Python Fraction・md5 0530d166…〕・verify_independent.ts〔純TS/BigInt・md5 b918dc50…〕）済み。
全レコードは `output/records.jsonl`（tag・witness石配置・3系統検証出力・CNF md5・conflicts・cap込み）。

### (6,5) q=5 — witness帯 m=8..28（下界 K0808 帯 m=8..19 を SAT で延伸）

- def-mode（行欠損極大安全配置の完全符号化）: m=19..27 全幅 SAT。
  conflicts 261 / 750 / 985 / 657 / 15,541 / 17,610 / 19,169 / 20,212 / 89,830
  （非単調・0.2s〜38.9s）。**M_{6,5} ≥ 28**。
- m=28: def-mode 240s INDET（894,706 conflicts）→ rowY=0 行固定分割 SAT
  （464,040 conflicts・146.1s・23石 rows [3,4,4,4,4,4,4]）。**M_{6,5} ≥ 29**。
- m=29（現前線）: rowY=0 220s INDET（720,202）・rowY=1/2 --sat 130s INDET
  （502,044 / 469,125）。いずれも cap 到達の正直な未解決記録で**不在主張ではない**。
- **K0808 の未解決ケース (6,5) 6×20 を解決**: greedy（≤1000 restart）は発見できなかったが
  def-mode SAT は 750 conflicts・0.6s で 23石単一欠損 witness を発見。
- **副次的**: 6×19 の def-mode SAT witness は **22石**（rows [4,4,4,2,4,4]・行3が2石の深欠損）。
  K0808 の greedy min 23 を改善し、m=19 の行欠損極大最小石数は **≤ 22** と確定
  （最小性の主張ではない）。

### (6,6) q=6 — witness帯 m=8..24・着手時下界16→25

- def-mode: m=16..24 全幅 SAT。conflicts 46 / 451 / 312 / 590 / 14,808 / 10,066 /
  277,198 / 919,243 / 889,446（0.1s〜134.2s）。**M_{6,6} ≥ 25**。
- **K0808 の未解決ケース (6,6) 6×16 を解決**: greedy は発見できず「存在是非は未解決」
  だった幅が **46 conflicts・0.1s** で SAT（29石 rows [5,4,5,5,5,5]）。K0808 の
  greedy 非発見が不在を意味しない、ということの最も鮮明な実例。
- 副次的: 6×20 の witness は **28石**（rows [5,3,5,5,5,5]・行1が3石の深欠損）。
  m=20 の行欠損極大最小石数は **≤ 28**（最小性の主張ではない）。
- m=25（現前線）: def 140s INDET（857,314）・rowY=0 140s INDET（860,873）・
  rowY=0 --lex=H 140s INDET（838,046）・rowY=0/1/2 --sat 130s INDET
  （1,014,217 / 951,654 / 929,165）。いずれも不在主張ではない。

### 帰結

- **M_{6,5} ∈ [29, 658]**（着手時 [20, 658]・上界は K0318 代入 U=658 のまま）。
- **M_{6,6} ∈ [25, 495]**（着手時 [16, 495]・上界 U=495 のまま）。
- 有限witness下界の更新であり、安定化長の全帯閉包の主張ではない。
  m=29 (q=5)・m=25 (q=6) の INDET は記録された cap 内未解決である。

## 較正

- 陽性対照: K0808 出版 witness（6×19 q=5・23石・6×15 q=6・29石・
  six-row-deficient-witnesses-20261113/output/scan_results.json）を3系統で再検証し
  全 PASS。def-mode 6×19 q=5 は 261 conflicts 0.2s で SAT（K0808 witness帯の内挿確認）。
- 実行環境リセット2回を跨いだ再実行で、m=20..27 def-mode の conflicts が
  byte-exact 再現（750 / 985 / 657 / 15,541 / 17,610 / 19,169 / 20,212 / 89,830・
  適用時点での同一バイナリ/同一スクリプト md5）。

## Claim（本レーンが走査する範囲 — 着手時の宣言）

- **(6,5) 前線 6×20**: def-mode（sat2.js・行欠損極大安全配置の完全符号化 K0810）
  で SAT 探索。SAT なら witness 帯は m=8..20 に延伸し **M_{6,5} ∈ [21, 658]**。
  全 UNSAT なら 6×20 欠損極大不在が確定し **M_{6,5} = 20 または ≥ 22**。
  def INDET 時は rowY=0/1/2 行固定分割（V-鏡映 y↔5-y で3クラスが全6行を被覆・
  K0829 と同一の被覆論）で決着を図る。
- 時間が許す限り 6×21, 6×22, ... の前線延伸、および **(6,6) 前線 6×16**
  （同様: M_{6,6} ∈ [16,495]）も同レーンで走査する。
- 着手時点の境界: **M_{6,5} ∈ [20, 658]**（下界 K0808 の貪欲 witness m=8..19・
  上界 K0318 代入 U=658）、**M_{6,6} ∈ [16, 495]**（K0808 m=8..15・U=495）。
- INDET は cap 到達であり不在主張ではない。

## 手法

- 生成器: sat2.js（four-row-q5-m22-class-split-20261115/scripts・
  md5 282ae832efa0080127c6c153e65e1c3c・K0810 core sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c
  上で全三つ組census・逐次カウンタ・極大性）。decode は sat3.js（同 directory・
  md5 d03f908ea99ba819caee2a6fbb471c1b）。
- rowY=0/1/2 行固定分割（`--rowY=Y`）は V-鏡映 y↔5-y で全6行を被覆し、
  (7,5)/(7,6) 前線解決（seven-row-q5-q6-frontier-row-split-20261115）と
  同一の被覆論。--lex=H・kissat --sat は探索支援の構成変更で、
  SAT witness の正当性は3系統検証のみに依存する。
- runner: scripts/run65.sh（1 instance 生成→kissat cap 実行→records.jsonl 追記→
  SAT時 decode＋3系統検証・INDET時 CNF 削除）。records の各レコードは
  生成 meta（vars/clauses/curves）・CNF md5・conflicts・cap・sec・
  witness石配置・3系統検証の生出力を含む。

## スコープ

有限機械検証（sat2.js def-mode 符号化の完全性 K0810・kissat 4.0.4 の正確性）まで。
各幅の def-mode UNSAT はその幅の欠損極大非存在の完全証明。SAT は witness 有限存在証明。
上界（K0318 代入）は不変。6×m の真の安定化長の全帯閉包は主張しない。
標準11×11空盤には一切言及しない。
