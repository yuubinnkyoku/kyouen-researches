---
id: K1059
title: "残余78行の39-witness depth-10掃引（WIN 0・REFUTED 39・CAPPED 0・順序矛盾0）と深さ飽和audit（d12/d14・残余分岐d16: 探索木は深さ14以内に飽和し全深さで先手勝ちなし、39 rootは閉鎖witnessとして永久使用不能）。候補poolは枯渇しておらず、次の一手は39 dead root除外後のresolve6再照合"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - execution of the resolve5 conditional plan (39 fresh pair witnesses covering the 78 residual rows)
  - 39-root depth-10 sweep with both AND orderings, cap 30M, pilot_d6 control (78/78 probes passed)
  - decomposition-independence check of the runner input (identical probe result for alternative min-bit decomposition)
  - depth-saturation audit of the 39 REFUTED roots (identical node counts at d12/d14 for 72 of 78 branches, d14/d16 for the 6 residuals; loss=false uncapped everywhere)
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
- path: research/experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/audit_candidate_supply_scope_20261120.mjs
  role: verifier
  note: resolve5の4,728 fresh-safe候補と39-root sweepの範囲を独立監査。4入力blob pin、D4・整数determinant安全性・削除被覆・78行pair matchingを検査
- path: research/experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/output/candidate-supply-scope-audit-20261120.json
  role: data
  note: 9 gate全合格。fresh-safe 4,728本のうちsweep39本の外に4,689本、706 pair辺のうち未選択667、78 singleton行は今回未使用。full 8,964 cache joinとpost-sweep matchingは未実施
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/depth-saturation/depth-saturation-audit-20261119.json
  role: data
  note: "深さ飽和audit正本（SHA-256 46afc523186cbd68225b70fcecc152951ebb8efde36bd1fc7d47f7f961ab24d5）。78分岐のd10/d12/d14（6残余分岐はd16）node対比・pilot gate・飽和分類（72: d12==d14、6: d14==d16）・d12総nodes 134,902,159（d10比+16.4%）"
- path: research/experiments/n11-residual78-39witness-depth10-sweep-20261119/depth-saturation/records-d12-w0.jsonl
  role: data
  note: depth 12生probe記録 worker0（40 record・pilot_d6 3,402 nodes全件合格）。records-d12/d14-w0/w1.jsonl・worker log・depth16残余分岐・driver-d12/d14.py・build scriptは同dirに同時出版

scope: >-
  K1057 resolve5 が計画した39本のfresh pair witness（残余78行の完全被覆）の
  depth-10両順序掃引の実行と分類、および39 REFUTED rootの深さ飽和audit
  （depth 12/14・残余分岐depth 16）まで。行の閉鎖・fold・二石root・空盤の
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
  **選択した39-root witness計画は全件REFUTED-D10で消費された**ことが確定した
  （fresh-safe候補集合全体の枯渇は未判定。追記参照）。
  （5）深さ飽和の追試: 同じ39 root・同じ(child,bit)分解・同じrunner・cap 30M・両順序で
  depth 12・14を全78 probe再実行（d12総nodes 134,902,159 = d10比+16.4%・d14総nodes
  134,917,058）。全probeでloss=false・uncapped・pilot_d6合格。72/78分岐はd12とd14のnode数が
  完全一致、差のあった6分岐（root 5個・うち1個は両順序）はdepth 16再probeでd14と完全一致。
  **runner v17の移動モデル・終端規則のもとでこの39 rootの探索木は深さ14以内に飽和し、
  全深さで先手勝ちが存在しない。この39 rootは残余78行の閉鎖witnessとして永久に
  使用不能**（node同一性による判定であり、verdictの読み替えではない。
  depth-saturation-audit-20261119.json）。
  （6）運用: セッション中の環境リセットによりローカルscratchを喪失したが、repo出版済みの
  pinのみから復旧して掃引を実施した（runnerのgit blob sha照合による同一性確認を含む）。
  K番号は並走レーン運用上の整理でK1058がfinite-field研究に割当済みのため本項はK1059。
  （7）解釈規約: REFUTED-D10および飽和裏付きのREFUTEDは、runner v17移動モデル内での
  各rootからの先手勝ち不存在のみを意味する。行のゲーム理論的値には一切言及せず、
  runner移動モデル外の着手・2石追加・他の閉鎖機構の可能性は否定しない。
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
---


## 追記: 39-root sweep後の候補供給範囲監査（2026-11-20）

K1059のsweepはresolve5が選んだ39本を全てREFUTED-D10とした。この39本は互いに素なpair matchingで残余78行を覆うが、resolve5正本の事前fresh-safe候補集合は4,728本であり、今回の入力はその39本だけである
。したがってこのsweep外のfresh-safe候補は4,689本。事前候補グラフには706個の異なるpair辺があり、選択matchingが使った39辺以外に667辺が残る。また78行全てにsingleton候補があり、今回の39本は全て2行pairなのでsingleton候補はこのsweepで消費されていない。

これは事前候補集合に関する範囲監査であり、sweep後の最大matchingを再計算したものではない。さらにresolve5の明示verdict結合は379 REFUTED / 168 WINで、K0863の8,964-root全体cacheとの結合ではない。よって4,689本が現在も全て未判定とも、別matchingが必ず残るとも主張しない。次は全体cacheをroot単位で再構成して候補へ結合し、39 REFUTEDを除外して再解決する。詳細は[実験](../../experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/README.md)と[研究ログ](../../log/2026-11-20-n11-residual78-candi
date-supply-scope-audit.md)。

## 追記: 39 REFUTED rootの深さ飽和audit（2026-11-19追試。追記セクションは出版順に並記）

REFUTED-D10がdepth>10に隠れた先手勝ちを残す可能性を閉じるため、同じ39 root・同じ(child,bit)分解・同じrunner v17でdepth 12・14を全78 probe（両AND順序・cap 30M・pilot_d6制御）再実行した。全probeでloss=false・uncapped。72/78分岐はd12とd14のnode数が完全一致し、差のあった6分岐（root 5個・うち1個は両順序）もdepth 16再probeでd14と完全一致した。d12総nodes 134,902,159（d10比+16.4%）。

**runner v17の移動モデル・終端規則のもとでこの39 rootの探索木は深さ14以内に飽和し、全深さで先手勝ちが存在しない。この39 rootは残余78行の閉鎖witnessとして永久に使用不能。**候補供給範囲監査（前節）と合わせると、正しい現状は「選択39-root計画の全滅＋39 rootの永久使用不能」であり、残余78行のadd-one-stone候補poolは枯渇していない。**次の一手はこの39 dead rootを除外した再照合（resolve6: 未選択667 pair辺・fresh-safe 4,689本のK0863 8,964-root全体cacheとの結合を含む）**である。この時点で初期出版文書の「候補供給枯渇（全行の被覆候補確実全滅の初波）」記述は撤回済みとする。

飽和はnode同一性による実験的判定であり、行のゲーム理論的値には一切言及しない。78行は1行も閉じず、frontier 6,213/492,021・solved S6 1,635・5親target 34/112は不変。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**詳細は[実験](../../experiments/n11-residual78-39witness-depth10-sweep-20261119/depth-saturation/README.md)。