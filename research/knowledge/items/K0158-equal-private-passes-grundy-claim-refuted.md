---
id: K0158
title: 一回だけパスできる版はgだけでは分類できない
kind: proposition
status: refuted
topics:
- variants
aliases:
- B227
relations: []
artifacts:
- path: research/verification/round18-equal-passes.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B227の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round18_local_geometry.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round18_local_geometry.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。
evidence: 原文監査 REFUTED / general_impossibility
---

# 一回だけパスできる版はgだけでは分類できない

否定された命題: 一回だけパスできる版はgだけでは分類できない。 プレイヤー各1回のパスを許す派生版で、通常版のgが等しい二局面の勝敗が異なる。

適用文脈: この節だけは派生ゲーム。標準ルールでの結論と混ぜない。円のみ版は4共線を許すが、4点が非退化円上にある場合は禁止する。

現在の結論: 両者が一回ずつ未使用パス権を持って開始する等権利状態では通常gが保存される。片方だけ消費した履歴状態は別条件で、即終了規約では一手終端可能性も必要。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
