# K1168（fold21外部第二検証）の出版後再現確認（2026-11-20）

本ノートは K1168（fold21（K1130）receipt foldの外部第二検証・part1 `3716fdbc`・
part2 item/log `f3b31970`・part3 README bullet `36fa231b`）の出版後に、
**出版byteをGitHubから取得し直して**同一の監査正本がbyte再生できることを実機で確認した
記録である（出版前のローカルbyteではなく、push後のrepo byteのみを使用）。

実施内容（21:31〜21:37Z）:

1. part1 commit `3716fdbc` から実験dir 5ファイル（README・reconstruct機 `a70b7983…`・
   検証機 `322ad6ca…`・監査正本 `80f00440…`・reproduction.log）をpinned-commit付きraw URLで
   再取得し、出版時のローカルstaged 5ファイルと`cmp`で5/5 byte一致を確認（fetch-back。
   日本語を含むREADME・logも含む全点一致）。
2. 検証機は再取得した出版byte（SHA-256 `322ad6ca…`・50,946 bytes）をそのまま実行した。
   Wは出版reconstruct機（`a70b7983…`）がref-B（検証時最新main `d323e780…`・宣言時HEAD
   `5e1273f57…` ともbyte一致確認済み）から再構成したW-B（52 pin fail-closed再照合込み・
   ref-A再構成のW-Aとfold21出力dirを除き全ファイルdiff一致）を、pubは同再構成のfold21出版dir 4点
   （receipt `9a4da2f6…`・機 `44399cc5…`・生成機 `51158e57…`・README `6e27c07b…`）を使用した。
   いずれもrepo byte由来で、出版に使ったローカルの検証機・証明書・正本の写しは使っていない。
3. 実行2回（21:36Z・21:37Z）: いずれもreturncode 0・`ALL 1394 GATES PASS`
   （P 13・I 60・C 1,292・X 15・T 14）・出力監査JSONが出版正本
   `80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63`（135,723 bytes）と
   byte-identical。1実行の実測wall 28秒（fold21出版機pristine再実行とfold20→fold18系
   rerun gate chain込み・検証機単独で完結）。

結論: K1168実験は**repoの出版byteのみから**（検証機はpart1出版byte、Wとpubは出版reconstruct機と
pinned Git参照、入力は出版チェーンbyte）第三者が同一の監査正本をbyte再生できる。
検証機の実行は、宣言ノート受入条件6項目で確認した5実行（同一cwd 2回＋隔離HOME別cwd＋
`PYTHONHASHSEED=random`＋ref-B W）に加え、post-publication 2実行の計7回すべてが同一SHA-256
`80f00440…` であった。本記録は検証の追加ではなく再現性の確認であり、K番号・README bulletは
不要（K1165/K1166のpostpub記録と同じ扱い）。

限界: 行は1行も閉じない。fold21時点残余38→35行はK1130の既出版簿記・pool 120,416根は不変。
nodes数・solved数を勝敗として読まない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
