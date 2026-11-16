# 2026-11-17：cost76d・cost77e両行のv17全行再検査（過去lane再検査キュー第5弾）— 2行併せて53 bitの大規模node補正・verdict反転0・WIN 4 bits全不変

開始時の最新mainは `427e29fa450482dc5572cdc33a66527a4040f1e9`（作業中に並走レーンのコミットが継続）。cost65n・66c・64d/64g・64fに続き、過去lane再検査キューの最後の未実施2行 **cost-76d**・**cost-77e** を再検査した。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

- **76d**: child `00000000040000003800080008000000`・76 swept bit・WIN7-D10 2 bits〔19/49・証明書二重検証済み〕・REFUTED-D10 74・capped 0・出版総nodes 96,246,915（max bit 112 = 10,150,705）。
- **77e**: child `00000000040000809002000000004000`・77 swept bit・WIN7-D10 2 bits〔37/69・証明書二重検証済み〕・REFUTED-D10 75・capped 0・出版総nodes 116,019,458（max bit 33 = 11,599,283）。

両行ともfbt logが警告した飽和圏（76c bit 113の8.2M反転事例を超えるper-bit探索を含む）で、head-1452構成行として再検査キューに残っていた最重量行である。

## 77e child-hex事故（記録）

最初の77eバックグラウンド実行は1文字誤記のchild `00000000040000809092000000004000`（`9002`→`9092`）で走り、総nodes 1.6M・terminalStoneRange [15,17] の異常から誤りを検出して全出力を破棄した。真正childは出版sweep記録 `class2-lane-cost77e-sweep-20261116.json` の `s6_child` フィールドから再取得し、証明書root hex（child|1<<bit）で相互確認した。誤child出力は `o77e-invalid-wrongchild/` に事故記録として保持（出版せず）。**要約やメモ経由でなく常にrepo出版記録からchild hexを取ること**が教訓。

## 実施内容

fbt修復済みv17 engine（blob `c132cc64`）で両行の全swept bit（76d 76 bits・77e 77 bits）を出版時と同一のbatch分割（各10バッチ）・depth 10・cap 1e9（両行とも0 cappedでcap不発動）・`--andclose 1`・候補ごとengine完全reset・pilot_d6制御付きで再実行し、出版raw batches 1-10（blob SHA pin照合・repo byte照合済み）と全フィールド比較した。76dは初期実行（前セッション起動）に加えて自家管理driverでの2回目全行実行、77eも2回の全行実行を行い、いずれもms以外全bit・全pilot一致で決定性を確認した。最大node補正bit（76d bit 112/99・77e bit 33/0）はv16/v17 × andclose 0/1のorder-matrix（4構成×4 bit）でverdict安定性を確認した。

## 結果

- **76d: 23/76 bitにnode補正・verdict反転0・WIN bits 19/49不変**。nodes総和 96,246,915 → 94,073,241（−2,173,674）。最大補正: bit 112 10,150,705 → 2,311,986（−7,838,719・−77%）・bit 99 1,952,317 → 8,022,542（+6,070,225・v16のサイレントdropによる過小計数の修正）・bit 2 −541,397。53 bitは完全一致（非飽和）。terminalStoneRange・capped・andcloseの不一致は0。
- **77e: 30/77 bitにnode補正・verdict反転0・WIN bits 37/69不変**。nodes総和 116,019,458 → 106,134,971（−9,884,487）。最大補正: bit 33 11,599,283 → 1,703,482（−9,895,801・−85%・これまでで最大の相対補正）・bit 0 3,948,711 → 1,915,259（−2,033,452）・bit 3 +1,513,742・bit 96 +461,376。47 bitは完全一致。
- pilot 20/20（両行×10バッチ・3402）。2回実行とも全bit完全一致（決定的）。
- 監査script 51 checks全PASS・監査JSON 2回実行byte-identical。

## order-matrix（最大補正bit・verdict安定性）

v16/v17 × andclose 0/1の4構成を、76d bit 112・99・77e bit 33・0の計4 bitで実行した。全構成REFUTED-D10で**verdictは順序・engineいずれに対しても安定**。node数はengine・順序で変動するが、v17の決定的値がengine-corrected値であることを確認した（詳細はorder-matrix JSONL）。

## 含意

1. 76dのREFUTED-D10 74 bit・77eのREFUTED-D10 75 bitはplanning証拠として有効（engine-consistencyの簿記確定）。node規模はv17値を正とする。
2. WIN bits 4個（19/49/37/69）は証明書+v17の双方で不変。76d/77e fold（preregistration済み）の基盤は無影響。
3. **飽和はnode数に非単調な大補正を出し得る**（bit 99の+6.07Mのように過小計数も起きる）ことが確定。76c bit 113のような反転が起きなかったのは、両行のREFUTED-D10が真であったためであり、node数規模による安全性の保証ではない。
4. 過去lane再検査キューのnode-exact比較可能な行（65n/66c/64d/64g/64f/76d/77e）は全て完了。残りは65f/65j/60c（v15 sweep由来・node-exact比較不能・別方式が必要）。

## 保存物

- 監査script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost76d77e_v17_full_row_rechecks_20261117.py`（stdlibのみ・入力blob SHA pin照合・engine blob pin照合・51 checks・2回実行byte-identical・決定性2回実行照合）
- 監査JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76d77e-v17-full-row-rechecks-20261117.json`
- v17生記録: 同output/配下 `class2-lane-cost76d-v17-recheck-batch{1..10}-20261117.jsonl`・`class2-lane-cost77e-v17-recheck-batch{1..10}-20261117.jsonl`（計20本）
- order-matrix: 同output/配下 `class2-lane-cost76d-v17-ordermatrix-20261117.jsonl`・`class2-lane-cost77e-v17-ordermatrix-20261117.jsonl`（bit 112/99・bit 33/0のv16/v17×andclose 0/1計16実行）
- 入力（出版済み・blob pin照合済）: `class2-lane-cost76d-raw-batch{1..10}-20261116.jsonl`（`d3c9ae36`/`9144839a`/`8dae0d02`/`3c1e4557`/`c0c152d5`/`dbf10a30`/`57c0eda0`/`f4862407`/`bc32bed9`/`8855f2d6`）・`class2-lane-cost77e-raw-batch{1..10}-20261116.jsonl`（`2034e397`/`cb883d07`/`a64d7a19`/`32d9d958`/`489f13e3`/`5846d047`/`106ac238`/`3956be4d`/`59df74f2`/`d9f4fa3c`）

## 信頼境界

v17自体の健全性は経験的証拠による（非飽和領域でv16一致・pilot不変・76c両順序安定・order-matrix安定）。本再検査はengine-consistencyの簿記確定であり、REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。NOT-STERILEも行の勝敗を意味しない。node補正は計算簿記の訂正であり勝敗の変化ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
