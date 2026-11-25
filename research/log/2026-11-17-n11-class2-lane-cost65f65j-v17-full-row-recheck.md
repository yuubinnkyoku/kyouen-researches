# 2026-11-17：cost65f/65j行のv17全行再検査（過去lane再検査キュー完走）— WIN 17 bits全不変・v16部8 bit node-exact・反転0・verdict-only部56 bit全一致

開始時の最新mainは `b27c0b5d2efbaa3dc4d471e59ffc27807fe0015e`。cost76d/77e再検査log（同日）に続き、fbt飽和欠陥logが挙げた過去lane再検査キューの最後の未実施行であるcost-65f/65j（child `00000000000000809102000080000000`・65候補中64 swept bit + 転写bit 113）を再検査し、**これで再検査キュー全行（65n/66c/64d/64g/64f/76d/77e/65f/65j）が完了した**。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

65f/65jは出版順序が特殊な行である: bit 1-64のraw batches 1-7（13 WIN + 44 REFUTED・bit 92はv4 erratum訂正済み）が**v15 engine**（2026-11-14出版・pilot_d6 5949 nodes）で、batches 8-9の8 bit（111/112/114/116/117/118/119/120）が**v16 engine**（2026-11-16出版・pilot_d6 3402 nodes）で掃引された。65j inflight v5はFOLD COMPLETE。WIN 17 bits（4/15/18/20/21/23/25/28/66/79/91/101/109/112/116/118/119）は全て証明書二重検証済み（65f win13 manifest `617d3d8d`・65j win4 manifest `d4981d7e`）で不動。REFUTED-D10 48 bitの証拠有効性と、v16部に潜む可能性のあるfb飽和が焦点。

## 実施内容

fbt修復済みv17 engine（blob `c132cc64`）で64 swept bit全部を出版時と同一のbatch分割（9バッチ: 65f raw 1-7 + 65j raw 8-9）・depth 10・cap 1e9・`--andclose 1`・候補ごとengine完全reset・pilot_d6制御付きで再実行した。比較は時代で分けた:

- **v16由来8 bit（batches 8-9）**: 全フィールド比較（node-exact）。fb飽和介入なしの想定。
- **v15由来56 bit（batches 1-7）**: **verdict-only比較**（loss field一致）。v15とv17はnode計数が非互換（pilot_d6が5949 vs 3402）でnodes/capped/terminalStoneRangeは参照記録のみ。

入力raw 9本とengineはblob SHA pin照合済み（`46ff5b20`/`cd3bfedb`/`1f3d6dc8`/`cfffbcdd`/`9d789a29`/`2ae5fd9b`/`89b554a3`/`963c9f80`/`52cd7d8d`・engine `c132cc64`）。

## 結果

- **v16部8 bit（111/112/114/116/117/118/119/120）が全フィールドnode-exact一致**（nodes含む・補正0件）。fb飽和なし。WIN 4 bit（112/116/118/119）とREFUTED 4 bit（111/114/117/120）がそのまま確定。
- **v15部56 bitのverdictが全て一致**（WIN 13 + REFUTED 43含む）。verdict反転0件。
- **WIN 17 bits全不変**（4/15/18/20/21/23/25/28/66/79/91/101/109/112/116/118/119）。証明書（65f win13・65j win4 manifests）と整合。
- capped 0。v17 pilot 9/9（3402 nodes）。v17 nodes総和 95,170,152（出版総和402,603,616はv15混在のため非比較可能・参照値）。
- **決定性**: 2回の完全独立実行（9バッチ×2）で全bit+全pilotが完全一致（msのみ相違）。
- 監査script 24 checks全PASS・2回実行で監査JSON byte-identical。

## 含意

1. 65f/65j行のREFUTED-D10 48 bitはplanning証拠として有効（v16部はnode-exact、v15部はverdict-only）。
2. **過去lane v17再検査キューが完走**: 65n（47 bit node-exact）・66c（58/59一致・bit 117 −22）・64d/64g（123 bit全一致）・64f（59 bit全一致）・76d（23/76補正・反転0）・77e（30/77補正・反転0）・65f/65j（本エントリ）。反転はキュー全体で0件。WIN bitsは全行で不変。76c bit 113（WIN→REFUTED）が唯一の反転事例のまま。
3. v17での相対補正は76d/77e（fb飽和・数十bit）と66c bit 117（−22）に限られ、**v17 engineのfb非飽和領域におけるnode-exact性**がさらに7行分の実測で裏付けられた。
4. 65f fold・65j fold（head 1472到達）の基盤は無影響。head-1472以降のcoverage設計はv17訂正後のnode数で再計算の必要なし（65f/65jは補正0）。
5. 次の焦点はcost64h fold receipt着地（並走・着手禁止中）と、head-1452以降の未掃引候補行。

## 保存物

- 監査script: `scripts/verify_cost65f65j_v17_full_row_recheck_20261117.py`（stdlibのみ・入力blob SHA pin照合・24 checks・2回実行byte-identical）
- 監査JSON: `output/class2-lane-cost65f65j-v17-full-row-recheck-20261117.json`
- v17生記録: `output/class2-lane-cost65f65j-v17-recheck-batch{1..9}-20261117.jsonl`（9本）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost65f-raw-batch{1..7}-20261114.jsonl`（`46ff5b20`/`cd3bfedb`/`1f3d6dc8`/`cfffbcdd`/`9d789a29`/`2ae5fd9b`/`89b554a3`）+ `class2-lane-cost65j-raw-batch{8,9}-20261116.jsonl`（`963c9f80`/`52cd7d8d`）

## 信頼境界

v17自体の健全性は経験的証拠による（非飽和領域でv16一致・pilot不変・76c両順序安定）。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。v15部はverdict-only比較であり、v15由来のnode数はv17での再計測値に置き換わらない。NOT-STERILEも行の勝敗を意味しない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
