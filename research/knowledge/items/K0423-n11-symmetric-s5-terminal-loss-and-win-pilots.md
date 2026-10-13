---
id: K0423
title: 11盤の対称S5二局面を終局DAGで独立証明し、共同計画の衝突候補209644は先手WIN
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods, provenance]
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 元先手固定のAND/OR極性と終局payoff
- type: depends_on
  target: K0422
  note: 索引558600・209644の現行パイロット選択と完全合法境界
- type: refutes
  target: K0417
  note: 保存された31,546計画をそのまま全要求LOSSで閉じられる仮定を反証。旧cache限定の組合せ計算自体は否定しない。
- type: supports
  target: K0420
  note: 極性衝突29候補の一つ209644についてWIN側要求を実際に証明
artifacts:
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/probe_pilots.py
  role: solver
  note: 二つの幾何監査済み入力の独立cold exact probe・node上限・hash保存
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/convert_probe.py
  role: source
  note: native依存トレースを到達部分へ剪定し共有の独立DAG検査器を適用
- path: research/experiments/n11-s5-s6-quotient-20261013/output/budget10m-manifest.json
  role: manifest
  note: 完了探索node数・元先手極性・solver source/binary/input/outputのhash
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilot-558600-terminal-dag.json.gz
  role: certificate
  note: 270,545節点・426,376辺・終局28,813・trusted葉0のLOSS証明
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilot-209644-terminal-dag.json.gz
  role: certificate
  note: 349,157節点・518,252辺・終局50,131・trusted葉0のWIN証明
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilot-558600-terminal-verification.json
  role: verifier
  note: 全保持節点の幾何・全称境界・存在証人・終局を独立検査したreceipt
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilot-209644-terminal-verification.json
  role: verifier
  note: 同じ検査器によるWIN証明の独立検査receipt
scope: 標準11×11・q=4・通常プレイ。点番号y*11+x、元先手固定視点。安全S5二局面のみ。
evidence: S={40,48,60,72,80}は元先手LOSS、S={49,55,60,65,71}は元先手WIN。両者とも全ての葉が幾何終局のDAGを保存し、solver/cacheを読まない検査器で完全検査。trusted葉0。二局面の分類で空盤勝敗は未確定。
---

索引558600のS={40,48,60,72,80}は元先手LOSS。後手手番の5石局面なので、後手が勝つ応手を持つ。
索引209644のS={49,55,60,65,71}は元先手WIN。後手手番の5石局面で、後手の全応手に対して先手が勝つ。

双方は親安定化群位数4の十字型で、合法手68/80、正準S6子17/20。
count-asc・cold TT・memo=2^20・node上限10Mで探索し、1,269,467/1,684,694 nodeで確定した。
初回の各1M probeはUNKNOWNであり、これを勝敗根拠にはしていない。

native依存トレースから到達部分だけを保持した終局DAGは、LOSS側270,545節点・426,376辺・終局28,813、WIN側349,157節点・518,252辺・終局50,131。
共有の独立検査器は整数幾何・合法追加・D4正準化・石数順位・全称節点の全具体合法手・存在節点の証人・終局payoffを全件再生成し、trusted葉0で通過した。
これはsolver-trustedなrootラベルだけの証拠より強い独立終局証明である。ただしLean内で具体DAGを形式検査したものではない。

209644はK0417の共同要求集合とK0420のWIN証人に共通する極性衝突候補。
WIN証明によりこの局面を要求するS4をLOSS側の選択肢から排除する必要がある。
31,546計画をそのまま全LOSSで閉じる仮定は成立しないが、中央応手そのものや11盤空盤の後手勝ち可能性は否定していない。
現在の計画修復と検証境界は同実験のREADMEとrepaired-joint-plan.jsonを参照。

11×11空盤勝敗、残り37パイロット、他のS5、全S6の求解は未完了。
