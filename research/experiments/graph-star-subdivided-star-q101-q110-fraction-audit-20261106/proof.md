# q=101〜110 の境界の独立有理数監査（2026-11-06）

対象: `graph-star-subdivided-star-q101-q110-odd-transitions-20261106/proof.md`。既存の整数不等式を直接コピーせず、変数変換後の関数値と最大値を分数で評価する。

奇数 k、r=q-3、a=(r+2)/(r+1)、y*=ka/(k+1)、F(y)=r-y-(a-y)y^k。候補区間 (1,a) で H(y)=(a-y)y^k の最大は y* である。k_- に対して H(y*)<r-a を確認すれば F(y)>0 が全候補区間で成立し、k_+ では F(y*)<0 と F(1)>0、F(a)>0 により2根が存在する。符号変化2回と k 単調性の一般論は元の証明を参照する。

以下は **Python標準ライブラリの Fraction だけ**を用いる独立算術検査であり、先行証明の交差乗算式を呼び出さない。

```python
from fractions import Fraction

bounds = [(101,1265),(102,1281),(103,1295),(104,1311),
          (105,1325),(106,1341),(107,1355),(108,1371),
          (109,1385),(110,1401)]
for q, kp in bounds:
    r = q-3
    a = Fraction(r+2, r+1)
    for k, exists in ((kp-2,False),(kp,True)):
        y = a * Fraction(k,k+1)
        assert 1 < y < a
        H = (a-y)*y**k
        F = r-y-H
        if exists:
            assert F < 0 and r-1-(a-1) > 0 and r-a > 0
        else:
            assert H < r-a
            assert F > 0
print("20 Fraction boundary checks passed")
```

検査結果: 20/20 PASS（2026-11-06）。境界以外の全奇数 k への拡張は既存の解析的単調性に依存する。この監査は算術検算の独立実装であり、新しい q 範囲の定理や一般 q の接触二重根不存在を主張しない。
