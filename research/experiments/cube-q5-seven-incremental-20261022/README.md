# 7立方: 合法手の差分更新と候補点だけの幾何判定

2026-10-22。K0505の7立方探索を、前回の11,568,207候補ラベルのprivate
checkpointから再開するための実装・回帰・速度測定。ここにある速度測定は根を
閉じておらず、7立方の弱解決ではない。規則は5点共平面または共球面禁止。

## 実装

安全な占有集合をS、合法追加点集合をV(S)、合法手をpとすると、

```
V(S+p) = (V(S) - {p}) - union(completion(T+p): T in combinations(S,3))
```

である。以前からある四点組の禁止点はV(S)ですでに除かれているため、新しい
着手を含む四点組だけを調べればよい。候補が空になればその時点で打ち切れる。
正規化に使った48対称性の変換を合法点集合にも適用する。

`--direct`は各四点組について343点すべてのcompletionを作る代わりに、現在の
候補点だけで整数余因子と内積を評価する。これは候補の近似や枝刈りではない。
共平面・共球面の判定自体は従来と同じ。full再計算は入力根・証明書抽出に残る。

`--dfs`は子の合法手数が小さい順に完全探索する別の探索順序。通常は深さ重み付き
df-pnである。どちらも勝敗を閉じたときだけP/Nをmemoへ入れる。df-pnの有限の
作業量推定値はINF-1で飽和させ、証明済み結果のINFと混同しない。

Q5MEMO2のレイアウトを保って8,192行ずつ読み書きする。UNKNOWNは保存しない。
数百万行の再開ファイルは独立未検査の作業用候補であり、証明の既知葉には使わない。
採用する結果は従来の独立Bareiss検査器へ渡す通常のQ5CUBE証明書で確認する。

## 回帰

`regression.json`と`regression-direct.json`は各方式について次を確認した。

- 固定seedの3立方30履歴・7立方12履歴で、945回・839回の差分更新が全再計算と一致。
  各実着手後には正規化後の合法集合も全再計算と照合。
- 既知3立方全20二石軌道をdf-pnとmobility DFSの両方でPと判定し、各証明書を
  別実装の5×5 Bareiss行列式検査器で独立検査。
- 新実装が書いたcheckpointを旧実装で読み、その旧実装が書いたcheckpointを
  新実装で読み戻す。全20根を追加展開なしで再利用。
- 幾何cache上限1での正しさ、bit128を越える7立方終端、予算0のUNKNOWNを確認。

これは全7立方局面の網羅検査ではない。

## 同一seedからの2万展開

入力は `target.txt` の五石根 `{0,2,5,26,69}`。前回の `descent-1m.memo` を別々に
コピーして旧weighted df-pn、差分更新、候補点直接判定を比較した。3件ともUNKNOWN、
候補memoは11,588,199行、累積展開数10,590,000。候補点直接判定と差分更新は
ともに3,991,037四点組、空候補への早期終了4,408回だった。

旧実装の全体時間は24.071秒、差分更新は7.210秒（探索1.71839秒）。候補点直接判定は
探索0.565399秒、全体18.314秒。この最後の測定は大きな探索2processと同時実行し、
復元だけで16.5076秒かかっている。全体時間で直接判定の優劣を決めない。
これは単発測定であり、一般的な高速化率ではない。入力と出力は
`benchmark-*.jsonl`、bashの時間と対応付けは `timing.json` を参照。

最初の2測定は`/tmp/q7-incremental`と従来の`/tmp/q7-dfpn-weighted`で実行した。
現在のengine.cppには、その後にDFS・直接判定・出力欄を追加した。通常df-pnと
差分更新の計算順序は同じ。実行バイナリのhashはmanifestに記録する。

## 再現

repo rootから:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-incremental-20261022/engine.cpp -o /tmp/q7-incremental-repro
g++ -O3 -std=c++17 research/experiments/cube-q5-seven-frontier-20261022/dfpn.cpp -o /tmp/q7-legacy-repro
g++ -O3 -std=c++17 research/experiments/cube-q5-seven-frontier-20261022/verify.cpp -o /tmp/q7-verifier-repro
python research/experiments/cube-q5-seven-incremental-20261022/regression.py /tmp/q7-incremental-repro /tmp/q7-legacy-repro /tmp/q7-verifier-repro
python research/experiments/cube-q5-seven-incremental-20261022/regression.py /tmp/q7-incremental-repro /tmp/q7-legacy-repro /tmp/q7-verifier-repro --direct
```

前回のprivate checkpointを保持している同じworkspaceでは、元ファイルを残して
作業用コピーから再開する。存在しないpathなら空memoから始まるので注意。

```sh
cp scratch/cube-q5-seven-frontier-20261022/descent-1m.memo scratch/q7-incremental-repro.memo
/tmp/q7-incremental-repro --batch 7 20000 3000000 /tmp/q7-inc-repro research/experiments/cube-q5-seven-incremental-20261022/target.txt scratch/q7-incremental-repro.memo --direct
```

大きなcheckpointはGitへ入れない。元checkpointのhashと再構築手順は前回実験の
manifest・READMEを参照。入力根は今回も未確定のため、速度測定から勝敗は従わない。
