# 11×11 reply27: 次のdual-tight S4 classを段階的に探索

## 結果

開始main `1739ddf2f9a5ec411ad5aeb0a2d8f9259951597c` で、最新のS5 cache、fail-closed隔離registry、raw replay履歴、保存済みS6/S7境界を再確認した。対象はS4 `(1188950301626859520,536870912)`、coverage `{55,65,100,108}`。独立Board幾何でcanonical S5子109局面を再生成し、保存cacheとの境界はLOSS 11 / WIN 0 / UNKNOWN 98だった。

未確定子のうちlegal数88と89の3局面を選んだ。各局面を2M nodesで先にprobeし、全てUNKNOWNだった。各々についてraw履歴とS6/S7保存成果を再監査してから15M nodesまで再試行し、3局面すべてで直接exact LOSSを得た。

| S5局面 | legal手数 | 2M probe | 15M probe |
|---|---:|---:|---:|
| `(3494793310840553472,536870912)` | 88 | UNKNOWN, 2,000,000 nodes | LOSS, 3,981,449 nodes |
| `(1188950301626859520,536936448)` | 89 | UNKNOWN, 2,000,000 nodes | LOSS, 2,335,333 nodes |
| `(1189513251580280832,536870912)` | 89 | UNKNOWN, 2,000,000 nodes | LOSS, 2,457,938 nodes |

合計6 runs、3 distinct局面、14,774,720 nodes（うちexact判定に使った15M retryは8,774,720 nodes）。全結果は元の先手固定視点のS5 AND判定である。S5 LOSS 3件は独立geometry・raw履歴・cache conflict監査で確認したが、solverの勝敗判定自体を終局まで独立再証明した証明書ではない。

exact cacheは5738行（WIN 158 / LOSS 5580）から5741行（WIN 158 / LOSS 5583）へ増えた。対象S4の完全109-child境界はLOSS 14 / WIN 0 / UNKNOWN 95となり、依然UNKNOWN。S4はOR層なので、3つのS5 LOSSだけではS4 LOSSにならない。

全3384 S4 classはLOSS 31 / WIN 272 / UNKNOWN 3081のまま。第三手被覆117/119、未被覆 `{100,108}`、整数最小追加class数1、有理LP双対1も不変。1個のS4 LOSS classが見つかればcover可能である事実は、そのclassのLOSSを証明したことを意味しない。

終了時のraw-history auditはexperimentsと`.local`の11925 CSVを調べ、対象109子のverdict conflict 0、15M以上UNKNOWN 0を確認した。残り95 UNKNOWN子に対するS6境界は5366 canonical局面で、raw exact S6 16、cache exact S6 17。対象範囲にraw/cache S7 intersectionおよびS6/S7由来S5 verdictはなかった。budget=0 projectionは使っていない。

次の低legal-count候補はS5 `(1152921504606851072,537001986)`、legal手数90。最新raw-historyと保存layer監査ではdispatch-ready、既存raw observationなし、S6/S7由来verdictなし。まだdispatchしていない。

`{60,27}` と11×11空盤の勝者は未確定。既存cache-only evidenceも残るため、全frontierは独立minimax証明DAGではない。

## 再現と監査

`input/`に完全S5境界と各probe input、`output/`にraw CSV、stdout/stderr、段階別raw-history/S6-S7監査、exact-only cache merge receipt、frontier再分類、report、SHA-256 inventoryを保存した。`scripts/plan_probe.py`と`plan_next_probe.py`はdispatch条件をassertし、`merge_s5_exact.py`等はraw結果をcacheへ加える前にcanonicality・安全性・S4親子geometry・legal数・隔離registryを確認する。

各probeのsolver commandは以下の形で再現できる。2M対象は`probe-target.csv`、`probe-target-2.csv`、`probe-target-3.csv`、raw CSVの出力先は対応する`probe-*.csv`である。

```powershell
.local/n11-independent-audit-solver.exe `
  --n=11 --memo=22 `
  --exact-replay=research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/input/probe-target.csv `
  --only=5 --exact-order=count --exact-replay-budget=2000000 `
  --csv=research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/probe-2m.csv
```

15M retryもbudgetとinput/outputだけを対応させる。各retry前の対象単独raw-history、S6/S7 preflight、およびsolver/source SHA-256は`escalation-plan*.json`に固定した。全artifactのSHA-256一覧は`output/artifact-sha256.json`にあり、inventory自身は一覧対象外。
