# 2026-11-17 高速レーン: 2トークン残余ゲーム z=6,y=16切片の全称証明

## 作業前の確認

作業開始時の最新mainは \`8f74c6cdae13e7019c84be486459842c78b84713\`。root \`AGENTS.md\`、\`research/knowledge/README.md\`、SCHEMA、K0832、K0873、K0903、K0904を確認した。research/knowledge、research/experiments、research/log以下に追加のAGENTS.mdはなかった。K0905は未使用だった。READMEの未解決一覧ではz=6,y≥16が次の境界であり、同じy=16を扱う既存項目はなかった。

## 選定と発見

次の自然な境界 \(y=16\) を選んだ。再帰
\[
A=H(R-1;(x-1,16);6),\quad
B=H(R-1;(x,15);6),\quad
C=1\oplus H(R-1;(x,16);5)
\]
により、Aは同じ切片のR強帰納、BはK0903、CはK0873へ落ちる。\(x=16\) ではA/Bの子が正準化後に同一の(16,15)状態へ合流する。

値2位置は基本ラダー \(\{1,3,5\}\) に加え、x=16で35、x=20で37、x=23で39,41,43,45、x≥24で39となった。値1位置も全xの閉形式を得た。過渡域はx=16..24、定常域はx≥25に分かれる。tailはR≥x+23で(x+16) mod 2。

値2位置はK0832の3族予想のz=6,y=16特殊化と一致する。ただし今回の証明範囲はこの切片だけで、3族予想全体を証明したものではない。

## 証明と独立監査の区別

全称性はA/B/C署名表、K0832のTheorem T、一般tail定理とR強帰納による。検証器は順序付き再帰と降順正準化再帰を実装し、z=6,y=16、z=6,y=15、z=5,y=16の公式アンカー19,305件を照合した。さらに署名2,044,550件、mex2,044,550件、奇数親上界1,022,771件、偶数親上界1,021,779件、値2位置1,985件、3族特殊化1,985件、tail129,025件、固定seed遠方tail2,000件を検査し、不一致0。監査JSONは別実行二回でバイト単位に一致した。

有限監査を全称証明とは扱わない。全称性の根拠は証明報告の明示的な署名表と帰納構造である。

## mainへの反映

- K0905: research/knowledge/items/K0905-two-token-z6-y16-boundary.md
- 証明: research/experiments/vertical-fiber-two-token-z6-y16-boundary-20261117/report.md
- 検証器: research/experiments/vertical-fiber-two-token-z6-y16-boundary-20261117/verify_z6_y16.py
- 監査: research/experiments/vertical-fiber-two-token-z6-y16-boundary-20261117/output/audit.json

K0832本文とknowledge READMEの証明済み境界をy=16へ進め、未解決境界をy≥17へ修正する。Knowledge generated workflowに検証器を追加し、生成ファイルは直接編集しない。

## 未解決

- z=6,y≥17の全Grundy分類
- z≥7の全Grundy分類
- 3族値2位置一般式の全称証明
- 標準二次元共円ゲームの固定幅・q点版の真の安定化長

次の境界候補はz=6,y=17。今回の依存はBにK0903、CにK0873を使え、Aはy=16の帰納仮説に接続できる。個別切片の積み上げだけでなく、3族一般式を直接閉じる方法も引き続き課題である。
