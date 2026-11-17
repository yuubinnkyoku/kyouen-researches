# n11 class2-lane presweep census v13: 79c行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost79c sweep完了（20 WIN7-D10 / 59 REFUTED-D10 / 0 capped・206,090,979 nodes）と
19証明書の出版（manifest blob `e904a376`・claim v2 blob `d16d7b1a`）、並走による
BigInt一般化円第三監査（bits [1,2,21] PASS・記録blob `50190347`・commit
`df3d8d2f`）を受け、head-1473 presweep censusをv12からv13に更新した。
v13は16番目のverdict map（cost79c: 20 WIN / 59 REFUTED / 0 capped）を
overlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v13_20261118.py`
  （v12スクリプト blob `876e1d56` を基盤に、79c raw batch / audit / claim v2 /
  certificate manifest の入力を追加し、16番目のverdict map `cost79c` を構築）。
- 79c生バッチ9ファイルを独立再監査（9×3402 pilot・79/79 per-bit verdict・
  node sum 206,090,979・audit per_bitのroot_canon == D4 canon(child|bit) を
  全79bitで検証）。
- bit 110がcost73k bit 87証明書でcanon-coveredであることを計算機検証
  （canon(79c_child|1<<110) == cost73k bit 87 d4_canon_root）。manifestの
  19 bits = 20 WIN − canon-transfer bit 110 が成立。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）
  はv1 censusとbit-exact一致。16 map構築は内部conflict 0・
  harvestとのcross-agreeを維持。
- 39 family行を再計算し、v12のpublished countsを39/39で再現
  （`family_row_open_v12_minus_79c_only_reproduced`: 差分は79c map由来のみ）。
- v13出力は2回のコールド実行でbyte-identical（md5 `c3e88c52…`）。

## 結果

- 79c行（`00000000000000c09002000200000000`）をswept扱いのexcluded行として
  記録（open 0・known 79・confirmation outcome 11/11でcensus v12 overlay予測と
  一致・0 conflict）。receipt foldは66i/66j/69j/71e/72d/73i/73j/73k/73l fold
  完了後に実施。
- 次ターゲット: **`00000000020000003800400080000000`（cost 79・open 72・
  confirmation 7・parent `00000000020000003800000080000000`・demand
  {c1:0, c2:0, c4:3}・石bits [31,46,59,60,61,89]）**。census v12 runner-up。
  confirmation 7 bits（5/27/41/79/90/93/115）は全てREFUTED-D10
  （pre-64h harvest ×3・cost74i ×2・cost75f ×2）で、sweepでfreshに再実行する。
  legal_candidates.py独立列挙と79bit（72 open + 7 confirmation）で一致。
- runner-up: `00000000020000003800000880000000`（cost 79・open 74）。
  ranking top-10の10行はすべてparent
  `00000000020000003800000080000000`（cost 79〜86・open 72〜78）。
- cross_checks新規（79c系）: win bits claim/audit/manifest一致 20/20（manifest
  19 = 20 − bit 110）・manifest totals（1,106,127 rows / 339,101,130 nodes /
  39,877,889 bytes・fbt_drops 0・capped 0）・confirmation 11/11・bit 110
  canon-covered・v15 cross-engine 14/14・BigInt第三実装 bits [21,30,117,120]
  PASS・並走一般化円監査 bits [1,2,21] PASS。

## 制限

- 本censusは探索計画bookkeepingのみ。新たなverdictは作っていない。
- 79cの証明書は「個別7石rootからdepth 10以内の先手勝ち」のみを証明し、
  manifest行のreceipt foldは未実施。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- cost 79d sweep（`00000000020000003800400080000000`）のclaim作成と実行
  （open 72 bitsを8×9 batch + confirmation 7 bitsを1 batch）。
- 並走管轄（着手禁止）: 66i/66j/69j/71e/72d/73i/73j/73k/73l receipt fold、
  cost73k測定系、K09xx系。
