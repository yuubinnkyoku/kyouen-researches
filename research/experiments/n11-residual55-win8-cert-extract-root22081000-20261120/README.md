# n11 残余55行 WIN8-D10 root `00000000000000801202000022081000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1095（残余72行 代替12根 depth-10掃引・正本 SHA-256
`335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`・本実験dir内
`output/.input-k1095.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した根のうち、**fold15/K1115 完了後（残余55行レーン）で抽出未着手・
未宣言候補の中で最安価**の
`00000000000000801202000022081000`（主張被覆3行・probe nodes 126,683/137,565・
root loser mobility 39 = 歴代抽出根最小）に対して、完全勝利戦略証明書
（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・
独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root801202200022081000-single-owner-note.md`
（commit `22eb87dfaf19bd1518c195976d33b16319d8cf49`）の下で実施した。
並走レーンが抽出宣言済みの root `00000000000200003800200008180000`（commit 4496c888）・
`0000000800000000380000000810000a` とは別根であり、抽出・fold済みの6根
（8003180・8005021・9840004・9090022・8890020・120000038）とも独立のプロセス・
機材による抽出である。着手時は並走がroot `…8890020`のfold16（receipt fold）を
宣言済み（着手中）であったが、本抽出の実行中にfold16はK1116として出版された
（コミット `cc12a2bfbe`・23番目receipt・閉鎖5行 = 主張4行+target外余剰1行）。
本rootの主張3行はfold16の閉鎖5行と着手前に機械的にdisjointであることを独立計算
済みであり、fold16の成否・残余55→51の移動に依存せず成立した（主張3行は残余51行
 内部のままでopen）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109/K1113/K1114と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000801202000022080000`（root − 最小セットビット bit 12）+ bit 12 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1095出版値と
  node-exact一致: andclose1 loss=true nodes 126,683・andclose0 loss=true
  nodes 137,565・terminal石数 [14,18]（output/probe-repro-both-orderings.jsonl・
  8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [12,19,25,29,49,57,60,71]・quadruple-free・
  D4正準（8対称像中最小hexがroot自身）・root loser mobility 39を
  純Python整数3×3余因子幾何で再導出（scripts/gen_root_legal_moves.py・
  output/root-legal-moves.txt）。
- **抽出器**: K1113出版 `cert_extractor_win8_root8890020.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root22081000.ts`（探索核・修復は
  すべて同一bytes）。各root初手 m を extractW(root+m, 9) の盲抽出・自己検査付き。
  fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス39本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全39初手を単一プロセスで一括。
  **3実行とも証明書bytes完全一致**（SHA-256
  `f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致（39/39）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（K1096〜K1114出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全39初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0・-terminal-range [14,18]の4番目
  CLI引数による厳密一致。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 39 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root22081000.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1113機械のroot定数・
  期待値のみを差し替え（ROOT_HEX・CERT_RELPATH・K1095正本SHA pin・probe nodes
  126,683/137,565・bit 12・mobility 39・主張3行・実験名。g01→K1095 pin・
  g06/g07/g08のK1095参照化・g19 len(claimed)==3）、K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1095被覆行 == K1097 claimed == intrinsic の三点一致）。

19 gate（g01〜g19）は K1113 と同構成: g01 K1095正本SHA pin・g02/g03 runner v17
git blob c132cc64…の記録と原本一致・g04 root shape safe・g05 mobility 39・g06 K1095
probes win uncapped・g07 主張3行・g08 probe再現 node-exact（4 pilot・各順序2回）・
g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move node-exact・
g12 B clean・g13 chunk vs 単一プロセスのnode会計（731,232 vs 534,121）・g14 証明書
sorted-unique・末尾改行・行format・g15 B nRows==証明書行・g16 第三方法全木再走査
PASS・g17 BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言存在・
g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000801202000022081000-20261120.n11`
  ・341,498 bytes・9,460戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f`。
- **root**: 8石 [12,19,25,29,49,57,60,71]・quadruple-free・D4正準・loser初手は39手
  （K1096〜K1114歴代抽出根の50/53手より少ない最小mobility）。
  K1095 greedy主張被覆3行 `00000000000000003800000808001000`・
  `00000000000000801202000000081000`・`00000000000000801202000020001000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎39プロセス）総nodes 731,232・最大初手
  nodes 54,999（move 76）・fbt_drops 0（全39初手）・fatal/conflict 0。
  Run A2も同一（初手単位 node-exact・rows byte-identical）。
  Run B（単一プロセス・memo温存）総nodes 534,121・戦略行9,460で内容不変
  （chunk/単一プロセスのnode会計の乖離はmemo効果のみ）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 23,542（sub-root単位）・winner-to-move 15,228・loser-to-move 5,032・
  loser応手辺 22,031・終端 3,282（全てloser-stuck）・終端石数 [14,18]・
  consumed union == 9,460 == 証明書行9,460（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 39。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1095出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000022080000 \
  --bits 12 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000801202000022080000 \
  --bits 12 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# （各順序2回ずつ計4回・probe-repro-both-orderings.jsonl は 8 records）
# root初手再導出
python3 scripts/gen_root_legal_moves.py
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root22081000.ts \
  --root 00000000000000801202000022081000 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 39 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000801202000022081000 --root-check
#   （--subroots 全39手 で bareiss-stats.txt）
# 検証3: python3 scripts/assemble_win8_audit_root22081000.py --out output/….json
```
