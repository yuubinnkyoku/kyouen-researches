---
id: K0259
title: m≥6の後手は最初の応答を反対行に選べる
kind: proposition
status: proved
topics:
- rectangles
- variants
aliases:
- B541
relations: []
artifacts:
- path: research/verification/round4-fixed-width.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B541の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_fixed_width.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_fixed_width.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 盤は `{0,…,m−1}×{0,1}`。各行の占有集合をA,B、行内の異なる二点の和集合をΣ₂(A),Σ₂(B)とする。各行高々3点とペア和衝突回避という既知の記述を出発点にする。
evidence: 原文監査 SUPPORTED / general_proof
---

# m≥6の後手は最初の応答を反対行に選べる

対象命題: m≥6の後手は最初の応答を反対行に選べる。 初手と同じ行に置かなければ勝てない初手は存在しない。

適用文脈: 盤は `{0,…,m−1}×{0,1}`。各行の占有集合をA,B、行内の異なる二点の和集合をΣ₂(A),Σ₂(B)とする。各行高々3点とペア和衝突回避という既知の記述を出発点にする。

現在の結論: 標準二行盤m≥6の後手は、相手の初手の反対行に置く勝ち応答を選べる。m6..8全数とm≥9一般一様終局証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
