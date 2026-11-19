---
id: K1059
title: "残余78行の39-witness depth-10掃引（resolve5条件付き計画の実行）: WIN 0・REFUTED 39・CAPPED 0・順序矛盾0（総nodes 115,940,695）で add-one-stone・depth-10レーンのfresh候補供給がこのスコープで枯渇。行は閉じずfrontier不変"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - execution of the resolve5 conditional plan (39 fresh pair witnesses covering the 78 residual rows)
  - 39-root depth-10 sweep with both AND orderings, cap 30M, pilot_d6 control (78/78 probes passed)
  - decomposition-independence check of the runner input (identical probe result for alternative min-bit decomposition)
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K1046
  note: 117-rootプールdepth-10完全判定・残余86行strandedの設定
- type: depends_on
  target: K1057
  note: resolve5の39 pair witness・残余78行完全被覆（stranded 0）が本項の入力計画
- type: depends_on
  target: K0865
  note: head-1410の5親targetとS6 receipt簿記（frontier座標）
artifacts:
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/roots.json
  role: data
  note: 39 witnessのrunner入力（child=root−最小セットビットの分解・covered rowsはresolve5のcoveringをそのまま記録・child|(1<<bit)==rootの構造gate通過・和集合78行）
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json
  role: data
  note: 掃引分類正本（WIN 0・REFUTED 39・CAPPED 0・conflict 0・SHA-256 f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246）
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/probe-records-w0.jsonl
  role: data
  note: 生probe記録 worker0（40 record・pilot_d6 3402 nodes全件合格）
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/probe-records-w1.jsonl
  role: data
  note: 生probe記録 worker1（38 record）
scope: >-
  K1057 resolve5 が計画した39本のfresh pair witness（残余78行の完全被覆）の
  depth-10両順序掃引の実行と分類まで。行の閉鎖・fold・二石root・空盤の
  勝敗確定は対象外。
evidence: >-
  （1）入力: resolve5正本（SHA-256 5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e）
  のwitness_full 39 root。runner v17 git blob c132cc6425eee3feaeef1d697dd74f968cfedb59
  （Repo内 n11-s2-5960-ms5-s7-reuse-20261113/scripts、ダウンロード後git blob sha1照合一致）、
  depth 10・cap 30M・両AND順序・pilot_d6制御・生maxbit child（canon_hex被せ禁止規約）。
  （2）分解規則: 各rootの(child,bit)はchild=root−最小セットビット。分解はprobeに非依存
  であることを実験確認: sweep43 root 00000000000000003800000008001081を出版時分解(bit 61)
  と代替分解(bit 0)の両方で両順序probeしnodes 3,164,139/loss=false/capped=falseが完全一致。
  （3）実行: 39 root×2順序=78 probe（worker0 40・worker1 38）。pilot_d6（3,402 nodes・
  loss=false）は全78 probeで合格。分類GATE（両順序完走・uncapped・partition一致）通過。
  結果: **WIN 0 / REFUTED 39 / CAPPED 0 / 順序矛盾0**、総nodes 115,940,695（最大単一probe
  9,930,490 nodes）。
  （4）帰結: REFUTED-D10はLOSS証明でないため78行は1行も閉じない。frontier・5親targetは
  K1057 fold後のまま（6,213行/492,021・solved S6 1,635・5親target 34/112・残余78行）。
  43-pair掃引のdeflation（4 WIN+39 REFUTED）後に再結合した39 fresh pairが全滅し、
  **残余78行に対するadd-one-stone・depth-10レーンのこのスコープの候補供給は枯渇**した
  ことが確定した（全行の被覆候補確実全滅の初波）。
  （5）運用: セッション中の環境リセットによりローカルscratchを喪失したが、repo出版済みの
  pinのみから復旧して掃引を実施した（runnerのgit blob sha照合による同一性確認を含む）。
  K番号は並走レーン運用上の整理でK1058がfinite-field研究に割当済みのため本項はK1059。
  （6）解釈規約: REFUTED-D10はdepth-10内の先手勝ちなし完全探索のみを意味する。
  深さ>10・2石追加・他の閉鎖機構の可能性は否定しない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
