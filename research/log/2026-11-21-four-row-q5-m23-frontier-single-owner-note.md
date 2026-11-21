# 2026-11-21 four-row q5 m=23 frontier — 単一オーナー宣言ノート（高速レーン）

- 宣言時刻: 2026-11-21T19:25Z
- 宣言時 HEAD: `5a9cf30492de286e9a80a196ce13606eab3ecf6f`
- オーナー: 高速レーン（本セッション）。branch / PR は作らず main に直接反映する。

## Claim

(4,23,5) の行欠損極大安全配置（deficient は行石数 ≤ q−2 = 3）の存在判定。
K1197（[item](../knowledge/items/K1197-four-row-q5-m22-deficient-nonexistence.md)）が
「次の前線は 4×23（着手には単一オーナー宣言と最新 main 再取得が必須）」と明示した未着手枠であり、
着手前に最新 main を再取得し、他レーンの同一 (4,23,5) 着手がないことを確認済み
（2026-11-21T19:25Z 時点の research/log 宣言列に 4×23 着手なし）。

- 判定: 全 piece UNSAT なら witness-free 幅集合 {21,22,23}・**M_{4,5} = 21 または ≥ 25**
  （K0821 監査規約: 幅 22/23/24 は成立不可能）。
- SAT なら witness 帯は m=23 まで復活し **M_{4,5} ∈ [24,140]**・witness を復号して検証する。

## 器材と較正（着手前環境で実施・全件 PASS）

- 生成器: `sat.js`（md5 `0cc6021a…`）・`sat2.js`・`sat3.js`・`sat4.js`（k-aware x2 上限版）。
  m21/m22 レーンの出版正本（four-row-q5-m21/22-class-split-20261115/scripts/）から取得。
- ソルバ: kissat 4.0.4 static linux-amd64（md5 `3a5eba830aa6008a604fcc9bbe99a325`・出版 pin と一致）。
- 較正 1: 陽性対照 (4,20,5) class {0} --krow=0:3 --minpos=1 の CNF が
  md5 `362034b2…` で byte-exact 再生・kissat が **SAT 375,415 conflicts bit-exact**
  （m21/m22/takeover の 3 レーン交差較正值と一致）。
- 較正 2: (4,22,5) c0k3p0 CNF（md5 `bf26eee9…`）・c0k3p0x2b1 CNF（md5 `7db59b4b…`）が
  byte-exact 再生（sat3 / sat4 k-aware の出版正本との一致）。

## 被覆の完全性（K1197 / m22 規約と同一構造・幅の違いのみ）

- 欠損クラス = 石数 ≤ 3 の行の集合。safe な行は ≤ 4 石なので欠損行の補集合は exactly 4 石
  （sat3.js --class は D 外の行を rowGe 単位で FULL 固定するため制約を課しても被覆は完全）。
- 行ミラー V（行 0↔3, 1↔2）で正準クラスは 9 個。
- 単一クラス {0},{1}: 正確な石数 k∈{0,1,2,3} と minpos p∈0..11 で分解
  （sound H-split: min(x1, 22−xk) ≤ floor(22/2) = 11。H は行を保存するのでクラス内で健全。
  minpos と lex の併用は unsound のため全インスタンス lex なし）。
- multi クラス 7 個は直接。INDET が出たら krow ピン分解（欠損行の正確な石数で追分解・m21 規約）。
- k3/k2 の抵抗バケットは x2 第 2 石位置分割（完全で disjoint な場合分解。k-aware 上限:
  k=3 → B ≤ m−2 = 21、k=2 → B ≤ m−1 = 22。m22 レーンで検証済みの sat4.js k-aware 版）。
- 計（直接）: multi 7 + k2 24 + k1 24 + k0 2 + k3 24 = 81 インスタンス + 陽性対照 1。

## 実行制約の誠実記録

- 本 sandbox の bash call は 300s 上限でバックグラウンドプロセスは call をまたいで生存しない
  （2026-11-21T19:21Z の実測）。そのため piece cap 260s（壁時計）の resumable chunk runner
  （1 call 数 piece 消化）で掃引する。cap 到達の INDET は honest negative であり不在主張ではない。
  INDT は分解（krow ピン / x2）で決着させる。決着レコードはこまめに増分 push する
  （環境リセットで未 push 分が消えた過去事故への対策）。

## 受入条件

1. records（append-only・CNF md5 収録・cap 記録）を実験 dir に出版し fetch-back byte 検証する。
2. SAT の場合 witness を sat3.js verifyConfig と verify_witness.py の少なくとも 2 系統で検証する。
   UNSAT の場合は被覆の完全性表（9 クラス × 直接/分割の内訳・INDET 残数 0）を README に明示する。
3. K item・session log・knowledge README bullet は完了時に出版する（K 番号は出版時点で 3 点確認）。

## 非目標

- m ≥ 24 の存在不在は一切主張しない。上界 U_{4,5} = 140（K0318）は不変。
- `mwq_stabilization.csv` は本レーンでは更新しない（K1201 前例）。
- conflicts 数・実行秒数を勝敗として読まない。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーンと無関係・UNKNOWN のまま。
