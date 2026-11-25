# 単一オーナー宣言ノート: fold20 receipt fold（root 08d10000）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold20（第27 receipt・10番目のWIN8-D10 receipt fold・root `00000000000000003800000008d10000`・
残余41行→38行・K1121証明書の五親S6 frontierチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T23:09:08Z
- 宣言時点の main HEAD: `ec24b235f806822086680fee4075820679c78acf`（push直前再取得）
  （fold20単体の外部第二検証の先行宣言なしを確認済み: repo内宣言ノート・直近コミット列挙で
  fold18=`c2e8eb09f`〔21:52:44Z宣言・他レーン〕・fold19=`9606203ae`〔21:42:10Z宣言・他レーン〕・
  fold21=K1168完了〔当レーン〕・fold22=K1167完了→K1170 pristine再実行第三検証完了〔当レーン〕・
  fold23=`90ac8eed`・fold25=`aad3b71ca`・K1166第三検証=`ec24b235`〔いずれも他レーン〕が
  宣言・完了済みでいずれも対象外。fold18/fold19宣言ノートはfold20単体を「他レーン予定含み」と
  言及するがこれは宣言ではなく、fold21単体ext2（K1168・当レーン）がfold23宣言ノートの
  「別途宣言する」予告に対してfirst-published-priorityで取得した前例と同じ扱いである。
  fold20 receipt は fold21/K1168・fold22/K1167 の外部検証機で chain 記録として機械照合され、
  fold20機は rerun gate 対象として再実行済みだが、fold20 receipt 自身の主張に対する
  外部第二検証は本宣言が初めての着手である）
- 対象出版物: `research/experiments/n11-residual38-win8-receipt-fold-root08d10000-20261120/`
  （receiptの出版 experiment dir 4ファイル: README・build機・fold20機・receipt正本）
- 対象正本（SHA-256・byte数はpinned commit `ec24b235f806822086680fee4075820679c78acf` からの実取得で実測）:
  - fold20 receipt正本 `output/win8-root08d10000-receipt-fold-20261120.json`
    `76fd255bf16f0e434d15579cf148015bd564929e85e10172f0a0ef87015842a2`（24,684 bytes）
  - fold20 出版機 `scripts/fold_win8_root08d10000.py`
    `9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72`（70,951 bytes・1,055行・PREVERIFIEDスイッチ系譜・約4.8秒/実行）
  - fold20 生成機 `scripts/build_fold20.py`
    `4ba91cd09170d482426514bee89f3f0e0fcbe7fc70af6041dd9ae24decf921db`（36,412 bytes）
  - 出版README `637841d2e26f416cc5e4944e3ace1ec0e06878d63dfcabee470a46225230881a`（9,056 bytes）
  - 直前のfold19 receipt正本
    `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae`（22,898 bytes）
  - fold19 出版機 `51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8`（68,386 bytes・1,028行）
  - K1121証明書本体 `8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2`
    （1,026,202 bytes・28,328行）
  - K1121監査正本 `0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940`（5,373 bytes・19 gate）
  - K1091掃引正本（K1121監査g01のmaster pin）
    `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`

## 位置づけ

fold20の出版は出版社レーン自身の3実行byte一致・49 pin fail-closed
（12 Git blob SHA-1 + 37 SHA-256）・fold19出版機pristine rerun gate（fold19正本 `c02d9a54…` 照合・
fold18 preverified rerun とその reverse patch 検証・K1120 gate 群はこの rerun の内部で推移的再検証）・
チェーン全段frontier再計算を含む。fold21/K1168・fold22/K1167 の外部検証機は fold20 receipt を
chain 記録として扱い、fold20機を rerun gate で再実行したが、fold20 receipt 自身の主張
（open 8行閉鎖・主張3行＋余剰5行・closed edge cost 599・残余41→38行・
五親112行 target 71→74行・frontier 6,152/487,418 → 6,144/486,819・solved 1,696→1,704・
incidence 11,711→11,701・needed 4,460/353,866 → 4,452/353,267・
28 canonical行分類 open 8/not-in-worklist 20/closed-before 0・win16候補 7→6根〔主張18→15行〕）の
値単位の独立確認はまだない。fold20の実験dirにはfold24以降の同梱独立監査機がないため、
fold21/K1168・fold22/K1167と同様に別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群（receipt・機・生成機・README・
   fold19正本・fold19機・K1121証明書・K1121監査・K1091正本）のSHA-256 pinを照合する。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold20機の入力49 pin〔12 Git blob pin + 37 SHA-256 pin〕をfail-closedで
   再照合し、pristine rerun gate用にfold19出版機・fold18出版機・fold18 preverified写しを
   SHA照合つきで配置し、fold20機自身をW rootにSHA照合つきで配置する）。
   fold19機の入力pin表がfold20機の49 pinの部分集合であることを、reconstruct機と検証機の
   両方が機械確認する（pin総数は機読み取りで確定させる）。
3. fold20出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。`FOLD_PREVERIFIED_CHAIN` 不使用）。
   全実行のreceipt出力SHA-256が出版正本 `76fd255b…` とbyte-identicalであること
   （fold19機pristine rerun gate〔fold19正本 `c02d9a54…` 照合〕とその内部の
   fold18 preverified rerun・K1120 gate群推移的再検証込み）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold20機・fold19機と
   幾何・集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む）で、
   worklist・census・audit・ledger/globalFold/previousCostFold・fold1..19 receipt記録・
   fold20正本・K1121証明書・監査・K1097 refsolveから:
   - fold19適用後open frontier 6,152行/487,418 cost・solved 1,696・incidence 11,711・
     残余41行・五親target 71/112行の再構成（fold9以前・windfall4等の各段published値との照合込み）、
   - K1121 root `00000000000000003800000008d10000`（石 [16,20,22,23,27,59,60,61]）の
     C(8,6)=28部分幾何のD4正準行を2方法（C(8,2) 2石除去×8 D4像の完全合成224操作と、
     C(8,6)=28部分集合のD4正準化の各々）で再導出し、閉鎖候補行
     （主張3行〔cost 74/75/76〕＋余剰5行〔cost 80/83/70/72/69〕・閉鎖edge cost 599・
     28 canonical行分類 open 8/not-in-worklist 20/closed-before 0）の再決定、
   - 親delta（影響4親: class 4の2親〔79→77〔2行〕・80→78〔2行〕〕とclass 2の2親
     〔12→9〔3行〕・40→37〔3行〕〕・計10 row-closing・完全閉鎖0）、
     frontier_after（6,144/486,819・solved 1,704・incidence 11,701・needed 4,452/353,267）、
     五親target 71→74行・残余41→38行・win16候補 7→6根（主張18→15行）を含む全統計の再計算、
   - K1121監査19 gate主要値（g01 K1091 master pin・g05 mobility 50・
     g06 uncapped probes 564,695/673,870〔andclose1/andclose0〕・terminal石数範囲[14,18]・
     g07主張3行・g13 node会計 A1 2,428,240 / B 1,748,509・
     third_method集計 terminal 15,513/visited 83,544/winner 53,570/loser 14,461/応手辺 72,930・
     証明書1,026,202 bytes・28,328行sorted unique・root幾何〔8石・quadruple-free・D4正準〕・
     合法手50の独立再導出）とK1097 27 gate・win16 footprint root 08d10000行の
     intrinsic == claimed == 3行・49行exactly-once partition・residual23不交差の再照合、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
   検証機はfold21外部検証機（K1168・SHA-256 `322ad6ca…`）の設計を踏襲してよいが、
   対象行・root幾何はfold20のものとし、fold21/22外部検証の検証結果は入力に使わない
   （fold19適用後までのchain再計算まではK1168と同型の独立再実装とする）。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold20単体の外部第二検証に限定される。fold17以下の単体ext2・
fold18/19/23/25/26の外部第二検証（各所有者: `c2e8eb09f`/`9606203ae`/`90ac8eed`/`aad3b71ca`/
fold26 receiptは未着地〔所有者宣言 e53cc60c/ba659878〕）は本宣言の対象外であり、
先行宣言があればそれに従う。新規depth-10 probe・新規証明書抽出・行の閉鎖claimは
本検証では一切行わない。本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
関係する行は1行も閉じない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
