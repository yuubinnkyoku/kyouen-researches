---
id: K1168
title: "fold21 receipt fold（root 80880200）の外部第二検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold21外部第二検証 root 00000000000000801202000800880200"
  - "K1130出版byteの第三実装による値単位再確認"
  - "別実装外部検証機・gate 1394・監査正本 80f00440…"
relations:
  - type: depends_on
    target: K1130
    note: fold21 receipt正本（SHA-256 9a4da2f6…・26,113 bytes）・出版機（44399cc5…・74,529 bytes）・生成機（51158e57…・27,265 bytes）・出版README（6e27c07b…・9,812 bytes）の出版実験dir 4ファイルを検証対象とする。
  - type: depends_on
    target: K1129
    note: fold20 receipt正本（76fd255b…）・fold20出版機（9e141d4a…）。fold21機pristine再実行のrerun gate対象であり、fold20機入力pin（12 blob + 37 SHA-256）の52 pin部分集合性確認の対象。
  - type: depends_on
    target: K1124
    note: K1124証明書本体（eca214f0…・934,278 bytes・25,783行）と19 gate監査正本（422e6109…）。検証機がroot幾何・合法手46・監査19 gate主要値・証明書byte検査を再照合する。
  - type: depends_on
    target: K1097
    note: refsolve記録のwin16_intrinsic_footprints 16根49行exactly-once分割。本検証のwin16候補 6→5根の再導出根拠。
artifacts:
  - path: research/experiments/n11-fold21-external-second-verification-root80880200-20261120/README.md
    role: source
    note: 位置づけ・固定pin・実施内容と結果・再現手順・限界
  - path: research/experiments/n11-fold21-external-second-verification-root80880200-20261120/scripts/reconstruct_inputs.py
    role: verifier
    note: W再構成機（固定Git参照つき・SHA-256 a70b7983…・10,765 bytes・52 pin fail-closed）
  - path: research/experiments/n11-fold21-external-second-verification-root80880200-20261120/scripts/verify_fold21_external_20261120.py
    role: verifier
    note: 第三実装の外部検証機（stdlibのみ・fail-closed・SHA-256 322ad6ca…・50,946 bytes・901行）
  - path: research/experiments/n11-fold21-external-second-verification-root80880200-20261120/output/external-audit.json
    role: verifier
    note: 外部監査正本（all_gates_pass true・gate 1,394・135,723 bytes・SHA-256 80f00440…）
  - path: research/experiments/n11-fold21-external-second-verification-root80880200-20261120/output/reproduction.log
    role: data
    note: 5実行のbyte-identity記録（宣言時HEADとref-B双方のWで同一SHA-256）
  - path: research/log/2026-11-20-n11-fold21-external-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 98c90cb5… 宣言・d323e780… 本文修正・受入条件6項目）
  - path: research/log/2026-11-20-n11-fold21-external-second-verification.md
    role: log
    note: 宣言から出版までの時系列記録
---

# fold21 receipt fold（root 80880200）の外部第二検証

## 対象と範囲

K1130のfold21 receipt fold（root `00000000000000801202000800880200`・残余38行→35行のWIN8-D10 receipt fold・
第28 receipt）に対し、出版社以外の実行主体が別実装の検証機で出版byteを再確認した。単一オーナー宣言
（commit `98c90cb5108be93a607ba5e35c4cd7255f61ebe5`・本文修正commit `d323e780f950d6adea15b8bd7a3309e11d136d55`・
宣言 2026-11-20T21:13:00Z・受入条件6項目）をすべて達成している。fold21実験dirにはfold24方式の
出版社同梱独立監査機がなく、K1167（fold22外部第二検証）もfold21記録をチェーン記録
（fold21 frontier・五親target・残余35行の出発点）として機械照合したのみで、fold21 receipt自身の主張に対する
外部第二検証は本検証が初めてである（宣言ノート記載のとおり・fold23単体ext2 `90ac8eed`・
fold25 ext2 `aad3b71ca`・fold26 `23bffdd4e4`・round-5 refsolve `ace38772d9`・WIN8抽出 `63877ffd2e`・
行共有監査 `c403614f`・fold20単体ext2・K1167 pristine-reexec第三検証（宣言 `53501d73`）は
いずれも他レーン宣言済みのため着手していない）。K番号は3点確認
（README見出し最大K1167・README全文grep K1168=0件・GitHub code searchでK1168先用0件）で取得した。

## 結果

- 検証機 `verify_fold21_external_20261120.py`（SHA-256 `322ad6ca…`・50,946 bytes・901行・stdlibのみ）は第三実装である。
  宣言ノートのとおりK1167検証機（`ca11cbbc…`）の設計を踏襲して対象をfold21に差し替え、本レーンが
  機械的region手術（`build_verifier_stage1.py`）で生成したが、幾何・集計プリミティブ
  （8 D4座標写像・4×4共円行列det4・survival-move規約の合法手再実装・census親対応）は独自実装のままで、
  fold22の検証結果を入力として一切使わず、fold21出版機ともfold20以下の出版チェーン機とも実装を共有しない。
  fail-closed・決定論的出力（時刻フィールドなし・失敗時は監査未書込でexit 1）。
- 出版byte 4点（receipt `9a4da2f6…`・出版機 `44399cc5…`・生成機 `51158e57…`・出版README `6e27c07b…`）と
  上流正本（fold20 receipt `76fd255b…`・fold20機 `9e141d4a…`・K1124証明書 `eca214f0…`・K1124監査 `422e6109…`）の
  SHA-256 pin照合、W再構成52 pin（12 Git blob pin + 40 SHA-256 pin）の再照合、
  fold20機入力pin（12 blob + 37 SHA-256）の52 pin部分集合性・値一致の機械確認、を確認した。
  Wは宣言時HEAD `5e1273f57…` と検証時最新main `d323e780…` の両pinned参照から再構成して全ファイルdiff一致
  （fold21/出力dirを除く）。
- 出版機pristine再実行4回（同一cwd 2回・隔離tree/cwd/HOME・隔離+`PYTHONHASHSEED=random`・
  `FOLD_PREVERIFIED_CHAIN` 不使用・各回fold20機pristine rerun gateとその内部のfold19→fold18系推移的再検証込み・
  1回あたり実測約6〜7秒）は全回receipt出力が出版正本 `9a4da2f6…` とbyte-identical。
- 全chain再導出は出版receiptと値単位で一致: base worklist 6,438行 →
  ledger/globalFold→previousCostFold→firstFold→secondThird→fold4→fold56→fold7/8→ninth-twelfth→
  windfall4（thirteenth-sixteenth）→fold10..fold20に至る全frontier連鎖の独立再計算で
  fold20適用後 open frontier 6,144行/486,819 cost・solved 1,704・incidence 11,701・残余38行・五親target 74/112行
  （fold9 solved 1,635・fs13 solved 1,639等の各段published値と全一致）。
  root 8石・四つ組共円/共線0・D4正準・合法手46（survival-move規約の独立再実装・K1124監査 g05/g09と一致）。
  C(8,6)=28部分幾何のD4正準行を2方法（8 D4像×C(8,2) 2石除去224合成opsと28部分集合正準化）で再導出し
  D4同変性を実測確認、28 canonical行分類 open-frontier 8/not-in-worklist 19/closed-before 1、
  閉鎖8行（五親target内主張3行 + 余剰5行）・closed edge cost 576、
  親delta 7親（class 2/4/6混在・計18 row-closing・80→77・17→14・45→43・81→78・74→72・59→56・48→46）、
  frontier_after 6,136/486,243・solved 1,712・incidence 11,683・needed 4,444/352,691、
  五親target 74→77・残余38→35・win16候補 6→5根（残存主張行12 = 49 − 37）を独立再計算し、
  出版receipt正本の全該当fieldと値単位一致。K1124監査19 gate主要値
  （uncapped probes 618,359/669,067・third-method 46/9,204/[14,18]/57,636/37,121/11,311/52,219・
  証明書934,278 bytes・25,783行sort -u・g01〜g17主要値・extraction nodes 1,670,778/1,383,269）と
  K1097 refsolve footprint 16根49行exactly-onceも再照合した。
- tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 253・K1124証明書 17522の1 byte XOR 0x01・
  出版社未試験位置・W隔離複写上）はいずれもreturncode≠0・`input blob mismatch`/`input sha256 mismatch`・
  出力未書込（rerun gate到達前の入力pin段）でfail-closed捕捉。隔離複写のため本番Wは無改変
  （事後にblob/SHA再照合）。
- gate 1,394全PASS（P pin 13・I入力pin 60・C再導出 1,292・X再実行 15・T tamper 14）。
  監査正本（SHA-256 `80f00440…`・135,723 bytes）は同一cwd 2回＋隔離HOME・別cwd＋`PYTHONHASHSEED=random`＋
  ref-B Wの計5実行でbyte-identical。検証機1実行は実測約27.6秒（user約22.8秒・fold21機6回起動込み）。

実験事実として、(a) 宣言ノートの初回push（`98c90cb5`）に実ファイル内容ではなくプレースホルダ文字列が入り、
55秒後の修正コミット（`d323e780`）で本文を差し替えた（file内容のpush APIへの渡しを正規化しなかった
レーン自身のオペレーションミス・修正後のfetch-backで本文byte一致を確認・宣言時刻は宣言ノート本文の記録どおり
2026-11-20T21:13:00Zで受入条件に影響なし・初回push前の先行宣言なし確認は有効のまま）、
(b) 折り返し時点の進行メモが「win16候補 6→5根（主張16→13行）」と転写していたが、
実receiptの `win_candidate_plan_impact` 主張は残存候補5根・残存主張行12行
（49 − 4-3-3-4-3-4-3-3-4-3-3 = 12）であり、再導出はreceipt記録値と完全一致した
（K1167で実証済みの「要約転写定数は検証機のfail-closed gateで捕捉される」教訓を本検証でも実証:
本検証は全定数を実レコードから読み取り打鍵した）、(c) 28 canonical行のうちclosed-before-this-receiptが
fold21時点で1行存在する: `00000000000000801202000800080000`（cost 72・unswept・
ledger closed_rows_66/globalFold/previousCostFoldのlegacy base段で閉鎖済み）。fold22検証では
closed-before 0だったのと対照的で、covered行open性判定は検証対象receiptの適用時点依存である。

## 限界

本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査であり、行を1行も閉じない。
fold21 receipt自体が8行（主張3＋余剰5）を閉じたのは出版社の成果簿記であり、本項目の成果は
その外部第二検証の成立である（fold21時点残余38→35行はK1130の既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限る証明書であり、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・
class 1/2/4はすべて**UNKNOWN**のまま。
