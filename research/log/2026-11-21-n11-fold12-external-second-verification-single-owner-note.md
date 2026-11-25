# 単一オーナー宣言ノート: fold12 receipt fold（root 8005021）の外部第二検証（2026-11-21）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold12（第19 receipt・2番目のWIN8 receipt fold・root `00000000000000003800000008005021`・
残余68行→65行・K1106証明書の五親S6 frontier receiptチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-21T00:41:00Z
- 宣言時点の main HEAD: push直前再取得で確定（commit `aed703c597`想定・取得失敗時は取得時点の最新HEAD）。
  fold12単体の外部第二検証の先行宣言なしを確認済み: 直近40コミット（2026-11-20T23:17Z以降、
  n11系は K1172 part gate補完群、fold11単体ext2宣言 `9be43128`〔23:27:12Z・他レーン・fold12-16は別途宣言と明記〕、
  fold17単体ext2宣言 `095581932b`〔23:33:34Z・他レーン・fold12-16は他レーン別途宣言と明記〕、
  fold20 ext2 `f221398219`→K1173→K1174 pristine re-exec `1d68addb`/`a853b533`/`bda65d3f`/`13a8b604`〔本レーン前回〕、
  n9-ge19 lane part5/6群・five-row q7 band-closure群・resume宣言 `92722ac3`（いずれもfold12単体を対象外））に
  fold12単体ext2の宣言・実験・logは0件。
- 対象出版物: `research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/`
  （出版実験dir 3ファイル: README・fold12機・receipt正本。builderファイルの同梱なし）
- 対象正本（SHA-256・byte数は2026-11-21T00:35Z時点の最新main〔HEAD `aed703c597`〕からの実取得で実測）:
  - fold12 receipt正本 `output/win8-root8005021-receipt-fold-20261120.json`
    `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`（19,322 bytes）
  - fold12 出版機 `scripts/fold_win8_root8005021.py`
    `706bfa7ae8b8ff022e2f05c91eb0c61da6bf3343805dce7ed7e35289bf3a906c`（37,868 bytes・純Python・乱数・時刻なし・約2.8秒/実行）
  - 出版README `314a37287285ff35f72d85174aeb35226308da574fd12182ccdfea4145dbe85c`（6,413 bytes）
  - 直前のfold11 receipt正本（fold12機のchain直前段・fold11機のrerun gate対象）
    `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`（17,008 bytes）
  - fold11 出版機 `fold_win8_root8003180.py`
    `9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1`（32,204 bytes）
  - K1106証明書検証正本（fold12 receipt の certificate_source記載・19 gate）
    `0bd2dd10c1d5b735a04f31425003c635d80266e4c03a6bef0fdff212d499408f`（5,370 bytes）
  - K1106証明書本体 `win8-root-00000000000000003800000008005021-20261120.n11`
    `69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5`（945,298 bytes・26,083行）
  - K1097 refsolve正本
    `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`（43,540 bytes・27 gate）
  - W入力25 pin（receipt `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 13 SHA-256）は
    receipt から機械読み取りして再構成機と検証機の両方でfail-closed照合する。
    チェーン入力はfold11機と同一の12 blob + 10 SHA-256 pin＋追加入力
    （fold11正本・fold11機・K1106監査・K1106証明書・K1097正本）。

## 位置づけ

fold12の出版は出版社レーン自身の3実行byte一致・25 pin fail-closed・K1106 19 gate・
K1097 27 gate再照合・fold11出版機pristine rerun gate・fold10込みチェーン全段frontier再計算を含む。
以降のfold13〜fold20の各出版機はfold12出版機をrerun gateで再実行し、fold20 extremalの
K1167/K1168/K1173の外部検証機もfold12記録をチェーン記録として機械照合したが、
**fold12 receipt自身の主張**（単一WIN8 receiptとして最多のopen 8行閉鎖〔主張3行＋余剰5行〕・
closed edge cost 584・残余68→65・五親112行target 44→47・frontier 6,201/491,110→6,193/490,526・
solved 1,647→1,655・incidence 11,803→11,790・needed 4,504→4,501・cost_needed 357,196→356,974・
影響5親〔c1×3: 58→56/65→63/75→72・c2×2: 44→41/25→22・完全閉鎖0〕・root合法手41・
28 canonical行分類 open 8/not-in-worklist 20・win16候補 15→14根〔主張45→42行〕・
K1106 third_method集計 terminal 10,191/visited 59,594/winner 38,442/loser 10,961/
応手辺 53,352・terminalRange [14,18]・unique_strategy_rows 26,083）の第三実装による
値単位の独立確認はまだない。fold12の実験dirには独立監査機がないため、fold20外部第二検証（K1173）と
同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群のSHA-256 pinを照合する
   （fold12機の入力pin表はreceiptから機械読み取りで確定させ、全25 pinをfail-closedで再照合する）。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold12機の入力pin全件の再照合・rerun gate・独立rerun用のfold11機の配置SHA照合・
   fold11機の入力pin表のfold12機pin表に対する部分集合性の機械確認）。
3. fold12出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。`FOLD12_W` 不使用・機内向けrerun gateは各回実行）。
   全実行のreceipt出力SHA-256が出版正本 `0f73795c…` とbyte-identicalであること。
   加えてfold11出版機を隔離W複写上で独立に再実行し、fold11正本 `d7bf2cd5…` と
   byte-identicalであることを確認する（fold12機が接続する上流rerun gateの外側からの再現）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold12機・fold11機の幾何・
   集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む。
   K1168/K1173検証機の設計を踏襲してよい）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・firstFold系・fold4/fold56/fold912/secondThird/foldv2・resolve6・fs13・sv17・
   fold10・fold11 receipt記録・fold12正本・K1106証明書・K1097 refsolveから:
   - base 6,438行（総cost 509,109）からfold11適用後open frontier 6,201行/491,110・
     solved 1,642→1,647・incidence 11,810→11,803・残余68行・五親target 44/112行までの
     チェーン各段の再構成（fold9以前・fs13・fold10・fold11の各段published値との照合込み）、
   - K1106 root `00000000000000003800000008005021`（8石）の幾何（石数・quadruple-free・D4正準）と
     合法手41の独立再導出（survival-move規約の再実装）、C(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と28部分集合のD4正準化の各々）で再導出し、
     28 canonical行の分類（open-frontier 8/not-in-worklist 20）とcoverage 8行
     （K1106 g07主張3行＋余剰5行）・各行cost/demand/parents・closed edge cost 584の再決定、
   - 親delta（影響5親・58→56〔c1〕/65→63〔c1〕/75→72〔c1〕/44→41〔c2〕/25→22〔c2〕・完全閉鎖0）、
     frontier_after（6,193行/490,526・solved 1,655・incidence 11,790・needed 4,501/356,974）、
     五親target 44→47・残余68→65行（65行hex全列挙照合）・win16候補 15→14根
     （主張45→42行・retired root `…8005021` 3行・残余23行不交差）を含む全統計の再計算、
     - K1106監査19 gate主要値（g06 uncapped probes 619,138/751,581・g13 nodes 3,272,039/2,876,091・
       証明書byte・行数sorted unique・third_method集計terminal 10,191/visited 59,594/
       winner 38,442/loser 10,961/応手辺 53,352・terminal_range [14,18]）と
       K1097 27 gate・win16 footprintの root 8005021行の intrinsic == claimed == 3行・
       49行exactly-once partition・残余23行不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold21外部検証機（K1168・`322ad6ca…`）等の設計を踏襲してよいが、対象行・root幾何は
   fold12のものであり、fold13以降のreceipt・外部検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold12単体の外部第二検証に限定される。fold11単体ext2（`9be43128`・他レーン）・
fold13-16単体ext2（root 9840004/9090022/120000038/8890020・ただし本宣言の存在に依らず
各レーンが個別に宣言する）・fold17単体ext2（`095581932b`）・
fold18/19/20/23/25/26の外部第二検証（fold20は本レーン前回K1173/K1174完了・
他は各所有者宣言済み）・round-5 refsolve（`ace38772d9`）・
WIN8 root `…40002001`証明書抽出（`63877ffd2e`）・WIN8証明書行共有監査（`c403614f`）・
n9-ge19（`21f8610464d2`）・n10 witness（`a6fb407c`）・five-row q7 band-closure（`92722ac3`）は
本宣言の対象外であり、先行宣言があればそれに従う。
新規depth-10 probe・新規証明書抽出・行の閉鎖claimは本検証では一切行わない。
本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない（fold12時点残余68→65行は当該receiptの既出版簿記・
pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
