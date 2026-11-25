# n11 class4 batch2 frontier: newly_solved_manifest_hexes 重複監査（2026-11-14）

## 対象

main の `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-batch2-frontier-update-20261114.json`。

## 独立した機械的検査

JSON の `covers_analysis.newly_solved_manifest_hexes` は8要素だが、集合としては **7要素**。次の鍵が2回出現する。

`000000000200000038000000a0000000`

一方、同じJSONの `frontier_delta.solved_s6_in_manifest` は657→665（+8）で、`unique_remaining_s6` は7189→7181（−8）。`marginal_in_manifest` も8と記録されている。従って、列挙された8行を「新たに解消した相異なる8軌道の完全な鍵一覧」とみなすことはできない。

## 判定・次の確認

これは **報告JSONの鍵一覧に関する整合性不良** であり、証明書のWIN/LOSS判定やfrontier集計値が誤っているとの結論ではない。元の `audit_class_frontier.py` を公開入力から再実行し、差分集合 `solved_after - solved_before` を直接出力して8個の相異なる鍵と照合する必要がある。集計値8を7に書き換えたり、欠けた鍵を推測で補ったりしてはならない。

11×11空盤、S2 {59,60}、二石root {49,60} は UNKNOWN のまま。
