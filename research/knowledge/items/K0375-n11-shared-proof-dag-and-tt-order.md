---
id: K0375
title: 11×11の既知S5六局面で共有TTと終局閉包証明DAGを実測
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の交互AND/OR規則
- type: depends_on
  target: K0355
  note: 対象S4に属する三つの既知S5 direct LOSS局面
- type: depends_on
  target: K0372
  note: exact solver値、信頼葉、独立終局閉包を区別する証拠規約
- type: depends_on
  target: K0374
  note: 最新候補S4とその既知LOSS S5子
artifacts:
- path: research/experiments/n11-proof-dag-engine-followup-20261011/README.md
  role: source
  note: 実装、比較、性能・容量、限界、再現手順
- path: research/experiments/n11-proof-dag-engine-followup-20261011/scripts/verify_shared_bundle.py
  role: verifier
  note: solverやTTを読まず共有証明DAGの幾何・遷移・AND/OR・閉包を検査
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/shared-s5-proof-bundle-reverse-v1/proof-dag-bundle.json.gz
  role: certificate
  note: 三つのS5 LOSSを終局まで閉じた共有証明DAG、trusted leaf 0
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/shared-s5-proof-bundle-reverse-v1/verification.json
  role: manifest
  note: 3 root LOSS、1,002,511 node、1,517,437 edge、128,528 terminal、trusted 0の検査receipt
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/shared-tt-benchmark-v1/summary.json
  role: data
  note: 旧候補S4の三既知S5におけるfresh/shared TT順序比較
- path: research/experiments/n11-proof-dag-engine-followup-20261011/input/current-s4-resolved-s5-positions.json
  role: data
  note: 最新mainに追加されたdirect LOSS三S5のrootとraw source provenance
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/shared-tt-current-s4-v1/summary.json
  role: data
  note: 最新候補S4の三既知S5で行った共有TT・順序比較。改善は観測されない
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz
  role: certificate
  note: 最新候補S4配下にある既知LOSS三S5を終局まで閉じた共有DAG
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/current-s4-proof-bundle-reverse-v1/verification.json
  role: manifest
  note: 最新候補S4の三S5 LOSS共有DAGの独立検査receipt
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/current-s4-proof-bundle-reverse-v1/summary.json
  role: data
  note: 最新候補S4のDAG生成・独立検査・容量・時間・RSS測定
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/capture-cost-same-binary-v1/summary.json
  role: data
  note: 同一binary/局面/計算環境での証明capture有無、trace hash一致、時間と最大RSS
- path: research/experiments/n11-proof-dag-engine-followup-20261011/output/final-sha256.json
  role: manifest
  note: experiment内の全保存成果物SHA-256目録（目録自身とPython cacheを除く）
scope: 11×11標準通常版の、異なる二つのS4配下から選んだ既にdirect LOSSと判定されていたS5六局面、およびexact TT共有・証明captureの測定。局面{60,27}のLOSS証明、S4全子の解決、未解決S5の探索を含まない。
evidence: 二組の各三S5根は終局のみを葉とする共有証明DAGを生成し整数幾何で独立検査した。六根全てLOSS、trusted leafなし。旧候補S4の三根では独立TT8,774,720 nodeに対してshared reverse4,807,724 node。最新候補S4の三根では独立TT13,897,366 node、shared forward13,958,217 node、shared reverse13,837,831 nodeで、共有の高速化は観測されない。root順序の効果はこの二組・一環境の有限計算結果に限る。
---

# 共有探索・証明DAGの有限結果

旧S4の三つの既知S5根では、solverのexact transposition tableを共有するとcold root別実行の8,774,720節点に対し、入力順forwardでは6,304,672節点、reverseでは4,807,724節点だった。reverseはこのroot集合で45.2%の節点削減となり、最後の根はTTから1節点で返った。最新候補S4配下の別の三既知LOSS根では、cold 13,897,366、shared forward 13,958,217、shared reverse 13,837,831節点で、同じ効果を再現できなかった。

各三根組のLOSSから証明DAGを生成した。solver/cacheを参照しない検査器が六根全てLOSSを確認し、trusted leafは0だった。証明には各局面の合法手数、合法な具体着手、canonical child、固定先手視点で全子を要する節点の全合法子、存在証人節点の勝ち筋、終局判定を含む。偶数S6 LOSSは元先手のOR層であり、全合法S7子LOSSを含む。

証明captureは旧S4配下の三根で同一binaryのcapture-offより一標本で15.75秒（73.6%）長く、最大RSSは849,612,800 byte増えた。最新候補S4配下では54.218秒（86.9%）長く、最大RSSは2,386,620,416 byte増え、証明書は72,771,052 byteだった。DAG記録を全探索へ既定有効化する根拠にはならない。root群の共有TT・順序効果も二組各三根に限られ、未解決S5やS4全体への一般化はしていない。
