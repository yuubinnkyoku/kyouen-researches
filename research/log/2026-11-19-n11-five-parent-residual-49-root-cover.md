# 2026-11-19 n11: receipt-aware five-parent residual cover — 97 rows, exact 49-root minimum

## 基準と問い

計算開始時のmainは `8af969be132ca709dd79fbc472ec198f55fe53d1`。AGENTS.md、knowledge README、K0863/K0865/K0868、head-1410のjoint-cover監査、head-1476のcost71e verdict join、global receipt fold、cost78c/79cのcombined foldを確認した。

head-1410の5親joint targetは112個のS6行を持つ。head-1589のglobal receipt foldはそのうち13行を既に閉じ、後続のcost78c/79c foldがさらに2行を閉じていた。ここを反映せずに112行すべてを新規探索対象とみなすのは無駄である。

## 1. 既存receiptを引いた残り

- 5親の対象行 union: **112**
- global fold 113行との交差: **13**
- cost78c/79c fold 19行との交差: **2**
- 交差は相互に重ならず、receipt閉鎖済みは **15行**
- 残る対象は **97行**

global foldとcost78c/79c foldのreceipt行を直接照合した。単なる親単位の件数差ではない。

## 2. 残97行の最小候補root cover

独立監査済みの全候補universeは6,542 D4 root（1行root 4,885、2行root 1,657）で、1 rootが覆う対象行は最大2行。したがって97行の被覆には少なくとも

[
\lceil 97/2 \rceil = 49
]

rootが必要。

31個の親部分集合に対する公開済みjoint witnessから117個の異なる候補rootを集め、明示的に利用できる既知verdictを照合した。

- 照合した既知verdict: REFUTED-D10 236 root、WIN7-D10 156 root
- 117候補との交差: REFUTED-D10 5 root、WIN7-D10 0 root
- 5個のREFUTED rootを除いた残余グラフ: 92 pair edge、14 singleton対象行
- 最大マッチング: **48 pair**
- unmatched row: `00000000020000809002000040000000`
- そのsingleton候補: `00000000040000801202000080080000`

48本のpair rootと1本のsingleton rootで97行を重複なく覆う。よって残97行の最小候補root coverは **ちょうど49本**。下界と達成例が一致した。

49本すべてをBigInt整数幾何で再検査した。各rootは7石、D4正準形、35個の四点組すべてでdet4≠0。残97行の被覆は97/97、重複0、欠落0。

## 3. 何が確定し、何が未確定か

今回確定したのは、既存receiptを反映した**候補root被覆の最小値と具体的な達成例**である。49本はまだWIN7-D10証明書ではなく、新しいengine verdictも作っていない。

既知verdictの照合範囲にも境界がある。head1476 cost71e、cost73j、cost78c、cost79cの公開sweep/transferと既存receipt foldを合算したが、K0863に記録された8,964件すべてのper-root cacheをこの回で再構成したわけではない。したがって49本の全cache照合は未完了であり、次の実探索前に残る作業である。

## 再現資料

- [再現スクリプト](../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_five_parent_residual_49_cover_20261119.mjs)（blob `bdf7650b236c30c6d18fdedb8405976db070dba1`）
- [結果JSON](../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json)（blob `a8eaf00bd6494eda50a68e7d06498bed833a7688`）
- 入力blob SHA、49 rootの一覧、全rootの幾何検査結果は結果JSONに固定した。

この回の数値計算は固定blobをV8上で再計算した。公開Nodeスクリプトそのものはこの実行環境のcheckout上では起動していない。入力blobのSHA pinと独立監査結果で照合している。

## 次の判断

1. 49候補を8,964件のper-root verdict cacheへ完全joinする。
2. 既知REFUTEDを除いたまま、coordinatorで実測探索費用を比較する。
3. 選ばれた候補だけを少数workerで探索し、WIN7-D10証明書を独立検証してからreceipt foldする。

反映直前にmainは `1b5683fb6e42b8e46f0e43f20a98def5d6fba81a` へ進んだが、今回の全入力blobとK0865/knowledge READMEはbyte-identicalだったため、このheadを親として直接反映した。

REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
