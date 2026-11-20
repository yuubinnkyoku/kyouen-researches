# n11 残余68行 WIN8-D10 root `00000000000000003800000008005021` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`・本実験dir内
`output/.input-k1086.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した7根のうち、**greedy計画順2位 `00000000000000003800000008005021`
（主張被覆3行）** に対して、完全勝利戦略証明書（n11-terminal-strategy-v1
original_first_WIN8 second_to_move_LOSS）の盲抽出・独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-win8-cert-extract-root8005021-single-owner-note.md`
（commit 7ffddc66）の下で実施した。並走レーンが宣言済みの root
`00000000000200003800200008180000`（commit 4496c888）・`…0810000a`
とは別根であり、K1096（root `…8003180`・fold11/K1105でfold済み）とも独立の
プロセス・機材による抽出である（複数root抽出の独立導出の体）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000003800000008005020`（root − 最小セットビット）+ bit 0 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1086出版値と
  node-exact一致: andclose1 loss=true nodes 619,138・andclose0 loss=true
  nodes 751,581・terminal石数 [14,18]（output/probe-repro-both-orderings.jsonl）。
- **root初手の独立再導出**: 8石・quadruple-free・root loser mobility 41を
  純Python整数4×4行列式で再導出（output/root-legal-moves.txt）。
- **抽出器**: K1096出版 `cert_extractor_win8_root8003180.ts` を
  root引数・filename guardのみ差し替えた `scripts/cert_extractor_win8_root8005021.ts`
  （探索核・修復はすべて同一bytes）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス41本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全41初手を単一プロセスで一括（別cwd）。
  **3実行とも証明書bytes完全一致**（SHA-256 `69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致。B（単一プロセス・memo温存）は
  A1の総nodes 3,272,039に対し2,876,091で Strategy行26,083は不変
  （抽出のnode費用はmemo状態依存・戦略は非依存の再実証）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（K1096出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全41初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 41 sub-root全走査・consumed union。
  (3) 監査機械 `scripts/assemble_win8_audit_root8005021.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1096機械の
  root定数・期待値のみを差し替え（g05 mobility 41・g07 主張3行・g08 bit 0・
  probe nodes差し替え）、K1097 refsolve正本（SHA-256 `2896deb0…`・
  `output/.input-k1097.json` にpin）の win16 footprint照合を
  **g19として追加**（K1086 greedy被覆行 == K1097 claimed == intrinsic の三点一致）。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000003800000008005021-20261120.n11`
  ・945,298 bytes・26,083戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5`。
- **root**: 8石 [0,5,12,14,27,59,60,61]・quadruple-free・loser初手は41手。
  K1086 greedy主張被覆3行 `…8001001`・`…8001020`・`…8005000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎41プロセス）総nodes 3,272,039・最大初手
  nodes 293,361・fbt_drops 0（全41初手）・fatal/conflict 0。
  Run B総nodes 2,876,091・戦略行26,083で内容不変。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 59,594（sub-root単位）・winner-to-move 38,442・loser-to-move 10,961・
  loser応手辺 53,352・終端 10,191（全てloser-stuck）・終端石数 [14,18]・
  consumed union 26,083 == 証明書行26,083（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 41。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `0bd2dd10c1d5b735a04f31425003c635d80266e4c03a6bef0fdff212d499408f`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回でaudit JSON byte-identical・
  時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1086出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000003800000008005020 \
  --bits 0 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000003800000008005020 \
  --bits 0 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root8005021.ts \
  --root 00000000000000003800000008005021 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 41 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000003800000008005021 --root-check
# 検証3: python3 scripts/assemble_win8_audit_root8005021.py --out output/….json
```
