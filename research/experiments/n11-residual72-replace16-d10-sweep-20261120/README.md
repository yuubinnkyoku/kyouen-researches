# n11 残余72行 代替16根 depth-10 掃引（2026-11-20）

## 目的

K1088（safe8 pool の REFUTED-D10 16根除外後の再解決・正本 SHA-256
`16b38d04a486617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724`）
README「次の一手」第1項のとおり、残余49行を完全被覆する greedy 代替16根に対して
runner v17 で depth-10 verdict 掃引を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace16-d10-sweep-single-owner-note.md`
（commit 7e038004638e68b3ab22bda3e247de21acdc7ea4）の下で実施した。

**verdict probe facts のみを記録する**。行の閉鎖claim・receipt fold・証明書抽出・
8石receipt被覆幾何の設計はいずれも本宣言の対象外である。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 対象: K1088正本 `scope1_refsolve_residual49.greedy_selection` の16根
  （各8石・quadruple-free・残余49行をleftover 0で完全被覆するgreedy代替根）。
  両AND順序（andclose 1/0）×depth 10 の **32 probes**・逐次・resume-safe。
- 機械: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）。
- 生child hex規約: child = root − 最小セットビット（簿記のみ。engineはrootの石集合を
  受け取るためverdictは指定に依存しない）。
- 入力3正本はSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・K1088 `16b38d04…`）で
  fail-closed読み出し。
- **残余49行宇宙は K1088 から取らず、K1085正本の残余72行 base state と K1086正本の
  per-root主張被覆から本実験機械内で独立に再導入**し（WIN8 7根の主張23行と REFUTED 16根の
  主張49行の disjoint な exactly-once 分割を再計算）、代替16根の被覆幾何
  （D4方位・部分集合関係・ちょうど1回被覆49行・gains hist {4:3,3:11,2:2}・
  popcount 8・quadruple-free・D4 min-canonical）を整数幾何（4点共円/共線の4×4行列式・
  Bareiss）で再導入してgate化した。

## 結果（32/32 probes 完走・capped 0・error 0・全13 gate PASS・順序間矛盾0）

| root (greedy replacement plan) | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000801202000001089000` | 4 | nodes 60828 loss false | nodes 64674 loss false | REFUTED-D10 fact |
| `00000000100008003800000009001000` | 4 | nodes 99967 loss false | nodes 229351 loss false | REFUTED-D10 fact |
| `00000010000010003800000008003000` | 4 | nodes 40780 loss false | nodes 178392 loss false | REFUTED-D10 fact |
| `00000000000000003800000008b10000` | 3 | nodes 226909 loss false | nodes 257478 loss false | REFUTED-D10 fact |
| `00000000000000003800100028002040` | 3 | nodes 162524 loss false | nodes 288299 loss false | REFUTED-D10 fact |
| `00000000000000043800000609000000` | 3 | nodes 107427 loss false | nodes 239967 loss false | REFUTED-D10 fact |
| `00000000000000103800000009080040` | 3 | nodes 6573 loss false | nodes 174419 loss false | REFUTED-D10 fact |
| `00000000000000801202000000840500` | 3 | nodes 736409 loss true | nodes 878391 loss true | **WIN8-D10 candidate** |
| `00000000000000801202000800880200` | 3 | nodes 618359 loss true | nodes 669067 loss true | **WIN8-D10 candidate** |
| `00000000000000801202020022001000` | 3 | nodes 8905 loss false | nodes 64035 loss false | REFUTED-D10 fact |
| `00000000000000821082000000000848` | 3 | nodes 6582 loss false | nodes 12386 loss false | REFUTED-D10 fact |
| `00000000000000821086800000100000` | 3 | nodes 10493 loss false | nodes 25949 loss false | REFUTED-D10 fact |
| `00000000000020809002000480100000` | 3 | nodes 350792 loss true | nodes 442824 loss true | **WIN8-D10 candidate** |
| `00000000010000809002000040000009` | 2 | nodes 74496 loss false | nodes 28768 loss false | REFUTED-D10 fact |
| `00000010000000801202040000000204` | 3 | nodes 40602 loss false | nodes 144794 loss false | REFUTED-D10 fact |
| `00000010000000809202000080000400` | 2 | nodes 41515 loss false | nodes 47124 loss false | REFUTED-D10 fact |

- **WIN8-D10 candidate: 3根**（両順序 loss=true・uncapped・順序整合。gained はすべて3）。
  主張被覆行は 3+3+3 = **残余49行のうち9行**:
  - `00000000000000801202000000840500` → `…00800100`, `…00800400`, `…00840000`
  - `00000000000000801202000800880200` → `0000000000000000380000000a002000`, `…00800200`, `…00880000`
  - `00000000000020809002000480100000` → `…00000001000`型3行（正本 `classification.win8_d10_candidates.covered_rows` 参照）
- **REFUTED-D10 fact: 13根**（両順序 loss=false・uncapped・順序整合）。
  当該13根の主張被覆40行は safe8 代替 pool 側で再度代替根を要する
  （pool P 120,458 − 13根 = 120,445根が次の再解決pool）。
- nodes総計 **6,339,079**（32 probes・平均約198K nodes/probe・最大probe 878,391 nodes・
  terminal石数union [12,18]）。K1086 greedy23掃引（平均約392K）に続き、8石probeは
  当該 pool でも7石depth-10掃引（平均約2.2M）を大きく下回る（観察で一般化ではない）。
- 実行時間: 32 probes 逐次4 workerで約21秒（本sandbox）。

## 独立再導入と再現性

- 残余49行の再導入: K1085残余72行×K1086 per_root主張から WIN8 23行 + REFUTED 49行の
  disjoint・exactly-once・union==72 分割を本機械が独立に再計算し、代替16根の49対主張は
  すべて「行hexは再導入49行のD4方位」かつ「行石集合 ⊆ rootのいずれかのD4像」・
  49行ちょうど1回被覆・gains hist {4:3,3:11,2:2}で一致（全gate PASS）。
- probe再実行: WIN 1根の両順序と REFUTED 1根の1順序の再実行で
  nodes/loss/capped/terminalStoneRange が記録と完全一致（msは除く）。
- assemble は同一cwd複数回＋別cwd別プロセス2回で正本JSON byte-identical
  （SHA-256 `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`）。
- 再現: `python3 scripts/replace16_d10_sweep_20261120.py run`（resume-safe・完走済みはskip）→
  `… assemble`（gate fail時exit 1）。入力3正本は output/.input-k1085.json・
  .input-k1086.json・.input-k1088.json（SHA-256 pin）または K1085_JSON/K1086_JSON/K1088_JSON 環境変数。

## 解釈規約

1. loss=true（uncapped）は「root位置で手番の側がdepth-10内に必敗する」のprobe事実
   （= 直前の着手を打った側の depth-10内必勝候補）であり、WIN8-D10 certificate
   再構築の対象候補にすぎない。抽出・独立二重検証・8石receipt fold・行閉鎖は別工程。
2. loss=false（uncapped）はREFUTED-D10 fact（depth-10内必勝不存在）であり、
   LOSS証明ではない。代替候補poolの浸食にしかならない。
3. capped/timeout probeは本掃引では発生していない（capped 0・error 0）。
4. nodes数・solved数を勝敗として読まない。
5. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
   残余72行は本掃引では1行も閉じていない。

## 次の一手（着手時は単一オーナー宣言を要する）

- REFUTED-D10となった代替13根をさらに除外した pool P′（120,458 − 13 = 120,445根）での
  greedy計画再解決（残余40行の代替被覆根選定）。 WIN8-3根の主張9行は候補被覆として
  控除した上での需要構造になる。
- 新WIN8-D10 candidate 3根の残余40行への内在被覆（intrinsic coverage）の確認
  （K1088の7根と同様に「主張被覆と同一・余剰なし」なら次回再解決の需要構造は
  主張9行控除で確定する。余剰があればwindfallとして40行側の供給が増える）。
- WIN8-D10 candidate は K1086の7根と合わせて累計10根（主張被覆32行）。
  証明書抽出（windfall型extractorの8石拡張）は別の単一オーナー宣言を要する
  （1根抽出の宣言ノートは並走レーンが先行出版済み:
  `research/log/2026-11-20-n11-residual72-win8-certificate-extract-single-owner-note.md`・commit 4496c888）。
