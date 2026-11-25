---
id: K1082
title: K1069 depth-10 39根掃引のper-probe nodeコスト台帳と出版集計の全数再導出照合
kind: computation
status: computed
topics: [search-methods, verification, statistics]
aliases: [K1069 node cost ledger, per-probe ledger re-derivation]
relations:
- type: verifies
  target: K1069
  note: 78 probe全数再実行によりK1069出版summary（総nodes 169,615,508・最大probe 14,249,420・WIN1/REFUTED38/CAPPED0/順序矛盾0）を厳密再導出・照合し、39根の分類ラベル・出版per-probe値3件とも一致
artifacts:
- path: research/experiments/n11-k1069-nodecost-ledger-20261120/output/k1069-nodecost-ledger-20261120.json
  role: data
  note: 正本SHA-256 b55e5d83… （ledger 78行・by_root 39行・gate 10/10 PASS）
- path: research/experiments/n11-k1069-nodecost-ledger-20261120/output/probe-records-k1069ledger.jsonl
  role: data
  note: 生probe記録78行（pilot_d6制御付き・全てuncapped・error 0）
- path: research/experiments/n11-k1069-nodecost-ledger-20261120/scripts/k1069_nodecost_ledger_20261120.py
  role: verifier
  note: membership・SHA pin・出版per-probe pin・depth-11標本拡張クロスチェック・集計再導出のfail-closed監査機械
- path: research/experiments/n11-k1069-nodecost-ledger-20261120/README.md
  role: source
  note: 手法・上位root表・丸め観察・再現手順
- path: research/log/2026-11-20-n11-k1069-nodecost-ledger.md
  role: log
  note: 単一オーナー宣言・着手判断・結果・供給判断への含意
scope: >-
  K1069 39-live witness depth-10掃引（正本SHA-256 22953ae1…）classification全39根・両AND順序
  （andclose 1/0）・depth 10・cap 30M・timeout 280s・runner v17固定コピーによる78 probe全数の
  再実行、per-probe node台帳の導出、およびK1069出版summary集計との照合。
evidence: >-
  78/78 probe完走・capped 0・error 0・pilot_d6制御全合格・76/78 probeが別cwd別プロセスの
  assembleでbyte-identical。再導出summaryは総nodes 169,615,508（厳密一致）・最大probe 14,249,420
  （root 00000000010000809002000040000080・andclose0・厳密一致）・WIN 1・REFUTED 38・CAPPED 0・
  順序矛盾 0の全項目でK1069出版値と一致。出版per-probe pin 3件・depth-11標本拡張（K1081系列）
  のD10測定8件とも厳密一致。39根ラベル整合0不一致。搬送の観察: 出版avg 2,174,557は
  169,615,508/78=2,174,557.79の切り捨て（総和は厳密一致・数学的内容への影響なし）。
---

## 命題と範囲

本項は有限計算（computation）であり、per-probe nodeコスト台帳と出版済み集計の独立再導出を
提供する。判定・分類・行の閉鎖は行っていない（K1069の出版済み判定の検証であり、その意味を
変えない）。

## 根拠

K1069正本のclassification 39根を生child hex規約（child=root−最小セットビット）で機械再導出し、
K1075掃引driverと同一引数形式（depth 10・cap 30M・timeout 280s・pilot_d6制御・逐次）で
78 probe全数を再実行した（総nodes 169,615,508・逐次約7分・sandbox）。assembleは10 gate
（runner blob pin・raw-child再導出39・K1069正本SHA pin・78 probe完走・pilot_d6全合格・
出版per-probe pin 3件・depth-11標本拡張クロスチェック8件・probe誤り0・集計再導出・
39根ラベル整合）をfail-closedで検証し、10/10 PASS。

## 台帳上の観察（コスト計画への利用）

- root別両順序合計nodesは約1.24×10^5から1.70×10^7の約2桁幅。
- 順序非対称: 最大probeのrootはandclose0=14,249,420に対しandclose1=2,731,659（約5.2倍差）。
  順序別root配置（どちらのorderingを先に走らせるか）で最大probeを抑制できる可能性。
- 正本JSONのby_root（39行）・ledger（78 probe行）がroot別コスト台帳を成す。

## 限界と解釈規約

再実行はK1075掃引と同一の決定論的プローブに基づくが、K1069の実行環境（4 worker並列）の
生worker logとは独立であり、worker logの所在・完全性はK1069レーンの管轄。capped/timeoutは
いかなる方向の証拠にもならない（本実験でcapped 0）。REFUTED-D10はLOSS証明ではない。
本台帳は行を閉じない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4はすべてUNKNOWNのまま。
