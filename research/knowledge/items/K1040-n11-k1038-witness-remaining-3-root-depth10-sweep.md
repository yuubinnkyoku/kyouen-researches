---
id: K1040
title: "K1038未試験witness残り3 rootのdepth-10判定（K1038 26-root witness全root判定完了）"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - n11 K1038 witness remaining-3-root depth-10 sweep
  - K1038 26-root witness fully judged
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0865
  note: head-1410の5親targetとS6 receipt簿記
- type: depends_on
  target: K1033
  note: base→first→second/third fold連鎖・117root候補プール
- type: depends_on
  target: K1036
  note: 第5・第6 WIN7-D10証明書（witness内の2 WIN root）
- type: depends_on
  target: K1038
  note: 第4receipt fold・refold 26-root witness・root_checks（stones 7・D4 canonical・unsafe 0）
- type: depends_on
  target: K1039
  note: 26 root中23 rootの先行判定（WIN 2・REFUTED 21）
- type: supports
  target: K0865
  note: K1038 witness 26 root全root判定完了による候補枯渇情報の確定（fold/resolveは未実施・簿記不変）
artifacts:
- path: research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/output/k1038-witness-remaining-3-root-depth10-sweep-20261119.json
  role: data
  note: 機可読sweep判定。3 root×両順序の全判定・K1038 witness 26 root合算結果・checks 7項・解釈guard。SHA-256 416abfb093293cdb2222a1d697737d5bf7921bcbdb2a1e120990b2f71820af17
- path: research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/output/k1038-witness-remaining-3-root-depth10-probe-records-20261119.jsonl
  role: data
  note: 全6 probe record（root/ordering/cap/bit/loss/nodes/capped/terminal_range・pilot_d6制御行つき）
- path: research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/scripts/probe_driver3.py
  role: source
  note: resumable probe driver。3 root inline（K1038 root_checksの7石hexそのまま）・7石assert・pilot_d6制御検査つき
- path: research/log/2026-11-19-n11-k1038-witness-remaining-3-root-depth10-sweep.md
  role: log
  note: 3 root probe実行・K1038突き合わせ・26 root合算と次のfold/resolve接続
scope: >-
  K1038 refold resolveのwitness_sweep_plan.untested_witness_roots 26 rootのうち
  K1039が判定しなかった残り3 root（計画被覆5行）に対するdepth-10判定。
  ここにはreceipt fold・frontier簿記・再解決の更新を含まない。
  二石root・空盤・クラス全体の勝敗は対象外。
evidence: >-
  K1038（HEAD d3a6e69f）の26-root witnessのうちK1039が23 rootを判定済み
  （WIN 2=第5・第6root〔K1036証明書つき〕・REFUTED 21）。残る未試験3 root
  00000000000000403800000008100020・00000000020000801202000100100000・
  00000000000000889002000080100000（K1038 root_checksでstones 7・D4
  canonical・unsafe_quadruples 0、計画被覆はそれぞれsingleton 1行・
  matched 2行・matched 2行）をrunner v17（git blob
  c132cc6425eee3feaeef1d697dd74f968cfedb59）で両AND順序
  （andclose1/andclose0）・cap 30,000,000均一で判定し、6 probeすべて
  未打切り（capped 0）で完了。pilot_d6制御（3,402 nodes・loss=false）は
  6/6でPASS、順序矛盾0。nodesはandclose1 554,728（254,303/126,480/173,945）
  ・andclose0 1,502,205（565,069/354,926/582,210）。3 rootすべて両順序で
  uncapped loss=false、すなわちREFUTED-D10（WIN 0・CAPPED 0）。
  合算でK1038 witness 26 root全rootのdepth-10判定が完了した
  （WIN 2・REFUTED 24・CAPPED 0）。
  構造的帰結: K1038 witness 26 rootの被覆49行のうち、証明書つき2 WIN root
  （foldは未実施）が担う2行（00000000000000805202000001000000・
  00000000020000809002000040000000）を除く残47行は、この26-root witness
  プール内のいかなる7石rootのdepth-10 WIN7 receiptでも閉じられない
  （候補枯渇の体系的情報であり数学的閉鎖不能証明ではない。
  eligible 60候補のうちwitness外34候補は未試験のまま、候補プール拡張や
  depth>10 receiptの可能性は排除しない）。
  本項ではreceipt fold・frontier簿記・再解決を実施しない。
  K1038の簿記（frontier 6,226行/492,970・solved 1,622・5親target 23/112・
  stranded 40〔structural 36・plan-dependent 4〕）は不変のまま。
  REFUTED-D10は7石rootからdepth-10以内の先手勝ちなしの完全探索判定であり、
  それ以前の局面のLOSS証明ではない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWN。
---
