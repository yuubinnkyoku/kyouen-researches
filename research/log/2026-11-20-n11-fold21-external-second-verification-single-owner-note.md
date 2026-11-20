# 単一オーナー宣言ノート: fold21 receipt fold（K1130）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold21（K1130・残余38行→35行 WIN8-D10 receipt fold root `00000000000000801202000800880200`）
出版成果に対する**外部第二検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T21:13:00Z
- 宣言時点の main HEAD: `5e1273f57c8c7733f0f2ba14a44000c2f5df0554`
  （fold21単体の外部第二検証の先行宣言なしを確認済み。fold22外部第二検証は本レーンの
  K1167として完了出版済み、fold23外部第二検証は宣言済み `90ac8eed`・fold24外部第二検証は
  完了出版済み〔K1164〕・fold25外部第二検証は宣言済み `aad3b71ca`。fold22宣言ノートは
  「fold21単体の外部第二検証は本宣言の対象外（着手する場合は別途宣言する）」と予告しており、
  それに従い本宣言をもって着手する）
- 対象出版物: `research/experiments/n11-residual35-win8-receipt-fold-root80880200-20261120/`
  （receiptの出版 experiment dir 4ファイル: README・build機・fold21機・receipt正本）
- 対象正本:
  - fold21 receipt正本 `output/win8-root80880200-receipt-fold-20261120.json`
    SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`（26,113 bytes）
  - fold21 出版機 `scripts/fold_win8_root80880200.py`
    SHA-256 `44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b`（74,529 bytes）
  - fold21 生成機 `scripts/build_fold21.py`
    SHA-256 `51158e57af1e520c70822a9e2d875978ee9450a845753bea1d686b6dbaa9f8d4`（27,265 bytes）
  - 出版README SHA-256 `6e27c07bb13ea3dc34d20c9537a1d4f8751a93850ea345151a082cde21ce9acc`（9,812 bytes）
  - 直前のfold20 receipt正本 SHA-256
    `76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2`
  - fold20 出版機 SHA-256
    `9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72`
    （fold21機のpristine rerun gateの対象）
  - K1124証明書本体 SHA-256
    `eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`
  - K1124監査正本 SHA-256 `422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172`

## 位置づけ

fold21の出版は出版社レーン自身の複数回実行・fold20出版機のpristine rerun gate・
チェーン全段frontier再計算を含み、fold22外部第二検証（K1167）のpristine再実行4回でも
fold21機は隔離W複写上で再実行されreceipt byte一致が確認されている。しかし
fold21 receipt自身の主張（open 8行閉鎖・主張3行＋余剰5行・closed edge cost 576・
残余38→35行・frontier delta・28 canonical行分類・7親delta・win16候補 6→5根）の
値単位の独立確認はまだない（fold22外部検証機がfold21 frontierまでのchainを再計算したが、
fold21 receiptのcoverage・parent delta・ certificat主要値の全field照合は対象外だった）。
そこで本検証では、fold21 receipt正本の全主張を第三実装で出版byteだけから再導出する。
fold21の実験dirにはfold24以降の同梱独立監査機がないため、fold22外部第二検証（K1167）と
同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記8正本（receipt・機・生成機・README・
   fold20正本・fold20機・K1124証明書・K1124監査）のSHA-256 pinを照合する。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold21機の12 Git blob pin + 40 SHA-256 pin = 52 pinをfail-closedで
   再照合し、rerun gate用にfold20出版機・fold18/19出版機・fold18 preverified写しを配置する）。
   fold20のchain入力がfold21機の52 pinの部分集合であることを機械確認する。
3. fold21出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   `PYTHONHASHSEED=random` 1回を含む・`FOLD_PREVERIFIED_CHAIN` 不使用）。
   全実行のreceipt出力SHA-256が出版正本 `9a4da2f6…` とbyte-identicalであること
   （fold20機pristine rerun gate・その内部のfold19/18系推移的再検証込み）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold21機・fold22機と
   幾何・集計補助関数を流用しない）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・fold1..20 receipt記録・fold21正本・K1124証明書・監査・K1097 refsolveから:
   - fold20適用後open frontier 6,144行/486,819 cost・残余38行の再構成、
   - K1124 root `00000000000000801202000800880200` のC(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、C(8,6)=28部分集合のD4正準化の各々）で
     再導出し、閉鎖候補行（主張3行＋余剰5行・閉鎖edge cost 576・28 canonical行分類）の再決定、
   - 親delta（7親・class 2/4/6混在・計18行）、frontier_after
     （6,136/486,243・solved 1,712・incidence 11,683・needed 4,444/352,691）・
     五親target 74→77行・残余38→35行・win16候補 6→5根（主張16→13行）を含む全統計の再計算、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold22外部検証機（K1167・SHA-256 `ca11cbbc…`）の設計を踏襲してよいが、
   対象行・root幾何はfold21のものとし、fold22の検証結果は入力に使わない
   （fold20までのchain再計算まではK1167と同型の独立再実装とする）。
5. tamper検査: 1 byte XOR改変（pin入力2件・本レーンが選んだ offset:
   `inputs/worklist.csv` offset 253 と K1124証明書 offset 17522）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## やらないこと・非主張

- fold20 receipt単体の外部第二検証（着手する場合は-fold22と同様に-別途宣言する）・
  fold23外部第二検証（`90ac8eed`所有）・fold25外部第二検証（`aad3b71ca`所有）・
  fold26 receipt fold（`23bffdd4e4`所有）・round-5 refsolve（`ace38772d9`所有）・
  WIN8-D10候補 `00000000010000809002000040002001` の証明書抽出（`63877ffd2e`所有）・
  WIN8証明書行共有監査（`c403614f`所有）は本宣言の対象外。
  新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証はreceipt簿記の再検査であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
