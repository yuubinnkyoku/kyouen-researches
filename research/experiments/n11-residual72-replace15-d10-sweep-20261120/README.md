# n11 残余72行 代替15根 depth-10 掃引（2026-11-20）

## 目的

K1090（safe8 pool の REFUTED-D10 29根除外後の残余40行再解決・正本 SHA-256
`48af6810173060eb769eb52b1fd50ceb81222c07ba7738c8a15832f8c552d3f5`）
README「次の一手」第1項のとおり、残余40行を完全被覆する greedy 代替15根に対して
runner v17 で depth-10 verdict 掃引を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace15-d10-sweep-single-owner-note.md`
（commit f1d78342567b63cef09b471edacddb7ebe9cad67）の下で実施した。

**verdict probe facts のみを記録する**。行の閉鎖claim・receipt fold・証明書抽出・
8石receipt被覆幾何の設計はいずれも本宣言の対象外である。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## プロトコル

- 対象: K1090正本 `scope1_refsolve_residual40.greedy_selection` の15根
  （各8石・quadruple-free・残余40行をleftover 0で完全被覆するgreedy代替根）。
  両AND順序（andclose 1/0）×depth 10 の **30 probes**・resume-safe。
- 機械: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）。
- 生child hex規約: child = root − 最小セットビット（簿記のみ。engineはrootの石集合を
  受け取るためverdictは指定に依存しない）。
- 入力4正本はSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`・
  K1090 `48af6810…`）で fail-closed読み出し。
- **残余40行宇宙は K1090 から取らず**、K1085正本の残余72行 base state と
  K1086正本のper-root主張被覆から残余49行宇宙を再導入し（WIN8 7根の主張23行と
  REFUTED 16根の主張49行の disjoint exactly-once 分割）、さらに K1089正本の
  per-root主張から**残余40行宇宙を独立に再導入**した（WIN8-3根の主張9行と
  REFUTED-13根の主張40行の disjoint exactly-once 分割・union==49）。
  15根の被覆幾何（D4方位・部分集合関係・ちょうど1回被覆40行・
  gains hist {4:2,3:9,2:1,1:3}・popcount 8・quadruple-free・D4 min-canonical）を
  整数幾何（4点共円/共線の4×4行列式・Bareiss）で再導入してgate化した
  （K1090帳簿との残余40行一致は独立導入のcrosscheck gateにも保持）。

## 結果（30/30 probes 完走・capped 0・error 0・全16 gate PASS・順序間矛盾0）

| root (greedy replacement plan) | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000801212000001009000` | 4 | nodes 192365 loss true | nodes 229502 loss true | **WIN8-D10 candidate** |
| `00000000020008003800000009001000` | 4 | nodes 32406 loss false | nodes 73911 loss false | REFUTED-D10 fact |
| `00000000000000003800000008d10000` | 3 | nodes 564695 loss true | nodes 673870 loss true | **WIN8-D10 candidate** |
| `00000000000000043800000008180010` | 3 | nodes 882327 loss true | nodes 1054873 loss true | **WIN8-D10 candidate** |
| `0000000000000010380000000b080000` | 3 | nodes 163509 loss false | nodes 193993 loss false | REFUTED-D10 fact |
| `00000000000000801202000000901002` | 3 | nodes 129142 loss false | nodes 74875 loss false | REFUTED-D10 fact |
| `00000000000000801202000001000448` | 3 | nodes 66127 loss false | nodes 105802 loss false | REFUTED-D10 fact |
| `00000000000000821082000000000890` | 3 | nodes 93857 loss false | nodes 36282 loss false | REFUTED-D10 fact |
| `00000000000000a21083000000001000` | 3 | nodes 31785 loss false | nodes 49100 loss false | REFUTED-D10 fact |
| `00000000000040809002000022100000` | 3 | nodes 68546 loss false | nodes 233735 loss false | REFUTED-D10 fact |
| `00000010000000003840000008080040` | 3 | nodes 57250 loss false | nodes 20290 loss false | REFUTED-D10 fact |
| `00000000000000801202020001005000` | 2 | nodes 87126 loss false | nodes 141870 loss false | REFUTED-D10 fact |
| `00000000010000809002000040000006` | 1 | nodes 14182 loss false | nodes 292326 loss false | REFUTED-D10 fact |
| `00000008000000003800000008100006` | 1 | nodes 196156 loss false | nodes 1065993 loss false | REFUTED-D10 fact |
| `00000010000000801202000000000414` | 1 | nodes 251581 loss false | nodes 305546 loss false | REFUTED-D10 fact |

- **WIN8-D10 candidate: 3根**（両順序 loss=true・uncapped・順序整合。gained 4/3/3）。
  主張被覆行は 4+3+3 = **残余40行のうち10行**:
  - `00000000000000801212000001009000` → `00000000000000003800200008001000`, `00000000000000003800200009000000`, `00000000000000801212000000001000`, `00000000000000801212000001000000`
  - `00000000000000003800000008d10000` → `00000000000000003800000008011000`, `00000000000000003800000008500000`, `00000000000000003800000008900000`
  - `00000000000000043800000008180010` → `00000000000000003800000008002040`, `00000000000000043800000008080000`, `00000000000000043800000008100000`
- **REFUTED-D10 fact: 12根**（両順序 loss=false・uncapped・順序整合）。
  当該12根の主張被覆30行は safe8 代替 pool 側で再度代替根を要する
  （pool P′ 120,445 − 12根 = **120,433根** が第3ラウンド再解決pool）。
- WIN3根の主張10行と REF12根の主張30行は残余40行の disjoint exactly-once 分割
  （機械gate保証・K1090計画の主張どおり）。
- nodes総計 **7,383,022**（30 probes・平均約246K nodes/probe・最大probe 1,054,873 nodes・
  terminal石数union [14,18]）。
- 実行時間: 30 probes 4 worker 逐次実行で約22秒（本sandbox）。

## 独立再導入と再現性

- 残余40行の再導入: K1085残余72行×K1086 per_root主張から残余49行を再計算し、
  さらにK1089の WIN3/REF13主張から残余40行（=REF13主張）を独立に再計算
  （win9 claims 9行 + ref13 claims 40行の disjoint・exactly-once・union==49）。
  15根の40対主張はすべて「行hexは再導入40行のD4方位」かつ
  「行石集合 ⊆ rootのいずれかのD4像」・40行ちょうど1回被覆・
  gains hist {4:2,3:9,2:1,1:3}で一致（全16 gate PASS）。
- probe再実行: WIN最大根 `00000000000000043800000008180010` の両順序と
  REFUTED 1根 `00000000000000801202000001000448` の1順序の再実行で
  nodes/loss/capped/terminalStoneRange が記録と完全一致（msは除く）。
- assemble は同一cwd複数回＋別cwd別プロセス1回で正本JSON byte-identical
  （SHA-256 `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`）。
- 再現: `python3 scripts/replace15_d10_sweep_20261120.py run [budget]`（resume-safe）→
  `… assemble`（gate fail時exit 1）。入力4正本は output/.input-k1085.json・
  .input-k1086.json・.input-k1089.json・.input-k1090.json（SHA-256 pin）または
  K1085_JSON/K1086_JSON/K1089_JSON/K1090_JSON 環境変数。

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

- REFUTED-D10となった代替12根をさらに除外した pool P″（120,445 − 12 = 120,433根）での
  greedy計画再解決（残余30行の代替被覆根選定・第3ラウンド）。
- 新WIN8-D10 candidate 3根の残余30行への内在被覆（intrinsic coverage）の確認
  （K1088/K1090と同様に「主張被覆と同一・余剰なし」なら次回再解決の需要構造は
  主張10行控除で確定する）。
- WIN8-D10 candidate は K1086の7根とK1089の3根と合わせて累計13根（主張被覆42行）。
  証明書抽出（windfall型extractorの8石拡張）は別の単一オーナー宣言を要する
  （1根抽出の宣言ノートは並走レーンが先行出版済み:
  `research/log/2026-11-20-n11-residual72-win8-certificate-extract-single-owner-note.md`・commit 4496c888）。
