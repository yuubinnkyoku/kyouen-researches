# 2026-11-17：2トークン残余ゲーム z=6,y=19 切片

## 開始時点の確認

開始時の最新mainは 9b195624285a9b74ac8cbeacb2571851ee5c2c97。AGENTS.md、research/knowledge/README.md、research/knowledge/generated/summary.md、SCHEMA.md、K0832、K0873、K0910、y=18の証明報告・検証器を確認した。

AGENTS.mdに従いmainへ直接反映し、branch / PRは作成しない。research/knowledge/generated/ とroot READMEの生成領域は直接編集しない。K0911はmainのファイル検索で未使用だった。

他の優先未解決課題として、標準二次元ゲームの固定幅・q点安定化長、4×m・q=8、3×m・q=4/5、s_n・K_nの未確定値、多人数・高次元の一般化、円・直線の整数論、極大配置とGrundyの一般則が残る。今回はK0910から一段進められ、A/B/C再帰とTheorem Tで全称的に閉じられる次の境界y=19を選んだ。

## 発見

\[
H(R;(x,19);6),\quad x\ge19,\ R\ge0
\]
のGrundy値0/1/2を完全分類した。値2位置は基本ラダー{1,3,5}に加え、x=19で41、x=23で43、x=26で{45,47,49,51}、x≥27で45。値1位置もx=19..27の過渡域とx≥28の偶奇別定常域に分けた閉形式を得た。一般tailはR≥x+26で(x+19) mod 2。

A/B/C再帰ではx=19のA/B子が正準化後に同じ(19,18)へ合流する。x≥20ではAにy=19のR強帰納、BにK0910、CにK0873を接続した。K0832のTheorem Tで奇数親の子値を{0,1}へ制限し、偶数親の値を高々1とする。x=19..27の過渡署名、x≥28の偶奇別定常署名を場合分けして1≤R≤x+25を覆い、残りを一般tail定理で閉じた。

値2位置は3族値2位置予想のz=6,y=19特殊化と一致した。これはこの切片の定理であり、3族予想全体の証明ではない。

## 独立監査

順序付き再帰と降順正準化再帰を独立に実装し、K0910とK0873のアンカーも直接照合した。署名・mex・偶奇上界・3族特殊化・tail・固定seed遠方tailを含む合計6,302,642検査で不一致0。検証器を初期状態から2回実行し、標準出力JSONがバイト単位で一致した。監査JSON内の sha256_without_hash_field は 8201e1b7e47dafc4775694be1843ae95cc70879f2de498bc2d6330b23b6f3797。

有限監査は全称証明ではない。全称性は署名表、Theorem T、一般tail定理、R強帰納に依る。

## 保存物

- research/knowledge/items/K0911-two-token-z6-y19-boundary.md
- research/experiments/vertical-fiber-two-token-z6-y19-boundary-20261117/report.md
- research/experiments/vertical-fiber-two-token-z6-y19-boundary-20261117/verify_z6_y19.py
- research/experiments/vertical-fiber-two-token-z6-y19-boundary-20261117/output/audit.json
- research/log/2026-11-17-vertical-fiber-two-token-z6-y19-boundary.md

research/knowledge/README.mdの証明済み範囲・未解決境界をy=19まで更新する。生成物は既存workflowに任せる。

## 検査境界

検証器を2回実行し、両方exit 0・JSON byte-identical・不一致0を確認した。GitHub connector経由の反映であり、この環境からGitHubを直接cloneできなかったため、repo checkout上の uv sync --locked、knowledge check、unittest、buildは実行できていない。GitHub Actionsの結果も反映後に確認する。11×11 rootや長時間探索は起動していない。
