# n11 残余29行 WIN8-D10 root `00000000000200003800200008180000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 addtwo-greedy23 depth-10掃引正本・schema
`n11-residual72-addtwo-greedy23-d10-sweep-20261120-v1`・SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`・本実験dir内
`output/.input-k1086.json` にSHA pin・正本内部12 gate全PASS）が、quadruple-freeな
23本のgreedy根で残余72行をちょうど1回ずつ被覆し、両AND順序46 probe
（pilot_d6制御必須・cap 30M・timeout 280s）でdepth-10判定した per_root辞書の
なかで、両AND順序 uncapped で WIN8-D10 candidate として確定した根のひとつ
`00000000000200003800200008180000`（主張被覆2行・probe nodes 261,294/288,448・
probe総nodes 549,742・root loser mobility 42）に対して、完全勝利戦略証明書
（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・
独立検証を行った。

選択の系譜: 本rootの抽出は残余72行時代の旧宣言（commit `4496c888`）が未完のまま
残っていたため、fold23（K1133・残余32→29行・出版正本 SHA-256 `04f334ff…`）完了後の
残余29行レーンで、単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000200003800200008180000-single-owner-note.md`
（commit `6fb426ba37`）により旧宣言を更新（supersede）して着手した。着手前機械
確認として、主張2行 `00000000000000003800200008100000`・
`00000000000000a09002000080000000` が fold23正本の残余29行 `residual_row_hex_after`
内でopenであること、K1097 refsolve win16 footprint（intrinsic == claimed == 2行）と
一致すること、本rootの28正準部分幾何で残余29内openは主張2行のみ（余剰なし）で
あることを確認済み。残余29レーンの残存候補は本rootを含む3根で、候補A
（root `00000000000000043800000008180010`）は並走がK1136として出版済み、
残る1根（root `0000000800000000380000000810000a`）は未着手である。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論は別工程であり、本実験では確定しない。
本実験はS6行を1つも閉じない。主張2行のreceipt fold（fold24候補Aの主張3行とは
不交差）は別の単一オーナー宣言を要する別機材の未着手領域である。
REFUTED-D10 は LOSS 証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109/K1113/K1117/K1119/K1121/K1124/K1136と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000200003800200008100000`（root − 最小セットビット bit 19）+ bit 19 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1086出版値と
  node-exact一致: andclose1 loss=true nodes 261,294・andclose0 loss=true
  nodes 288,448・terminal石数 [14,18]
  （output/probe-repro-both-orderings.jsonl・8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [19,20,27,45,59,60,61,81]・quadruple-free・
  D4正準・root loser mobility 42
  （1,2,3,5,6,8,10,16,22,29,33,38,42,43,44,66,68,69,71,76,78,85,86,88,92,98,101,
  102,103,104,105,106,107,108,109,111,112,113,114,116,117,120）を純Python整数
  3×3余因子幾何で再導出
  （scripts/gen_root_legal_moves.py・output/root-legal-moves.txt）。
- **抽出器**: K1124出版 `cert_extractor_win8_root80880200.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root00000000000200003800200008180000.ts`
  （探索核・修復はすべて同一bytes・差分はroot hex定数3箇所とfilename guard 2箇所・
  ヘッダー文言のみ。差し替えは出現回数assertつきで実施しsmoke test PASS）。
  各root初手 m を extractW(root+m, 9) の盲抽出・自己検査付き。fbtOR 修復込みで
  fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス42本（xargs -P 4・1実行1ファイル厳守）、
  Run A2 = A1の完全再実行（同一cwd）、Run B = 全42初手を単一プロセスで一括。
  **3実行とも証明書行集合 byte-identical**（証明書SHA-256
  `7bd64a47bed13c25fe069b0b3563c06081639cd3d2ad09b28a1e6c65a41fa61d`・
  A1とA2の組立cmp一致・Bのsort -u行集合もcmp一致）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致（42/42）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（歴代出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全42初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過終端石数 [14,18]のCLI引数による厳密一致。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 42 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械
  `scripts/assemble_win8_audit_root00000000000200003800200008180000.py`
  （Python stdlibのみ・engine importなし・第三実装として独自に全木を再走査）。
  K1124出版機 `assemble_win8_audit_root80880200.py` のroot定数差し替え版で、
  変換は出現回数assertつきジェネレータで実施（ROOT_HEX・CERT_RELPATH〔root hex
  4箇所〕・K1089→K1086・sweep SHA `3045e152…`・probe nodes 261,294/288,448・
  bit 9→19・mobility 46→42〔g05 gate名・root_mobility・subroots_passed・
  len(bare_stats)・loserMobility〕・主張3行→2行〔g07〕・実験名・スクリプト名。
  構文検査・AST検証・旧定数残存grep 0で機械確認）。
  g19は本レーン向けに拡張し、K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint照合
  （K1086被覆行 == K1097 claimed == intrinsic の三点一致）に加えて、fold23出版正本
  （SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`・
  `output/.input-fold23.json` にpin）の残余29行内で主張2行がopenであることを
  検証し、`pinned_inputs` にfold23_record_sha256を追加した。

19 gate（g01〜g19）は K1113/K1117/K1119/K1121/K1124/K1136 と同構成:
g01 K1086正本SHA pin・g02/g03 runner v17 git blob c132cc64…の記録と原本一致・
g04 root shape safe・g05 mobility 42・g06 K1086 probes win uncapped・
g07 主張2行・g08 probe再現 bit 19 node-exact（4 pilot・各順序2回）・
g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move node-exact・
g12 B clean・g13 chunk vs 単一プロセスのnode会計（1,399,389 vs 1,057,553）・
g14 証明書sorted-unique・末尾改行・行format・g15 B nRows==証明書行・
g16 第三方法全木再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・
g18 解釈guard文言存在・g19 K1097 footprint三点一致+fold23残余29行内open。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行行集合一致）

- **証明書**: `certs/win8-root-00000000000200003800200008180000-20261120.n11`
  ・706,180 bytes・19,525戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `7bd64a47bed13c25fe069b0b3563c06081639cd3d2ad09b28a1e6c65a41fa61d`。
- **root**: 8石 [19,20,27,45,59,60,61,81]・quadruple-free・D4正準・loser初手は42手。
  K1086 greedy主張被覆2行 `00000000000000003800200008100000`・
  `00000000000000a09002000080000000` はK1097 win16 footprint（intrinsic == claimed）
  とも一致し、fold23残余29行内でopen（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎42プロセス）総nodes 1,399,389・最大初手
  nodes 196,428（move 10）・fbt_drops 0（全42初手）・fatal/conflict 0。
  Run A2も同一（初手単位 node-exact・rows byte-identical）。
  Run B（単一プロセス・memo温存）総nodes 1,057,553・戦略行19,525で内容不変
  （chunk/単一プロセスのnode会計の乖離はmemo効果のみ）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 43,649・winner-to-move 28,170・loser-to-move 8,556・loser応手辺 39,665・
  終端 6,923（全てloser-stuck）・終端石数 [14,18]・consumed union == 19,525 ==
  証明書行19,525（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 42（sub-root 42/42）。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （5,654 bytes・SHA-256
  `dafa177bf74fd528c34e9a858a83345df4cf8138c17f33ca0102c28840f28c04`・
  19/19 gate PASS・同一cwd 2回＋別cwd・別EXPERIMENT_ROOT・別プロセス1回で
  audit JSON byte-identical・時刻・乱数入力なし）。
- **chain上の位置（fold23時点の出版簿計）**: 5親112行target 83/112・残余29行・
  frontier 6,126行/485,438・solved S6 1,722・incidence 11,666。本抽出はこれらの
  簿記を一切変更しない。

## 再現

```
# probe再現（pilot込み・K1086出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000200003800200008100000 \
  --bits 19 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000200003800200008100000 \
  --bits 19 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# （各順序2回ずつ計4回・probe-repro-both-orderings.jsonl は 8 records）
# root初手再導出
python3 scripts/gen_root_legal_moves.py
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root00000000000200003800200008180000.ts \
  --root 00000000000200003800200008180000 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 42 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000200003800200008180000 --root-check
#   （--subroots 全42手 で bareiss-stats.txt）
# 検証3: python3 scripts/assemble_win8_audit_root00000000000200003800200008180000.py \
#   --out output/win8-cert-extract-verification-20261120.json
```
