---
id: K0466
title: 3×5・q=6の左右対称列では非等差なら6点円は最大2本、等差なら最大4本
kind: proposition
status: proved
topics:
- rectangles
- variants
- geometry
- grundy
- maximal-safe
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイのGrundy定義
artifacts:
- path: research/experiments/fixed-width/reports/q36-symmetric-five-columns.md
  role: proof
  note: 左右対称な任意の5列・正実数行間隔での全称円分類、3型への帰着
- path: research/experiments/fixed-width/scripts/symmetric_five_columns_q6.py
  role: verifier
  note: 二点和の式と全15点部分集合のGrundy後退計算
- path: research/experiments/fixed-width/scripts/symmetric_five_columns_q6_independent.cpp
  role: verifier
  note: 整数持ち上げ行列式による全5005六点組の独立検査と全局面計算
- path: research/experiments/fixed-width/output/symmetric_five_columns_q6_audit.txt
  role: data
  note: Pythonと独立C++による5代表の検証結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
solution:
  board: 3×5・q=6・左右対称な実数5列
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全u>v>0、a,b>0、全安全局面
  conditions: 各行の横座標が共通の{-u,-v,0,v,u}、縦座標{0,a,a+b}
  verification:
  - mathematical-proof
  - exhaustive-enumeration
  - independent-enumeration
  certificate: 二点和の重複条件と円の根の積から全称3型帰着、15点全局面mex
  independent_check: 5整数代表について全5005六点組を独立行列式検査し全局面結果を照合
  note: u≠2vでは最大2円、空盤gは円本数0,1,2に対して1,0,1。u=2vでは最大4円。
scope: 左右対称な5列を各行で共通使用する全正実数u>v>0、a,b>0。6点禁止・通常プレイ。
evidence: '2026-10-21監査。左右対称5列の二点和重複・積差による全称分類を確認。Pythonと独立C++の幾何・全局面を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 3×5・q=6の左右対称列での円本数と勝敗の剛性

横座標を各行共通で \(\{-u,-v,0,v,u\}\)（\(u>v>0\)）、行座標を \(0,a,a+b\)（\(a,b>0\)）とする。

\(u\ne2v\) なら、6点円は高々2本。2本となる必要十分条件は \(a=b=\sqrt{(u^2-v^2)/2}\)。この場合は全3行の中央列が6点円から自由である。\(u=2v\) なら最大4本、4本は \(a=b=v\) に限る。

非等差5列での円本数0・1・2に対する空盤Grundy値はそれぞれ **1・0・1**、安全局面数は32768・32256・31776、最大Grundy値は1・1・3。これは全正実数についての二点和代数的分類と、各禁止集合型についての有限完全mex計算を組み合わせた結果である。非対称な5列・行ごとに異なる横座標には拡張していない。
