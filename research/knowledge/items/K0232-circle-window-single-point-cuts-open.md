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
- path: research/experiments/original-claims/reports/round4-circle-windows.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B457の原文・定義（現在の結論は採用報告を優先）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round4_circle_windows.json
  role: data
  note: 採用報告の証人・完了範囲・検算を再確認する資産
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round4_circle_windows.py
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

## 2026-10-17 bounded advance

Scope clarification: B457 decomposed into four layers. Layer 0 (q>=3 no-holes) proved (K0299). Layer 1 (sufficiently large windows) q>=3 count >= q<=2 count, equality possible (m=6 example). Layer 2 (small fixed windows) has counterexample candidate (m=6,n=5: q>=3 has 3 kinds vs q<=2 has 5). Layer 3 (statistical tendency) has unspecified population/quantifiers.

Next steps: aggregate round4 fixed-side data to confirm minimal Layer 2 counterexample; separate Layer 2 as explicit open question; specify population or withdraw statistical tendency. The local draft proposed open, but the unspecified statistical quantifiers keep the current status scope-unclear.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
