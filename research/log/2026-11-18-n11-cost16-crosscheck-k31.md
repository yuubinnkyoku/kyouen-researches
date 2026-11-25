# 2026-11-18 N11 cost-16 生存曲線 crosscheck k=31拡張 — 112 checks・network/local両モード 0 failures・k=31出版4コミットの第三系統独立検証完了

直前のk=31本計算出版（script+log `cf8d7dcc`〔script blob `7a292ea91fd5c19758ed5b84cfda04a8a2caa155`〕・result JSON `5da4cc6c`〔blob `0d9f67ee69ad4fb8aa37904ddbf6666745786807`〕・record JSONL `a4bef2aa`〔blob `d308b6d537e8606dadef33c52cdade6cda109320`・5,362 records〕・log `bb0d6e3b`）を受けて、独立crosscheck script（`cost16_survival_k13_k14_crosscheck_20261118.py`）をk30まで（98 checks）から**k31までに拡張（112 checks）**し、network・local両モードで0 failuresを確認した。本拡張は実験scriptを一切importしない第三検証系統（pm再計算なし・出版数値の厳密BigInt算術とpinned aggregateからの独立census再導出とrecord joints単独の再加算のみ）である。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。**

## 拡張内容

- PINSにk31 result JSON（blob `0d9f67ee69ad4fb8aa37904ddbf6666745786807`）を追加・value layerの基準系列をk30→k31（K=31）に更新。marginal chain・monotonicity・reproduce anchors・kill series一致（k13〜k31全出版間）は自動的にk31点まで延長。新たに検証される生存点は kill(31)=2,526,118,818,461,447,714（85.156282%）・A_survive 352,166,075,034,634,327（11.871632%）・**B_survive 88,165,448,184,399,315（2.972086%・初の3%割れ・歴史最低）** で、出版JSONの小数点6桁のshare値もBigInt再計算と一致（5e-6 tolerance）。
- **preread erratumの独立確認が構造的に含まれる**: k31 JSONのsurvival.marginal detail m31=120,181,378,067,473,629がpinned aggregateのmembership（`marginal_le_membership_k14_k31` check）と厳密一致し、rank31_rootのa_part 92,082,202,719,887,124 / b_part 28,099,175,347,586,505もaggregate派生のmembership_A_part / membership_B_partと`rank_root_fields_match_aggregate_k16_k31` checkで一致する（A+B==M31厳密成立・prereadのNode double丸め3項〔120181378067473630 / 92082202719887120 / 28099175347586504〕が出版値に入り込んでいないことの第三系統確認）。census系は小整数で丸めの影響を受けない。
- quint era機構: 5-subset census機械再導出をn=31まで拡張（C(31,5)=169,911全件を独立classifierで再分類し、出版k31 JSONのcensus {b_only 6,787 / zero 163,124 / disjoint 0}・二重行hist {15:1,003, 16:239, 18:4,149, 19:1,396}〔rank-31 (18,26)では行26が史上初被覆で二重行族に一切参加しない構造事実と整合〕・`quints_zero_synth_count`=C(30,4)−819=26,586と厳密一致）。層接続checkに(31,30)を追加（full(31) − rank-31新層 819 b_only + 26,586 zero = full(30) census {5,968/136,538/0}）。
- record layer: k31 JSONL pin（blob `d308b6d537e8606dadef33c52cdade6cda109320`）を追加し、5,362 recordを全件再検証。quint era再導出で得た新b_only集合（819本）とrecord集合の集合としての一致も検証。

## k=31 record layerの検証結果（全PASS）

1. kind counts機械導出と厳密一致: pair 30 + triple C(30,2)=435 + quad C(30,3)=4,060 + quint 819（b_only再導出集合とrecord集合が集合として厳密一致）+ anchor2 4 + anchor3 2 + anchor4 2×2 + cross 3/4/5/q4 各2 = 5,362。
2. anchor4両lineage（lazypm/mypm）A/B joint一致・union再導出・anchor/cross record全match。anchor4の2 comboはk30出版record layerのdisjoint quads (4,13,25,29)/(4,16,25,29)。
3. 新quad census再導出 {b_only 986 / zero 3,025 / disjoint 49} がk31 JSON structureと厳密一致。新triple census C(31,3)=4,495={2,717/930/848}も全triple再導出と一致。
4. **I-E恒等式3本をrecord joints単独から厳密再加算**: marginal_total = 52,914,484,706,624,166・A型 41,353,998,417,711,129・B型 11,560,486,288,913,037が出版kill(k31)−kill(k30)のA/B分割と全一致（pm呼び出しに一切依存しない独立検証）。
5. 新pair 30本がちょうど15 shared / 15 disjoint（行18ハブ帯共有15本・行26は他のどの上位rootとも行を共有しない）であることもpair recordの行集合再導出から確認。

## 実行記録

- local mode（pinned入力JSON 18+agg+JSONL 6のsha1照合）112 checks 0 failures（約2秒）・network mode（jsdelivr + raw.githubusercontent fallback・全pin sha1照合・k31出版体をmainから取得）112 checks 0 failures（約9秒）。fail-loud sha1機構でk31出版直後のstale serveも検出されず。
- 112 checks内訳: 旧98 + k31 quint census/double-rows 2 + era接続 (31,30) 1 + k31 record layer 11。

本check拡張により、k=31のcost-16生存曲線は (a) 実験scriptの51 checks finalize（二重実行byte-identical）、(b) k=31 preread事前census（commit `188106bb`）と本計算JSON内のpreread_match 5検査・preread_erratum記録、(c) 本crosscheck（第三系統・record joints単独）の三系統で完全独立に検証された。生存曲線はban回避代替最小cover計画の組合せ数であり、勝敗に関する何らのverdictも生成しない。**標準11×11空盤はUNKNOWNのまま。**
