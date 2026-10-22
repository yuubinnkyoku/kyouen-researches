# 7立方の18石極大安全集合

2026-10-22。mobility順の100万展開中に見つかった候補を、checkpointを使わず
1局面の証明書に作り直し、別実装のBareiss行列式検査器で独立検査した。

点番号は`(x*7+y)*7+z`。占有点は

```
1 7 8 42 58 62 68 130 139 184 218 243 245 263 264 289 294 300
```

である。全5点組が共平面・共球面にならず、残る325点はどれも合法に追加できない。
`terminal18-verified.json`は1局面・0辺・1終端、1,037,340回の5×5整数行列式評価を
記録する。従って最大安全石数は少なくとも18。最大値18や空盤の勝敗は未証明。

## 再現

前のREADMEのコンパイル後、存在しない新しいcheckpoint名を使う:

```sh
/tmp/q7-incremental-repro --batch 7 1 10000 /tmp/q7-terminal18-repro research/experiments/cube-q5-seven-incremental-20261022/terminal18-root.txt /tmp/q7-terminal18-fresh.memo --direct --validate
gzip -dc research/experiments/cube-q5-seven-incremental-20261022/terminal18.cert.gz > /tmp/q7-terminal18-repro.cert
/tmp/q7-verifier-repro /tmp/q7-terminal18-repro.cert
```

証明書の検査には探索器もprivate checkpointも不要。

候補を発見した`mobility-dfs.jsonl`は五石根 `{0,2,5,26,69}` を100万展開して
UNKNOWN。`checkpoint-profile-dfs.json`の18石P候補の最小maskを取り出した。
この大きなcheckpoint全体のラベルを独立検査したという意味ではない。
