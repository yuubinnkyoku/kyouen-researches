# 一自由点の補助値xor1則と既存記述の訂正

任意有限不偏ゲームでh(G+一自由点)=h(G) xor1。
低h制限ゲームも一自由点の直和と可換で、tについてもxor1となる。
以前のproof資料の「xor1とは限らない」は誤りで、訂正を[proof.md](proof.md)に記録した。
任意直和でのh同士のxor加法性は成立しない。

```sh
uv run --locked python research/experiments/misere-one-free-point-xor-20261108/verify.py
```

全birthday≤4の65,536ゲーム形式と、既存純三点58,146核の自由点対を独立照合する。
