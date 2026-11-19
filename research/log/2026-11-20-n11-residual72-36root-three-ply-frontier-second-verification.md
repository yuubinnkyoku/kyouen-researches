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
