---
id: K1167
title: "fold22 receipt fold（root 840500）の外部第二検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold22外部第二検証 root 00000000000000801202000000840500"
  - "K1132出版byteの第三実装による値単位再確認"
  - "別実装外部検証機・gate 1463・監査正本 b4b082f8…"
relations:
  - type: depends_on
    target: K1132
    note: fold22 receipt fold正本（SHA-256 f6e011f4…）・出版機（d5721408…）・生成機（a73995be…）・出版README（0e6861bf…）の出版実験dir 4ファイルを検証対象とする。
  - type: depends_on
    target: K1130
    note: fold21 receipt正本（9a4da2f6…）・fold21出版機（44399cc5…）。出版機pristine再実行のrerun gate対象であり、W pinの部分集合確認機械対象。
  - type: depends_on
    target: K1125
    note: K1125証明書本体（21ad6195…・1,067,425 bytes・29,468行）と19 gate監査正本（06c65f76…）。検証機が主要gate値・third-method統計・証明書byte検査を再照合する。
  - type: depends_on
    target: K1097
    note: refsolve記録（2896deb0…）のwin16_intrinsic_footprints 16根49行exactly-once分割・residual23。本検証のwin16候補 5→4根の再導出根拠。
artifacts:
  - path: research/experiments/n11-fold22-external-second-verification-root840500-20261120/README.md
    role: source
    note: 位置づけ・固定pin・実施内容と結果・再現手順・限界
  - path: research/experiments/n11-fold22-external-second-verification-root840500-20261120/scripts/reconstruct_inputs.py
    role: verifier
    note: W再構成機（固定Git参照つき・SHA-256 dfa50996…・10,102 bytes）
  - path: research/experiments/n11-fold22-external-second-verification-root840500-20261120/scripts/verify_fold22_external_20261120.py
    role: verifier
    note: 第三実装の外部検証機（stdlibのみ・fail-closed・SHA-256 ca11cbbc…・48,949 bytes）
  - path: research/experiments/n11-fold22-external-second-verification-root840500-20261120/output/external-audit.json
    role: verifier
    note: 外部監査正本（all_gates_pass true・gate 1,463・141,752 bytes・SHA-256 b4b082f8…）
  - path: research/experiments/n11-fold22-external-second-verification-root840500-20261120/output/reproduction.log
    role: data
    note: 4実行のbyte-identity記録（ref-A/ref-B双方のWで同一SHA-256）
  - path: research/log/2026-11-20-n11-fold22-external-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 01c0855fd935b1951d686294efbb9305a3e4f4d8）・受入条件6項目
  - path: research/log/2026-11-20-n11-fold22-external-second-verification.md
    role: log
    note: 宣言から出版までの時系列記録
---

# fold22 receipt fold（root 840500）の外部第二検証

## 対象と範囲

K1132のfold22 receipt fold（残余35行→32行のWIN8-D10 receipt fold）に対し、出版社以外の実行主体が
別実装の検証機で出版byteを再確認した。単一オーナー宣言
（commit `01c0855fd935b1951d686294efbb9305a3e4f4d8`・2026-11-20T20:46:23Z，受入条件6項目）を
すべて達成している。fold21単体の外部第二検証・fold23外部第二検証（`90ac8eed`所有）・
fold25外部第二検証（`aad3b71ca`所有）・fold26 receipt fold・round-5 refsolve・WIN8-D10候補
`00000000010000809002000040002001` の証明書抽出は宣言どおり着手していない。
K番号は3点確認（README見出し最大K1166・README全文grep・GitHub code searchでK1167の先用を確認）で取得した。

## 結果

- 検証機はstdlibのみの第三実装で、fold22出版機・fold21以下の出版チェーン機と実装を共有しない。
  fail-closed・決定論的出力（時刻フィールドなし）。
- 出版byte 4点（receipt `f6e011f4…`・出版機 `d5721408…`・生成機 `a73995be…`・README `0e6861bf…`）と
  上流正本（fold21 record `9a4da2f6…`・fold21機 `44399cc5…`・K1125証明書 `21ad6195…`・K1125監査 `06c65f76…`）の
  SHA-256 pin照合、W再構成55 pin（12 Git blob + 43 SHA-256）の再照合、
  fold21 chain入力の55 pin部分集合性の機械確認、を確認した。
- 出版機pristine再実行4回（同一cwd 2回・隔離tree/cwd/HOME・隔離+`PYTHONHASHSEED=random`・
  `FOLD_PREVERIFIED_CHAIN` 不使用・各回fold21機pristine rerun gate込み）は全回receipt byte-identical。
- 全chain再導出は出版receiptと値単位で一致: base 6,438行（総cost 509,109）→globalFold base→
  21記録適用段→fold21 frontier 6,136/486,243・solved 1,712・incidence 11,683・残余35・五親target 77/112。
  root 8石・四つ組共円/共線0・D4正準・合法手58（survival-move規約の独立再実装）。
  C(8,6)=28部分幾何のD4正準行を2方法（8 D4像×C(8,2) 2石除去224合成opsと28部分集合正準化）で再導出し
  28 canonical行分類 open 6/not-in-worklist 22/closed-before 0、主張3行＋余剰3行の6行閉鎖・
  closed edge cost 484、親delta 4親class 2（14→11・51→48・47→44・69→66・計12）、
  frontier_after 6,130/485,759・solved 1,718・incidence 11,671・needed 4,438/352,207、
  五親target 77→80・残余35→32、win16候補 5→4根（主張12→9行）。K1125監査19 gate主要値・
  K1097 footprint 16根49行exactly-once・residual23非接触も再照合。
- tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 1099・K1125証明書 21212の1 byte XOR 0x01）は
  いずれもreturncode≠0・`input blob mismatch`/`input sha256 mismatch`・出力未書込でfail-closed捕捉。
- gate 1,463全PASS（P pin 13・I入力pin 63・C再導出 1358・X再実行 15・T tamper 14）。
  監査正本（SHA-256 `b4b082f8…`・141,752 bytes）は同一cwd 2回＋隔離HOME・別cwd・`PYTHONHASHSEED=random` の
  3実行byte-identical。さらに宣言時HEAD `9a1c7a98…` と最新main `34c29854…` の双方から再構成したWでも
  同一SHA-256を確認（最終版で計4実行byte一致・W/pub全ファイル2参照間diff一致）。

実験事実として、検証機初版のfold14/fold15/fold19 covered_n打鍵定数に要約経由の転写誤り
（3/2/9→正5/6/5）があり、検証機自身のfail-closed gate（covered行数・frontier solved増分照合）が
実行1回目で即捕捉した（K1158・K1160・K1164のpin転写typoと同じ防御パターンが要約転写定数にも有効）。
またfold22 receiptのwin16候補note列挙文がfold18 retired root（`00901010`・3主張行）を本文から落としているが、
noteの数列 `49-4-3-3-4-3-4-3-3-4-3-3-3 = 9` はfold18 retire込みの12 retire計40行を正しく加算しており、
再導出はreceipt数値と完全一致した（列挙漏れは表現上の省略で数値への影響なし、を機械確認）。

## 限界

本検証はreceipt簿記の再検査であり、行を1行も閉じない。fold22 receiptが6行（主張3＋余剰3）を閉じたのは
出版社の成果簿記で、本項目の成果はその外部第二検証の成立である。WIN8-D10は当該8石rootの
ゲーム木に限る証明書であり、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
