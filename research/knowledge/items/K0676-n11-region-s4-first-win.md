---
id: K0676
title: 四石領域位置S4-A/S4-Bは先手勝ち（各94合法子のうち37先手勝ち五石子）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0675
  note: 94五石位置の勝敗分類（78先手/16第二手）
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json
  role: data
  note: 五石位置勝敗の一次データ（78先手/16第二手）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/region_test.py
  role: verifier
  note: 94五石子の共通四石親の同定と合法子数・先手勝ち子数の計数
- path: research/log/2026-11-07-n11-region-s4-first-win.md
  role: log
  note: 領域検証の経緯
scope: 標準11x11完全指摘・通常プレイの四石位置 S4-A/S4-B およびその五石子。S3以下・二石root・空盤勝敗は含まない。
evidence: >-
  94五石位置の共通四石親として S4-A（00000000000000203800000000000000、49五石子を含む）および S4-B（00000000000000003800800000000000、41五石子を含む）が同定され、各94合法子を持つ（独立幾何 vf.legal で数え上げ）。各四石位置の94合法子のうち37がK0675の先手勝ち五石位置（各五石位置の第二手全応手が手番WINであることが独立監査済み）であり、したがって四石領域位置は手番（先手）の勝ちと確定する（手番の勝ち手＝先手勝ち五石子への着手）。S3以下・二石root・空盤勝敗はUNKNOWN。
---

# 四石領域位置の先手勝ち

94 五石位置の共通四石親として、S4-A（`00000000000000203800000000000000`、49 五石子を含む）と
S4-B（`00000000000000003800800000000000`、41 五石子を含む）が同定され、各 **94 合法子** を持つ
（独立幾何 `verify_five_terminal_loss7` の `legal()` で数え上げ）。

各四石位置の 94 合法子のうち **37 が K0675 の先手勝ち五石位置** であり、したがって
四石領域位置は手番（先手）の勝ちと確定する（手番の勝ち手＝先手勝ち五石子への着手）。

上流（S3・二石root・空盤）の勝敗は UNKNOWN のままである。
