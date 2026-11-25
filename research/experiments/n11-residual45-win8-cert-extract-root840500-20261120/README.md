# n11 残余45行 WIN8-D10 root `00000000000000801202000000840500` 証明書抽出・三重検証（2026-11-20）

## 目的

K1089（残余72行 replace16 depth-10掃引・正本 SHA-256
`808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`・本実験dir内
`output/.input-k1089.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した根3候補（840500・80880200・20809002・うち20809002は並走がK1123、
80880200は本レーンがK1124として出版済み）のうち、**fold18/K1122 完了後
（残余45行レーン）で抽出未着手・未宣言候補の最後の1根**である
`00000000000000801202000000840500`（主張被覆3行・probe nodes 736,409/878,391・
probe総nodes 1,614,800・root loser mobility 58）に対して、
完全勝利戦略証明書
（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・
独立検証を行った。これでK1089掃引正本per_root辞書に出版probe pinを持つ
残余候補3根の抽出・出版がすべて完了する。

選択の系譜: K1089 replace16掃引正本のper_root辞書（キー=root hex・sweep_idx 8）に
本rootの uncapped両AND順序 loss=true [14,18] のprobe記録が存在することは
K1124実験で確認済みであり（先行レーンの「fresh-probe基盤必要」記載の誤りを
K1124/K1123で訂正済み・残余72行掃引正本はK1093で独立二次検証済み16/16 gates）、
本rootは残余候補3根の中でprobe総nodesが最大（1,614,800 ⁄ 80880200
1,287,426 ⁄ 20809002 793,616）であるが、他2根の出版完了により残った唯一の
未抽出候補である。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801202000000840500-single-owner-note.md`
（commit `1d968ac4`）の下で実施した。抽出・fold済みの11根
（8003180・8005021・9840004・9090022・8890020・120000038・22081000/K1117・
1009000/K1119・901010/K1120・08d10000/K1121・00901010/K1122）およびK1123/K1124
の2根とも独立のプロセス・機材による抽出である。fold18/K1122（残余48→45）の
閉鎖3行は着手前の機械照合で本rootの主張3行と完全にdisjointであり、主張3行は
残余45行 `residual_row_hex_after` 内でopenである。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109/K1113/K1117/K1119/K1121/K1124と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000801202000000840400`（root − 最小セットビット bit 8）+ bit 8 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1089出版値と
  node-exact一致: andclose1 loss=true nodes 736,409・andclose0 loss=true
  nodes 878,391・terminal石数 [14,18]
  （output/probe-repro-both-orderings.jsonl・8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [8,10,18,23,49,57,60,71]・quadruple-free
  （順列展開厳密零判定70組全非零）・D4正準（8対称像distinct）・root loser mobility 58
  （0,1,3,4,12,14,17,19,20,21,22,26,29,31,32,33,35,39,42,43,44,50,51,53,55,56,58,
  61,63,64,65,66,67,72,73,74,75,76,77,79,83,84,85,86,87,88,90,97,99,102,103,110,
  111,112,113,114,116,119）を純Python整数3×3余因子幾何で再導出
  （scripts/gen_root_legal_moves.py・output/root-legal-moves.txt）。
- **抽出器**: K1124出版 `cert_extractor_win8_root80880200.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root840500.ts`（探索核・修復は
  すべて同一bytes・差分はroot hex定数3箇所のみ。系譜はK1113
  `cert_extractor_win8_root8890020.ts`）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス58本（xargs -P 4・1実行1ファイル厳守）、
  Run A2 = A1の完全再実行（同一cwd）、Run B = 全58初手を単一プロセスで一括。
  **3実行とも証明書行集合 byte-identical**（証明書SHA-256
  `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`・
  A1とA2の組立cmp一致・Bのsort -u行集合もcmp一致）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致（58/58）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（歴代出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`・K1124版とcmp一致）:
  root+全58初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過終端石数 [14,18]の4番目CLI引数による厳密一致。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 58 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root840500.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1124機械
  `assemble_win8_audit_root80880200.py` の定数のみを差し替え（ROOT_HEX・
  CERT_RELPATH〔root hex 4箇所〕・probe nodes 736,409/878,391・bit 9→8・
  mobility 46→58〔g05 gate名・root_mobility・subroots_passed・len(bare_stats)・
  loserMobilityの全定数〕・実験名・スクリプト名・出現回数assert・AST検証・
  旧定数残存grep 0で機械確認）。K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1089被覆行 == K1097 claimed == intrinsic の三点一致）。

19 gate（g01〜g19）は K1113/K1117/K1119/K1121/K1124 と同構成: g01 K1089正本SHA pin・
g02/g03 runner v17 git blob c132cc64…の記録と原本一致・g04 root shape safe・
g05 mobility 58・g06 K1089 probes win uncapped・g07 主張3行・g08 probe再現 bit 8
node-exact（4 pilot・各順序2回）・g09 root初手リスト==独立再導出・g10 A1/A2 clean・
g11 A1==A2 per-move node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計
（2,310,103 vs 1,984,636）・g14 証明書sorted-unique・末尾改行・行format・
g15 B nRows==証明書行・g16 第三方法全木再走査PASS・g17 BigInt/Bareiss/python三者の
全集計値一致・g18 解釈guard文言存在・g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行行集合一致）

- **証明書**: `certs/win8-root-00000000000000801202000000840500-20261120.n11`
  ・1,067,425 bytes・29,468戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`。
- **root**: 8石 [8,10,18,23,49,57,60,71]・quadruple-free・D4正準・loser初手は58手。
  K1089 greedy主張被覆3行 `00000000000000801202000000800100`・
  `00000000000000801202000000800400`・`00000000000000801202000000840000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎58プロセス）総nodes 2,310,103・最大初手
  nodes 209,633（move 112）・fbt_drops 0（全58初手）・fatal/conflict 0。
  Run A2も同一（初手単位 node-exact・rows byte-identical）。
  Run B（単一プロセス・memo温存）総nodes 1,984,636・戦略行29,468で内容不変
  （chunk/単一プロセスのnode会計の乖離はmemo効果のみ）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 59,990（sub-root単位・Bareiss per-sub-root seen総計=59,990）・
  winner-to-move 38,458・loser-to-move 11,722・loser応手辺 52,360・
  終端 9,810（全てloser-stuck）・終端石数 [14,18]・consumed union == 29,468 ==
  証明書行29,468（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 58。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1089出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000000840400 \
  --bits 8 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000000840400 \
  --bits 8 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# （各順序2回ずつ計4回・probe-repro-both-orderings.jsonl は 8 records）
# root初手再導出
python3 scripts/gen_root_legal_moves.py
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root840500.ts \
  --root 00000000000000801202000000840500 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 58 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000801202000000840500 --root-check
#   （--subroots 全58手 で bareiss-stats.txt）
# 検証3: python3 scripts/assemble_win8_audit_root840500.py --out output/….json
```
