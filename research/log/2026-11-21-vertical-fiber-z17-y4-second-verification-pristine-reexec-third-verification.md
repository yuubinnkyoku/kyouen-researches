# vertical-fiber two-token z17-y4第二検証（K1079）のpristine再実行第三検証 — 研究log

- 日付: 2026-11-21
- 担当: 本レーン（ext2第三検証系列・単一オーナー）
- 単一オーナー宣言ノート: `research/log/2026-11-21-vertical-fiber-z17-y4-second-verification-pristine-reexec-third-single-owner-note.md`（commit `d6858a93679f5ce914f123505702dd4dde760731`・2026-11-21T07:02Z・宣言時HEAD `c1a2a333ea8a18263195ec79e111681643f9d7c4`・sha256 `e420f3fb…`）
- 成果物: `research/experiments/vertical-fiber-two-token-z17-y4-second-verification-pristine-reexec-third-20261121/`（part1 commit `1ca882335932e04dfa87b65d818250e7ef994ef4`）・本K item（K1195）

## レーン選定

ext2第二検証ラティス（25実験ディレクトリ）を俯瞰し、pristine re-exec第三検証が未着手なのは (a) refuted50-refsolve（他レーンがHEAD `236586d0` 06:44:52Zで単一オーナー宣言済み・着手禁止）と (b) vertical-fiber-two-token-z17-y4-second-verification-20261120（K1079）の2件のみ。後者を取得した（ラティス最後の未着手枠）。垂直繊維系の第三検証は境界切片出版（K1076）・第二検証（K1079）に続き本件が初号。

## 宣言と事前実測（発見順）

1. pin commit `2339957f…`・検体5ファイル（report.md `12a937dc…`/verify `83002a3b…` 19,036 bytes/census `5f84ccbd…`/audit.json `bfc2fb34…` 1,183 bytes/census.txt `48bde24a…` 6,801 bytes）をraw固定URLで取得し出版値と照合。K1076検証器固定ref `412d75b9…`（SHA `a7878b8e…`・blob `911dc4bf…`）の閉形式ブロック（6,677 bytes・`73435e45…`）が両subjectスクリプトにbyte-exact spliceされていることを抽出規約「`def odd(r:`先行〜`@lru_cache(maxsize=None)\ndef raw_recursive`直前の空白行1 byteを除く」で独立検証。
2. 宣言前予備実測（K1191運用）: pristine verify 1回 rc=0 31.7秒・監査byte一致。census 0.37秒・byte一致。tamper事前実測: t1 verify@2,257 XOR 0x01 rc=1 `AssertionError: (14, 19, 0)` output無し / t2 verify@11,908 rc=1 `AssertionError: (5, 10)` / t3 census@3,918 rc=0 census.txt `status=FAIL`・`mismatch_vs_published=5`（検出記録型・失敗設計5種目目）。byte再生性を確認したうえで受入条件をbyte一致条件として宣言した。
3. 単一オーナー宣言ノート出版: commit `d6858a93679f5ce914f123505702dd4dde760731`（07:02Z・fetch-back byte一致）。

## battery 実施（宣言ノート出版後）

第三検証harness `verify_z17y4v_third_20261121.py`（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対path/volatile排除・SHA `bfe265b4…` 19,086 bytes）を構築し、4 battery実施:

- B1（fresh base全stage）: 87 gate全PASS。
- B2（同一base全stage再実行・pin/recon再取得込み）: 140秒・監査正本B1と`cmp`完全一致。
- B3（隔離fresh base + `env -i` + 隔離HOME/TMPDIR + `PYTHONHASHSEED=random` + 別cwd）: 139秒・byte一致。
- B1f（fresh base独立capture）: 137秒・byte一致。

4 capture完全一致: 監査正本 `audit_z17y4v_third.json` SHA-256 `a9d310d7df5ea6cf259ca2319f6323d88941ebf7eb570b928f35b60c232ba3c5`（5,444 bytes・gate 87〔pin 24・recon 9・rerun 34・tampers 20〕・all_gates_pass true・解釈ガード5文+unknown guard）。rerunはverify 4回/battery×4 battery+予備1回=計17回・censusも17回、すべて出版正本とbyte-identical（erratumなし）。宣言ノートの受入条件はbattery 3を想定していたが、実施は4 batteryで上回って満たしている（実験dir READMEどおり誠実に記載）。

## 出版（3部構成）

- **part1**（実験dir 4ファイル一括）: commit `1ca882335932e04dfa87b65d818250e7ef994ef4`（2026-11-21T07:14:56Z）。push直後に発生した作業環境の圧縮を挟み、再開時にlist_commitsでHEAD=本コミット・メッセージ存在を確認したうえで、raw固定URL（pin commit版）fetch-backで4ファイルSHA-256照合・byte一致を確認（README `8462d51b…`・harness `bfe265b4…`・監査 `a9d310d7…`・reproduction.log `8fd4437a…`）。なお再開直後のfetch-back確認にtools経由のURL fetchを用いたところ、抽出テキストが出版byteと互いに微小に変化していた（+9/+2/+1/+2 byte）。これは当該fetch経路のテキスト抽出由来と特定し、curlによる生byte取得（`sha256sum`一致4点）でfetch-back照合を成立させた。検証・監査の内容には影響なし。
- **part2**（本log+K item）: K番号はpush直前3点確認（最新main README grep〔K1193まで〕・直近コミット〔K1194系なし〕・item path 404）に加え、refuted50第三検証レーンの宣言ノート（commit `236586d0`）が「K1193の次はK1194を想定」と明記しているため、**K1194を空けてK1195を採番**した（衝突回避・番号一意性は維持）。
- **part3**（knowledge README bullet）: 最新mainのREADMEを再取得し、並走コミット（K1189-K1193以降の増分）を温存したうえで自bulletのみ末尾append。

## 実験事実・知見

- (a) K1079第二検証の監査byte（audit.json・census.txtとも）は第三実装・第三実行環境でpristine再生（verify 17回・census 17回）すべてbyte一致。json sort_keys決定性・lru_cacheのcache_info報告値も含めpath・環境・hash seed非依存。
- (b) splice整合（K1076閉形式ブロックが両subjectスクリプトにbyte-exactで存在）を第三実装の抽出規約で機械確認。第二検証の根幹の第三検査成立。
- (c) tamper 3探針が3種の独立検出経路（生再帰子アンカー・第一導出閉形式照合・H3第三実装照合）で発火。t3により「検出を監査に記録する」型の失敗設計実測例が5種目として加わった（fold10書込型・resolve7/replace16 SystemExit不書込型・t36 RuntimeError不書込型・文言入SHA型〔refuted50第三ノート揭載〕に続く）。
- (d) **ext2第二検証ラティスの全枠が第三検証着手済み**となった（25実験dir。refuted50分は他レーン `236586d0` の受入待ち）。
- (e) 運用面: api.github.com core quotaが本実行中に枯渇した（rate_limit残0確認）。本レーンの検証・fetch-backはraw固定commit URL冪等取得で完結するため影響なし（api listはHEAD確認のみ使用）。HTML版コミットページ・README grepを代替手段として使用。K1193で記録された「隔離batteryのPATH起因失敗」は本レーンのB3では発生せず（宣言時点でPATH実在確認を含めて手続き化していたため）。1実行内で宣言から出版まで完結（battery 1巡約140秒×4+予備実測）。

## 位置づけと限界

本作業はK1079検体のpristine再実行検査であり、新しい全称主張ではない。z=17・y=4切片のGrundy分類の正しさはK1076のx外帰納と全R署名帯表による。K1076パッケージのbyte-pin不整合の修正はK1076レーン管轄。次候補はK1079 resume記載の z=17・y=5（B=K1076・C=1⊕K1074）/ z=18・y=4（B=K1078・C=1⊕K1076）で、いずれも着手前に単一オーナー宣言が必要。n11（標準11×11）の勝敗状態は本作業で一切変化しない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**nodes数・solved数・照合数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。
