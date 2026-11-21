# K1079第二検証（vertical-fiber two-token z=17 y=4境界切片）のpristine再実行第三検証

- 日付: 2026-11-21
- 対象: K1079「出版済みK1076 z=17・y=4境界切片の独立第二検証」（status computed・`research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/`）
- 状態: **第三検証成立（全87 gate PASS・4 battery監査byte同一・出版監査/censusのbyte再生性を第三実装・第三環境で確認）**
- 単一オーナー宣言: commit `d6858a93679f5ce914f123505702dd4dde760731`（2026-11-21T07:02Z・宣言時HEAD `c1a2a333ea8a18263195ec79e111681643f9d7c4`・受入条件5項目・先行宣言の不在を機械列挙で確認）
- pin commit（検体）: `2339957f76a548e75b23e9b73b3d5b4b172084f6`（2026-11-19T22:24:18Z・実験dir・研究log・K1079 itemの単一コミット出版）
- K1076検証器固定ref: `412d75b93d14752f528c4fa4c6b5d472a4ca5ac8`（検証器 `verify_z17_y4.py`・SHA-256 `a7878b8e…`・git blob `911dc4bf…`）

## 位置づけ

K1079の第二検証は「出版済みK1076検証器の閉形式ブロック（`def odd`〜`expected_signature`・6,677 bytes・SHA-256 `73435e45…`）をbyte-exact spliceで固定ターゲットとし、当日K1076と独立に構築された複数オラクル（順序保持/降順正準化の二種の生再帰・第三実装census・第一導出閉形式）で17,254,465照合」する。本第三検証はこの第二検証を第三の実行環境でpristine再実行し、(1)出版byteの機械再取得、(2)K1076固定ターゲットのsplice整合の機械検証、(3)監査byteの環境非依存決定性、(4)改変検出のfail-closed挙動、を独立に検査する。ext2第二検証ラティス（25実験ディレクトリ）のうち第三検証ディレクトリ が存在しなかった残り2件のうち refuted50分は他レーンが宣言済み（`236586d0`）で、本レーンは本件 vertical-fiber z17-y4 分を取得した。**これで第二検証ラティスの全枠が第三検証着手済みまたは完了となった。**

## 対象の同定とW構成

検体5ファイル（report.md `12a937dc…` 7,326 bytes・verify_z17_y4_second.py `83002a3b…` 19,036 bytes・census_z17_y4_second.py `5f84ccbd…` 9,806 bytes・output/audit.json `bfc2fb34…` 1,183 bytes・output/census.txt `48bde24a…` 6,801 bytes）をpin commitのraw固定URLから再取得してSHA-256+byte数を出版値と照合。K1079 item・研究logがpin commit/宣言時HEAD/宣言commitの3 refでbyte同一であることを機械確認。検証機は外部入力を持たない完全自己完結（閉形式・オラクルともソース内蔵・stdlibのみ）で、reconは「K1076出版検証器のbyte取得→ブロック抽出→両スクリプトのspliceとのbyte等価」を独立実装で行う。

## stage別結果（gate数・内容的担保）

| stage | gate数 | 内容 |
|---|---:|---|
| pin | 24 | 検体5ファイルがpin commit/宣言時HEADの両refで出版SHA-256+byte数一致・相互byte同一。item/logの3 ref一致。宣言ノート `e420f3fb…` 7,600 bytes のpin。 |
| recon | 9 | K1076検証器が固定ref/HEAD/宣言commitの3 refでbyte同一（SHA `a7878b8e…`・blob `911dc4bf…`）。ブロック抽出（`def odd(r:`先行〜`@lru_cache…def raw_recursive`直前の空白行1 byteを除く規約）が6,677 bytes・SHA `73435e45…`で、verify/census両spliceとbyte一致。 |
| rerun | 34 | verify 4回/battery×4 battery（計16回+宣言前予備1回=17回）すべて rc=0・stdout・`output/audit.json` とも出版正本 `bfc2fb34…` とbyte-identical・同一cwd 2回を含む4出力相互byte同一。census 17回すべて rc=0・stdout `checks=2961 mismatch=0 status=PASS`・`output/census.txt` が出版正本 `48bde24a…` とbyte-identical。1回約31.7秒。 |
| tampers | 20 | 下表の3探針。offset事前byte assert（`'9'`/`'0'`/`'1'`）込み。事後W無改変再照合。gate合計87。 |

### tamper探針（1 byte XOR 0x01・3種の独立検出経路・既知探針位置universeと非重複）

| 探針 | 対象/offset | 改変 | 挙動（全3 batteryで再現） |
|---|---|---|---|
| t1 | verify @2,257 | 出版ブロック側 g17y3 `odd(r, 1, 19)` の '9'→'8' | rc=1・stderr末行 `AssertionError: (14, 19, 0)`（check 2 child_anchor_K1067 の生再帰照合が検出）・output dir 事前事後とも不在（**監査不書込型fail-closed**・約1.2秒） |
| t2 | verify @11,908 | 第一導出オラクル側 cand_pred x==5 `r>=10` の '0'→'1' | rc=1・stderr末行 `AssertionError: (5, 10)`（check 6 first_derivation_vs_published が検出）・output dir 不在（約3.1秒） |
| t3 | census @3,918 | census側出版ブロック in_parent_P x==5 `r >= 10` の '1'→'0' | rc=0・**`output/census.txt` は書込まれるが `status=FAIL`・`mismatch_vs_published=5` を記録**（H3第三実装照合が検出・checks=2961不変・byteは出版正本と不一致） |

- t1/t2のstderr末行文言はpath非含有で環境非依存（traceback本体は絶対pathを含むためbyte比較対象外。K1192 t36第三と同じgate設計）。t1とt2は異なるオラクル系（生再帰子アンカー vs 第一導出閉形式）が独立して同一改変を捕捉し、t3はcensusの失敗設計としての「検出を記録する」型（fold10 gate-failed書込型・resolve7/replace16 SystemExit不書込型・t36 RuntimeError不書込型に続く5種目の失敗設計実測）を第三環境から機械記録した。

## finalize（battery決定性）

第三検証harness `verify_z17y4v_third_20261121.py`（SHA-256 `bfe265b48ff34c94ad565e4672eeea41b9d0b21a8b0783109253db50561c7333`・19,086 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed〔監査JSONは全gate通過時のみ書込〕・時刻/絶対path/volatile排除）の監査正本 `audit_z17y4v_third.json`（SHA-256 `a9d310d7df5ea6cf259ca2319f6323d88941ebf7eb570b928f35b60c232ba3c5`・5,444 bytes・gate 87〔pin 24・recon 9・rerun 34・tampers 20〕・all_gates_pass true・解釈ガード5文+unknown guard）が次の4 batteryでbyte-identical（`cmp`完全一致）:

- B1: fresh base全stage
- B2: 同一base全stage再実行（pin/recon再取得込み）140秒
- B3: 隔離fresh base + `env -i` + 隔離HOME/TMPDIR + `PYTHONHASHSEED=random` + 別cwd 139秒
- B1f: fresh base独立capture 137秒

battery 1巡約140秒（verify 4回×約31.7秒が主体）。第二検証出版（2026-11-19T22:24Z）から約33時間で第三検証確定。K1189の「軽量対象ほど早期に第三検証を潰す」運用の中堅適用例。

## 実験事実・知見

- (a) **K1079第二検証の監査byte（audit.json・census.txtとも）は第三実装・第三実行環境でpristine再生（verify 17回・census 17回・内訳はbattery rerun 16回+宣言前予備1回）すべてbyte一致**。json sort_keys決定性・lru_cacheのcache_info報告値（`ordered_states` 903,285等）も含め、path・環境・hash seedに非依存な決定性を確認。
- (b) **splice整合の独立実装検証**: K1076出版検証器（11,517 bytes）から「`def odd(r:` 〜 `@lru_cache(maxsize=None)\ndef raw_recursive` 直前（空白行1 byteを含む）の1 byte手前まで」の規約で抽出したブロックが、第二検証verify/census両スクリプトにbyte-exactで埋め込まれていることを第三実装で機械確認（K1079レーンのbyte-exact splice主張の第三検査）。
- (c) **K1191「byte再生性は宣言前に予備実測から受入条件に課す」運用の適用第n号**: 本レーンも宣言前にpristine 1回+tamper 3探針を予備実測し、受入条件5項目をbyte一致条件として宣言に焼いた。batteryは全5項目PASSで.erratumなし（replace16 K1191の「出版監査byte再現不能」erratum型と対照的）。
- (d) **ext2第二検証ラティスの閉鎖**: 25実験ディレクトリのうち第三検証未着手は refuted50（他レーン `236586d0` で着手済み）と本件の2枠であった。本レーンの宣言・受入で**本件が完了し、ラティス上の全枠が着手済み**となった（refuted50分は相手レーンの受入待ち）。
- (e) K1076パッケージのbyte-pin不整合（コミット済み検証器 `a7878b8e…` vs コミット済み監査 pin `388e1a47…`）はK1079の検出報告どおりで、本レーンでは修正を行わない（non-goals）。第三検証は影響を受けない（検体pinが静的であることを3 refで確認済み）。

## 限界

本項はK1079検体のpristine再実行検査であり、新しい全称主張ではない。z=17・y=4切片のGrundy分類の正しさはK1076のx外帰納と全R署名帯表（有限監査はその補強）による。z=17・y=5（B=K1076・C=1⊕K1074）とz=18・y=4（B=K1078・C=1⊕K1076）はK1079の記載どおり別途単一オーナー宣言が必要な未着手候補で、本レーンでは着手しない。n11（標準11×11）の勝敗状態は本項で一切変化しない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**nodes数・solved数・照合数を勝敗として読まない。

## SHA-256（本実験dir出版ファイル）

- verify_z17y4v_third_20261121.py: `bfe265b48ff34c94ad565e4672eeea41b9d0b21a8b0783109253db50561c7333`
- audit_z17y4v_third.json: `a9d310d7df5ea6cf259ca2319f6323d88941ebf7eb570b928f35b60c232ba3c5`
- reproduction.log: `8fd4437a9d68b1bc469067a75c213e0d5a626ae973f4b4b69d2f70cf919d7dc7`
- README.md: このファイル
