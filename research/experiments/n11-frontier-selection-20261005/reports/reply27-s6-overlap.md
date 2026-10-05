# reply 27 frontierの直下s6は60%重複する

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

`reply27-frontier.md` の31-class witnessは、2,262個の異なるcanonical s5 rootを要求する。
これらを1本ずつ独立exact solveするのが本当に自然かを調べるため、全合法s6 childを厳密列挙した。

## 結果

| 指標 | 値 |
|---|---:|
| 対象canonical s5 | 2,262 |
| s5→s6合法遷移 | 206,536 |
| 異なるcanonical s6 | **81,999** |
| 重複遷移 | **124,537** |
| unique率 | **39.70%** |
| 重複率 | **60.30%** |
| s5ごとの合法手 | 70〜105、平均91.31 |

さらに81,999個のs6は**全て複数の対象s5から到達**する。

親s5の個数分布:

```
2 parents: 42,021
3 parents: 37,562
4 parents:  2,344
6 parents:     72
```

親1個だけのs6は0件。

## 意味

これは「s6を81,999件解けばs5が全部ただちに判定できる」という主張ではない。
5石局面はAND側なので、各s5の判定にはその子のWIN/LOSS配置が関係し、
s6自体を解く費用も一様ではない。

それでも、2,262個のs5を完全に独立な問題として扱うと、
直下だけで206,536回現れるs6を81,999種類へ正規化できる。
**最初の1層だけで60%超の重複**がある。

この形はCheckers/Pentagoの終盤表やOthelloのboundary solvingに近い。
また過去の量化探索では、別s5 queryがmain TT内部の既解局面を再利用し、
後続queryが1 nodeで閉じた実測がある。今回の有限列挙はその深い再利用が
偶然ではなく、選択frontier自体に大量の共有子があることを示す。

したがって次の本命実装は、

1. s5 rootを1件ずつcold solveするだけでなく、
2. 選択frontier全体のunique s6（さらに可能ならs7/s8）をまとめ、
3. exact verdict/nimberを共有して上へ戻す

という**frontier batch solving**である。

Sprouts型のsmall-component Grundy共有はこのさらに深い層の共有を担当でき、
両者は競合せず組み合わせられる。

## 再現

`research/experiments/n11-frontier-selection-20261005/scripts/reply27_s6_overlap.py`

は31-class witnessからs5集合を再生成し、各s5の盤面合法手を整数行列式で再計算して
s6をD4正規化する。保存済みs6一覧を信用しない。

**勝敗は未確定であり、この重複率からLOSS/WINは導かない。**
