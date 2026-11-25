# 4石根への追加探索と再開データ

2026-10-23。五石N・六石Pの独立証明はfive-results.mdに記録した。
その後、確定Pから1石取り除いたN親の再利用を9石以下に適用し、4石根を探索した。

|根|追加展開|結果|終了理由|
|---|---:|---|---|
|`{0,2,5,69}`|2,000,000|UNKNOWN|node-limit|
|`{0,5,26,69}`|2,000,000|UNKNOWN|node-limit|
|`{0,2,5,69}`|4,890,897|UNKNOWN|未確定tree100万局面の上限|

これらは三石根 `{0,5,69}` 配下の候補である。4石根を閉じておらず、三石根、
二石根、空盤も未確定。今回確定した五石根を再びUNKNOWNへ戻すという意味ではない。

## 保存範囲

最終private checkpointは
`scratch/cube-q5-seven-balanced-20261023/balanced-final.memo`。
35,412,458候補行、系譜上の累積展開counter36,288,126。全ラベルは独立未検査。
P/Nが閉じた候補だけを保存し、UNKNOWNと未確定treeのproof numberは保存しない。
tree上限に達した最後の100万未確定局面は、次回にそのまま復元されるわけではない。
`manifest-frontier.json`にbyte数・SHA-256・header・信頼範囲を記録した。

`frontier-final.json`は候補ラベルの集計であり、独立検査済み全局面表ではない。
5石Nが23件、6石Pが4件、6石Nが165件を含むが、この全てを個別検査したわけではない。
新たに採用した5石N・6石PはK0517の全証明書、6石N・7石PはK0506の全証明書による。

旧来の全盤面completion型検査器でも五石証明の参照実行を始めたが、差分更新型の
独立Bareiss検査器で五石・六石両方の全証明書が完了したため、重複する長時間の
参照実行は結果未取得のまま停止した。これを検査通過として数えない。
`legacy-full-status.json`に記録した。新検査器の幾何は探索器の余因子法と独立である。

## 次回の再開

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-balanced-20261023/retro.cpp -o /tmp/q7-retro-repro
cp scratch/cube-q5-seven-balanced-20261023/balanced-final.memo scratch/q7-balanced-next.memo
/tmp/q7-retro-repro --batch 7 1000000 1000000 /tmp/q7-next research/experiments/cube-q5-seven-balanced-20261023/four-one.txt scratch/q7-balanced-next.memo --base 4 --tree 2000000 --direct --reverse 9
```

元seedからの系譜を再現する場合、six-results.md・five-results.mdの手順の後、
同じ作業用checkpointでfour-targets.txtを各200万展開、four-one.txtを500万予算で
実行する。最後のtree上限は100万、先の2件は200万とする。未確定treeは根ごとに
消去する。入力・出力は保存済みJSONLと照合する。
