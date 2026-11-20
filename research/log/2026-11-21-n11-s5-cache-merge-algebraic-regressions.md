# N11 S5 worker-cache merge の代数的回帰検査（2026-11-21）

## 開始時点

最新mainの `AGENTS.md` と `research/knowledge/README.md` を確認し、既存のS5 merge実装・quarantine policy・registry・13系統の敵対的回帰記録を読み直した。既存のmerge実装は変更せず、既にCIで実行される `dfpn_s5_merge_test.sh` の検査範囲だけを広げる。

固定した既存入力:

- merge実装: Git blob `5658cab3492c3df7f453ed7dbc39532374ed5e56`
- quarantine policy: Git blob `0f38efc3720d321b7f43e2d0514eea0f8114e99c`
- quarantine registry: Git blob `6a320237545874ddd841c90be095cccccc46249d`
- 変更前テスト: Git blob `dafcd8ef64f306a4c4241895b4ea34e579c87508`

## 追加した性質検査

3 workerのcacheに、同じverdictで重複する4鍵を分散させた。

| 鍵 | worker側の記録 | 期待値 |
|---|---|---|
| A | LOSS nodes 13, 7（baseにもLOSS nodes 10） | LOSS / 7 |
| B | WIN nodes 20, 9 | WIN / 9 |
| C | LOSS nodes 30, 11 | LOSS / 11 |
| D | WIN nodes 15, 6 | WIN / 6 |

このfixtureについて次を検査する。

1. 3 workerの入力順6通りすべてで、同じ4鍵・最小node数・出力bytesになる（可換性・順序独立性）。
2. 出力済みcacheを再び入力へ含めてmergeしてもbytesが変わらない（冪等性）。
3. `merge(merge(base, x, y), z)` と `merge(base, x, y, z)` の出力bytesが一致する（結合性）。

異なるverdictの衝突は従来どおり拒否対象であり、これらの性質は**整合するWIN/LOSS記録の集合上だけ**で検査する。node数は同一verdictの重複記録に対する最小値選択であり、勝敗の根拠ではない。

## 実行結果

Proxmox LXC `pve-hp-aio:204`（Debian 13・Python 3.13.5）で、GitHub mainから取得した4入力のGit blob SHA-1を照合してから実行した。root filesystemは7.8 GiB中7.3 GiB使用・空き143 MiBだったため、実験木と一時ファイルを `/dev/shm`（7.8 GiB中6.6 GiB空き）へ置き、root filesystemへの試験書込みを避けた。

- 既存13系統: 全PASS
- 追加の3-worker全6順列: byte-identical
- 再merge: byte-idempotent
- 段階mergeと一括merge: byte-identical
- 最終表示: `MERGE_GUARD_OK`
- 終了コード: 0

変更後テストscriptは10,991 bytes、Git blob SHA-1 `1740db7a0bf3b481d6f667042b00b1fde7cff448`、SHA-256 `621e2bca68875f4ed8e0551b6d9ddcd3c29c111dd8de8a2a9aeee742eb6cda48`。GitHubからのfetch-backもbytes完全一致。

## 解釈境界

これはmerge演算の実装回帰検査であり、cacheの実件数・WIN/LOSS verdict・証明書・manifest coverageを増やさない。merge実装・cache・quarantine registryは変更していない。新しいDFPN探索、証明書抽出、receipt fold、S6行閉鎖は行っていない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのまま。
