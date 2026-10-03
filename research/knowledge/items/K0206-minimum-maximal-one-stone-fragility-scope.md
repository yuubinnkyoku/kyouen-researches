---
id: K0206
title: 最小極大配置は一石の故障に弱い
kind: proposition
status: scope-unclear
topics:
- maximal-safe
- geometry
aliases:
- B361
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
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B361の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: 安全極大Sに対し、元から空だった点を一つでも合法に戻すために必要な最小石除去数をρ(S)とする。除去した場所そのものを再着手可能と数えない。
evidence: 原文監査 SCOPE_UNCLEAR / degenerate_endpoint_and_complete_finite_nondegenerate_support
---

# 最小極大配置は一石の故障に弱い

対象命題: 最小極大配置は一石の故障に弱い。 s_nを達成するすべてのSでρ(S)=1。前回の一重被覆点予想より弱く、全禁止三つ組が一つの石を共有する場合も含める。

適用文脈: 安全極大Sに対し、元から空だった点を一つでも合法に戻すために必要な最小石除去数をρ(S)とする。除去した場所そのものを再着手可能と数えない。

現在の結論: 一石除去で新たに合法になる元の空点数を使う故障率ρ。n1は元の空点がなく未定義。n2..8の全最小極大はρ=1だが、n≥9一般は未証明。

採用境界: n1の全占有最小極大には空点なし、B078の存在節は偽・ρは未定義。非空空点の読みはn2..8全最小極大でmin b1・ρ1、n≥9一般命題は未証明。

根拠は原文量化を照合した最新索引と下記採用報告。旧batchの強いラベルを再採用せず、有限証人・完全列挙・一般証明の範囲を区別する。
