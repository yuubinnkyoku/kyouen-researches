# 2026-11-17：2トークン残余ゲーム z=6,y=21 切片

## 開始時点の確認

開始時のmainは 15187d22c7d65d7a4efa5578c9c40f9e3fa33041（K0913）。AGENTS.md、research/knowledge/README.md、research/knowledge/SCHEMA.md、K0832、K0873、K0913、y=20の証明報告・検証器、knowledge integrityと生成ビュー更新の両workflowを確認した。K0914は未使用で、z=6,y=21の既存証明は見つからなかった。README/K0832が示す未解決境界はz=6,y≥21。branch / PRを作らずmainへ直接反映する方針、generated領域を直接編集しない方針を確認した。

作業中に別レーンのK0909測定コミット 439ad7e3c49f343500a844a65b86dacfdcb0d573 がmainへ入ったため、差分を確認した。変更はn=11測定記録とK0909関連ファイルに限られ、今回の対象とは独立だった。最新mainを再取得し、その上に統合する。

## 選定と発見

直前のK0913からB子を閉じられる次の切片 H(R;(x,21);6) を選んだ。A/B/C再帰では、x=21のA/B子が正準化後に同じ(21,20)状態へ合流する。x≥22ではAに同じy=21切片のR強帰納、BにK0913、CにK0873を接続できる。

値2位置は基本ラダー{1,3,5}に加え、x=21で45、x=25で47、x=28で{49,51,53,55}、x≥29で49。値1位置はx=21..29の過渡域とx≥30の偶奇別定常域に分類した。一般tailはR≥x+28で(x+21) mod 2。

特にx=29を独立境界に残す必要がある。x=29のA子は例外切片x=28を参照し、偶数親の選択肢署名がx≥30の定常署名とは異なる（50..56で{0,2}）。Grundy値1の集合は同じ区間になるが、署名証明ではこの差を落とさない。

K0832のTheorem Tにより奇数親の選択肢値は{0,1}、偶数親の値は高々1。x=21..29の過渡署名表とx≥30の偶奇別定常署名を場合分けし、1≤R≤x+27を覆う。残りは一般tail定理、R=0は終局値で閉じる。したがって全称性は有限標本の外挿ではなく、署名表・tail・R強帰納による。

値2位置はK0832の3族予想のz=6,y=21特殊化と一致する。家族BのEXTがd=0,4、家族Aのランがd=7、定常位置がd≥8に現れる。ただし一般3族予想全体は未証明。

## 独立監査

順序付き再帰と降順正準化再帰を独立実装し、K0913とK0873のアンカーも照合した。選択肢署名・mex・偶奇上界・値2位置・3族特殊化・tail・固定seed遠方tailを含む計6,312,251検査で不一致0。初期状態から2回実行し、両方exit 0・監査JSON byte-identical。監査JSONの sha256_without_hash_field は 8936649273231de493ddfa40bd4d35c9dbc77f76cf3a8ba50b5fe95c7772d3c9。

有限監査は全称証明ではない。全称性の根拠は上記の選択肢署名表、Theorem T、一般tail定理、R強帰納である。

## 保存物

- research/knowledge/items/K0914-two-token-z6-y21-boundary.md
- research/experiments/vertical-fiber-two-token-z6-y21-boundary-20261117/report.md
- research/experiments/vertical-fiber-two-token-z6-y21-boundary-20261117/verify_z6_y21.py
- research/experiments/vertical-fiber-two-token-z6-y21-boundary-20261117/output/audit.json
- research/log/2026-11-17-vertical-fiber-two-token-z6-y21-boundary.md

research/knowledge/README.mdとK0832の証明済み切片一覧・未解決境界をy=21まで更新し、K0913の直近の未解決境界もy≥22へ更新する。knowledge integrityと生成ビュー更新の既存workflowへ検証器を追加する。generated領域は直接編集しない。

## 検査境界

検証器は分析環境で2回実行し、両方exit 0・監査JSON byte-identical・不一致0を確認した。GitHub connector経由の反映であり、この環境にrepo全体のcheckoutはないため、uv sync --locked、tools/knowledge/check.py、unittest、buildは未実施。GitHub Actionsの結果は反映後に確認する。11×11 rootや長時間探索は起動していない。
