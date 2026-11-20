# n11 残余72行 safe8 pool の REFUTED-D10 16根除外後再解決の単一オーナー宣言（2026-11-20）

本レーンは K1086（残余72行 add-two greedy 23根 depth-10掃引・正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）
README「次の一手」第2項である **REFUTED-D10 16根を除外した safe8 pool での残余49行
greedy計画再解決** について単一オーナーとして着手する。
並走レーンは本宣言項目に着手しないこと。

## 範囲（やること）

- 入力は2つの出版正本のみを SHA-256 pin で fail-closed 読み出す:
  K1085 census 正本（SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`
  = `research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json`）
  と K1086 掃引正本（上記）。
- Stage B universe82（72行×空き2石 generation witness 471,960 events → canon dedup
  380,098根・safe8 120,474・unsafe8 259,624）と coverage/demand を本実験機械内で
  K1085実験と独立に再導入し、出版集計（coverage hist・per-row demand min/max/sum・
  greedy 23根の完全再現含む）と照合する。
- K1086 verdict による除外: 16 REFUTED-D10 根を safe8 pool から除外し、
  残余49行（greedy計画上16根が主張被覆していた行）について
  (a) 除外後 pool での per-row demand・zero-demand（stranded）行の有無、
  (b) lex-smallest-max-gain greedy 再解決（被覆根数・gains hist・leftover）、
  (c) 情報論的下界 ceil(49/4)=13 に対する超過、
  (d) 最大マッチング・witness（blossom port）,
  (e) 下位的測定: WIN8-D10 candidate 7根の内在被覆（intrinsic coverage）が
      残余49行に及ぶか（WIN receipt fold 将来時の追加閉鎖可能性の幾何学的事実）
  を計算する。
- 決定性: stdlib のみ・逐次・2回実行 + 別cwd別プロセス1回で正本JSON byte-identical。

## やらないこと

- いかなる行も閉じない。証明書抽出・receipt fold・新規probe・掃引は行わない。
- greedy/witness の結果は条件付き計画（候補根の簿記）であり証明書ではない。
- REFUTED-D10 は LOSS 証明ではない。nodes数・solved数を勝敗として読まない。

## 解釈規約

本計算は depth-10 verdict で REFUTED と判定済みの16根を候補供給から除外した上での
計画再解決の簿記である。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
