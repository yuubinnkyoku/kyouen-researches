# n11 残余72行 代替15根 depth-10 掃引（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-replace15-d10-sweep-single-owner-note.md](2026-11-20-n11-residual72-replace15-d10-sweep-single-owner-note.md)
（commit f1d78342567b63cef09b471edacddb7ebe9cad67）の下で、K1090
（safe8 pool の REFUTED-D10 29根除外後の残余40行再解決）README「次の一手」第1項
を完走した。verdict probe facts のみを記録し、行の閉鎖claim・receipt fold・
証明書抽出は行っていない。

- 機械: `research/experiments/n11-residual72-replace15-d10-sweep-20261120/scripts/replace15_d10_sweep_20261120.py`
  （stdlibのみ・入力4正本SHA pin・残余49/40行宇宙の独立再導入・resume-safe・
  全16 gate fail-closed）・runner v17 repo原本固定コピー（git blob `c132cc64…`）
- 正本: `research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json`
  （SHA-256 `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`）
- 逐次記録: 同 `output/probe-records-replace15.jsonl`（30 probes）

## プロトコル

入力4正本（K1085 census `5fdd342d…`・K1086掃引 `3045e152…`・K1089掃引 `808fbda1…`・
K1090再解決 `48af6810…`）をSHA-256 pinでfail-closed読み出し。残余49行宇宙は
K1085残余72行とK1086 per-root主張から、残余40行宇宙はK1089のWIN8-3根主張9行と
REFUTED-13根主張40行のdisjoint exactly-once分割（union==49）から独立に再導入。
K1090掃引対象の15根（scope1 greedy_selection・gains hist {4:2,3:9,2:1,1:3}）の
被覆幾何（40対主張・D4方位・部分集合関係・popcount 8・quadruple-free・
D4 min-canonical）をBareiss 4x4行列式の整数幾何で再導入しgate化した
（K1090帳簿の残40行との一致はcrosscheck gate）。probeは両AND順序（andclose 1/0）・
depth 10・cap 30M・timeout 280s・pilot_d6制御（nodes 3,402・loss=false）。
生child hex規約: child = root − 最小セットビット（簿記のみ・verdict非依存）。

## 結果（30/30 probes完走・capped 0・error 0・全16 gate PASS・順序矛盾0）

1. **WIN8-D10 candidate 3根**（両順序uncapped loss=true・gained 4/3/3・主張被覆10行）:
   - `00000000000000801212000001009000`（nodes 192,365/229,502・greedy第1根）
   - `00000000000000003800000008d10000`（564,695/673,870）
   - `00000000000000043800000008180010`（882,327/1,054,873・最大probe）
2. **REFUTED-D10 fact 12根**（両順序uncapped loss=false・主張被覆30行）。
   K1090掃引対象の残り12根すべて。
3. WIN3主張10行+REF12主張30行は残余40行のdisjoint exactly-once分割（機械gate保証）。
4. nodes総計7,383,022（平均約246K/probe・terminal石数union [14,18]）。
   実行時間30 probes約22秒（4 worker・本sandbox）。
5. 全体計画は **13 WIN候補根（K1086の7根=23行+K1089の3根=9行+K1091の3根=10行・
   主張42行）+ 第3ラウンド代替根（残余30行）** に更新（候補根の簿記であり
   証明書ではない）。第3ラウンド再解決poolは P″ = 120,445 − 12 = **120,433根**。

決定性: probe再実行（WIN最大根 `43800000008180010` の両順序 + REFUTED 1根
`80120200001000448` の1順序）がnode-exact一致。assembleは同一cwd複数回+別cwd別プロセス
1回の計3回で正本JSON byte-identical（SHA-256 `edd7ac84…`）。stdlibのみ・乱数・時刻なし。

## 解釈規約（再掲）

loss=true（uncapped）はroot位置で手番側がdepth-10内に必敗するprobe事実であり
証明書ではない（抽出は別宣言、1根抽出の宣言ノートは並走レーンが先行出版済み:
commit 4496c888）。REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として
読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。本掃引は行を1つも閉じない: 残余72行は全行open。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. pool P″（120,433根）での残余30行 greedy計画再解決（第3ラウンド・新しい
   単一オーナー宣言ノートを先行出版してから実施）。
2. 新WIN8-D10 candidate 3根の残余30行への内在被覆（intrinsic coverage）確認
   （再解決機械で計算する。主張と同一・余剰なしなら需要構造は主張10行控除で確定）。
3. 累計13根のWIN8-D10候補の証明書抽出（1根単位の宣言と独立二重検証）。
