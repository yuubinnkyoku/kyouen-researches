# six-row-q5-q6-frontier-20261120

IN FLIGHT (claim) — 高速レーン（単一オーナー宣言・2026-11-20 13:25Z）。
repo検索時点で (6,5)/(6,6) のSAT前線掃引は未着手・未宣言。

## Claim（本レーンが走査する範囲）

- **(6,5) 前線 6×20**: def-mode（sat2.js・行欠損極大安全配置の完全符号化 K0810）
  で SAT 探索。SAT なら witness 帯は m=8..20 に延伸し **M_{6,5} ∈ [21, 658]**。
  全 UNSAT なら 6×20 欠損極大不在が確定し **M_{6,5} = 20 または ≥ 22**。
  def INDET 時は rowY=0/1/2 行固定分割（V-鏡映 y↔5-y で3クラスが全6行を被覆・
  K0829 と同一の被覆論）で決着を図る。
- 時間が許す限り 6×21, 6×22, ... の前線延伸、および **(6,6) 前線 6×16**
  （symp 同様: M_{6,6} ∈ [16,495]・witness 帯 m=8..15）も同レーンで走査する。
- 着手時点の境界: **M_{6,5} ∈ [20, 658]**（下界 K0808 の貪欲 witness m=8..19・
  上界 K0318 代入 U=658）、**M_{6,6} ∈ [16, 495]**（K0808 m=8..15・U=495）。
  K0808 は (6,5) m=20・(6,6) m=16 を貪 greedy（≤1000 restart）で発見できず
  「存在是非は未解決」と明記しており、本レーンはこの有限決着を SAT で行う。
- INDET は cap 到達であり不在主張ではない。

## 手法・較正（実行後に記録を追記）

- 生成器: sat2.js（four-row-q5-m22-class-split-20261115/scripts・
  md5 282ae832efa0080127c6c153e65e1c3c・K0810 core sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c
  上で全三つ組census・逐次カウンタ・極大性）。decode は sat3.js（同 directory・
  md5 d03f908ea99ba819caee2a6fbb471c1b）のdecode。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。
- 検証: (1) sat.js verifyConfig（census不使用）・(2) verify_witness.py（純Python Fraction・
  md5 0530d166572987988a01ec40dee12d4c・ロジック独立）・(3) verify_independent.ts
  （純TS/BigInt・md5 b918dc50530a9b87b67d96a6ef4687cd）の3系統。SAT witness は3系統検証する。
- 較正: 陽性対照として K0808 出版 witness（6×19 q=5・23石・scan_results.json）を
  3系統で再検証し、(6,5) 6×19 def-mode kissat SAT（期待: SAT）を同じ toolchain で実行する。

## スコープ

有限機械検証（sat2.js def-mode 符号化の完全性 K0810・kissat 4.0.4 の正確性）まで。
各幅の def-mode UNSAT はその幅の欠損極大非存在の完全証明。SAT は witness 有限存在証明。
上界（K0318 代入）は不変。6×m の真の安定化長の全帯閉包は主張しない。
