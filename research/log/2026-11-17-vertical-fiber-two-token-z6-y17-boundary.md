# 2026-11-17 高速レーン: 2トークン残余ゲーム z=6,y=17切片の全称証明

## 作業前の確認

作業開始時の最新mainは 3d091a2a3cf9c18ce6300ca01cf1cba1dba3f83f。root AGENTS.md、research/knowledge/README.md、K0832、K0873、K0905と現行の未解決一覧を確認した。AGENTS.mdはrootの1件だけで、下位ディレクトリに追加規約はない。K0908とy=17実験ディレクトリは未使用だった。

READMEではz=6,y=1..16の切片が証明済み、y≥17が未解決。K0832の本文・artifact一覧にはy=9以降の反映漏れがあったため、今回y=9..17を追記し、証明済み境界をy=17へ更新する。knowledge integrity workflowもy=10で止まっていたため、y=11..17の検証器を登録する。

## 選定と発見

次の境界y=17を選んだ。再帰は

\[
A=H(R-1;(x-1,17);6),\quad
B=H(R-1;(x,16);6),\quad
C=1\oplus H(R-1;(x,17);5).
\]

x=17ではA/Bの子が正準化後に同じ(17,16)状態へ合流する。x≥18ではAは同じ切片のR強帰納、BはK0905、CはK0873に帰着する。

値2位置は基本ラダー{1,3,5}に加え、x=17で37、x=21で39、x=24で41,43,45,47、x≥25で41。値1位置も過渡域x=17..25と定常域x≥26の閉形式を得た。tailはR≥x+24で(x+17) mod 2。

3族値2位置予想のz=6,y=17特殊化と一致する。ただし今回の証明範囲は固定切片だけで、3族予想全体は未証明。

## 証明と独立監査の区別

全称性はA/B/C署名表、K0832のTheorem T、一般tail定理とR強帰納による。検証器は順序付き再帰と降順正準化再帰を別実装し、z=6,y=17、z=6,y=16、z=5,y=17の公式アンカー19,104件を照合した。さらに署名2,046,496件、mex2,046,496件、奇数親上界1,023,744件、偶数親上界1,022,752件、値2位置1,984件、3族特殊化1,984件、tail128,960件、固定seed遠方tail2,000件を検査し、不一致0。監査JSONは独立実行二回でバイト単位に一致した。

有限監査を全称証明とは扱わない。全称性の根拠は証明報告の明示的な署名表と帰納構造である。

## mainへの反映

- K0908: research/knowledge/items/K0908-two-token-z6-y17-boundary.md
- 証明: research/experiments/vertical-fiber-two-token-z6-y17-boundary-20261117/report.md
- 検証器: research/experiments/vertical-fiber-two-token-z6-y17-boundary-20261117/verify_z6_y17.py
- 監査: research/experiments/vertical-fiber-two-token-z6-y17-boundary-20261117/output/audit.json

K0832本文とknowledge READMEの証明済み境界をy=17へ進め、未解決境界をy≥18へ変更する。Knowledge integrity workflowへy=11..17の検証器を登録し、生成ビュー更新workflowも起動する。生成ファイルは直接編集しない。

## 未解決

- z=6,y≥18の全Grundy分類
- z≥7の全Grundy分類
- 3族値2位置一般式の全称証明
- 標準二次元共円ゲームの固定幅・q点版の真の安定化長

次の境界候補はz=6,y=18。今回の依存はBにK0905、CにK0873を使え、Aはy=17の帰納仮説に接続できる。個別切片の積み上げだけでなく、3族一般式を直接閉じる方法も引き続き課題である。
