---
id: K1173
title: "fold20 receipt fold（root 08d10000）の外部第二検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold20外部第二検証 root 00000000000000003800000008d10000"
  - "K1129出版byteの第三実装による値単位再確認"
  - "別実装外部検証機・gate 1317・監査正本 5a9bb98f…"
relations:
  - type: depends_on
    target: K1129
    note: fold20 receipt正本（SHA-256 76fd255b…・24,684 bytes）・出版機（9e141d4a…・70,951 bytes）・生成機（4ba91cd0…・36,412 bytes）・出版README（637841d2…・9,056 bytes）の出版実験dir 4ファイルを検証対象とする。
  - type: depends_on
    target: K1121
    note: K1121証明書本体（8513e366…・1,026,202 bytes・28,328行）と19 gate監査正本（0088ebab…）。検証機がroot幾何・合法手50・監査19 gate主要値・証明書byte検査を再照合する。
  - type: depends_on
    target: K1097
    note: refsolve記録のwin16_intrinsic_footprints 16根49行exactly-once分割。本検証のwin16候補 7→6根の再導出根拠。
artifacts:
  - path: research/experiments/n11-fold20-external-second-verification-root08d10000-20261120/README.md
    role: source
    note: 位置づけ・固定pin・実施内容と結果・再現手順・限界
  - path: research/experiments/n11-fold20-external-second-verification-root08d10000-20261120/scripts/reconstruct_fold20_inputs.py
    role: verifier
    note: W再構成機（固定Git参照つき・SHA-256 bf21d042…・10,168 bytes・49 pin fail-closed）
  - path: research/experiments/n11-fold20-external-second-verification-root08d10000-20261120/scripts/verify_fold20_external_20261120.py
    role: verifier
    note: 第三実装の外部検証機（stdlibのみ・fail-closed・SHA-256 30877bef…・52,131 bytes・913行）
  - path: research/experiments/n11-fold20-external-second-verification-root08d10000-20261120/output/external-audit.json
    role: verifier
    note: 外部監査正本（all_gates_pass true・gate 1,317・128,175 bytes・SHA-256 5a9bb98f…）
  - path: research/experiments/n11-fold20-external-second-verification-root08d10000-20261120/output/reproduction.log
    role: data
    note: 再構成2参照・pristine再実行4回・検証機3実行のbyte-identity記録
  - path: research/log/2026-11-20-n11-fold20-external-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 5f6c1b7a…・宣言 2026-11-20T23:09:08Z・受入条件6項目）
  - path: research/log/2026-11-20-n11-fold20-external-second-verification.md
    role: log
    note: 宣言から出版までの時系列記録

---

# fold20 receipt fold（root 08d10000）の外部第二検証

## 対象と範囲

K1129のfold20 receipt fold（root `00000000000000003800000008d10000`・残余41行→38行のWIN8-D10 receipt fold・
第27 receipt・10番目のWIN8 receipt fold）に対し、出版社以外の実行主体が別実装の検証機で出版byteを再確認した。
単一オーナー宣言（commit `5f6c1b7a910e695349ad497cde309d3042d4636a`・宣言 2026-11-20T23:09:08Z・
push直前main HEAD `ec24b235f806822086680fee4075820679c78acf`・受入条件6項目）をすべて達成している。
fold20実験dirにはfold24方式の出版社同梱独立監査機がなく、K1167（fold22外部第二検証）・
K1168（fold21外部第二検証）もfold20記録をチェーン記録として機械照合しfold20機をrerun gateで再実行したのみで、
fold20 receipt自身の主張に対する外部第二検証は本検証が初めてである（宣言ノート記載のとおり・
fold18 ext2 `c2e8eb09f`・fold19 ext2 `9606203ae`・fold23 ext2 `90ac8eed`・fold25 ext2 `aad3b71ca`・
fold26（所有者宣言 e53cc60c/ba659878）・K1166第三検証 `ec24b235` はいずれも他レーン宣言済みのため着手していない）。
K番号はREADME見出し最大K1172・README全文grep K1173=0件・直近コミット列挙でK1173先用0件を
push直前に確認して取得した。

## 結果

- 検証機 `verify_fold20_external_20261120.py`（SHA-256 `30877bef…`・52,131 bytes・913行・stdlibのみ）は第三実装である。
  宣言ノートのとおりK1168検証機（fold21外部検証機）の設計を踏襲して対象をfold20に差し替え、本レーンが
  機械的region手術で生成したが、幾何・集計プリミティブ（8 D4座標写像・4×4共円行列det4・
  survival-move規約の合法手再実装・census親対応）は独自実装のままで、fold21/fold22の検証結果を入力として
  一切使わず、fold20出版機ともfold19以下の出版チェーン機とも実装を共有しない。
  fail-closed・決定論的出力（時刻フィールドなし・失敗時は監査未書込でexit 1）。
- 出版byte 4点（receipt `76fd255b…`・出版機 `9e141d4a…`・生成機 `4ba91cd0…`・出版README `637841d2…`）と
  上流正本（fold19 receipt `c02d9a54…`・fold19機 `51442d96…`・K1121証明書 `8513e366…`
  （1,026,202 bytes・28,328行）・K1121監査 `0088ebab…`・K1091掃引正本 `edd7ac84…`）のSHA-256 pin照合、
  W再構成49 pin（12 Git blob pin + 37 SHA-256 pin）の再照合、fold19機入力pin（12 blob + 34 SHA-256）の
  49 pin部分集合性・値一致の機械確認、を確認した。Wは宣言時HEAD `ec24b235…` と検証時最新main
  `299264789…` の両pinned参照から再構成して全ファイルdiff一致（W20のfold20出力dirを除く）。
- 出版機pristine再実行4回（同一cwd 2回・隔離tree/cwd/HOME・隔離+`PYTHONHASHSEED=random`・
  `FOLD_PREVERIFIED_CHAIN` 不使用・各回fold19機pristine rerun gateとfold18 preverified・K1120 gate群の
  推移的再検証込み・単独実行は実測約4.7〜4.8秒）は全回receipt出力が出版正本 `76fd255b…` とbyte-identical。
- 全chain再導出は出版receiptと値単位で一致: base worklist 6,438行 →
  ledger/globalFold→previousCostFold→firstFold→secondThird→fold4→fold56→fold7/8→ninth-twelfth→
  windfall4（thirteenth-sixteenth）→fold10..fold19（16段のchain再計算）で
  fold19適用後 open frontier 6,152行/487,418 cost・solved 1,696・incidence 11,711・残余41行・
  五親target 71/112行（fold9 solved 1,635・fs13 solved 1,639等の各段published値と全一致）。
  root 8石 [16,20,22,23,27,59,60,61]・四つ組共円/共線0・D4正準・合法手50（survival-move規約の独立再実装・
  K1121監査 g05/g11/g12と一致）。C(8,6)=28部分幾何のD4正準行を2方法（8 D4像×C(8,2) 2石除去224合成opsと
  28部分集合正準化）で再導出しD4同変性を実測確認、28 canonical行分類 open-frontier 8/not-in-worklist 20/
  closed-before 0、閉鎖8行（五親target内主張3行〔cost 74/75/76〕+ 余剰5行〔cost 80/83/70/72/69〕）・
  closed edge cost 599・親delta 4親（class 4: 79→77〔2行〕・80→78〔2行〕・class 2: 12→9〔3行〕・40→37〔3行〕・
  計10 row-closing・完全閉鎖0親）、frontier_after 6,144/486,819・solved 1,704・incidence 11,701・
  needed 4,452/353,267・五親target 71→74・残余41→38・win16候補 7→6根
  （1根retire・retired_root_predecessor `00000000000000801212000001009000`・残存主張行15 = 49 − 4-3-3-4-3-4-3-3-4-3）を
  独立再計算し、出版receipt正本の全該当fieldと値単位一致。K1121監査19 gate主要値
  （g01 K1091 master pin・g02==g03 c132cc64…・g06 564,695/673,870・g13 2,428,240/1,748,509・
  g14 1,026,202 bytes/28,328行・g15 28,328・g17 bareiss 50/15,513・
  third-method 15,513/83,544/53,570/14,461/72,930・terminal石数 [14,18]・g19 K1097 record sha 2896deb0…）と
  K1097 refsolve 27 gate・footprint 16根49行exactly-once・intrinsic==claimed・residual23不交差も再照合した。
- tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 5077・K1121証明書本体 28081の1 byte XOR 0x01・
  出版社未試験位置・W隔離複写上）はいずれもreturncode≠0・`input blob mismatch`/`input sha256 mismatch`・
  出力未書込でfail-closed捕捉。隔離複写のため本番Wは無改変（事後にblob/SHA再照合）。
- gate 1,317全PASS（P pin 13・I入力pin 60・C再導出 1,215・X再実行 15・T tamper 14）。
  監査正本（SHA-256 `5a9bb98f…`・128,175 bytes）は同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`の
  3実行でbyte-identical。検証機1実行は実測約21秒（fold20機6回起動込み）。

実験事実として、(a) 検証機のregion手術中にC1末尾ブロック（post-fold19 residual 41の検証: W内fold19記録SHA照合・
frontier全再計算・receipt previous_fold照合）が消えており、初回実行の `NameError`（fa19）で発見、
アンカーspliceで本来位置に再挿入して修復した（splice後の挿入text実在のgrep確認を必須とする運用教訓）、
(b) 復旧したgateは初め `receipt previous_fold record ref ends with fold19 sha` で失敗した: receiptの
previous_fold.record文字列は「(sha256 c02d9a54…)」で終わるため、同じfold19記録SHAをそのまま照合する
containment判定に修正した（受入条件の実質は不変・fail-closedのまま）、
(c) part1出版の初回pushで監査正本JSONが輸送層の読み取りcap（63,999文字）で打ち切られ、
fetch-back byte検証が即捕捉した。30,000 bytes分割の部品結合で全128,175 bytesを復元し
（結合体のFNV-1a 32照合 1222417471つき）、修正コミット `cf453602` で全文を反映、
fetch-back 5/5 byte一致を確認した（K1166/K1172レーンのstatus-string混入事故と同じ教訓:
pushはfetch-back byte検証を通るまで完了扱いにしない）。

## 限界

本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査であり、行を1行も閉じない。
fold20 receipt自体が8行（主張3＋余剰5）を閉じたのは出版社の成果簿記であり、本項目の成果は
その外部第二検証の成立である（fold20時点残余41→38行はK1129の既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限る証明書であり、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
