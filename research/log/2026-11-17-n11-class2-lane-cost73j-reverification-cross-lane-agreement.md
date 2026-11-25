# 2026-11-17 長期レーン: cost73j証明書16本のBigInt再検証2件のcross-lane完全一致（合意照合・11×11はUNKNOWNのまま）

## 何をしたか

cost73j sweep の WIN7-D10証明書16本（class2-lane-cost73j-certificates、証明書自体は並走レーンが
mainに出版済み）について、**互いに独立に実行された2件のBigInt bytes再検証**を機械比較し、
完全一致を確認した。重複出版は行わず、合意照合記録（agreement record）のみを反映した
（cost60/65n系のcross-lane agreement record の先例に倣う）。

1. **本レーン（Lane B）の独立再検証（出版は見送り）**: 並走が02:41Zに同一成果を出版済みと
   push直前に判明したため、本レーンが別途計算した再検証JSON（script
   `reverify_cost73j_certificates_bigint_20261117.py` を自前実装、pin commit
   `6758f03e` のband 77ファイルをraw CDNで別途ミラー、BigInt厳密4x4判定・sub-root全件・
   terminal [13,17]・rootcheck・sidecar照合、2回実行でbyte-identical、
   md5 `e4329bd0369b2e8bec79277bc8ed27bf`）は**出版せず**、同一パス名での上書きを回避した
   （3ファイルとも並走版と同名だったため）。
2. **合意照合**: mainの並走版JSON（`class2-lane-cost73j-certificates-bigint-`
   `independent-reverification-20261117.json`、pin commit `8803a3b0` 側のミラーで実施）と
   本レーン版JSONを、`check_cost73j_reverification_cross_lane_agreement_20261117.py` で
   **16 entries × 36共通スカラー字段 + 14分割証明書のpart pin（pinned_blob_sha/bytes）を
   機械比較した結果: field checks 632、mismatch 0、verdict AGREEMENT**。
   - 両レーンとも: verifier 16/16 PASS、record_rows総計 726,778、extraction_nodes 166,238,087、
     sub-roots 58/根（rootcheck・sidecar含む全字段一致）、joined blob sha 16/16 一致、
     parts pin 28/28（14分割×2part）+ whole 2本のbytes/md5/sha256/git_blob_sha 全一致。
   - 両レーンのpin commit（`6758f03e` vs `8803a3b0`）が異なること自体が、band内容が
     両時点でblobレベル同一（pins全一致）であることの追加証拠になっている。
3. **独立検証可能性の状態**: これにより cost73j の16証明書は「抽出レーンとは別の2計算環境で
   bytes再検証が合意」した状態。65n（26 bit）と同様に、証明書は独立検証可能な形でmainにある。

## 解釈上の注意（interpretation guard）

- WIN7-D10証明書は**個別7石rootのdepth-10内先手勝ちのみ**を証明する。16根の被覆は
  cost73j manifestの簿記であり、**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 の勝敗はいずれもUNKNOWNのまま**。REFUTED-D10はLOSS証明ではない。
- cost73iの証明書12本は未出版（並走レーンの出版待ち）。cost73kは別セッションがclaim中
  （着手禁止）。76c bit61は並走がguard出版済み・抽出待ち（着手禁止）。

## レジューム

1. **cost73i/73j sweepの完全独立再実行検証**（本レーン、65n precedent踏襲）: 73iの
   73bit全バッチrerunはnode-exact一致済み。検証フェーズのraw batch9ファイル名バグ
   （`-confirmation-` 接尾辞）を修正し、73iのrerun JSONL 9本を再利用、73j 9バッチを再計算中。
   完了後、verification JSONとともに1-2コミットで出版予定（出版前にmain再取得・衝突確認必須）。
2. cost73k claimレーンのsweep終了後、census v7の7 confirmation bits（bit 14 WIN含むと
   concurrent-recordに記録）の整合確認が本レーンの次の検証対象候補。
