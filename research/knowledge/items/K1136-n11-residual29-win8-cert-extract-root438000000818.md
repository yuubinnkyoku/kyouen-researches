---
id: K1136
title: 残余29行のWIN8-D10 root 00000000000000043800000008180010 証明書抽出・三重検証（fold24候補A・標準掃引pin基盤）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold24 candidate A cert-extract root 438000000818
  - K1091掃引正本per_root pin基盤のWIN8証明書抽出（fresh probes 882,327/1,054,873 node-exact再現）
  - 残存win16候補3根のうちprobe総nodes最小・主張最小の根の新規証明書
relations:
  - type: depends_on
    target: K1091
    note: replace15-d10-sweep正本（SHA-256 edd7ac84…・output/.input-k1091.json にpin）per_root探査記録（andclose1 882,327・andclose0 1,054,873・両順序 uncapped loss=true・終局石数[14,18]・covered_rows 3行/gained_rows 3）が本実験fresh-probeのnode-exact一致源
  - type: depends_on
    target: K1097
    note: refsolve正本（SHA-256 2896deb0…）win16_intrinsic_footprints で本根は intrinsic == claimed == 3行（g19で機械照合）
  - type: depends_on
    target: K1133
    note: fold23正本（SHA-256 04f334ff…・output/.input-fold23.json にpin）残余29行内で主張3行が全行open（g19）。fold23出版機の輸送打ち切り欠陥（63,938 bytes/894行）は真機（82,697 bytes/1,200行・SHA-256 c908f6c0…）で修復済み（commit ce5361dc・fold24 rerun gateは修復機を用いる）
  - type: depends_on
    target: K1119
    note: 研究log（git blob 51bad3fac…・SHA-256 4d11ca89…）に本根probe総nodes 1,937,200の出版記載（K1091 pinとの二重pin）
  - type: depends_on
    target: K1121
    note: 抽出器（cert_extractor_win8_root08d10000.ts）・Bareiss/BigInt検証器・監査機械の出版系譜。本実験の抽出器はroot引数・filename guard・ヘッダのみ差し替え（探索核同一bytes）
artifacts:
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/README.md
    role: source
    note: 候補選定・標準掃引pin基盤・プロトコル・19 gate構成・結果・解釈上の制限
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/certs/win8-root-00000000000000043800000008180010-20261120.n11
    role: data
    note: 証明書正本（34,843戦略行 + root行 + header行・1,260,393 bytes・SHA-256 dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004）
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/output/win8-cert-extract-verification-20261120.json
    role: verifier
    note: 19/19 gate監査正本（all_gates_pass・3実行byte-identical・SHA-256 d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c）
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/scripts/cert_extractor_win8_root00000000000000043800000008180010.ts
    role: verifier
    note: K1121出版抽出器の根差し替え版（fbt_drops 0・recordRow衝突拒否込み・A1/A2/B 3実行で行集合byte-identical）
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/scripts/assemble_win8_audit_root438000000818.py
    role: verifier
    note: K1121監査機械の適応版（root定数・probe定数・bit 16→4・g19 fold23残余29行open拡張・第三実装全木再走査は同一ロジック）
  - path: research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/runner_v17.ts
    role: source
    note: runner v17 repo原本固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・g03で照合）
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000043800000008180010.md
    role: log
    note: 選定・宣言・実行・三重検証・出版（part1 b07375a9・part2 a6fe34e3・part3 25170449・採番K1136）の研究記録
  - path: research/log/2026-11-20-n11-win8-cert-extract-root00000000000000043800000008180010-single-owner-note.md
    role: log
    note: 単一オーナー宣言（先行出版 commit 811c2423・採番規則とK番号二重採番衝突の記録を含む）
---

# 残余29行のWIN8-D10 root 00000000000000043800000008180010 証明書抽出・三重検証（fold24候補A）

fold23（K1133）出版後の残余29行に対する新規掃引設計の第1着手として、残存win16候補3根のうち
probe総nodes最小（1,937,200）かつ主張最小（3行）の根
`00000000000000043800000008180010`（石[4,19,20,27,59,60,61,66]・mobility 50）の
完全勝利戦略証明書を盲抽出・三重独立検証した。**標準掃引pin基盤**（K1091正本per_root pinを
fresh-probe両順序×2回でnode-exact再現）。

## 主要結果

- **証明書**: 34,843戦略行 + root行 + header行・1,260,393 bytes・行は昇順一意。
  SHA-256 `dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004`。
- **fresh-probe（K1091 pin再現）**: bit 4（root − 最小セットビット）child
  `00000000000000043800000008180000` + bit 4・depth-10・cap 4,000,000・両AND順序×2回で
  andclose1 882,327 / andclose0 1,054,873（合計 1,937,200）・両順序 uncapped loss=true・
  終局石数 [14,18]・pilot_d6 制御 4/4（nodes 3,402）がK1091掃引正本per_root pinとnode-exact一致。
- **抽出3実行**: A1 = 初手ごと新規プロセス50本（総nodes 3,539,166・最大初手 move 3 の 349,453・
  fbt_drops 0）・A2 = A1完全再実行（初手単位node-exact一致）・B = 単一プロセス一括（2,564,865・
  K1121と同型の一括メモ会計削減）。**3実行とも証明書行集合byte-identical**。
- **三重独立検証の全数値一致**: BigInt 3x3余因子 / Bareiss 4x4整数行列式 / Python第三実装全木再走査の
  3方法で visited 77,154・winner-to-move 49,599・loser-to-move 14,382・loser応手辺 67,581・
  終端 13,173（全loser-stuck）・終端石数 [14,18]・consumed union == 34,843 == 証明書行
  （missing 0 / extra 0）・Bareiss 50 subroot が完全一致。
- **19/19 gate監査**: g01 K1091正本SHA-256 pin・g02 runner v17 git blob pin・g03 固定コピーblob一致・
  g04 root shape safe（8石・quadruple-free）・g05 mobility 50・g06 K1091 per_root probes
  uncapped loss=true〔882,327/1,054,873〕・g07 covered_rows 3行・g08 fresh-probe再現 bit 4
  node-exact（pilot 4・各順序2回）・g09 初手リスト==独立再導出・g10/g11/g12 抽出3実行clean・
  g13 node会計（A1 3,539,166 vs B 2,564,865）・g14 証明書format sorted-unique・g15 B nRows一致・
  g16 第三方法全木再走査PASS・g17 三方法集計一致・g18 解釈guard文言・
  **g19 K1097 footprint intrinsic == claimed == 3行 + fold23正本pin（04f334ff…）+
  残余29行内で主張3行全行open**。正本は同一cwd 2回 + 隔離複写・別cwd別HOME 1回の3実行で
  byte-identical（SHA-256 `d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c`）。
- 主張3行 `00000000000000003800000008002040`（cost 66）・`00000000000000043800000008080000`（cost 75）・
  `00000000000000043800000008100000`（cost 84）はfold23残余29行内でopen（閉鎖edge cost 225・余剰なし）。

## fold24に向けて

本証明書のreceipt fold（fold24・残余29→26予定）は別機材・別単一オーナー宣言の工程であり、
本実験では行を1つも閉じない。fold24機はfold23出版正本（04f334ff…）と修復済みfold23出版機
（SHA-256 c908f6c0…・commit ce5361dc）をchain入力に追加して生成する。

## 採番注記

本実験のエントリはK1136。2026-11-20 08:21-08:29にK1133の二重採番衝突（fold23 laneとvertical-fiber lane）が
発生し、本レーン宣言ノート（commit 811c2423）が first-published-priority 規則と衝突検出を先行出版した結果、
vertical-fiber laneは自らの項目をK1135に再番号した（n6q8 laneがK1134を採番済みのため本実験はK1136）。

## 解釈規約

本証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold意味論は別工程であり、
行の閉鎖claimは本実験では行わない。REFUTED-D10 は LOSS 証明ではない。
node数・solved数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
