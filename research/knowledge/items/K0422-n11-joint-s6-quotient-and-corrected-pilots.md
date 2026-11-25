---
id: K0422
title: 11盤共同S5計画の319万合法辺は156万相異なるS6へ縮約し、訂正済み39パイロットは2269子
kind: computation
status: computed
topics: [search-methods, certificates, verification, square-outcomes, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: 31,546相異なるS5を要求する既存19-root共同計画
- type: depends_on
  target: K0420
  note: 極性訂正済みcheapest10と衝突29件の入力
- type: depends_on
  target: K0421
  note: 親安定化群による軌道数と正準子数の全称的一致
artifacts:
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/census.py
  role: source
  note: 独立整数幾何BoardとBurnsideによる全要求S5の合法S6完全列挙
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/verify.cpp
  role: verifier
  note: 別C++実装・平行移動3x3行列式・直接D4変換による全件独立検算
- path: research/experiments/n11-s5-s6-quotient-20261013/scripts/verify.py
  role: verifier
  note: 入力hash、親全件と集計照合、改変入力拒否
- path: research/experiments/n11-s5-s6-quotient-20261013/output/joint.json.gz
  role: data
  note: 全31,546親の合法数・安定化群・子数・順位と集計
- path: research/experiments/n11-s5-s6-quotient-20261013/output/joint-verification.json
  role: certificate
  note: 全31,546親の独立照合成功receipt、入力・実装SHA256
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json
  role: data
  note: 訂正済み39候補の全正準S6子・着手対応
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilots-verification.json
  role: certificate
  note: 全39親の独立照合成功receipt
scope: K0417の共同要求31,546 S5と、現行pilot-candidatesのcheapest10＋polarity_conflicts29の39 S5。全合法追加の幾何・同値・親間共有のみ。
evidence: 合法辺3,191,228、親内正準子incidence3,169,651、全親和集合1,564,737子。Pythonと独立C++で全親・全集計が一致。入力hashを保存。候補39件は3,273合法辺・2,363親内正準子・2,269和集合。
---

共同計画31,546個のS5について全合法S6を列挙した。合法辺3,191,228、親内対称性縮約後3,169,651 incidence、全親を横断した相異なるS6は1,564,737。
親内削減は21,577（約0.68%）、親間共有による重複incidenceは1,604,914。
S6の親数の完全分布は1親3,778・2親1,536,980・3親4,034・4親19,914・5親31。

親安定化群の位数は1が31,054・2が484・4が8。全親でBurnside軌道数と正準子数が一致し、K0421の一般証明を有限範囲で支持する。
独立C++が各親の安全性・合法数・安定化群位数・Burnside軌道数・正準子数を再計算し、和集合と親数分布も全て一致した。合法数を改変した入力の拒否も検査済み。

現行39パイロットはcheapest10＋極性衝突29件で、旧極性のdual_use16件を使用していない。3,273合法辺、2,363親内正準子、2,269相異なるS6、共有94子（各2親）。
最小義務数は索引558600の17子（68手・位数4）、次は衝突候補209644の20子（80手・位数4）。合法数だけで最少の528497は30子（60手・位数2）。

これは幾何的な子集合の有限完全列挙で、子の勝敗を取得していない。LOSS要求S5を閉じるにはあるS6 LOSSが必要、WIN要求S5には全S6 WINが必要（元先手固定視点）。従って全和集合のS6を必ず解く必要があるとは主張しない。共有は局面同一性であり、逆極性の要求を満たす共有証拠を意味しない。
実探索時間、未知局面の勝敗、11×11空盤勝敗の結論はなく、空盤はUNKNOWNのまま。
