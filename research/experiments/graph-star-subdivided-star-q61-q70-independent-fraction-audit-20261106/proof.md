# q=61〜70 奇数次数切替の独立有理数監査（2026-11-06）

## 対象と判定

先行記録 `research/experiments/graph-star-subdivided-star-q61-q70-odd-transitions-20261106/proof.md` の20個の境界判定を、先行コードの交差乗算式を使わず、`fractions.Fraction` で元の関数を直接評価した。

`r=q-3`, `a=(r+2)/(r+1)`, `y_*=ka/(k+1)`, `F(y)=r-y-(a-y)y^k` とし、各 q に対して `F_{k_-}(y_*)>0` と `F_{k_+}(y_*)<0` を検査した。前者だけでは根なしを導けないため、別途 `H(y_*)<r-a` も確認する。これが先行証明の非存在側で必要な条件である。

## 再現コード（Python標準ライブラリのみ）

```python
from fractions import Fraction

for q in range(61, 71):
    r = q - 3
    km = 687 + 14 * (q - 61)
    kp = km + 2
    a = Fraction(r + 2, r + 1)
    def terms(k):
        y = Fraction(k, k + 1) * a
        H = (a - y) * y**k
        F = r - y - H
        return y, H, F
    ym, hm, fm = terms(km)
    yp, hp, fp = terms(kp)
    assert 1 < ym < a and 1 < yp < a
    assert hm < r - a  # 全区間の非存在を保証
    assert fm > 0 and fp < 0  # 存在側の中間値判定
    print(q, km, kp, 'PASS')
```

実行結果：q=61,62,63,64,65,66,67,68,69,70 の全10行が PASS。

## 証明の論理境界

- `H(y)=(a-y)y^k` の区間 `(1,a)` における最大点は `ka/(k+1)`。この微分事実と `H(y_*)<r-a` により、根なし側は全区間に及ぶ。
- `F(1)>0`, `F(a)>0`, `F(y_*)<0` から2つの相異なる根があり、デカルトの符号法則で重複度込み2個以下となる。
- `k\mapsto F_k(y)` は固定 `1<y<a` で狭義減少。根なし側は `H_k(y)\le H_{k_-}(y)` によって小さい奇数次数へ延長できる。
- この監査は境界算術の別実装照合であり、独立した形式証明器による全証明検査ではない。一般の q に対する接触二重根の不存在は依然未解決。

## 注意

非存在側で `F_{k_-}(y_*)>0` **だけ**を調べても全区間での正値性は従わない。必ず `H(y_*)<r-a` を使う必要がある。今回の監査では両者を区別して検査した。
