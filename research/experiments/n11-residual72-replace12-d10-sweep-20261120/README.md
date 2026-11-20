# n11 残余72行 代替12根 depth-10 掃引（2026-11-20）

## 目的

K1094（safe8 pool の REFUTED-D10 41根除外後の残余30行再解決・正本 SHA-256
`e19244904779d906853de603d42c07903e08ab80008aeeb621913669a249baa8`）
README「次の一手」第1項のとおり、残余30行を完全被覆する greedy 代替12根に対して
runner v17 で depth-10 verdict 掃引を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace12-d10-sweep-single-owner-note.md`
（commit 71536f20561f15e98f293bf238b45ad214aa2f2b）の下で実施した。

**verdict probe facts のみを記録する**。行の閉鎖claim・receipt fold・証明書抽出・
8石receipt被覆幾何の設計はいずれも本宣言の対象外である。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 対象: K1094正本 `scope1_refsolve_residual30.greedy_selection` の12根
  （各8石・quadruple-free・残余30行をleftover 0で完全被覆するgreedy代替根）。
  両AND順序（andclose 1/0）×depth 10 の **24 probes**・resume-safe。
- 機械: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）。
- 生child hex規約: child = root − 最小セットビット（簿記のみ。engineはrootの石集合を
  受け取るためverdictは指定に依存しない）。
- 入力5正本はSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`・
  K1091 `edd7ac84…`・K1094 `e1924490…`）で fail-closed読み出し。
- **残余30行宇宙は K1094 から取らず**、K1085正本の残余72行 base state と
  K1086正本のper-root主張被覆から残余49行宇宙を再導入し、K1089正本から残余40行を、
  さらに K1091正本のper-root主張から**残余30行宇宙を独立に再導入**した
  （WIN8-3根の主張10行と REFUTED-12根の主張30行の disjoint exactly-once 分割・
  union==40）。12根の被覆幾何（D4方位・部分集合関係・ちょうど1回被覆30行・
  gains hist {3:8,2:2,1:2}・popcount 8・quadruple-free・D4 min-canonical）を
  整数幾何（4点共円/共線の4×4行列式・Bareiss）で再導入してgate化した
  （K1094帳簿との残余30行一致は独立導入のcrosscheck gateにも保持）。

## 結果（24/24 probes 完走・capped 0・error 0・全18 gate PASS・順序間矛盾0）

| root (greedy replacement plan) | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000083800000048300000` | 3 | nodes 23524 loss false | nodes 87055 loss false | REFUTED-D10 fact |
| `00000000000000103800000209080000` | 3 | nodes 5279 loss false | nodes 159862 loss false | REFUTED-D10 fact |
| `00000000000000801202000000901010` | 3 | nodes 198622 loss true | nodes 240848 loss true | **WIN8-D10 candidate** |
| `00000000000000801202000001004440` | 3 | nodes 80063 loss false | nodes 118586 loss false | REFUTED-D10 fact |
| `00000000000000801202000022081000` | 3 | nodes 126683 loss true | nodes 137565 loss true | **WIN8-D10 candidate** |
| `000000000000008210820000000008c0` | 3 | nodes 27847 loss false | nodes 62182 loss false | REFUTED-D10 fact |
| `00000000000000a21083000000100000` | 3 | nodes 21984 loss false | nodes 66147 loss false | REFUTED-D10 fact |
| `00000000020000809202000800100000` | 3 | nodes 10056 loss false | nodes 25455 loss false | REFUTED-D10 fact |
| `00000000000040809002000040102000` | 2 | nodes 112243 loss false | nodes 120752 loss false | REFUTED-D10 fact |
| `00000000040000801202100100800000` | 2 | nodes 55252 loss false | nodes 74759 loss false | REFUTED-D10 fact |
| `0000000800000000380000000810000a` | 1 | nodes 1226804 loss true | nodes 1416679 loss true | **WIN8-D10 candidate** |
| `00000010000000801202000000000444` | 1 | nodes 255692 loss false | nodes 1046283 loss false | REFUTED-D10 fact |

- **WIN8-D10 candidate: 3根**（両順序 loss=true・uncapped・順序整合。gained 3/3/1）。
  主張被覆行は 3+3+1 = **残余30行のうち7行**:
  - `00000000000000801202000000901010` → `00000000000000003800100008002000`, `00000000000000801202000000101000`, `00000000000000801202000000900000`
  - `00000000000000801202000022081000` → `00000000000000003800000808001000`, `00000000000000801202000000081000`, `00000000000000801202000020001000`
  - `0000000800000000380000000810000a` → `00000008000000003800000008100000`
- **REFUTED-D10 fact: 9根**（両順序 loss=false・uncapped・順序整合）。
  当該9根の主張被覆23行は safe8 代替 pool 側で再度代替根を要する
  （pool P″ 120,433 − 9根 = **120,424根** が第4ラウンド再解決pool）。
- WIN3根の主張7行と REFUTED 9根の主張23行は残余30行の disjoint exactly-once 分割
  （機械gate保証・K1094計画の主張どおり）。
- nodes総計 **5,700,222**（24 probes・平均約238K nodes/probe・最大probe 1,416,679 nodes・
  terminal石数union [12,18]）。
- 実行時間: 24 probes 4 worker 並列で約18秒（本sandbox）。

## 独立再導入と再現性

- 残余30行の再導入: K1085残余72行×K1086 per_root主張から残余49行を再計算し、
  K1089の WIN3/REF13主張から残余40行（=REF13主張）、K1091の WIN3/REF12主張から
  残余30行（=REF12主張）を独立に再計算（win11 claims 10行 + ref12 claims 30行の
  disjoint・exactly-once・union==40）。12根の30対主張はすべて
  「行hexは再導入30行のD4方位」かつ「行石集合 ⊆ rootのいずれかのD4像」・
  30行ちょうど1回被覆・gains hist {3:8,2:2,1:2}で一致（全18 gate PASS）。
- probe再実行: WIN最大根 `0000000800000000380000000810000a` の両順序と
  REFUTED 1根 `00000000000000083800000048300000` の1順序の再実行で
  nodes/loss/capped/terminalStoneRange が記録と完全一致（msは除く）。
- assemble は同一cwd複数回＋別cwd別プロセス1回で正本JSON byte-identical
  （SHA-256 `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`）。
- 再現: `python3 scripts/replace12_d10_sweep_20261120.py run [budget]`（resume-safe）→
  `… assemble`（gate fail時exit 1）。入力5正本は output/.input-k1085.json・
  .input-k1086.json・.input-k1089.json・.input-k1091.json・.input-k1094.json
  （SHA-256 pin）または K1085_JSON/K1086_JSON/K1089_JSON/K1091_JSON/K1094_JSON 環境変数。

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

- REFUTED-D10となった代替9根をさらに除外した pool P‴（120,433 − 9 = 120,424根）での
  greedy計画再解決（残余23行の代替被覆根選定・第4ラウンド）。
- 新WIN8-D10 candidate 3根の残余30行への内在被覆（intrinsic coverage）の確認
  （K1088/K1090/K1094と同様に「主張被覆と同一・余剰なし」なら次回再解決の需要構造は
  主張7行控除で確定する）。
- WIN8-D10 candidate は K1086の7根・K1089の3根・K1091の3根と合わせて累計16根
  （主張被覆49行）。証明書抽出は別の単一オーナー宣言を要する
  （宣言ノート先行出版済み: 1根 `00000000000000043800000008180010`・commit 4496c888・
  1根 `00000000000000003800000008003180`・commit 0360f21a）。
