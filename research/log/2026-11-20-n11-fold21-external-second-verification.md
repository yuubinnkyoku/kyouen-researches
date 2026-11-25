# fold21 receipt fold（K1130）の外部第二検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T21:13:00Z）**: fold21外部第二検証の単一オーナー宣言ノートを
  [単一オーナー宣言ノート](2026-11-20-n11-fold21-external-second-verification-single-owner-note.md)
  として先に出版した。宣言時点のmain HEADは `5e1273f57c8c7733f0f2ba14a44000c2f5df0554` で、
  fold21単体の外部第二検証の先行宣言なし（fold23宣言ノート `90ac8eed` が「fold21単体は別途宣言する」と
  予告していたが、その時点ではfold21単体の宣言は存在せず、first-published-priorityにより本レーンが取得）。
  受入条件は6項目を定めた（出版byte pin照合・W再構成52 pin・pristine再実行4回・
  別実装による全統計再導出・tamper 2件fail-closed・監査正本複数実行byte-identical）。
- **初回push事故と修復**: 宣言ノートの初回push（commit `98c90cb5108be93a607ba5e35c4cd7255f61ebe5`）に
  実ファイル内容ではなくプレースホルダ文字列が入り、55秒後の修正コミット
  （`d323e780f950d6adea15b8bd7a3309e11d136d55`・21:13:56Z）で本文を差し替えた。
  原因はfile内容のpush APIへの渡しを正規化しなかった本レーン自身のオペレーションミス。
  修正後のfetch-backで本文byte一致を確認し、宣言時刻（宣言ノート本文記録の2026-11-20T21:13:00Z）と
  受入条件6項目に影響しない。初回push前に実施した先行宣言なし・衝突なしの確認は
  失敗に依存しないため有効のまま（実験事実として当該READMEに記録済み）。
- **出版byte pin照合**: fold21出版実験dir（`n11-residual35-win8-receipt-fold-root80880200-20261120/`）の
  receipt `9a4da2f6…`・出版機 `44399cc5…`・生成機 `51158e57…`・README `6e27c07b…` の4点と、
  上流のfold20 receipt `76fd255b…`・fold20機 `9e141d4a…`・K1124証明書 `eca214f0…`（934,278 bytes・25,783行）・
  K1124監査 `422e6109…` をGitHubのpinned commitから取得してSHA-256照合した。
- **W再構成**: 本レーン定義の `reconstruct_inputs.py`（SHA-256 `a70b7983…`・10,765 bytes）を宣言時HEAD
  `5e1273f57…` で実行し、fold21機の入力52 pin（12 Git blob pin + 40 SHA-256 pin）をfail-closed再照合、
  rerun gate用にfold20出版機・fold18/19出版機・fold18 preverified写しをSHA照合つきで配置した
  （fold20機の入力pin〔12 blob + 37 SHA-256〕の52 pin部分集合性・値一致はreconstruct機と検証機の
  両方が機械確認）。
- **手動確認段階**: 出版機をpristine実行（`FOLD_PREVERIFIED_CHAIN` 不使用・実測約6〜7秒）し、
  receipt出力が出版正本 `9a4da2f6…` とbyte一致することを最初に確認した。
- **検証機生成**: 上記を一括する第三実装の外部検証機 `verify_fold21_external_20261120.py`
  （SHA-256 `322ad6ca…`・50,946 bytes・901行・stdlibのみ）を、K1167検証機（fold22外部検証機・
  出版byte `ca11cbbc…`）を対象fold21に機械的region手術（`build_verifier_stage1.py`）で差し替えて生成した。
  D4座標変換（明示的8写像）・det4余因子展開・survival-move規約の合法手再実装（石3点組と
  共円/共線 det4==0 の空点をblockedとする）・親対応・frontier統計・五親target連鎖・
  win16 footprint再照合は出版機と実装を共有せず、fold22の検証結果も入力としていない。
- **全受理条件の成立**: gate 1,394全PASS（P 13・I 60・C 1,292・X 15・T 14）。
  tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 253・K1124証明書 17522の1 byte XOR 0x01）は
  returncode≠0・`input blob mismatch`/`input sha256 mismatch`・出力未書込（rerun gate到達前の入力pin段）で捕捉。
- **決定論性・参照独立性**: 監査正本 `80f00440…`（135,723 bytes）は同一cwd 2回＋隔離HOME・別cwd＋
  `PYTHONHASHSEED=random`＋ref-B W（最新main `d323e780…` から再構成）の計5実行でbyte-identical。
  W/pubは宣言時HEAD `5e1273f57…` と検証時最新main `d323e780…` の2参照間で全ファイルdiff一致
  （W21の`fold21/`出力dirを除く）。検証機1実行は実測約27.6秒（user約22.8秒・fold21機6回起動込み）。
- **出版（part1）**: 実験dir 5ファイル（README・reconstruct機・検証機・監査正本・reproduction.log）を
  単一コミット `3716fdbcdd595a3a577239adbb5e229263040b4b`（21:30:27Z）でmainへ直接反映し、
  fetch-back 5/5 byte-identical（audit `80f00440…`・verify `322ad6ca…`・reconstruct `a70b7983…` の
  SHA一致とREADME/logの内容一致）を確認した。

## 結果

- fold21 receipt（K1130）の全数値主張が、出版社と実装を共有しない第三実装の検証機によって
  出版byteだけから再導出され、値単位で一致した。fold21 receipt自体が8行（主張3＋余剰5）を閉じたのは
  出版社の成果簿記であり、本項の成果はその外部第二検証の成立である
  （残余38→35・五親target 74→77・frontier_after 6,136/486,243・solved 1,712・
  win16候補 6→5根・残存主張行12行の全主張再現）。
- 実験事実として、(a) 折り返し時点の進行メモが「win16候補 6→5根（主張16→13行）」と転写していたが、
  実receiptの主張は残存候補5根・残存主張行12行（49 − 4-3-3-4-3-4-3-3-4-3-3 = 12）であり、
  再導出はreceipt記録値と完全一致した（本検証は全定数を実レコードから読み取り打鍵し、
  K1167で実証した「要約転写定数はfail-closed gateで捕捉される」防御構造が本検証でも有効）、
  (b) 28 canonical行のうちclosed-before-this-receiptがfold21時点で1行存在する
  （`00000000000000801202000800080000`・cost 72・unswept・legacy base段で閉鎖済み）。
  fold22検証ではclosed-before 0だったのと対照的で、covered行open性判定が検証対象receiptの
  適用時点依存であることを確認した。

## 限界

行は1行も閉じない（fold21時点の残余38→35行は出版社の既出版簿記であり、本検証は追加の行を閉じない・
pool 120,416根は不変）。本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査である。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
