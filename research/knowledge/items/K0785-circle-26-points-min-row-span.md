---
id: K0785
title: 26点円の最小行スパン43（中心窓で全称・R=2210は一意）と34..48点の上界（円11050）— 本文は未投入のプレースホルダ
kind: proposition
status: needs-review
topics: [rectangles, geometry, variants]
aliases: []
relations: []
artifacts:
- path: research/experiments/circle-26pt-min-rowspan-20261112/reports/circle-26pt-min-rowspan.md
  role: proof
  note: "定理A/B/C・補題鎖L0-L6・限界・K0786との役割分担（2026-11-13時点で本文はプレースホルダ）"
- path: research/experiments/circle-26pt-min-rowspan-20261112/output/circle_26pt_min_rowspan.json
  role: data
  note: "family E/O/Zの全数列挙・bestK・good13・spectrum・verify・controls（同様にプレースホルダ）"
- path: research/experiments/circle-26pt-min-rowspan-20261112/scripts/circle_26pt_min_rowspan.ts
  role: solver
  note: "単独再現機械（STAGE分割: E/O/Z全数列挙＋witness検証）"
scope: "連続整数行の円の格子点数。2026-11-13時点では見出しのみで、主張・根拠・限界の本文が未投入。"
evidence: "未投入。コミット9d6cfc8b/a8cc2daf/42359e98/4d5670c7 が置いた本文・report・output・logはいずれも `<KITEM>` / `<REPORT>` / `<OUTPUT>` / `<LOG>` というプレースホルダで、検証できる内容が無い。"
---

## 状態

このファイルは 2026-11-13 06:27 のコミット `9d6cfc8b` が `<KITEM>` という 1 行だけの
プレースホルダとして追加したもので、front matter が無く knowledge 検査を落としていた。
同時に追加された report / output / log も同様に `<REPORT>` / `<OUTPUT>` / `<LOG>` の
プレースホルダである。

ビルドを通すための最小限の補修として、コミットメッセージに書かれた見出しだけを front matter
へ移し、status を `needs-review`（採用根拠の監査不足）とした。**内容の主張は行っていない。**

## 限界

- 定理・証明・数値（行スパン43、R=2210、34..48点の上界、円11050 など）は
  コミットメッセージにしか存在せず、本文・report・output からは検証できない。
- 著者による本文と report / output の投入後に status と relations を付け直す必要がある。
- K0786（幅36..48の円ストリップ証人）との役割分担も未投入。
