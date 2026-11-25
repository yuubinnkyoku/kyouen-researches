# fold21（K1130）外部第二検証: 別実装検証機による出版byte再確認（2026-11-20）

## 位置づけ

K1130のfold21 receipt fold（root `00000000000000801202000800880200`・残余38行→35行のWIN8-D10 receipt fold・
twenty-eighth receipt）は、Publisherレーンが実験dir
`n11-residual35-win8-receipt-fold-root80880200-20261120/`
（receipt `9a4da2f6…`・機 `44399cc5…`・生成機 `51158e57…`・README `6e27c07b…`）として出版した時点で、
複数回実行・fold20出版機のpristine rerun gate・チェーン全段frontier再計算までを確認ずみである。
fold24以降と異なりfold21の実験dirには出版社同梱の独立監査機（`verify_foldN_independent.py`）がなく、
fold22外部第二検証（K1167）もfold21記録をチェーン記録として機械照合した（covered行open性・
closed edge cost再計算・frontier_after再計算・五親target再計算をfold22 vantageから実施）が、
fold21 receipt自身の主張に対する、root幾何・K1124監査19 gate・証明書byte・C(8,6)=28部分幾何の
2方法再導出・28 canonical行分類・親delta値単位照合・pristine再実行・tamper込みの**外部第二検証**は
本検証が初めてである（宣言ノート記載のとおり）。本検証は単一オーナー宣言
（[宣言ノート](../../log/2026-11-20-n11-fold21-external-second-verification-single-owner-note.md)・
宣言コミット `98c90cb5108be93a607ba5e35c4cd7255f61ebe5`・本文修正コミット
`d323e780f950d6adea15b8bd7a3309e11d136d55`・宣言 2026-11-20T21:13:00Z・受入条件6項目）の下で実施した。
検証機 `scripts/verify_fold21_external_20261120.py` は第三実装である: K1167検証機（fold22外部検証機・
出版byte `ca11cbbc…`・repo commit `4eb6cbf05`）の設計を宣言ノートのとおり踏襲し、対象をfold21に差し替えて
本レーンが機械的region手術で生成したが、幾何・集計プリミティブ（8 D4座標写像・4×4共円行列det4・
survival-move規約の合法手再実装・census親対応）は検証機群の独自実装のままであり、fold22の検証結果を
入力として一切使わず、fold21出版機ともfold20以下の出版チェーン機とも実装を共有しない。
出力はソート済みkey・時刻を含まない決定論的な監査JSON 1点である（失敗時は監査未書込でexit 1）。

## 固定pin

出版byteはGitHubのpinned commitから再取得し（宣言時HEAD `5e1273f57c8c7733f0f2ba14a44000c2f5df0554`
と検証確定時最新main `d323e780f950d6adea15b8bd7a3309e11d136d55` の両方でbyte一致を確認）、
下記SHA-256を照合した。

- 出版receipt正本 `win8-root80880200-receipt-fold-20261120.json`
  SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`（26,113 bytes）
- 出版機 `fold_win8_root80880200.py`
  SHA-256 `44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b`（74,529 bytes）
- 出版生成機 `build_fold21.py`
  SHA-256 `51158e57af1e520c70822a9e2d875978ee9450a845753bea1d686b6dbaa9f8d4`（27,265 bytes）
- 出版README SHA-256 `6e27c07bb13ea3dc34d20c9537a1d4f8751a93850ea345151a082cde21ce9acc`（9,812 bytes）
- fold20 receipt正本 SHA-256 `76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2`
  （fold21機のpristine rerun gateの対象）
- fold20 出版機 SHA-256 `9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72`
- K1124証明書本体 SHA-256 `eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`
  （934,278 bytes・25,783行）
- K1124監査正本 SHA-256 `422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172`

もう一方の入力tree Wは、本実験dir同梱の `scripts/reconstruct_inputs.py`
（SHA-256 `a70b79834bb38fa3b02a563b75ae5cdf528a789e4f65150a5a9bcce775230095`・固定Git参照引数つき）で
再構成する。fold21機の入力pin 52点（12 Git blob pin + 40 SHA-256 pin）をfail-closedで再照合し、
rerun gate用にfold20出版機・fold19出版機・fold18出版機・fold18 preverified写しをSHA照合つきで配置する
（`fold20のchain入力（12 blob + 37 SHA-256）がfold21機の52 pinの部分集合である`ことを
reconstruct機と検証機の両方が機械確認する）。

## 実施内容と結果

監査正本は `output/external-audit.json`
（135,723 bytes・SHA-256 `80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63`・gate 1,394）で、
`all_gates_pass` は true である。gate内訳は P系 13（出版pin）・I系 60（W 52 pin + pin鎖整合）・
C系 1,292（別実装再導出）・X系 15（pristine再実行）・T系 14（tamper fail-closed）。
主な内容は次のとおり。

- **出版pin照合・W再構成（P/I系）**: 上記8正本のSHA-256照合、W 52 pin全件再照合、
  fold20機pin表（12 blob + 37 SHA-256）のfold21機52 pinに対する部分集合・値一致の機械確認。
- **pristine再実行4回（X系）**: 出版fold21機を `FOLD_PREVERIFIED_CHAIN` 不使用で実行。
  同じW上で4回（同一cwd 2回・隔離tree/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回）が
  すべてreturncode 0・receipt出力SHA-256出版正本 `9a4da2f6…` とbyte-identical
  （各回はfold20出版機のpristine rerun gateとその内部のfold19→fold18系推移的再検証込み・
  単独実行の実測は約6〜7秒）。宣言ノートpush前にレーン単独でも同一cwd 2回・隔離・
  隔離+random hash seedの4回再実行で同一結果を得ている（reproduction.log参照）。
- **別実装再導出（C系 1,292）**: base worklist 6,438行からledger/globalFold→previousCostFold→
  firstFold tarball→secondThird→fold4→fold56→fold7/8→ninth-twelfth→windfall4(thirteenth-sixteenth)→
  fold10..fold20に至る全frontier連鎖を独立再計算し、fold20適用後open frontier 6,144行/486,819 cost・
  solved 1,704・incidence 11,701・残余38行・五親target 74/112行を再構成（fold9 solved 1635・
  fs13 solved 1639等の各段published値と全一致）。K1124のroot `00000000000000801202000800880200` は
  石8・四つ組共円/共線0・D4正準を独立確認し、合法手46をsurvival-move規約の再実装で再導出
  （K1124 gate g05・g09と一致）。C(8,6)=28部分幾何のD4正準行を2方法
  （(A) 8 D4像×C(8,2) 2石除去224操作の完全合成と (B) C(8,6)=28部分集合のD4正準化）で再導出して
  集合として一致（D4同変性の実測確認）、28 canonical行の分類 open-frontier 8/not-in-worklist 19/
  closed-before-this-receipt 1を再決定（fold22検証では0だったclosed-before行がfold21時点で
  1行あることも再導出で確認。該当行 `00000000000000801202000800080000`〔cost 72・unswept〕は
  legacy base〔ledger closed_rows_66/globalFold/previousCostFold段〕で閉鎖済みの行であった
  ことを本レーンの追跡スクリプトでも確認）。閉鎖8行のうち五親target内主張3行（K1089 claimed == K1097 footprint
  `intrinsic == claimed`・exactly-once 49行分割の一部）と余剰5行への分割、closed edge cost 576、
  親delta 7親（class 2/4/6混在・80→77・17→14・45→43・81→78・74→72・59→56・48→46・計18 row-closing）、
  frontier_after 6,136/486,243・solved 1,712・incidence 11,683・s6_needed 4,444・cost_needed 352,691、
  五親target 74→77行・残余38→35行・win16候補 6→5根（残存主張行 12 = 49 − 37）を再計算し、
  出版receipt正本の全該当field（coverage行単位のcost/demand/parents・controls 63 boolean・
  独立検証ブロック・解釈ガード5文を含む）と値単位で一致。K1124監査19 gateの主要値
  （uncapped probes 618,359/669,067・third-method 46/9,204/[14,18]/57,636/37,121/11,311/52,219・
  証明書934,278 bytes・25,783行sort -u・header行・g01 K1089 master pin・g02==g03 runner blob・
  g13 extraction nodes 1,670,778/1,383,269・g16==recorded third_method・g17三方法一致）と
  K1097 refsolve footprint 16根49行exactly-onceも再照合した。
- **tamper 2件（T系）**: 宣言ノートで宣言済みの本レーンoffset
  `inputs/worklist.csv` byte offset 253 とK1124証明書 byte offset 17522 の1 byte XOR 0x01改変を
  Wの隔離複写上で実施し、それぞれ `input blob mismatch`・`input sha256 mismatch`・
  returncode≠0・出力未書込（rerun gate到達前の入力pin段でのfail-closed）を確認。
  隔離複写のため本番Wは無改変（事後にblob/SHA再照合）。

監査正本は4実行（同一cwd 2回＋隔離HOME/別cwd＋`PYTHONHASHSEED=random`）でbyte-identical、
さらに宣言時HEAD `5e1273f57…` と最新main `d323e780…` の2つのpinned refから独立再構成したW双方で
同一SHA-256 `80f00440…` を確認した（計5実行byte一致・W/pubは2参照間で全ファイルdiff一致・
W21の`fold21/`出力dirを除く）。検証機1実行は実測約27.6秒（user約22.8秒・fold21機6回起動込み）。
実行記録は `output/reproduction.log` に置いた。

### 実験事実

- 宣言ノートの初回push（`98c90cb5`）に実ファイル内容ではなくプレースホルダ文字列が入り、
  55秒後の修正コミット（`d323e780`）で本文を差し替えた。file内容のpush APIへの渡しを
  正規化しなかったレーン自身のオペレーションミスであり、修正後のfetch-backで
  本文byte一致を確認して受入条件に影響しない。宣言時刻は宣言ノート本文の記録どおり
  2026-11-20T21:13:00Z（本文修正コミットは宣言時刻直後に後続）。登録済みdeclarationの先取り・衝突なしの確認は初回push前に
  実施済みで有効（並走レーンは失敗に依存しない）。
- 進行中メモ（compaction summary）の「win16候補 6→5根（主張16→13行）」は記録値と不一致だった:
  実receiptの `win_candidate_plan_impact` 主張は「残存候補5根・残存主張行12行」
  （49 − 4-3-3-4-3-4-3-3-4-3-3 = 12）。本検証の再導出（fold11..fold20 retired 10根34行 +
  fold21 retire 3行 = 37行、K1097 footprint 16根49行exactly-once・残り5根12行）は
  receipt記録値と完全一致した。K1167で確認済みの「要約転写定数は検証機のfail-closed gateで捕捉される」
  教訓を改めて実証: 本検証は全定数を実レコードから読み取り打鍵した。

## 再現手順

```
python3 scripts/reconstruct_inputs.py <W_dir> <pub_dir> [<git_ref>]
python3 scripts/verify_fold21_external_20261120.py <W_dir> <pub_dir> <out_json>
```

`<pub_dir>` はfold21出版実験dir（出版byte 4ファイル）。`reconstruct_inputs.py` のデフォルト
Git参照は `5e1273f57c8c7733f0f2ba14a44000c2f5df0554`（検証時main `d323e780…` でもbyte一致済み）。
検証機は単一プロセス・直列で約28秒（実測27.6秒・user 22.8秒）で終了し、
`<out_json>` が本README記載のSHA-256 `80f00440…`（135,723 bytes・gate 1,394）と一致すれば再現成立である。

## 限界

本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査であり、
S6行・五親target行を1行も閉じない。fold21 receipt自体が8行（主張3+余剰5）を閉じたのは
Publisherの成果簿記であり、本検証はその外部確認である。WIN8-D10証明書は当該8石rootの
ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。**
