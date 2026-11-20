# 単一オーナー宣言ノート: fold11 receipt fold（root 8003180）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold11（第18 receipt・初のWIN8 receipt fold・root `00000000000000003800000008003180`・
残余72→68行・K1096証明書の五親S6 frontier receiptチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T23:28:00Z（push直前に再取得した main HEAD を出版時のコミット列で確定し、受入条件1の固定commitとして使う）
- 先行宣言の確認: 直近コミット列挙（21:00Z以降全件）・commit code search
  （`fold11 external second verification`・`root8003180 external`）で
  **fold11単体の外部第二検証の宣言・実験・log は main 上に存在しない**ことを確認した。
  fold18（`b5e1d5f6`系・ext2宣言 `c2e8eb09f7`）・fold19（ext2宣言 `9606203aec`）・
  fold20（ext2宣言 `5f6c1b7a91`・23:09:11Z・他レーン）・fold23（`90ac8eed`）・
  fold25（`aad3b71ca`）・fold26 receipt（`e53cc60c`/`ba659878`）・
  K1172 part gate補完（`50d80188`・23:16:09Z・進行中）は他レーン宣言済み着手禁止。
  fold21=K1168・fold22=K1167・fold24=K1164/K1165・fold29 cert-extract=K1166/K1172は
  ext2・第三検証まで完了済みで対象外。fold12〜16（root 8005021/9840004/9090022/
  120000038/8890020）のext2にも現時点で先行宣言がないが、本宣言はfold11に限定し、
  fold12以降は別途宣言を要する。
- 対象出版物: `research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/`
  （README 5,304 bytes・出版機 `scripts/fold_win8_root8003180.py` 32,204 bytes・
  receipt正本 `output/win8-root8003180-receipt-fold-20261120.json` 17,008 bytes の3点）
- 対象正本（SHA-256・byte数は固定commitからの実取得で実測）:
  - fold11 receipt正本 `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`（17,008 bytes）
  - fold11 出版機 `9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1`（32,204 bytes・純Python・乱数・時刻なし・約1.4秒/実行）
  - fold11 出版README `c2361ae14b8e6e68c8148c9e7eff55bff8e931f1e73f17164f6baba267a837c0`（5,304 bytes）
  - fold10 receipt正本（previous_fold.record）
    `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`
    （`n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json`）
  - fold10 出版機 `fold_seventeenth.py`（同実験dirから再取得しSHA-256を実測で打鍵・rerun gate用途）
  - K1096 監査正本 `ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da`（18 gate）
  - K1096 証明書本体 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`
    （1,251,923 bytes・34,529行・sorted unique・合法手53）
  - K1097 refsolve正本 `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`（27 gate）
  - W入力22 pin（receipt `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 10 SHA-256・
    worklist/ledger/globalFold/previousCostFold/firstFoldTarball/census/audit/secondThirdFold/
    fold4/fold56/fold912/fold_fourth_fifth_sixth.py/fold7/fold8/resolve6/fs13/sv17正本/sv17証明書/
    fold10正本/K1096監査/K1096証明書/K1097正本）

## 位置づけ

fold11の出版は出版社レーン自身の3実行byte一致・22 pin fail-closed・K1096 18 gate・
K1097 27 gateの再照合・チェーン全段frontier再計算（6,259/495,507→…→6,206/491,497・
incidence 11,826→11,818→11,810・residual 74→72）を含む。以降のfold12以降の各出版機は
fold11出版機をrerun gateで再実行し、K1167/K1168の外部検証機もfold11を連鎖再計算で
間接的に通過させているが、**fold11 receipt自身の主張**（open 5行閉鎖・主張4行＋余剰1行
`0000000000000000380000000800000c`・closed edge cost 387・残余72→68・五親112行target
40→44・frontier 6,206/491,497→6,201/491,110・solved 1,642→1,647・incidence 11,810→11,803・
影響3親〔c2・64→61/27→25/25→23〕・needed 4,509→4,504・cost 357,583→357,196・
28 canonical行分類 open 5/closed-before 1〔`…8003000`〕/not-in-worklist 22・
win16候補 16→15根〔主張49→45行〕・残余23行不変）の第三実装による値単位の独立確認は
まだない。fold11はWIN8 receipt foldの最初のfoldで、fold12以降の全chainの最初の拡張段
であるため、起点の独立検証は残りの未検証分（fold12〜16）の前段として最も優先度が高い。

## 作業範囲（受入条件）

1. 出版byteをGitHub（main固定commit）から再取得し、上記正本群（receipt・出版機・README・
   fold10正本・fold10出版機・K1096監査・K1096証明書・K1097正本）のSHA-256 pinを照合する。
   W入力22 pinはGit blob SHA-1（12点）とSHA-256（10点）でfail-closed照合する。
2. W入力treeをrepo出版byteのみから本レーンが書く再構成機で再構築し
   （fold11機・fold10機ともW外にSHA照合つきで配置）、全pinの値一致を機械確認する。
3. fold11出版機をpristine再実行する（同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回・計4回）。全回のreceipt出力SHA-256が出版正本
   `d7bf2cd5…` とbyte-identicalであること。加えてfold10出版機 `fold_seventeenth.py` を
   隔離W複写上で再実行し、fold10正本 `bed7d331…` とbyte-identicalであることを確認する
   （fold11機が接続する上流のrerun gateを独立に再現）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold11機・fold10機の幾何・
   集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む）で、
   worklist・ledger・census・audit・各段receipt記録・fold10正本・fold11正本・
   K1096証明書・監査・K1097 refsolveから:
   - base 6,438行（総cost 509,109）からfold10適用後open frontier 6,206行/491,497・
     solved 1,642・incidence 11,810・残余72行・五親target 40/112行までの
     チェーン各段の再構成（fold9以前・fs13・fold10の各段published値との照合込み）、
   - K1096 root `00000000000000003800000008003180`（8石）のC(8,6)=28部分幾何の
     D4正準行を2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、C(8,6)=28部分集合の
     D4正準化の各々）で再導出し、閉鎖候補行（主張4行〔cost 74/75/76系〕＋余剰1行
     `0000000000000000380000000800000c`〔cost 83〕・閉鎖edge cost 387・
     5行のopen性と5親target内外の分類・28 canonical行分類 open/closed-before/not-in-worklist
     の再決定、
   - 親delta（影響3親・いずれもclass 2・rows 64→61/27→25/25→23・完全閉鎖0）、
     frontier_after（6,201/491,110・solved 1,647・incidence 11,803・needed 4,504/357,196）、
     五親target 40→44行・残余72→68行・win16候補16→15根（主張49→45行・residual23不変）を
     含む全統計の再計算、
   - K1096 18 gate主要値（証明書1,251,923 bytes・34,529行sorted unique・root幾何
     〔8石・quadruple-free・D4正準〕・合法手53の独立再導出・third_method集計
     terminal 13,364/visited 76,955/winner 49,509/loser 14,082/応手辺 67,420）と
     K1097 27 gate・win16 footprint root 8003180行の intrinsic == claimed == 4行・
     49行exactly-once partition・残余23行不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold21外部検証機（K1168・`322ad6ca…`）の設計を踏襲してよいが、対象行・
   root幾何はfold11のものであり、fold21/22等の検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

## 管轄の限界

本宣言はfold11単体の外部第二検証に限定される。fold12〜16のext2、fold18/19/20/23/25/26の
外部第二検証（既に他レーン宣言済み）は本宣言の対象外であり、先行宣言に従う。
新規depth-10 probe・新規証明書抽出・行の閉鎖claimは本検証では一切行わない。
本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない（fold11時点残余72→68行はK1105の既出版簿記・
pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
