# q=171〜180 奇数次数切替の独立有理数監査（2026-11-07）

対象：`graph-star-subdivided-star-q171-q180-odd-transitions-20261106/proof.md` に記載された10組・20境界。開始時点の main は `4250feae`。

## 方法

先行記録の整数化不等式は使わず、`fractions.Fraction` で極大点 `y*=ka/(k+1)` と `H=(a-y*)y*^k` を直接構成した。ここで `r=q-3`, `a=(r+2)/(r+1)`。非存在側は `H<r-a`、存在側は `H>r-y*` を検査する。全境界で `1<y*<a` も検査した。

```python
from fractions import Fraction

for q in range(171, 181):
    r = q - 3
    a = Fraction(r + 2, r + 1)
    k_plus = 2353 + 16 * (q - 171)
    for k, exists in ((k_plus - 2, False), (k_plus, True)):
        y = Fraction(k, k + 1) * a
        h = (a - y) * y**k
        assert 1 < y < a
        if exists:
            assert h > r - y, (q, k, "existence")
        else:
            assert h < r - a, (q, k, "nonexistence")
    print(q, "PASS")
```

## 実測結果

```text
171 PASS
172 PASS
173 PASS
174 PASS
175 PASS
176 PASS
177 PASS
178 PASS
179 PASS
180 PASS
```

各PASSは二つの境界の双方に対する厳密な有理数比較を意味する。Python標準実装で再実行済み。

## 証明上の位置づけ

これは有限20境界の**独立した算術監査**であって、解析的な単調性・根候補区間への還元・デカルトの符号法則の独立再証明ではない。既存定理と矛盾しないことを確認したが、新しい切替点の発見ではない。一般のqの接触二重根不存在も未解決。knowledgeのstatus変更は行わない。
