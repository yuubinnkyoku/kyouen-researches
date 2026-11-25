# cost63a bit119 WIN7証明書 TSサンドボックス独立検証 (2026-11-14)

## 目的
class2 lane cost63a の bit119-root WIN7証明書 (root=0x00800000000000809102000800000000, 7石 {35,49,56,60,63,71,119}, loser=P2手番, 追加手=119) を、証明書生成コードから独立に再実装したTypeScript検証器で検証した。native実行環境(bash/git)が利用不可のため、run_typescriptサンドボックスによる代替独立検証である。

## 手法 (コンパクト中間アーティフクト経由: Step A/B -> C1 -> C2)
- 生テキスト証明書 (part1of2=514,887B, commit 19261f13ed43e07c40302a0018267ec9e8d1aa5b / part2of2=513,526B, commit 4b2d1fcc44554e86dc0bc896c6ffa1dcd553c421, join md5 c042fbf46be29ecc0ac74ceb25324b16) をStep A/Bでtscompact形式 (LEB128 varint key-delta + 1B move, fnv1a照合) に変換 (part1=14254行/63,555B/fnv1a=ecbc3d9d, commit 2c343c7844 / part2=14255行/77,249B/fnv1a=43f351c2, commit ec3526f96f)。meta行 (rows/first/last/bytes/fnv1a/root/src) と全28,509行のdelta decodeを検証。
- 幾何は3点決定円の行列式係数による共円/共線判定を独立実装 (tm cache)。合法手=occupied+全三重組共円マスク和の補集合。
- DFS検証: 偶数深度(winner手番)は表必須ヒット+strategy move合法性+consumed bit設定、奇数深度(loser手番)は表非存在+全合法手再帰+legal==0ならterminal。depth上限14, POPCAP=150,000/サブroot, seen重複スキップ。
- C1 (サブroot 0-24, 25個): nodes=28,117, terminals=3,727, maxDepth=9, tmComputes=213,200, hits=18,414, failなし。consumed bitmap (3,564B, fnv1a=1fef08be) をmainにpush (commit 4ff6085dcc3bc60da1ef02472f840680d71e2e02)。
- C2 (サブroot 25-48, 24個): nodes=23,656, terminals=3,163, maxDepth=9, hits=15,483, failなし。consumed bitmap (3,564B, fnv1a=d73fddcb) をmainにpush (commit b31000510a92b4db22ebd28bfe9db11f5760554c)。
- C1/C2 bitmapを再fetchしてfnv1a照合のうえOR合算を独立にやり直し、popcount==28,509を確認 (missing=0, extra=0, union fnv1a=dd56f509)。

## 結果
- **verdict: PASS** — 49/49サブrootについて、証明書記載のstrategy treeが幾何・合法手・手番規則のすべての検査に合格し、28,509個のキーがすべて消費された (C1=18,414, C2=15,483, 重複5,388行を含む。union coverage=28,509)。
- root検査: 石構成 {35,49,56,60,63,71,119}・root合法手49・root表外・rootの7石に4共円なし・parent(6石)合法手63 すべて一致。なお旧資料の石構成 [23,26,37,40,53,63,119] はbit番号計算のbyte順序誤りであり、本検証で訂正済み。

## 11x11 status
**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。** 本検証は個別7石rootの深さ10以内WINのみを証明する。sterile/REFUTED-D10はchildのrefutationではない。
