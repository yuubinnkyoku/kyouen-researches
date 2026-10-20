---
id: K0478
title: 任意三平行線の6点禁止ゲームで18候補不足極大は同和弦energy14の剛性型に限る
kind: proposition
status: needs-review
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
scope: 任意の実数座標上の3本の平行直線、各線18点以上の有限候補、q=6、完全指摘・通常プレイ。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 18候補の不足極大が存在する場合の剛性

各線に18点以上あるのに15石未満の極大安全配置が存在するなら、石数は不足線4石・他の2線各5石であり、不足線の候補点はちょうど18点。外2線の無順序二点和energyは14で、14本の候補円がそれぞれ既存4石の1点と異なる空候補14点を結ぶ必要がある。

5点集合B,Cのenergy14には、(i) B=Cで自己energy14、(ii) 同公差5項等差数列が半公差ずれ、(iii) 一方が等差で他方の二点和10個中9個が一致、の3型しかない。5点集合の二点和多重集合が元の5点集合を一意復元することを、Newton恒等式で証明する。

**未解決**：上記必要条件を満たす実配置が存在するか、したがって18候補が一様十分か。19候補の十分性は別添証明で得られるが、整数格子の真の閾値M3,6=9と混同しない。
