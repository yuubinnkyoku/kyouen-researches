---
id: K0543
title: 九段から選ぶ二線五石の全8001型で第三線の安全四石が塞ぐ空点は高々8個
kind: proposition
status: proved
topics: [geometry, variants, maximal-safe, certificates, verification]
aliases: []
relations: []
artifacts:
- path: research/experiments/q6-rational-third-line-blockers-20261024/proof.md
  role: proof
  note: 全実数第三線の三円パラメータへの有限帰着、特異組排除、無理数成分の次数1上界
- path: research/experiments/q6-rational-third-line-blockers-20261024/generate.py
  role: solver
  note: Cramer・判別式・有理根グラフで全8001型の証明書を生成
- path: research/experiments/q6-rational-third-line-blockers-20261024/check.py
  role: verifier
  note: Gaussian消去・根軸で全558238三円組と全11624パラメータの被覆上界を独立確認
- path: research/experiments/q6-rational-third-line-blockers-20261024/certificate.json
  role: certificate
  note: 有限原型の全パラメータと次数和または独立集合による上界
- path: research/experiments/q6-rational-third-line-blockers-20261024/audit.json
  role: data
  note: 全分類と原型欠落・パラメータ欠落・虚偽上界の拒否receipt
scope: 二平行線の各5石の高さB,Cが同じ縦平行移動・等方拡大で{0,...,8}の部分集合となる場合。第三線の位置・線間距離・安全な高々四石の高さは任意の実数。
evidence: 全称有限帰着と8001有理原型の全三円組・全正パラメータの独立厳密認証。有限原型以外のB,Cには拡張しない。
---

# 九段二線五石型の第三線被覆上界8

二線の各5石の高さを{0,...,8}から選び、第三線には任意の実数位置の安全な高々4石Aを置く。
線間距離と第三線の位置も任意とする。このとき6点円の完成で第三線の追加を禁じる未占有点は高々8個。

有理二線型では三円共通点を生じる第三線パラメータを有限有理数集合へ帰着できる。
その集合外では各点が高々2円に属するので四石の被覆は8以下。
集合内では、無理数根は共役相手1点しか塞がないことを利用して有理根グラフだけを検査する。

全8001型・全558238三円組を独立検査し、全11624正パラメータのうち11618個は次数和上界8以下、
残る6個は独立集合の開近傍上界6と確認した。

これは有限個の外線原型について全実数第三線を覆う命題である。
任意の実数高さB,Cについての被覆上界8、ゲームの一様候補閾値13や16、上界8の鋭さは主張しない。
