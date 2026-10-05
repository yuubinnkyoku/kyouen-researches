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

ここで注意が要る。従来の集計 `2:42021, 3:37562, 4:2344, 6:72` は
**canonical s6への遷移本数**の分布であり、異なる親s5数ではなかった。
対称なs5では別の合法手が同じcanonical s6へ落ちることがある。

異なる親s5で数え直すと:

```
2 distinct parents: 42,021
3 distinct parents: 39,891
4 distinct parents:     15
5 distinct parents:     72
```

親1個だけのs6は0件、最大は5親である。したがって「全s6が複数s5から共有される」
という結論は維持されるが、最大親数6という旧表現は訂正する。

## 意味

これは「s6を81,999件解けばs5が全部ただちに判定できる」という主張ではない。
5石局面はAND側なので、各s5の判定にはその子のWIN/LOSS配置が関係し、
s6自体を解く費用も一様ではない。

それでも、2,262個のs5を完全に独立な問題として扱うと、
直下だけで206,536回現れるs6を81,999種類へ正規化できる。
**最初の1層だけで60%超の重複**がある。

ただし81,999個を全部解く必要もない。5石局面は後手番なので、first-player LOSSの
s5を示すにはLOSSなs6 childを1本見つければよい。そこで勝敗を無視した親子構造だけに
set coverをかけると、2,262個のs5全てへ少なくとも1本のs6 childを割り当てる
**847個のcanonical s6からなる明示的な構造被覆**が得られた。

この847件がLOSSだという主張ではない。実際の証明ではWINなs6候補を捨てて別候補を
試す必要がある。しかし「81,999件の終盤表を先に全埋めする」より、
**s5を覆うLOSS s6 witnessだけを選択的に探す**方が自然である。
1つのs6が覆える異なるs5は最大5なので、この一層witness方式だけなら
容量下界は `ceil(2262/5)=453` 件。847は大域最適値ではなく構成上界である。

この形はCheckers/Pentagoの終盤表、Othelloのboundary solving、Sproutsの小部分ゲーム共有の
中間にある。frontier全体を一括して見るが、全境界を埋めず、上位証明に必要なLOSS witnessだけを拾う。

したがって次の本命実装は、

1. s5 rootを1件ずつcold solveするのではなく、
2. 高共有s6候補をまとめてexact判定し、
3. LOSSになったs6だけをwitnessとして複数s5へ同時に返し、
4. 未被覆s5に対して次の候補を選ぶ

という**witness-oriented frontier batch solving**である。

Sprouts型のsmall-component Grundy共有はこのさらに深い層の共有を担当でき、
両者は競合せず組み合わせられる。

## 再現

`research/experiments/n11-frontier-selection-20261005/scripts/reply27_s6_overlap.py`

は31-class witnessからs5集合を再生成し、各s5の盤面合法手を整数行列式で再計算して
s6をD4正規化する。保存済みs6一覧を信用しない。

`research/experiments/n11-frontier-selection-20261005/scripts/reply27_s6_structural_cover.py`

は異なる親s5集合を再構成し、固定seedのgreedy coverで847件の構造被覆を再現して、
2,262/2,262 s5が覆われることを検査する。

**勝敗は未確定であり、この重複率や847件の構造被覆からLOSS/WINは導かない。**
