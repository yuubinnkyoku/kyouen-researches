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

## 続行結果（2026-10-10、probe 4–10）

前節の3 LOSS checkpoint後、legal数順のS5 childを7件だけ追加調査した。各childを2M nodesでprobeし、UNKNOWNなら対象単独でraw履歴とsaved S6/S7を再監査してから15M nodesまでretryした。6件はdirect exact LOSS、1件は15M nodesでもUNKNOWNだった。

| S5局面 | legal | 2M | 15M |
|---|---:|---:|---:|
| `(1152921504606851072,537001986)` | 90 | UNKNOWN, 2,000,000 | LOSS, 4,519,790 |
| `(1188950301626859520,536870976)` | 90 | UNKNOWN, 2,000,000 | LOSS, 8,361,840 |
| `(1188950301626859520,603979776)` | 90 | UNKNOWN, 2,000,000 | UNKNOWN, 15,000,000 |
| `(10412322338481635328,536870912)` | 91 | UNKNOWN, 2,000,000 | LOSS, 2,569,967 |
| `(1189091039115214848,536870912)` | 92 | UNKNOWN, 2,000,000 | LOSS, 4,808,557 |
| `(1765411053930283008,536870912)` | 92 | UNKNOWN, 2,000,000 | LOSS, 4,785,007 |
| `(1152921504606851072,570425346)` | 93 | UNKNOWN, 2,000,000 | LOSS, 6,730,471 |

14 runで60,775,632 nodesを処理し、うち6つのexact LOSSは合計31,775,632 nodesだった。3件の直前checkpoint分も合わせると累計20 run・10 distinct S5 positions・9 direct LOSS、75,550,352 total nodes（exact判定40,550,352 nodes）。15M UNKNOWN 1件はcacheに入れていない。

現行exact S5 cacheは5,747 rows（WIN 158 / LOSS 5,589）、quarantine key 0。対象S4の完全109-child境界はLOSS 20 / WIN 0 / UNKNOWN 89で、S4は依然UNKNOWN。全3,384 classはLOSS 31 / WIN 272 / UNKNOWN 3,081、第三手被覆117/119、残り`{100,108}`、整数最小追加class数1、有理LP双対1のまま。

終了時の全target raw auditは11,947 CSVを走査し、cache exact intersection 20、prior raw exact 13 keys（26 rows）、same-budget-or-higher UNKNOWN 1、lower-budget UNKNOWN 11、dispatch-ready UNKNOWN 88、verdict conflict 0を確認した。ready 88件のS6 unionは5,283 canonical keys（raw exact S6 13 / cache exact S6 14）。S7 intersectionとS6/S7からのS5派生は0。最後に選んだ次候補は`(1188950301626859520,536870913)`、legal 94、raw observationなし・saved-layer verdictなしでready。まだdispatchしていない。

各6 LOSSはraw solver CSVとmerge receiptに追跡でき、独立Boardがsafe canonicality・legal count・S4/S5 edgeを検査した。solverのexact verdict自体をterminal-only独立証明に置き換えてはいない。基礎cacheにcache-only evidenceが残るため、このcheckpointも全面的な独立minimax DAGではない。継続内容は`output/report-continuation.json`、SHA-256全件は`output/artifact-sha256.json`を参照。

## 最新main `f3c0c8ec` の共有S5 LOSSを統合

探索中にorigin/mainが進み、commit `f3c0c8ec265e034a3e69c03e6eee6d5d9a4a8e43` から、別experimentでraw・geometry監査されたS5 LOSS 2件が到着した。両方ともこのS4の合法109子に属する。キー `(1152921504606851072,536870946)` はlegal98・3,651,923 nodes、`(1188950301626860544,536870912)` はlegal99・5,040,200 nodes。各2M retryはUNKNOWNで、15Mでdirect LOSS。新mainのprobe auditはbaseline cache 5,741から5,743 rowsへのmerge、conflict0、S4新判定0を記録する。

新main exact cacheと本実験の6 direct LOSSをキー重複・verdict conflictなしでreconcileしたcacheは5,749 rows（WIN158 / LOSS5,591）。独立Boardで両experimentの追加8 childについてsafe canonicality・legal数・対象S4 edgeを再検査した。対象境界はLOSS22 / WIN0 / UNKNOWN87でUNKNOWNのまま。全classはLOSS31 / WIN272 / UNKNOWN3,081、第三手被覆117/119、整数最小1、有理dual1である。

最新mainの全raw-history再監査は11,960 CSVを検査し、target109、cache intersection22、exact conflict0、同以上budget UNKNOWN1、dispatch-ready86。保存layer監査はS6 boundary 5,249、raw/cache exact S6 13/14、S7 intersection0、S6/S7由来S5 verdict0。次のready候補は`(1188950301626859520,536870913)`、legal94でraw観測なし。最新mainに基づくrebase receipt、report、frontier、raw/layer auditは`output/latest-main-cache-rebase.json`と`output/report-after-main-rebase.json`以下に保存する。

この統合手順の主要な再生成コマンドは次の通り。再分類・raw-history・layer auditの引数と出力先は同experimentの`output/`を使う。

```powershell
uv run --locked python research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/scripts/rebase_latest_main_cache.py
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/reclassify_frontier.py --cache research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-9-rebased-main.cache --compare-to-cache research/experiments/n11-two-target-design-20261010/output/merged-exact-s5.cache --out research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/frontier-after-main-rebase.json
uv run --locked python research/experiments/n11-boundary-recovery-20261006/scripts/audit_s5_raw_history.py --targets research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/input/class-s5-complete.csv --root research/experiments --root .local --current-cache research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-9-rebased-main.cache --budget 15000000 --out research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/raw-history-after-main-rebase.json
uv run --locked python research/experiments/n11-reply27-class-1297036692683751424-16-20261010/scripts/layer_preflight.py --preflight research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/geometric-cache-preflight.json --raw-s5-audit research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/raw-history-after-main-rebase.json --out research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/saved-layer-after-main-rebase.json
uv run --locked python research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/scripts/plan_next_probe.py --raw research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/raw-history-after-main-rebase.json --layer research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/saved-layer-after-main-rebase.json --cache research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-9-rebased-main.cache --suffix 11
uv run --locked python research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/scripts/build_rebased_main_report.py
uv run --locked python research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/scripts/build_artifact_inventory.py
```
