# 単一オーナー宣言ノート: fold19 receipt fold（root 1009000）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold19（第26 receipt・9番目のWIN8-D10 receipt fold・root `00000000000000801212000001009000`・
残余45行→41行・K1119証明書の五親S6 frontierチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T21:40:00Z
- 宣言時点の main HEAD: `9350457d99f02031ad3094974316765c9be6c758`
  （fold19単体の外部第二検証の先行宣言なしを確認済み: repo内 `単体`・外部第二検証宣言の
  全文検索で fold19 は未着手。fold20/fold21/fold22 の外部第二検証は fold21=`98c90cb510`〔K1168完了〕・
  fold22=K1167完了・fold23=`90ac8eed`・fold25=`aad3b71ca` が宣言・完了済みでいずれも対象外。
  fold19 receipt は fold20..fold22 の外部検証機で chain 記録として機械照合され、fold19機は
  rerun gate 対象として再実行済みだが、fold19 receipt 自身の主張に対する外部第二検証は
  本宣言が初めての着手である）
- 対象出版物: `research/experiments/n11-residual41-win8-receipt-fold-root1009000-20261120/`
  （receiptの出版 experiment dir 4ファイル: README・build機・fold19機・receipt正本）
- 対象正本（SHA-256・byte数はpinned commit `9350457d…` からの実取得で実測）:
  - fold19 receipt正本 `output/win8-root1009000-receipt-fold-20261120.json`
    `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae`（22,898 bytes）
  - fold19 出版機 `scripts/fold_win8_root1009000.py`
    `51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8`（68,386 bytes・1,028行）
  - fold19 生成機 `scripts/build_fold19.py`
    `7398d87b2457fac0a745e8eaf2a1c8f58c5db33088766d36cc1c2f56534439f0`（37,721 bytes）
  - 出版README
    `0dae2479969a2b6b9756959ff4f5242ad607334f4da45b60022dd9ea317e96c4`（9,515 bytes）
  - 直前のfold18 receipt正本
    `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`
  - fold18 出版機 `dcdfbf92d62409cc3a92f9f16f319e1328180622660b39791921b5de72800091`
  - fold18 preverified写し `d342f1f883d2e22ecca25903ec14ed24f16c77a0895e3ed022ab8832736e7f9e`
    （fold19機のpreverified rerun gateが隔離W複写（FOLD18_W）で1回実行する対象）
  - K1119証明書本体 `b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c`
    （587,989 bytes・16,262行）
  - K1119監査正本 `4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100`（19 gate）
  - K1091掃引正本 `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`
    （K1119監査g01のmaster pin）

## 位置づけ

fold19の出版は出版社レーン自身の3実行byte一致・preverified rerun gate採用設計
（fold11〜18の再帰rerun連鎖を廃し、直前機fold18のみpreverified写しで1回再実行し
fold18正本SHA `18b543c4…` と照合する設計・出版実測約3.0秒/実行）・46 pin fail-closed・
チェーン全段frontier再計算を含む。fold20外部第二検証（他レーン予定含む）・fold21外部第二検証
（K1168・本レーン）・fold22外部第二検証（K1167）はfold19 receiptをchain記録として扱い、
fold19機をrerun gateで再実行したが、fold19 receipt自身の主張
（open 5行閉鎖・主張4行＋余剰1行・closed edge cost 382・残余45→41行・
五親112行 target 67→71行・frontier 6,157/487,800 → 6,152/487,418・solved 1,691 → 1,696・
incidence 11,721 → 11,711・needed 4,465 → 4,460 / 354,248 → 353,866・
28 canonical行分類 open 5/not-in-worklist 23/closed-before 0・win16候補 8→7根〔主張22→18行〕）の
値単位の独立確認はまだない。そこで本検証では、fold19 receipt正本の全主張を第三実装で
出版byteだけから再導出する。fold19の実験dirにはfold24以降の同梱独立監査機がないため、
fold21/K1168・fold22/K1167と同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群（receipt・機・生成機・README・
   fold18正本・fold18機・preverified写し・K1119証明書・K1119監査・K1091正本）の
   SHA-256 pinを照合する。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold19機の入力46 pin〔12 Git blob pin + 34 SHA-256 pin〕をfail-closedで
   再照合し、preverified rerun gate用にfold18出版機とpreverified写しをSHA照合つきで配置し、
   fold19機自身をW rootにSHA照合つきで配置する）。
   fold18機の入力pin表がfold19機の46 pinの部分集合であることを、reconstruct機と検証機の
   両方が機械確認する（pin総数は機読み取りで確定させる）。
3. fold19出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   `PYTHONHASHSEED=random` 1回を含む・`FOLD_PREVERIFIED_CHAIN` 不使用）。
   全実行のreceipt出力SHA-256が出版正本 `c02d9a54…` とbyte-identicalであること
   （preverified fold18 rerun gate（fold18正本 `18b543c4…` 照合）とその内部の
   K1120 gate群推移的再検証込み）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold19機・fold18機と
   幾何・集計補助関数を流用しない）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・fold1..18 receipt記録・fold19正本・K1119証明書・監査・K1097 refsolveから:
   - fold18適用後open frontier 6,157行/487,800 cost・solved 1,691・incidence 11,721・
     残余45行・五親target 67/112行の再構成（fold9以前・windfall4等の各段published値との照合込み）、
   - K1119 root `00000000000000801212000001009000`（石 [12,15,24,49,52,57,60,71]）の
     C(8,6)=28部分幾何のD4正準行を2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、
     C(8,6)=28部分集合のD4正準化の各々）で再導出し、閉鎖候補行
     （主張4行〔cost 72/78/78/74〕＋余剰1行〔cost 80〕・閉鎖edge cost 382・
     28 canonical行分類）の再決定、
   - 親delta（影響4親・いずれもclass 2）、frontier_after（6,152/487,418・solved 1,696・
     incidence 11,711・needed 4,460/353,866）、五親target 67→71行・残余45→41行・
     win16候補 8→7根（主張22→18行）を含む全統計の再計算、
   - K1119監査19 gate主要値（g01 K1091 master pin・g05 mobility 44・
     g06 uncapped probes 192,365/229,502〔andclose1/andclose0〕・terminal石数範囲[14,18]・
     g07主張4行・g13 node会計 A1 865,602 / B 712,106・
     third_method 集計 terminal 5,783/visited 37,696/winner 24,352/loser 7,561/応手辺 34,261・
     証明書587,989 bytes・16,262行sorted unique・root幾何〔8石・quadruple-free・D4正準〕・
     合法手44の独立再導出）とK1097 27 gate・win16 footprint root 1009000行の
     intrinsic == claimed == 4行・49行exactly-once partition・residual23不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold21外部検証機（K1168・SHA-256 `322ad6ca…`）の設計を踏襲してよいが、
   対象行・root幾何はfold19のものとし、fold20/21/22外部検証の検証結果は入力に使わない
   （fold18適用後までのchain再計算まではK1168と同型の独立再実装とする）。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold19単体の外部第二検証に限定される。fold20単体・fold18以下の単体ext2・
fold23/25/26の外部第二検証（各所有者: `90ac8eed`/`aad3b71ca`/fold26 receiptは未着地）は
本宣言の対象外であり、先行宣言があればそれに従う。新規depth-10 probe・新規証明書抽出・
行の閉鎖claimは本検証では一切行わない。本検証は検証の検証（簿記・決定性・入力pin・
fail-closed防衛の再検査）であり、関係する行は1行も閉じない。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
