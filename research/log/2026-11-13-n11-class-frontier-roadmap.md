# 2026-11-13 n11 S2 {59,60}: 未解決blocker類2・4の最新フロンティア・ロードマップ（証明書優先順位と実効ワークリスト削減）

長期レーン。main = `2da40f42`（class-2 batch1/batch1b 証明書込み・並走のclass-2監査シリーズと主題独立）。
AGENTS.md・research/knowledge/README.md・K0783・milestone-5実験README・
ms5-s7-reuse実験の全verified JSONとrefutation文書を確認してから着手した。

## 目的

blocker類1 {5,115} は条件付き閉鎖済みで、残るは類2 {27,93} と類4 {23,31,89,97}。
class-2 レーンは現在4番目のS5候補 `00000000000000003802000008000000` を消化中だが、
**類2の次の候補と類4の攻略順序**について、全公開レシートを織り込んだ最新の
優先順位表が存在しなかった（s5-remaining-after-reuse.json はbatch以前の古い状況）。
本セッションで最新のフロンティア会計を作成した。

## 手法（bookkeepingのみ・新規証明なし）

- 入力: `win7-reuse-hits.csv.gz`（498親）+ 全12個のverified JSONの**WIN7計67根**の
  covers()（D4正準6部分集合）+ 反証済みLOSS6鍵3個（`...80920200040000...`・
  `...3800004008...0008`・`...80520200000002000`）+ `s5-remaining-after-reuse.csv.gz` の
  classes列 + `s5-s6-remaining-incidences.csv.gz`（14,558行）。
- 実行はsandbox内の等価なTypeScript実装（gzip展開は自作raw-DEFLATE実装）。
  repo用に同一論理の `scripts/audit_class_frontier.py` を同梱した
  （outputsはTS実行分である点を明記。制御値はscript内にassertとして固定）。
- **制御（全て最新の公開監査と一致）**: incidences 14,558・hits 498・classes 186・
  manifest 7,867・solved∩manifest **638**（batch1b監査の635+3と整合）・
  残S5 **177**・残unique S6 **7,208**・残cost **565,500**・
  現行class-2 TARGETの残り **32**・反証pruned S5 8。

## 結果

1. **実効ワークリスト削減（24.8%）**: 残7,208 S6 orbitのうち **1,783 orbitは
   類1のS5候補からのみ要求される**（cost 139,993相当）。類1 blocker {5,115} は
   既に条件付き閉鎖済み（class1-blocker-closure.md）なので、
   **未解決blocker（類2・4）に必要な実効ワークリストは 5,425 orbit / 425,507 S7辺**
   に縮む。これら1,783 orbitは類2・4の閉鎖には不要で後回しにできる
   （全blocker閉鎖後にS2判定正しさの検証で使う分はそのまま残る）。
2. **証明書の需要側ランク付け**: 各残S6について「それを子に持つ残りS5候補数」
   （類別）を計数。open-only需要ヒストグラム: c2=2,c4=0: 1,356 / c2=0,c4=2: 3,078 /
   c2=0,c4=1: 531 / c2=1,c4=0: 279 / c2=2,c4=2: **66**（両類から二重に需要される
   最優先証明書ターゲット）など。
3. **類2の次候補**: 現行TARGET（32残り）の次は
   `00000000000000809082000000000000`（37/2,507）→ `00000000000000809102000000000000`
   （40/2,850）→ `00000000000000803202000000000000`（41/2,776）。
   S5候補の多くは反証（SECOND_WIN）で死ぬ可能性があるため、順位は
   残数ベースのヒューリスティックである（既存レーン規約と同じ・証明ではない）。
4. **類4の最良候補**: `00000000020000003800000080000000`（43 S6 / 3,391辺）。
   その43個のS6子は多くが **c4需要3**（1枚のWIN7証明書で類4候補3個を同時に
   前進させる）を持つ。全43子の個別リスト（cost・需要付き）は
   `output/class-frontier-top-candidates-s6.csv` 参照。

## 成果物

- `scripts/audit_class_frontier.py` — 上記を再計算するsnapshot監査（assert込み）
- `output/class-frontier-roadmap.json` — 要約とスケープ
- `output/class-frontier-s5-ranking.csv` — 残り177 S5全件の順位表
- `output/class-frontier-top-candidates-s6.csv` — 類4最良候補43子 + 類2現行TARGET 32子の詳細

## スコープ

公開レシート（WIN7監査記録・verified JSON・refutation文書）を前提とした
ブックキーピングであり、新しいverdictは1つも生成・検証していない。
**11×11空盤・二石root {49,60}・S2 {59,60} は全て UNKNOWN のまま。**
