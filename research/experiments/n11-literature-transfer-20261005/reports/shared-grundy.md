# Sprouts型の共有Grundy表を11×11残余ゲームで試す

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

T. Čížek, M. Balko, M. Schmid, *Massively Parallel Proof-Number Search for Impartial Games and Beyond* (arXiv:2511.10339v1, AAAI 2026) は、Sproutsで二段階並列PNS/DFPNを行い、worker間で計算済みGrundy値を共有する。1024 coreで逐次DFPN比 **332.97±26.8倍**、従来Sprouts solver GLOP比では概算4桁高速化を報告している。

共円ゲームも通常プレイの不偏ゲームであり、現在の残余hypergraphは独立連結成分へ分解してGrundy xorを取れる。そこで「共有すべき小部品が実際に別の11×11残局へ再出現するか」を保存済み残局で測った。

## 方法

`research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json` の826 snapshots（200 greedy trajectories）を使う。

各snapshotについて、inclusion-minimal residual hypergraphをfull incidenceで連結成分分解し、各成分をrank 2/3/4の全edgeを含むclutterとして扱う。color refinement後、未分離cellの全置換を列挙して完全同型のcanonical labelを作り、同じtrial内だけの繰返しを除外して別trialにも現れる型だけを共有候補とした。各型は独立mexで解き、「毎回fresh solve」と「型ごとに一度だけsolve」のmemo state数を比較した。

pair graphやhashだけで同一視しない。今回のcross-trial候補はすべて置換gate内で完全canonical化できた。

## 結果

- snapshots: **826**
- residual connected components: **1,011**
- 別trialへ再出現する完全同型型: **26**
- その出現総数: **603**
- 孤立1点を除く非自明成分の出現: **238**

| 成分頂点数 | 型数 | 出現数 |
|---:|---:|---:|
| 1 | 1 | 365 |
| 2 | 1 | 92 |
| 3 | 2 | 53 |
| 4 | 7 | 53 |
| 5 | 10 | 30 |
| 6 | 5 | 10 |

Grundy値別では g=0 が8型22出現、g=1が5型480出現、g=2が6型82出現、g=3が7型19出現だった。

同じ型を毎回fresh mexすると、この再出現部分だけでmemoized residual stateが **1,676**。型ごとに一度だけ計算して共有すれば **174** で足り、構造上 **89.6%減**。孤立1点を除いても **946 → 172、81.8%減** だった。

## 解釈

これは本番exact searchのwall timeが81.8%減るという意味ではない。保存snapshotはgreedy軌跡に偏り、canonical化やresidual構築にも費用がある。

それでも、Sprouts論文の「Grundy値は小さく、worker間で配りやすく、広く再利用できるkey result」という条件が、共円の終盤残余成分でも少なくとも有限実験上成立している。

現在のC++ residual micro-kernelは成分分解とmexを持っているため、次の実装差分は比較的小さい。

- component canonical label → Grundy の専用cacheをmain df-pn TTとは分離して持つ。
- process内だけでなく、coordinator worker間でも小さいcomponent resultを共有する。
- まず legal<=12 のresidual micro-solver内だけで発火させる。
- cold s5 replay 23 rootsで、cacheなし/局所cache/共有component cacheを同一wall条件で比較する。
- hit数ではなくaggregate wall timeで採否を決める。

特にSprouts論文と同様、proof/disproof bound全体を同期するより、確定した小さなGrundy部品だけを同期する方が通信量と健全性の境界を小さくできる。

## 再現

```bash
uv run --locked python research/experiments/n11-literature-transfer-20261005/scripts/component_reuse_audit.py \
  --out research/experiments/n11-literature-transfer-20261005/output/component-reuse-audit.json
```

## C++実装A/B

その後、上の候補を `cpp/solvers/kyouen_residual_micro.hpp` と
`cpp/solvers/kyouen_dfpn_root.cpp` に実装した。main TTとは分離し、
小残余成分だけを任意頂点置換でcanonical化して完成Grundy値を共有する。

健全性は、4頂点以下の全clutter **2,068件**について
素朴mex / 従来micro-kernel / 共有Grundy版の3者一致で検査した。

11×11の固定s5 replay 3件では、share gate=6で:

| 指標 | 共有なし | 共有あり |
|---|---:|---:|
| residual memo states | 3,803,408 | **1,066,012** |
| shared hits | 0 | **1,064,207** |
| 最終shared component型 | 0 | **1,805** |

memo state数は約72%減った。一方、最初の完全canonical化実装は6頂点で最大 `6!=720`
置換を毎回列挙したため、wallは **123s → 145s** と悪化した。

そこで頂点–hyperedge incidenceにisomorphism-invariant color refinementをかけ、
安定色が同じ頂点だけを置換するよう変更した。完全同型canonical keyの厳密性は保つ。
この変更後、同じCI A/Bは **123s → 126s** まで改善した。

したがって現在の評価は「構造圧縮は明確に効くが、gate=6ではwallで約2.4%負ける」。
共有方式そのものを捨てる根拠ではなく、canonical化費をもう少し下げるか、
より再利用率の高いbatch/worker間共有で償却するのが次の焦点である。

観測run: CI run `37256739394`（head `415b27ed2e4c10830875d0d825e3b9d4e3755789`）。
