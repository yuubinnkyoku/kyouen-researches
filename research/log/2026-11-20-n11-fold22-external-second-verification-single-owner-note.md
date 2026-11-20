# 単一オーナー宣言ノート: fold22 receipt fold（K1132）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold22（K1132・残余32行 WIN8-D10 receipt fold root `00000000000000801202000000840500`）
出版成果に対する**外部第二検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T20:46:23Z
- 宣言時点の main HEAD: `9a1c7a98f39103013a0221f4f63fc10eba6a9061`
  （fold22外部第二検証の先行宣言なしを確認済み。fold23外部第二検証は宣言済み `90ac8eed`・
  fold25外部第二検証は宣言済み `aad3b71ca`・fold24外部第二検証は完了出版済み〔K1164〕。
  fold23宣言ノートは「fold22 receipt単体の外部第二検証は別途宣言する」と予告しているが、
  本宣言時点で先行するfold22単体宣言は存在しない）
- 対象出版物: `research/experiments/n11-residual32-win8-receipt-fold-root840500-20261120/`
  （receiptの出版は単一コミット `ac7b8be685a720915515fba04ceb61d7d1e505ab`:
  README・build機・fold22機・receipt正本の実験dir 4ファイル）
- 対象正本:
  - fold22 receipt正本 `output/win8-root840500-receipt-fold-20261120.json`
    SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`（25,349 bytes）
  - fold22 出版機 `scripts/fold_win8_root840500.py`
    SHA-256 `d5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d`（78,343 bytes）
  - fold22 生成機 `scripts/build_fold22.py`
    SHA-256 `a73995be2ac448f2e56f804b3263330513c5bcb8a9e4042661c56e1deb4d7085`（27,000 bytes）
  - 直前のfold21 receipt正本 SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`
  - fold21 出版機 SHA-256 `44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b`
    （fold22機のpristine rerun gateの対象）
  - K1125証明書本体 SHA-256 `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`（1,067,425 bytes）
  - K1125監査正本 SHA-256 `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`

## 位置づけ

fold22の出版は出版社レーン自身の3回実行（同一cwd 2回＋隔離W複写・別cwd・別HOME）・
fold21出版機のpristine rerun gate・チェーン全段frontier再計算・K1125 19 gate全再検証を含むが、
出版社以外の実行主体による第二検証はまだない（fold22の実験dirには出版社同梱の独立監査機がなく、
fold24以降の `verify_foldN_independent.py` 方式の同梱監査も持たないため、
本検証はfold24外部第二検証〔K1164〕のような同梱監査の再実行項目を持たない分、
別実装再導出が検証の本体になる）。fold22 receipt正本（`f6e011f4…`）は
fold23・fold24外部第二検証のチェーン再計算・frontier再構成の入力として間接照合に
使われてはいるが、fold22 receipt自身の主張（open 6行閉鎖・closed edge cost 484・
残余35→32行・frontier delta・28 canonical行分類・4親delta・win16候補 5→4根）の
値単位の独立確認はまだない。fold22より前のfold21（K1130）単体の外部第二検証は
本宣言の対象外とする（着手する場合は別途宣言する）。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記7正本（receipt・機・生成機・
   fold21正本・fold21機・K1125証明書・K1125監査）のSHA-256 pinを照合する。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold22機の12 Git blob pin + 43 SHA-256 pin = 55 pinをfail-closedで
   再照合し、rerun gate用にfold21出版機・fold18/19/20出版機・fold18 preverified写しを配置する）。
   fold21のchain入力（12 blob + 40 SHA-256）がfold22機の55 pinの部分集合であることを機械確認する。
3. fold22出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   `PYTHONHASHSEED=random` 1回を含む・`FOLD_PREVERIFIED_CHAIN` 不使用）。
   全実行のreceipt出力SHA-256が出版正本 `f6e011f4…` とbyte-identicalであること
   （fold21機pristine rerun gate・その内部のfold20/19/18系推移的再検証込み）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold22機・fold21機の
   幾何・集計補助関数を流用しない）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・fold1..21 receipt記録・fold22正本・K1125証明書・監査・K1097 refsolveから:
   - fold21適用後open frontier 6,136行/486,243 cost・残余35行・五親target 77/112行の再構成、
   - K1125 root `00000000000000801202000000840500` のC(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、C(8,6)=28部分集合のD4正準化の各々）で再導出し、
     cover conventionに基づく閉鎖候補行（主張3行＋余剰3行・閉鎖edge cost 484・
     28 canonical行分類 open 6/not-in-worklist 22/closed-before 0）の再決定、
   - 親delta（4親・すべてclass 2・14→11・51→48・47→44・69→66・計12）、frontier_after
     （6,130/485,759・solved 1,718・incidence 11,671・s6_needed 4,438・cost_needed 352,207）・
     五親target 77→80行・残余35→32行・win16候補 5→4根（主張12→9行）を含む全統計の再計算、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold24外部検証機（SHA-256 `9bc24e38…`）・fold25同梱独立監査機の設計を踏襲してよいが、
   root幾何・chain再構成の対象行はfold22のものとし、fold23/fold24の検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（pin入力2件・本レーンが選んだ offset:
   `inputs/worklist.csv` offset 1099 と K1125証明書 offset 21212）が
   fail-closed（returncode 1・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## やらないこと・非主張

- fold21 receipt単体の外部第二検証・fold23外部第二検証（`90ac8eed`所有）・
  fold25外部第二検証（`aad3b71ca`所有）・fold26 receipt fold（`23bffdd4e4`所有）・
  round-5 refsolve（`ace38772d9`所有）・WIN8-D10候補 `00000000010000809002000040002001`
  の証明書抽出（`63877ffd2e`所有）・WIN8証明書行共有監査（`c403614f`所有）は本宣言の対象外。
  新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証はreceipt簿記の再検査であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
