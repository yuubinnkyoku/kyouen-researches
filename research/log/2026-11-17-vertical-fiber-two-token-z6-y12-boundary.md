# 2026-11-17 高速レーン: 2トークン残余ゲーム z=6,y=12切片の全称証明

## 作業前の確認

最新mainは 2700ed3c4b1354582bb3db701602a70d209a0d9b。AGENTS.mdの直接main反映・SSOT・生成物非編集・検査規則を確認した。research/knowledge/README.mdではz=6,y=1..11がK0877/K0878/K0879/K0880/K0884/K0885/K0887/K0888/K0890/K0892/K0894で全称証明済み、y≥12とz≥7が未解決と記されていた。K0895は別レーンのREMO項目で使用済み、K0896は未使用だった。K0832、K0873、K0890、K0892、K0894の現行正本と対応する証明・検証器を読み、今回のA/B/C依存を確認した。

## 発見

次の自然な境界 y=12 を選んだ。再帰
\[
A=H(R-1;(x-1,12);6),\quad
B=H(R-1;(x,11);6),\quad
C=1\oplus H(R-1;(x,12);5)
\]
により、Aは同じ切片のR強帰納、BはK0894、CはK0873へ落ちる。x=12ではA/Bが同じ正準化子に合流する。

選択肢署名を導くと、過渡域x=12..20と定常域x≥21に分かれた。値2位置は
\[
\{1,3,5\}\cup
\begin{cases}
\{27\}&x=12,\\
\{29\}&x=16,\\
\{31,33,35,37\}&x=19,\\
\{31\}&x\ge20,\\
\varnothing&\text{otherwise}.
\end{cases}
\]
値1位置もK0896の証明報告に閉形式で記録した。tailはR≥x+19で(x+12) mod 2。

値2位置はK0832の3族予想のz=6,y=12特殊化と一致する。ただし今回の証明範囲はこの切片だけで、3族予想全体を証明したものではない。

## 証明と独立監査の区別

全称性はA/B/C署名表、K0832のTheorem T、一般tail定理とR強帰納による。検証器は順序付き再帰と降順正準化再帰の二方式を実装し、z=6,y=12、z=6,y=11、z=5,y=12の公式アンカーを5,394件照合した。さらに署名2,036,736件、mex2,036,736件、奇数親上界1,018,865件、偶数親上界1,017,871件、3族特殊化1,989件、tail129,285件、固定seed遠方tail2,000件を検査し、不一致0。別実行二回の監査JSONはバイト単位で一致した。

この有限監査を全称証明とは扱わない。全称性の根拠は証明報告の明示的な署名表と帰納構造である。

## 反映

- K0896: research/knowledge/items/K0896-two-token-z6-y12-boundary.md
- 証明: research/experiments/vertical-fiber-two-token-z6-y12-boundary-20261117/report.md
- 検証器: research/experiments/vertical-fiber-two-token-z6-y12-boundary-20261117/verify_z6_y12.py
- 監査: research/experiments/vertical-fiber-two-token-z6-y12-boundary-20261117/output/audit.json

READMEの証明済み境界をy=12へ進め、未解決境界をy≥13とz≥7へ更新した。Knowledge integrity workflowへ検証器を追加し、生成ビュー更新を既存workflowに任せる。生成ファイルは直接編集しない。

## 未解決

- z=6,y≥13の全Grundy分類
- z≥7の全Grundy分類
- 3族値2位置一般式の全称証明
- 標準二次元共円ゲームの固定幅・q点版の真の安定化長

次の境界候補はz=6,y=13。今回の依存はBにK0896、CにK0873を使える。
