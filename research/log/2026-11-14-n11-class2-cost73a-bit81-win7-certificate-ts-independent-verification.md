# cost73a bit81 WIN7証明書 TSサンドボックス独立検証 (2026-11-14)

## 目的
class2 lane cost73a の bit81-root WIN7証明書 (root=0x00000000000200809082000000000010, 7石 {4,49,55,60,63,71,81}, loser=P2手番, 追加手=81) を、証明書生成コードから独立に再実装したTypeScript検証器で検証した。native実行環境が利用不可のため、run_typescriptサンドボックスによる代替独立検証である。

## 手法
- 証明書アーティファクト (keys-delta-v2 part1/part2, commit f3d16630f63e39cfdc86d593de0287d4369f7b64) を取得し、meta行 (rows/first/last/bytes/fnv1a/root/cert_commit) とLEB128 varint delta decodeを全行検証。part1=18632行/99651B/fnv1a=2f4f4d53、part2=18677行/116380B/fnv1a=4edef148、計37309行。
- 幾何は4x4行列式 (det4) による共円/共線判定を独立実装。合法手=全三重組共円マスク和の補集合。
- DFS検証: 偶数深度(winner手番)はkeys表ヒット+strategy move合法性を必須検査、奇数深度(loser手番)はkeys表非存在+全合法手再帰。512 pop毎+サブroot毎に合法手全再計算でoptsを照合。
- C1 (サブroot 0-24): pops=31950, even visits=20816, terminals=4871, maxDepth=9, failなし。consumed bitmap (bits=20816) をmainにpush (commit de9234970db6271e4a5328388b582d62460c8b96)。
- C2 (サブroot 25-50): pops=36043, even visits=23677, terminals=5120, maxDepth=9, failなし。C1 bitmapをfnv1a検証後にOR合算。
- 合計 consumed popcount = 37309 = 期待値37309。missing=0, extra=0。

## 結果
- **verdict: PASS** — 51/51サブrootについて、証明書記載のstrategy treeが幾何・合法手・手番規則のすべての検査に合格し、37309個のキーがすべて消費された。
- root検査: parent再構成(parent|BIT[81]==root)・両局面safe(共円4点なし)・parent合法手73・root合法手51 すべて一致。

## 11x11 status
**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。** 本検証は個別7石rootの深さ10以内WINのみを証明する。sterile/REFUTED-D10はchildのrefutationではない。
