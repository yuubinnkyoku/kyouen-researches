# 共円ゲーム研究の入口

現在成立する命題、計算結果、反証、未解決問題、検証境界の唯一の正本は[knowledge/items](knowledge/README.md)です。
K番号とaliasは正本を指す識別子であり、旧資料のラベルを現在のstatusとして採用しません。

| 目的 | 所在 |
|---|---|
| 現在の結論・未解決・検証境界 | [knowledge](knowledge/README.md) |
| 再現手順・コード・入力・出力・実行条件 | [experiments](experiments/README.md) |
| 発見順・判断・失敗・引き継ぎ | [log](log/README.md) |
| 旧計画・supersededなまとめ・当時の監査 | [archive](archive/README.md) |
| 現在有効な使い方・仕様・解説 | [docs](../docs/README.md) |
| 公開・横断集計のmachine-readable result | [results](../results/README.md) |

experiment・log・archiveの数学的記述は当時の一次資料です。現在の結論の正本として並行更新しません。
共有solver/verifierはcpp・scripts・rustに置き、実験ごとに複製しません。
構造移行の経緯は[MIGRATION](MIGRATION.md)を参照してください。
