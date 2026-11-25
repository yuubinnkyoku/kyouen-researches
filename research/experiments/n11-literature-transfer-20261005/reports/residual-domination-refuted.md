# 7-in-a-row型の頂点支配は共円残局では使えない

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

## 動機

Czifra–Csóka–Zombori–Makay, *Towards solving the 7-in-a-row game* は、
maker-breaker型の残余超グラフで「頂点 (u) が (v) の所属辺をすべて含むなら、
(v) の代わりに (u) を選べる」という頂点支配を使い、PNSを大きく縮めている。

共円の終盤も残余超グラフで表せるため、一見かなり移植しやすい。
しかし共円の残局はmaker-breakerではなく、両者が同じ合法手集合から石を取る
**不偏normal-play** である。そこで移植前にsoundnessを全件監査した。

## 抽象clutterでは即反例

4頂点、最小禁止辺

```
{0,1,2}
{0,1,3}
```

を考える。頂点0は2より多くの辺に属し、所属辺集合は

```
E(0) = {両方}
E(2) = {{0,1,2}}
```

なので、maker-breaker流には0が2を支配する。

ところが厳密mexでは

- 2を打った後のGrundy = **0**
- 0を打った後のGrundy = **2**

となる。現在局面の手番側にとって2は勝ち手、0は勝ち手ではない。
したがって一般の不偏clutterでは支配置換は不正。

## 実11×11盤面にも反例

保存済みn=11残局826局面を、残余連結成分へ分解して全監査した。

- 残余成分: **1,011**
- strict incidence dominationを含む成分: **191**
- ordered domination pair: **330**

反例は snapshot 13 / trial 3 に存在した。

占有点:

```
14,22,29,35,51,56,59,66,75,76,94,97,119
```

合法点:

```
8,43,93,101,109,112
```

最小残余辺:

```
{8,43}
{43,93}
{43,101}
{43,109}
{93,112}
{101,109}
```

43は4本の辺、8は1本の辺に属し、8の所属辺は43の所属辺に完全包含される。
それでも厳密mexでは

- 8を打った後のGrundy = **0**
- 43を打った後のGrundy = **1**

であり、8は勝ち手だが43は勝ち手ではない。

さらに既存の独立幾何実装
`verify_modules.independent_geometry` で占有13点から合法点と残余辺を再生成し、
上の6辺と完全一致した。保存JSONの転記ミスではない。

## 結論

**7-in-a-row型の頂点支配を、共円の残余micro-solverやdf-pnのsoundな枝刈りとして
導入してはいけない。**

同じ「超グラフの包含関係」でも、

- maker-breaker: 強い頂点へ置換できる単調性がある
- 共円残局: 手数偶奇・mexが絡むため、より多くの禁止辺を消す手が有利とは限らない

という差が本質的。

これは性能上の失敗ではなく、**正しさの反例**なので候補から除外する。

## 再現

```bash
python research/experiments/n11-literature-transfer-20261005/scripts/audit_residual_domination.py \
  research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json \
  --out /tmp/residual-domination-audit.json
```

要約結果は
`research/experiments/n11-literature-transfer-20261005/output/residual-domination-audit.json`
に保存した。
