# 物理SSOT移行のprovenance

開始main：`48fa9f78f0933a9f20485f4f2be16d88a4bce232`（2026-10-04）。
[path対応表](paths.tsv)のhistorical_pathは当時の配置、current_pathは移動後の所在です。
これは移行履歴の索引で、現在の知識・status・関係を維持する管理体系ではありません。
現在知識の唯一の正本は[knowledge/items](../../knowledge/README.md)です。

## 当時のpathとhash

以下の9ファイルは開始mainのGit blobをそのまま保存しています。当時のpathやSHA256を新path・現在のsource hashへ無条件に書き換えていません。
同じ内容のpath/hashが合致するかを当時のcommitで監査できます。現在のファイルを開く際はpath対応表を使用してください。
移動・参照修正・歴史資料bannerによって現在のsource byte列が変わった場合、当時のhashは現在ファイルのhashを保証しません。

- [SOURCE_SHA256SUMS.txt](../source-snapshot-2026-09/SOURCE_SHA256SUMS.txt)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [SHA256SUMS.txt](../../../release-assets/SHA256SUMS.txt)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [knowledge-open-freshness-main-2026-10-04.json](../audits/knowledge-open-freshness-main-2026-10-04.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [progress-integration-2026-09-28-audit.json](../audits/progress-integration-2026-09-28-audit.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [round26_original_scope_index.json](../../experiments/original-claims/output/round26_original_scope_index.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [round4_b501_prand.json](../../experiments/original-claims/output/round4_b501_prand.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [round9_n7_n8_overlap.json](../../experiments/original-claims/output/round9_n7_n8_overlap.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [saturation_20261003_verified.json](../../experiments/saturation/output/saturation_20261003_verified.json)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。
- [SHA256SUMS.txt](../../../results/9x9/factorial/effect-heterogeneity/SHA256SUMS.txt)：開始mainに存在した監査・source checksum。path/hashと監査metadataは当時のsnapshot。

round26のoriginal_scope_indexは原文と当時の行番号・hash・preferred_reportを保存した歴史的監査です。
logの実行標準出力、archive内の旧引き継ぎ・未完了コードにある旧pathも当時の記録です。
このような記録は実行pathやMarkdownリンクとして扱いません。knowledgeのartifactsと現在のrunner/workflow/linkは新pathを参照します。

saturation回帰は当時のhash receiptを保存し、再実行のsource hashを一時出力へ記録します。
全ての数学的データを比較し、時刻・source hashと同じ根拠ファイルの移動先文字列だけを比較時に正規化します。
未追跡の大きなcache・build補助物はrepo管理外のscratch/ssot-local-cacheへ移して、legacy directoryの実在を残していません。

削除は空dump・一時的な編集/debug片・3個の完全一致重複に限定しています。証人・独立replication・実行ごとのreceipt・唯一の出力は保持しています。
