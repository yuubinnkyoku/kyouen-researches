---
id: K0478
title: 任意三平行線の6点禁止ゲームで18候補不足極大は同和弦energy14の剛性型に限る
kind: proposition
status: proved
topics:
- rectangles
- geometry
- variants
- maximal-safe
aliases: []
relations:
- type: depends_on
  target: K0342
  note: 二点和energyの鋭い上界と同和弦による円計数
- type: depends_on
  target: K0350
  note: 任意平行線上の満容量問題の定義と21候補上界
artifacts:
- path: research/experiments/q6-18-rigidity-20261018/proof.md
  role: proof
  note: 二点和復元・energy14剛性と18候補の必要条件の全称証明
- path: research/experiments/q6-18-rigidity-20261018/verify.py
  role: verifier
  note: 5点集合の63504組のenergy分類と二点和復元の独立有限監査
- path: research/experiments/q6-18-rigidity-20261018/audit_independent.cpp
  role: verifier
  note: 別実装で63504組を照合
- path: research/experiments/q6-18-rigidity-20261018/supporting-q6-19-proof.md
  role: proof
  note: 19候補十分定理と例外E16の1820記号型検査への帰着
- path: research/experiments/q6-18-rigidity-20261018/supporting-q6-19-verify.py
  role: verifier
  note: 例外E16の1820型を有理数演算で完全検査
- path: research/experiments/q6-18-rigidity-20261018/supporting-q6-19-audit.cpp
  role: verifier
  note: 例外E16の1820型の独立C++検査
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 任意の実数座標上の3本の平行直線、各線18点以上の有限候補、q=6、完全指摘・通常プレイ。
evidence: '2026-10-21監査。energy14の剛性分類・被覆の等号条件を確認。四円の全1820有理連立式をPython・独立C++で再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 18候補の不足極大が存在する場合の剛性

各線に18点以上あるのに15石未満の極大安全配置が存在するなら、石数は不足線4石・他の2線各5石であり、不足線の候補点はちょうど18点。外2線の無順序二点和energyは14で、14本の候補円がそれぞれ既存4石の1点と異なる空候補14点を結ぶ必要がある。

5点集合B,Cのenergy14には、(i) B=Cで自己energy14、(ii) 同公差5項等差数列が半公差ずれ、(iii) 一方が等差で他方の二点和10個中9個が一致、の3型しかない。5点集合の二点和多重集合が元の5点集合を一意復元することを、Newton恒等式で証明する。

**未解決**：上記必要条件を満たす実配置が存在するか、したがって18候補が一様十分か。19候補の十分性は別添証明で得られるが、整数格子の真の閾値M3,6=9と混同しない。
