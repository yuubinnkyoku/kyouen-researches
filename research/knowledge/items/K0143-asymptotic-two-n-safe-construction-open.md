---
id: K0143
title: 2n−O(1)石の安全配置を無限族で作れる
kind: question
status: open
topics:
- maximum-safe
- geometry
aliases:
- B088
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round61-full-split-prime-safe-construction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B088の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 PARTIAL / explicit_full_split_prime_linear_construction
---

# 2n−O(1)石の安全配置を無限族で作れる

未確定の命題: 2n−O(1)石の安全配置を無限族で作れる。 有限体上の放物線などの整数化から、共線・共円の両方を避ける格子点族を構成できる。有限体での安全性を整数盤へ移す条件が本体。

現在の結論: p≡1 mod4の全素数でKp≥pの自足構成はあるが、原文の2n−O(1)係数に届いていない。線形下界があることだけで原文を証明済みにしない。

採用境界: p≡1 mod4でa²=-1、(t²+t,a(t²-t))の全p整数代表が安全。四点行列式8a VandermondeでKp≥pを自足証明・独立検算。既知線形下界の再構成、原文2n−O(1)は未達。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
