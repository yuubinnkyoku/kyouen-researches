# 単一オーナー宣言ノート: fold23 receipt fold（K1133）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold23（K1133・残余32行 WIN8-D10 receipt fold root `00000000000020809002000480100000`）
出版成果に対する**外部第二検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T18:55:00Z
- 宣言時点の main HEAD: `afd50466633b6c15f7a7bc0a2f5d1cc1bd58fda6`
  （fold22/fold23外部第二検証の先行宣言なしをcode search確認済み。
  fold24外部第二検証は本レーンが完了・出版済み〔K1164〕。fold25外部第二検証は別工程として宣言済み `aad3b71ca3`）
- 対象出版物: `research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/`
  （receiptの出版は単一コミット `2a116cb5d8b3cd313bb865600d235da3b2555daa`:
  README・ビルド機・fold23機・receipt正本の実験dir 4ファイル）
- 対象正本:
  - fold23 receipt正本 `output/win8-root208090020004-receipt-fold-20261120.json`
    SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`（25,106 bytes）
  - fold23 出版機 `scripts/fold_win8_root208090020004.py`
    SHA-256 `c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e`（82,697 bytes）
  - 直前のfold22 receipt正本 SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`
  - K1123証明書本体 SHA-256 `b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e`（855,258 bytes）
  - K1123監査正本 SHA-256 `6ea634c9fdd005626904669e08cb7139e59e78120c0b8c9e1dd48fde0b70ddf0`

## 位置づけ

fold23の出版は出版社レーン自身の3回実行（同一cwd 2回＋隔離W複写・別cwd・別HOME）
・fold22出版機のpristine rerun gate・チェーン全段frontier再計算までを含むが、
出版社以外の実行主体による第二検証はまだない（fold23の実験dirには出版社同梱の独立監査機がなく、
本検証はfold24外部第二検証〔K1164〕のような同梱監査の再実行項目を持たない分、
別実装再導出が検証の本体になる）。fold23 receiptはfold24外部第二検証が入力として
frontier 6,126/485,438の再導出で間接的に照合済みだが、fold23 receipt自身の主張
（open 4行閉鎖・closed edge cost 321・残余32→29行・frontier delta・28 canonical行分類・
win16候補 4→3根）の値単位の独立確認はまだない。fold23は出版済みWIN8証明書の
receipt foldとして最後のfold（fold23の成立によりreceipt foldは枯渇）である。
fold22 receipt正本（`f6e011f4…`）は本検証の再導出過程で
frontier照合の対象になるが、fold22 receipt単体の外部第二検証は本宣言の対象外とする
（別途宣言する）。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記5正本（receipt・機・fold22正本・K1123証明書・K1123監査）のSHA-256 pinを照合する。
2. 出版済み `research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/reconstruct_inputs.py`
   （fold24実験dir・SHA-256 `f4e1fa8e69b10c07d9eec7f0b798458b0e73a97308bd418b622d1e9542873591`・
   固定Git参照 `b91e85a99f0480f084835bdff51533d0cf5feaa8`）でWを再構成し、
   fold23機の58入力pin（12 Git blob pin + 46 SHA-256 pin）をfail-closedで再照合する
   （fold23のchain入力はfold24の61 pinの部分集合であることを機械確認する）。
3. fold23出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   `PYTHONHASHSEED=random` 1回を含む）。出力receipt JSONは全実行で出版正本
   SHA-256 `04f334ff…` とbyte-identicalであること（fold22機の隔離pristine rerun gate込み。
   `FOLD_PREVERIFIED_CHAIN` は不使用のpristine実行とする）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold23機の幾何補助関数を流用しない）で、
   worklist・census・fold1..21 receipt記録・fold22正本・K1123証明書・K1123監査・K1097 refsolveから:
   - fold22適用後open frontier 6,130行/485,759 cost・残余32行・五親target 80/112行の再構成、
   - K1123 root `00000000000020809002000480100000` のC(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成と、部分集合のD4正準化の各々）で再導出し、
     cover conventionに基づく閉鎖候補行（主張3行＋余剰1行・閉鎖edge cost 321・
     28 canonical行分類 open 4/not-in-worklist 22/closed-before 2）の再決定、
   - 親行delta（3親・すべてclass 2・9→8・11→9・55→53・計5）・frontier_after
     （6,126/485,438・solved 1,722・incidence 11,666・needed 4,434・cost_needed 351,886）・
     五親target 80→83行・残余32→29行・win16候補 4→3根を含む全統計の再計算、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   ただし本検証機はfold24外部検証機（SHA-256 `9bc24e38…`）の設計を踏襲してよいが、
   root幾何・chain再構成の対象行はfold23のものとし、fold24の検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（pin入力2件、出版社検査済みoffsetとは別位置）が
   fail-closed（returncode 1・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること。

## やらないこと・非主張

- fold22 receipt単体の外部第二検証・fold25外部第二検証（`aad3b71ca3`所有）・fold26 receipt fold・
  round-5 refsolve・WIN8-D10候補 `00000000010000809002000040002001` の証明書抽出は本宣言の対象外。
  新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証はreceipt簿記の再検査であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
