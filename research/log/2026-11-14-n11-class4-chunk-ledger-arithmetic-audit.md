# 11×11 class4 chunk ledger の節点集計監査（2026-11-14）

対象: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-batch1-chunk-decomposition.json`（main、2026-11-14 01時台確認）。

公開JSONを別集計（整数加算）した結果:

| 対象 | kill表 | kill節点表 | batch_nodesの和 | totals.nodes | 差（batch−totals） |
|---|---:|---:|---:|---:|---:|
| bit7 | 50 | 50 | **4,157,121** | **4,156,721** | **400** |
| bit25 | 50 | 50 | 6,768,196 | 6,768,196 | 0 |

両方でkill表とkill節点表の鍵集合は一致する。bit25のkill節点表の和は1,848,372で、報告値と一致し、残り4,919,824との和も6,768,196に一致する。

**監査上の留保:** bit7の400節点差は集計の不整合であり、どちらが正しいかは実行ログと照合するまで決めない。探索のWIN/LOSSを反証するものではないが、節点数を精密な性能比較に使用する前に解消する必要がある。既存の証明書の独立検証を今回再実行したわけではない。bit25は深さ10の候補であり、証明書再構築・独立検証前に確定WINへ昇格させない。

再現: JSONの各 `totals.batch_nodes` を整数加算し、`totals.nodes` と比較する。さらに `kill_table` と `kill_chunk_nodes` の鍵集合、bit25の `kill_nodes_sum` と `pass_chunk_nodes_sum` を照合する。

標準11×11空盤、S2 {59,60}・{49,60}は **UNKNOWN**。
