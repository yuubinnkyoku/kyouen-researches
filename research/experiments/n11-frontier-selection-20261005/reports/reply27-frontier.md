# 中央初手の後手返信選択: r2=27 は r2=0 より小さい31-class s5 frontierを持つ

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

## 問い

中心60を初手としたあと、中央初手を反証するには後手の返信20軌道のうち
**1本でも二石rootをLOSSにできればよい**。従来のcertificate研究は隅返信
`r2=0` に集中していたが、これは探索対象として最安とは限らない。

Othelloの弱解決で使われるroot分割・必要frontier選択の考え方にならい、
20返信についてs4 class coverの構造コストを比較した。

## 20返信のclass-cover最小値

中心60のD4代表20返信について、盤面整数幾何から全safe s4 classを再列挙し、
set coverを厳密に解いた。

- 中央から見て反射軸上にある10返信
  `0,5,12,16,24,27,36,38,48,49`: **OPT=31**
- 一般位置の10返信
  `1,2,3,4,13,14,15,25,26,37`: **OPT=56**

一般位置ではclassの最大coverageが4、反射軸上では最大6。
従って中央初手の反証候補はまず10本へ絞れる。

## s5 frontierの比較

31 classを固定し、各class配下のcanonical s5 root集合の和を小さくする。
加法的なchild数最小化の後、実際のset unionを目的に一class交換と二class交換を行った。

代表的な結果:

| reply | 加法的31-class解のunique s5 | union局所交換後 |
|---|---:|---:|
| 0 | 2,879 | 2,715（既知cache固定なし） |
| 16 | 2,689 | 2,288 |
| 27 | 2,671 | **2,262** |
| 36 | 2,718 | 2,473 |

reply 0にはK0329の既知LOSS s5が209件あるため、別途それを強制利用した
`direct-union-cover.md` の実運用frontierは **2,319 unknown s5** まで下がっている。

それでもreply 27は既知cacheとのoverlapが0であるにもかかわらず
**2,262 s5** で31-class coverを構成でき、reply 0の現在の2,319より
**57件少ない**。

unique-s5目的の大域最適性は主張しない。2,262は明示的上界である。

## 31 classの最小性

reply 27については数値MILPだけに依存しない。

62個の第三手頂点に重み1/2を置くと、全3,384 canonical s4 classについて
その重み和は高々1である。したがって任意のcoverは少なくとも31 classを要する。

同時に、保存したwitnessは31 classで119/119第三手を覆う。

よってreply 27について

```
minimum number of structural s4 cover classes = 31.
```

これは厳密である。

有限データ:
- safe s4 edges: 6,871
- canonical s4 classes: 3,384
- dual positive vertices: 62
- dual denominator: 2
- explicit cover: 31 classes
- selected distinct canonical s5 roots: **2,262**

## 弱解決への意味

従来は `r2=0` で319件のs5 verdict cacheと2 LOSS classを持っているため、
そこを伸ばすのが自然だった。しかし「中央初手を反証する」という上位目的では、
**reply自体を選び直す**自由がある。

現時点のs5 root個数だけなら:

```
r2=27: 2262 new targets
r2=0 : 2319 new targets (209 known LOSS s5を利用後)
```

なので、r2=27を独立workerレーンとして開始する価値がある。

ただしwall time比較は未実施。s5ごとのexact costは約10倍以上ばらつくため、
次の比較では単なるtarget数ではなくcold replay node costを使うべきである。

## 検証物

- witness:
  `research/experiments/n11-frontier-selection-20261005/output/reply27-direct-union-cover.json`
- independent verifier:
  `research/experiments/n11-frontier-selection-20261005/scripts/verify_reply27_frontier.py`

検証器は保存済みclass表を信用せず、盤面規則からsafe edge/classを再生成し、
dual制約、31-class coverage、2,262 s5 union、およびr2=0既知209件とのoverlap 0を再計算する。

**この結果だけではreply 27がLOSSとは言えず、11×11空盤はUNKNOWNのまま。**
