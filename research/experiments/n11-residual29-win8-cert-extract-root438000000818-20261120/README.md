# n11 残余29行 WIN8-D10 root `00000000000000043800000008180010` 証明書抽出・三重検証（2026-11-20）: fold24 候補A・標準掃引pin基盤

## 目的

fold23（K1133・残余 32→29）出版後の残余 29 行に対する新規掃引設計の第1着手として、
残存 WIN8-D10 候補 3 根（他 2 根 `00000000000200003800200008180000`〔mobility 42〕・
`0000000800000000380000000810000a`〔mobility 58〕）のうち **probe総nodesが最小**
（K1091 掃引正本 per_root pin 882,327/1,054,873・合計 1,937,200）かつ
**主張 3 行（他候補の残余主張のうち最小）を採る** root
`00000000000000043800000008180010`（石 [4,19,20,27,59,60,61,66]・quadruple-free・
D4 正準・root loser mobility 50・閉鎖 edge cost 225・幾何 open == 主張のみ・余剰なし）に対して、
完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の
盲抽出・独立検証を行った。**verdict基盤は標準プロトコル（掃引正本pin）** であり、
K1091 replace15-d10-sweep 正本の per_root probe 記録（両 AND 順序 uncapped loss=true・
終局石数 [14,18]・covered_rows 3 行）を本実験の fresh-probe（両順序×2回）で
node-exact 再現して pin する。K1119 研究 log にも本 root の probe 総nodes 1,937,200 の
出版記載があり二重pinとなる。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000000000043800000008180010-single-owner-note.md`
（commit `811c2423`）の下で実施した。主張 3 行
`00000000000000003800000008002040`（cost 66）・`00000000000000043800000008080000`（cost 75）・
`00000000000000043800000008100000`（cost 84）は K1097 refsolve 正本の
win16_intrinsic_footprints で intrinsic == claimed == 3 行であり、fold23 正本
`output/.input-fold23.json`（SHA-256 `04f334ff…`）の残余 29 行内で全 3 行 open
（着手前機械確認・g19 で再検証）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論は別工程であり、本実験では確定しない。
本実験はS6行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（歴代WIN8抽出実験と同一構成・全機材は本dirに同梱）

- **fresh-probe（verdict基盤の再現）**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000043800000008180000`（root − 最小セットビット bit 4）+ bit 4 の
  両AND順序 depth-10 probeを計4回実行（各順序2回・cap 4,000,000）。いずれの順序も
  uncapped loss=true・終局石数 [14,18]: andclose1 nodes 882,327・andclose0 nodes 1,054,873・
  **合計 1,937,200 がK1091掃引正本 per_root pin とnode-exact一致**
  （output/probe-repro-both-orderings.jsonl・8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [4,19,20,27,59,60,61,66]・quadruple-free・
  D4正準・root loser mobility 50を純Python整数3x3余因子幾何で再導出
  （scripts/gen_root_legal_moves.py・output/root-legal-moves.txt）。
- **抽出器**: K1121出版 `cert_extractor_win8_root08d10000.ts` をroot引数・filename guard・
  ヘッダのみ差し替えた `scripts/cert_extractor_win8_root00000000000000043800000008180010.ts`
  （探索核・fbtOR修復・recordRow衝突拒否はすべて同一bytes。系譜はK1113 WIN7抽出器）。各root初手 m を
  extractW(root+m, 9) の盲抽出・自己検査付き。fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）: Run A1 = 初手ごと新規プロセス50本・
  総nodes 3,539,166（最大初手: move 3 の 349,453・fbt_drops 0）、Run A2 = A1の完全再実行
  （初手単位node-exact一致・row集合byte-identical）、Run B = 全50初手を単一プロセスで一括
  （nodes 2,564,865・K1121 root 08d10000 と同型の一括メモ会計削減）。
  **3実行とも証明書行集合完全一致（34,843行）**。
- **独立検証3方法**:
  (1) TS BigInt 3x3余因子展開（`scripts/verify_win8_certificate_bigint_independent.mjs`・
  歴代出版検証器と同一bytes）: root+全50初手から全木走査・全winner行の消費・選択手
  合法性・全loser応手展開・終端はloser-stuckのみ・被覆union過不足0・terminal-range
  [14,18] のCLI引数による厳密一致。
  (2) TS Bareiss 4x4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 50 sub-root全走査・consumed union・per-sub-root stats。
  (3) 監査機械 `scripts/assemble_win8_audit_root438000000818.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1121出版機のroot定数・
  probe定数（882,327/1,054,873）・probe bit（16→4）・g19 gate適応に加え、
  **fold23正本pin（SHA-256 `04f334ff…`・残余29行）による主張3行open検証をg19に拡張**した。

19 gate（g01〜g19）構成: g01 K1091正本SHA-256 pin・g02 runner v17 git blob pin・
g03 runner v17固定コピーgit blob一致・g04 root shape safe（8石・quadruple-free）・
g05 mobility 50・g06 K1091 per_root probes uncapped loss=true [14,18] 882,327/1,054,873・
g07 K1091 covered_rows 3行（gained_rows 3）・g08 fresh-probe再現 bit 4 node-exact
（pilot 4・各順序2回）・g09 root初手リスト==独立再導出・g10 A1/A2 clean・
g11 A1==A2 per-move node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計
（3,539,166 vs 2,564,865・Bの一括メモ削減はK1121と同型で行集合は不変）・
g14 証明書sorted-unique・末尾改行・行format・g15 B nRows==証明書行・
g16 第三方法全木再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・
g18 解釈guard文言存在・g19 K1097 footprint intrinsic==claimed==3行 + fold23正本pin +
残余29行内で主張3行open。

## 結果（全19 gate PASS・3方法の全数値一致・3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000043800000008180010-20261120.n11`
  ・1,260,393 bytes・34,843戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004`。
- **root**: 8石 [4,19,20,27,59,60,61,66]・quadruple-free・D4正準・loser初手は50手。
  K1091/K1097主張3行 `00000000000000003800000008002040`・`00000000000000043800000008080000`・
  `00000000000000043800000008100000`（intrinsic == claimed）はfold23正本の残余29行内でopen。
  fold時は別工程（fold24 receipt fold・別機材・別宣言）。
- **三重検証の全数値一致**: visited 77,154・winner-to-move 49,599・loser-to-move 14,382・
  loser応手辺 67,581・終端 13,173（全loser-stuck）・終端石数 [14,18]・
  consumed union == 34,843 == 証明書行（missing 0 / extra 0）。
  Bareiss root-check: stones 8・loserMobility 50・sub-root 50。
- **抽出会計**: A1 chunked 3,539,166・B single-process 2,564,865（差 974,301 は一括
  メモ会計削減・K1121と同型。行集合は3実行完全一致）。
- **監査**: 19/19 gate PASS。同一cwd 2回 + 別cwd別プロセス（EXPERIMENT_ROOT隔離
  複写・別HOME）1回の3実行で監査JSON byte-identical・正本
  `output/win8-cert-extract-verification-20261120.json` SHA-256
  `d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c`。

## 再現

```sh
# fresh-probe（両順序×2回・pilot_d6制御込み）
node --experimental-strip-types runner_v17.ts --child 00000000000000043800000008180000 \
  --bits 4 --depth 10 --cap 4000000 --andclose 1 --out probe-ac1.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000043800000008180000 \
  --bits 4 --depth 10 --cap 4000000 --andclose 0 --out probe-ac0.jsonl
# root初手
python3 scripts/gen_root_legal_moves.py   # mobility 50 -> output/root-legal-moves.txt
# 抽出（初手ごと1プロセス・A1/A2。Bは全初手一括）
node --experimental-strip-types scripts/cert_extractor_win8_root00000000000000043800000008180010.ts \
  --root 00000000000000043800000008180010 --moves 1 --subtree-depth 9 \
  --summary-out ext-summary-a1.jsonl --rows-out rows-a1.txt
# 検証
node scripts/verify_win8_certificate_bigint_independent.mjs \
  certs/win8-root-00000000000000043800000008180010-20261120.n11 50 14,18
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-00000000000000043800000008180010-20261120.n11 \
  --root 00000000000000043800000008180010 --root-check
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-00000000000000043800000008180010-20261120.n11 \
  --root 00000000000000043800000008180010 --subroots 1,2,3,8,...,120
python3 scripts/assemble_win8_audit_root438000000818.py \
  --out output/win8-cert-extract-verification-20261120.json
```

## 解釈上の制限（不変）

本証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は
別工程であり、行の閉鎖claimは本実験では行わない（本抽出は行を1つも閉じない）。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**
