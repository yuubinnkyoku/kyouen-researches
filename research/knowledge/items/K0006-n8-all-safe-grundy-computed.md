---
id: K0006
title: 8×8の全6,700,711,937安全局面をGrundy DPで完全計算
kind: computation
status: computed
topics:
- grundy
- square-outcomes
- verification
aliases: []
relations:
- type: depends_on
  target: K0002
  note: ''
- type: supports
  target: K0113
  note: 一石局面の非零Grundy値は {1,3} のみ（すべて奇数）。n=8有限盤の証拠で、無界全称は証明しない
- type: supports
  target: K0119
  note: J_8は64頂点・1,380辺でunion-find/BFS二方式とも1成分（連結）。n=8有限盤の証拠
- type: supports
  target: K0182
  note: 後手勝ち8×8の一石nimberの種類数は2（{1,3}）。n=8有限盤の証拠
- type: supports
  target: K0183
  note: σ_8=4層で欠番なし（missing=[]）。有限盤の観測で無界全称は証明しない
- type: supports
  target: K0184
  note: σ_8=4層の正の欠番なし（真空に「2の冪」を満たす）。有限盤の観測
artifacts:
- path: research/experiments/original-claims/reports/round5-batch-n8.md
  role: source
  note: 全安全局面列挙・streaming DP完走と集計
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round5_prand_n8.json
  role: data
  note: 層別状態数・P/N数・最大安全サイズを保存
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/log/claim-audit/round5_n8_progress.md
  role: log
  note: 列挙再実行・交差検証・streaming solve完走の記録
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: README.md
  role: source
  note: 空盤勝敗と全局面計算の検証境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n8-grundy-layer-profiles-20261101/output/n8_analysis.json
  role: verifier
  note: grundy専用ストリーミングDP（新規実装）で全67億状態を再走査し、層サイズ・P/N数・K_8=15・g_root=0・禁止四点数14564を完全一致で確認。1石/2石層のmex再照合・J_8連結性・σ_8=4を含む
- path: research/experiments/n8-grundy-layer-profiles-20261101/output/n8_grundy.json
  role: data
  note: 層別集計とGrundyヒストグラム（2026-11-03、別実装の再走)
solution:
  board: 8×8
  level: strong
  outcome: second-player-win
  classification:
  - root
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 6,700,711,937/6,700,711,937安全局面
  conditions: 標準q=4・完全指摘・通常プレイ
  verification:
  - reported-streaming-dp
  certificate: 全局面証明書なし。空盤証明書は別項目
  independent_check: n=6で既知値と全一致、n=7で既知層サイズを照合。2026-11-03にgrundy_onlyストリーミングDPの新規実装で8×8の全局面を再走査し、層サイズ・P/N数・K_8=15・g_root=0・禁止四点数14564が完全一致（同一線譜の別実装。mex標本照合とJ_8連結性も一致）。全局面を覆う証明書はなく独立性は実装再現による
  note: 全局面Grundy DP完走済み。独立全状態検査・強解決証明書は未整備
---

# 8×8の全6,700,711,937安全局面をGrundy DPで完全計算

Round5で全6,700,711,937安全集合を列挙し、streaming DPで全局面のGrundy値とp_randを計算した。集計はP=1,457,674,065、N=5,243,037,872、最大安全サイズK_8=15で、空盤はg=0となり既知の後手勝ちと一致する。

実装はn=6で既知の状態数・層別P/N・p_randと完全一致し、n=7でも既知の層サイズとの照合を行ってからn=8を実行した。古いREADME・考察文書にある「8×8以上は全局面未計算」という記述は、このRound5完走より前の状態を反映したものなので更新する。

これは計算内容として8×8の強解決に相当する。ただし8×8の67億状態を別実装で全再計算した独立監査や、全局面を覆う配布用の強解決証明書があるという意味ではない。「全局面計算済み」と「独立全件検査済み」は区別する。

2026-11-03の再計算では、grundy値のみを保持する専用ストリーミングDP（`grundy_only_stream_solve.cpp`、int8 g/状態）を新規に作り、列挙spillと合わせて全6,700,711,937安全局面を再走査した。層サイズ・層別P/N数・K_8=15・g_root=0・禁止四点数14,564がRound5の集計と完全一致し、1石層64点・2石層300点のmexを再照合、σ_8=4の最適証人mask=148032（g=11）を独立に再計算して確認した。これは同一線譜の別実装による再現であり、全局面を覆う独立証明書ではない。詳細と環境は `research/experiments/n8-grundy-layer-profiles-20261101/README.md`、発見の記録は`research/log/2026-11-03-n8-grundy-layer-profiles.md`を参照。
