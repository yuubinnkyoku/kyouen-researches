# 単一オーナー宣言ノート: fold18 receipt fold（root 00901010）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold18（第25 receipt・8番目のWIN8-D10 receipt fold・root `00000000000000801202000000901010`・
残余48行→45行・K1120証明書の五親S6 frontierチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T21:54:00Z
- 宣言時点の main HEAD: `5d65700715e68f0ca123b96202a95b5f86d9f163`（push直前再取得・直前HEAD `9606203aec…` との差分は着他レーンn9-ge19 part3 `5d657007` のみを確認済み）
  （fold18単体の外部第二検証の先行宣言なしを確認済み: repo内宣言ノートの全列挙で
  fold19=`9606203aec`〔直前21:42:10Z宣言・他レーン〕・fold20=他レーン予定含み・
  fold21=K1168完了・fold22=K1167完了・fold23=`90ac8eed`・fold25=`aad3b71ca`
  が宣言・完了済みでいずれも対象外。fold18 receipt は fold19..fold22 の外部検証機で
  chain 記録として機械照合され、fold19機のpreverified rerun gate対象として再実行済みだが、
  fold18 receipt 自身の主張に対する外部第二検証は本宣言が初めての着手である）
- 対象出版物: `research/experiments/n11-residual48-win8-receipt-fold-root00901010-20261120/`
  （receiptの出版 experiment dir 3ファイル: README・fold18機・receipt正本）
- 対象正本（SHA-256・byte数はpinned commit `9606203aec…` からの実取得で実測）:
  - fold18 receipt正本 `output/win8-root00901010-receipt-fold-20261120.json`
    `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`（22,049 bytes）
  - fold18 出版機 `scripts/fold_win8_root00901010.py`
    `dcdfbf92d62409cc3a92f9f16f319e1328180622660b39791921b5de72800091`（65,777 bytes・再帰rerun gate設計・約186秒/実行）
  - 出版README `3b12d1d421f3d0ab2477af838a910fda8a8ee0c80df2ba0d2421e7f306348de1`（8,865 bytes）
  - fold17 receipt正本 `1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674`（22,925 bytes）
  - fold17 出版機 `e4c32aed731076e2032768b1e8252713bd586dcad08676e0af21668c2a8094c4`（61,371 bytes）
  - K1120証明書本体 `d6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1`
    （484,892 bytes・13,422行）
  - K1120監査正本 `ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516`（5,361 bytes・19 gate）
  - K1095掃引正本（K1120監査g01のmaster pin）
    `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`

## 位置づけ

fold18の出版は出版社レーン自身の3実行byte一致・43 pin fail-closed
（12 Git blob SHA-1 + 31 SHA-256）・fold17機隔離W複写（FOLD17_W）rerun gate
（fold17→fold16→…→fold11 の再帰rerun 8機連鎖込み）・チェーン全段frontier再計算を含む。
fold19..fold22 の外部検証機は fold18 receipt を chain 記録として扱い、fold18機を
preverified/rerun gate で再実行したが、fold18 receipt 自身の主張
（open 4行閉鎖・主張3行＋余剰1行・closed edge cost 294・残余48→45行・
五親112行 target 64→67行・frontier 6,161/488,094 → 6,157/487,800・solved 1,687→1,691・
incidence 11,729→11,721・needed 4,469→4,465 / 354,542→354,248・
28 canonical行分類 open 4/not-in-worklist 23/closed-before 1・win16候補 9→8根〔主張25→22行〕）の
値単位の独立確認はまだない。fold18の実験dirにはfold24以降の同梱独立監査機がないため、
fold21/K1168・fold22/K1167 と同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群（receipt・機・README・
   fold17正本・fold17機・K1120証明書・K1120監査・K1095正本）のSHA-256 pinを照合する。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold18機の入力43 pin〔12 Git blob pin + 31 SHA-256 pin〕をfail-closedで
   再照合し、再帰rerun gate用にfold11〜fold17出版機をSHA照合つきで配置し、
   fold18機自身をW rootにSHA照合つきで配置する）。
   fold11〜fold17機の入力pin表の連鎖を、reconstruct機と検証機の両方が機械確認する。
3. fold18出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。約186秒/回・再帰rerun gate込み）。
   全実行のreceipt出力SHA-256が出版正本 `18b543c4…` とbyte-identicalであること。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold18機・fold17機と
   幾何・集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む）で、
   worklist・census・audit・ledger/globalFold/previousCostFold・fold1..17 receipt記録・
   fold18正本・K1120証明書・監査・K1097 refsolveから:
   - fold17適用後open frontier 6,161行/488,094 cost・solved 1,687・incidence 11,729・
     残余48行・五親target 64/112行の再構成（fold9以前・windfall4等の各段published値との照合込み）、
   - K1120 root `00000000000000801202000000901010`（石 [4,12,20,23,49,57,60,71]）の
     C(8,6)=28部分幾何のD4正準行を2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、
     C(8,6)=28部分集合のD4正準化の各々）で再導出し、閉鎖候補行
     （主張3行〔cost 74/71/68〕＋余剰1行〔cost 81〕・閉鎖edge cost 294・
     1行がK1096/fold11閉鎖済み〔`00000000000000003800000008003000`〕を含む
     28 canonical行分類 open 4/not-in-worklist 23/closed-before 1）の再決定、
   - 親delta（影響4親・いずれもclass 2: 15→14〔1行〕・19→17〔2行〕・59→57〔2行〕・37→34〔3行〕・
     完全閉鎖0）、frontier_after（6,157/487,800・solved 1,691・incidence 11,721・
     needed 4,465/354,248）、五親target 64→67行・残余48→45行・
     win16候補 9→8根（主張25→22行）・residual23不交差を含む全統計の再計算、
   - K1120監査19 gate主要値（g01 K1095 master pin・g05 mobility 45・
     g06 uncapped probes 240,848/198,622・terminal石数範囲[14,18]・g07主張3行・
     g13 node会計 631,539/524,342・third_method集計 terminal 4,336/visited 30,999/
     winner 20,028/loser 6,635/応手辺28,516・証明書484,892 bytes・13,422行sorted unique・
     root幾何〔8石・quadruple-free・D4正準〕・合法手45の独立再導出）と
     K1097 27 gate・win16 footprint root 00901010行のintrinsic == claimed == 3行・
     49行exactly-once partition・residual23不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold21外部検証機（K1168・SHA-256 `322ad6ca…`）の設計を踏襲してよいが、
   対象行・root幾何はfold18のものとし、fold19〜fold22外部検証の検証結果は入力に使わない
   （fold17適用後までのchain再計算まではK1168と同型の独立再実装とする）。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold18単体の外部第二検証に限定される。fold20単体（他レーン予定含み）・
fold19/23/25/26の外部第二検証（各所有者: `9606203aec`/`90ac8eed`/`aad3b71ca`/fold26 receiptは未着地）・
fold17以下の単体ext2は本宣言の対象外であり、先行宣言があればそれに従う。
新規depth-10 probe・新規証明書抽出・行の閉鎖claimは本検証では一切行わない。
本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。

<!-- content-fix (fold23 839057fb / fold21 d323e780 precedent): corrected a one-character transcription slip in the fold17 machine sha256 (65-hex -> 64-hex, tail ...a8094c4c). Declaration time, acceptance items and jurisdiction are unchanged. Baseline measured bytes are unaffected (fold17 machine 61,371 bytes, sha256 ...(corrected value) as byte-verified during reconstruction). -->
