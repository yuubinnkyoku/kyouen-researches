# n11 残余51行 WIN8-D10 root `00000000000000801212000001009000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1091（fold15後残余確定用の代替根 depth-10掃引・正本 SHA-256
`edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`・本実験dir内
`output/.input-k1091.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した根のうち、**fold16/K1116 完了後（残余51行レーン）で抽出未着手・
未宣言候補の中で最安価**の
`00000000000000801212000001009000`（主張被覆4行・probe nodes 192,365/229,502・
probe総nodes 421,867 = 残り候補中最小・root loser mobility 44）に対して、
完全勝利戦略証明書
（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・
独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000000801212000001009000-single-owner-note.md`
（commit `93f56291df82955662017397e2be953b3c01ffd9`）の下で実施した。
並走レーンがroot `00000000000000801202000022081000`の抽出（K1117）・
同rootのfold17（receipt fold）宣言（commit `7f8243644c…`）を行っているが、
本rootはそれらとは別根であり、抽出・fold済みの7根
（8003180・8005021・9840004・9090022・8890020・120000038・22081000/K1117）とも
独立のプロセス・機材による抽出である。K1116（fold16）が残余55→51に移動した
際の閉鎖5行・fold15閉鎖行は着手前に本rootの主張4行と機械的にdisjointである
ことを確認済みであり、主張4行は残余レーン内でopenのままである（本dirのpush直前に
出版されたfold17/K1118の閉鎖7行〔K1117主張3行+target外余剰4行〕とも機械照合で
disjoint・fold17後は残余48行内でopen）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109/K1113/K1114/K1117と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000801212000001008000`（root − 最小セットビット bit 12）+ bit 12 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1091出版値と
  node-exact一致: andclose1 loss=true nodes 192,365・andclose0 loss=true
  nodes 229,502・terminal石数 [14,18]（output/probe-repro-both-orderings.jsonl・
  8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [12,15,24,49,52,57,60,71]・quadruple-free・
  D4正準（8対称像中最小hexがroot自身）・root loser mobility 44を
  純Python整数3×3余因子幾何で再導出（scripts/gen_root_legal_moves.py・
  output/root-legal-moves.txt）。
- **抽出器**: K1117出版 `cert_extractor_win8_root22081000.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root1009000.ts`（探索核・修復は
  すべて同一bytes。系譜はK1113 `cert_extractor_win8_root8890020.ts`）。各root初手 m を
  extractW(root+m, 9) の盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス44本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全44初手を単一プロセスで一括。
  **3実行とも証明書bytes完全一致**（SHA-256
  `b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致（44/44）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（歴代出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全44初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0・-terminal-range [14,18]の4番目
  CLI引数による厳密一致。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 44 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root1009000.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1113機械のroot定数・
  期待値のみを差し替え（ROOT_HEX・CERT_RELPATH・K1091正本SHA pin・probe nodes
  192,365/229,502・bit 12・mobility 44・主張4行・実験名。g01→K1091 pin・
  g05 mobility 44・g07 主張4行・g19 len(claimed)==4）、K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1091被覆行 == K1097 claimed == intrinsic の三点一致）。

19 gate（g01〜g19）は K1113/K1117 と同構成: g01 K1091正本SHA pin・g02/g03 runner v17
git blob c132cc64…の記録と原本一致・g04 root shape safe・g05 mobility 44・
g06 K1091 probes win uncapped・g07 主張4行・g08 probe再現 node-exact（4 pilot・各順序2回）・
g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move node-exact・
g12 B clean・g13 chunk vs 単一プロセスのnode会計（865,602 vs 712,106）・g14 証明書
sorted-unique・末尾改行・行format・g15 B nRows==証明書行・g16 第三方法全木再走査
PASS・g17 BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言存在・
g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000801212000001009000-20261120.n11`
  ・587,989 bytes・16,262戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c`。
- **root**: 8石 [12,15,24,49,52,57,60,71]・quadruple-free・D4正準・loser初手は44手。
  K1091 greedy主張被覆4行 `00000000000000003800200008001000`・
  `00000000000000003800200009000000`・`00000000000000801212000000001000`・
  `00000000000000801212000001000000` はK1097 win16 footprint（intrinsic == claimed）
  とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎44プロセス）総nodes 865,602・最大初手
  nodes 73,618（move 99）・fbt_drops 0（全44初手）・fatal/conflict 0。
  Run A2も同一（初手単位 node-exact・rows byte-identical）。
  Run B（単一プロセス・memo温存）総nodes 712,106・戦略行16,262で内容不変
  （chunk/単一プロセスのnode会計の乖離はmemo効果のみ）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 37,696（sub-root単位）・winner-to-move 24,352・loser-to-move 7,561・
  loser応手辺 34,261・終端 5,783（全てloser-stuck）・終端石数 [14,18]・
  consumed union == 16,262 == 証明書行16,262（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 44。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1091出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000801212000001008000 \
  --bits 12 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000801212000001008000 \
  --bits 12 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# （各順序2回ずつ計4回・probe-repro-both-orderings.jsonl は 8 records）
# root初手再導出
python3 scripts/gen_root_legal_moves.py
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root1009000.ts \
  --root 00000000000000801212000001009000 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 44 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000801212000001009000 --root-check
#   （--subroots 全44手 で bareiss-stats.txt）
# 検証3: python3 scripts/assemble_win8_audit_root1009000.py --out output/….json
```
