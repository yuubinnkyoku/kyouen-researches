---
id: K1139
title: 残余29行のWIN8-D10 root 0000000800000000380000000810000a 証明書抽出・三重検証（3候補最終根・K1095掃引pin基盤・g19拡張）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - residual29 final candidate cert-extract root 0810000a
  - K1095掃引正本per_root pin基盤のWIN8証明書抽出（fresh probes 1,226,804/1,416,679 node-exact再現）
  - 残存win16候補3根の最終根の新規証明書（残余29レーン出版probe pin候補抽出枯渇）
relations:
  - type: depends_on
    target: K1095
    note: replace12-d10-sweep正本（SHA-256 335eca5e…・output/.input-k1095.json にpin）per_root探査記録（andclose1 1,226,804・andclose0 1,416,679・両順序 uncapped loss=true・終局石数[14,18]・covered_rows 1行）が本実験fresh-probeのnode-exact一致源
  - type: depends_on
    target: K1097
    note: refsolve正本（SHA-256 2896deb0…・output/.input-k1097.json にpin）win16_intrinsic_footprints で本根は出版probe pin候補で唯一 intrinsic_equals_claimed == false（claimed 1行・intrinsic 2行）。余剰intrinsic行 00000000000000003800000008001080 はK1097上root 00000000000000003800000008003180 の主張行（g19で機械照合）
  - type: depends_on
    target: K1133
    note: fold23正本（SHA-256 04f334ff…・output/.input-fold23.json にpin）残余29行内で主張1行がopen（g19・residual_target_rows==29照合込み）
  - type: depends_on
    target: K1105
    note: fold11（root 00000000000000003800000008003180 receipt）正本（SHA-256 d7bf2cd5…・output/.input-fold11.json にpin）の receipt covered rows が余剰intrinsic行を簿計閉鎖済み・fold23残余29行外であることがg19の3点検証のうち2点
  - type: depends_on
    target: K1096
    note: 余剰intrinsic行の主張オーナーroot 00000000000000003800000008003180 のWIN8証明書のように先行出版で同rootのゲーム木が確定済みであることが K1097/K1105 の前提
  - type: depends_on
    target: K1137
    note: 抽出器（cert_extractor_win8_root00000000000200003800200008180000.ts）・監査機械の出版系譜。本実験の抽出器・監査機はroot定数・probe定数・g19拡張のみ差し替え（探索核・第三実装ロジック同一bytes・生成器の出現回数assertつき変換）
artifacts:
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/README.md
    role: source
    note: 候補選定・K1095掃引pin基盤・g19拡張プロトコル・19 gate構成・結果・解釈上の制限
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/certs/win8-root-0000000800000000380000000810000a-20261120.n11
    role: data
    note: 証明書正本（48,018戦略行 + root行 + header行・1,739,641 bytes・SHA-256 089e175d781dbbc620b3dce7733dc29993d5bd686670e047591a968917e6a6d1）
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/output/win8-cert-extract-verification-20261120.json
    role: verifier
    note: 19/19 gate監査正本（all_gates_pass・3実行byte-identical・SHA-256 e706ca6fd2390d014509546279398f854197975bb57c44e87dba06f6668d4daf）
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/scripts/cert_extractor_win8_root0000000800000000380000000810000a.ts
    role: verifier
    note: K1137出版抽出器の根差し替え版（fbt_drops 0・recordRow衝突拒否込み・A1/A2/B 3実行で行集合byte-identical）
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/scripts/assemble_win8_audit_root0000000800000000380000000810000a.py
    role: verifier
    note: K1137監査機の適応版（root定数・probe定数・bit 19→1・g19宣言ノート拡張・fold11正本pin追加・第三実装全木再走査は同一ロジック）
  - path: research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/runner_v17.ts
    role: source
    note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・g03で照合）
  - path: research/log/2026-11-20-n11-residual29-win8-cert-extract-root0810000a.md
    role: log
    note: 選定・宣言・実行・三重検証・出版（part1 0ac6e503da・part2 4f5619838・part3採番K1139）の研究記録
  - path: research/log/2026-11-20-n11-residual29-win8-cert-extract-root0810000a-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 943dfc3608・g19プロトコル拡張宣言・残余72期旧宣言のsupersede込み）の先行出版
---

# 残余29行のWIN8-D10 root 0000000800000000380000000810000a 証明書抽出・三重検証（3候補最終根）

fold23（K1133）出版後の残存WIN8-D10候補3根（A=K1136 root `00000000000000043800000008180010`・
B/C=K1137 root `00000000000200003800200008180000`・本根）の最終根
`0000000800000000380000000810000a`（石[1,3,20,27,59,60,61,99]・mobility 58）の完全勝利戦略証明書を
盲抽出・三重独立検証した。**K1095 replace12掃引正本per_root pin基盤**（fresh-probe両順序×2回で
node-exact再現）。**本出版で残余29レーンの3候補すべての証明書が出版済みとなる（出版probe pin候補の
抽出枯渇マイルストーン）**。

## 主要結果

- **証明書**: 48,018戦略行 + root行 + header行（48,020行）・1,739,641 bytes・行は昇順一意。
  SHA-256 `089e175d781dbbc620b3dce7733dc29993d5bd686670e047591a968917e6a6d1`。
- **fresh-probe（K1095 pin再現）**: bit 1（root − 最小セットビット）child
  `00000008000000003800000008100008` + bit 1・depth-10・cap 4,000,000・両AND順序×2回で
  andclose1 1,226,804 / andclose0 1,416,679・両順序 uncapped loss=true・終局石数 [14,18]・
  pilot_d6 制御 4/4（nodes 3,402）がK1095掃引正本per_root pinとnode-exact一致。
- **抽出3実行**: A1 = 初手ごと新規プロセス58本（xargs -P 4・総nodes 3,515,506・最大初手 move 120 の
  186,821・fbt_drops 0）・A2 = A1完全再実行（初手単位node-exact一致）・B = 単一プロセス一括
  （2,808,991・歴代と同型の一括メモ会計削減）。**3実行とも証明書行集合byte-identical**。
- **三重独立検証の全数値一致**: BigInt 3x3余因子 / Bareiss 4x4整数行列式 / Python第三実装全木再走査の
  3方法で visited 102,267・winner-to-move 65,449・loser-to-move 18,943・loser応手辺 89,522・
  終端 17,875（全loser-stuck）・終端石数 [14,18]・consumed union == 48,018 == 証明書行
  （missing 0 / extra 0）・Bareiss root-check stones 8 / loserMobility 58・58 subroot完全一致。
- **19/19 gate監査**: g01〜g03 基盤pin（K1095正本SHA・runner v17 git blob）・g04/g05 root形状と
  mobility 58・g06〜g08 K1095 pinとfresh-probe再現・g09 初手リスト==独立再導出・g10〜g13
  抽出3実行とnode会計・g14/g15 証明書format・g16/g17 第三方法と三方法集計一致・g18 解釈guard文言・
  **g19 拡張版**（後述）。正本は同一cwd 2回 + 別cwd別HOME別プロセス（隔離EXPERIMENT_ROOT複写）1回の
  3実行でbyte-identical（SHA-256 `e706ca6fd2390d014509546279398f854197975bb57c44e87dba06f6668d4daf`）。

## g19拡張（宣言ノート基盤・本根固有）

本根は出版probe pin候補で唯一K1097 win16 footprintが intrinsic_equals_claimed == false
（主張1行 `00000008000000003800000008100000` に対しintrinsic 2行）。単一オーナー宣言ノート
（commit `943dfc3608`）が宣言したfail-closed拡張を機械化した: (1) claimed == covered == 1行
（K1095 per_root covered_rowsと監査機自身のroot 6石部分幾何の一致）・(2) 主張行がfold23正本残余29行内で
open・(3) intrinsic == 主張 ∪ {`00000000000000003800000008001080`}（K1097正本pinと一致）・
(4) 余剰intrinsic行が (a) K1097でroot `00000000000000003800000008003180` のclaimedに含まれ
(b) fold11正本（SHA-256 `d7bf2cd5…`）のreceipt covered rows 4行に含まれ (c) fold23残余29行外である
3点機械検証。fold11は18番目receiptで当該行を簿計閉鎖済み（残余29行外）であるため、
将来の本rootのreceipt foldの簿計対象は主張1行のみとなる。

## 抽出枯渇の位置づけ

残余29レーンの3候補（K1136・K1137・本抽出）の証明書がすべて出版済みとなり、出版probe pinを持つ
WIN8-D10候補根の証明書抽出は枯渇した。残余29行の縮小には各候補のreceipt fold（fold24候補Aは並走宣言
済み commit `0c9e174e9c`・候補Bは未宣言）が別機材・別単一オーナー宣言で必要であり、本実験は
行を1つも閉じない。

## 解釈規約

本証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold意味論は別工程であり、
行の閉鎖claimは本実験では行わない。REFUTED-D10 は LOSS 証明ではない。
node数・solved数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
