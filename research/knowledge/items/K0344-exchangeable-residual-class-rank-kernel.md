---
id: K0344
title: 交換可能残余classはrank以下へ縮めて通常Grundyとmisère補助mexを保存し、誘導削除上限は全rankで最良
kind: proposition
status: proved
topics:
- residual-games
- grundy
- search-methods
- variants
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 継続ゲームは二点グラフではなく全包含極小残余辺で表す
- type: depends_on
  target: K0002
  note: 通常プレイのmex。misère補助mexは終端値1で別に定義する
- type: generalizes
  target: K0336
  note: 同一全linkの独立双子は混合深さ1の特殊例
artifacts:
- path: research/experiments/n11-reduction-followup-20261005/reports/exchangeable-kernel.md
  role: proof
  note: 内部容量の商DAG、混合深さ付き偶奇の全称帰納、安価な容量1検出の証明
- path: research/experiments/n11-reduction-followup-20261005/reports/misere-kernel.md
  role: proof
  note: 孤立二点の補助mex周期とmisèreへの全称拡張。成分xorを使わない
- path: research/experiments/n11-reduction-followup-20261005/reports/rank-sharpness.md
  role: proof
  note: 全rank≥2の証人族のGrundy閉再帰と誘導点削除上限の最良性
- path: research/experiments/n11-reduction-followup-20261005/reports/independent-kernel-audit.md
  role: proof
  note: 別担当によるcleanup非依存のcount-subset定式化と通常・misère証明監査
- path: research/experiments/n11-reduction-followup-20261005/scripts/module_core.py
  role: solver
  note: 全置換class検出、容量・深さ偶奇kernel、incidence hashによる安価な部分kernel
- path: research/experiments/n11-reduction-followup-20261005/scripts/verify_modules.py
  role: verifier
  note: 別占有subset mexで全小clutterと全交換不変族を検査し実格子証人を再生成
- path: research/experiments/n11-reduction-followup-20261005/scripts/independent_count_audit.py
  role: verifier
  note: 全残余更新を使わないcount-subsetの独立通常・misère補助mex
- path: research/experiments/n11-reduction-followup-20261005/scripts/verify_sharpness.py
  role: verifier
  note: 閉再帰公式をrank2..64で検算し、小rankでは別全占有subsetとも照合
- path: research/experiments/n11-reduction-followup-20261005/scripts/sample_n11.cpp
  role: solver
  note: 既存共有geometryと既存全R生成器を再利用したbounded greedy sampler
- path: research/experiments/n11-reduction-followup-20261005/output/audit.json
  role: data
  note: 全7020小clutter、全5219交換不変族、727実n11残局の通常・misère検査と測定
- path: research/experiments/n11-reduction-followup-20261005/output/independent-count-audit.json
  role: data
  note: 全5219族と720広rank標本の別count-subset監査
- path: research/experiments/n11-reduction-followup-20261005/output/rank-sharpness-audit.json
  role: data
  note: 全rank証明の有限回帰、rank2..64の公式値、45ケースの別subset照合
- path: research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json
  role: data
  note: seed20261005、n11の200 greedy軌跡から全826 late snapshotsを保存
scope: 任意有限点集合の禁止clutterを避ける一点追加ゲーム。全内部二点交換が全辺族を保存するclassの誘導点削除kernel。通常Grundyと、最後の合法手が負けるmisèreの終端値1の補助mexを各々保存する。rank上限の最良性は外部を保持する通常Grundyの誘導点削除方式に関する。
evidence: 容量の商DAG、混合深さと外部点数の帰納、全rank証人族の閉再帰による全称証明。全小clutter・全交換不変族の別mex、別担当のcount-subset監査、実n11の独立geometry証人。df-pn速度改善の証拠は得ていない。
---

# 交換可能残余classのrank kernel

現在合法なV上の全包含極小残余辺Fで、X内の全二点交換がFの自己同型なら
Xを交換可能classとする。単なる自己同型の一軌道や二点グラフPだけでは足りない。

Xだけの辺の最小サイズがc+1なら、Xをc点へ誘導削除して継続ゲームの商DAGを保存する。
内部辺がない場合はd=max|e∩X|とする。孤立d=0は点数mod2へ減らす。
d≥1では点数がd以上で同じ偶奇ならGrundyが等しく、d/d+1の一方へ減らせる。
削除点を含む辺は丸ごと消し、辺から点だけを除いてはいけない。

全辺サイズが高々Rなら内部容量c≤R−1、内部なしの混合深さd≤R−1なので
各classは高々R点になる。標準共円ゲームの全残余辺ではR≤4であり、
classは高々4点、内部clique classは1点となる。複数classへ順次適用してよい。
これはV全体の点数上限ではない。

通常Grundy保存は容量商DAGと(外部点数,d)の辞書式帰納による全称証明。
孤立二点を加えてもmisère補助mex hは変わらないことを別に証明し、
同じkernelが終端h=1・非終端h=mex(子h)も保存することへ拡張した。
misèreのP/Nは保存するが、hに通常成分xorを適用してはいけない。
偶奇kernelはゲーム木・終局手数・元の全手順を保存する主張ではない。

R点上限は、外部を保持した誘導点削除方式として全R≥2で最良。
XをR点、外部をa,b,cとし、全Xの(R−1)点+b、全Xの(R−2)点+a+c、{b,c}を
禁止する族が証人となる。閉再帰でXを任意のR−1点以下へ減らした通常Grundyは
元と異なることを証明した。R=4では元g=3、X0/1/2/3点の値は0/1/2/2。
別の種類のゲームへの置換や外部点も変更するkernelを否定する下界ではない。

全7020小clutterとX6点/外部2・3点/rank4の全122+5097交換不変clutterで、
原始辺・占有subsetによる別DPと、誘導削除後・各ノードkernelの通常値と
misère補助mexが一致した。別担当のcount-subset mexも全5219族と720広rank族で一致。
これら有限検算が全称証明の代わりにはならない。

n11の200 greedy軌跡から826 late snapshotsを保存し、253で初期kernelが縮む。
188で内部容量classが縮み、深さ2以上の非内部class圧縮は0。最大初期削除7点。
|L|≤14の727 snapshotsでは通常・misère補助mexを独立検査した。
通常memo合計17324→10477、既知の全成分xorも併用して9341だった。
全Rが連結かつ三点辺を持つ独立geometry証人はg=4、memo36→17。

単純Python prototypeはmemoが減っても実時間が増え、安価な全incidence hash版も
今回の測定ではbaseline速度を上回らなかった。全R構築の時間も除外している。
共有df-pnへの常時導入、空盤・s5の探索速度改善は主張しない。
**11×11空盤勝敗は引き続きUNKNOWN。**
