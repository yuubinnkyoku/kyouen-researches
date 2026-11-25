# 2026-11-20 n11 残余72行36-root三手先D4 frontier censusの独立第二検証

## 着手判断

最新mainのAGENTS.md、research/knowledge/README.md、11×11関連のknowledge・experiments・logを確認した。K1075の36-root witnessを使った三手先censusは既に出版済みだが、元実装はJavaScript BigIntの余因子展開・Leibniz展開であり、別言語・別の厳密判定式による全件第二検証はまだ見当たらなかった。

36-root depth-10 sweepは単一オーナー宣言済みの別レーンであり、同一probeの再実行・重複出版はしない。そこで、探索を起動せず、公開済みの36-root幾何censusだけを独立再導出した。

## 入力と実行

- K1075候補供給正本 SHA-256: `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`
- 先行census正本 SHA-256: `94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023`
- 監査時main HEAD: `da4b167811aec6d2405d5222759a6086e435ac1e`

Proxmox CT204（Debian 13・Python 3.13.5）で逐次実行。実装はPython標準ライブラリのみで、元JavaScriptはimportしていない。放物面持ち上げ点の外積・内積による整数判定を使い、16,007,211回の点判定と132,291個の三点組を再計算した。最大RSSは約152 MiB。

## 結果

**19/19 gate PASS。** K1075から36 rootを読み、全rootの7石・D4正準形・安全性を再検査し、D4像×単石除去から残余72行への所属を独立再導出した。さらに全合法な1・2・3手を列挙し、全per-root表・全221 pairwise overlap・4 worker集計まで先行census正本と完全一致した。

主要値は9石56,597、raw 10石733,855、root別D4 membership 733,800、全体D4類728,370、root間重複membership 5,430（0.739984%）、pairwise overlap 5,435、うちworker境界をまたぐもの4,193（77.148114%）。

2回の別プロセス・別作業ディレクトリで正本JSONはbyte-identical。SHA-256は `a6272056df6aa1dc348a00e1961a95223b4642a230a7da95a04b857bd9118b83`。

## 判断と限界

三手先の幾何重複が0.74%と小さい一方、重複の77.15%がworker境界をまたぐという既存判断は独立実装でも再現した。ただし、これは探索表の実命中率ではない。同じD4類でも探索深さ・境界・証明情報が異なり得るため、共有表の大規模化や分割変更は引き続き保留する。

36-root depth-10 sweepの結果は本監査の対象外。探索probe・新しいverdict・証明書・receipt・frontier閉鎖は発生していない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。


## リポジトリ検査と関連メタデータ修正

- `uv sync --locked` は成功。
- sparse checkoutに関連する3つの実験入力ディレクトリを追加し、リポジトリ内の配置で独立検証器を再実行。19/19 gate PASS、出力SHA-256 `a6272056df6aa1dc348a00e1961a95223b4642a230a7da95a04b857bd9118b83` が別cwd実行と一致。
- K1084のfront matterと4つのartifact pathを個別検査してPASS。新規ファイルの `git diff --check` もPASS。
- K1084のrelation先K1075が既存front matterのYAML構文エラーで読み込めなかったため、K1075のコロンを含むaliasを引用符で囲み、topicを既存語彙の `residual-games/search-methods/statistics` に修正、artifact role `note` を許可語彙の `log` に修正した。K1075が依存するK1063にも同種の未引用コロンがあったため、該当noteとコロンを含むaliasを引用符で囲んだ。主張・数値・判定は変更していない。
- リポジトリ全体のknowledge check/buildは成功扱いにしない。全体サイズは約3.2 GBでCT204の空き容量内に完全checkoutできず、sparse checkoutでは既存artifact欠落が大量に報告される。unit testは31件中30件通過・1件エラーで、既存20項目にaliases欠落があるためMigrationBoundaryTestsがKeyErrorになった。K1084自身のaliasesとartifact pathは個別PASS。既存の別項目のYAML/語彙エラーはこの変更では修正していない。
- root READMEとknowledge/generatedの再生成は、全artifactを含まないsparse checkoutでは信頼できる差分を作れないため未実施。GitHub status APIでも当該commitにstatus/workflow runは返らず、CI成功とは扱わない。


- 追加の絞り込み検査ではK1084とK1075にエラーは出なかった。K1063の残存指摘は、旧項目K1057/K1059のfront matter未整備と、このsparse checkoutに未展開の既存artifactに限られる。
