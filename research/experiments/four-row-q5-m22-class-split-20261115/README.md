# (4,22,5) class-split 掃引 — absence-capable 完全被覆 (2026-11-15 高速レーン・IN FLIGHT)

## 位置づけ

`M_{4,5} = 21 または ≥ 23` (K0857・4×21 witness-free 確定済み・上界
U_{4,5}=140 (K0318)・witness 帯 m=5..20 (K0833))。**前線は 4×22**。
本掃引は (4,22,5) を absence-capable に完全分解して決着を目指す。
完了して全 UNSAT なら witness-free 幅集合は {21,22}・鋭い形は
**M_{4,5} = 21 または ≥ 24**。SAT が出たら M ∈ [22,140] に戻り
witness を復号・検証する。

## 被覆の完全性 (4×21 lane と同一構造・幅だけ違い)

- 欠損クラス = 石数 ≤ q−2 = 3 の行の集合。safe な行は ≤ 4 石なので、
  欠損行の補集合は exactly 4 石 (sat3.js --class は D 外の行を rowGe 単位で
  FULL 固定するため、この制約を課しても被覆は完全)。
- 行ミラー V (行 0↔3, 1↔2) で類別すると正準クラスは 9 個。
- 単一クラス {0},{1} は正確な石数 k∈{0,1,2,3} と minpos p∈0..10 で分解
  (sound H-split: min(x1, 21−x_k) ≤ floor(21/2) = 10。H は行を保存する
  のでクラス内で健全)。minpos と lex の併用は unsound なため全インスタンス
  lex なし (four-row-q4-m35-class-split-20261115 規約)。
- multi クラスは直接。INDET が出たら krow ピン、それでも抵抗する
  {0}k3p0/p1 バケットは **第2石 x2 分割** (sweepp0x2.sh 方式・
  4×21 ではこれで 37バケット全 UNSAT・1枚 ≤185s に決着) で追分解する。
- 計: 陽性対照 1 + k3 22 + multi 7 + k2 22 + k1 22 + k0 2 = 76 インスタンス。
  cap 600s・resumable (records.jsonl key skip・CNF 生成は決定的・
  comma-anchored key 照合)。

## 陽性対照

(4,20,5) class {0} --krow=0:3 --minpos=1: m=20 witness (rows [4,4,4,3]) の
V 像を含み、4×21 lane では SAT 20.0s / 375,415 conflicts で V 像を再発見
(js+py 検証)。本 lane でも同一対照を最初に実行する
(cross-lane bit-exact 再現が較正になる)。

## 運用

- 2コア制約: ge20_cuts (n10 lane) と排他・kissat は常時1プロセスのみ。
- IN FLIGHT claim: output/inflight-claim-20261115.json。
- driver: sweep22.sh (sweep21.sh の m=21→22 版・minpos 0..10 不変)。
- records.jsonl は driver 実行中 append のみ (m21 lane の修復事故の教訓)。

## 結果

IN FLIGHT — 実行中 (2026-11-15 17:12Z 起動)。決着後に本 README を更新し
K 項目へ昇格する。
