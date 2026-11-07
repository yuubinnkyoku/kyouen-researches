# 共通合法点への一手で通常値が非有界に増える整数盤

既知のコグラフH_kのNode Kayles値2^kを、純三点残余族の共通合法点cへの一手後に実現する。
一手前は常にg=1。自由点一個を加えれば一手前g=0、一手後2^k+1。
根のg≤3というK0692の制約は、子の値を一様には制限しない。

```sh
uv run --locked python research/experiments/common-pivot-unbounded-one-move-jump-20261108/verify.py --with-free-geometry
```

[証明と既知構成への帰属](proof.md)を参照。
対象は指定安全占有を持つ有限整数点盤。全正方形格子盤の非有界性は未解決。
