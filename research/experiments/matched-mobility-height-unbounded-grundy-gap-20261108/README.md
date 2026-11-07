# 同一盤・同じ基本計数でもGrundy差は非有界

同じ有限整数点盤の二安全局面で、占有石数・合法点数・最大追加手数を全て揃え、
通常Grundyを2^kと0にできる。
さらに終局長の可能集合全体まで揃え、値を2^(k+1)と1にする変形もある。
証明は[proof.md](proof.md)。既知のコグラフ構成への帰属を明記して使う。

```sh
uv run --locked python research/experiments/matched-mobility-height-unbounded-grundy-gap-20261108/verify.py --matched-terminal-support
```

基本対の初回監査は`output/audit.json`、強化対を含む追加監査は`output/audit_terminal_support.json`。
具体的な10点整数盤を保存する。全正方形格子盤の無界性は主張しない。
