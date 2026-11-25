# 単一オーナー宣言ノート: fold17 receipt fold（root 22081000）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold17（第24 receipt・7番目のWIN8-D10 receipt fold・root `00000000000000801202000022081000`・
残余51行→48行・K1117証明書rootの五親S6 frontierチェーンへのfold）出版成果に対する
**外部第二検証（単体ext2）**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T23:33:00Z
- 宣言時点の main HEAD: push直前再取得で確定させる（fold17単体の外部第二検証の
  先行宣言なしを確認済み: 直近83コミット〔2026-11-20T20:00Z以降〕にfold17単体ext2宣言は
  0件、唯一のfold17言及はfold18 ext2宣言ノートのfold17出版機SHA転写訂正
  `b64c2c9e`〔21:57:19Z・rerun gate機の照合用言及でfold17単体の着手宣言ではない〕、
  fold11単体ext2宣言 `9be43128`〔23:27:12Z・他レーン・fold12-16は別途宣言予定と明記〕、
  fold18 `c2e8eb09f`・fold19 `9606203ae`・fold20 `5f6c1b7a`〔完了〕・fold21=K1168・fold22=K1167・
  fold23 `90ac8eed`・fold25 `aad3b71ca`・fold26〔e53cc60c/ba659878〕・K1166第三検証 `ec24b235` の
  いずれもfold17単体を対象外。fold20宣言ノートもfold17以下を明示的に対象外としている）
- 対象出版物: `research/experiments/n11-residual51-win8-receipt-fold-root22081000-20261120/`
  （receiptの出版実験dir 3ファイル: README・fold17機・receipt正本。
  fold20出版と異なりbuilderファイルは同梱されない）
- 対象正本（SHA-256・byte数は2026-11-20T23:32Z時点の最新mainからの実取得で実測）:
  - fold17 receipt正本 `output/win8-root22081000-receipt-fold-20261120.json`
    `1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674`（22,925 bytes）
  - fold17 出版機 `scripts/fold_win8_root22081000.py`
    `e4c32aed731076e2032768b1e8252713bd586dcad08676e0af21668c2a8094c4`（61,371 bytes）
  - 出版README `786403013a6e18da5ea1846b939abc1e43b5995d1bf82b83fc5e3f3af45d4bce`
    （8,742 bytes）
  - 直前のfold16 receipt正本（fold17機のchain直前段）
    `edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b`（20,963 bytes・
    `win8-root8890020-receipt-fold-20261120.json`）
  - K1117証明書検証正本（fold17 receiptのcertificate_source記載・
    `n11-residual55-win8-cert-extract-root22081000-20261120`・39-mobility 3-claim WIN8
    候補・triple verification 19 gates）
    `3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9`
  - K1117証明書本体のSHA-256、およびfold16機・fold15機以下のチェーン機器群のSHA-256は、
    fold17機の入力pin表（receiptの `source_blob_pins`/`source_sha256_pins` と機内部pin表）から
    機械読み取りして再構成機と検証機の両方でfail-closed照合する

## 位置づけ

fold17の出版は出版社レーンの複数回実行byte一致・入力pin fail-closed・fold16出版機の
pristine rerun gate・チェーン全段frontier再計算を含む。fold18/fold19/fold20/fold21/fold22の
外部検証機はfold17記録をチェーン記録として機械照合したが、fold17 receipt 自身の主張
（frontier_before 6,168行/488,575 cost・solved 1,680・incidence 11,743・残余51行〔五親target
61/112行〕→ frontier_after 6,161行/488,094 cost・solved 1,687・incidence 11,729・残余48行〔
target 64/112行〕・coverage 3行・閉鎖7行〔solved差分〕・win16候補影響）の値単位の独立確認は
まだない。fold17の実験dirには独立監査機がないため、fold20外部第二検証（K1173）と同様に
別実装再導出が検証の本体になる。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記正本群のSHA-256 pinを照合する
   （fold17機の入力pin表は機械読み取りで確定させ、全pinをfail-closedで再照合する）。
2. W入力treeをrepo出版byteのみから再構築する（本レーンが書く固定Git参照つき
   reconstruct機: fold17機の入力pin全件の再照合・rerun gate用のfold16機以下の配置SHA照合・
   fold16機等の入力pin表のfold17機pin表に対する部分集合性の機械確認）。
3. fold17出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME 1回＋
   隔離+`PYTHONHASHSEED=random` 1回。`FOLD_PREVERIFIED_CHAIN` 不使用）。
   全実行のreceipt出力SHA-256が出版正本 `1175244d…` とbyte-identicalであること
   （fold16機pristine rerun gate とその内部の推移的再検証込み）。
4. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold17機やfold16機と
   幾何・集計補助関数を流用しない・fail-closed・証明書行の第三実装再検査を含む。
   K1168/K1173検証機の設計を踏襲してよい）で、worklist・census・audit・ledger/globalFold/
   previousCostFold・fold1..fold16 receipt記録・fold17正本・K1117証明書・K1097 refsolveから:
   - fold16適用後open frontier 6,168行/488,575 cost・solved 1,680・incidence 11,743・
     残余51行・五親target 61/112行の再構成（各段published値との照合込み）、
   - K1117 root `00000000000000801202000022081000` の幾何（石数・quadruple-free・D4正準）と
     合法手39の独立再導出（survival-move規約の再実装）、C(8,6)=28部分幾何のD4正準行を
     2方法（C(8,2) 2石除去×8 D4像の完全合成と28部分集合のD4正準化）で再導出し、
     28 canonical行の分類（open/not-in-worklist/closed-before）とcoverage 3行の再決定、
   - 親delta・frontier_after・五親target 61→64・残余51→48・win16候補影響・
     閉鎖7行の親クラス別会計を含む全統計の再計算と、出版receipt正本の
     全該当fieldの値単位照合、
   - K1117監査19 gate主要値（root幾何・mobility 39・probe統計・証明書byte・行数sorted unique）、
     K1097 refsolve 27 gate・footprint分割・residual23不交差の再照合、
   を独立に導出する。
5. tamper検査: 1 byte XOR改変（本レーンが選ぶ出版社未試験のpin入力2件のoffset）が
   fail-closed（returncode≠0・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`
   の3実行でbyte-identicalであること（時刻・実行時間フィールドを含まない決定論的設計）。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## 管轄の限界

本宣言はfold17単体の外部第二検証に限定される。fold11単体ext2（`9be43128`・他レーン）・
fold12-16単体ext2（fold11宣言ノートで別途宣言予告）・fold18/19/20/23/25/26の外部第二検証
（各所有者: `c2e8eb09f`/`9606203ae`/fold20=本レーン完了/fold26は所有者宣言 e53cc60c/ba659878）は
本宣言の対象外であり、先行宣言があればそれに従う。fold12-16が他レーン先着で宣言された
場合はfold17より前段の検証としてそちらを優先して参照する。新規depth-10 probe・
新規証明書抽出・行の閉鎖claimは本検証では一切行わない。本検証は検証の検証
（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、関係する行は1行も閉じない。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
