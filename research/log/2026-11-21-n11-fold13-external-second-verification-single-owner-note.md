# 単一オーナー宣言ノート: fold13 receipt fold（root 9840004）の外部第二検証（2026-11-21）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold13（第20 receipt・3番目のWIN8 receipt fold・root `00000000000000003800000009840004`・
残余65行→62行・K1108証明書の五親S6 frontier receiptチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-21T01:00:00Z
- 宣言時点の main HEAD: push直前再取得で確定（commit `928ae7834e`想定・取得失敗時は取得時点の最新HEAD）。
  fold13単体の外部第二検証の先行宣言なしを確認済み: 直近30コミット（2026-11-21T00:10Z以降、
  n11系は本レーンfold12外部第二検証（K1175: 宣言 `de32ca573b`・part1/part2/part3群）、
  fold20 ext2→K1173 pristine re-exec第三検証 K1174（`1d68addb`/`a853b533`/`bda65d3f`/`13a8b604`〔他レーン〕）、
  n9-ge19 lane part6 marathon群・five-row q7 band-closure群・binary-cube GP-census群（K0568出版・`f541f30c`/`912d09fe`）、
  four-row q6/q7 witness frontier宣言 `528ec9605b`（いずれもfold13単体を対象外））に
  fold13単体ext2の宣言・実験・logは0件。fold12単体ext2宣言ノート（`de32ca573b`）の「fold13-16は各レーン個別宣言」記載どおり、
  本宣言がfold13単体の最初の宣言である。
- 対象出版物: `research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/`
  （出版実験dir 3ファイル: README・fold13機・receipt正本。builderファイルの同梱なし）
- 対象正本（SHA-256・byte数は2026-11-21T00:58Z時点の最新main〔HEAD `928ae7834e`〕からの実取得で実測）:
  - fold13 receipt正本 `output/win8-root9840004-receipt-fold-20261120.json`
    `c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae`（20,416 bytes）
  - fold13 出版機 `scripts/fold_win8_root9840004.py`
    `5c27f1ae1362c6f436e126786891bd4617ec92e403d22eff0b3b7537e51b0020`（42,315 bytes・fold12機の移行型・純Python・乱数・時刻なし・約5.6秒/実行）
  - 出版README `ca7ead2b6691d56bf5868d3e06f7488ee2b06c103aee7abd6c2d181293660f39`（7,169 bytes）
  - 直前のfold12 receipt正本（fold13機のchain直前段・fold12機のrerun gate対象）
    `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`（19,322 bytes）
  - fold12 出版機 `fold_win8_root8005021.py`
    `706bfa7ae8b8ff022e2f05c91eb0c61da6bf3343805dce7ed7e35289bf3a906c`（37,868 bytes）
  - fold11 receipt正本（fold12機のchain直前段・fold11機のrerun gate対象）
    `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`（17,008 bytes）
  - fold11 出版機 `fold_win8_root8003180.py`
    `9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1`（32,204 bytes）
  - K1108証明書検証正本（fold13 receipt の certificate_source記載・19 gate）
    `2e453a76fc3168b8eb2e5c224d4a271eea0839eb5256d51fd9c02eb54bb1f648`（5,376 bytes）
  - K1108証明書本体 `win8-root-00000000000000003800000009840004-20261120.n11`
    `5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143`（1,640,220 bytes・45,286行・n11-terminal-strategy-v1全証明書中最大行数）
  - K1097 refsolve正本
    `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`（43,540 bytes・27 gate）
  - W入力pin（receipt `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 16 SHA-256 の計28件）は
    receipt から機械読み取りして再構成機と検証機の両方でfail-closed照合する。
    チェーン入力はfold12機と同一の12 blob + 13 SHA-256 pin＋追加入力
    （fold12正本・K1108監査正本・K1108証明書）。

## 位置づけ

fold13の出版は出版社レーン自身の3実行byte一致・28 pin fail-closed・K1108 19 gate・
K1097 27 gate再照合・fold11・fold12出版機pristine rerun gate・fold10込みチェーン全段frontier再計算を含む。
K1173/K1174のfold20外部検証機もfold12記録までをチェーン照合し、fold12単体ext2（K1175・本レーン前回完了）も
fold12記録までで完結したため、**fold13 receipt自身の主張**（単一WIN8 receiptとして最多を更新する
open 9行閉鎖〔K1108/K1097主張3行＋余剰6行・余剰6行は単一receiptとして最多〕・
closed edge cost 713・残余65→62・五親112行target 47→50・frontier 6,193/490,526→6,184/489,813・
solved 1,655→1,664・incidence 11,790→11,775・needed 4,501→4,492・cost_needed 356,974→356,261・
影響5親〔c4×3: 87→84/90→87/75→72・c2×2: 61→58/16→13・完全閉鎖0〕・root合法手57・
28 canonical行分類 open 9/not-in-worklist 19・win16候補 14→13根〔主張42→39行〕・
K1108 third_method集計 terminal 17,333/visited 103,531/winner 66,627/loser 19,571/
応手辺 91,337・terminalRange [14,18]・unique_strategy_rows 45,286・
g06 uncapped probes nodes 1,143,198/1,528,656・g13 nodes 4,109,768/3,075,922）の第三実装による
値単位の独立確認はまだない。fold13の実験dirには独立監査機がないため、fold20外部第二検証（K1173）・
fold12外部第二検証（K1175）と同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群のSHA-256 pinを照合する
   （fold13機の入力pin表はreceiptから機械読み取りで確定させ、全28 pinをfail-closedで再照合する）。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold13機の入力pin全件の再照合・rerun gate・独立rerun用のfold11機・fold12機の配置SHA照合・
   fold11機・fold12機の入力pin表のfold13機pin表に対する部分集合性の機械確認）。
   K1175レーンで確立した静的raw URL再構成機設計（api.github.com非依存・全byte digest照合）を踏襲する。
3. fold13出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。`FOLD13_W` 不使用・機内向けrerun gate〔fold11機・
   隔離W複写上のfold12機〕は各回実行）。全実行のreceipt出力SHA-256が出版正本 `c2bf8051…` と
   byte-identicalであること。加えてfold12出版機を隔離W複写上で独立に再実行し、fold12正本 `0f73795c…` と
   byte-identicalであることを確認する（fold13機が接続する上流rerun gateの外側からの再現）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold13機・fold12機・fold11機の幾何・
   集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む。
   K1175検証機の設計を踏襲してよい）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・firstFold系・fold4/fold56/fold912/secondThird・resolve6・fs13・sv17・
   fold10・fold11 receipt記録・fold12 receipt記録・fold13正本・K1108証明書・K1097 refsolveから:
   - base 6,438行（総cost 509,109）からfold12適用後open frontier 6,193行/490,526・
     solved 1,647→1,655・incidence 11,803→11,790・残余65行・五親target 47/112行までの
     チェーン各段の再構成（fold9以前・fs13・fold10・fold11・fold12の各段published値との照合込み）、
   - K1108 root `00000000000000003800000009840004`（8石）の幾何（石数・quadruple-free・D4正準）と
     合法手57の独立再導出（survival-move規約の再実装）、C(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と28部分集合のD4正準化の各々）で再導出し、
     28 canonical行の分類（open-frontier 9/not-in-worklist 19）とcoverage 9行
     （K1108 g07主張3行＋余剰6行）・各行cost/demand/parents・closed edge cost 713の再決定、
   - 親delta（影響5親・87→84〔c4〕/90→87〔c4〕/75→72〔c4〕/61→58〔c2〕/16→13〔c2〕・完全閉鎖0）、
     frontier_after（6,184行/489,813・solved 1,664・incidence 11,775・needed 4,492/356,261）、
     五親target 47→50・残余65→62行（62行hex全列挙照合）・win16候補 14→13根
     （主張42→39行・retired root `…9840004` 3行・残余23行不交差）を含む全統計の再計算、
     - K1108監査19 gate主要値（g06 uncapped probes nodes 1,143,198/1,528,656・g13 nodes 4,109,768/3,075,922・
       g05 mobility 57・証明書byte 1,640,220/行数45,286 sorted unique・third_method集計terminal 17,333/visited 103,531/
       winner 66,627/loser 19,571/応手辺 91,337・terminal_range [14,18]）と
       K1097 27 gate・win16 footprintの root 9840004行の intrinsic == claimed == 3行・
       49行exactly-once partition・残余23行不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold12外部検証機（K1175・`43afc1cd…`）等の設計を踏襲してよいが、対象行・root幾何は
   fold13のものであり、fold14以降のreceipt・外部検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold13単体の外部第二検証に限定される。fold11単体ext2（`9be43128`・他レーン）・
fold12単体ext2（K1175・本レーン前回完了）・fold14-16単体ext2（root 9090022/120000038/8890020・ただし本宣言の存在に依らず
各レーンが個別に宣言する）・fold17単体ext2（`095581932b`）・
fold18/19/20/23/25/26の外部第二検証（fold20はK1173/K1174完了・fold12はK1175完了・他は各所有者宣言済み）・
round-5 refsolve（`ace38772d9`）・
WIN8 root `…40002001`証明書抽出（`63877ffd2e`）・WIN8証明書行共有監査（`c403614f`）・
n9-ge19（`21f8610464d2`）・n10 witness（`a6fb407c`）・five-row q7 band-closure（`92722ac3`）・
binary-cube GP-census（K0568完了）・four-row q6/q7 witness frontier（`528ec9605b`）は本宣言の対象外であり、先行宣言があればそれに従う。
新規depth-10 probe・新規証明書抽出・行の閉鎖claimは本検証では一切行わない。
本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない（fold13時点残余65→62行は当該receiptの既出版簿記・
pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
