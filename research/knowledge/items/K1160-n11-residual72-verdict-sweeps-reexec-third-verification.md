---
id: K1160
title: "残余72行 4掃引depth-10全probe再実行第二検証（K1144）のpristine再実行第三検証: 132 probe×2 passの出版byteのみからの完全再実行・4 fresh run（隔離tree/cwd/HOME・PYTHONHASHSEED=0/random含む）・assemble監査正本6297c646…の3 pair byte再生・tamper 2件fail-closed捕捉"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - "third verification (post-publication pristine re-execution) of K1144: from published bytes only (machine 7f072984, runner v17 git blob c132cc64, 4 sweep masters, published passA/passB JSONL, published assemble audit 6297c646), a post-publication third party re-ran the machine's 132-probe depth-10 full re-execution pass four times (runA same-cwd 114.9s; runB isolated tree/cwd/HOME 114.1s; runC PYTHONHASHSEED=random 112.3s; runD PYTHONHASHSEED=0 109.9s); every run reproduced all 132 probes (err/capped/timeout 0, nodes total 37,454,794, pilot_d6 3,402 x 132) with deterministic fields equal to the published records"
  - "assemble canonical byte reproduction: the machine's assemble mode on the fresh runs emitted, for all three passA-variant x passB pairings, output byte-identical to the published canonical audit 6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637 (6/6 gates, fresh nodes total 37,454,794 == published)"
  - "structural reproducibility note: the machine's run-mode JSONL embeds per-probe wall_s (timing), so published pass JSONLs are not byte-reproducible by construction; the byte-reproducible canonical artifact is the assemble audit JSON; the harness pins published run JSONLs as provenance and reproduces deterministic-field equality plus canonical-audit byte equality"
  - "tamper fail-closed: 1-byte XOR mutations of the K1086 record JSON (offset 500, sha 83520f33) and the K1095 probe-records JSONL (offset 300, sha b6cf0f86) are each caught by the machine's SHA-256 pins before any probing (exit 1, no records written); no row closed, no game-theoretic content added"
relations:
  - type: verifies
    target: K1144
    note: "残余72行 4掃引（K1086/K1089/K1091/K1095・132 probe）depth-10全probe再実行第二検証（出版commit c84e2b0e・machine 7f072984…・assemble監査 6297c646…）の、出版後の別実行者によるpristine再実行第三検証。fresh 4 run×132 probeの決定論的field完全一致とassemble監査のbyte再生で確定"
  - type: depends_on
    target: K1086
    note: greedy23掃引正本（record 3045e152…・JSONL 773fef42…・46 probe）
  - type: depends_on
    target: K1089
    note: replace16掃引正本（record 808fbda1…・JSONL 75fda6ad…・32 probe）
  - type: depends_on
    target: K1091
    note: replace15掃引正本（record edd7ac84…・JSONL 47165331…・30 probe）
  - type: depends_on
    target: K1095
    note: replace12掃引正本（record 335eca5e…・JSONL 89e2c30d…・24 probe）
artifacts:
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/README.md
  role: document
  note: "実験README（14 pin表・4 fresh run表・assemble 3 pair byte一致表・tamper 2件・harness仕様・宣言転写訂正・再現コマンド・解釈規約）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/scripts/verify_k1144_reexec_third_20261120.py
  role: verifier
  note: "第三検証harness（stdlibのみ・fail-closed・乱数・時刻・絶対path出力なし・14 fail-closed pin+4 gate・SHA-256 990977e5143bc6fd…・16,729 bytes）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/output/third-verification-audit-20261120.json
  role: data
  note: "監査正本（SHA-256 c32a1963d3a1ab611b0c67f8b540e8d896ebebdb587ae1510df519bc4cfae467・7,906 bytes・pin 14/14・fresh-run 4/4・assemble 3/3 byte一致・tamper 2/2捕捉・interpretation_guard同梱・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random 1回の3実行byte-identical）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/
  role: data
  note: "第三検証者のfresh再実行4本（runA same-cwd・runB isolated-cwd-home・runC hashseed-random・runD hashseed-0・各132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）"
- path: research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification.md
  role: log
  note: "実行記録（取得→宣言→4 fresh run→assemble byte再生→harness→part1出版・fetch-back 20/20）"
- path: research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit 9b3807a310a53285fa7d2799bd819290e52b3168…・2026-11-20T16:14:18Z宣言・先行出版。本文の出版監査SHA 1文字転写…8b3750…→正…8b3350…はitem/log/実験READMEで訂正記録・宣言原文は保持）"
scope: >-
  K1144（残余72行 4掃引 depth-10 132 probe全件再実行第二検証・出版commit c84e2b0e）の
  pristine再実行第三検証。出版byte（機械 7f072984・runner v17 blob c132cc64・4掃引正本8ファイル・
  出版passA/passB JSONL・出版assemble監査 6297c646）のみを起点に、(1) 14 pin機械照合、
  (2) 機のrun modeでfresh再実行4回（各132 probe・隔離/hasheseeed環境含む・決定論的field完全一致）、
  (3) assemble mode 3 pair全てで出版監査byte再生、(4) tamper 2件fail-closed確認、
  (5) 第三検証harnessの監査正本3環境byte一致。行は1行も閉じない。
---

# 残余72行 4掃引depth-10全probe再実行第二検証（K1144）のpristine再実行第三検証

K1144（出版commit `c84e2b0e`）は、残余72行レーンの4掃引
（K1086 addtwo greedy23・K1089 replace16・K1091 replace15・K1095 replace12・計132 probe）の
depth-10記録をpinned runner v17で全件**再実行**した独立第二検証であった。
本項目はその出版後の第三検証である: 出版byteだけをGitHubから再取得した第三者が
機を何も加えないpristineのまま再実行し、132 probe × 2 passの再実行宇宙が完全に再生できること、
assemble監査正本 `6297c646…` が自前のfresh runからbyte単位で再生できることを確定した。

## 確定したこと

1. **出版byteの再取得とpin照合 14/14**: 第二検証機 `7f072984…`（27,091 bytes）・
   runner v17（SHA-256 `192903714b…`・git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
   4掃引正本8ファイル（record JSON 4 + probe JSONL 4）・出版passA/passB JSONL
   （`1ade916b…`/`e351f6cc…`）・出版assemble監査（`6297c646…`）が全てpin一致。
2. **fresh再実行4回**: 機のrun mode（budget 240・worker 4・resume-safe・出版プロトコル引数そのまま）で
   132 probe全件を4環境で実行（同一cwd・隔離tree複製+別cwd+隔離HOME・PYTHONHASHSEED=random・
   PYTHONHASHSEED=0・各110〜115秒・err/timeout/capped 0）。4回とも全132 probeの決定論的field
   （label/root/ordering/depth/bit/child/cap/timeout・result nodes/loss/capped/
   terminalStoneRange・pilot_d6 control nodes 3,402）が出版passA/passB記録と完全一致・
   nodes総計 37,454,794。
3. **assemble正本のbyte再生 3 pair**: 機のassemble modeにfresh runを渡すと
   runA×runB・runC×runB・runD×runBの全pairで出力SHA-256が出版正本
   `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637`（7,327 bytes）と
   一致し、byte比較でも出版監査と完全一致（6/6 gate PASS）。
4. **tamper fail-closed 2件**: K1086 record JSON offset 500（改変後SHA `83520f33…`）と
   K1095 probe JSONL offset 300（改変後SHA `b6cf0f86…`）の1 byte XOR 0x01が、
   いずれもprobe起動前に機のSHA pin gateで捕捉（exit 1・記録未書込）。
5. **harness決定性**: 第三検証harness（`990977e5143bc6fd…`・16,729 bytes・stdlibのみ）の監査正本
   `c32a1963d3a1ab611b0c67f8b540e8d896ebebdb587ae1510df519bc4cfae467`（7,906 bytes）は
   同一cwd 2回＋隔離tree/cwd/HOME+PYTHONHASHSEED=random 1回の3実行でbyte-identical。
   harness初版のrunner ts pin定数SHA転写誤りはharness自身のfail-closed pinが実行前に捕捉した。

## 構造的知見（新規実験事実）

- **run出力のbyte非安定は機械設計由来で正本はassemble監査**: 第二検証機のrun modeは
  per-probe記録に`wall_s`（実行秒）を埋めるため、run JSONLのbyteはタイミングで変わる
  （出版passA/passB JSONLも同様・両者のbyteが異なるのはこのため）。byte再現の正本は
  assemble監査JSONであり、toggle gate（wall非依存）のみを含むため完全byte安定する。
  第三検証は「決定論的field完全一致 + assemble監査byte再生」の2層で確定した。
- **1パス1コマンド分割の復元可能性**: 機のrunはbudget 240s・resume-safeなので、
  実行環境の1コマンド300秒制限下でも1パス1コマンドで4 fresh runを完走できる
  （第二検証出版時の「1回のbash呼び出しに収まらない」制約はパス分割で回避可能と確定）。

## 実行しなかったこと・不変のもの

- 132 probeのdepth-10 verdict（WIN8-D10候補16根・REFUTED-D10 50根の再導入分類）は
  第二検証と一致するが、これはdepth-10探査の再現であり勝敗決着ではない。
  REFUTED-D10はLOSS証明ではなく、WIN8-D10候補は証明書ではない。
  nodes数・solved数を勝敗として読まない。
- 行は1行も閉じない。残余宇宙の簿記は不変。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/README.md)・
[harness](../../experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/scripts/verify_k1144_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/output/third-verification-audit-20261120.json)・
[fresh runs](../../experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/)・
[研究ログ](../../log/2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification.md)・
[単一オーナー宣言](../../log/2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification-single-owner-note.md)。
