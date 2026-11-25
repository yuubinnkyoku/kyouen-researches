# n11 残余23行 代替9根 depth-10掃引 全件再実行による独立第二検証（2026-11-20）

## 目的

K1146（残余23行の代替9根depth-10掃引・掃引正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eefbf7f912cccc88ded1e`）の
18 probes（9根×両AND順序）のうち出版時に再実行されたのは4件のspot-check
のみだった。K1144が上流4掃引（K1086/K1089/K1091/K1095・132 probes）に対して
確立した「全probe再実行による第二検証」の replace9 版として、
単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-reexec-second-verification-single-owner-note.md`
（commit `3f340466218bb47a08d1f7421947ff720bc52b85`・先行出版）の下で実施した。

**出版probe事実の再実行照合のみを行う**。行の閉鎖claim・receipt fold・
証明書抽出は対象外。REFUTED-D10 は LOSS 証明ではない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。

## プロトコル

- runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・取得時にSHA-1一致検査済み）。
  depth 10・cap 30,000,000・timeout 280s・両AND順序・pilot_d6制御必須
  （nodes 3,402・loss=false・不成立時abort）。
- 入力はSHA-256 pinでfail-closed読み出し: K1085 `5fdd342d…`・
  K1086 `3045e152…`・K1089 `808fbda1…`・K1091 `edd7ac84…`・
  K1095 `335eca5e…`・K1097 `2896deb0…`・K1146掃引正本 `e8f5d674…`・
  K1146 probe-records JSONL `bdacf0e7…`（出版コミット `e9ea153bc4` の
  ファイルから計算）・掃引機械 `d163b2a1…`。
- pass A（本tree）と pass B（隔離cwd・別HOME・入力複写の別tree）で
  18 probe全件を再実行し、nodes/loss/capped/terminalStoneRange の
  決定性字段を出版記録と全件照合（ms/wall は照合から除外）。
- 残余23行宇宙はK1097・K1095正本の結論から取らず、K1085→K1086→K1089→
  K1091→K1095の連鎖を本検証機内で独立に再導入（D4正準形表は本検証のための
  独立実装・4×4 Bareiss行列式）。9根の被覆幾何（23行exactly-once・
  D4方位・quadruple-free・D4 min-canonical・gains hist {3:6,2:2,1:1}・
  child=root−最小セットビット）を再導入してgate化。
- 出版掃引機械 `replace9_d10_sweep_20261120.py` を隔離treeでpristine再実行
  （assemble・出版probe-records入力）し、20 gate PASS・出力が出版正本と
  byte-identical であることを確認した（本検証READMEとは別工程・監査JSONの
  `pristine-reassemble-volume-byte-identical` gateで固定）。

## 結果（24/24 gate PASS・3実行byte-identical）

- **pristine再assemble**: 20/20 gate PASS・出力SHA-256 `e8f5d674…`が
  出版正本とbyte-identical（出版機械・出版記録・6入力正本の整合を隔離環境で
  全再検証）。
- **pass A（本tree・18 probes・実行約13.0秒）**: 18/18 probeで
  nodes/loss/capped/terminalStoneRange が出版記録と全件一致
  （nodes総計 3,574,172 == 出版値）。fresh再分類で WIN8-D10 candidateは
  `00000000010000809002000040002001` ただ1根（両順序 uncapped loss=true・
  nodes 608,293/691,784）・REFUTED-D10 8根・順序間矛盾0・
  pilot_d6制御全件PASS。
- **pass B（隔離cwd/HOME・入力複写・18 probes・実行約12.7秒）**: pass Aと
  同一の決定性字段が18/18で成立（passA vs passB 探針間不一致0）。
- 残余23行の連鎖再導入（72→49→40→30→23・各段distinct/disjoint/union検査つき）
  とK1097帳簿crosscheck（per_row_residual23一致・scope1==scope2同一選定）PASS。
  9根の23行exactly-once被覆・claims ⊆ D4像・gains {3:6,2:2,1:1} PASS。
- 監査正本 `output/replace9-sweep-reexec-second-verification-20261120.json`
  （SHA-256 `27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072`）
  は同一cwd2回+別cwd別HOME 1回の3実行でbyte-identical。

## 意味

- K1146のprobe事実（WIN8-D10 candidate 1根・REFUTED-D10 8根・nodes総計・
  分類）は、出版機械から独立の環境・独立の再実装による全件再実行で
  再現された。第5ラウンドの前提（pool P⁗ 120,416根・残余20行の代替被覆）
  の入力側はこれで二重固定された。
- 本検証で行は1行も閉じない。WIN候補の証明書抽出receipt foldは別工程・
  別宣言のまま。

## 検証機械

- `scripts/verify_replace9_reexec_20261120.py`
  （SHA-256 `77cdd9e3…`・41,175 bytes・stdlib＋Node.js runner・乱数・時刻なし）。
- 再現: pass Aは `python3 scripts/verify_replace9_reexec_20261120.py run 240
  --pass A --workers 4 --k1085 … --k1097 … --records … --volume …`、
  pass Bは機械一式と入力を複写した隔離treeで `--pass B`、
  assembleは `python3 scripts/verify_replace9_reexec_20261120.py assemble
  --pass-a DIR --pass-b DIR --pristine PRISTINE_OUTPUT --k1085 … --k1097 …
  --records … --volume …`（gate fail時exit 1）。
- 入力の所在（repo相対）: K1085は
  `n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json`、
  K1086/K1089/K1091/K1095は各掃引実験dir `output/`の各正本JSON、
  K1097は `n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json`、
  records/volumeは `n11-residual72-replace9-d10-sweep-20261120/output/`。
  すべてSHA-256 pinでfail-closed読み出しするため取得元は問わない。
- 参照時点のmain: 宣言出版時 `3f340466218bb47a08d1f7421947ff720bc52b85`。

## 解釈規約

1. loss=true（uncapped）はdepth-10内必敗のprobe事実の再現であり、
   証明書抽出・行閉鎖の資格を本検証は与えない。
2. loss=false（uncapped）はREFUTED-D10 probe事実の再現であり、LOSS証明ではない。
3. 本検証はcapped/timeout/errorを出していない（全36探針完走）。
4. nodes数・solved数を勝敗として読まない。
5. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
   すべてUNKNOWNのまま。** 残余23行は全行open。

## 次の一手（着手時は単一オーナー宣言を要する）

- 第5ラウンドrefsolve計画簿記（宣言 `ace38772d9` 所有）の到着後に、
  残余20行greedy・下界・最小性をpool P⁗（120,416根）上で再解決する。
- 新WIN8-D10 candidate `00000000010000809002000040002001` の証明書抽出
  （宣言 `63877ffd2e` 所有）出版後のreceipt fold。
- fold26（root `0000000800000000380000000810000a`）は先行レーン宣言
  （`e53cc60c87`・2026-11-20T11:28:44Z）のままで本レーンは着手しない。
