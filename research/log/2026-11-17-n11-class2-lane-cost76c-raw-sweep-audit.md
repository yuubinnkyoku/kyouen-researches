# 2026-11-17：cost76c raw sweep 全10 batchの再集計・監査

開始時の最新mainは `92f1f2f9f511ca28c3330b5e50d8d1372dc8a958`。作業前に `AGENTS.md`、`research/knowledge/README.md`、K0863/K0865/K0868、cost76c claim、head-1452 presweep、関連するcost64h/75e/76d/77eの研究記録を確認した。

## 対象と再集計

対象S6 child: `00000000010000809002000001000000`  
親S5: `00000000000000801202000040000000`  
head: `1452/174/6396/506144/4669/370058`

公開済みのraw batch 1〜10をすべて取得し、各JSONLを独立に読み直した。結果は次のとおり。

- 10 batch、76 bit record、重複bit 0。
- claimの合法候補76個とraw recordのbit集合が完全一致。
- claimの各batch bit列とrawファイルのbit列が10/10一致。
- pilot d6 controlは10/10で `loss=false, nodes=3402, capped=false`。
- 全76候補が `andclose=true`、terminalStoneRange `[13,17]`、capped 0。
- **WIN7-D10: bits 61, 99, 113 の3件。**
- REFUTED-D10: 73件。これはLOSS証明ではない。
- 候補本体のnodes合計 **141,221,576**。pilot 34,020 nodesを含めると **141,255,596**。

### 既存転送との照合

K0863の転送表にある15 bitは、すべてraw batchにも再登場し、全15件が `loss=false && capped=false` だった。内訳はclaim上の5 crosscheck bitと10 reuse bit。したがって、今回のraw結果では転送15件にWIN/REFUTED矛盾はない。

ただし、claimの `engine_candidate_bits` は「61 open + 5 crosscheck = 66 engine bits、10 transfer bitsは再利用」と記す一方、`engine.batches` の配列と実raw batchは**全76合法bit**を実行している。実際に10 reuse bitも再実行された。今回の実行量は66ではなく76であり、10件の節約として数えない。この差を監査JSONとclaim更新に明記した。

## 3つのWIN root

head-1452 presweep censusのD4正準形と照合した。

| bit | root canon | v16 nodes |
|---:|---|---:|
| 61 | `0000000001000080b002000001000000` | 752,696 |
| 99 | `00000000040000809002000000400800` | 4,168,961 |
| 113 | `00000000040000809002000000400008` | 8,174,662 |

3 rootともpresweep時点ではopen。これらは個別7石rootのWIN7-D10候補であり、まだ証明書は抽出・独立検証されていない。

## 保存物

- 監査器: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76c_raw_batches_20261117.py`
- 監査結果: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76c-raw-audit-20261117.json`
- immutable claim input snapshot: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76c-claim-input-20261117.json`（Git blob `8932f2d5e100325549a5f251a1d883558cae0708`、監査入力）
- current claim: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76c-inflight-20261116.json`（sweep-complete / certificate-pendingへ更新）

監査結果にはimmutable claim input snapshot・presweep・10 raw batchのGit blob SHA-1を固定し、候補集合・batch列・pilot・verdict・転送bit・root canonをassertする再現用Python標準ライブラリ監査器を追加した。

作成コミット:
- 監査器: `e37b381f30b8870707f9e58073218dd01473c384`
- 結果JSON: `f9438beda5fe6d62b01190107d5fb797688cd816`

## 信頼境界と次

これはraw batchの完全性・集計・転送整合性の監査であり、v15別実装との照合ではない。3 WIN rootの証明書抽出、独立証明書検査、v15 cross-engine照合、receipt foldは未実施。

次はbits 61/99/113をblind extractionし、各証明書を独立検証してから、fold時点の最新canonical headへrebaseする。head 1472はcost64h preregの予測値であり、現時点の確定headとして扱わない。

**標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4 はすべてUNKNOWN。** REFUTED-D10、STERILE、solved headはいずれも空盤の勝敗を決めない。


## 最終固定・実行境界

- immutable claim snapshot: `c7c52094c7b1539a7e3111395c417dbda87c2133`（blob `8932f2d5e100325549a5f251a1d883558cae0708`）
- 最終監査器: `11e3d4cc1badb7ecf8db82ff7e373d6663882b3e` の後、winner-canon assertionを明確化した `e6928642cbdc43d97894e36d481b5bfc028b14a8`
- 最終監査JSON: `0be02d250c07d4c0933dab929382860fc4cbcb7a`（18/18項目をこのrunの独立再集計でPASS）
- current claim更新: `08fe56eb29ea05ea903f66ffe4dc34941bb24fc5`
- このログの最終更新: 本追記を含むコミットで確定。

監査JSONの18項目は、GitHubから取得した実ファイルをこのrunで再集計した結果。Python監査器は再現用に出版したが、このrunではリポジトリを実行できるPython環境を確保できず、Python版そのものの実行は未確認。ローカルの構文検査は旧版に対してのみ実施済みなので、最終版の実行成功とは扱わない。GitHub commit statusは空で、CI成功も未確認。
