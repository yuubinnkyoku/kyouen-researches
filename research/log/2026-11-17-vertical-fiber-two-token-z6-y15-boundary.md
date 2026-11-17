# 2026-11-17 高速レーン: 2トークン残余ゲーム z=6,y=15切片の全称証明

## 作業前の確認

作業開始時の最新mainは afd3a452195533af9d396e14deead67a00e403be。AGENTS.mdの直接main反映・SSOT・生成物非編集・検査規則を確認した。research/knowledge/README.md、SCHEMA、VOCABULARY、K0832、K0873、K0899、K0901と直近のREMO K0902を確認した。research、research/knowledge、research/experiments、research/log以下に追加のAGENTS.mdはなかった。K0903は未使用だった。

## 選定と発見

次の自然な境界 y=15 を選んだ。再帰
\[
A=H(R-1;(x-1,15);6),\quad
B=H(R-1;(x,14);6),\quad
C=1\oplus H(R-1;(x,15);5)
\]
により、Aは同じ切片のR強帰納、BはK0901、CはK0873へ落ちる。x=15ではA/Bの子が正準化後に同一の(15,14)状態へ合流する。

値2位置は基本ラダー {1,3,5} に加え、x=15で33、x=19で35、x=22で37,39,41,43、x≥23で37となった。値1位置も全xの閉形式を得た。過渡域はx=15..23、定常域はx≥24に分かれる。tailはR≥x+22で(x+15) mod 2。

値2位置はK0832の3族予想のz=6,y=15特殊化と一致する。ただし今回の証明範囲はこの切片だけで、3族予想全体を証明したものではない。

## 証明と独立監査の区別

全称性はA/B/C署名表、K0832のTheorem T、一般tail定理とR強帰納による。検証器は順序付き再帰と降順正準化再帰を実装し、z=6,y=15、z=6,y=14、z=5,y=15の公式アンカー17,388件を照合した。さらに署名2,042,601件、mex2,042,601件、奇数親上界1,021,797件、偶数親上界1,020,804件、値2位置1,986件、3族特殊化1,986件、tail129,090件、固定seed遠方tail2,000件を検査し、不一致0。監査JSONは別実行二回でバイト単位に一致した。

有限監査を全称証明とは扱わない。全称性の根拠は証明報告の明示的な署名表と帰納構造である。

## 反映

- K0903: research/knowledge/items/K0903-two-token-z6-y15-boundary.md
- 証明: research/experiments/vertical-fiber-two-token-z6-y15-boundary-20261117/report.md
- 検証器: research/experiments/vertical-fiber-two-token-z6-y15-boundary-20261117/verify_z6_y15.py
- 監査: research/experiments/vertical-fiber-two-token-z6-y15-boundary-20261117/output/audit.json

K0832本文、knowledge READMEの証明済み境界をy=15へ進め、未解決境界をy≥16へ修正する。Knowledge generated workflowに検証器を追加し、生成ファイルは直接編集しない。

## 未解決

- z=6,y≥16の全Grundy分類
- z≥7の全Grundy分類
- 3族値2位置一般式の全称証明
- 標準二次元共円ゲームの固定幅・q点版の真の安定化長

次の境界候補はz=6,y=16。今回の依存はBにK0901、CにK0873を使え、Aはy=15の帰納仮説に接続できる。
