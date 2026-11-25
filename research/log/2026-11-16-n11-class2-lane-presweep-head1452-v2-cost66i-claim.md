# 2026-11-16：head-1452 presweep census v2（64h/76c掃引overlay付き次ターグット選定）と cost-66i claim v1

開始時の最新mainは `8719c6ea5922ac1a37b10786b0dba5a172c058f8`。作業前に `AGENTS.md`、`research/knowledge/README.md`、cost64h/cost76c のclaim・audit・fold prereg、head-1452 presweep v1、v17 fbt修復記録を確認した。

## 目的

head-1452 presweep census v1（git blob `0d9a94a272de9fe45708757f17bfea60239a3c9b`）の出版後に完了した2つの掃引（cost-64h・cost-76c）は、v1 census作成時点では未完了だったためv1に反映されていない。両掃引のreceipt foldはまだmainに着地していない（着手禁止）が、7石rootのverdictとしては確定している。そこでv1を基線に両verdictをoverlayし、次に掃くべき行を厳密に選び直す。

## 方法（`next_target_presweep_head1452_v2_20261116.py`）

- v1 census JSON（blob pin検証）を権威ある基線として読み込み、3つのactionable family（`00000000000000403800000008000000` / `00000000000000801202000040000000` / 76cのfamily）の全行について、legal候補bitの再列挙（`legal_candidates.py`・厳密整数Bareiss 4x4）と候補rootのD4 canonical hex再計算（foldproj1450由来のcanon関数のverbatim移植）を行った。
- cost-64h: raw batch 1-8（blob pin検証・pilot d6=3402 exact・capped 0）から64bitのverdict mapを再構築し、WIN7-D10 23bitがprereg receipts（git blob `5074a8a0...`）のd4_canonical_hex集合と完全一致することをassertした。
- cost-76c: v17 raw batch 1-10（fbt修復済みエンジン）から76bitのverdict mapを再構築した。WIN7-D10はbit 61/99のみ（bit 113はv16→v17でWIN→REFUTED反転、fbt飽和欠陥修復によるもの）。v16 10 batchとの一致は75/76、不一致はbit 113のみであることをassertした。
- claim v4（git blob `58b60b0c...`）のwinner_roots 3件とtransfers 15件、計18件のroot_canon hexを「真child|1<<bitのD4 canon」として再計算し、18/18が一致することをassertした。
- pending fold（64h prereg 20行・76cのWIN bitが閉じる行）を閉鎖予定行として除外し、残った行をcost→open数→hex順で再ランキングした。

## データ品質メモ（本セッション内で発見・解決、外部影響なし）

本スクリプトの未出版ドラフト版では、76c child定数のローカル転記誤り（`...809002...`を`...809092...`とする8石誤記。77e事故と同じ`9002→9092`パターン）により、claim v4のhexが「D4像として不正」という誤った疑いを生成していた。正しい6石child `00000000010000809002000001000000` で再計算したところ、claim hexesは18/18完全一致で、疑いは撤回された。ドラフトは一切出版しておらず、main上の成果物への影響はない。この経緯と18/18検証結果はcensus v2 JSONの`claim_hex_verification`フィールドに記録した。

## 結果

- **選定ターゲット（claim対象）**: `00000000000000801226000000000000`（cost 66、primary pure class-2 family `00000000000000403800000008000000` の残余最安行、demand c2=2、66 legal bits = 63 open + 3 confirmation bits [23, 100, 109]）。
  - bit 100のroot canon `00000000000000c89002000000100000` はcost-64h掃引（64h bit 103）でREFUTED-D10確定済みのためopen数はv1の64から63に減った。bits 23/109はv1 harvest由来REFUTED転送。3bitともcross-agreement確認として再実行する。
- **runner-up**: `00000000000000801282000040000000`（cost 64、overlay後55 open）。best-coverable familyに属するが、同familyの行 `00000000000000801202000040000400` がSTERILE（K0863・depth-10では永久閉鎖不能）のため、family全体の閉鎖には寄与しない。
- cross-checks: v1 bit-tableとのcanon一致16/16行全bit、prereg WIN canon一致23/23、verdict conflict 0、64h prereg閉鎖20行とfamily内検出の一致。
- 出力: `class2-lane-next-target-presweep-1452-v2-20261116.json`（2回実行でbyte-identical、git blob `67d6a5c192953b9bc95fd13b356e5aabeac2a12c`）。

## cost-66i claim v1 出版

選定行の掃引をclaim v1（`class2-lane-cost66i-inflight-20261116.json`、git blob `9eb3991abe1ee32d7296607990218a4958a571f0`）として出版した。engineはv17（blob `c132cc64...`、fbt修復済み・新規掃引に必須）、depth 10・cap 1e9・andclose 1・9 batch（8x8+2）・4並列・pilot d6=3402 exact制御。raw batchは本log出版時点で未着手。

## 解釈上の注意

探索計画の簿記のみであり、この時点で新しいverdictは1つも作られておらず、行は1つも閉じていない。WIN7-D10証明書は個々の7石rootのdepth-10内先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。**11x11空盤はUNKNOWNのまま**である。二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
