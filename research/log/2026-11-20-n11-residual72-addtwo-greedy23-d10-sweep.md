# n11 残余72行 add-two greedy 23根 depth-10 掃引（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-addtwo-greedy23-d10-sweep-single-owner-note.md](2026-11-20-n11-residual72-addtwo-greedy23-d10-sweep-single-owner-note.md)
（commit b943a20875）の下で、K1085（残余72行 fresh-unsafe 2,871本の構造分類・add-two-stones
拡張census）README「次の一手」第1項を実施した。**行の閉鎖claim・証明書抽出・receipt fold・
8石receipt被覆幾何の設計は行っていない**。記録したのは runner v17 による depth-10 verdict
probe facts のみである。

- 機械: `research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/scripts/addtwo_greedy23_d10_sweep_20261120.py`
  （stdlibのみ・greedy計画幾何の独立再導入込み・全11 gate fail-closed）
- 正本: `research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json`
  （SHA-256 `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）
- 生probe記録: `output/probe-records-add2greedy23.jsonl`（46行・assembleの唯一の入力）
- 実験README: 上記実験dir `README.md`（全per-root表・被覆行主張・解釈規約込み）

## プロトコルと入力の信頼境界

K1085正本（SHA-256 `5fdd342d…`・全39 gate PASSの出版済みcensus）から greedy set cover
23根を読み出し、runner v17 repo原本固定コピー（git blob `c132cc64…`）で depth 10・
cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false）・両AND順序の
46 probes を実行した。生child hex規約は child = root − 最小セットビット（簿記のみで
verdictに影響しない）。本実験機械は greedy計画幾何（72対の被覆関係のD4方位・部分集合関係・
ちょうど1回被覆・gains hist {4:7,3:13,2:2,1:1}・23根と72行のquadruple-free）を
K1085実験とは独立に整数幾何（4点共円/共線の4×4行列式・Bareiss）で再導入してgate化し、
すべて一致した。

## 結果（46/46 probes・capped 0・error 0・順序間矛盾0・全11 gate PASS）

- **WIN8-D10 candidate 7根**（両順序 loss=true・uncapped）
  - `00000000000000003800000008003180`（gained 4・nodes 903,977/1,146,417）
  - `00000000000000003800000008005021`（gained 3・619,138/751,581）
  - `00000000000000003800000009840004`（gained 3・1,143,198/1,528,656）
  - `00000000000000909002200080100000`（gained 4・512,590/614,246）
  - `00000000010000889002000080100000`（gained 4・409,407/575,570）
  - `00000000012000003800080009000000`（gained 3・657,152/825,127）
  - `00000000000200003800200008180000`（gained 2・261,294/288,448）
  - greedy計画上の主張被覆行は 4+4+4+3+3+3+2 = **残余72行のうち23行**（候補であり行の閉鎖ではない）。
- **REFUTED-D10 fact 16根**（両順序 loss=false・uncapped）。greedy計画の16根分の被覆行
  （残余72行のうち49行）は add-two 候補 pool 側で代替根を要する。
- nodes総計 **18,032,471**・平均約392K nodes/probe・最大 1,528,656・terminal石数union [12,18]。
  同protocolの7石depth-10掃引（sweep39live・78 probes・169,615,508 nodes・平均約2.2M）と比較して
  **当該23根では8石probeは約1/5.7の節点費用**。rootでの石数増によるblocking初期密度の構造効果と
  読めるが、23根の観察であり一般化ではない。
- 逐次実行で全46 probes約49秒（2コアsandbox）。

## 決定性の確認

- probe再実行: WIN2本（`…03180` 両順序・`…81000000` andclose0）とREFUTED1本
  （`…0040c` andclose0）の再実行で nodes/loss/capped/terminalStoneRange が全て記録と一致。
- assemble は同一cwd2回＋別cwd別プロセス1回で正本JSON byte-identical
  （SHA-256 `3045e152…`）。

## 解釈規約（再掲）

loss=true（uncapped）は「root位置で手番の側がdepth-10内に必敗」のprobe事実であり、
WIN8-D10 certificate再構築の**対象候補**にすぎない。8石receiptの被覆幾何（7石の
「8 D4像−1石」に対応する「8 D4像×2石除去」join）と fold 意味論は本掃引では確定しておらず、
証明書抽出には別の単一オーナー宣言を要する。loss=false（uncapped）は REFUTED-D10 fact
（depth-10内必勝不存在のprobe事実）であり LOSS 証明ではない。nodes数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. WIN8-D10 candidate 7根の証明書抽出（windfall型extractorの8石拡張）・独立二重検証
   （BigInt 3x3/4x4 Bareiss等・第三方法）・8石receipt被覆幾何の設計。
2. REFUTED-D10 16根を除外した safe8 pool（120,474根）での greedy計画再解決
   （残余49行の代替被覆根選定・下界18根は不変）。
3. 見つかったWIN8候補の被覆23行のうち、7石候補（add-one fresh-safe witness）でも
   供給される行との重複構造の整理（collateral計画最適化）。
