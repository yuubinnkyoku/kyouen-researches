# Relevance-Zone Reduction の共円への直接移植は不健全

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

Go/Connect6系のRelevance-Zone Searchでは、証明に関係しないzone外の着手をnull moveとして扱い、局所証明を再利用する。共円ゲームでも残余局面が局所成分へ分かれるため一見似ているが、通常プレイの不偏ゲームではzone外の独立成分が手番偶奇を変え得る。

保存済み11×11残局から、直接移植への具体的反例を得た。

## 反例

occupied:

`{14,22,29,35,51,56,59,66,75,76,94,97,101,119}`

legal:

`{8,93,112}`

inclusion-minimal residual edges:

`{{93,112}}`

したがってfull-incidence residual gameは二成分へ分かれる。

- 孤立成分 `{8}`: Grundy **1**
- pair成分 `{93,112}` with edge `{93,112}`: Grundy **1**

全体Grundyは `1 xor 1 = 0` なのでP-position。

もし `{8}` を「局所証明のzone外で、内部の合法性を変えないnull move」として捨てると、残る成分のGrundyは1なのでN-positionになる。**勝敗が反転する。**

## 結論

Connect6/Go型の「zone外は無視して同じ局所戦略をreplayする」という規則は、共円の通常プレイへそのまま持ち込めない。外側の一手が局所hypergraphを変化させなくても、独立なnormal-play componentとしてGrundy xorへ寄与するためである。

共円での健全な対応物は次の形になる。

- zone/component内部は局所canonical化・局所証明してよい。
- zone外を削除してはいけない。
- zone外の独立成分は **Grundy値へ要約**して残す。
- 再利用キーは「局所zone pattern」だけでなく、他成分nimberとのxor文脈を含めるか、局所成分のnimberそのものを保存する。

これはSprouts型の共有Grundy表がRelevance-Zoneの直接移植より共円に適している理由でもある。

## 出典データ

`research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json` の snapshot index 14 / trial 3。
