---
id: K0228
title: 中心分母の素因数型で格子点数上限を整理できる
kind: proposition
status: proved
topics:
- geometry
aliases:
- B453
relations: []
artifacts:
- path: research/verification/round10-circle-denominator.md
  role: proof
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B453の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round10_circle_denominator.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round10_circle_denominator.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: '起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。'
evidence: 原文監査 SUPPORTED / general_proof
---

# 中心分母の素因数型で格子点数上限を整理できる

対象命題: 中心分母の素因数型で格子点数上限を整理できる。 qの数値順ではなく、2進部分・1 mod 4素因数・3 mod 4素因数に分けると、q=3対4の逆転を説明する上限が得られる。

適用文脈: 起点: [個票07・B131〜B137](verification/batch-07.md)。分母に対する単調性は捨てる。半径が同じだが片側が0点という退化比較も除き、双方4格子点以上の円を主に扱う。

現在の結論: 分母素因数型と剰余類の完全格子点数上界、q=3/4の等号。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
