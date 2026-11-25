# n11 残余72行 代替12根 depth-10 掃引（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-replace12-d10-sweep-single-owner-note.md](2026-11-20-n11-residual72-replace12-d10-sweep-single-owner-note.md)
（commit 71536f20561f15e98f293bf238b45ad214aa2f2b）の下で、K1094
（safe8 pool REFUTED-D10 41根除外後の残余30行再解決）README「次の一手」第1項の
**代替12根 depth-10 verdict 掃引**を実施した。**行の閉鎖claim・receipt fold・
証明書抽出は行っていない**。

- 機械: `research/experiments/n11-residual72-replace12-d10-sweep-20261120/scripts/replace12_d10_sweep_20261120.py`
  （runner v17 repo原本固定コピー・入力5正本SHA pin・残49/40/30行宇宙の独立再導入・
  被覆幾何D4+Bareiss再導入・pilot_d6制御・全18 gate fail-closed・resume-safe）
- 正本: `research/experiments/n11-residual72-replace12-d10-sweep-20261120/output/replace12-d10-sweep-20261120.json`
  （SHA-256 `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`）
- 生記録: 同 output/probe-records-replace12.jsonl（24 probes・pilot_d6制御つき）

## 結果（24/24 probes 完走・capped 0・error 0・全18 gate PASS・順序間矛盾0）

1. **WIN8-D10 candidate 3根**（両順序 loss=true・uncapped）:
   `00000000000000801202000000901010`（nodes 198,622/240,848・主張3行）・
   `00000000000000801202000022081000`（nodes 126,683/137,565・主張3行）・
   `0000000800000000380000000810000a`（nodes 1,226,804/1,416,679・主張1行）。
   主張被覆は残余30行のうち**7行**。
2. **REFUTED-D10 fact 9根**（両順序 loss=false・uncapped・主張被覆23行）。
   除外集合はREFUTED-D10累計41+9 = **50根**となり、第4ラウンド再解決poolは
   P‴ = 120,474 − 50 = **120,424根**（再解決行は残余23行）。
3. nodes総計 **5,700,222**（24 probes・平均約238K/probe・最大1,416,679・
   terminal石数union [12,18]）。完走までの所要は約18秒（4 worker）。
4. WIN8-D10候補は累計**16根**（K1086の7根+K1089の3根+K1091の3根+本掃引3根）・
   主張被覆**49行**（72行の簿記上の過半。ただしすべて候補であり行閉鎖ではない）。

## 独立再導入と再現性

- 残余30行宇宙はK1094正本から取らず、K1085+K1086（残49行）+K1089（残40行）+
  K1091（残30行: win3b主張10行+ref12主張30行のdisjoint exactly-once・union==40）から
  独立再導入。12根の30対主張・ちょうど1回被覆・gains hist {3:8,2:2,1:2}・
  popcount 8・quadruple-free・D4 min-canonicalを整数幾何（4点共円/共線の4×4行列式・
  Bareiss）で再導入し全18 gate PASS（K1094帳簿の残30行一致はcrosscheck gate）。
- probe再実行: WIN最大根 `0000000800000000380000000810000a` の両順序と
  REFUTED 1根 `00000000000000083800000048300000` の1順序でnodes/loss/capped/
  terminalStoneRangeが記録と完全一致（node-exact）。
- assembleは同一cwd複数回＋別cwd別プロセス1回で正本JSON byte-identical
  （SHA-256 `335eca5e…`）。

## 解釈規約（再掲）

loss=true（uncapped）はWIN8-D10 certificate再構築の対象候補にすぎない。
REFUTED-D10は「当該rootの当該sideのdepth-10内必勝不存在」のprobe事実であり
LOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。本掃引は行を1つも閉じない: 残余72行は全行open。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. REFUTED 9根をさらに除外した pool P‴（120,424根）での残余23行greedy再解決
   （第4ラウンド・K1090/K1094機械の継承）。
2. 新WIN8-D10 candidate 3根の残余30行への内在被覆（intrinsic coverage）確認
   （K1094のwin13検証と同じくper-root主張一致・余剰有無を機械gate化）。
3. 累計16根のWIN8-D10候補の証明書抽出（1根単位の単一オーナー宣言と独立二重検証。
   宣言ノート先行出版済み2根: commit 4496c888・0360f21a）。
