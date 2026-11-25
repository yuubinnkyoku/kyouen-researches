# n11 残余72行 add-two greedy 23根 depth-10 掃引（2026-11-20）

## 目的

K1085（残余72行 fresh-unsafe 2,871本の構造分類・add-two-stones拡張census、
正本 SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`）
README「次の一手」第1項のとおり、add-two 8石候補の greedy set cover 23根に対して
runner v17 で depth-10 verdict 掃引を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-addtwo-greedy23-d10-sweep-single-owner-note.md`
（commit b943a20875）の下で実施した。

**verdict probe facts のみを記録する**。行の閉鎖claim・receipt fold・証明書抽出・
8石receipt被覆幾何の設計はいずれも本宣言の対象外である。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 対象: K1085正本 `add_two_stones_census.greedy_roots` の23根（各8石・quadruple-free・
  greedy set cover で残余72行を leftover 0 で完全被覆する計画根）。両AND順序
  （andclose 1/0）×depth 10 の **46 probes**、逐次・resume-safe。
- 機械: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）。
- 生child hex規約: child = root − 最小セットビット（簿記のみ。engineはrootの石集合を
  受け取るためverdictは指定に依存しない）。
- K1085正本はSHA-256 pin（`5fdd342d…`）でfail-closed読み出し。
- greedy計画幾何（72対の被覆関係・D4方位・完全1回被覆・gains hist・quadruple-free）は
  本実験機械内で K1085実験とは独立に整数幾何（4点共円/共線の4×4行列式）で再導入しgate化。

## 結果（46/46 probes 完走・capped 0・error 0・全11 gate PASS・順序間矛盾0）

*表の nodes は両順序ともcap内で決定的（機種非依存の費用単位）。terminal石数のunionは [12,18]。*

| root (greedy plan) | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000003800000008003180` | 4 | nodes 903977 loss true | nodes 1146417 loss true | WIN8-D10 candidate |
| `00000000000000003800000008005021` | 3 | nodes 619138 loss true | nodes 751581 loss true | WIN8-D10 candidate |
| `00000000000000003800000008710000` | 3 | nodes 101112 loss false | nodes 249156 loss false | REFUTED-D10 fact |
| `00000000000000003800000009840004` | 3 | nodes 1143198 loss true | nodes 1528656 loss true | WIN8-D10 candidate |
| `0000000000000000380010000a002010` | 3 | nodes 106359 loss false | nodes 131523 loss false | REFUTED-D10 fact |
| `00000000000000043800020008900000` | 3 | nodes 1064515 loss false | nodes 1325001 loss false | REFUTED-D10 fact |
| `00000000000000083820000048100000` | 4 | nodes 35114 loss false | nodes 234480 loss false | REFUTED-D10 fact |
| `00000000000000143800000009080000` | 4 | nodes 409899 loss false | nodes 509436 loss false | REFUTED-D10 fact |
| `00000000000000801202000000840300` | 3 | nodes 112275 loss false | nodes 302769 loss false | REFUTED-D10 fact |
| `00000000000000801202000001004408` | 3 | nodes 22084 loss false | nodes 53828 loss false | REFUTED-D10 fact |
| `00000000000000801202040000901000` | 4 | nodes 132665 loss false | nodes 177229 loss false | REFUTED-D10 fact |
| `00000000000000801212000001081000` | 4 | nodes 50558 loss false | nodes 80786 loss false | REFUTED-D10 fact |
| `00000000000000821082000000000818` | 3 | nodes 72484 loss false | nodes 130387 loss false | REFUTED-D10 fact |
| `00000000000000821086800000001000` | 3 | nodes 21818 loss false | nodes 94416 loss false | REFUTED-D10 fact |
| `00000000000000841202000000880400` | 3 | nodes 186038 loss false | nodes 286992 loss false | REFUTED-D10 fact |
| `00000000000000909002200080100000` | 4 | nodes 512590 loss true | nodes 614246 loss true | WIN8-D10 candidate |
| `00000000000040809002000802100000` | 3 | nodes 64906 loss false | nodes 180515 loss false | REFUTED-D10 fact |
| `00000000000200003800200008180000` | 2 | nodes 261294 loss true | nodes 288448 loss true | WIN8-D10 candidate |
| `00000000010000889002000080100000` | 4 | nodes 409407 loss true | nodes 575570 loss true | WIN8-D10 candidate |
| `00000000012000003800080009000000` | 3 | nodes 657152 loss true | nodes 825127 loss true | WIN8-D10 candidate |
| `00000000020000801202080800100000` | 3 | nodes 25660 loss false | nodes 64060 loss false | REFUTED-D10 fact |
| `0000001000000080120200000000040c` | 1 | nodes 63084 loss false | nodes 77795 loss false | REFUTED-D10 fact |
| `00000010040000801202000100000200` | 2 | nodes 249995 loss false | nodes 1178731 loss false | REFUTED-D10 fact |

- **WIN8-D10 candidate: 7根**（両順序 loss=true・uncapped・順序整合）。greedy計画上の
  主張被覆行は 4+4+4+3+3+3+2 = **23行**（残余72行のうち）。証明書再構築の対象候補であり、
  8石receiptの被覆/Fold意味論は本掃引では確定していない（抽出には別の単一オーナー宣言を要する）。
- **REFUTED-D10 fact: 16根**（両順序 loss=false・uncapped・順序整合）。当該8石rootの
  depth-10内必勝不存在のprobe事実であり、それ以前の局面のLOSS証明ではない。
  greedy計画の16根分の被覆行（残余72行のうち49行）は add-two 候補 pool 側で代替根を要する。
- nodes総計 **18,032,471**（46 probes・平均約392K nodes/probe・最大probe 1,528,656 nodes）。
  参照: add-one 7石depth-10掃引は sweep39live 78 probes 169,615,508 nodes（平均約2.2M）。
  **8石probeは当該計画では7石probeの約1/5.7の節点費用**（石が多くrootでの
  blocking初期密度が高い構造効果。当該23根の観察であり一般化ではない）。
- 実行時間: 46 probes 逐次で約49秒（本pub sandbox・2コア）。

## 独立再導入と再現性

- greedy計画幾何の再導入: claimed 72対すべて「行hexは残余72行のD4方位である」
  かつ「行集合 ⊆ rootのいずれかのD4像」、「各残余行はちょうど1根で被覆」、
  gains hist {4:7, 3:13, 2:2, 1:1}、23根と72行すべて quadruple-free。すべてPASS。
- probe再実行: WIN2本（両順序計3 probe）とREFUTED1本（1 probe）の再実行で
  nodes/loss/capped/terminalStoneRange が記録と完全一致（msは除く）。
- assembleは別cwd別プロセスを含む再実行で出力JSON byte-identical
  （SHA-256 `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）。
- 再現: `python3 scripts/addtwo_greedy23_d10_sweep_20261120.py run` （resume-safe・
  完走済み(root,ordering)はskip）→ `… assemble`（gate fail時exit 1）。

## 解釈規約

1. loss=true（uncapped）は「root位置で手番の側がdepth-10内に必敗する」のprobe事実
   （= 直前の着手を打った側の depth-10内必勝候補）であり、WIN8-D10 certificate
   再構築の対象候補にすぎない。抽出・独立二重検証・8石receipt fold・行閉鎖は別工程。
2. loss=false（uncapped）はREFUTED-D10 fact（depth-10内必勝不存在）であり、
   LOSS証明ではない。候補poolの浸食にしかならない。
3. capped/timeout probeは本掃引では発生していない（capped 0・error 0）。
4. nodes数・solved数を勝敗として読まない。
5. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 次の一手（着手時は単一オーナー宣言を要する）

- WIN8-D10 candidate 7根の証明書抽出（windfall型extractorの8石拡張）と
  8石receiptの被覆幾何（「8 D4像×2石除去」join）の設計・独立二重検証。
- REFUTED-D10となった16根を除外した safe8 pool での greedy計画再解決
  （49行の代替被覆根の選定）。
