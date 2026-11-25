# n11-residual78-windfall4-receipt-fold-20261120

K1066 が三重独立検証済み証明書とともに出版した cost65h windfall 4 root
（child `00000000000000803202000000001000` の bit 40/43/99/118）を
receipt として消費する **fold (第13〜第16 receipt)** の正本。
branch/PR は作らず main に直接出版。

## 何をしたか

- fold 機械 `scripts/fold_windfall4.py` は、出版済み fold 機械
  `fold_ninth_twelfth.py` の全連鎖 gate（base frontier 6,259/495,507 →
  cost78c/79c → first → second/third → fourth → fifth/sixth → seventh →
  eighth → 6,222行/492,688・incidence 11,848・verdict universe
  340/164 → sweep43 後 379/168、全て再計算）をそのまま検証した上で、
- 第9〜第12 receipt（ninth-twelfth fold, sha256 pin `ee002d792…`）は
  sweep43 WIN root からの**幾何再導出**（8 D4 像・全 single-bit 削除）で
  covered S6 rows / covered five-parent target rows / frontier を重建し、
  出版記録の全 row list・frontier 統計（6,213/492,021・solved 1,635・
  incidence 11,826・needed 4,513/357,882）と一致を gate。
- 同じく sha256 pin した resolve5 記録・resolve6 記録（ともに残余 78 行
  list 完全一致を gate）を経て、windfall 4 receipt を閉鎖計上:
  - 各 root の raw root hex (child|1<<bit)・canonical root 写像
    （bit 99/118 は raw が D4 非正準形）・popcount 7・unsafe quadruples 0
    を gate。
  - 証明書 sha256・bytes・header・root 行 (raw maxbit child 規約)・
    rows 数を K1066 記録から再検証。抽出 run1/rerun summary の
    nodes・rows・per-move ok/uncapped・fbt_drops 0・rerun byte-identical
    を gate。
  - TS Bareiss subroot stats（aggregate seen/terminals/opponentEdges）・
    union audit（missing 0 / extra 0 / consumed_unique == rows）・
    純 python Bareiss replay（terminal {13,15,17}）・BigInt 独立検証
    （terminal [13,17]）をすべて再読み込み、bigint と TS Bareiss の
    状態流量一致 (visited states / terminal count / loser reply edges)
    を gate。
  - runner v16 fresh 再現 (crosscheck jsonl) の nodes が resolve6 出版
    raw bit_line (batch3/4/7/8) と node-exact 一致、pilot_d6
    loss=false 3,402 nodes 合格を gate。
  - legal move list を legal_moves_of で独立再導出し証明書の moves と一致
    (48/58/52/56) を gate。
  - K1066 の 50 gate が全 PASS であること、resolve6/K1066 両記録の
    covered residual rows が一致すること、被覆 row が fold 前後の開放
    frontier に存在し二重閉鎖でないことを gate。

## 結果 (output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json が正本)

- **fold はちょうど 4 行を閉鎖**（追加の frontier 副次閉鎖はなし）:

| receipt | bit | raw root (証明書 root 行) | canonical root | moves | 被覆 target row (cost) |
|----|----|----|----|----|----|
| thirteenth | 40 | 00000000000000803202010000001000 | 同左 | 48 | 00000000000000801202010000001000 (64) |
| fourteenth | 43 | 00000000000000803202080000001000 | 同左 | 58 | 00000000000000801202080000001000 (79) |
| fifteenth | 99 | 00000008000000803202000000001000 | 00000000000000803800000008001200 | 52 | 00000000000000003800000008001200 (76) |
| sixteenth | 118 | 00400000000000803202000000001000 | 00000000010000803800000008100000 | 56 | 00000000010000003800000008100000 (80) |

- frontier: **6,213行/492,021 cost → 6,209行/491,722**、solved S6
  1,635→**1,639**、parent incidence 11,826→**11,818**、
  s6_needed 4,513→**4,509**、needed cost 357,882→**357,583**、
  closed edge cost **299**。remaining_s5_orbits 173 は不変。
- 5親 112 行 target: **34 → 38 閉鎖（残余 78 → 74 行）**、
  fully-closed parent 0・affected parents は parent_closure 参照。
- 2 回実行で出力 byte-identical。
  出力 SHA-256
  `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2`。
- verdict 基底: 各 receipt は depth-10 単一順 (andclose=1) engine verdict
  に**三重独立検証済み証明書**が裏付けた receipt である（sweep43 系の
  双順序 verdict-duality 規約とは異なる variant。詳細と出典は
  `verdict_basis_note` と各 receipt の `verdict_basis` を参照）。

## 入力 (W layout → repo path。すべて fold 時点の main から raw fetch し git blob sha1 を照合)

- `inputs/*`, `ex48/*`, `excov/*`, `foldv2/*`, `fold4rec/*`, `fold56rec/*`,
  `sweep35/*`, `sweep6/*`, `sweep28/*`, `sweep43/*`,
  `fold_fourth_fifth_sixth.py`, `fold9/*` (ninth-twelfth fold + resolve5),
  `windfall/output/*` (resolve6):
  すべて `source_blob_pins` / `previous_fold` / 既出版各実験の
  output JSON・scripts に対応（fold9 記録 sha256 `ee002d792…`、
  resolve5 `5a2f4815…`、resolve6 `e85d4bfb…`、K1066 verify
  `a3ca1b3df…`、証明書 4 本の sha256 は記録内 pin 参照）。
- windfall 証明書と検証 artifact は K1066 実験
  `research/experiments/n11-residual78-windfall4-cert-extract-20261120/`
  の `certs/` と `output/` から直接読み込む。
- 機械は `/home/user/work` を W とする layout で実行した
  （fold9 機械と同一規約。上記 mapping で再現可能）。
  実行時 main head: `68b04984f22fe907120ded2deaf5b03182108fd7`。

## 解釈規約（他の n11 項目と同一）

- WIN7-D10 は各 7 石 root からの depth-10 内の先手必勝のみを主張する。
  空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  **すべて UNKNOWN のまま**。
- REFUTED-D10 は LOSS 証明ではない。pn/dn・solved 数は勝敗ではない。
- fold は行被覆の簿記である。残余 74 行は resolve5 の 39-root live
  witness 計画（条件付き）で引き続き独自に全被覆されている。74 行の
  各自の receipt が出版されるまでは閉鎖計上されない。
