---
id: K0761
title: "6×m（q=7）1行欠損クラスは6×13/16/19に存在 — 5×19（K0759）との質的対比、m≥20は未解決"
kind: computation
status: computed
topics: [rectangles, variants, maximal-safe, verification]
aliases: []
scope: "6×m整数格子・q=7・1行欠損（行占有(5,6,6,6,6,6)・35石）の極大安全配置。m∈{13,16,19}でwitness実在、m=22の1鏡映代表S0={0,5,10,15,20}で不在（その代表に限る）、m≥20の一般は未解決"
evidence: "幅6移植DFS機械（census内蔵verify）と、census不使用の独立検証（石3つ組外心列挙・厳密整数演算）"
relations:
- type: depends_on
  target: K0760
  note: 危険円census（chord法・6×13で3点外心brute-forceと一致検証済み）を機械が使用
- type: depends_on
  target: K0759
  note: 5×19では同クラスが不在（全極大安全配置が満容量30石）— 本項目はその幅6版が6×19では在ることを示す対比
- type: depends_on
  target: K0747
  note: 移植元のmulti_deficient_runner機械（アルゴリズム・探索順・計数を同一移植）
- type: supports
  target: K0332
  note: 幅6安定化長M_{6,7}は m≥20 の候補に絞られた（6×19では35石極大安全配置が存在するため）
artifacts:
- path: research/experiments/six-row-q7-deficient-20261112/scripts/six_row_one_deficient_runner.ts
  role: source
  note: 幅6 1行欠損機械（probe + census verify + 独立検証。1実行1エントリの手順は冒頭）
- path: research/experiments/six-row-q7-deficient-20261112/output/six_row_one_deficient.json
  role: data
  note: 全実行結果・witness・独立検証・サンプリング較正
- path: research/log/2026-11-12-six-row-one-deficient-class.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（計算された事実）

6×m整数格子・q=7（7石の共円・共線禁止）において:

1. **1行欠損witnessの実在（機械+独立検証）**: m ∈ {13,16,19} の各々で、
   行占有 (5,6,6,6,6,6)・35石の極大安全配置が存在する。
   - 6×13: 最初の鏡映代表 S0={0,1,2,3,4} 単独で >1,006,128 個
     （600k node cap までの計数。クラス内で豊富）。
   - 6×16: 28ノードで発見。
   - 6×19: 203,446ノード完走で 3 個。最初のwitness
     rows=[[0,1,2,3,4],[3,9,12,13,14,16],[7,8,13,14,16,17],
     [1,7,8,10,14,15],[6,8,10,12,13,15],[0,2,7,8,13,15]]。
     census内蔵verify（safe+maximal）PASS に加え、census不使用の独立検証
     （石3つ組外心列挙・厳密整数演算）で最悪円石数6・未block空点0。
2. **5×19との質的対比**: 5×19 では同クラス（(5,6,6,6,6)）は
   K0738〜K0759 の完全列挙で全滅・全極大安全配置が満容量30石だったのに対し、
   幅6では 6×19 でも35石極大安全配置が残る。
   **幅6の安定化長 M_{6,7}（全極大安全配置が満容量36石となる最小m）は
   存在するとしても ≥20**。
3. **限定的な不在（1代表のみ）**: 6×22 の鏡映代表 S0={0,5,10,15,20} は
   249,271ノード完走で witness 0（この1代表に関する完全列挙による不在）。
   m ∈ {20,22} の S0={0,1,2,3,4} は 300k node cap で未完（open）。

## 根拠

- 機械は 5×19 multi_deficient_runner（K0747〜K0759で使用）の幅6移植で、
  探索アルゴリズム・blocker割当・計数は同一。危険曲線は行直線と
  census円（≥7点）のみ（非水平直線は6行と≤6点で交わり7点直線は存在しない、
  証明）。censusはchord法（K0760制御2で6×13の3点外心brute-forceと
  circle set完全一致済み）。
- witnessはすべて (a) census内蔵verify、(b) census不使用の石3つ組独立検証
  （7石以上の円は必ず石3つ組を含むため完全）の両方で safe+maximal。
- 6×19 witnessの発見ノード数 203,446 は 200k cap では witness 0（capped）、
  203k で最初のwitness — witnessはDFSの深い位置で現れる。

## 限界・スコープ

- 6×13/16/19 の「クラスが空でない」はwitnessの実在による証明だが、
  **クラスの不在・全滅はどこでも主張しない**。m≥20 の存在是非は未解決。
- 6×22 の S0={0,5,10,15,20} 不在は1鏡映代表のみの有限事実
  （全鏡映代表は m=22 で 17,722+ 個）。
- サンプリング較正: (5,6,6,6,6,6) の乱数20kサンプルは m=19〜28 で
  safe 79-97% だが maximal-safe 0（m=19でも0・witness実在にもかかわらず）。
  このクラスの不在にはDFS機械が必須で、サンプリングは不感。
- レジューム: (1) m=20/21/22 を高いnode capで（census構築とDFSの分割や
  増分再開でdeadline管理）、(2) 6×13 全1,212鏡映代表の完全列挙
  （最初の幅6クラス完走データ）、(3) 2行欠損クラスへの拡張。
