---
id: K1144
title: 残余72行 4掃引（K1086/K1089/K1091/K1095）depth-10 probe全件再実行の独立第二検証
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - independent second verification of the residual72 four sweep depth-10 probe records by full re-execution
  - greedy23 replace16 replace15 replace12 sweeps probe re-execution verification
relations:
- type: verifies
  target: K1086
  note: K1086の46 probeをrunner v17再実行で全field照合
- type: verifies
  target: K1089
  note: K1089の32 probeをrunner v17再実行で全field照合
- type: verifies
  target: K1091
  note: K1091の30 probeをrunner v17再実行で全field照合
- type: verifies
  target: K1095
  note: K1095の24 probeをrunner v17再実行で全field照合
- type: depends_on
  target: K1093
  note: K1093の幾何・台帳第二検証は再実行を対象外としており、本項はその空白を埋める
- type: depends_on
  target: K1097
  note: 4掃引verdictはK1097以降のpool構築の源流
artifacts:
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/README.md
  role: source
  note: 対象・入力SHA-256 pin・2 pass再実行方法・6 gate・検証境界
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/scripts/verify_sweeps_reexec_20261120.py
  role: verifier
  note: fail-closed 8入力SHA-256 pin・runner git blob照合・child指定再導入・出版内部整合・132 probe ×2 pass実行・6 gate assemble
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/runner_v17.ts
  role: verifier
  note: runner v17 pinned copy（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59）
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/output/verdict-sweeps-reexec-second-verification-20261120.json
  role: data
  note: 6/6 gate PASS・nodes総計37,454,794完全一致・3実行byte-identical
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/output/probe-records-reexec-passA.jsonl
  role: data
  note: pass A 132 probe生記録（SHA-256 1ade916b…）
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/output/probe-records-reexec-passB.jsonl
  role: data
  note: pass B（隔離cwd/HOME/入力）132 probe生記録（SHA-256 e351f6cc…）
- path: research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-second-verification.md
  role: log
  note: 着手判断・方法・結果・解釈規約
- path: research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-second-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言（commit 259e4019db・先行出版）
scope: >-
  K1086/K1089/K1091/K1095の4掃引depth-10 probe記録計132件（両AND順序・cap 30M・
  pilot_d6 control付き）のpinned runner v17による全件再実行。決定論的比較fieldは
  nodes・loss・capped・terminalStoneRange。出版記録の幾何・台帳照合はK1093/K1102が
  別途実施済みであり本項は再実行に専念する。新規probe・証明書抽出・receipt fold・
  S6行の閉鎖・行のゲーム理論的値は対象外。
evidence: >-
  4正本のrecord JSONとprobe-records JSONL計8ファイルをSHA-256 pinでfail-closed読み出し、
  runner v17をgit blob SHA-1 c132cc…で固定した。各recordのchild指定ルール（root −
  最小セットビット）を再導出し、protocol定数・pilot_d6 controlを132 record全件で
  検査した。出版内部整合（JSONL vs per_root）とclassification pin
  （WIN8-D10 7/3/3/3根・REFUTED-D10 16/13/12/9根・nodes総計18,032,471/6,339,079/
  7,383,022/5,700,222・capped 0・error 0）を最初に独立検査し、次に132 probe全件を
  同一tree（pass A）と隔離cwd/HOME/入力（pass B）の2 passで再実行した。
  6 gate（runner blob・出版内部整合・classification pin・passA-vs-出版・passB-vs-出版・
  passA-vs-passB）すべてPASS。264回の実行で不一致0・欠落0・timeout 0・capped 0、
  両passのnodes総計37,454,794が出版総計と正確に一致。監査JSONはtiming非依存で
  3実行byte-identical（SHA-256 6297c646…）。
---

## 判定範囲

WIN8-D10 candidateは証明書ではなく、REFUTED-D10はLOSS証明ではない。行は1つも閉じない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。
