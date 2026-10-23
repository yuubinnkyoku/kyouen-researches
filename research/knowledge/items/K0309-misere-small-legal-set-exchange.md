---
id: K0309
title: 合法点5個以下では通常値とmisère補助値は0と1だけ交換される
kind: proposition
status: proved
topics: [variants, grundy]
aliases: []
relations: []
artifacts:
- path: research/experiments/game-structure/reports/game-structure-20261003.md
  role: proof
  note: 5合法点交換則の一般証明
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/reports/game-structure-20261003-extra.md
  role: source
  note: 6合法点での最初の例外分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/experiments/game-structure/output/game_structure_20261003_complexes.json
  role: data
  note: 6頂点全族の完全分類
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 合法点5個以下では通常値とmisère補助値は0と1だけ交換される

任意の遺伝的配置ゲームで、現在の合法点が5個以下なら、通常Grundy値gと終端を1にしたmisère補助mex値hは0↔1を交換し、2以上は不変である。列挙に依存しない構造証明がある。

境界は鋭く、合法点6個で初めて例外が現れる。6頂点の7,785,062族を完全分類すると例外69,940個、同型169種で、全て両ルールで負ける局面である。


## 2026-10-24：長い固定幅盤では全安全局面で交換則

上の「現在の合法点5個以下」という一般定理とは別に、**合法点数が大きい局面も含む特別な無限盤族**で交換則が成立する。

`τ(0)=1,τ(1)=0,τ(k)=k (k≥2)` とする。通常Grundy値 `g`（終局0）と、最後の合法手を打つ側が負けるmisère補助mex `h`（終局1）について：

- 標準q点共線・共円禁止版：任意の `q≥4,w≥1,m≥T_{w,q}`（K0024の十分長さ）、**全安全局面**で `h(S)=τ(g(S))`。misère空盤は `(q−1)w` 偶数なら先手勝ち、奇数なら後手勝ち。
- 二次形式四点禁止版 `det[x²+λy²,x,y,1]=0`（退化も禁止）：任意の実数λ、`w≥1,m≥T_w=3+2[C(3w−2,3)−(w−1)]`、**全安全局面**で同じ交換則。misère空盤は偶数幅なら先手勝ち、奇数幅なら後手勝ち。偶数幅のGrundy値2の二石局面だけは通常・misèreとも手番側勝ち、それ以外は勝敗反転する。

**数学的証明**：標準q点版はK0024により全終局の石数が一定なので、終局までの手数の偶奇で両mexが定まる。二次形式版はK0518の全幅長盤定理により終局が三石（等方直線）または3w石に限られ、四石以上は満容量へ延長される。三石から降順にmex帰納すると、奇数幅では全三石の `(g,h)=(0,1)`、偶数幅では階数3の三石が `(1,0)`、階数2が `(0,1)`。偶数幅の二石は階数3の三石へ必ず延長でき、等方三石への延長の有無に応じ `(2,2)` または `(0,1)`。一石・空盤も交換則を満たす。例外局面数はK0518の二石nimber2閉公式に等しい。

[詳細な全称証明・独立完全列挙・再現手順](../../experiments/quadratic-pencil-misere-phase-20261024/README.md)。有限検算は閾値内の54,088安全局面で不一致0、閾値未満の3盤で反例を確認した。これは短盤への無条件の拡張を意味しない。
