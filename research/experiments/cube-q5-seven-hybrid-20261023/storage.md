# 継続探索の保存方式と現在の再開手順

`graph.cpp` と `layers.hpp` は先の凍結版 `engine.cpp` / `disk.hpp` を拡張する。
元の版のmanifestを変更せず、新しい版は `manifest-graph.json` に記録する。

確定候補表を読み取り専用の層へ移し、新しい確定候補だけをRAMに置く。
各層の依存先fingerprint・行数・累積counterが一致しない読み込みは拒否する。
全局面表の独立検査ではないので、採用する勝敗は必ず通常の全AND/OR証明書を抽出し、
独立Bareiss検査器で検査する。索引監査は全key・label・witnessの一致だけを検査し、
そのlabel自体のゲーム理論的正しさは検査しない。

Q5HYB2は未確定局面ごとにkey・合法追加集合・正の有限PN/DN・子数を136 bytesで保存し、
子のkeyは再開時に再生成する。先のQ5HYB1も読み込める。未確定PN/DNは探索の作業量
推定にすぎず、P/N確定ラベルや証明書の葉には使わない。
`--promote` は最後の層から未確定treeだけを引き継ぎ、その確定候補を新しい層にする。
小盤面の連続探索とpromotionの最終展開数・証明書が一致することも確認した。

Q5IDX3は全key照合を維持しつつ、負の照会にBloom filterを使う。
filterは不在判定だけに使う。全35,412,458基礎行と最初の追加層34,736,179行の
key・label・witnessを各索引経由で全照合した（`base-index-audit.json`,
`overlay-index-audit.json`）。索引は再構築可能で、旧Q5IDX2も読める。
tree置換時にも、削除した未確定keyが不変の基礎層にないという情報を再計算終了まで
保持する。これにより大量の同じ負のディスク照会を避ける。

## 明示的に起動する継続controller

`run_campaign.py` は手動でのみ起動する。状態と最新の再開commandはprivateな
`scratch/cube-q5-seven-hybrid-20261023/run-state.json` に記録する。
checkpointを原子的に保存し、UNKNOWNなら凍結層へ移して次の段階へ進む。
中断後も同じ作業ディレクトリと状態ファイルから再開できる。
排他lockで重複起動を防ぎ、既存の凍結層は上書きしない。
再実行時の旧reportはattempt番号を付けて保存する。
根が確定したら独立検査し、検査成功後に証明書を圧縮する。
pushや通常のworkflowで自動起動しない。

最初は角を含む4石根 `{0,2,5,69}` を探索した。全二石調査後、
`central-four.txt` の `{3,169,173,339}` へ対象を移した。
この第四手は未解決三石 `{3,169,173}` の一つの候補であり、
全称の対称応手戦略を仮定していない。従来の確定候補も未確定treeも保持する。
終了済みreportと実行中reportを混同せず、根のUNKNOWNから勝敗を推測しない。

## 古いprivate cacheの可逆圧縮

`private-archives.json` は9個の古いraw `.memo` の現所在を記録する。
raw合計15,285,429,824 bytesをgzip合計3,385,245,672 bytesへ可逆圧縮した。
元rawのSHA-256・bytes、gzipのSHA-256・bytes、全展開での一致を記録した後にrawを除去した。
凍結済みの歴史manifestのraw pathは当時の値のままである。
再利用する場合は対応する `.memo.gz` を元pathへ展開し、raw hashを照合する。
稼働中の `balanced-final.memo` はrawのまま保持している。

復元例（既存rawへの上書きを避け、圧縮元も保持する）:

```sh
gzip -dk scratch/cube-q5-seven-frontier-20261022/dfs-2820k.memo.gz
sha256sum scratch/cube-q5-seven-frontier-20261022/dfs-2820k.memo
```

これら巨大privateファイルはGitには入れていない。
