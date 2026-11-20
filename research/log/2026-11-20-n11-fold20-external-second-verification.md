# fold20 receipt fold（K1129）の外部第二検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T23:09:08Z）**: fold20外部第二検証の単一オーナー宣言ノートを
  [単一オーナー宣言ノート](2026-11-20-n11-fold20-external-second-verification-single-owner-note.md)
  として先に出版した。宣言時点のmain HEADは `ec24b235f806822086680fee4075820679c78acf` で、
  fold20単体の外部第二検証の先行宣言なし（fold21=K1168完了・fold22=K1167完了→K1170第三検証完了
  〔いずれも当レーン〕・fold18 `c2e8eb09f`・fold19 `9606203ae`・fold23 `90ac8eed`・fold25 `aad3b71ca`・
  K1166第三検証 `ec24b235`〔いずれも他レーン〕は対象外、fold18/fold19宣言ノートの「他レーン予定含み」
  言及は宣言ではなく、fold21単体ext2がfold23宣言ノートの予告に対してfirst-published-priorityを
  取得した前例と同じ扱い）。
  受入条件は6項目を定めた（出版byte pin照合・W再構成49 pin・pristine再実行4回・
  別実装による全統計再導出・tamper 2件fail-closed・監査正本3実行byte-identical）。
  push後のfetch-backで本文byte一致（10,140 bytes・SHA-256 `03e07ceaa…`・プレースホルダ0件）を確認した。
- **出版byte pin照合とW再構成**: fold20出版実験dir（`n11-residual38-win8-receipt-fold-root08d10000-20261120/`）の
  receipt `76fd255b…`（24,684 bytes）・出版機 `9e141d4a…`（70,951 bytes）・生成機 `4ba91cd0…`
  （36,412 bytes）・README `637841d2…`（9,056 bytes）の4点と、上流のfold19 receipt `c02d9a54…`
  （22,898 bytes）・fold19機 `51442d96…`（68,386 bytes）・K1121証明書 `8513e366…`
  （1,026,202 bytes・28,328行）・K1121監査 `0088ebab…`・K1091掃引正本 `edd7ac84…` を
  pinned commitから取得してSHA-256照合した。本レーン定義の `reconstruct_fold20_inputs.py`
  （SHA-256 `bf21d042…`・10,168 bytes・204行）を宣言時HEAD `ec24b235…` で実行し、
  fold20機の入力49 pin（12 Git blob pin + 37 SHA-256 pin）をfail-closed再照合、
  rerun gate用にfold19機・fold18機（`dcdfbf92…`）・fold18 preverified写し（`d342f1f8…`）を
  SHA照合つきで配置、W rootにfold20機自体をSHA照合つきで配置した
  （fold19機の入力pin表〔12 blob + 34 SHA-256〕の49 pin部分集合性・値一致はreconstruct機と検証機の両方が
  機械確認・実行は実測約18.5秒）。
- **手動確認段階**: 出版機をpristine実行（`FOLD_PREVERIFIED_CHAIN` 不使用・同一cwd 2回が実測約4.8秒・
  隔離copytree W/cwd/HOME 2回〔うち1回は `PYTHONHASHSEED=random`〕が約4.7秒）し、
  4回ともreceipt出力が出版正本 `76fd255b…` とbyte一致することを最初に確認した
  （各回はfold19機pristine rerun gateとfold18 preverified・K1120 gate群の推移的再検証込み・
  GATE FAILED 0）。
- **検証機生成**: 上記を一括する第三実装の外部検証機 `verify_fold20_external_20261120.py`
  （SHA-256 `30877bef…`・52,131 bytes・913行・stdlibのみ）を、K1168検証機（fold21外部検証機・
  `verify_fold21_external_20261120.py`）を対象fold20に機械的region手術で差し替えて生成した。
  D4座標変換（明示的8写像）・det4余因子展開・survival-move規約の合法手再実装・親対応・frontier統計・
  五親target連鎖・win16 footprint再照合は出版機と実装を共有せず、fold21/22の検証結果も入力としていない。
- **手術中の事故2件**: (a) region手術の過程でC1末尾ブロック（post-fold19 residual 41の検証: W内fold19記録の
  SHA照合・frontier全再計算・receipt previous_fold照合）が消えており、初回実行時に `NameError`（fa19）として
  発見した。fold19 chain_step直後にアンカーspliceで再挿入して修復した。
  (b) 再挿入したgateは初め `endswith` 判定で失敗した（receiptのprevious_fold.record文字列は
  「(sha256 c02d9a54…)」で終わる）。同じfold19記録SHAを照合するcontainment判定に修正した
  （受入条件の実質は不変・fail-closedのまま）。
- **全受理条件の成立**: gate 1,317全PASS（P 13・I 60・C 1,215・X 15・T 14）。
  tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 5077・K1121証明書本体 28081の
  1 byte XOR 0x01・出版社未試験位置）はreturncode≠0・`input blob mismatch`/`input sha256 mismatch`・
  出力未書込で捕捉（W隔離複写上のため本番W無改変・事後再照合）。
- **決定論性・参照独立性**: 監査正本（SHA-256 `5a9bb98f…`・128,175 bytes）は同一cwd 2回＋
  隔離cwd/HOME＋`PYTHONHASHSEED=random`の3実行でbyte-identical（実測約21.4秒・21.1秒・約21秒・
  各実行にfold20機6回起動込み）。W/pubは宣言時HEAD `ec24b235…` と検証時最新main `299264789…` の
  2参照から再構成して全ファイルdiff一致（W20のfold20出力dirを除く・2回目の再構成は実測約14.8秒）。
- **出版（part1）**: 実験dir 5ファイル（README・reconstruct機・検証機・監査正本・reproduction.log）を
  commit `f22139821931181154b698c94c60bca21acde304` でmainへ直接反映した。fetch-backで
  監査正本JSONのみが63,999 bytesで打ち切られていることを検出（輸送層read cap・他4ファイルはbyte一致）。
  30,000 bytesへのbyte分割・結合（結合体FNV-1a 32照合 1222417471）で128,175 bytes全文を組み直し、
  修正コミット `cf45360245f66489c8364ac16df7eda0fc01e22e` で反映、fetch-back 5/5 byte-identicalを確認した。

## 結果

- fold20 receipt（K1129）の全数値主張が、出版社と実装を共有しない第三実装の検証機によって
  出版byteだけから再導出され、値単位で一致した。fold20 receipt自体が8行（主張3〔cost 74/75/76〕＋
  余剰5〔cost 80/83/70/72/69〕）を閉じたのは出版社の成果簿記であり、本項の成果はその外部第二検証の成立である
  （残余41→38・五親target 71→74・frontier_after 6,144/486,819・solved 1,704・incidence 11,701・
  needed 4,452/353,267・closed edge cost 599・親delta 4親10 row-closing・win16候補 7→6根・
  残存主張行15行の全主張再現）。
- 実験事実として、(a) 検証機region手術でC1末尾ブロックが消失し実行時NameErrorとして検出・修復した
  （splice後のgrep実在確認を必須とする教訓）、(b) previous_fold照合はreceiptのrecord文字列形式を
  見たbyteレベルの判定ミスをfail-closed gateが第一次実行で正確に捕捉し、
  containment判定に修正して全gate通過（受入条件不変）、(c) part1初回pushの監査JSON打ち切りを
  fetch-back byte検証が捕捉し、分割結合+修正コミットで全文復元（pushはfetch-back通過まで完了扱いにしない
  運用の有効性を再実証）。

## 限界

行は1行も閉じない（fold20時点の残余41→38行は出版社の既出版簿記であり、本検証は追加の行を閉じない・
pool 120,416根は不変）。本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査である。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
