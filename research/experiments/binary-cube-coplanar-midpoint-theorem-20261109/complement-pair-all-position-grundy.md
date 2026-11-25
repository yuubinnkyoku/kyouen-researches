# 補対頂点層ゲームの全安全局面Grundy公式（2026-11-10）

## 対象と証拠水準

既存の [重み1・重み(d−1)層の固定終局長](weight-one-coweight-one-fixed-length.md) の通常プレイを強化する。d>=3 とし、頂点を d 個の補対 P_i={e_i,1-e_i} に分ける。禁止集合は二つの補対の合併。以下は **全称数学的証明** であり、独立した全安全局面の再帰列挙でも d=3..7 を照合した。

## 定理

安全局面 S について、両頂点が選ばれた補対の個数を c（0または1）、一方だけが選ばれた補対の個数を b、どちらも選ばれていない補対の個数を a とする。a+b+c=d。

通常プレイの Sprague–Grundy 値は

- c=1 の場合、g(S)=a mod 2。
- c=0 の場合、a+b=0 なら g(S)=0。それ以外は **a が偶数なら1、奇数なら0**。

特に空盤は g=1 (d偶数)、g=0 (d奇数)。しかも全安全局面のGrundy値は0か1だけであり、局面の幾何学的な位置には依存しない。

## 証明

c=1 の局面では、既に完成した補対があるため、他の補対の残りの頂点を選ぶことはできない。空の補対から一つ選ぶ手だけが可能で、a が1減る。従って g=a mod 2。

c=0 の局面で b>0 なら、一石補対を完成させる手が存在し、その子は c=1、空補対数 a のため値 a mod 2。a>0 なら空補対に置く手があり、子は c=0、空補対数 a−1、一石補対数 b+1 となる。

a=0,b>0 なら完成手しかなく、g=mex{0}=1。a=b=0 なら合法手がなく g=0。a>0 の場合、a に関する帰納法を使う。空補対への着手後の値は、a−1 が偶数なら1、奇数なら0、すなわち a mod 2 が0なら0、1なら1。b>0 の場合、完成手の値も a mod 2 で一致する。b=0 の場合も空補対への着手後の値は同じである。したがって mex{a mod 2}=1−(a mod 2)。証明終。

## 独立全局面照合

以下は **補対ごとの状態を圧縮せず**、2d 個の頂点のビット集合から合法手を生成して再帰的に mex を求める検算である。d=3..7 で全安全局面を検査し、件数は 54,189,648,2187,7290。一般式は c=0 の3^d局面と c=1 の d*3^(d−1)局面の和、(d+3)3^(d−1) に等しい（ただし c=1 の残りの補対は空/片方選択の3状態）。

```python
from functools import lru_cache

for d in range(3, 8):
    @lru_cache(None)
    def grundy(mask):
        children = set()
        for k in range(2*d):
            if mask >> k & 1:
                continue
            nxt = mask | (1 << k)
            completed = sum(
                bool(nxt >> i & 1) and bool(nxt >> (d+i) & 1)
                for i in range(d)
            )
            if completed <= 1:
                children.add(grundy(nxt))
        return next(x for x in range(3) if x not in children)

    checked = 0
    for mask in range(1 << (2*d)):
        c = sum(bool(mask >> i & 1) and bool(mask >> (d+i) & 1)
                for i in range(d))
        if c > 1:
            continue
        a = sum(not ((mask >> i & 1) or (mask >> (d+i) & 1))
                for i in range(d))
        expected = a % 2 if c else int(a % 2 == 0 and mask != (1 << (2*d))-1)
        # c=0, a=b=0 cannot occur for d>=1, so expected reduces to parity.
        assert grundy(mask) == expected, (d, mask)
        checked += 1
    assert checked == (d+3) * 3**(d-1)
    print(d, checked, grundy(0))
```

注: c=0, a=b=0 は d>=1 では不可能であり、上の一般式の例外分岐は抽象的な d=0 の場合だけ必要。

## 範囲

重み1と重み(d−1)層のみを使う変種の全局面結果。全頂点版のGrundy値や共円ゲーム標準盤の勝敗を主張しない。既存の固定終局長定理から空盤勝敗は分かっていたが、全安全局面の値が0/1に限られることは追加の結果である。
