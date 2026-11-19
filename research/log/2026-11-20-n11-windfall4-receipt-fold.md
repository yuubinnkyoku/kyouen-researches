# 2026-11-20 n11 長期レーン: windfall 4 証明書の receipt fold（第13〜第16 receipt・K1067）

## 経緯

- K1066（windfall 4 証明書の抽出・三重独立検証）の「次の一手」1番:
  4 証明書を入力とする receipt fold（4 行の閉鎖計上、fold 機械の入力
  chain 再構築）。本実験で実行。
- fold 記録の系譜: 第9〜第12 receipt（sweep43 の 4 WIN・fold9 記録
  sha256 `ee002d79…`）と resolve5 正本（sha256 `5a2f4815…`）が直前の
  基底（残余 78 行・frontier 6,213行/492,021 cost）。windfall 4 根は
  K1063 resolve6 正本（sha256 `e85d4bfb…`）の
  win-coverage-of-residual evidence が出典（c65h child bit
  40/43/99/118・raw batch3/4/7/8 の bit_line）。

## 何をしたか

- fold 機械 `scripts/fold_windfall4.py` を書いた。構成は
  （a）published fold9 機械の全連鎖 gate を base 6,259/495,507 から
  eighth 6,222/492,688（incidence 11,848・verdict universe 340/164 →
  sweep43 後 379/168）まで verbatim 再現、
  （b）第9〜第12 receipt は cert9 ファイルを再検証せず、fold9 出版
  記録（sha256 pin）の 4 root から幾何再導出（8 D4 像・全 single-bit
  削除）して covered rows・target rows・post-twelfth frontier
  （6,213/492,021・solved 1,635・needed 4,513/357,882・
  incidence 11,826）の全一致を gate、
  （c）windfall 4 receipt の gate（下記）、
  （d）frontier・5親 target の閉鎖計上と出力。
- windfall receipt の gate は K1066 成果物を直接消費:
  raw root = c65h|1<<bit、canonical 写像（bit 99/118 は非正準 raw）、
  証明書 sha256・bytes・header・root 行（raw 規約）・行数、抽出
  run1/rerun summary（nodes 3,074,926/7,700,023/3,355,354/6,137,302・
  rows 31,189/51,767/36,625/55,838・fbt_drops 0・per-move 全 ok/
  uncapped・rerun byte-identical）、TS Bareiss subroot stats + union
  audit、純 python Bareiss replay（terminal {13,15,17}）、BigInt 独立検証
  （terminal [13,17]）、bigint と TS Bareiss の状態流量一致、
  runner v16 fresh nodes が published raw bit_line
  （1,105,860/3,269,824/1,114,855/2,307,338）と node-exact 一致、
  pilot_d6 対照、legal moves 48/58/52/56 の独立再導出、K1066 の 50 gate
  全 PASS、WIN/LOSS 衝突 0、covered residual rows が resolve6/K1066 と
  完全一致、fold 前から開放・二重閉鎖なし。
- 入力 33 ファイルは fold9 機械と同じ W layout（`/home/user/work`）に
  main から raw fetch し git blob sha1 を照合（誤り 1 件:
  excov/cover49.json は five-parent-refuted-excluded-cover-resolve ではなく
  five-parent-residual-49-cover（residual 97）の誤配線だったため修正。

## 結果

- **fold はちょうど 4 行を閉鎖**（副次閉鎖 0 行）:

| receipt | bit | target row | cost |
|----|----|----|----|
| thirteenth | 40 | 00000000000000801202010000001000 | 64 |
| fourteenth | 43 | 00000000000000801202080000001000 | 79 |
| fifteenth | 99 | 00000000000000003800000008001200 | 76 |
| sixteenth | 118 | 00000000010000003800000008100000 | 80 |

- frontier: 6,213行/492,021 → **6,209行/491,722**、solved S6
  1,635→**1,639**、incidence 11,826→**11,818**、needed 4,513→4,509・
  357,882→357,583、closed edge cost **299**、fully-closed parent 0・
  affected parents 5、remaining_s5_orbits 173 不変。
- 5親 112 行 target: **34 → 38 閉鎖（残余 78 → 74 行）**。
- 出力 2 回実行 byte-identical（SHA-256 `24db2352ad0d…`）。
  snap 時 main head `68b04984f2…`。

## 解釈規約（他の n11 項目と同一）

- windfall receipt は depth-10 単一順（andclose=1）engine verdict に
  三重独立検証済み証明書が裏付けた receipt（sweep43 系の双順序
  verdict-duality とは別の正当化経路。記録の verdict_basis_note 参照）。
- REFUTED-D10 は LOSS 証明ではない。fold は行被覆の簿記。
  pn/dn・solved 数を勝敗として読まない。
- 残余 74 行は resolve5 の 39-root live witness 計画（条件付き）で
  引き続き独自に全被覆。74 行の各自の receipt 出版までは閉鎖計上しない。
- **二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・標準 11×11 空盤は
  すべて UNKNOWN のまま。**

## 次の一手（労力の少ない順）

1. 残余 74 行の coverage 再解決（resolve6 方式の 74 行版。windfall 4 根を
   known-WIN に加えた verdict universe join で witness 計画を更新）。
2. 39 live witness 掃引（K1059 同一規約・runner v17・pilot_d6）の
   74 行版への切替（候補が 4 行分減る）。
3. 追加の cost-lane raw batch 正本からの windfall 探索
   （resolve6 の join は明示 pinned source のみに限定していたため、
   corpus 内に未結合の WIN hit が残っている可能性）。
