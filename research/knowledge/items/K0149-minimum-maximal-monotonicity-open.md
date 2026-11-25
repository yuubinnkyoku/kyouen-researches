---
id: K0149
title: s_nは単調増加する
kind: question
status: open
topics:
- maximal-safe
- geometry
aliases:
- B097
relations:
- type: depends_on
  target: K0026
  note: ''
- type: depends_on
  target: K0312
  note: 11盤の境界は単調性を証明も反証もしない
- type: depends_on
  target: K0034
  note: s_10=10確定済み。10→11の非減少性のみ未確定
artifacts:
- path: research/experiments/original-claims/reports/round54-small-board-saturation-jump.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md
  role: source
  note: B097の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 8≤s_11≤10。n=10から11への非減少性はこの区間では決まらない
scope: 標準q=4のs_nの全nにわたる非減少性。
evidence: 原文監査 PARTIAL / complete_finite_saturation_sequence; s_1..s_10=[1,3,5,5,5,6,7,8,9,10]（s_10=10はK0034の九石全域排除により確定）; monotonicity holds n=1..10; 10→11以降は未確定。11×11の8/9石極大の排除が10→11に有効（5/6/7石はK0312で排除済み）
---

# s_nは単調増加する

標準正方形盤で全nについてs_{n+1}≥s_nかは未証明。

s_1..s_10=[1,3,5,5,5,6,7,8,9,10]（s_10=10はK0034の九石全域排除・AUDIT PASSにより確定）なのでn=1..10の有限系列は非減少と確認できる。最新の11盤は8≤s_11≤10であり、n=10から11への大小関係は未確定。

11盤の10石極大やn=11..15のn−1石構成は存在上界であって最小性の証明ではない。盤の包含だけからs_nの単調性を推論しない。

## 2026-10-17 bounded advance

New finite evidence: s_1..s_9 = [1,3,5,5,5,6,7,8,9], 9<=s_10<=10; monotonicity holds for n=1..9 (and 9->10). For 10->11, excluding both 8/9-stone maximal sets on 11x11 would suffice; this is not an equivalence while s_10 is unresolved (5/6/7 already excluded by K0312). Bounded exact search: 41M nodes (k=8) and 16M nodes (k=9) plus 60s heuristic runs found no witness but were incomplete.

Scope clarification: constructions s_12<=11..s_15<=14 are upper bounds only and do not establish monotonicity for larger n.

Next steps: complete chunked/resumable 11x11 eight-stone enumeration over D4 first-stone representatives. Status remains open.

統合監査（2026-10-20）: 添付されていたローカル追記の s_10=10 は新たな排除証明を伴わないため採用せず、既存の9≤s_10≤10を維持した。有界探索の不成功は非存在証明ではない。

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。

## 2026-11-03 訂正：s_10=10 はK0034で確定済み

上記2つの監査が維持していた「9≤s_10≤10」は、K0034（九石全域排除、D4第一石代表15点・95,816,876,802節点・全15代表 `complete:true, found:false`、チャンク連鎖・resume整合を機械検査 AUDIT PASS、manifest第487チャンクのsha256固定）により**s_10=10へ決着した**。したがって n=1..10 の有限系列は [1,3,5,5,5,6,7,8,9,10] で非減少。残る未確定は 10→11 以降であり、11×11の8/9石極大の排除（5/6/7石はK0312で排除済み）が必要。s_1..s_11 の完全排除だけでは11→12も単調性の証明にはならない（n=11→12も別途必要）。statusはopenのまま。
