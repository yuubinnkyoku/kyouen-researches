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


## cold exact sample による後続A/B

その後、保存したfrontierから決定的に先頭・中央・末尾の3件ずつを取り、
同じGitHub Actions runner上でfresh exact replayした。各rootは別solverで、
main TTのroot間共有は無い。

| reply | sample exact nodes | process wall |
|---|---:|---:|
| r2=0 | 3,331,065 + 3,995,891 + 3,286,176 = **10,613,132** | **25.80 s** |
| r2=27 | 4,956,038 + 6,553,161 + 8,992,350 = **20,501,549** | **51.14 s** |

3点だけの決定的標本なので全2,319/2,262件への外挿値を証明扱いしてはいけない。
ただし1件あたりのnode costはこの標本でr27が約1.93倍であり、target数の
2.46%減を大きく上回る。既知cache 209件もr0側にしか無い。

したがって、**「s5 target数が少ないためr27をr0より優先する」という判断は撤回する。**
現時点ではr0を主レーンに保ち、r27は比較用holdout/副レーンとする方が妥当。
reply選択の目的関数はtarget数ではなく、cold replayから推定した
`marginal unique s5 exact node cost` にすべきである。

再現workflow:
`.github/workflows/n11-frontier-bench.yml`

観測run:
`N11 frontier target sample benchmark` run 37253550332
(head `90a14f98143224fe2c945559f15c631f5c7bfc5e`)。


## 2,262-target full replay and selected-frontier closure

The reply=27 lane was subsequently run as a four-shard cold exact replay on the
Xserver worker, with a 15M-node cap per canonical s5 root.  The completed pass
reported:

- rows: **2,262 / 2,262**
- exact WIN: **42**
- exact LOSS: **2,187**
- UNKNOWN at 15M: **33**
- proved-verdict conflicts: **0**

The 31 selected s4 classes then classified as **10 LOSS / 14 WIN / 7 UNKNOWN**.
Only nine distinct hard s5 roots remained inside those seven still-viable
selected classes.

Those nine roots were independently closed by the archived full canonical s6
boundary proof documented in
`reply27-hard9-boundary-closure.md` (Actions run `37269759034`):
**8 LOSS / 1 WIN / 0 UNKNOWN** at s5.

Combining the two stages resolves every one of the originally selected 31
classes:

```
selected s4 frontier: LOSS 16 / WIN 15 / UNKNOWN 0
```

This does **not** prove reply=27 LOSS: the 15 WIN classes cannot be members of a
LOSS certificate and must be replaced.

The compact result-preservation manifest is
`output/reply27-selected31-verdicts.json`.  Its stage-2 hard9 evidence is
archived and independently reproducible.  The stage-1 Xserver shard files had
not yet been archived in-repo when the manifest was written, so that part is
explicitly marked as a computation-result preservation record rather than a
self-contained certificate.

## Repair after the 31-class split

Rebuilding all 3,384 canonical s4 classes from geometry and using the 16 proved
LOSS classes as unconditional certificate material gives:

- secured third-move vertices: **62 / 119**
- still unsecured: **57**
- exact minimum additional class count: **15**

The last number is certified by MILP with zero gap and is also consistent with
the earlier global 31-class lower bound: with 16 LOSS classes already paid for,
fewer than 15 additional classes could not yield a 31-class certificate.

For scheduling, class count alone is not the best objective.  From the selected
LOSS classes one can derive 1,340 exact LOSS s5 child keys; the archived hard9
cache adds one exact WIN key.  On that compact derived cache:

- exact 15-class repair minimizing additive uncached s5 work:
  **1,471 additive / 1,471 unique targets**
- unconstrained additive-work optimum:
  **17 repair classes / 1,393 additive / 1,375 unique targets**

Thus allowing two extra repair classes reduces the immediate unique s5 work by
96 roots in this cache view.

Reproduction:

- script:
  `scripts/reply27_selected31_repair.py`
- workflow:
  `.github/workflows/n11-reply27-selected31-repair.yml`
- successful structural verification run:
  `37275756113`

Observed verifier output:

```
SECURED 62
UNCOVERED 57
MIN_ADDITIONAL 15
ADDITIVE_OPT 17 1393 1375
FIXED15 1471 1471
```

The 17 repair classes remain UNKNOWN and are only a scheduling frontier.
Proving reply=27 LOSS still requires enough of those replacement classes to
become exact LOSS.  **11×11 empty-board outcome remains UNKNOWN.**
