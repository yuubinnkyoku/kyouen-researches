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

## 追記 (2026-11-15 17:25Z: 掃引開始直後の状況と道具の整備)

- **陽性対照 bit-exact 再現**: ctrl_4x20_c0k3p1 = SAT 39.3s / 375,415
  conflicts (4×21 lane の 20.0s / 375,415 と conflicts が完全一致 —
  同一 CNF・同一軌跡の cross-lane 較正として機能。秒数差は CPU 配分差)。
- **c0k3p0 = INDET** (cap 600s / 3,852,260 conflicts)。m21 では直接
  決着したバケット群だが m22 では x2 分割が必要になる可能性が高い
  (m21 の最難 x2 サブバケット 1,969,663 conflicts の約2倍を費やして
  未決着)。
- **CPU 割り当ての判明**: 本 sandbox の cgroup は `cpu.max 100000 100000`
  = **実効 1.0 CPU** (nproc=2 は表示上)。driver の cap 600s は壁時計
  なので、並走プロセス (n10 ge20_cuts) との共存中は実効 cap が目減り
  する。ge20 側を renice +5 して本掃引に ~75% を優先配分した。
  INDET 判定は cap 到達打ち切りであり bit-exact でない旨は m21 lane
  と同様に記録する。
- **sat4.js の --x2 上限を k-aware 化**: 従来の無条件 `B ≤ m−2` は
  k=2 バケットで正当な B=m−1 (=21) ケースを落としていた不完全な
  上限だった。`--krow=y:2` のとき `B ≤ m−1`、k≥3 のとき従来通り
  `m−2`。k≥3 に対する既存インスタンスは一切不変 (4×21 lane の
  37 サブバケットの md5 に影響なし)。k=2 分割の完全性に必要。
- **汎用分割 driver 追加**: `sweepp0x2gen.sh` (c{0,1}k{2,3}p{p} 任意
  バケット対応・CAP 環境変数・resumable・comma-anchored key 照合・
  SAT 時の js+py 二系統 witness 検証)。INDET バケットが出次第
  `bash sweepp0x2gen.sh <bucket>` で追分解する。


## 追記 (2026-11-15 17:55Z: k3 直接試行の連続 INDET と driver 並べ替え)

- **c0k3p0/p1/p2 が全て 600s INDET** (3,852,260 / 6,854,166 / 6,939,580 conflicts)。
  m21 では p2 以降は 76〜400s で直接決着していた一方、m22 は p2 も抵抗
  → **m22 の k3 バケットは広く 600s cap を超える** (m21 比 ~1.5〜2倍で
  一貫した難化。multi c01 は 451s/5,022,943 conflicts UNSAT・m21 310.8s/
  3,957,766 と同じ比率)。
- このまま残り19個の k3 直接試行に各 600s を焼くのは非効率なため、
  driver を **sweep22fast.sh** (multi → k2 → k1 → k0 を先に、k3 直接試行
  を最後) に並べ替えた。既知 INDET の c0k3p0/p1/p2 は sweepp0x2gen.sh
  (x2 分割・cap 900s) で追分解する。multi の INDET が出たら krow ピン
  (欠損行の正確な石数 0..3 で分割・sweep35 規約) で追分解する。
- cap 600s 到達の INDET の conflicts は壁時計打ち切り (同一 CNF の
  再実行は同一軌跡を辿るが、打ち切り点は bit-exact ではない)。
