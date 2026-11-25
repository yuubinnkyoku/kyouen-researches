---
id: K0589
title: ひまわり型r容量制約の終局長は公差r−1で三制約から任意の欠番が生じ奇数rでは全局面を偶奇で強解決できる
kind: proposition
status: proved
topics: [maximal-safe, maximum-safe, residual-games, strategy-length, grundy, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常Grundy値とmisère補助mexの定義
artifacts:
- path: research/experiments/three-quota-terminal-gaps-20261031/proof.md
  role: proof
  note: 任意r・異容量の全称母関数、奇数rの強解決、11整数点のq=4幾何実現
- path: research/experiments/three-quota-terminal-gaps-20261031/verify.py
  role: verifier
  note: 2016抽象構成と整数平面330四点組・1262安全局面の独立完全検査
scope: r≥2の共通芯Hと互いに素な固有点群P_iによるr容量制約、各固有点群の大きさx_i≥容量p_i≥1。平面実現は明示11整数点・q=4のみ。
evidence: 極大条件の必要十分性と全終局長の偶奇帰納による数学的全称証明。平面例は全330四点組の整数行列式による有限完全列挙。
---

# 三制約から終局長に任意個の欠番が生じる

互いに素なH,P_1,...,P_r,Zについて |H|=c、|P_i|=x_i≥p_i≥1、|Z|=z とし、各 |S∩(H∪P_i)|≤p_i を課す。J=min(c,p_1,...,p_r) とすると、極大配置の母関数は

`Σ_{j=0}^J C(c,j) (∏_i C(x_i,p_i−j)) u^{z+Σp_i−(r−1)j}`。

従って終局長は公差r−1の等差数列、最小極大石数s=z+Σp_i−(r−1)J、最大安全石数K=z+Σp_i、間の欠番数は(r−2)J。特にr=2では連続（K0588と整合）だが、r=3かつc=x_i=p_i=tなら終局長はt,t+2,...,3tとなり、**三制約だけで欠番がt個**（任意のt≥1）。

**奇数rでは全安全局面を強解決**でき、通常Grundy値 `g(S)=(z+Σp_i−|S|) mod 2`、misère補助mex値 `h(S)=1−g(S)`。これは全終局長の偶奇一致とmex帰納法による。

平面の標準q=4ルールについても、11個の明示整数点上で三つの異なる円が共通2点と各固有3点を持ち、他の禁止4点組を持たない構成を得た。その終局長多項式は **`27u^5+54u^7+u^9`** で、6・8石の極大配置は存在しない。空盤は通常g=1、misère補助h=0、全11初手は通常勝ち手。全330四点組の直接整数行列式検査、全1262安全局面の点別mexで確認した。

**限界**：無界のtを持つ三制約構成は抽象容量ゲームの定理であり、無界tの平面三円実現は主張しない。整数平面11点は標準11×11格子盤ではない。11×11残局への適用には残余禁止集合が正確にこの構造であることの別途確認が必要。2016構成の列挙は全称証明の代替ではない。
