# 7立方の全2石軌道と4手終局境界

点番号は `49*x+7*y+z`、各座標は0から6。盤の48等長変換で非順序2石集合を
まとめると1516軌道となる。各2石集合Aと第三手cについて、異なる第四手dにより
全第五手を禁止できるかを調べた。そのようなdがない第三手を未被覆とする。
未被覆の三石集合は、Aの固定部分群だけでなく全48変換で再び軌道化した。

全1516軌道の最少未被覆数は31。未被覆三石軌道数の最小値は5で、その達成組は
`{168,173}` と `{169,173}` の2種類（いずれも未被覆32手）だった。
全第三手を4手終局だけで覆う2石組は存在しない。
これは4手終局応手方式の限界であり、2石P局面の不存在や空盤勝敗を意味しない。

`{169,173}` は座標 `(3,3,1),(3,3,5)`。残る三石軌道の代表は
`{3,169,173}`, `{10,169,173}`, `{17,169,173}`, `{24,169,173}`, `{66,169,173}`。
この5根をNと証明できれば、その他の第三手には終端Pの第四手応手があるため、
当該2石局面をPと証明できる。現時点ではその5根も2石根も未解決である。
従来の角を含む組 `{0,5}` は未被覆35手・19軌道である。

## 二つの正確な計算

`rank_pairs.cpp` は三石の持上げ差ベクトルが張る2次元空間に第四点の差が入るかを
整数の小行列式で調べる。`verify_pairs.cpp` は探索器を呼ばず、独立に48変換を生成し、
独立検査器の5×5 Bareiss行列式を使う。両者の1516行は第三手集合・軌道代表まで一致。
後者は143,767,411行列式を評価した。結果は `pair-ranking-verified.json`。

後者の終端判定は次の線形代数による。点を `(x²+y²+z²,x,y,z,1)` に持ち上げる。
盤上の5点 `0,1,2,7,49` の持上げは行列式2の基底である。4石の行に各基底点を
追加した全5行列式が0なら、行列式の最終行に関する線形性により、任意の第五点でも0。
一つでも非零なら、その基底点自体が合法な第五手で、4石は終端でない。
したがって第五手343点の走査を5基底点で完全に置き換えられる。

4石の持上げ階数が3以下とは、元の4点が共円または共線であることに対応する。
非共線の共平面4点でも共円でなければ持上げ階数4なので、4手終局とはならない。

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-hybrid-20261023/rank_pairs.cpp -o /tmp/rank-pairs
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-hybrid-20261023/verify_pairs.cpp -o /tmp/verify-pairs
/tmp/rank-pairs 7 > research/experiments/cube-q5-seven-hybrid-20261023/pair-ranking.jsonl
/tmp/verify-pairs 7 > research/experiments/cube-q5-seven-hybrid-20261023/pair-ranking-independent.jsonl 2> research/experiments/cube-q5-seven-hybrid-20261023/pair-ranking-independent-counts.json
python research/experiments/cube-q5-seven-hybrid-20261023/audit_pairs.py
```
