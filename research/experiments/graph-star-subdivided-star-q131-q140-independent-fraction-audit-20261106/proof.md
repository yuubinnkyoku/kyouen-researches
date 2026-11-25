# q=131〜140 奇数次数切替の独立有理数監査（2026-11-06）

## 対象と証拠水準

先行記録 `research/experiments/graph-star-subdivided-star-q131-q140-odd-transitions-20261106/proof.md` の10組・20境界を、先行記録の整数不等式を再利用せず `fractions.Fraction` で直接検査した。**境界の算術的な独立検証**であり、解析的な全称部分（単調性・デカルトの符号法則）の独立形式化ではない。

奇数 `k`、`r=q-3`、`a=(r+2)/(r+1)` とし、
`F_k(y)=r-y-(a-y)y**k`、`y*=k*a/(k+1)` とする。

- 非存在境界 `k_-=k_+-2`: `(a-y*)*y* ** k_- < r-a` を検査する。これにより `1<y<a` の全域で `F_k(y)>0`。
- 存在境界 `k_+`: `F_k(y*)<0` を検査する。さらに `1<y*<a` を明示的に検査する。

以下は標準ライブラリのみで再現可能。大きな整数の有理数演算なので丸めはない。

```python
from fractions import Fraction

bounds = [
    (131, 1721), (132, 1737), (133, 1753), (134, 1769),
    (135, 1783), (136, 1799), (137, 1815), (138, 1831),
    (139, 1847), (140, 1861),
]
for q, k_plus in bounds:
    r = q - 3
    a = Fraction(r + 2, r + 1)
    for k, existence in ((k_plus - 2, False), (k_plus, True)):
        y = Fraction(k, k + 1) * a
        assert 1 < y < a
        H = (a - y) * y**k
        F = Fraction(r) - y - H
        if existence:
            assert F < 0, (q, k)
        else:
            assert H < r - a, (q, k)
    print(q, "pass")
```

## 実行結果

`131 pass` から `140 pass` まで全10行を確認。20境界すべて成立、反例なし。先行証明における `k` 単調性を用いると、各 `q` の全奇数 `k≥3` について切替が従う。

## 限界・次の課題

この監査は先行記録の解析的議論と独立ではない。特に一般の `q` における接触二重根の不存在は未解決。knowledge 項目の更新および全体回帰はこの記録では実施していない。
