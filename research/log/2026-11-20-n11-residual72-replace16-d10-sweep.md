# n11 残余72行 代替16根 depth-10 掃引（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-replace16-d10-sweep-single-owner-note.md](2026-11-20-n11-residual72-replace16-d10-sweep-single-owner-note.md)
（commit 7e038004638e68b3ab22bda3e247de21acdc7ea4）の下で、K1088（safe8 pool
REFUTED-16除外後再解決）README「次の一手」第1項を実施した。**行の閉鎖claim・
証明書抽出・receipt fold・8石receipt被覆幾何の設計は行っていない**。記録したのは
runner v17 による depth-10 verdict probe facts のみである。

- 機械: `research/experiments/n11-residual72-replace16-d10-sweep-20261120/scripts/replace16_d10_sweep_20261120.py`
  （stdlibのみ・入力3正本SHA pin・残余49行宇宙のK1085+K1086からの独立再導入込み・全13 gate fail-closed）
- 正本: `research/experiments/n11-residual72-replace16-d10-sweep-20261120/output/replace16-d10-sweep-20261120.json`
  （SHA-256 `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`）
- 生probe記録: `output/probe-records-replace16.jsonl`（32行・assembleの唯一の入力）
- 実験README: 上記実験dir `README.md`（全per-root表・被覆行主張・解釈規約込み）

## プロトコルと入力の信頼境界

K1088正本（SHA-256 `16b38d04…`・全16 gate PASS）から代替16根
（`scope1_refsolve_residual49.greedy_selection`・残余49行をleftover 0で完全被覆する
greedy計画根）を読み出し、runner v17 repo原本固定コピー（git blob `c132cc64…`）で
depth 10・cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false）・
両AND順序の32 probes を実行した。生child hex規約は child = root − 最小セットビット
（簿記のみでverdictに影響しない）。

**残余49行宇宙はK1088からは取らず**、K1085正本の残余72行 base state と K1086正本の
per-root主張被覆から本実験機械内で独立に再導入した: WIN8 7根の主張23行と REFUTED 16根の
主張49行は disjoint・exactly-once・union==72 の分割として再計算され、代替16根の
49対の主張は「行hexは再導入49行のいずれかのD4方位」かつ「行石集合 ⊆ rootのいずれかの
D4像（いずれの向きでも）」・49行ちょうど1回被覆・gains hist {4:3,3:11,2:2}・
16根すべて popcount 8・quadruple-free（4点共円/共線の4×4行列式・Bareiss・整数演算のみ）・
D4 orbit最小hex（min-canonical）で一致した。

## 結果（32/32 probes・capped 0・error 0・順序間矛盾0・全13 gate PASS）

- **WIN8-D10 candidate 3根**（両順序 loss=true・uncapped）
  - `00000000000000801202000000840500`（gained 3・nodes 736,409/878,391）
  - `00000000000000801202000800880200`（gained 3・nodes 618,359/669,067）
  - `00000000000020809002000480100000`（gained 3・nodes 350,792/442,824）
  - 主張被覆行は 3+3+3 = **残余49行のうち9行**（候補であり行の閉鎖ではない）。
- **REFUTED-D10 fact 13根**（両順序 loss=false・uncapped）。主張被覆40行は
  safe8 代替 pool 側で再度代替根を要する（pool P 120,458 − 13根 = 120,445根）。
- nodes総計 **6,339,079**・平均約198K nodes/probe・最大 878,391・terminal石数union [12,18]。
  K1086 greedy23掃引（平均約392K）と同水準で、7石depth-10掃引（sweep39live・平均約2.2M）の
  約1/11。8石rootのblocking密度による構造効果と読めるが、当該16根の観察であり一般化ではない。
- 実行時間: 32 probes を4 workerで約21秒。
- 累計WIN8-D10 candidate簿記: K1086の7根（主張23行）+ 本項3根（主張9行）= **10根・主張32行**
  （すべて候補。証明書抽出・foldまでは行閉鎖に計上しない）。

## 決定性の確認

- probe再実行: WIN 1根（`…80880200` 両順序）と REFUTED 1根（`…01089000` andclose0）の
  再実行で nodes/loss/capped/terminalStoneRange が全て記録と一致。
- assemble は同一cwd複数回＋別cwd別プロセス2回（/tmp・/home/user）で正本JSON
  byte-identical（SHA-256 `808fbda1…`）。

## 解釈規約（再掲）

loss=true（uncapped）は「root位置で手番の側がdepth-10内に必敗」のprobe事実であり、
WIN8-D10 certificate再構築の**対象候補**にすぎない。抽出には別の単一オーナー宣言を要する
（1根抽出の宣言ノートは並走レーンが先行出版済み:
`2026-11-20-n11-residual72-win8-certificate-extract-single-owner-note.md`・commit 4496c888）。
loss=false（uncapped）は REFUTED-D10 fact（depth-10内必勝不存在のprobe事実）であり
LOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. REFUTED-D10 代替13根を除外した pool P′（120,445根）での残余40行 greedy計画再解決
   （WIN8-3根の主張9行を候補被覆として控除した需要構造）。
2. 新WIN8-D10 candidate 3根の残余40行への内在被覆確認（K1088の7根分析と同じ手法。
   余剰があればwindfall供給、無ければ需要構造確定）。
3. 累計10根のWIN8-D10候補の証明書抽出（windfall型extractorの8石拡張・1根単位の
   単一オーナー宣言と独立二重検証）。
