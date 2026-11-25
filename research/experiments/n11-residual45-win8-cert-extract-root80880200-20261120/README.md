# n11 残余45行 WIN8-D10 root `00000000000000801202000800880200` 証明書抽出・三重検証（2026-11-20）

## 目的

K1089（残余72行 replace16 depth-10掃引・正本 SHA-256
`808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`・本実験dir内
`output/.input-k1089.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した根のうち、**fold18/K1122 完了後（残余45行レーン）で抽出未着手・
未宣言候補の中で、出版probe記録（掃引正本pin）を持ち、かつprobe総nodesが最小**の
`00000000000000801202000800880200`（主張被覆3行・probe nodes 618,359/669,067・
probe総nodes 1,287,426・root loser mobility 46）に対して、
完全勝利戦略証明書
（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・
独立検証を行った。

選択にあたっては先行レーンの申立てを訂正した。残余候補3根
（840500・80880200・20809002）は「fresh-probe基盤が必要・出版probe pinなし」と
されていたが、K1089 replace16掃引正本のper_root辞書（キー=root hex・sweep_idx 8）
に本rootの uncapped両AND順序 loss=true [14,18] のprobe記録が存在することを
確認した（残余72行掃引正本はK1093で独立二次検証済み16/16 gates）。この訂正を
単一オーナー宣言ノートに明記した上で、他レーンが抽出宣言済みの
`00000000000000043800000008180010`（8180010）と
`00000000000020809002000480100000`（20809002・commit e75c65b4）を除けば
最安価な本rootの抽出を宣言した。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000800880200-single-owner-note.md`
（commit `de0a505bc8332b748a9f0622f26b1846224bf00b`）の下で実施した。
並走レーンがfold18/K1122でroot `00000000000000801202000000901010`（00901010）の
抽出・foldを出版済みだが、本rootは別根であり、抽出・fold済みの11根
（8003180・8005021・9840004・9090022・8890020・120000038・22081000/K1117・
1009000/K1119・901010/K1120・08d10000/K1121・00901010/K1122）とも独立の
プロセス・機材による抽出である。fold18/K1122（残余48→45）の閉鎖3行は着手前の
機械照合で本rootの主張3行と完全にdisjointであり、主張3行は残余45行
`residual_row_hex_after` 内でopenである。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109/K1113/K1114/K1117/K1119/K1121と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000801202000800880000`（root − 最小セットビット bit 9）+ bit 9 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1089出版値と
  node-exact一致: andclose1 loss=true nodes 618,359・andclose0 loss=true
  nodes 669,067・terminal石数 [14,18]（output/probe-repro-both-orderings.jsonl・
  8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [9,19,23,35,49,57,60,71]・quadruple-free・
  D4正準（8対称像中で最小hexがroot自身・8像すべてdistinct）・root loser mobility 46
  （0,3,4,6,14,17,18,22,26,32,33,42,43,44,50,52,53,54,56,58,63,64,65,72,73,75,76,77,
  84,86,87,88,94,98,102,103,105,106,110,111,112,113,114,116,117,120）を純Python
  整数3×3余因子幾何で再導出（scripts/gen_root_legal_moves.py・
  output/root-legal-moves.txt）。
- **抽出器**: K1121出版 `cert_extractor_win8_root08d10000.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root80880200.ts`（探索核・修復は
  すべて同一bytes。系譜はK1113 `cert_extractor_win8_root8890020.ts`）。各root初手 m を
  extractW(root+m, 9) の盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス46本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全46初手を単一プロセスで一括。
  **3実行とも証明書bytes完全一致**（SHA-256
  `eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致（46/46）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（歴代出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全46初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0・-terminal-range [14,18]の4番目
  CLI引数による厳密一致。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 46 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root80880200.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1121機械のroot定数・
  期待値のみを差し替え（ROOT_HEX・CERT_RELPATH・K1089正本SHA pin〔K1119/K1121と
  同一replace16正本〕・probe nodes 618,359/669,067・bit 9・mobility 46・主張3行・
  実験名・lane表記。gate名は3行版で g19 len(claimed)==3）。K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1089被覆行 == K1097 claimed == intrinsic の三点一致）。

19 gate（g01〜g19）は K1113/K1117/K1119/K1121 と同構成: g01 K1089正本SHA pin・g02/g03
runner v17 git blob c132cc64…の記録と原本一致・g04 root shape safe・g05 mobility 46・
g06 K1089 probes win uncapped・g07 主張3行・g08 probe再現 bit 9 node-exact（4 pilot・
各順序2回）・g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move
node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計（1,670,778 vs
1,383,269）・g14 証明書sorted-unique・末尾改行・行format・g15 B nRows==証明書行・
g16 第三方法全木再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・
g18 解釈guard文言存在・g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000801202000800880200-20261120.n11`
  ・934,278 bytes・25,783戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`。
- **root**: 8石 [9,19,23,35,49,57,60,71]・quadruple-free・D4正準・loser初手は46手。
  K1089 greedy主張被覆3行 `0000000000000000380000000a002000`・
  `00000000000000801202000000800200`・`00000000000000801202000000880000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎46プロセス）総nodes 1,670,778・最大初手
  nodes 193,088（move 98）・fbt_drops 0（全46初手）・fatal/conflict 0。
  Run A2も同一（初手単位 node-exact・rows byte-identical）。
  Run B（単一プロセス・memo温存）総nodes 1,383,269・戦略行25,783で内容不変
  （chunk/単一プロセスのnode会計の乖離はmemo効果のみ）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 57,636（sub-root単位）・winner-to-move 37,121・loser-to-move 11,311・
  loser応手辺 52,219・終端 9,204（全てloser-stuck）・終端石数 [14,18]・
  consumed union == 25,783 == 証明書行25,783（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 46。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1089出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000800880000 \
  --bits 9 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000800880000 \
  --bits 9 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# （各順序2回ずつ計4回・probe-repro-both-orderings.jsonl は 8 records）
# root初手再導出
python3 scripts/gen_root_legal_moves.py
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root80880200.ts \
  --root 00000000000000801202000800880200 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 46 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000801202000800880200 --root-check
#   （--subroots 全46手 で bareiss-stats.txt）
# 検証3: python3 scripts/assemble_win8_audit_root80880200.py --out output/….json
```
