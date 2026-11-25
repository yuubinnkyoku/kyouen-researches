# n11 残余29行 WIN8-D10 root `0000000800000000380000000810000a` 証明書抽出・三重検証（2026-11-20）: 3候補の最終根・K1095掃引pin基盤・g19拡張

## 目的

fold23（K1133・残余 32→29）出版後の残存 WIN8-D10 候補 3 根のうち最後に残る根
`0000000800000000380000000810000a`（石 [1,3,20,27,59,60,61,99]・quadruple-free・
D4 正準・root loser mobility 58・K1095 replace12掃引正本 per_root pin
andclose1 1,226,804 / andclose0 1,416,679・主張被覆 1 行）に対して、
完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の
盲抽出・独立検証を行った。**verdict基盤は標準プロトコル（掃引正本pin）** であり、
K1095 replace12-d10-sweep 正本の per_root probe 記録（両 AND 順序 uncapped loss=true・
終局石数 [14,18]・covered_rows 1 行）を本実験の fresh-probe（両順序×2回）で
node-exact 再現して pin する。候補A root `00000000000000043800000008180010`
（K1136 出版済み）・候補B/C root `00000000000200003800200008180000`（K1137 出版済み）に続き、
**本出版で残余29レーンの全3候補の証明書が出版済みとなる（出版probe pin候補の抽出枯渇）**。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual29-win8-cert-extract-root0810000a-single-owner-note.md`
（commit `943dfc3608`・残余72期旧宣言の更新〔supersede〕込み）の下で実施した。

**本根は出版probe pin候補で唯一 K1097 win16 intrinsic footprint が
`intrinsic_equals_claimed == false`** である: 主張 1 行
`00000008000000003800000008100000`（== K1095 per_root covered_rows）に対し
intrinsic 2 行（主張 + `00000000000000003800000008001080`）。余剰intrinsic行は
K1097 win16計画上 root `00000000000000003800000008003180` の主張行であり、
fold11（18番目receipt・正本 SHA-256 `d7bf2cd5…`）の receipt covered rows で
簿計閉鎖済み・fold23正本の残余29行外である（着手前機械確認込み）。このため監査機械の
g19 gate は宣言ノートに基づく **fail-closed拡張**（主張==幾何==1行・fold23残余29行内open・
intrinsic==主張∪余剰・余剰行の3点検証〔K1097 root `…8003180` claimed・fold11 covered・
fold23残余29外〕）を採用した。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論は別工程であり、本実験では確定しない。
本実験は行を1つも閉じない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1114/K1120/K1124/K1136/K1137 と同一構成・全機材は本dirに同梱）

- **fresh-probe（verdict基盤の再現）**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000008000000003800000008100008`（root − 最小セットビット bit 1）+ bit 1 の
  両AND順序 depth-10 probeを計4回実行（各順序2回・cap 4,000,000）。いずれの順序も
  uncapped loss=true・終局石数 [14,18]: andclose1 nodes 1,226,804・andclose0 nodes
  1,416,679 がK1095掃引正本 per_root pin とnode-exact一致
  （output/probe-repro-both-orderings.jsonl・8 records = pilot 4 + probe 4）。
- **root初手の独立再導出**: 8石 [1,3,20,27,59,60,61,99]・quadruple-free・
  D4正準・root loser mobility 58を純Python整数3x3余因子幾何で再導出
  （scripts/gen_root_legal_moves.py・output/root-legal-moves.txt・58手）。
- **抽出器**: K1137出版 `cert_extractor_win8_root00000000000200003800200008180000.ts` を
  root引数・filename guard・ヘッダのみ差し替えた
  `scripts/cert_extractor_win8_root0000000800000000380000000810000a.ts`
  （hex 5箇所+文言差し替え・生成器で出現回数assert。探索核・fbtOR修復・recordRow衝突拒否は
  すべて同一bytes。系譜はK1113 WIN7抽出器）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）: Run A1 = 初手ごと新規プロセス58本
  （xargs -P 4）・総nodes 3,515,506（最大初手: move 120 の 186,821・fbt_drops 0）、
  Run A2 = A1の完全再実行（初手単位node-exact一致・row集合byte-identical）、
  Run B = 全58初手を単一プロセスで一括（nodes 2,808,991・K1121/K1136/K1137 と同型の
  一括メモ会計削減）。**3実行とも証明書行集合完全一致（48,018行）**。
- **独立検証3方法**:
  (1) TS BigInt 3x3余因子展開（`scripts/verify_win8_certificate_bigint_independent.mjs`・
  歴代出版検証器と同一bytes）: root+全58初手から全木走査・全winner行の消費・選択手
  合法性・全loser応手展開・終端はloser-stuckのみ・被覆union過不足0・terminal-range
  [14,18] のCLI引数による厳密一致（subroots 58/58 PASS）。
  (2) TS Bareiss 4x4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check（stones 8・loserMobility 58）+ 58 sub-root全走査・consumed union・
  per-sub-root stats（output/bareiss-stats.txt）。
  (3) 監査機械 `scripts/assemble_win8_audit_root0000000800000000380000000810000a.py`
  （Python stdlibのみ・engine importなし・第三実装として独自に全木を再走査）。
  K1137出版機からroot定数・probe定数（1,226,804/1,416,679・andclose0/andclose1 逆転なし）・
  probe bit（19→1）・全体差し替え（出現回数assertつき生成器変換）を行い、
  **g19は上記宣言ノートの拡張版**とし、**fold11正本 pin（SHA-256 `d7bf2cd5…`）を
  `output/.input-fold11.json` として追加**した。

19 gate（g01〜g19）構成: g01 K1095正本SHA-256 pin・g02 runner v17 git blob pin・
g03 runner v17固定コピーgit blob一致・g04 root shape safe（8石・quadruple-free）・
g05 mobility 58・g06 K1095 per_root probes uncapped loss=true [14,18]
1,226,804/1,416,679・g07 K1095 covered_rows 1行（主張と一致）・g08 fresh-probe再現
bit 1 node-exact（pilot 4・各順序2回）・g09 root初手リスト==独立再導出・g10 A1/A2 clean・
g11 A1==A2 per-move node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計
（3,515,506 vs 2,808,991・Bの一括メモ削減は歴代と同型で行集合は不変）・
g14 証明書sorted-unique・末尾改行・行format・g15 B nRows==証明書行・
g16 第三方法全木再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・
g18 解釈guard文言存在・**g19 K1095/K1097/fold23正本pin + 主張1行のfold23残余29行内open
+ intrinsic==主張∪余剰 + 余剰intrinsic行の3点検証（K1097 root `…8003180` claimed・
fold11 covered〔4行〕・fold23残余29外）**。

## 結果（全19 gate PASS・3方法の全数値一致・3実行byte-identical）

- **証明書**: `certs/win8-root-0000000800000000380000000810000a-20261120.n11`
  ・1,739,641 bytes・48,018戦略行 + root行 + header行（48,020行・行は昇順・一意）。
  SHA-256 `089e175d781dbbc620b3dce7733dc29993d5bd686670e047591a968917e6a6d1`。
- **root**: 8石 [1,3,20,27,59,60,61,99]・quadruple-free・D4正準・loser初手は58手。
  主張1行 `00000008000000003800000008100000` はfold23正本の残余29行内でopen。
  余剰intrinsic行 `00000000000000003800000008001080` はK1097上はroot
  `00000000000000003800000008003180` の主張行でfold11 receiptがclosure済み
  （残余29行外）。将来の本rootのreceipt foldは別の単一オーナー宣言を要し、
  fold23残余29内にopenな行は主張1行のみであるため簿計対象も主張1行のみとなる。
- **三重検証の全数値一致**: BigInt・Bareiss・python第三実装の3方法で
  visited 102,267・winner-to-move 65,449・loser-to-move 18,943・loser応手辺 89,522・
  終端 17,875（全loser-stuck）・終端石数 [14,18]・
  consumed union == 48,018 == 証明書行（missing 0 / extra 0）・
  Bareiss root-check: stones 8・loserMobility 58・58 sub-root完全一致。
  （BigInt検証正本: forbidden triple cache 26,763 entries・legal state cache 73,696 entries。）
- **抽出会計**: A1 chunked 3,515,506・B single-process 2,808,991（差 706,515 は一括
  メモ会計削減・歴代と同型。行集合は3実行完全一致）。
- **監査**: 19/19 gate PASS。同一cwd 2回 + 別cwd別プロセス（EXPERIMENT_ROOT隔離複写・
  別HOME）1回の3実行で監査JSON byte-identical・正本
  `output/win8-cert-extract-verification-20261120.json` SHA-256
  `e706ca6fd2390d014509546279398f854197975bb57c44e87dba06f6668d4daf`。

## 再現

```sh
# fresh-probe（両順序×2回・pilot_d6制御込み）
node --experimental-strip-types runner_v17.ts --child 00000008000000003800000008100008 \
  --bits 1 --depth 10 --cap 4000000 --andclose 1 --out repro-ac1.jsonl
node --experimental-strip-types runner_v17.ts --child 00000008000000003800000008100008 \
  --bits 1 --depth 10 --cap 4000000 --andclose 0 --out repro-ac0.jsonl
# root初手
python3 scripts/gen_root_legal_moves.py   # mobility 58 -> output/root-legal-moves.txt
# 抽出（初手ごと1プロセス・A1/A2。Bは全初手一括）
node --experimental-strip-types scripts/cert_extractor_win8_root0000000800000000380000000810000a.ts \
  --root 0000000800000000380000000810000a --moves 1 --subtree-depth 9 \
  --summary-out ext-summary-a1.jsonl --rows-out rows-a1.txt
# 検証
node scripts/verify_win8_certificate_bigint_independent.mjs \
  certs/win8-root-0000000800000000380000000810000a-20261120.n11 58 14,18
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-0000000800000000380000000810000a-20261120.n11 \
  --root 0000000800000000380000000810000a --root-check
node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
  --cert certs/win8-root-0000000800000000380000000810000a-20261120.n11 \
  --root 0000000800000000380000000810000a --subroots 2,4,5,14,...,118,120
python3 scripts/assemble_win8_audit_root0000000800000000380000000810000a.py \
  --out output/win8-cert-extract-verification-20261120.json
```

## 解釈上の制限（不変）

本証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は
別工程であり、行の閉鎖claimは本実験では行わない（本抽出は行を1つも閉じない）。
REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**
