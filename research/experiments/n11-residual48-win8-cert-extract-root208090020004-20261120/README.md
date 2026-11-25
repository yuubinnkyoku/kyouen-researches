# n11 残余48行 WIN8-D10 root `00000000000020809002000480100000` 証明書抽出・三重検証（2026-11-20）: fresh-probe基盤第1例

## 目的

K1089（replacement16）由来の WIN8-D10 候補根で、K1091掃引正本 per_root（15根）にも
K1095掃引正本 per_root（12根）にもprobe記録が存在せず、**probe総nodesが最小**
（K1119研究log出版値 793,616）となる `00000000000020809002000480100000`
（石 [20,31,34,49,60,63,71,77]・主張被覆3行・root loser mobility 54）に対して、
完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）
の盲抽出・独立検証を行った。**出版probe記録（掃引正本pin）を持たない根としては
fold17/K1118後の未着手・未宣言候補の中で最安価**であり、掃引正本pinの代わりに
K1119研究log（残余51行レーン・7根全測定・出版済み）の probe総nodes 793,616
（両AND順序 uncapped loss=true）を本実験のfresh-probe（両順序×2回）でnode-exact
再現してpinする、**fresh-probe基盤のプロトコル拡張適用第1例**である。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000020809002000480100000-single-owner-note.md`
（commit `e75c65b47632398474797de40922acad043cf560`）の下で実施した。
実行中に並走レーンが fold18/K1122（root `00000000000801202000000901010`・
receipt fold・残余48→45）を出版したため、主張3行のopen性はfold18正本
（SHA-256 `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`・
`output/.input-fold18.json` にpin）の残余45行 `residual_row_hex_after` に対して
機械照合した（fold18閉鎖4行〔3 claimed + 1 extra〕と主張3行は完全にdisjoint・
主張3行は残余45行内でopen）。fold19（root 1009000/K1119証明書のreceipt fold）は
並走が宣言済み（commit `3a23ccf30b`）で経路不競合。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論は別工程であり、本実験では確定しない。
本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（歴代WIN8抽出実験と同一構成・全機材は本dirに同梱）

- **fresh-probe（verdict基盤の確立）**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000020809002000480000000`（root − 最小セットビット bit 20）+ bit 20 の
  両AND順序 depth-10 probeを計4回実行（各順序2回・cap 4,000,000）。いずれの順序も
  uncapped loss=true・終局石数 [14,18]: andclose1 nodes 350,792・andclose0 nodes
  442,824・**合計 793,616 がK1119研究log（git blob
  `51bad3fac4c36fcd1cbf6aeec01b7e153d9adb89`・SHA-256
  `4d11ca896815b73e4e0616a07c81f7abc582d4f5401174462d63e3abd27a4472`・
  `output/.input-k1119-log.md` にpin）の出版総nodesとnode-exact一致**
  （output/probe-repro-both-orderings.jsonl・8 records = pilot 4 + probe 4）。
  K1091/K1095両掃引正本に本rootのper_root記録がないことを機械確認済み。
- **root初手の独立再導出**: 8石 [20,31,34,49,60,63,71,77]・quadruple-free・
  D4正準（8対称像中最小hexがroot自身）・root loser mobility 54を
  純Python整数3x3余因子幾何で再導出（scripts/gen_root_legal_moves.py・
  output/root-legal-moves.txt）。
- **抽出器**: K1121出版 `cert_extractor_win8_root08d10000.ts` をroot引数・filename
  guardのみ差し替えた `scripts/cert_extractor_win8_root20809002000480100000.ts`
  （探索核・fbtOR修復はすべて同一bytes。系譜はK1113
  `cert_extractor_win8_root8890020.ts`）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス54本・総nodes 3,009,765（最大初手: move 117 の
  165,221・fbt_drops 0）、Run A2 = A1の完全再実行（初手単位node-exact一致・
  row集合byte-identical）、Run B = 全54初手を単一プロセスで一括（nodes 3,009,765）。
  **3実行とも証明書行集合完全一致（23,621行）**。Bのnode会計はA1と同一だった
  （K1109 root 9090022 と同型。戦略行の不変性が本質でありmemoによる会計削減は
  本rootでは現れなかった）。
- **独立検証3方法**:
  (1) TS BigInt 3x3余因子展開（`scripts/verify_win8_certificate_bigint_independent.mjs`・
  歴代出版検証器と同一bytes）: root+全54初手から全木走査・全winner行の消費・選択手
  合法性・全loser応手展開・終端はloser-stuckのみ・被覆union過不足0・terminal-range
  [14,18] のCLI引数による厳密一致。
  (2) TS Bareiss 4x4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 54 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root208090020004.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1121機械のroot定数・
  期待値差し替えに加え、**fresh-probe基盤のgate再構成**を行った: g01/g02 はK1091/K1095
  掃引正本pinの代わりにK1119研究logのSHA-256/git blob pinと「本root probe総nodes
  793,616 出版済み・両AND順序uncapped loss=true」記述の機械照合、g06/g08 は本実験の
  fresh-probe記録（350,792/442,824・合計==793,616）のnode-exact検証、g07 は主張3行の
  唯一の出版キャリアとしてのK1097 refsolve正本（SHA-256 `2896deb0…`）footprint照合、
  g19 はK1097 footprint三点一致 + fold18正本SHA pin・残余45行内で主張3行がopen
  （fold18閉鎖4行との完全disjoint）の追加検証。

19 gate（g01〜g19）構成: g01 K1119 log SHA-256/git blob pin・g02 K1119 log内
本rootprobe総出版記述・g03 runner v17 copy git blob一致・g04 root shape safe・
g05 mobility 54・g06 fresh-probe定数合計==793,616・g07 K1097主張3行・
g08 probe再現 bit 20 node-exact（4 pilot・各順序2回）・g09 root初手リスト==独立再導出・
g10 A1/A2 clean・g11 A1==A2 per-move node-exact・g12 B clean・g13 chunk vs 単一
プロセスのnode会計（3,009,765 vs 3,009,765）・g14 証明書sorted-unique・末尾改行・
行format・g15 B nRows==証明書行・g16 第三方法全木再走査PASS・g17
BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言存在・g19 K1097
footprint + fold18残余45行内open。

## 結果（全19 gate PASS・3方法の全数値一致・3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000020809002000480100000-20261120.n11`
  ・855,258 bytes・23,621戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e`。
- **root**: 8石 [20,31,34,49,60,63,71,77]・quadruple-free・D4正準・loser初手は54手。
  K1097 refsolve win16 footprintの主張3行
  `00000000000000801202040000001000`・`00000000000000801202040000800000`・
  `00000000000020809002000080000000`（intrinsic == claimed・g07/g19）はfold18正本の
  残余45行内でopen。fold時は別工程。
- **三重検証の全数値一致**: visited 49,094・winner-to-move 31,623・loser-to-move
  9,955・loser応手辺 43,650・終端 7,516（全loser-stuck）・終端石数 [14,18]・
  consumed union == 23,621 == 証明書行（missing 0 / extra 0）。
  Bareiss root-check: stones 8・loserMobility 54。
- **監査**: 19/19 gate PASS。同一cwd 2回 + 別cwd別プロセス（EXPERIMENT_ROOT隔離
  複写）1回の3実行で監査JSON byte-identical・正本
  `output/win8-cert-extract-verification-20261120.json` SHA-256
  `6ea634c9fdd005626904669e08cb7139e59e78120a0b8c9e1dd48fde0b70ddf0`。

## 再現

```sh
# fresh-probe（両順序×2回・pilot_d6制御込み）
node --experimental-strip-types runner_v17.ts --child 00000000000020809002000480000000 \
  --bits 20 --depth 10 --cap 4000000 --andclose 1 --out probe-ac1.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000020809002000480000000 \
  --bits 20 --depth 10 --cap 4000000 --andclose 0 --out probe-ac0.jsonl
# root初手
python3 scripts/gen_root_legal_moves.py   # mobility 54 -> output/root-legal-moves.txt
# 抽出（初手ごと1プロセス・A1/A2。Bは全初手一括）
node --experimental-strip-types scripts/cert_extractor_win8_root20809002000480100000.ts \
  --root 00000000000020809002000480100000 --moves 0 --subtree-depth 9 \
  --summary-out ext-summary-a1.jsonl --rows-out rows-a1.txt
# 検証
node scripts/verify_win8_certificate_bigint_independent.mjs certs/win8-root-00000000000020809002000480100000-20261120.n11 54 14,18
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-00000000000020809002000480100000-20261120.n11 \
  --root 00000000000020809002000480100000 --root-check
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-00000000000020809002000480100000-20261120.n11 \
  --root 00000000000020809002000480100000 --subroots 0,2,4,...,118
python3 scripts/assemble_win8_audit_root208090020004.py \
  --out output/win8-cert-extract-verification-20261120.json
```

## 解釈上の制限（不変）

本証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は
別工程であり、行の閉鎖claimは本実験では行わない（本抽出は行を1つも閉じない）。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**
