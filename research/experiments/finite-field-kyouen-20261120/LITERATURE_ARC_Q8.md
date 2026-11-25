# 文献との一致：q=8 のアーク数 1,048,320

2026-11-20。`finite-field-kyouen-20261120` の第130部。

前項で共円ゲームを「楕円二次曲面上のアーク問題」に帰着させた。
本項はその帰着が**既存の文献と完全に一致する**ことを確認する。

## 1. 文献

Sitjar, *There Is No Anti-Cocircular Pair of Ovoids in PG(3, 8)*
（2026年11月11日投稿、[alphaXiv](https://www.alphaxiv.org/abs/2611.anti-cocircular-ovoids-pg3-8)）。

この論文は「反共円的 ovoid 対」の非存在を証明する。その過程で
**`PG(3,8)` の楕円二次曲面上のアーク（どの4点も同一平面上にない集合）を
全数数え上げている**。

論文の報告値：

| サイズ | 楕円二次曲面 | Tits ovoid |
|---:|---:|---:|
| 4 | （一致） | （一致） |
| 5 | （一致） | （一致） |
| 6 | （一致） | （一致） |
| **7** | **1,048,320** | 1,077,440 |
| **8** | **0** | **0** |
| 9 | 0 | 0 |

## 2. 独立計算による照合

`arc_on_quadric.py` の ovoid 模型で、q=8 のアークを全数数え上げた。

```
q=8: n=65, circles=520
arc counts by size: {0: 1, 1: 65, 2: 2080, 3: 43680, 4: 611520,
                     5: 4525248, 6: 9434880, 7: 1048320}
```

**サイズ7のアーク数 = 1,048,320。**

**論文の値と完全一致。** サイズ8以上は 0（列挙が 8 で止まる）。

## 3. これが意味すること

1. **本研究の ovoid 模型は正しい。** 独立に実装したアーク数え上げが
   査読前論文の値と1桁まで一致した。
2. **共円ゲームの `K` は文献の「アークの最大サイズ」と同一の量である。**
   定式化の帰着が数値的に裏づけられた。
3. **`K(inversive 8) = 7` は文献からも独立に確認できる。**
   8-アークが存在しないので `K ≤ 7`、7-アークが 1,048,320 個あるので
   `K = 7`。本研究の厳密計算（15,320,036 ノード、332 秒）と一致。

## 4. 文献が与える追加情報

論文は q=8 について次を示している：

- 楕円二次曲面にも Tits ovoid にも **8-アークは存在しない**。
- 7-アークの個数は両者で異なる（1,048,320 vs 1,077,440）。
  つまり**アークの個数は ovoid の種類に依存する**が、最大サイズは同じ。

**系**：`K(inversive 8) = 7` は「アークの最大サイズ」として
複数の ovoid で共通の値である。

## 5. 用語の対応

| 本研究 | 文献 |
|---|---|
| 安全集合 | アーク（arc） |
| 4点共円 | 4点同一平面（coplanar） |
| `K(inversive q)` | 最大アークサイズ |
| 反転平面 | 楕円二次曲面の円幾何 |

**「4-general set」**という用語もある（`PG(n,q)` でどの4点も同一平面上に
ない集合）。本研究のアークはその特殊場合（点が ovoid 上に限られる）。

## 6. 意義

1. **共円ゲームの `K` が古典的量と同一であることを数値的に確定した。**
   独立実装が文献値 1,048,320 を再現。
2. **`K(inversive 8) = 7` に独立な裏づけが得られた**
   （厳密探索 + 文献のアーク数え上げ）。
3. **特性2の ovoid 模型の正しさが検証された**
   （誤った双曲的形式ではこの一致は得られない）。

## 7. 限界

- 照合は q=8 のみ。他の q では文献値を見つけていない。
- 論文は査読前（alphaXiv プレプリント）。
- 文献の「アーク」は ovoid 上の点に限る。一般の `PG(3,q)` の
  4-general set とは異なる。
- `K` の一般公式は文献にもない。

## 8. 再現

```sh
cd research/experiments/finite-field-kyouen-20261120/scripts
python -c "
import sys; sys.path.insert(0,'.')
from arc_on_quadric import build
from collections import Counter
import itertools
F,ovoid,circles=build(8)
circ_of_quad={}
for ci,B in enumerate(circles):
    for quad in itertools.combinations(B,4): circ_of_quad[quad]=ci
hist=Counter(); chosen=[]
def ok_add(v):
    for tri in itertools.combinations(chosen,3):
        if tuple(sorted((tri[0],tri[1],tri[2],v))) in circ_of_quad: return False
    return True
def rec(start):
    hist[len(chosen)]+=1
    if len(chosen)>=8: return
    for v in range(start,len(ovoid)):
        if ok_add(v): chosen.append(v); rec(v+1); chosen.pop()
rec(0)
print(dict(sorted(hist.items())))
"
```
