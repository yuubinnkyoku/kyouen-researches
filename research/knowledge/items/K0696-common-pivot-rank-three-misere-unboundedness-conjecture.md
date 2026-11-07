---
id: K0696
title: 二点辺一本のrank三共通pivot族で通常値0に固定して全misère補助値3以上を実現でき、補助値は無界
kind: proposition
status: proved
topics:
- grundy
- residual-games
- variants
- geometry
aliases: []
relations:
- type: depends_on
  target: K0694
  note: 二点辺付きpivot変換と自由二点の補助値周期2
- type: depends_on
  target: K0692
  note: 同じ対象の通常Grundyは全点数・全辺数で3以下
- type: depends_on
  target: K0683
  note: 各有限rank三族の指定有限整数点盤での実現
artifacts:
- path: research/experiments/common-pivot-misere-larger-values-20261108/proof.md
  role: proof
  note: 無界性をグラフh0/1制限ゲームへ帰着する証明と、有限Tなら上界T+4の条件付き証明
- path: research/experiments/common-pivot-misere-larger-values-20261108/verify.py
  role: verifier
  note: リンク値t6/7の再計算とh8/9の別C++全占有subset照合
- path: research/experiments/common-pivot-misere-larger-values-20261108/output/audit.json
  role: certificate
  note: 十九点h8・二十点h9の二根と790944安全状態の一致
- path: research/log/2026-11-08-misere-mobility-gap-and-larger-pivot-values.md
  role: log
  note: 値9までの有限証拠と無界性予想・同値帰着を分けた記録
- path: research/experiments/common-pivot-misere-all-values-20261108/proof.md
  role: proof
  note: 性質Rと二側相互帰納で全t=mを実現し、paired/pureの無界性を証明
- path: research/experiments/common-pivot-misere-all-values-20261108/verify.py
  role: verifier
  note: m0..6両側の原始g/h/tと全残余R、別subset18根を比較
- path: research/experiments/common-pivot-misere-all-values-20261108/output/audit.json
  role: certificate
  note: 全14グラフと18根4396安全状態の一致
- path: research/experiments/common-pivot-misere-all-values-20261108/dag_audit.py
  role: verifier
  note: グラフやcellを使わず文字通りの子ゲーム集合と直和で再計算
- path: research/experiments/common-pivot-misere-all-values-20261108/output/dag_audit.json
  role: certificate
  note: m0..64両側130根と4363ゲームDAG局面の独立一致
- path: research/experiments/common-pivot-misere-all-values-20261108/verify_geometry.py
  role: verifier
  note: 小型paired/pure族を別残余縮約・subset・整数盤で検査
- path: research/experiments/common-pivot-misere-all-values-20261108/output/geometry.json
  role: certificate
  note: 15/31/22/23点の四整数盤、49000四点組と3222安全状態
- path: research/experiments/common-pivot-misere-all-values-20261108/output/failed_ternary_doubling.json
  role: log
  note: 最初の三コピーdoublingではhが6へ出て失敗した記録
- path: research/log/2026-11-08-misere-unboundedness-mutual-recursion.md
  role: log
  note: 有限証拠による予想から二側相互帰納の全称証明へ進めた経緯
scope: サイズ二/三の全極小残余辺が一点cを共有し、二点辺が少なくとも一本ある有限一点追加ゲーム。点数・辺数は無制限。hは終局1のmisère補助mex。指定有限整数点盤に実現できるが、標準全正方形盤は対象外。
evidence: 二側コグラフ相互再帰で全m>=0・a=0/1にh=a,t=mを構成し、自由点での低h所属保存を含めて全称帰納。K0694で全非負hへ移す。グラフ原始再帰14根・別subset18根4396安全状態、独立DAG130根、具体的四整数盤の49000四点組も一致。
---

## 全非負補助値の達成

全残余辺が一点cを共有するサイズ二/三の有限族で、二点辺があるものの
misère補助値hのスペクトルは **全非負整数**。従って非有界である。
さらに全q≥3は、二点辺を **一本** にし、通常Grundyを **0** に固定してh=qを実現できる。
同じ対象の通常値はK0692により常に3以下。
hは直和のSprague–Grundy値ではなく、終局1の補助mexである。

## 予想を解く二側相互再帰

グラフHのNode Kaylesからh=0/1の局面だけを残した通常ゲームのSGをt(H)とする。
全グラフでのtの上限Tは、以前にhの非有界性と同値と証明していた。
新たに任意m≥0、a∈{0,1}で **h(G_m^a)=a,t(G_m^a)=m** となるコグラフを構成した。

G_0^1は空グラフ、G_0^0は三頂点道二つの非交和。
m≥1ではG_m^aを、全j<mの(G_j^(1−a)⊔一自由点)をjoinしたグラフとする。
全後続で自由点追加が低h所属を保存する性質Rを同時に帰納することで、
制限通常ゲームの自由点xorだけを正当に使用できる。
制限子値集合は正確に0..m−1となり、相互帰納が閉じる。

a=1,m≥1のリンクに一poison点zを加え、二点辺{c,z}と三点辺{c,u,v}を作る。
外側点数が偶数なのでK0694の式によりh=m+2、通常値は0。
q≥4での合法点数は5·2^(q−3)+1、q=3では九点の構成を得る。
最小性は主張しない。h=0,1,2は小型の二点辺族で達成する。
[全称帰納・閉形式・全値達成の証明](../../experiments/common-pivot-misere-all-values-20261108/proof.md)を参照。
純三点辺だけへの強化はK0703に分けて記録する。

## 以前の有限証拠と新しい監査

十九合法点の(g,h)=(0,8)、自由点付き二十合法点の(1,9)と、
リンクt6/7の監査は以前の有限証拠として保持する。
それ自体は非有界性の証明ではなく、新しい相互帰納が全称量化を解決した。

新構成を、ラベル付き閉近傍削除と自由点0/1/2の原始再帰でm=0..6の両側14根を検査し、
全到達残余の性質Rも確認した。小型18根は別C++生subsetの4,396安全状態で一致。
さらに独立なoption-DAGと直和再帰はm=0..64の両側130根、4,363ゲーム局面で一致した。
指数サイズのグラフの全subsetを展開したという主張ではない。
15/31/22/23点の四整数座標盤でも全49,000四点組と両値を確認した。

K0683により各有限構成を指定有限整数点盤へ実現できる。
標準全正方形格子盤、misère直和の完全分類、達成例の最小点数、世界初性は未主張。
