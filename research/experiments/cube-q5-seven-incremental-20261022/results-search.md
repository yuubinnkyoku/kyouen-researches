# 差分更新版による追加探索の終了記録

2026-10-22。対象は全て五石根 `{0,2,5,26,69}`。以下の各予算を使い切り、
いずれもUNKNOWNだった。三石根69、二石根 `{0,5}`、空盤の勝敗は確定していない。

|方式|追加展開|探索秒|終了時候補memo行数|
|---|---:|---:|---:|
|差分更新・weighted df-pn|5,000,000|355.774|16,588,190|
|候補点直接判定・weighted df-pn|10,000,000|147.750|26,588,183|
|候補点直接判定・mobility DFS|500,000|18.2487|27,264,695|

これらは直列に同じcheckpointを引き継いだ。最初の入力は前回の11,568,207行から
差分更新の2万展開を加えた11,588,199行。最終headerの累積展開数26,090,000は
この系譜のcounterであり、別分岐の実験を合算した総実行数ではない。

別分岐では、同じ11,588,199行からmobility DFSを100万展開し、12,938,068行で
UNKNOWNになった。その中の18石終端は独立証明書に抽出して検査した
（`terminal18.md`）。この分岐は最終checkpointへmergeしていない。

`checkpoint-profile-dfpn.json`と`checkpoint-profile-direct.json`は500万・1000万
終了時のラベル分布を独立未検査の候補として集計した。少石側は6石Nが9件、7石Pが
9件のままで、三石・四石・五石根を新たに閉じたという成果ではない。多数の終盤局面を
処理できても、今回の上位局面の未確定性は解消しなかった。

## 信頼範囲と保存

27,264,695行全体は独立未検査。UNKNOWNをP/Nと解釈しない。今回新たに独立検査
した7立方の結論は明示的18石集合の安全性・極大性である。探索の高速化と既知盤回帰は
最初のREADME、独立証明はterminal18.mdに分けて記録した。

private checkpointは`manifest-search.json`にworkspace相対path・byte数・SHA-256・
headerを記録した。最終ファイルは
`scratch/cube-q5-seven-incremental-20261022/mobility-direct-500k.memo`。
これを変更せず、別pathへコピーして次の探索を再開できる。

```sh
cp scratch/cube-q5-seven-incremental-20261022/mobility-direct-500k.memo scratch/q7-next.memo
/tmp/q7-incremental-repro --batch 7 1000000 1000000 /tmp/q7-next research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-next.memo --direct --dfs
```

元seedからこの系譜を再構築する場合は、前回実験の手順で`descent-1m.memo`を
再構築した後に、次の順で実行する。各段階の候補行数と結果は保存済みJSONLで照合する。
バイナリのビルド手順はREADMEを参照。

```sh
cp scratch/cube-q5-seven-frontier-20261022/descent-1m.memo scratch/q7-chain.memo
/tmp/q7-incremental-repro --batch 7 20000 3000000 /tmp/q7-chain research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-chain.memo
/tmp/q7-incremental-repro --batch 7 5000000 3000000 /tmp/q7-chain research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-chain.memo
/tmp/q7-incremental-repro --batch 7 10000000 1000000 /tmp/q7-chain research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-chain.memo --direct
/tmp/q7-incremental-repro --batch 7 500000 1000000 /tmp/q7-chain research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-chain.memo --direct --dfs
```
