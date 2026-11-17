# 2026-11-17：2トークン残余ゲーム z=6,y=20 切片

## 開始時点の確認

開始時の最新mainは 2341f41c7deaceb2f052f7048e415fbec1b7c4ba（K0912）。AGENTS.md、research/knowledge/README.md、research/knowledge/generated/summary.md、SCHEMA.md、K0832、K0873、K0911、y=19の証明報告・検証器、両knowledge workflowを確認した。K0913は未使用で、z=6,y=20の既存成果も見つからなかった。公開open issueは0件。

AGENTS.mdに従いmainへ直接反映し、branch / PRは作成しない。生成領域は直接編集しない。未解決課題には標準二次元ゲームの固定幅・q点安定化長、4×m・q=8、3×m・q=4/5、s_n・K_n、多人数・高次元、円・直線の整数論などが残る。今回は直前のK0911からA/B/C再帰で閉じられる次の境界y=20を選んだ。

## 発見

\[
H(R;(x,20);6),\quad x\ge20,\ R\ge0
\]
のGrundy値0/1/2を全称分類した。値2位置は基本ラダー{1,3,5}に加え、x=20で43、x=24で45、x=27で{47,49,51,53}、x≥28で47。値1位置もx=20..28の過渡域とx≥29の偶奇別定常域に分けた閉形式を得た。一般tailはR≥x+27で(x+20) mod 2。

A/B/C再帰ではx=20のA/B子が正準化後に同じ(20,19)へ合流する。x≥21ではAにy=20のR強帰納、BにK0911、CにK0873を接続した。K0832のTheorem Tで奇数親の子値を{0,1}へ制限し、偶数親の値を高々1とする。x=20..28の過渡署名、x≥29の偶奇別定常署名を場合分けして1≤R≤x+26を覆い、残りを一般tail定理で閉じた。

値2位置はK0832の3族予想のz=6,y=20特殊化と一致した。家族BのEXTがd=0,4、家族Aのランがd=7、定常位置がd≥8に現れる。ただし一般3族予想全体を証明したわけではない。

## 独立監査

順序付き再帰と降順正準化再帰を独立実装し、K0911とK0873のアンカーも直接照合した。選択肢署名・mex・偶奇上界・値2位置・3族特殊化・tail・固定seed遠方tailを含む合計6,306,363検査で不一致0。検証器を初期状態から2回実行し、両方exit 0・標準出力JSON byte-identical。監査JSON内の sha256_without_hash_field は 978221f057d4d9bcaf3b6f4b85ba9d807a4fbc1420870029c5ea2f573a27e009。

有限監査は全称証明ではない。全称性は署名表、Theorem T、一般tail定理、R強帰納に依る。

## 保存物

- research/knowledge/items/K0913-two-token-z6-y20-boundary.md
- research/experiments/vertical-fiber-two-token-z6-y20-boundary-20261117/report.md
- research/experiments/vertical-fiber-two-token-z6-y20-boundary-20261117/verify_z6_y20.py
- research/experiments/vertical-fiber-two-token-z6-y20-boundary-20261117/output/audit.json
- research/log/2026-11-17-vertical-fiber-two-token-z6-y20-boundary.md

research/knowledge/README.mdとK0832の証明済みスライス一覧・未解決境界をy=20まで更新する。knowledge integrityと生成ビュー更新の既存workflowへ検証器を追加する。生成物はworkflowに任せる。

## 検査境界

検証器は分析環境で2回実行し、両方exit 0・監査JSON byte-identical・不一致0を確認した。GitHub connector経由の反映であり、この環境からrepo checkoutを用意できないため、uv sync --locked、tools/knowledge/check.py、unittest、buildは未実施。GitHub Actionsは反映後に確認する。11×11 rootや長時間探索は起動していない。
