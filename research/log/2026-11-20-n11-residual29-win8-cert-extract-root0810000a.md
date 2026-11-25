# n11 残余29行 WIN8-D10 root 0000000800000000380000000810000a 証明書抽出・三重検証（3候補最終根・K1095掃引pin基盤・2026-11-20）

## 選定

fold23（K1133・残余32→29）出版後の残存win16候補3根のうち、K1136（候補A root `00000000000000043800000008180010`）・
K1137（候補B/C root `00000000000200003800200008180000`）が出版済みで、残る唯一の未着手根
`0000000800000000380000000810000a`（石 [1,3,20,27,59,60,61,99]・quadruple-free・D4正準・mobility 58・
K1095 replace12掃引正本 per_root pin andclose1 1,226,804 / andclose0 1,416,679・主張被覆1行）を本実行の対象とした。

本根は出版probe pin候補で唯一 K1097 win16 footprint が `intrinsic_equals_claimed == false`（主張1行
`00000008000000003800000008100000` に対しintrinsic 2行・余剰行 `00000000000000003800000008001080` は
K1097上root `00000000000000003800000008003180` の主張行でfold11〔K1105〕receiptが簿計閉鎖済み・
fold23残余29行外）であるため、着手前に単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual29-win8-cert-extract-root0810000a-single-owner-note.md`
（commit `943dfc3608`・残余72期旧宣言のsupersede込み・着手前機械確認込み）を先行出版し、
g19プロトコル拡張を宣言した。

## 実行

- **fresh-probe**: runner v17固定コピー（git blob `c132cc64…`）で child=`00000008000000003800000008100008`
  （root − bit 1）+ bit 1 の両AND順序×2回（depth-10・cap 4,000,000）。
  andclose1 1,226,804 / andclose0 1,416,679・両順序 uncapped loss=true・終局石数 [14,18]・pilot_d6 4/4（3,402）。
  **K1095掃引正本per_root pinとnode-exact一致**（output/probe-repro-both-orderings.jsonl 8 records）。
- **root初手再導出**: 純Python 3x3余因子幾何で mobility 58（output/root-legal-moves.txt・58手）。
- **抽出**: K1137出版抽出器のroot引数・filename guard・ヘッダのみ差し替えた
  `cert_extractor_win8_root0000000800000000380000000810000a.ts`（hex 5箇所+文言差し替え・生成器で出現回数assert・
  探索核同一bytes）で A1（初手×58プロセス・xargs -P 4・総nodes 3,515,506・最大 初手120 の 186,821・fbt_drops 0）・
  A2（完全再実行・初手単位node-exact一致・rows byte-identical）・B（単一プロセス一括 2,808,991・
  歴代と同型のメモ会計削減）の3実行。**行集合byte-identical（48,018行）**。
- **三重検証**: BigInt 3x3余因子展開（subroots 58/58 PASS・union missing/extra 0）・Bareiss 4x4整数行列式
  （root-check stones 8 / loserMobility 58・subroots 58・per-sub-root stats）・Python監査機械（第三実装全木再走査）。
  3方法の全集計値一致: visited 102,267・winner 65,449・loser 18,943・応手辺 89,522・終端 17,875（全loser-stuck）・
  終端石数 [14,18]。
- **監査機械**: K1137出版機を適応（root定数・probe定数 1,226,804/1,416,679・g08 bit 19→1・
  **g19を宣言ノートの拡張版に差し替え**〔主張1行のfold23残余29行内open・intrinsic==主張∪余剰・
  余剰行の3点検証（K1097 pred-claim owner・fold11 covered 4行・残余29外）〕・
  **fold11正本pin（SHA-256 `d7bf2cd5…`）を `.input-fold11.json` として追加**・
  差し替えは出現回数assertつき生成器変換）。
  **19/19 gate PASS**。同一cwd 2回 + 隔離EXPERIMENT_ROOT複写・別cwd別HOME別プロセス1回の3実行で
  監査JSON byte-identical（SHA-256 `e706ca6fd2390d014509546279398f854197975bb57c44e87dba06f6668d4daf`）。

## 出版

- part1 `0ac6e503da`（README + scripts 5 + runner_v17.ts + output 13ファイル・計20ファイル）
- part2 `4f5619838`（証明書本体 certs/win8-root-0000000800000000380000000810000a-20261120.n11・
  1,739,641 bytes・push後raw CDN fetch-backでSHA-256 `089e175d…` byte-exact確認）
- fetch-back照合: part1は20ファイルすべてraw CDN fetch-back byte-identical（4 input pin・監査正本・
  runner_v17.ts・抽出器・監査機・README込み）
- part3 K1139 item（本ファイル）+ 本log + index bullet

## 採番（K1139）

push直前の3点確認（search_code・knowledge README全文grep・itemsパス404確認）でK1139が未使用であることを確認した。
K1133（fold23）〜K1138（縦繊維y=9 fit）は使用済み・fold24（候補A receipt fold）は並走宣言済み
（commit `0c9e174e9c`）で本レーンの対象外。採番衝突は検出されなかった。

## 限界と次段

- 本実験は行を1つも閉じない（証明書はrootのゲーム木のみを証明）。**残余29レーンの3候補
  （K1136・K1137・本抽出）の証明書がすべて出版済みとなり、出版probe pin候補の抽出は枯渇**。
- 残余29行の縮小は各候補のreceipt foldが担当（fold24候補Aは並走宣言済み・候補Bは未宣言・本rootは未宣言）。
  fold23残余29内で本rootの冪等な簿計対象は主張1行のみ（余剰intrinsic行はfold11閉鎖済み・残余29外）。
- 本rootのreceipt fold・fold後のrefsolveは着手時に別の単一オーナー宣言を要する。

## 解釈規約（不変）

WIN8-D10 は当該 8 石 root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。
nodes 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
