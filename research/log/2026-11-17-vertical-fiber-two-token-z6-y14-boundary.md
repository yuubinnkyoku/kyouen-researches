# 2026-11-17 高速レーン: 2トークン残余ゲーム z=6,y=14切片の全称証明

## 作業前の確認

作業開始時の最新mainは cc3ac6a69e3a4b5b7988f90e1f82974500791478。AGENTS.mdの直接main反映・SSOT・生成物非編集・検査規則を確認した。research/knowledge/README.mdではz=6,y=1..13が全称証明済み、y≥14とz≥7が未解決。K0832本文、K0873、K0890、K0892、K0894、K0896、K0899と対応する証明・検証器を確認した。K0901は未使用で、K0900は別レーンのREMO r=12独立検証項目だった。research以下に追加のAGENTS.mdはなかった。

## 選定と発見

次の自然な境界 y=14 を選んだ。再帰
\[
A=H(R-1;(x-1,14);6),\quad
B=H(R-1;(x,13);6),\quad
C=1\oplus H(R-1;(x,14);5)
\]
により、Aは同じ切片のR強帰納、BはK0899、CはK0873へ落ちる。x=14ではA/Bの子が正準化後に同一の(14,13)状態へ合流する。

値2位置は基本ラダー {1,3,5} に加え、x=14で31、x=18で33、x=21で35,37,39,41、x≥22で35となった。値1位置も全xの閉形式を得た。過渡域はx=14..22、定常域はx≥23に分かれる。tailはR≥x+21で(x+14) mod 2。

値2位置はK0832の3族予想のz=6,y=14特殊化と一致する。ただし今回の証明範囲はこの切片だけで、3族予想全体を証明したものではない。

## 証明と独立監査の区別

全称性はA/B/C署名表、K0832のTheorem T、一般tail定理とR強帰納による。検証器は順序付き再帰と降順正準化再帰を実装し、z=6,y=14、z=6,y=13、z=5,y=14の公式アンカー11,562件を照合した。さらに署名2,040,649件、mex2,040,649件、奇数親上界1,020,821件、偶数親上界1,019,828件、3族特殊化1,987件、tail129,155件、固定seed遠方tail2,000件を検査し、不一致0。監査JSONは別実行二回でバイト単位に一致した。

この有限監査を全称証明とは扱わない。全称性の根拠は証明報告の明示的な署名表と帰納構造である。

## 反映

- K0901: research/knowledge/items/K0901-two-token-z6-y14-boundary.md
- 証明: research/experiments/vertical-fiber-two-token-z6-y14-boundary-20261117/report.md
- 検証器: research/experiments/vertical-fiber-two-token-z6-y14-boundary-20261117/verify_z6_y14.py
- 監査: research/experiments/vertical-fiber-two-token-z6-y14-boundary-20261117/output/audit.json

knowledge READMEとK0832本文の証明済み境界をy=14へ進め、未解決境界をy≥15へ修正する。Knowledge generated workflowに検証器を追加し、生成ファイルは直接編集しない。

## 未解決

- z=6,y≥15の全Grundy分類
- z≥7の全Grundy分類
- 3族値2位置一般式の全称証明
- 標準二次元共円ゲームの固定幅・q点版の真の安定化長

次の境界候補はz=6,y=15。今回の依存はBにK0899、CにK0873を使え、Aはy=14の帰納仮説に接続できる。