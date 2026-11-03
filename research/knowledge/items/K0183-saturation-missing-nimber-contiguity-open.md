---
id: K0183
title: 飽和開始層で欠けるnimberは連続しない
kind: question
status: open
topics:
- grundy
aliases:
- B321
relations:
- type: depends_on
  target: K0002
  note: ''
artifacts:
- path: research/experiments/original-claims/reports/round28-seven-board-original-verdicts.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B321の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_audited.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_layers.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round28_n7_independent.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n8-grundy-layer-profiles-20261101/output/n8_analysis.json
  role: data
  note: 2026-11-03 n=8全局面再走による飽和開始層σ_8=4の完全プロファイル（missing=[]、σ証人mask=148032 g=11）
scope: '起点: [個票02・B025〜B030](../../log/claim-audit/batch-02.md)。飽和開始の次層以降が埋まるというmexの直接帰結は新仮説に数えない。'
evidence: 原文監査 PARTIAL / finite_complete_classification
---

# 飽和開始層で欠けるnimberは連続しない

未確定の命題: 飽和開始層で欠けるnimberは連続しない。 `0≤j<K_n−σ_n`でjとj+1の両方が欠落することはない。

適用文脈: 起点: [個票02・B025〜B030](../../log/claim-audit/batch-02.md)。飽和開始の次層以降が埋まるというmexの直接帰結は新仮説に数えない。

現在の結論: n7飽和開始k4では0..10が全て現れ、穴がない。全盤の穴の隣接条件は未確定。

採用境界: 7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。

## 2026-10-17 bounded advance

New finite evidence: saturation-start layer histograms recomputed for n=1..7; no pair of consecutive missing nimbers below K_n-sigma_n. Missing values: {0} for n=1,2,3; {1,4} for n=4; {4} for n=6; none for n=5,7. Matches original B321 audit (all_n_no_consecutive_missing=true for n=2..6).

Scope clarification: n>=8 saturation-start layers unchecked (no complete Grundy profiles). Universal claim unproved.

Next steps: extend complete Grundy data to n>=8. Status remains open.

## 2026-10-17 bounded advance (round 4)

New finite evidence: n=8 data checked. Level sizes from n8_stream_enum.json; partial enumeration counts for k=0..4 match (1,64,2016,41664,620812). Loaded 620,812 four-stone positions; memoized Python Grundy sample of 20 positions with 120 s cap completed none, so no layer-4 nimber values obtained. No stored n=8 Grundy layer profiles exist; no n=8 streaming solver available in environment.

Scope clarification: sigma_8 not determined; saturation-start layer and nimber histogram for n=8 unknown. K0183 finite evidence remains limited to n=1..7. No n=8 counterexample or confirmation claimed; no fabrication.

Next steps: optimized streaming DP over all 6,700,711,937 safe positions recording per-level max Grundy/histogram. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。

## 2026-11-03 bounded advance（n=8完全再計算）

8×8の全6,700,711,937安全局面を別実装で再走査し、飽和開始層が **σ_8=4**（M_8(k)=[0,3,4,6,11,…]、D_8(k)=[15,11,9,6,0,…] 単調非増加、天井不変式 M≤K−k 全層で成立、K_8=15）と完全に決定した。σ_8層（k=4）の実現nimberは [0..11] で、**欠番は存在しない（missing=[]）**。よってこの有限盤では連続する欠番の反例は存在しない。最適証人 mask=148032（idx 2558、g=11）を独立に再計算済み。上の2026-10-17節の「n=8完全Grundyは不可能」はこの再走で解消された。

Scope clarification: n≤8の有限盤の分類であり、無界全称は証明しない。statusはopenのまま。
