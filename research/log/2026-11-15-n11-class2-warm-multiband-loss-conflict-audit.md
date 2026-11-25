# 2026-11-15 class2 warm multiband 35証明書のWIN/LOSS衝突監査

## 監査対象

監査時のmainは `3631e7ba84b4db97329e4b7de670dde95ce2c814`。その後の `52fd92c12c27fe02d94d76fe58964b47d4a6fa73` はseven-row q9実験READMEのみの変更で、今回の11×11入力には影響しないことをcommit diffで確認した。

warm multiband batchの35個のWIN7 rootを、同じS2再利用実験の全 `*-verified.json`（17 manifest）と、中央49条件付き計画のLOSS7親持ち上げmanifest、既知LOSS候補表に照合した。D4変換は同実験の `audit_published_candidates.py` にある8座標変換をそのまま用い、128-bit整数で正規化した。浮動小数点は使用していない。

## 結果

- warm multiband: 35 records、35 distinct roots、35 distinct D4 orbit、すべて7石。
- 既存の17 verified manifests: 277 records（WIN7 77、LOSS7 200）。各verdict内で重複D4 orbitなし、WIN7/LOSS7間の交差も0。
- warm 35 rootsと既存WIN7 77 orbitの交差: **0**。
- warm 35 rootsと既存LOSS7 200 orbitの交差: **0**。
- 中央49 terminal LOSS7 parent-lift manifest: 274 keys、274 D4 orbit。warmとの交差: **0**。
- `ms5_s7_knownloss_candidates.csv`: category=1の396行、396 D4 orbit。warmとの交差: **0**。これは公開候補分類表であり、396件を独立LOSS7証明書とは数えない。
- 既存LOSS7 200 + central parent-lift 274 + category-1 candidate 396の合計870 D4 orbitは相互に重複しなかった。

したがって、今回の35 WIN7 rootは、列挙した既存WIN7/LOSS7証明・親持ち上げ・既知LOSS候補との間に、完全一致だけでなくD4対称同値の衝突もない。35件内部も互いに別のD4 orbitである。

## 限界

これは公開済みmanifestと候補表に対する範囲限定の衝突監査である。全raw verdict cache、非公開worker cache、リポジトリ内の全証明書ファイルを走査したものではない。従って「全体で衝突なし」とは主張しない。warm multiband各証明書の戦略内容の正しさは、元のwarm multiband記録にあるBigInt独立検証の範囲に依存する。本監査はその再検証ではない。

S6 frontierの計数は変更しない。manifest被覆の増加を勝敗確定へ読み替えない。

## 再現

- `scripts/audit_warm_multiband_loss_conflicts_20261115.mjs`
- `output/warm-multiband-loss-conflict-audit-20261115.json`

実行: `node scripts/audit_warm_multiband_loss_conflicts_20261115.mjs`（repo rootからの通常Node環境）。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、class 4はすべて UNKNOWN。**


## 追補: 知識項目のメタデータ修復

K0783のfront matterで、過去の追記により `evidence` の後ろへ置かれていた7件のartifact項目を `artifacts` 配列へ戻し、`scope`・`evidence` の前に整理した。今回追加した3 artifactも同じ配列内に置いた。これは証明内容やfrontier数を変更するものではなく、知識索引の構造を正す修復である。知識整合性検査はGitHub Actions待ちで、合格は未確認。
