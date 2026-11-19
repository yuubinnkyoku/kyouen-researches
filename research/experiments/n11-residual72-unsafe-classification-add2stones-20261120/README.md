# n11 残余72行 fresh-unsafe 2,871本の構造分類と add-two-stones 拡張census（2026-11-20）

単一オーナー宣言: [research/log/2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md](../../log/2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md)

K1075（候補供給再構築）「次の一手」第2項の実行: 残余72行のadd-one候補のうち
未判定かつunsafeな2,871本（fresh-unsafe）の構造分類と、残余72行への2石追加
（add-two-stones）8石候補宇宙のcensus・コスト見積り。新規掃引・新規判定・
証明書抽出・receipt fold・行の閉鎖は一切行わない。

## ファイル

- `unsafe_classification_add2stones_20261120.py`: 機械（SHA-256 `f5ef884622d64d981aa90b869790db4ef3143b23c5d1dc78d4fb663b65df275e`・stdlibのみ・repoルートから実行・約2分）
- `output/residual72-unsafe-classification-add2stones-20261120.json`: 機械可読正本（39,221 bytes・SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`・全39 checks PASS）

## 入力（すべてSHA-256 pin、fail-closed）

K1075候補供給正本 `49b6f85f…`・resolve6正本 `e85d4bfb…`・resolve5正本
`5a2f4815…`・fold9正本 `24db2352…`・fold10正本 `bed7d331…`・sv17 38gate正本
`c1073bae…`・39 live掃引正本 `22953ae1…`・resolve7正本 `207f4094…`・
sweep43正本 `7940638f…`・sweep39 dead正本 `f8608d0a…`・K0863 scan corpus
（manifest 1,279中1,272 sha verified・post-scan changed 7除外・unresolved raw 10除外）。

## 要約

- 現main corpusのera drift（engine bits 10,261 vs resolve6-era 8,960）を記録し、
  published K1075 stage-1 verbatim一致の代わりにfresh-unsafe pool identity gate
  （部分集合かつcount 2,871一致→集合同一・追加179 judgedは全てfresh-safe側）を課した。
- eroded fresh-safe poolでは行 `0000000000000000380000000a002000` がadd-one
  fresh-safe候補を使い果たしたstranded行（matching 35・greedy 39・witness 36で
  71/72行）。add-one単独の計画では72行の完全被覆は不可能であり、これがadd-twoの動機。
- Stage A: 四つ組3,279個（per-root {1:2,482, 2:370, 3:19}）をcollinear 670・
  axis_rect 189・axis_square 20・other_circle 2,400に分類、外心28 type class
  （half/half 1,774・int/int 340）、support全4、covered row events 2,964、
  全四つ組が追加石を含み、inside_row_image 0、72行全行 quadruple-free。
- Stage B: universe82 380,098根 = safe8 120,474 + unsafe8 259,624
  （7石judgedと交差0）。coverage hist {1:82,602, 2:33,104, 3:4,718, 4:50}、
  per-row demand 1,714〜2,944（zero-demand行0）、39,255根の幾何crosscheck
  mismatch 0、greedy set cover 23根でleftover 0、下界ceil(72/4)=18根。
- Stage C: plan arithmetic add-one 36根→72 probes・add-two greedy 23根→46
  probes・下界18根→36 probes・breakeven Fraction(36,23)。出版3掃引正本の
  node costを7石計測ベースのcaveat付きで引用。

## 解釈

本記録はどの行も閉じない。残余72行は全行openのまま。REFUTED-D10はLOSS証明では
なく、分類・census・greedy/witness listはすべて候補供給の簿記・条件付き計画で
ある。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**正本の interpretation_guard 5文言を参照のこと。

研究ログ: [research/log/2026-11-20-n11-residual72-unsafe-classification-add2stones.md](../../log/2026-11-20-n11-residual72-unsafe-classification-add2stones.md)
