# 2026-11-17 長期レーン: cost73i/73j sweepの完全独立再実行検証（両73bit node-exact一致・証明書出版前の品質ゲート・11×11はUNKNOWNのまま）

## 何をしたか

cost73i・cost73j 両sweep（並走レーン出版済み、blob pin付きraw batch 18件+audit JSON 2件）を、
**本レーン独自のスクリプトで全73bit×9バッチ完全再実行**し、出版記録との node-exact 比較を行った
（65n precedent 踏襲、証明書抽出前の決定制御の品質ゲート）。

1. **スクリプト**: `verify_cost73ij_sweep_independent_rerun_20261117.py`。engine は main の
   `class4_child1_runner_v17.ts`（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59` を実行時照合）、
   depth 10 / cap 1e9 / andclose 1、73i child `00000000000000403800400008000000`・
   73j child `00000000000000403800000408000000`。各バッチ9bit、4 worker 並列。
   出版raw batch 18件の git blob sha をピン照合（20/20 match、audit JSON 2件含む）。
2. **結果**: **MISMATCHES 0、checks 215**。
   - 73i: WIN7-D10 12 bits `[1,9,11,18,29,38,54,82,97,100,110,111]`、REFUTED 61、capped 0、
     candidate nodes **131,402,821**（pilot 3,402×9 含め出版auditと完全一致）。
   - 73j: WIN7-D10 16 bits `[0,1,6,29,44,49,52,69,74,82,87,91,98,100,110,118]`、REFUTED 57、
     capped 0、candidate nodes **168,445,380**（同一致）。
   - 各bitの loss/nodes/capped/terminalStoneRange/andclose 全字段が出版rawと1つ残らず一致。
     terminalStoneRange は両targetとも [13,17]。
3. **運用上の修正（実験事実として記録）**: 初回実行は検証フェーズで、batch9 の出版rawファイル名が
   `*-raw-batch9-confirmation-20261117.jsonl`（`-confirmation-` 接尾辞）であるのに対し
   `*-raw-batch9-20261117.jsonl` を参照して FileNotFoundError でクラッシュした。**バグは検証
   フェーズのみ**で、ThreadPoolExecutor の結果は全18バッチ計算後に失われた。再実行では
   (a) パス構築を修正、(b) 73iの rerun JSONL 9本（同一スクリプトの同一セッション内計算で
   クラッシュ前に着地済み）を再利用し、73j の9バッチのみ再計算した
   （`reused_in_session_rerun_batches` に透明に記録）。
4. **独立検証可能性**: これにより 73i/73j 両sweepの全bit verdicts と node counts が
   「出版レーンとは別環境での完全再実行」で確定。73j証明書16本は同日、2レーンの独立BigInt
   bytes再検証でも完全一致（別記の cross-lane agreement record 参照）。

## 解釈上の注意（interpretation guard）

- WIN7-D10証明書は**個別7石rootのdepth-10内先手勝ちのみ**を証明する。REFUTED-D10は
  LOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 の
  勝敗はいずれもUNKNOWNのまま**。solved数・head 1472はmanifest被覆の簿記である。
- 73i証明書12本は未出版（並走レーンの出版待ち・着手禁止）。73kは別セッションclaim中。

## レジューム

1. 73i証明書が並走レーンから出版された後、65n/73j と同様の独立BigInt bytes再検証が
   本レーンの次の候補（出版前にmain再取得・同名衝突確認必須）。
2. 73k claimレーンのraw batch出版後、本rerunスクリプトのバッチ構成を差し替えて
   同様の独立再実行検証が可能（batch9の `-confirmation-` 命名規約に注意）。
