---
id: K0437
title: 残余禁止辺h本の一点追加ゲームはGrundy値が最大2^h−1（h≥1）
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
  target: K0002
  note: 通常プレイのmexと独立成分のxor
- type: depends_on
  target: K0108
  note: 極小残余禁止辺による継続ゲームの表現
artifacts:
- path: research/experiments/sparse-hyperedge-nimber-20261019/reports/sparse-hyperedge-nimber.md
  role: proof
  note: 署名類・mexによる全称証明と2辺での鋭い整数格子例
- path: research/experiments/sparse-hyperedge-nimber-20261019/scripts/verify_sparse_hyperedge.py
  role: verifier
  note: 2種類の独立再帰と小超グラフの有限全数監査
- path: research/experiments/sparse-hyperedge-nimber-20261019/scripts/verify_two_circle.cpp
  role: verifier
  note: 独立C++行列式・部分集合Grundy検証
- path: research/experiments/sparse-hyperedge-nimber-20261019/output/verification.json
  role: data
  note: 7点整数座標例と6頂点全2辺監査の再現結果
- path: research/experiments/knowledge-audit-20261021/README.md
  role: log
  note: 証明の論理監査・再実行範囲・判定
scope: 任意有限禁止集合超グラフの一点追加通常プレイ。現在の安全局面の極小残余禁止辺数h。h=0ではg≤1、h≥1ではg≤2^h−1。misèreや他人の専有石を含む多人数ゲームには直接適用しない。
evidence: '2026-10-21監査。署名交換による子局面同型、空署名のxor分離、上界2^h−1のxor閉性を確認。Python全1180二辺型とC++113安全局面を再検査。 監査記録: research/experiments/knowledge-audit-20261021/README.md。'
---


# 少数残余禁止辺からGrundy値を一様に抑える

任意の有限点集合・任意の禁止点数について、現在の残余禁止辺がh本なら、h≥1で `g≤2^h−1`、h=0で `g≤1`。残余辺に対する所属署名が等しい合法手は同型の子を生む。空署名点は独立した自由手なのでxorで分離でき、残りの署名種類数からmex上界を得る。

特に残余辺2本以下なら `g≤3` で、この上界は鋭い。整数格子7点 `[(3,4),(-5,0),(-4,-3),(-4,3),(1,0),(2,-3),(6,-5)]` は共円・共線4点組が `{0,1,2,3}` と `{0,4,5,6}` のみ。安全局面 `{1,4,5}` で `g=3`。35組の整数行列式検査、113安全局面の完全再帰、独立C++検査、6頂点の2辺超グラフ1180種類の監査で再確認した。

全称上界の証明、整数格子達成例の有限完全検査、補助的な標本監査を区別する。11×11の根の勝敗・計算時間改善は主張しない。


## 4本以下・辺サイズ4以下の鋭い改善（2026-10-27）

**計算機援用の全称定理：** 現在の安全局面で、包含極小残余禁止辺が高々4本、各辺のサイズが高々4なら、全合法継続のGrundy値は **g≤5**。一般の h=4 上界15を5へ改善する。抽象禁止集合ゲームでの上界5は鋭く、9点・四辺の明示証人を持つ。

証明は四辺の各頂点を15通りの所属署名に分け、辺サイズ2..4かつ相互非包含の全37,592ラベル付き署名型へ**全称的に有限帰着**したうえで、Pythonの署名残数mexと独立C++の個別頂点占有ビットmexを全件照合するもの。Grundy値の分布は g=0,1,2,3,4,5 の順に 13,508・13,427・5,111・5,270・240・36。辺サイズ上限2なら最大3（70型）、上限3なら自由点を除く核で最大4（2,760型）。核の外の自由点はxor 1の偶奇成分であり、四辺未満も独立2点辺を追加して上界5へ帰着できる。

**証拠の区別：** 無限の盤への適用は署名による数学的な有限帰着、具体的な上界5は二方式の有限完全列挙による計算機援用証明。抽象9点証人は標準整数格子の幾何的実現を示さず、11×11の勝敗・探索時間短縮も主張しない。

[全称帰着・完全列挙・9点証人](../../experiments/game-structure/four-edge-rank4-20261027/README.md)／[署名別再帰](../../experiments/game-structure/four-edge-rank4-20261027/verify_venn.py)／[独立部分集合再帰](../../experiments/game-structure/four-edge-rank4-20261027/verify_subset.cpp)。


## 二点残余辺9本以下の鋭い上界（2026-10-27）

**計算機援用の全称定理：** 極小残余禁止辺がすべて2点集合で、その本数を h（1≤h≤9）とする。孤立した自由点を任意個許すとき、通常Grundy値の鋭い上界は h=1,...,9 の順に

\[
\boxed{1,\ 3,\ 3,\ 3,\ 3,\ 3,\ 5,\ 5,\ 7}
\]

である。特に二点残余辺が6本以下なら g≤3、8本以下なら g≤5、9本以下なら g≤7。g=6 または g=7 の実現に必要な二点残余辺の最小本数は **9**。

証明は、孤立点のない h 辺単純グラフを辺追加の三操作で全生成する数学的帰着と、h≤9 の全非同型グラフのGrundy値の有限完全列挙による。h=9 の核は1,476種類、g=0,...,6 の度数は (366,405,309,309,56,28,3)。自由点はxor 1として作用する。C++の残存頂点再帰とPythonの占有独立集合再帰が全度数表で一致した。

9辺・10点でg=6となる明示グラフに孤立点を1点追加するとg=7となり、上界は鋭い。これは**抽象的な二点禁止集合ゲーム**の定理であり、標準整数格子での実現や11×11の勝敗を示すものではない。三点以上の極小残余辺が存在する場合にも適用できない。

[全称帰着・全度数表・証人](../../experiments/game-structure/rank2-nine-edge-sharp-20261027/README.md)／[独立C++検証器](../../experiments/game-structure/rank2-nine-edge-sharp-20261027/verify_graph_cpp.cpp)／[独立Python検証器](../../experiments/game-structure/rank2-nine-edge-sharp-20261027/verify_graph_python.py)。


## 二点残余辺11本以下への拡張（2026-10-27）

**計算機援用の全称定理：** 二点集合のみからなる包含極小残余禁止辺が高々11本なら、任意個の自由点を許しても **g≤7**。10辺の孤立点なし核4,613種類の最大値は7（達成3種類）、11辺の核15,216種類でも最大7（達成35種類）。自由点なしでg=7を実現するための最小辺数は**10**。

辺追加三操作による全称的有限帰着と完全同型判定に基づく。C++の残存集合mexと占有集合mexが11辺まで全件一致し、Pythonによる独立生成・占有集合mexは10辺まで一致した。**11辺の同型類生成自体は独立実装で未照合**。整数格子での実現や11×11の探索速度改善は未確認。

[全度数表・証人・証明](../../experiments/game-structure/rank2-eleven-edge-sharp-20261027/README.md)／[残存集合検証器](../../experiments/game-structure/rank2-eleven-edge-sharp-20261027/verify_graph_cpp.cpp)／[占有集合検証器](../../experiments/game-structure/rank2-eleven-edge-sharp-20261027/verify_occupied_cpp.cpp)／[Python独立検証器](../../experiments/game-structure/rank2-eleven-edge-sharp-20261027/verify_graph_python.py)。


## 森をなす二点残余辺12本以下（2026-10-27）

**計算機援用の全称定理：** 極小残余禁止辺がすべて二点集合で、対応する競合グラフが森、辺数が12以下なら、自由点を任意個許しても **g≤7**。12辺・13頂点の非同型木1,301種類のうち9種類で **g=7**。**連結な木でg=7を達成する最小辺数は12**（11辺以下の木では最大6）。12辺の森全体も上界7が鋭い。

任意の木は葉を一つ除去して帰納的に全生成できる。全根付き括弧符号の最小値による完全同型判定、二つの独立なGrundy再帰、さらに別の木生成器による12辺までの全件照合を実施。森の全称帰着は連結木のxor分解による。これは**抽象的な森に限る**計算機援用証明で、閉路を持つ12辺グラフや標準整数格子での実現は未確認。

[証明・度数表・12辺証人](../../experiments/game-structure/rank2-forest-twelve-edge-20261027/README.md)／[標準ライブラリ検証器](../../experiments/game-structure/rank2-forest-twelve-edge-20261027/verify_trees.py)／[別生成器の独立照合](../../experiments/game-structure/rank2-forest-twelve-edge-20261027/verify_networkx.py)。
