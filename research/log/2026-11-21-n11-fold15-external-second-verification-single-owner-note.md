# 単一オーナー宣言ノート: fold15 receipt fold（root 120000038）の外部第二検証（2026-11-21）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold15（第22 receipt・5番目のWIN8 receipt fold・root `00000000012000003800080009000000`・
残余58行→55行・K1114証明書の五親S6 frontier receiptチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-21T01:30:00Z想定（push直前実測 2026-11-21T01:26:10Z）。
- 宣言時点の main HEAD: push直前再取得で確定（commit `132364c9` 以降の最新HEAD想定・
  取得失敗時は取得時点の最新HEAD）。
  fold15単体の外部第二検証の先行宣言なしを確認済み: 直近コミット列
  （2026-11-21T00:28Z以降、n11系は本レーンfold12外部第二検証（K1175）・
  fold13外部第二検証（K1176: 宣言 `5a9e814294`・part1 `f2fe7d58e9`/`dffc4af0c1`/`51d86169c1`・
  part2 `74fe6e1bb9`・part3 `9dac01caf6`）・fold14外部第二検証（K1178: 宣言 `2a6f14de95`・
  part1 `23de00dc`・part2 `30239f51`・part3 `132364c9`）・
  fold20 ext2→K1173/K1174第三検証群、four-row q6/q7 witness群（K1177・`d6b2c948`/`fc2fba7b`）・
  binary-cube GP-census群（K0568出版））にfold15単体ext2の宣言・実験・logは0件。
  fold13宣言ノート（`5a9e88...`→`5a9e814294`）の「fold14-16は各レーン個別宣言」記載どおり、
  本宣言がfold15単体の最初の宣言である。
- 対象出版物: `research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/`
  （出版実験dir 3ファイル: README・fold15機・receipt正本。builderファイルの同梱なし）
- 対象正本（SHA-256・byte数は2026-11-21T01:26Z時点の最新mainからの実取得で実測）:
  - fold15 receipt正本 `output/win8-root120000038-receipt-fold-20261120.json`
    `bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef`（20,759 bytes）
  - fold15 出版機 `scripts/fold_win8_root120000038.py`
    `03000c14f443bc4cf694e233d189fef159ef2b7a20420fa94c30879986ef771e`（52,350 bytes・
    fold14機の移行型・純Python・乱数・時刻なし）
  - 出版README `c1cd67687e14f8a7e047bc6819ce9121b8eb3ee9a8adc1ded3b22f954027ed1f`（8,678 bytes）
  - 直前のfold14 receipt正本（fold15機のchain直前段・fold15機内fold14 rerun gate対象）
    `ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71`（19,295 bytes）
  - fold14 出版機 `fold_win8_root9090022.py`
    `7b88a56565f897a858b90e273199651cb1cf8bb237480b9d78a592edf17c9252`（46,844 bytes）
  - fold13 receipt正本（fold13機のrerun gate対象）
    `c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae`（20,416 bytes）
  - fold13 出版機 `fold_win8_root9840004.py`
    `5c27f1ae1362c6f436e126786891bd4617ec92e403d22eff0b3b7537e51b0020`（42,315 bytes）
  - fold12 receipt正本（fold12機のrerun gate対象）
    `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`（19,322 bytes）
  - fold12 出版機 `fold_win8_root8005021.py`
    `706bfa7ae8b8ff022e2f05c91eb0c61da6bf3343805dce7ed7e35289bf3a906c`（37,868 bytes）
  - fold11 receipt正本（fold11機のrerun gate対象）
    `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`（17,008 bytes）
  - fold11 出版機 `fold_win8_root8003180.py`
    `9b3e06c8fcf5f37949a611dba57ce6546a7ced69a7e97b7588c66c588c55a5e1`（32,204 bytes）
  - K1114証明書検証正本（fold15 receipt の certificate_source記載・19 gate）
    `ab8cd535c14637c150c02ceeb688b335eb2da9dc1c5778b6a7c05a1a0906f67e`（5,374 bytes・
    `n11-residual58-win8-cert-extract-root120000038-20261120`）
  - K1114証明書本体 `win8-root-00000000012000003800080009000000-20261120.n11`
    `5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c`
    （1,171,958 bytes・32,470行・主張3行の候補・root mobility 53・fold15機の文言は
    「first 53-mobility fold」）
  - K1097 refsolve正本
    `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`（43,540 bytes・27 gate）
  - W入力pin（receipt `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 22 SHA-256 の計34件）は
    receipt から機械読み取りして再構成機と検証機の両方でfail-closed照合する。
    22 SHA-256 pinはfold14の19 pin（fold11/fold12/fold13/fold14正本・K1096・K1106・K1108・
    K1109/K1114監査/証明書・K1097・sv17・fs13・resolve6・fold10等の正本群）に
    fold14正本・K1114監査正本・K1114証明書を加えたものである。
    fold14機はpin表外の追加入力（rerun gate対象）として配置SHA照合する。

## 位置づけ

fold15の出版は出版社レーン自身の3実行byte一致・34 pin fail-closed・K1114 19 gate・
K1097 27 gate再照合・fold11/fold12/fold13/fold14出版機pristine rerun gate・fold10込み
チェーン全段frontier再計算を含む。
K1173/K1174のfold20外部検証機もfold12記録までを・K1175（fold12単体ext2）もfold12記録までで・
K1176（fold13単体ext2）はfold13記録までで・K1178（fold14単体ext2）はfold14記録までで
完結したため、**fold15 receipt自身の主張**（coverage 6行〔K1114/K1097主張3行＋余剰3行〕・
28 canonical行分類 open-frontier 6/not-in-worklist 22〔closed-before-this-receipt 0行〕・
closed edge cost 486・残余58→55・五親112行target 54→57・
frontier 6,179/489,440→6,173/488,954・solved 1,669→1,675・incidence 11,765→11,753・
needed 4,487→4,481・cost_needed 355,888→355,402・影響4親〔全c2: 13→10/62→59/54→51/40→37・
各3行closing・計12 row-closings・完全閉鎖0〕・win16候補 12→11根〔主張35→32行・
retired root `…120000038` 3行〕・root合法手53・K1114 g05 mobility 53〔gate名 g05_root_mobility_53〕・
g06 uncapped probes nodes 825,127/657,152・g13 nodes 2,723,200/2,141,807・証明書 1,171,958 bytes/32,470行・
third_method terminal 11,338/visited 69,115/winner 44,580/loser 13,197/応手辺 61,058/range [14,18]）の
第三実装による値単位の独立確認はまだない。
fold15の実験dirには独立監査機がないため、fold20外部第二検証（K1173）・fold12外部第二検証（K1175）・
fold13外部第二検証（K1176）・fold14外部第二検証（K1178）と同様に別実装再導出が検証の本体になる。

**宣言時点で確認済みの予備観察（検証実施時に精査・監査記録する）**:
fold15 receiptの `independent_verification.source_record` フィールドは
`research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120`（K1109・root 9090022・
fold14の証明書抽出実験）を指しているが、fold15自身の証明書抽出はK1114実験
（`n11-residual58-win8-cert-extract-root120000038-20261120`）であり、
`certificate_source.record`/`k1086_claims_record`・`verdict_join_summary`（K1114を正記載）と
整合しない。fold12 receiptでK1175監査がerratumとして記録したstale参照フィールドと
同種の文書フィールドである可能性が宣言時点の実測で確認されている。
検証実施時に本フィールドを検証機で精査し、判定をfold12/fold13/fold14との対照として
監査JSONのobservations欄に記録する（receiptのbyteは一切変更しない）。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群のSHA-256 pinを照合する
   （fold15機の入力pin表はreceiptから機械読み取りで確定させ、全34 pinをfail-closedで再照合する）。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold15機の入力pin全件の再照合・rerun gate・独立rerun用のfold14機の
   配置SHA照合・fold14機（および下流のfold11・fold12・fold13機）の入力pin表の
   fold15機pin表に対する部分集合性の機械確認）。
   K1175/K1176/K1178レーンで確立した静的raw URL再構成機設計（api.github.com非依存・
   全byte digest照合）を踏襲する。
3. fold15出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。`FOLD15_W` 不使用・機内向けrerun gate
   〔fold11機・隔離W複写上のfold12機・fold13機・fold14機〕は各回実行）。
   全実行のreceipt出力SHA-256が出版正本 `bae2b3c1…` とbyte-identicalであること。
   加えてfold14出版機を隔離W複写上で独立に再実行し、fold14正本 `ed3159fd…` と
   byte-identicalであることを確認する（fold15機が接続する上流rerun gateの外側からの再現）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold15機・fold14機・fold13機・
   fold12機・fold11機の幾何・集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む。
   K1178検証機の設計を踏襲してよい）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・firstFold系・fold4/fold56/fold912/secondThird・resolve6・fs13・sv17・
   fold10・fold11 receipt記録・fold12 receipt記録・fold13 receipt記録・fold14 receipt記録・
   fold15正本・K1114証明書・K1097 refsolveから:
   - base 6,438行からfold14適用後open frontier 6,179行/489,440・solved 1,669・
     incidence 11,765・残余58行・五親target 54/112行までのチェーン各段の再構成
     （fold9以前・fs13・fold10・fold11・fold12・fold13・fold14の各段published値との照合込み）、
   - K1114 root `00000000012000003800080009000000`（8石）の幾何（石数・quadruple-free・D4正準）と
     合法手53の独立再導出（survival-move規約の再実装）、C(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と28部分集合のD4正準化の各々）で再導出し、
     28 canonical行の分類（open-frontier 6/not-in-worklist 22）と coverage 6行
     （K1114 g07主張3行＋余剰3行）・各行cost/demand/parents・closed edge cost 486の再決定、
   - 親delta（影響4親・全c2: 13→10/62→59/54→51/40→37・計12 row-closings・完全閉鎖0）、
     frontier_after（6,173行/488,954・solved 1,675・incidence 11,753・needed 4,481/355,402）、
     五親target 54→57・残余58→55行（55行hex全列挙照合）・win16候補 12→11根
     （主張35→32行・retired root `…120000038` 3行・残余23行不交差）を含む全統計の再計算、
     - K1114監査19 gate主要値（g07主張3行〔`g07_k1086_root_claimed_coverage_3rows`〕・
       g06 uncapped probes nodes 825,127/657,152・g13 nodes 2,723,200/2,141,807・
       g05 mobility 53〔gate名 g05_root_mobility_53〕・証明書byte 1,171,958/行数32,470
       sorted unique・third_method集計〔K1114監査正本から機械読み取り〕・terminal_range照合）と
       K1097 27 gate・win16 footprintの root 120000038行の intrinsic == claimed == 3行・
       49行exactly-once partition・残余23行不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold14外部検証機（K1178・`d966dad5…`）の設計を踏襲してよいが、対象行・root幾何は
   fold15のものであり、fold16以降のreceipt・外部検証結果は入力に使わない。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset。
   fold14レーンの @200,222/@888,222 と異なる位置）がfail-closed（returncode≠0・正本未書込）で
   捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold15単体の外部第二検証に限定される。fold11単体ext2（`9be43128`・他レーン）・
fold12単体ext2（K1175・完了）・fold13単体ext2（K1176・完了）・fold14単体ext2（K1178・完了）・
fold16単体ext2（root 8890020・ただし本宣言の存在に依らず各レーンが個別に宣言する）・
fold17単体ext2（`095581932b`）・fold18/19/20/23/25/26の外部第二検証（fold20はK1173/K1174完了・
fold12はK1175完了・fold13はK1176完了・fold14はK1178完了・他は各所有者宣言済み）・
round-5 refsolve（`ace38772d9`）・WIN8 root `…40002001`証明書抽出（`63877ffd2e`）・
WIN8証明書行共有監査（`c403614f`）・n9-ge19（`21f8610664dd`）・n10 witness（`a6fb407c`）・
five-row q7 band-closure（`92722ac3`）・binary-cube GP-census（K0568完了）・
four-row q6/q7 witness frontier（`528ec9605b`・`d6b2c948`）は本宣言の対象外であり、
先行宣言があればそれに従う。
新規depth-10 probe・新規証明書抽出・行の閉鎖claimは本検証では一切行わない。
本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない（fold15時点残余58→55行は当該receiptの既出版簿記・
pool 120,416根は不変）。nodes数・solved数・coverage数を勝敗として読まない。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのままである。**
