---
id: K0138
title: 最小極大配置には一重被覆点がある
kind: proposition
status: scope-unclear
topics:
- maximal-safe
- geometry
aliases:
- B078
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/verification/round47-private-cover-and-global-minima.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B078の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 本文の原文量化と現在の採用境界
evidence: 原文監査 SCOPE_UNCLEAR / degenerate_endpoint_and_complete_finite_nondegenerate_support
---

# 最小極大配置には一重被覆点がある

対象命題: 最小極大配置には一重被覆点がある。 s_nを達成するSなら、ある空点pで `b_S(p)=1`。B077と両立し、最小性に由来する脆さだけを主張する。

現在の結論: n1の全占有最小極大に空点はなく、「一重被覆点が存在」は偽。非空空点を条件とする読みではn2..8全最小極大でmin b=1だがn≥9は未証明。

採用境界: n1の全占有最小極大には空点なし、B078の存在節は偽・ρは未定義。非空空点の読みはn2..8全最小極大でmin b1・ρ1、n≥9一般命題は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
