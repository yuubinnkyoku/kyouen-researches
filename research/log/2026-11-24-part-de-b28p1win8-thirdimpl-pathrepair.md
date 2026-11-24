# Part DE path repair: A1-A3 scaffoldのpath-prefix誤りと修復 (verdict不消費・実行前の事故)

- 2026-11-24T03:23Z (authoring time; commit timestampはGitHub側)
- 対象: 本Partは宣言 `5de0f35f` (repair `707be9a5`) のA1-A3 scaffold 3 commits
  `b96ce14b` / `04e2d5fe` / `451de93a` の**出版path**のみ。探索・検証・gate・verdictには一切触れない。

## 発生した事象

- A1-A3の 3 commitsは、宣言済み实验dir
  `research/experiments/n11-centralreply-closure-b28p1win8-thirdimpl-20261124/`
  の代わりに **repo root直下** `n11-centralreply-closure-b28p1win8-thirdimpl-20261124/`
  へpushされていた (push_filesへのpath渡しで `research/experiments/` prefixが欠落)。
- 検知経緯: 宣言済みpathでのfetch-back検証が main・commit SHA pin両方で67/67 "Not Found"。
  raw stale可能性との区別は get_file_contents のtree列挙と get_commit のfilename一覧で機械実施
  → root直下に実在、正pathに不存在、と確定。

## 内容検証 (誤path側で実施)

- root直下 (pin `451de93a`) の67ファイルをcommit-pinned fetchし、宣言 pin 群と同一byteである
  ローカルkit正本とsha256比較: **67/67 一致**。push内容自体は正しく、誤りはpathのみ。
- この時点で A1-A3 の「出版物byte検証」は内容面で完了 (path面は下記修復で解消)。

## 修復 (publish-then-execute規約に従い正pathへbyte同一再出版)

- R1 `a3b6361f`: scripts 7 + input 13 (A1相当)。
- R2 `fd1eb53f`: sources 37 = raw 16 + published-input 8 + published-input-bf 4 + top 9
  (A2相当・queue-registry 8c4216c6含む)。
- R3 `5465b6da`: val-gate 8 + canonical caches 2 (A3相当・CO 854800f3 / DB 04b0a239)。
- fetch-back: pin `5465b6da` で67/67 sha256一致、修復後HEAD `9bda85ce` pinでも67/67一致。
- root直下の誤配置68ファイル (67 + 計画外混入 `sources/.de-a2-bytecheck.txt`) は
  cleanup commits 68件で完全除去。root path 404を機械確認。git上に空dirは残らない。
  (stray bytecheckは宣言のsources 39集合に含まれないA2混入物であり、併せ除去した。)

## 影響範囲と主張の限定

- D1-D9の実行は**(全工程)未着手**のため、検証結果・gate・verdictへの影響はゼロ。
- verdict不消費 (対象8行は honest WIN labels のまま)・adoption不実施・閉鎖・被覆・secured・
  root勝敗の主張は一切しない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・対象8キー含む) は全時点でUNKNOWNのまま。**
- scaffoldの全ファイルは宣言 pin 群とbyte同一のため、D1-D9は正pathのscaffoldからそのまま継続可能。

## 記録 (将来のレーンへの教訓)

- fetch-back 404時は「raw stale」と「path誤り」を混同しない: 404が全文件一致で続く場合は
  get_commit (filename一覧) / get_file_contents (tree列挙) で実在pathを機械確認してから判断する。
- push_filesへ渡すpath群は、assembly時に宣言済み实验dir prefixの付与を1箇所で検査する。
