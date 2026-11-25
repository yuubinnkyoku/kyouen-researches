# 7立方の探索重み変更で得た6石N・7石P

2026-10-23。前回の27,264,695行のprivate checkpointから再開した。
前回の深さprior `(344)^(17-k)` は浅い枝の切替えを強く抑制していた。
これを `4^(17-k)` に緩めた100万展開では未確定treeの最大サイズが211,624に
増え、五石根はUNKNOWNだったが、下記の新たな部分証明を得た。
priorは作業順序だけに使い、勝敗の判定には使わない。

点番号は`(x*7+y)*7+z`。

- `{7,10,28,42,49,51}` はN。証明書12,404局面・16,437辺。
- `{7,9,49,52,196,244,294}` はP。証明書12,403局面・16,436辺。

両者は旧来の独立Bareiss検査器で、それぞれ169,495,593回・169,490,508回の
整数行列式評価により確認した。最大15石までの全AND/OR条件を検査している。

## P子からの逆向き再利用

安全なP局面Tから任意の1石pを取り除いた局面は、pを戻してPへ進めるのでN。
正規化を挟んでも立方体対称性は合法性を保つ。`lift.cpp`は7石P証明に6石Nの
根を1件加えるだけで、7つの6石親の証明書を作る。7件全てを既存の独立検査器で
検査した。根の一覧は`lifted-six-roots.jsonl`、検査結果は`lifted-six-verified.json`。
証明書の子を既知葉として省略せず、各証明書に全12,403子孫を含めた。

`retro.cpp`は石数上限付きでこの操作を探索中にも適用する。`--reverse 9`は
9石以下の確定Pからのみ逆向き親を追加する資源制限であり、他の局面をP/Nと
決める条件ではない。既知3立方20根と逆向きに得た1石親4軌道を独立検査した。

## 再現

repo rootから:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-balanced-20261023/engine.cpp -o /tmp/q7-balanced-repro
g++ -O3 -std=c++17 research/experiments/cube-q5-seven-balanced-20261023/lift.cpp -o /tmp/q7-lift-repro
g++ -O3 -std=c++17 research/experiments/cube-q5-seven-frontier-20261022/verify.cpp -o /tmp/q7-old-verifier-repro
gzip -dc research/experiments/cube-q5-seven-balanced-20261023/seven-p.cert.gz > /tmp/q7-seven-p-repro.cert
/tmp/q7-old-verifier-repro /tmp/q7-seven-p-repro.cert
/tmp/q7-lift-repro /tmp/q7-seven-p-repro.cert /tmp/q7-parent-repro
```

探索を再現する場合、前回のcheckpointを作業用pathへコピーしてから:

```sh
/tmp/q7-balanced-repro --batch 7 1000000 1000000 /tmp/q7-base4-repro research/experiments/cube-q5-seven-balanced-20261023/target.txt scratch/q7-base4-repro.memo --base 4 --direct
```

`scratch/q7-base4-repro.memo`への事前コピー元は前回manifestの
`scratch/cube-q5-seven-incremental-20261022/mobility-direct-500k.memo`。
checkpoint全体は独立未検査。上記の有限部分証明だけを独立検査した。
この記録は7立方の空盤の勝敗証明ではない。
