# 2026-11-17 n11 class2-lane: cost-64a v17 full-row re-check (past-lane queueの漏れ行) + census runner-up harvest-gap修正

## 概要

過去lane v17再検査キュー（fbt飽和修復後のv16掃引行再実行:
64d/64g/64f/76d/77e/65f/65j/65n/66c/58c/76c）に**cost-64aだけが含まれていなかった**
ことを発見し、同一セッションで2つの成果を出版した:

1. **cost-64a（child `00000000000000801282000040000000`）の v17 full-row re-check**:
   64 legal bits全てをfbt修復済みv17 engine（blob `c132cc64`）でfresh再実行
   （8 batch・batch分割は出版v16 raw batchesと同一・depth 10・cap 1e9・andclose 1）。
   **64/64 REFUTED-D10・verdict反転0・node-exact 63/64**（bit 87のみ
   2,102,913→2,101,158の−1,755節点修正）・総nodes **38,157,151→38,155,396**・
   terminalStoneRange [13,17]全行・pilot d6 = 3402 × 8。
   determinism re-run（batch 5・8 = 16 bits）はloss/nodes/capped/terminalStoneRange
   全フィールド一致。**STERILE（64/64 REFUTED-D10）はv17でも確定**。
   4つの出版verdict map（64h/76c/66i/66j）とのcross-source conflict scanは
   conflict 0（重複bit 98は両側REFUTEDで一致）。

2. **head-1472 presweep census v4 runner-up の false-open 修正**:
   census v4のranking #1（cost 64・55 open・`00000000000000801282000040000000`）は
   **上記の通り全面掃引済みのSTERILE行**。v1 harvestはclaim JSON
   （`class2-lane-cost64a-inflight-20261116.json`）を「no win bits」でskipしており
   （verdictsが`win7_bits`リストではなく`sweep_result`カウンタとして保存されているため）、
   64aの64 bit分のverdict mapはcensus frameに一度も取り込まれていなかった
   （64f/76d/77e/65f/65jと異なり明示的raw-batch取り込みpassも無い）。
   bit tableのopen 56 / harvested_refuted 8はbookkeeping artifactであり、
   修正後の行statusは **swept・STERILE・open=0**。
   これにより ranking から同childが除外され、残る最安未掃引行は
   cost-69 `00000000000000403800000008000020`（in-flightのcost-69j）の次の
   `00000000000000c09002000000002000`（cost 71・70 open・demand c2=2/c4=2）
   （fold-pending除外はv4 selection policyどおり・確定選定は次回censusが行う）。
   v1 bit tableの他の12 open行は全て未掃引（またはoverlay/claim処理済み）で、
   同種のgapはこの1行のみ。

## 位置づけ

- 本記録はengine再実行 + census簿記修正のみで、**manifest行の閉鎖・head更新はない**
  （head 1472不変）。STERILE行はdepth-10 receiptsでは閉鎖不能（K0863）。
- S5 `00000000000000801202000040000000` familyはcost-76 child
  `00000000010000809092000001000000`（WIN7-D10 bits {61,99}・fold pending）経由でしか
  閉鎖できないことが確定した。
- REFUTED-D10はLOSS証明ではない。

## 検証

- script `verify_cost64a_v17_full_row_recheck_20261117.py`: v1 census（blob `0d9a94a2`）
  とv4 census（blob `d70eae09`）・64a claim（blob `08551cd0`）・v16 raw 8本・
  v17 recheck 8本・det 2本の全入力をgit blob sha pinで照合し、
  bit table root_canon 64/64をD4 canon再計算と一致assert、
  harvest skip reasonの実在assert、census status計数の正確性assertを含む。
  出力は2回実行でbyte-identical（md5 `db659e7ba88a8868ff7aab2dd7e8766c`）。

## 11×11ステータス

**11×11空盤はUNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は
いずれもUNKNOWNのまま。

## 成果物

- `scripts/verify_cost64a_v17_full_row_recheck_20261117.py`
- `output/class2-lane-cost64a-v17-full-row-recheck-20261117.json`
- `output/class2-lane-cost64a-v17-recheck-batch{1..8}-20261117.jsonl`
- `output/class2-lane-cost64a-v17-det-batch{5,8}-20261117.jsonl`

## 次の一手

- 次回census（v5）は本記録の64a verdict mapを取り込んだ上で次ターゲットを選定する
  （候補: `00000000000000c09002000000002000` cost 71、ただしfold-pending除外の再評価を含む）。
- 69j certificate（6 WIN7-D10）の着地監視。76c/66i/66j/69j fold receiptは並走管理のまま着手禁止。
