---
id: K0783
title: n11 S2{59,60} milestone-5のS6ワークリスト（鍵・classes・cost）が完全独立再導出で公開manifestと全行一致し、S7再利用候補8,763は既知LOSS396と証明書プール候補8,367に完全分解される（K0675条件下）
kind: proposition
status: computed
topics: [verification, certificates, provenance, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0675
  note: 94オラクル位置（78 FW + 16 SW）と14 LOSS sweep鍵が導出の全入力
- type: depends_on
  target: K0726
  note: focus2154の62証明書（27 WIN7 + 35 LOSS7）が再利用分類の入力
artifacts:
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_candidates_part1.csv
  role: data
  note: 候補S7表 s7_hex,s6_hex,move,cat（1=既知LOSS子、2=プール候補）。part1..3で計8,763行
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_stats.json
  role: manifest
  note: 導出anchor・md5一致・再利用分類の全計数
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ms5_s7_reuse_analysis.ts
  role: verifier
  note: 決定論的な再導出・再分類プログラム
- path: research/log/2026-11-13-n11-ms5-worklist-derivation-and-s7-reuse-partition.md
  role: log
  note: 経緯と再現上の注意（メモリ上限・実装上の修正点）
scope: n11 S2 {59,60} milestone-5のワークリスト検証とS7証明書再利用の会計。勝敗判定は含まない。
evidence: 再導出hex,cost,classes表（辞書順ソート）のmd5 0e95a438dbcb486368393de9c73fc21eが公開6パート連結と一致。anchor 3868/196/17524/479/13/10/7867/615497全一致。S7候補の分類は決定論的集合演算。
---

## 主張

1. milestone-5のS6ワークリスト7,867行（鍵・classes・cost全部門）は、K0675オラクル入力のみから Independent な再導出で公開manifestと**全行バイト一致**する（md5 0e95a438dbcb486368393de9c73fc21e、辞書順）。
2. ワークリストS6のoracle補完候補S7（|O\S6|=1かつx合法）は8,763個で、既知LOSS396・possible-win-pool 8,367の2値に**完全分解**され、未分類0・certWin直接一致0。

## 帰結

- 公開manifestの鍵集合・classes列・cost列は3系統（生成器・geometry監査・本再導出）で一致した。
- 外部レーンはcat=2の8,367鍵をwin_childプールと照合するだけで、hitした親S6を（K0675条件下で）WINとして即閉鎖できる。1,591個のS6はoracle補完候補を持たず、新規探索が必要。

## 限界

- 全てのwin/loss記述はK0675オラクル（78 FW + 16 SW）の条件付き。オラクルが崩れれば本項も崩れる。
- **11x11空盤・二石root {49,60}・S2 {59,60}はいずれもUNKNOWNのまま。**本項は勝敗を一切確定させない。
- possible-win-poolは「 witness候補」であって証明済みWIN7ではない。hitしたものだけが閉鎖になる。
