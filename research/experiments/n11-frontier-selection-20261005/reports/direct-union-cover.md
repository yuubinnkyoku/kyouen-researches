# Othello型frontier選択をunique s5集合へ直接寄せる

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

## 背景

`weighted-cover.md` では、Othelloの弱解決で使われた「根の証明に必要な中間局面だけを選ぶ」考え方を
中心初手60・隅応手0の二石rootへ移し、31-classという既知最小class数を固定したまま、
各classの未解決s5 child数の**加法和**をMILPで最小化した。

しかし本当に支払うexact仕事は加法和ではない。複数classが同じcanonical s5 rootを共有するなら、
そのrootは一度解けばよい。従って直接の対象は

```
selected classes が要求する unknown canonical s5 key の集合和
```

である。

## 現在の検証済み情報を固定

K0329の独立検証済み結果だけを既知情報として使う。

- LOSS class `(1152921504606846983,0)`: s5 child 103件
- LOSS class `(1152921504606848001,4)`: s5 child 106件
- 上の2集合のoverlapは0、既知LOSS s5は合計 **209件**
- WIN class `(1152921504606848001,8)` は候補から除外

二つのLOSS classは31-class witnessへ必ず含める。

## 探索

K0335のdual certificateで正の重みを持つ62頂点について、31-class coverは各classがちょうど2頂点を
覆う必要がある。従って31-class witnessはこの62頂点上のperfect matchingとして探索できる。

1. 各dual pairについて未知s5 childが少ないclassを選び、minimum-weight matchingを初期解にする。
2. 同じdual pairを持つ別classへの置換を試す。
3. matchingの2辺 `ab,cd` を `ac,bd` または `ad,bc` へ交換する。
4. 交換後も119/119第三手を覆う場合だけ受理する。
5. 評価値は加法和でなく、**既知209件を除いたcanonical s5 key集合の実際のunion size**。

これは局所探索なので、unique-s5目的の大域最適性は主張しない。
直接unionを0-1変数化したMILPも試せるが、class 3396に加えてs5変数が12万個規模となるため、
まず明示witnessを得て検証する方を優先した。

## 結果

31 class・119/119 coverageを保ち、既知LOSS 2 classを必須、既知WIN classを除外した明示witnessが得られた。

| frontier | 全selected unique s5 | 既知209件を除くunique unknown s5 |
|---|---:|---:|
| K0335の定理witness | 3,336 | **3,229** |
| 既存の加法的weighted cover | — | **2,812** |
| **direct-union witness** | **2,528** | **2,319** |

定理witness比で **3,229 → 2,319、910件減、28.18%減**。
既存の加法的weighted cover比でも **2,812 → 2,319、493件減、17.53%減**。

class数は31のままなので、K0335の最小class数を犠牲にしていない。

## 意味

これはwall timeが28.18%減るという主張ではない。s5 rootごとのexact node数は大きく異なる。
ただし現在のcoordinatorの目的関数を「coverage最大・unknown child数最小」から、
**最終31-class certificate全体のmarginal unique s5集合**へ変える価値は明確になった。

特に今後は、各unknown s5に一律1ではなく

- cold replay実測node数
- timeout時の下限node数
- residual micro-solverの推定cost
- 既存component Grundy cacheで即答できるか

を重みにし、集合和の「新規に支払う予測node cost」を直接下げるのが自然である。

Othello型の教訓は「全境界局面を速く解く」だけでなく、
**根の証明に本当に必要な境界局面集合そのものを選び直す**ことだと解釈できる。
共円ではs4 coverがその選択層になっている。

## 検証

witness:
`research/experiments/n11-frontier-selection-20261005/output/direct-union-cover.json`

独立再計算:
```bash
uv run --locked python research/experiments/n11-frontier-selection-20261005/scripts/verify_direct_union_cover.py
```

検証器は保存済みcoverageやchild数を信用せず、盤面規則から全3396 classを再生成し、

- 31 class
- 119/119 coverage
- 既知LOSS 2 classを含む
- 既知WIN classを含まない
- known s5 = 209
- selected unique s5 = 2528
- unknown unique s5 = 2319
- 定理witnessのunknown unique s5 = 3229

を再計算する。
