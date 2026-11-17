# 2026-11-17：2トークン残余ゲーム z=6,y=18 切片

## 開始時点の確認

開始時の最新mainは 7d4d2b31e4884f35bcb3db5274efed6541228178（cost73lの幾何・D4監査を記録したコミット）。rootのAGENTS.md、research/knowledge/README.md、SCHEMA.md、VOCABULARY.yaml、K0832、K0873、K0905、K0908とy=17の証明報告・検証器を確認した。

AGENTS.mdに従いmainへ直接反映する。branch / PRは作成しない。generatedとroot READMEの生成領域は直接編集しない。新規K番号は検索でK0909が未使用と確認した。

開始時点の残る近接課題は、z=6,y≥18の全Grundy切片、z≥7の全Grundy切片、3族値2位置予想の全称証明。別の優先課題として、標準二次元ゲームの固定幅q点安定化長、4×m・q=8、3×m・q=4/5、s_n・K_nの未確定値、多人数・高次元の一般化が残る。今回は直前のy=17証明を使って、こちらだけで閉じられる次の切片y=18を選んだ。

## 発見

全x≥18,R≥0で H(R;(x,18);6) のGrundy値0/1/2を分類した。値2位置は基本ラダー{1,3,5}に加え、x=18で39、x=22で41、x=25で{43,45,47,49}、x≥26で43。値1位置も過渡域と定常域に分けた閉形式を得た。tailはR≥x+25で(x+18) mod 2。

A/B/C再帰ではx=18のA/B子が正準化後に同じ(18,17)へ合流する。x≥19ではAにy=18のR強帰納、BにK0908、CにK0873を接続する。K0832のTheorem Tで奇数親の子値を{0,1}へ制限し、偶数親の値を高々1とする。x=18..25の過渡署名、x=26の境界署名、x≥27の偶奇別定常署名を場合分けして全Rを覆った。

値2位置はK0832の3族予想のz=6,y=18特殊化と一致する。これはこの切片の定理であり、3族予想全体の証明ではない。

## 独立監査

順序付き再帰と降順正準化再帰を独立に実装し、K0908とK0873のアンカーも直接照合した。署名・mex・偶奇上界・値2位置・tail・固定seed遠方tailを含む合計6,299,078検査で不一致0。検証器を初期状態から2回実行し、監査JSONがバイト単位で一致した（sha256_without_hash_field: 49daa84031130d99a4d6ad02aded0e18e1e3f6930dbdb287df2f105631d0775a）。

有限監査は全称証明ではない。全称性は署名表、Theorem T、一般tail定理、R強帰納に依る。

## 保存物

- research/knowledge/items/K0909-two-token-z6-y18-boundary.md
- research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/report.md
- research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/verify_z6_y18.py
- research/experiments/vertical-fiber-two-token-z6-y18-boundary-20261117/output/audit.json
- research/log/2026-11-17-vertical-fiber-two-token-z6-y18-boundary.md

K0832とknowledge READMEの証明済み範囲・未解決境界をy=18まで更新する。生成物は既存workflowに任せる。

## 検査境界

この実行ではGitHub connector経由でmainを読み書きしており、repo checkout上のuv sync、knowledge check、unittest、buildは実行していない。GitHub Actionsの結果も反映後に別途確認する。11×11 rootや長時間探索は起動していない。
