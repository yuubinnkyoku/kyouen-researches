---
id: K0159
title: 円の点数に応じた禁止緩和が非単調な勝敗列を作る
kind: proposition
status: computed
topics:
- variants
aliases:
- B228
relations: []
artifacts:
- path: research/verification/round22-b228-circle-thresholds.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B228の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_b228_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_rules_cases.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round22_rules_scan.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。
evidence: 原文監査 SUPPORTED / finite_witness
---

# 円の点数に応じた禁止緩和が非単調な勝敗列を作る

対象命題: 円の点数に応じた禁止緩和が非単調な勝敗列を作る。 盤上点数の多い円から順に禁止を追加すると、空盤勝者が少なくとも2回反転する盤がある。

適用文脈: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。

現在の結論: 全直線を保持して円を点数降順に丸ごと追加する系列で空盤g=2→0→2。禁止増加に対し勝敗は単調でない。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
