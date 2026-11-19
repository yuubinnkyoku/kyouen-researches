---
id: K1039
title: "head-1410 28-root witnessの全面depth-10判定（3 WIN・25 REFUTED・CAPPED 0）とK1038未試験witnessの実質解消"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - n11 witness 28-root full depth-10 sweep
  - 28-root witness full sweep verdicts
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0865
  note: head-1410の5親targetとS6 receipt簿記
- type: depends_on
  target: K1033
  note: 28-root witness（53行）の選定と生死プール
- type: depends_on
  target: K1035
  note: witness内の先行3候補判定（root C WIN・2 REFUTED）とその証明書
- type: depends_on
  target: K1036
  note: 第5・第6 WIN7-D10証明書
- type: depends_on
  target: K1038
  note: 第4receipt fold・refold後の26-root witness・stranded 40行分類（本sweepの突き合わせ基準）
- type: supports
  target: K0865
  note: depth-10 candidate poolから23 rootを新規除外確定（fold/resolve3は未実施・K1038簿記は不変）
artifacts:
- path: research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-sweep-20261119.json
  role: data
  note: 機可読sweep判定。28 rootの全判定・checks 7項・構造的帰結・解釈guard。SHA-256 a77eaac992f399282e81931cd18ba96f037491f48e1fb9cb01339c42220647f1
- path: research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-probe-records-20261119.jsonl
  role: data
  note: 全56 probe record（root/ordering/cap/bit/loss/nodes/capped/terminal_range・pilot_d6制御行つき）
- path: research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/scripts/probe_driver28.py
  role: source
  note: resumable probe driver。28 root inline・anchor assert・pilot制御検査つき
- path: research/log/2026-11-19-n11-witness-28-root-full-depth10-sweep.md
  role: log
  note: sweep実行・決定性アンカー照合・K1038突き合わせ・今後のfold/resolve3接続
scope: >-
  K1033のcover resolveが選定した28-root witness（53行）の全rootに対する
  depth-10判定と、その結果のK1038 refold未試験witness（26 root）への
  突き合わせ。ここにはreceipt fold・frontier簿記・再解決の更新を含まない。
  二石root・空盤・クラス全体の勝敗は対象外。
evidence: >-
  runner v17（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59）を
  K1033 cover resolve（blob 600b23d3…）が選定した28 root各々に、両AND順序
  （andclose1/andclose0）・cap 30,000,000均一で実行し、56 probeすべて
  未打切り（capped 0）で完了。pilot_d6制御（3,402 nodes・loss=false）は
  56/56でPASS、順序間のWIN/REFUTED矛盾は0。総nodesは
  andclose1=47,142,180・andclose0=120,224,379。判定はWIN 3
  （00000000000000801202060001000000=K1035・00000000000000805202080001000000
  と00000000040000801202000080100000=K1036、いずれも出版証明書のrootと
  SHA-256で一致）・REFUTED-D10 25（うち2 root 00000000000000003800000008001021
  と00000000020000801222000000100000はK1035の先行判定の機械的再現、
  残り23 rootが新規除外）。決定性アンカー3件が出版値と完全一致:
  root C 3,294,339/3,953,563 nodes（K1035出版値）、
  00000000000000003800000008001021 andclose1 926,192 nodes、
  00000000020000801222000000100000 andclose1 261,501 nodes
  （K1035 probe_runs。cap 30Mは両rootの非cap要件を満たす）。
  K1033簿記に対する構造的帰結: witness 53行のうち証明書つき3 WIN rootが
  cover主張で宣言する行はユニーク4行、残49行はこの28-rootプール内の
  depth-10 WIN7候補では閉じ不可（候補枯渇の体系的情報。
  数学的閉鎖不能証明ではない）。
  同日12:13出版のK1038（HEAD d3a6e69f）のrefold resolve
  （fold前簿記: 5親target 23/112・残余89行・eligible 60候補・
  26-root witness未試験）のuntested_witness_roots 26 rootと本sweepの
  28 rootをhex左ゼロ正規化で突き合わせた結果: 23 rootが本sweepで判定済み
  （WIN 2 = 第5root・第6root、証明書つき。REFUTED 21 = 当該
  eligibleプール内候補としての除外確定）。K1038の未試験witness残りは
  00000000000000403800000008100020・00000000020000801202000100100000・
  00000000000000889002000080100000の3 root（K1038計画上の被覆5行）のみ。
  21 REFUTED rootがK1038計画で被覆する予定だった42行（マッチング枠、
  2行×21 root）は本プール内のproviderを失う。行ごとの代替eligible候補
  の評価は未実施であり、次回の再解決（resolve3）で処理する。
  またplan-dependent行00000000000040809002000000100000のeligible provider
  2件のうち00000000000040889002000000100000を本sweepがREFUTED-D10で
  除外した（残るprovider 00000010000000801202040000000400は未試験）。
  本項ではreceipt fold・frontier簿記・再解決を実施しない。
  K1038の簿記（frontier 6,226行/492,970・solved 1,622・5親target 23/112・
  stranded 40）は不変のまま。
  REFUTED-D10は7石rootからdepth-10以内の先手勝ちなしの完全探索判定
  であり、それ以前の局面のLOSS証明ではない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---
