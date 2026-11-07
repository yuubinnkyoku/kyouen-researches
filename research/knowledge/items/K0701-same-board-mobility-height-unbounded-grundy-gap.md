---
id: K0701
title: 同一整数盤で石数・合法点数・最大追加手数が同じでもGrundy差は非有界で、終局長可能集合も一致させられる
kind: proposition
status: proved
topics: [grundy, residual-games, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0700
  note: 既知コグラフHkの定義・Grundy・子値集合と出典
- type: depends_on
  target: K0683
  note: 二グラフの非交和を一つの指定有限整数点盤へ実現
- type: depends_on
  target: K0041
  note: 通常Grundyは最大追加手数以下であり、基本対はその両端を達成
- type: depends_on
  target: K0108
  note: 占有・不合法点を除いた残余グラフとのゲーム同型
artifacts:
- path: research/experiments/matched-mobility-height-unbounded-grundy-gap-20261108/proof.md
  role: proof
  note: 基本対・同一盤の同石数埋込み・終局長可能集合まで一致する強化の全称証明
- path: research/experiments/matched-mobility-height-unbounded-grundy-gap-20261108/verify.py
  role: verifier
  note: 別グラフ再帰とsubset、具体的同一盤からの直接合法手再帰で全指標を照合
- path: research/experiments/matched-mobility-height-unbounded-grundy-gap-20261108/output/audit.json
  role: certificate
  note: 基本対k1..3・148安全状態、同一10点整数盤の同石数二局面
- path: research/experiments/matched-mobility-height-unbounded-grundy-gap-20261108/output/audit_terminal_support.json
  role: certificate
  note: 強化対13/37合法点の終局長全可能集合、別subset267安全状態
- path: research/log/2026-11-08-cograph-geometric-unbounded-gaps.md
  role: log
  note: 一手増加の族から同一盤・同指標の非有界差へ進んだ研究記録
scope: q4完全指摘通常プレイ、指定有限整数点盤の二安全局面。各パラメータで同じ盤を共有し石数も一致。μは合法点数、Lは最大合法追加手数。盤と局面はパラメータに依存する。全正方形格子盤・終局長の個数分布一致は含まない。
evidence: 既知Hkと同じ点数・独立数のクリーク非交和を比較し、両側最大独立集合の占有で同一盤の同石数局面へ移す。さらにjoinとtrue-twin拡張で終局長可能集合を揃える全称構成。グラフ・生subset・具体的10点整数盤の独立有限監査が一致。
---

任意k≥1に対し、一つの有限整数点盤の二つの安全局面で、
占有石数・合法点数μ・最大追加手数Lが一致し、

\[
(\mu,L)=(3^k,2^k),\qquad (g_1,g_2)=(2^k,0)
\]

とできる。従って、これらの指標を全て与えてもgの差は一様には抑えられない。
0≤g≤Lの両端を同じ指標で達成する。

基本対はH_kと、3^k点を2^k個の非空クリークに分けた非交和。
両者の独立数は2^kで、後者のgは偶数個の1のxorなので0。
二グラフを非交和して一つの整数盤に入れ、片側の最大独立集合を占有してその側を全て閉塞する。
他側だけが合法ゲームとして残り、両側の最大独立集合は同サイズなので石数も一致する。

さらに終局までの追加手数の可能集合全体も、両局面で正確に1..2^(k+1)へ揃えられる。
この強化ではμ=4·3^k+1、L=2^(k+1)、gは2^(k+1)と1で、差はやはり非有界。
最大長だけでなく最小長と全可能長を知っても、一様なg予測はできない。
各長さの終局数や到達経路数が一致するとは主張しない。

具体的10点整数盤の二局面では、両方とも石数6・合法点数3・最大追加手数2で、gは2と0。
[全称証明・同一盤埋込み・強化対・独立監査](../../experiments/matched-mobility-height-unbounded-grundy-gap-20261108/proof.md)を保存する。
対象は選択された有限整数点盤であり、K0327等の標準全正方形盤の問題を解決しない。
Lはミゼール補助mex hとは別の量である。
