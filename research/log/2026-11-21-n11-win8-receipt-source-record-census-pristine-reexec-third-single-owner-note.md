# 単一オーナー宣言ノート: K1181（WIN8 receipt provenance census・n11-win8-receipt-source-record-census-20261121）のpristine再実行第三検証

本ノートは 11×11 長期レーンの衝突防止のため、既刊 K1181
（WIN8 receipt provenance census・folds 11-25 の15 receipt の
IV.source_record / certificate_source 機械判定・own 12 / stale 3・fold18 stale 新規発見・
コピー仮説 3/3・180 structural gate）出版成果に対する
**pristine再実行第三検証**（第三の実行環境から出版byteのみを再取得して再実行・
入力pin・fail-closed防衛・監査byte決定性を検査する）の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された場合は
本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-21T07:36Z
- 宣言時点の main HEAD: `f7466198215f9367d842aace9f772ee7fdd115a3`
  （07:29:21Z「n11: publish balanced 36-root worker partition candidate」・宣言直前の最新1コミット）
- 先行宣言の不在を機械確認済み: commit code search
  （`K1181 pristine` / `K1181 third` / `source-record-census third` /
  `source-record-census pristine reexec` の各クエリ0ヒット）・
  `research/log/` の census 系ノートは census 単一オーナー宣言（`32cb492c5b`）・研究log・
  part3修正記録の既刊のみで第三検証系ノートなし・
  `research/experiments/` に census 系 pristine-reexec-third dir なし・
  items は K1195 が最大で K1181 対象の第三検証項目なし。
  直近90コミットに K1181 census を対象とする宣言・実験・log なし。
  refuted50第三（`236586d0` 宣言・他レーン進行中）・fold11/17/18/19/23/25/26 単体ext2
  （いずれも他レーン宣言済み）・m22 class-split・s11 minimal-maximal・
  four-row q6 band extension・3行q4決定レーン（`72fdd106`）はいずれも本対象と無関係。
- 対象出版物（いずれも変更なしの再取得対象・固定pin）:
  - census 実験dir `research/experiments/n11-win8-receipt-source-record-census-20261121/`
    （4ファイル: README `689aa3b5…` 5,034 bytes・
    機械 `win8_receipt_source_record_census.py` `e7cffd18…` 12,983 bytes・
    census正本 `output/census.json` `c801564d…` 34,840 bytes・
    `output/reproduction.log` `e9076e7b…` 3,116 bytes）
    pin commit = part1 出版 `d9d1bfa8`（part2 `08e13676`・現mainともbyte一致を宣言前に実測済み）
  - K1181 item `265e4bf0…` 7,218 bytes（pin commit `08e13676`・現mainとbyte一致を確認済み）
  - census 研究log `2026-11-21-n11-win8-receipt-source-record-census.md` 5,314 bytes
    （宣言時HEAD `f7466198` 版をpin・`08e13676` 版からpart3修正記録コミット `02c4776d3`
    追加分を含む後追い更新を受けるため宣言時HEAD版を正本とする）
  - census 単一オーナー宣言ノート `43261ebd…` 3,539 bytes（pin commit `32cb492c5b`）
- 機械内pin: 対象機械の入力universeは機械内定数
  `PIN = 32cb492c5b13bdab00f5bdad11de06391fcb1274`（census 宣言出版HEAD）の
  静的raw固定commit URL 45 fetch（15 receipt JSON + 15 証明書 `.n11` + 15 検証JSON）に固定。
  第三検証はこの45入力を PIN と宣言時HEADの両refから取得してbyte一致
  （全45点で実測済み・unstable 0・receipt記載の certificate_sha256 / verification_sha256
  と実在byteのSHA-256一致45/45）を照合する。

## 宣言前予備実測（受入条件の根拠・宣言前に本sandboxで実測）

1. **pristine再実行**: 出版機械（`e7cffd18…`・byte一致確認後に無改変実行）で
   rc=0・stdout `census written: 15 receipts, 180 gates, stale folds: ['fold12', 'fold15', 'fold18']`・
   出力が出版census正本 `c801564d…` と**byte-identical**。
2. **45入力の2参照一致**: PIN `32cb492c` 版と現main版で45/45 byte一致。
3. **erratum候補の観測（ byte数記載不一致）**: 出版README・K1181 item・研究logは
   census正本を「34,758 bytes」と記載するが、実在byteは **34,840 bytes**
   （sha256 `c801564d…` は全記載と一致・純ASCII・文字数とbyte数の混同ではない:
   実測 34,840 bytes = 34,840 chars）。第三検証ではこの記載不一致を observations として
   記録する（出版byteは一切変更しない・erratum判断の権限は K1181 記録所有者に留保）。

## 検証環境の制約記録（tamper設計理由）

本sandboxはTLS証明書生成能力を持たない（openssl・cryptography・pip導入が禁止・
信頼CA秘密鍵不存在）ため、raw URL への通信内容改竄（MITM）は実施不可能。
このため内容系tamperは**pin済み45入力のbyte完備cacheをtransportとする注入runner**
（対象機械のbyteは不変・機械の `urllib.request.urlopen` の返り値のみを
cache由来に差し替える・差し替えのまま無改変実行）で実施し、
「cacheがpin byteを忠実に運ぶこと」をtamper前に注入対照実行（T0）で
census正本byte一致として立証する。あわせて真の通信不能系probe（T5・閉鎖port
proxy env によるfetch全失敗）を機械のpristine subprocess実行で実施する。

## tamper計画（探針位置は既知の全レーン探針位置と重複なし）

既知探針位置: fold12〜16第三 @{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/
{277,555,877,666}/{351,111,611,222}・fold20/21/22/24第三 @{7,777,500,000}/{253,17,522}/
{1,234,17,522,4,096}/{117,777,777,777}・fold20/fold15/fold16出版社試験 @{5,077,28,081}/
{208,888,919,191}/{300,111,740,321}・fold10 ext2第三 @{12,345,1,234,567}・
resolve7第三 @{2,345,23,456}・replace16第三 @{5,678,9,012}・t36第三 @{51,234,8,765}・
candidate-supply第三 @{33,333,44,456}・refuted50第三 @{16,789,25,678}
（いずれも本計画の @{4,936}/{543,210}/{4,321}/{11} と別位置・別入力file）。

- **T0（注入対照・正制御）**: cache注入のまま改竄なしで機械を実行 →
  rc=0・出版正本とbyte一致（注入transportの忠実度立証）。
- **T1** fold13 receipt JSON（20,416 bytes・`"verdict": "WIN8-D10"` 値先頭 byte）
  @4,936 XOR 0x20（`W`→`w`）→ gate「verdict not WIN8-D10 for fold13」fail-closed。
- **T2** fold12 証明書 `win8-root-…-8005021-20261120.n11`（945,298 bytes）
  @543,210 XOR 0x01（`0`→`1`）→ gate「own-dir certificate SHA-256 mismatch for fold12」
  fail-closed。
- **T3** fold25 検証JSON `win8-cert-extract-verification-20261120.json`
  （n11-residual29-win8-cert-extract-root…08180000 dir・5,654 bytes）
  @4,321 XOR 0x02（`,`→`.`）→ gate「own-dir verification SHA-256 mismatch for fold25」
  fail-closed（機械は検証JSONをparseしないためSHA gate単独発火が期待値）。
- **T4** fold11 receipt JSON（17,008 bytes）@11 XOR 0x02（1番目の`:`→`8`・schema行内部）
  → 受領直後の `json.loads` parse失敗 → `FAIL-CLOSED: parse …` fail-closed。
- **T5** 真の通信不能系: pristine subprocess を `https_proxy=http://127.0.0.1:9/`
  実行 → 最初のfetch失敗 → `FAIL-CLOSED: fetch error for …` fail-closed。
- 各T1〜T5とも: rc≠0・stderr先頭行 `FAIL-CLOSED:` ・出力 `output/census.json` 未書込
  （隔離run dirで実施後に不存在を検査）・探針後にpin byteを無改変で再取得照合。
- T1とT2/T3は互いに別入力・別gateの独立発火、T4はparse段階・T5はfetch段階の
  別失敗段階で、1 battery内で「parse前fetch / parse / verdict gate / 証明書SHA gate /
  検証JSON SHA gate」の5段階のfail-closed発火を確認する。

## 受入条件（battery はすべて本ノート出版後の第三実行環境で実施・api.github.com非依存・待機 pollingなし）

1. **pin**: 対象4+3ファイル（実験dir 4ファイル・K1181 item・研究log〔宣言時HEAD版〕・
   census単一オーナー宣言ノート）を各pin commitのraw固定URLから取得し
   SHA-256 + byte数を照合（7点とも出版値と一致）。あわせて宣言時HEAD版と
   宣言commit（本ノート）ref_b版のbyte一致を確認。
2. **recon**: 対象機械の45入力（15 receipt + 15 証明書 + 15 検証JSON）を
   機械内pin `32cb492c` と宣言時HEAD `f7466198` の両refから取得し、
   各SHA-256照合・2参照間byte一致・receipt記載SHA一致（45/45）・
   機械内定数（PIN・FOLDS 15 dir・15 receipt JSON名）の正しい固定を照合。
   注入cacheはPIN版を正本としてSHA照合のうえ構築。
3. **rerun**: 出版機械を改変なしpristine再実行（真のnetwork fetch・真のsubprocess）で
   1 battery 4回 × 3 battery（同一cwd 2回・隔離copytree+別cwd+別HOME 1回・
   隔離+`PYTHONHASHSEED=random` 1回・計12回）。各回 rc=0・stdout 一行一致・
   出力census.jsonが出版正本 `c801564d…`（34,840 bytes）とbyte-identical。
4. **tampers**: T0正制御 + T1〜T5計6探針がすべて上記期待どおりfail-closed
   （rc≠0・stderr `FAIL-CLOSED:`・出力未書込）・各探針後に本番W無改変再照合。
5. **finalize (監査byte決定性)**: 第三検証harness
   `verify_k1181_census_third_20261121.py`（stdlibのみ・stage分割
   pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対path/volatile排出なし）の
   出力監査JSONが3 battery（B1 fresh base全stage・B2 同一base全stage再実行〔pin再取得込み〕・
   B3 隔離base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`）でbyte-identical。
   失敗gateがある場合の監査書込はbattery内で1回のみ（fail-closed設計）。

## 位置づけ・非目標（解釈ガード）

- 本第三検証はcensus（報告）の**再現性・入力pin・fail-closed防衛・監査byte決定性**の
  検査であり、ゲーム木計算・証明書内容の検証・receipt fold・行の閉鎖を一切行わない。
  行は1行も閉じない。stale判定はprovenance記録誤り候補の報告であり、
  当該rootの証明書・検証の成否を左右しない。
- nodes数・solved数・coverage数を勝敗として読まない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
  receipt foldは行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
- 本レーンは K1181 記録（機械・正本・README・item・log）のbyteを変更しない。
  byte数記載不一致（34,758 vs 34,840）のerratum判断は記録所有者に留保し、
  本第三検証はobservations欄への記録のみを行う。

## 出版計画

- part1: 実験dir
  `research/experiments/n11-win8-receipt-source-record-census-pristine-reexec-third-verification-20261121/`
  （README・harness・監査正本・reproduction.log・fetch-back byte一致確認）
- part2: K item（K番号はpush直前に3点確認〔items/404・README grep・直近コミット〕で確定）+ 研究log
- part3: knowledge README の第三検証bullet追加（既存bullet温存・UTF-16 code unit照合→fetch-back byte一致）
