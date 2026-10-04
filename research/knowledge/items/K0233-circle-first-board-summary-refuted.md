---
id: K0233
title: 完全点数・外接幅・原始二次係数では四点初出を決定できない
kind: proposition
status: refuted
topics:
- geometry
aliases:
- B458
relations: []
artifacts:
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 原文・量化・採用根拠・旧記録のhashを固定した監査索引
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round16-first-appearance.md
  role: source
  note: 同じ要約量で四点初出が異なる反例と無限拡大族
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round16_first_appearance.json
  role: data
  note: 反例円と初出プロファイルの厳密データ
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/scripts/round16_first_appearance.py
  role: verifier
  note: 完全点集合と初出サイズの独立検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md
  role: source
  note: B458の原文
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 完全点数・外接幅・原始二次係数では四点初出を決定できない

B458を、完全格子点数m・外接矩形の幅と高さ・原始円方程式の二次係数B（さらに中心分母qまで）から、その円の四点初出サイズν₄が決まる、という具体的な命題として読むと反証される。

保存済み反例C,Dはともに完全点数6、幅差=高さ差17、B=q=3であるにもかかわらず、`ν₄(C)=12`、`ν₄(D)=15`。さらに3 mod 4素数による拡大でこれらの要約量の関係を保ったまま初出差を無限に拡大できるため、有限の加法誤差での予測も不可能である。

「短く分類できる」という未定義な表現は独立の数学命題として残さない。少なくともB458が提案した自然な有限要約による決定性は反証済みである。
