# 2026-11-18 N11 cost-16 生存曲線 crosscheck k=30拡張 — 98 checks・network/local両モード 0 failures・k=30出版3コミットの第三系統独立検証完了

直前のk=30本計算出版（script+log `69b4e029`・result JSON `f6a08dc5`〔blob `9c24e7a30ad213d3b7675e620ec606b00f73a330`〕・record JSONL `b3b5ee32`〔blob `98062c66b522e8df6604cd508427f37b2fbe8220`・5,435 records〕）を受けて、独立crosscheck script（`cost16_survival_k13_k14_crosscheck_20261118.py`）をk29まで（84 checks）から**k30までに拡張（98 checks）**し、network・local両モードで0 failuresを確認した。本拡張は実験scriptを一切importしない第三検証系統（pm再計算なし・出版数値の厳密BigInt算術とpinned aggregateからの独立census再導出とrecord joints単独の再加算のみ）である。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。**

## 拡張内容

- PINSにk30 result JSON（blob `9c24e7a30ad213d3b7675e620ec606b00f73a330`）を追加・value layerの基準系列をk29→k30（K=30）に更新。marginal chain・monotonicity・reproduce anchors・kill series一致（k13〜k30全出版間）は自動的にk30点まで延長。
- quint era機構: 5-subset census機械再導出をn=30まで拡張（C(30,5)=142,506全件を独立classifierで再分類し、出版k30 JSONのcensus {b_only 5,968 / zero 136,538 / disjoint 0}・二重行hist {15:925, 16:221, 18:3,536, 19:1,286}〔行14はquad二重行族には初参加するがquint二重行族には入らない構造事実と整合〕・`quints_zero_synth_count`=C(29,4)−1,328=22,423と厳密一致）。層接続checkに(30,29)を追加（full(30) − rank-30新層 = full(29) census）。
- record layer: k30 JSONL pin（blob `98062c66…`）を追加し、5,435 recordを全件再検証。

## k=30 record layerの検証結果（全PASS）

1. kind counts機械導出と厳密一致: pair 29 + triple C(29,2)=406 + quad C(29,3)=3,654 + quint 1,328（b_only再導出集合とrecord集合が集合として厳密一致）+ anchor2 4 + anchor3 2 + anchor4 2×2 + cross 8 = 5,435。
2. anchor4両lineage（lazypm/mypm）A/B joint一致・union再導出・anchor/cross record全match。
3. 新quad census再導出 {b_only 1,302 / zero 2,241 / disjoint 111} がk30 JSON structureと厳密一致。
4. **I-E恒等式3本をrecord joints単独から厳密再加算**: marginal_total = 32,540,616,778,647,828・A型 25,598,110,010,638,470・B型 6,942,506,768,009,358が出版kill(k30)−kill(k29)のA/B分割と全一致（pm呼び出しに一切依存しない独立検証）。

## 実行記録

- local mode（pinned入力21+JSONLs 5のsha1照合）98 checks 0 failures・network mode（jsdelivr + raw.githubusercontent fallback・全pin sha1照合・k30出版体をmainから取得）98 checks 0 failures。network runはk30ファイル出版直後でもstale serveなし（sha1検査で実証済みのfail-loud機構がそのまま有効）。
- 98 checks内訳: 旧84 + k30 quint census/double-rows 2 + era接続 (30,29) 1 + k30 record layer 11。

本check拡張により、k=30のcost-16生存曲線は (a) 実験scriptの46 checks finalize、(b) preread独立census導出（commit `43323db78`系列）、(c) 本crosscheck（第三系統・record joints単独）の三系統で完全独立に検証された。生存曲線はban回避代替最小cover計画の組合せ数であり、勝敗に関する何らのverdictも生成しない。
