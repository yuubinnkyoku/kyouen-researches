# n11 fold12（root 8005021）外部第二検証: 宣言から出版までの記録（2026-11-21）

単一オーナー宣言 `research/log/2026-11-21-n11-fold12-external-second-verification-single-owner-note.md`
（commit `de32ca573b`・00:38:35Z出版・宣言 2026-11-21T00:41:00Z・受入条件6項目）に基づく
fold12 receipt fold（第十九 receipt・2番目WIN8 receipt fold・root
`00000000000000003800000008005021`）単体の外部第二検証の実行記録。
対象出版実験 `research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/`
（receipt `0f73795c…` 19,322 bytes・出版機 `706bfa7a…` 37,868 bytes・README `314a3728…`）。

## 時系列 (UTC)

- 00:35Z: セッション再開。最新main（`aed703c597`）でfold12〜fold16単体ext2の宣言なし・
  fold11/fold17等は他レーン宣言済みを確認。knowledge bulletの指示通りfold12単体ext2を
  本レーンの最も価値の高い未着手枠と判断。
- 00:38:35Z: 単一オーナー宣言ノート出版（commit `de32ca573b`）。fetch-back byte一致
  （SHA-256 `4475ed34…`）。受入条件6項目を宣言に含めた。
- 00:37-00:47Z: 対象正本・テンプレート機材（K1173 W再構成機・fold20検証機）を取得。
  W入力12 blob pinのうち9件は宣言前researchで静的URL解決済み。残る3件
  （worklist `2fee1d07…`・ledger `e8785d50…`・audit `7cdc7c9e…`）はapi.github.com
  trees APIでのby_sha走査を予定していたが、**無認証quotaが403枯渇**（回復01:04:10Z）。
  待機の代わりに静的パス探索に切替: fold4実験の出版機sourceのpin表（`fold_fourth_win7_
  receipt_20261119.mjs` 内 `const P`) からworklist・ledgerのrepo内パスを、
  cost16 five-parent幾何witness監査の研究logからaudit.jsonのrepo内パスを特定し、
  raw固定commit URL+blob-SHA-1照合で全3件解決（audit.jsonは15,611 bytes・`7cdc7c9e…`一致）。
- 00:52Z: `reconstruct_fold12_inputs.py`（api依存ゼロ・全25 pin fail-closed・
  fold11機pin表の部分集合性機械確認）を執筆・実行。W12再構成完了
  （25 pin全byte照合・fold11機 `9b3e06c8…` 配置・fold11 pin表 12+10 がfold12表と一致）。
- 00:54Z: fold12出版機をcwd=W12でpristine実行（rc=0・receipt `0f73795c…` byte一致・
  機内fold11 rerun gateもPASS）。OUTがcwd相対・rerun gateが `W/fold/output` 読み取り
  であるため実行はcwd==Wが正しいレイアウトと特定。
- 00:56-01:15Z: 第三実装検証機 `verify_fold12_external_20261121.py` を執筆
  （fold20検証機の設計踏襲・C1チェーンはfold11までに短縮〔fold12検証機はfold12以降の
  chain_step不使用〕・C2をK1106 19 gateに差替〔probes 619,138/751,581・cert 945,298
  bytes 26,083行・third_method 10,191/59,594/38,442/10,961/53,352/[14,18]〕・C3 root
  合法手41・C4 fold12 delta〔cost 584・5親・target 44→47・residual 65行全列挙〕・
  C5 K1097 27 gate+partition〔retired 2根: fold11 8003180+fold12 8005021〕・
  V = fold11機独立rerun・X 4回pristine〔各回ともfold11 rerun receipt byte確認〕・
  T tamper 2件〔本レーンoffset 96,300/456,789〕・E 監査JSON）。
  2つの実装bugを自力で捕捉・修正（X段のrmtree後読み取り、erratum文字列のquote）。
- 01:15Z: **全655 gate PASS**（初回実行・約14.4秒）。監査正本 `c309d693…`
  （70,149 bytes）を3実行（同一cwd 2回＋隔離cwd/HOME+`PYTHONHASHSEED=random`）で
  byte-identical生成。
- 01:17Z: reproduction.log・README執筆。
- 出版直前: 最新main再取得（HEAD `affb7c9ffd` 00:48:52Z・five-row q7 lane）。
  自レーン宣言 `de32ca573b` は保持・fold12 ext2への他レーン着手なし・自path無接触を確認。
- part1 3分割push: commit `20e5f2f215`（README・再構成機 `caa30f34…`・reproduction.log
  `d85d8c3d…`）→ `984c48a767`（検証機 `43afc1cd…`）→ `adb1e8f605`（監査正本 `c309d693…`）。
  **fetch-back 5/5 byte一致**（pinned commit `adb1e8f605` raw URL）。
- part2: knowledge item K1175（3点確認: items/のK1175〜K1185は404・knowledge README末尾は
  K1174まで・00:48Z時点コミットにK1175言及なし）＋本log。
- part3: knowledge README末尾bullet追記（base無損失・chunk連結・fetch-back byte検証）。

## 受入条件対照（宣言6項目）

1. 出版byte再取得+SHA照合: W再構成機が3ファイル（receipt・機・README）+25 pinを
   固定commit `de32ca573b` からbyte取得し、pin表はreceiptから機械読み取り。→ 達成。
2. W再構成機（pin再照合・rerun gate・fold11機配置SHA照合・部分集合性機械確認）: → 達成
   （api.github.com非依存の静的URL設計も付加）。
3. pristine 4回＋fold11機独立rerun: → 達成（4回ともreceipt出力byte一致・各回の機内
   fold11 rerun出力byte一致・加えてvr段でfold11機をW複写上で独立実行し `d7bf2cd5…` 再現）。
   注: 全runとも実行環境上の制約で `FOLD12_W` をbyte-pinnedなW12またはその完全複写に
   明示指定（K1173 fold20 ext2の `FOLD20_W` 実行matrixと同一形式。W内容は全pin照合済み）。
4. 別実装検証機による全再導出: → 達成（655 gate。チェーン8記録再計算・K1106 19 gate・
   root幾何41・2方法28行・coverage cost 584・5親delta・frontier_after全統計・残余65全列挙・
   win16 partition・K1097 27 gate）。
5. tamper 2件 fail-closed: → 達成（worklist @96,300・証明書 @456,789。
   rc≠0・fold12/fold11出力未書込・本番W無改変再照合）。
6. 監査正本3実行byte一致: → 達成（`c309d693…` 3回）。

## 実験事実

1. api.github.com無認証quota枯渇（403・shared IP・01:04:10Z回復予定）が再発。trees APIの
   by_sha走査を諦め、repo内の出版機source pin表と研究logから静的パスを特定することで
   待機せずにW12を再構成した。静的URL+blob/SHA照合のfallback設計は以降の
   fold13-16単体ext2にもそのまま使える（検証レーンの再現性向上）。
2. **出版receipt側のerratum特定**: fold12 receiptの `independent_verification.source_record`
   がfold11証明書抽出実験のパス（root 8003180）を指したままでK1106（root 8005021）を
   指していない。fold12機sourceの固定文字列（`fold_win8_root8005021.py` 内
   `independent_verification` ブロック）由来の文書エラーで、`certificate_source` ブロック・
   全sha pin・統計は正しい。監査JSONのobservations欄にerratumとして記録した
   （検証失敗ではなく出版記載の訂正事項。fold12 receiptのbyteは一切変更せずそのまま）。
3. fold12機のOUTはcwd相対（`fold12/output/...`）でrerun gate読み取りは `W/fold/output`
   絶対パス。実行はcwd==Wで行う必要があり、検証機X段のexecution matrixはこの点を明示して
   いる（fold20機はW絶対OUTでcwd自由と異なるレイアウト差）。
4. fold20検証機流用時の置換点を3箇所学習: (a) chain_step対象はfold10・fold11のみで
   打ち切り（fold12検証機はfold12以降のreceiptを入力にしない）・(b) C4の「閉鎖行は
   class-1 demandゼロ」はfold20固有gate（fold12の余剰行はc1要求を持つ）なので5親の
   分類別件数gateに置換・(c) controls件数（19）・receipt ordinalなどのレシート定数群。
   教訓としてfold13-16検証機にも当てはまる。

## 解釈規約（判定は変わらない）

本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、行は1行も
閉じない（fold12時点残余68→65行は当該receiptの既出版簿記・pool P⁗ 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
