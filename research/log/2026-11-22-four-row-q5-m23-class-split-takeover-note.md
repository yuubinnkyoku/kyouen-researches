# 単一オーナー宣言（takeover）: (4,23,5) class-split 掃引 lane の引き継ぎ — 残りバケットの完走と (4,23,5) の決着（2026-11-22）

- 宣言時刻: 2026-11-22T10:28:25Z（直前の最新 main HEAD: af44ea8ab0c7442f886c624783b3f3599089898a・push 直前に再取得して記録する）。
- オーナー: 高速レーン（本セッション）・単一オーナー。同名の毎時タスクが並走する可能性があるため、本宣言以降は下記スコープへの同内容の並行着手を避けること。

## 引き継ぎの経緯

先行宣言 `research/log/2026-11-21-four-row-q5-m23-frontier-single-owner-note.md`（commit d6b478ba・2026-11-21T19:23Z・
K1197 が明示的に次前線として指名した 4×23）のスコープを、records part1（commit 03ae14d5・19:49Z・
k2 24 + k1 24 + k0 2 = 50 UNSAT pieces + c01 multi 220s INDET・51 行）まで出版した後、
実行環境失効で中断した（kit 側ミラーの mtime 2026-11-21T20:27Z・main には以後の追記なし）。
中断セッションの kit ローカル観測値（multi c012/c013/c0123 UNSAT・c01/c02/c03/c12 INDET・
k3 c1k3p5..p11 UNSAT・c0k3p0/c1k3p0 INDET の 15 追加分）は未出版であり、
本セッションはこれを「観測済み予備情報」として扱い、すべて本環境でやり直して records に載せる。
UNSAT 決着行は conflicts bit-exact で再現することが期待され（決定的 CNF 生成 + pinned kissat）、
一致した場合のみ kit 観測値との相互検証として記録する。INDET 行の conflicts は壁時計打ち切り点であり bit-exact でない。

## 本セッションのスコープ（被覆規約は K1197/m=22 と同一）

1. **残り直接バケットの決着**: k3 直接 c1k3p1..p4・c0k3p1..p11（cap は壁時計で INDET = honest negative）。
2. **multi INDET バケットの追分解**: c01/c02/c03/c12 の 220s INDET は欠損行の正確な石数 0..3 による
   krow ピン分割（sweep35 規約）で追分解する。
3. **k3 抵抗バケットの x2 分割**: c0k3p0/c1k3p0 は第2石 x2 分割（x2gen23.sh 方式・k-aware 上限）で完全分解する。
4. **全バケット決着後の判定**: 全 UNSAT なら 4×23 row-deficient witness-free（witness-free 幅集合 {21,22,23}・
   **M_{4,5} = 21 または ≥ 25**）。いずれかで SAT が出たら witness を復号・二系統検証（sat.js 整数 verifyConfig +
   Python Fraction verify_witness.py）して **M_{4,5} ∈ [24,140]** とし掃引を停止する。
5. **出版**: records23.jsonl は増分 push（append-only）、driver/log 類は中断レーンの実験 dir
   research/experiments/four-row-q5-m23-class-split-20261121/ へ追記、決着後に README 結果節・K 項目・
   knowledge README bullet・mwq_stabilization.csv を更新する。

## 非目標

- 4×24 以降への主張はしない。上界 U_{4,5}=140（K0318）は不変。
- 標準 11×11 空盤・二石 root は本レーンの無関係・UNKNOWN のまま。conflicts 数・実行秒数を勝敗として読まない。
- branch/PR は作らず main に直接出版する。fetch-back は byte/sha 照合で行う。
