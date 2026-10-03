---
id: K0232
title: 円窓B457の種類数比較は量化が未指定、q≥3の穴なしは証明済み
kind: question
status: scope-unclear
topics:
- geometry
aliases:
- B457
relations:
- type: depends_on
  target: K0299
  note: q≥3の穴なしスペクトル定理は証明済み部分として分離
artifacts:
- path: research/verification/round4-circle-windows.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B457の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round4_circle_windows.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round4_circle_windows.py
  role: verifier
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
scope: qは中心の正確な共通分母。完全円上点数mを揃えた固定窓の比較。統計的傾向の母集団・窓サイズ・集計量は未指定。
evidence: 原文監査 PARTIAL / partial_general_spectrum_result
---

# 円窓B457の種類数比較は量化が未指定、q≥3の穴なしは証明済み

中心の正確な共通分母q≥3の完全格子円Pについて、任意の固定整数正方形窓サイズnで、実現点数は0から最大点数M_n(P)まで穴がない。この一般定理はK0299へ独立したproved項目として分離した。

同じ完全点数mの円同士を双方収容できる十分大きい同サイズで比べると、q≥3の種類数はq≤2以上だが、厳密に多いとは限らない。

原文B457の「変えやすい・種類が多い」という比較には、小さい固定窓でのM_n(P)の比較と、統計的傾向をいうなら円の母集団・窓サイズ・集計量の指定が残る。未指定の量化を勝手に全称命題へ直さずscope-unclearとする。

新しい分母5・6・8の完全点数・最小半径の定理や全中心n≤112の最大点数計算は、この同点数での窓スペクトル比較を決着するものではない。
