---
id: K1069
title: "残余78行の39 live witness（resolve6最大matching）depth-10全面掃引: WIN 1 / REFUTED-D10 38 / CAPPED 0・順序矛盾0・総nodes 169,615,508。WIN7-D10 root 00004000000000821082000000000100 が残余2行（82108...01/04・windfall4 fold閉鎖4行とは別行）を被覆、第17証明書抽出候補として確定"
kind: computation
status: computed
topics: [certificates, search-methods]
aliases:
  - single-owner execution of the K1063-declared 39 live witness depth-10 sweep (residual78 post-saturation scope, concurrency note published first)
  - 78 probes (39 roots x both AND orderings), runner v17 pinned blob c132cc64, cap 30M uniform, pilot_d6 control all-pass
  - 15 duplicated probes from slice-restart re-executed in separate processes with node-exact agreement (determinism cross-check)
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1063
  note: resolve6正本（SHA-256 e85d4bfb…c281a）のwitness_full 39 live root・残余78行・matching 39が本項の入力
- type: depends_on
  target: K1059
  note: 39witness掃引のdriver/protocol規約（runner v17・両AND順序・cap 30M・pilot_d6・生child・canon_hex禁止）
- type: depends_on
  target: K1066
  note: windfall4証明書抽出・三重検証の規約（本掃引WIN根の証明書化はこの規約を継承）
artifacts:
- path: research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json
  role: data
  note: 分類正本（SHA-256 22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc）。9 gate全PASS・fail-closed
- path: research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/driver.py
  role: verifier
  note: 4-worker resume-safe掃引driver（probe 280s timeout・records append resume）
- path: research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/assemble.py
  role: verifier
  note: 生記録からの独立分類組立（partition/duplicate-agreement/uncapped/pilot/order-consistency/covered-rows/anatomy gate）
- path: research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/roots.json
  role: data
  note: resolve6 witness_fullから機械生成（popcount==7・child|1<<bit==root gate込み・covered rows==残余78行）
scope: >-
  resolve6の39 live witness rootのdepth-10両順序判定まで。WIN根の証明書抽出・
  独立検証・receipt fold・行の閉鎖計上、depth-saturation audit、resolve7再照合、
  二石root・空盤の勝敗確定は対象外。
evidence: >-
  （1）入力pin: resolve6正本のSHA-256一致、runner v17はcommit-SHAピンraw取得で
  git blob SHA-1 c132cc6425eee3feaeef1d697dd74f968cfedb59を当環境で再計算一致。
  roots.jsonはwitness_full 39根（全7石・D4正準形・全safe）から機械生成、
  covered rowsの和集合==残余78行をgate検証。child = root − 最小セットビットの
  生整数hex（canon_hex禁止・K1046事故規約）。分解非依存性（runnerはchild+bitの
  盤面を解く）は39witness版READMEの検証実績どおり。
  （2）掃引: runner v17・depth 10・cap 30M均一・両AND順序（andclose 1/0）・
  4 worker・78 probe完走（2026-11-19 20:32Z〜20:41Z UTC、約9分。
  Mozilla級並列は4 workerのみ・共有サーバー高負荷回避規約どおり）。
  pilot_d6制御行は全probeでloss=false・3,402 nodes（runner内fail-closed＋
  assemble gate）。CAPPED 0・error 0。
  （3）結果: WIN 1（root 00004000000000821082000000000100、bit 8、child
  00004000000000821082000000000000、両順序loss=true・uncapped・terminal石数
  [13,17]、nodes 1,576,372〔andclose1〕/ 2,544,178〔andclose0〕、
  被覆行 00000000000000821082000000000001・00000000000000821082000000000004）/
  REFUTED-D10 38 / CAPPED 0 / 順序矛盾 0。総nodes 169,615,508、
  最大単一probe 14,249,420。
  （4）決定論: スライス再開に伴い同一(root, ordering) 15 probeが別プロセスで
  再実行され、nodes・loss・capped全てで完全一致（duplicate-agreement gate・
  不一致0）。run-to-run node-exact再現の追加証拠。
  （5）解釈規約: REFUTED-D10はLOSS証明でない。WIN根は証明書抽出候補であり
  抽出・独立二重検証・receipt foldまでは閉鎖計上しない。本掃引はそれ自体では
  どの行も閉じない（windfall4 foldで残余は78→74行になっており、WIN根の2行は
  その74行内）。38 REFUTED rootはdepth-10閉鎖witnessとして使用不能だが
  depth-saturation（永久使用不能）判定は別audit待ち。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
---

## 詳細

K1063（resolve6）が「witnessのdepth-10掃引・4 WIN rootの証明書抽出・receipt
foldは対象外。次の一手」として宣言した39 live witness掃引を、単一オーナー
調整ノート（research/log/2026-11-20-n11-residual78-39livewitness-sweep-concurrency-note.md）
を先行出版した上で実行した。resolve6の最大matching 39（stranded 0）は
残余78行を1回被覆で完全に覆う選択であり、本掃引はその選択計画の全根判定で
ある。結果はWIN 1 / REFUTED-D10 38で、windfall4（cache由来WIN4根・fold済み）
を除けばpost-saturationスコープで初のWIN根となる。

WIN7-D10 root `00004000000000821082000000000100` はhead-1410系
（0000000000000082108200000000…系D4像）の行ペア
（00000000000000821082000000000001・00000000000000821082000000000004）を
被覆し、windfall4 foldで閉じた4行（00000000000000003800000008001200・
00000000000000801202010000001000・00000000000000801202080000001000・
00000000010000003800000008100000）とは交差しない。証明書抽出・三重独立検証
（K1066規約）・第17receipt foldまでは被覆2行は閉鎖計上しない。
詳細は[実験](../../experiments/n11-residual78-39livewitness-depth10-sweep-20261120/README.txt)・[研究ログ](../../log/2026-11-20-n11-residual78-39livewitness-depth10-sweep.md)。
