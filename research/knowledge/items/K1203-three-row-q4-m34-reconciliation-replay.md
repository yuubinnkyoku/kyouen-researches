---
id: K1203
title: "M_{3,4}=24はK0351で先行確定済み — 2026-11-21の3行q=4レーン群の区間表記はレーン内有効な再検証であり、K0351計算背骨は第三実装（Node.js移植）でm=24..68全45幅bit-exactに再生"
kind: verification
status: verified
topics: [rectangles, variants, maximal-safe, verification, provenance]
aliases: ["K0351 engine replay", "three-row q4 corpus reconciliation"]
relations:
- type: verifies
  target: K0351
  note: "K0351エンジンq34_support_exclusion.cpp（sha256 6960331d…）のNode.js文対文移植でm=24..68全45幅を再掃引し、出版正本q34_exact_threshold.json（e08c4aba…）とthree_sets・cover_exists・両候補計数・witnessの全比較フィールドでbit-exact一致（検証機45/45 gate PASS・m=24,34,40再実行一致）。m=23では出版witness両系を座標レベルで再発見。K0351のstatus・本文は不変"
- type: related
  target: K1183
  note: "witness band m=4..23・witness-free {24..31}・区間表記M_{3,4}∈[24,69]（m≥32未掃引）はレーン内の有限検証範囲で有効な記述であり、Mの確定値はK0351/K0302が先行してprovedで出版済み（本項のリコンサイル判断）。K1183のwitness 3件は本レーンの3系統検証でもPASS。本文・status不変"
- type: related
  target: K1202
  note: "def-mode m≤68の自己完結第2certificateと系3の掃引窓縮減はK0351の先行証明と整合し、残り幅32..68の有限掃引は本レーンの第三実装再生で独立に満たされた（ただし手法は同一アルゴリズムの移植であり、K1183の列挙閉包・SAT・K1202計数が独立手法の交叉裏付け）。本文・status不変"
- type: related
  target: K0302
  note: "5閾値確定（24,12,16,13,11）のうちのM_{3,4}=24。mwq_stabilization.csv行exact-threshold,3,4,4,24,proved,K0351;K0302;K0068と整合。本文不変"
- type: related
  target: K0068
  note: "下界witness（rows {0:[4,15,18],1:[18,19],2:[9,12,18]}）はq34_deficient_witness_audit.py・kit witness_check.py（整数行列式）の両系で新環境再検証PASS。本文不変"
artifacts:
- path: research/experiments/three-row-q4-k0351-replay-20261121/README.md
  role: proof
  note: "検証方法・全結果・事故2件（JS shift-mod-32ポートバグ修正・背景二重書き込み破棄）の誠実記録・再現手続き・解釈規約"
- path: research/experiments/three-row-q4-k0351-replay-20261121/scripts/q34_exclusion_port.js
  role: verifier
  note: "K0351エンジンのNode.js移植正本（sha256 a11e0091d5c3…）。unsigned __int128→3×32bit語・popcount/整数sqrt同型・ループ順序・枝刈り閾値・(k&&j<i)対称カット・候補計数位置すべて原本どおり"
- path: research/experiments/three-row-q4-k0351-replay-20261121/scripts/verify_port_vs_published.py
  role: verifier
  note: "出版正本とのbit-exact照合機（three_sets/cover_exists/candidates_exact/witnesses_equalの45幅gate）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/port_sweep_24_43.jsonl
  role: data
  note: "m=24..43生掃引出力20行（全幅cover_exists [0,0]・両候補計数）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/port_sweep_44_68.jsonl
  role: data
  note: "m=44..68生掃引出力25行"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/verify_24_68.json
  role: certificate
  note: "照合機出力widths_checked 45・widths_ok 45・all_ok true"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/m23_rediscovery.jsonl
  role: data
  note: "m=23 witness再発見（出版m23_outer/middleと座標一致・cover_exists [1,1]）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/m32_rerun.jsonl
  role: certificate
  note: "ポートバグ修正後のm=32再掃引（出版候補計数[2854244,1031094]とbit-exact）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/witness_check_3system.out
  role: certificate
  note: "witness 3件の第三系統検証（整数行列式 witness_check.py・ok=true size=8）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/deficient_witness_audit_rerun.out
  role: certificate
  note: "出版q34_deficient_witness_audit.pyの新環境再実行（管理witness 3/3 PASS・determinant述語とFraction幾何述語の全4点組一致検証込み）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/q34_independent_recheck_rerun.json
  role: certificate
  note: "出版q34_independent_recheck.pyの全再実行出力（3独立述語A/B/C・全内部検査PASS）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/input-pins.md
  role: manifest
  note: "使用出版正本のsha256 pin表（cpp・threshold JSON・audit JSON・検証py×2・witness_check.py）"
- path: research/experiments/three-row-q4-k0351-replay-20261121/output/sha256_manifest.txt
  role: manifest
  note: "実験dir全ファイルのsha256表"
- path: research/log/2026-11-21-three-row-q4-k0351-replay-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（宣言時HEAD・対象・受入条件5項目・非目標）"
---

# M_{3,4}=24はK0351で先行確定済み・K0351計算背骨の第三実装再生

## 1. コーパス・リコンサイル（確認事実）

**M_{3,4}=24は2026-10-03にK0351（status: proved、以降不変）で証明・出版済みである**。K0302は5閾値確定（24,12,16,13,11）のひとつとしてM_{3,4}=24を主張し、K0068は下界witness M_{3,4}≥24を与え、`results/fixed-width/mwq_stabilization.csv`の行`exact-threshold,3,4,4,24,proved,K0351;K0302;K0068`がmachine-readable正本である。証明構造は (i) m≥69の一般上界、(ii) 外部2行の安全な完了、(iii) 対象行の一行被覆問題への正確な縮約、(iv) 2つの安全な枝刈り、(v) m=24..68の有限完全排除、(vi) m=23の8石極大witnessからなる。

2026-11-21の3行q=4レーン群（K1183〔m28レーン・witness band 4..23+witness-free {24..31}〕、K1202〔def-mode m≤68の自己完結第2certificate〕、m≥32治具拡張レーン〔宣言3aa6fb7f・wsearch35系〕）は、いずれもK0351/K0302/K0068をrelationsに持たず、K1183のtitleは「M_{3,4}∈[24,69]（m≥32未掃引）」、K1202本文は「37幅32..68の有限掃引は依然必要」と記述している（2026-11-21T13:05Z HEAD `e9e3bea5`で確認）。

本項の判定: **反証・矛盾は皆無であり、すべての成果はM_{3,4}=24と整合する**（witness bandは23で終端・24..31 witness-free・def-mode は m≤68・m≥69はK0024/K1202の一般上界と一致）。したがってこれらの区間表記はレーン内の有限検証範囲に関する有効な記述であり、Mの確定値としてはK0351/K0302が先行する。m≥32治具レーンの掃引（および他の任意の手法）は先行証明に対する第3の独立検証として位置づけられる。

**矛盾検出インターフェース**: 何らかの手法がm≥24の任意の幅で行欠損極大安全配置を発見した場合、それはK0351（proved）とのmaterial conflictであり、statusのretraction審査対象である。本レーンの全幅再生はこの方向の反例をm=24..68の全45幅で発見していない。

## 2. 第三実装による計算背骨の再生（本項の検証対象と範囲）

K0351エンジン`q34_support_exclusion.cpp`（sha256 `6960331d…`）をNode.jsに文対文移植（`unsigned __int128`→3×32bit語、popcount・整数sqrt補正は同型、ループ順序・枝刈り閾値`|base|<m−32`・`|base∪support|<m−14`・k=1の半領域カット・候補計数位置は原本どおり）し、m=24..68全45幅を新環境で再掃引した:

- **45/45幅でbit-exact一致**: three_sets、cover_exists [0,0]、両kindの候補計数（全掃引での候補対合計46,840,024の枝刈り通過列がpublish値と同一順序で再現）、witness全域null。
- m=23では出版`q34_audit.json`の`m23_outer_witness`・`m23_middle_witness`を座標レベルで同一の優先順序で再発見（cover_exists [1,1]）。
- witness 3件（再発見2件+K0068下界1件）は3系統で検証PASS: 出版`q34_deficient_witness_audit.py`再実行（管理3/3）、kit`witness_check.py`（整数行列式）、`q34_independent_recheck.py`全再実行（独立述語A〔Fraction円方程式〕/B〔Q上ランク〕/C〔F_1000003ランク〕全一致）。
- 決定性: m=24/34/40の再実行で比較可能フィールド全一致。
- 事故: 初版ポートにJS shift-mod-32起因のm=32/m=64偽witnessバグがあったが、出版値との照合で即検出し`2**m`表現に修正、修正後の両幅はbit-exact（m32_rerun.jsonl）。中間の二重書き込み事故ファイルは破棄し単一起動で再生成。

## 3. 制限（検証水準の明示）

- ポートはアルゴリズム忠実度が高いため、原本から翻訳された誤りが両系で同一に現れる場合はbit-exact一致では検出できない。独立手法（K1183の列挙閉包・SAT・K1202の計数上界）およびwitnessへの独立述語群がこの制限を交叉裏付けする。
- 本項はK0351証明の数学的部分（外部行完了補題・縮約の健全性・m≥69一般上界）を再証明しない。
- K1183/K1202/K0351/K0068/K0302の本文・statusは一切不変（relationsは本項側にのみ記述・逆リンクは生成器負担）。
- 計算結果を全称定理として読み替えない。checked数・seconds数を勝敗として読まない。
- Pの幅単調性は未証明のまま。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は本レーンと無関係でUNKNOWNのまま。**
