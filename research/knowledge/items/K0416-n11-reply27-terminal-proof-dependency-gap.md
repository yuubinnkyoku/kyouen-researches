---
id: K0416
title: 二石root {60,27} のterminal-only証明には2,992個の未閉鎖S5依存根が残る
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0414
  note: 119/119 solver-trusted LOSS proofと32個の使用S4 LOSS class
- type: depends_on
  target: K0372
  note: terminal-only検査器、cache隔離、trusted leafの区別
- type: depends_on
  target: K0375
  note: 現S4配下3根の共有terminal-only証明
- type: depends_on
  target: K0377
  note: 同3根のcompact witness-switch証明
- type: depends_on
  target: K0378
  note: 6根統合DAGから再利用できるterminal-only subset
artifacts:
- path: research/experiments/n11-reply27-terminal-proof-priority-20261012/README.md
  role: source
  note: 依存分析、asset再利用、pilot優先順位、限界
- path: research/experiments/n11-reply27-terminal-proof-priority-20261012/scripts/analyze_proof_gap.py
  role: verifier
  note: S4全S5境界を独立再生成し、cache root・既存DAG重複を数える
- path: research/experiments/n11-reply27-terminal-proof-priority-20261012/output/terminal-proof-priority.json
  role: data
  note: 2,995必要S5根、K0375/K0378重複、pilot候補とSHA-256
- path: research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json
  role: certificate
  note: 32 S4 witness classと119 root-move cover
- path: research/experiments/n11-proof-dag-incremental-20261011/output/integration-audit.json
  role: manifest
  note: K0378 six-root terminal-only proof audit
scope: K0414 `{60,27}` root LOSS proofで使われた32 S4 classから導かれる2,995個の異なるS5 LOSS依存根。terminal-only独立DAGは今回生成しない。
evidence: 独立BoardがS4→S5の3,297 dependency edgeを再生成し、2,995個のunique S5 root全てに現行exact cacheのLOSSがあることを照合した。cache `nodes>0` は65根（合計388,074,801 nodes）、`nodes=0` は2,930根。K0378の6根終局閉包DAGと依存集合の交差は3根で、残る2,992根はこのanalysisでは閉じていない。K0375/K0377も同じ現S4配下の三根資産。solver captureと再探索は実施せず、direct-node低・中・高標本の候補を優先順位として保存した。node countからcertificate費用を外挿せず、root lossはsolver-trusted leavesを使う。
---

K0414で使った32個のS4 LOSS classは、全3,297本のS4→S5 edgeを通じて2,995個の異なるS5 LOSS根に依存する。現行exact cacheの全根verdictはLOSSだが、終局only独立証明DAGと照合できる根はK0378の6根のうち3根である。残る2,992根のsolver/cache信頼を除くには、個別または共有DAGでのterminal closureが要る。

作業量の優先順位はdirect solver node数の低・中・高標本からproof captureの実測を行い、次に `nodes=0` のcache-rootから合法手数帯別に小標本を取ること。今回の計算はサイズ測定用の候補選定であり、巨大証明書の生成や未解決探索を開始していない。
