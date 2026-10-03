---
id: K0164
title: 勝者を保つ最小禁止族はD4非対称である
kind: proposition
status: refuted
topics:
- variants
aliases:
- B256
relations: []
artifacts:
- path: research/verification/round23-b256-symmetric-minimum.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B256の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round23_minimum_family_verified.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round23_minimum_family.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。
evidence: 原文監査 REFUTED / general_impossibility
---

# 勝者を保つ最小禁止族はD4非対称である

否定された命題: 勝者を保つ最小禁止族はD4非対称である。 あるnについて、標準版と同じ空盤勝者を与える非自明な最小サイズ禁止族は、D4不変な族としては達成できない。元が後手勝ち等、空族との自明な一致を除く。

適用文脈: この節では盤点を固定して禁止4点族だけを変える。標準版での局面ラベルをそのまま流用しない。

現在の結論: 全nで勝敗保持の非空基数最小族一個または二個を、D4不変な互いに素な四点組で達成できる。基数最小族が必ず非対称という主張は偽。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
