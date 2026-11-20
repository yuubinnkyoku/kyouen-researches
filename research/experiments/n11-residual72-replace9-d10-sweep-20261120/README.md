# n11 残余72行 代替9根 depth-10 掃引（2026-11-20）

## 目的

K1097（safe8 pool の REFUTED-D10 50根除外後の残余23行再解決・正本 SHA-256
`2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`）
README「次の一手」第1項、および8根被覆判定実験
（`n11-residual23-eight-root-cover-decision-20261120`・greedy 9根計画の
候補根数最小性を P‴ 上で確定済み）の「次の課題」第1項のとおり、
残余23行を完全被覆する greedy 代替9根に対して runner v17 で
depth-10 verdict 掃引を実施した。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md`
（commit `51bbb938809c36eafbf5a762f03bf729c097fe6f`・先行出版）の下で実施した。

**verdict probe facts のみを記録する**。行の閉鎖claim・receipt fold・証明書抽出は
本宣言の対象外。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。

## プロトコル

- 対象: K1097正本 `scope1_refsolve_residual23.greedy_selection` の9根
  （各8石・quadruple-free・残余23行をleftover 0で完全被覆するgreedy代替根・
  gains {3:6, 2:2, 1:1}）。両AND順序（andclose 1/0）×depth 10 の **18 probes**・
  resume-safe。
- 機械: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・取得時にSHA-1一致検査済み）。
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・
  不成立時abort）。生child hex規約: child = root − 最小セットビット
  （簿記のみでverdictに影響しない）。
- 入力6正本をSHA-256 pin（K1085 `5fdd342d…`・K1086 `3045e152…`・
  K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`・
  K1097 `2896deb0…`）でfail-closed読み出し。
- **残余23行宇宙は K1097・K1095正本の結論から取らず**、
  K1085（残余72行）→K1086（残余49行）→K1089（残余40行）→K1091（残余30行）→
  K1095（WIN3根主張7行+REFUTED9根主張23行の disjoint exactly-once・
  union==残余30行）の連鎖で本掃引機械内で独立に再導入した。9根の被覆幾何
  （23行のexactly-once被覆・popcount 8・D4 min-canonical・quadruple-free・
  claims ⊆ D4部分集合・gains hist {3:6,2:2,1:1}）を整数幾何
  （4×4 Bareiss行列式）で再導入してgate化した
  （K1097帳簿（per_row_residual23・scope1==scope2選定）との残余23行一致は
  crosscheck gateにも保持）。

## 結果（18/18 probes 完走・capped 0・error 0・全20 gate PASS・順序間矛盾0）

| root (greedy plan) | gained | andclose1 | andclose0 | verdict |
| --- | --- | --- | --- | --- |
| `00000000000000083800040048100000` | 3 | nodes 11664 loss false | nodes 80912 loss false | REFUTED-D10 fact |
| `00000000000000143800000209000000` | 3 | nodes 572204 loss false | nodes 292251 loss false | REFUTED-D10 fact |
| `00000000000000821082000000001018` | 3 | nodes 53667 loss false | nodes 74966 loss false | REFUTED-D10 fact |
| `00000000000000821086800000000800` | 3 | nodes 42629 loss false | nodes 23112 loss false | REFUTED-D10 fact |
| `00000000000040809002000800100200` | 3 | nodes 120916 loss false | nodes 81137 loss false | REFUTED-D10 fact |
| `00000000010000809002000040002001` | 3 | nodes 608293 loss true | nodes 691784 loss true | **WIN8-D10 candidate** |
| `00000000000000103800000008080041` | 2 | nodes 13781 loss false | nodes 242618 loss false | REFUTED-D10 fact |
| `00000000020000801202000800100001` | 2 | nodes 11535 loss false | nodes 126875 loss false | REFUTED-D10 fact |
| `00000010000000801202000000000448` | 1 | nodes 148782 loss false | nodes 377046 loss false | REFUTED-D10 fact |

- **WIN8-D10 candidate: 1根**（両順序 loss=true・uncapped・順序整合。gained 3）。
  主張被覆行（残余23行のうち3行）:
  - `00000000010000809002000040002001` → `00000000000000801202000001000400`,
    `00000000000000801202000001080000`, `00000000010000809002000040000000`
- **REFUTED-D10 fact: 8根**（両順序 loss=false・uncapped・順序整合）。
  当該8根の主張被覆20行は次ラウンド再解決で代替根を要する。
- WIN 1根の主張3行と REFUTED 8根の主張20行は残余23行の disjoint exactly-once
  分割（機械gate保証・K1097計画の主張どおり）。
- nodes総計 **3,574,172**（18 probes・平均約199K nodes/probe・最大probe 691,784
  nodes・terminal石数union [14,18]）。
- 実行時間: 18 probes 4 worker 並列で約13.3秒（本sandbox）。

## 累計簿記

- WIN8-D10 candidate は累計 **17根**（K1086の7+K1089の3+K1091の3+K1095の3+
  本掃引の1・主張 49+3=52行）。証明書抽出は各根個別の単一オーナー宣言を要する。
- REFUTED-D10 は累計 **58根**（16+13+12+9+本掃引の8）。
  第5ラウンド再解決 pool P⁗ = safe8 120,474 − 58 = **120,416根**。
- 残余23行のうち20行が第5ラウンドの代替被覆対象。行は1行も閉じていない。

## 独立再導入と再現性

- 残余23行の再導入: K1085残余72行×K1086 per_root主張から残余49行を再計算し、
  K1089主張から残余40行、K1091主張から残余30行、K1095主張
  （WIN3根7行+REFUTED9根23行）から残余23行を独立に再計算した
  （すべてdistinct・disjoint・union検査つき）。9根の23対主張はすべて
  「行hexは再導入23行のD4方位」かつ「行石集合 ⊆ rootのいずれかのD4像」・
  23行ちょうど1回被覆・gains hist {3:6,2:2,1:1}・
  K1097 scope1/scope2同一選定と一致（全20 gate PASS）。
- probe再実行: WIN根 `00000000010000809002000040002001` の両順序と
  REFUTED 1根 `00000000000000083800040048100000` の両順序の再実行で
  nodes/loss/capped/terminalStoneRange が記録と完全一致（msは除く）。
- assemble は同一cwd複数回＋別cwd・別HOME 1回で正本JSON byte-identical
  （SHA-256 `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`・
  15,403 bytes）。
- 機械 `scripts/replace9_d10_sweep_20261120.py`
  （SHA-256 `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41`・
  33,969 bytes・stdlib＋Node.js runner・乱数・時刻なし）。
  再現: `python3 scripts/replace9_d10_sweep_20261120.py run [budget] --k1085 …
  --k1097 … [--workers N]`（resume-safe）→
  `python3 scripts/replace9_d10_sweep_20261120.py assemble --k1085 … --k1097 …`
  （gate fail時exit 1）。
- 参照時点のmain: 宣言出版時 `51bbb938809c36eafbf5a762f03bf729c097fe6f`。

## 解釈規約

1. loss=true（uncapped）は「root位置で手番の側がdepth-10内に必敗する」のprobe事実
   （= 直前の着手を打った側の depth-10内必勝候補）であり、WIN8-D10 certificate
   再構築の対象候補にすぎない。抽出・独立二重検証・8石receipt fold・行閉鎖は別工程。
2. loss=false（uncapped）はREFUTED-D10 fact（depth-10内必勝不存在）であり、
   LOSS証明ではない。代替候補poolの浸食にしかならない。
3. capped/timeout probeは本掃引では発生していない（capped 0・error 0）。
4. nodes数・solved数を勝敗として読まない。
5. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
   UNKNOWN のまま。** 残余72行は本掃引では1行も閉じていない。

## 次の一手（着手時は単一オーナー宣言を要する）

- REFUTED-D10 8根を除外した pool P⁗（120,416根）での残余20行のgreedy再解決
  （第5ラウンド）。 stranded行の有無・下界・計画最小性の確認を経て次掃引へ。
- 新WIN8-D10 candidate `00000000010000809002000040002001` の証明書抽出は
  別の単一オーナー宣言を要する（累計17 WIN候補の証明書抽出は既存の宣言・
  並走レーン管轄の抽出手続きに従う）。
- 残るWIN候補の証明書抽出・receipt foldの進捗に応じた需要構造の再計算
  （本掃引のWIN主張3行は残余23行のうちのため、fold後の需要は減る方向にのみ動く）。
