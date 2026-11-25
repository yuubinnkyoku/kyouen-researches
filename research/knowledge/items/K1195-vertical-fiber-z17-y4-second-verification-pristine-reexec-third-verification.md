---
id: K1195
title: "vertical-fiber two-token z17-y4第二検証（K1079）のpristine再実行第三検証"
kind: verification
status: verified
topics: [grundy, verification, certificates]
aliases:
  - "K1079 (published K1076 z=17 y=4 boundary slice second verification) pristine re-execution third verification"
  - "ext2第二検証ラティス（25実験dir）のz17-y4分第三検証（出版byte 5点pin・K1076閉形式ブロックsplice照合・検証機87 gate pristine 4回/battery×4 battery・harness監査 gate 87 4巡byte一致）"
  - "出版監査/censusのbyte再生成立（verify 17回・census 17回すべてbyte一致・erratumなし）・fail-closedは監査不書込型2探針+検出記録型（census書込 status=FAIL）1探針の5種目失敗設計実測・第三検証harness監査正本 a9d310d7…（gate 87〔pin 24・recon 9・rerun 34・tampers 20〕）"
  - "ext2第二検証ラティスの全枠着手済みの完結枠（refuted50分はK1194〔他レーン宣言 236586d0〕として相手レーンの受入待ち）"
relations:
  - type: depends_on
    target: K1079
    note: "検証対象。z=17・y=4切片のK1076閉形式に対する独立第二検証（17,254,465照合）を、第三の実行環境（本sandbox）が出版byteのみからpristine再実行・tamper・監査byte決定性を検査する。"
  - type: depends_on
    target: K1076
    note: "第二検証の固定ターゲット出版検証器（ref 412d75b9…・SHA-256 a7878b8e…・blob 911dc4bf…）の閉形式ブロック（6,677 bytes・73435e45…）が両subjectスクリプトにbyte-exact spliceされていることを第三実装の抽出規約で独立照合。K1076パッケージのbyte-pin不整合（a7878b8e… vs 監査pin 388e1a47…）の修正はK1076レーン管轄で本レーンは非対象。"
  - type: related
    target: K1189
    note: "本レーンの同一手続き系列の先行例（fold10 ext2第三検証）。api.github.com非依存のraw固定commit URL取得・監査不書込型fail-closed・harness監査の決定性設計を踏襲。"
  - type: related
    target: K1192
    note: "t36第三検証。tracebackに絶対pathを含むAssertionError系のgateは末行文言特定とする設計（path非含有で環境非依存）を本Kのt1/t2でも踏襲。"
  - type: related
    target: K1193
    note: "直前系列のcandidate-supply whole-record第三検証。宣言前予備実測でbyte再生性を受入条件に焼くK1191運用（erratumなし受入）を本Kも適用。K番号はK1194がrefuted50第三検証レーン（宣言ノート 236586d0 で K1194を想定と明記）のために空け、本KはK1195を採番。"
artifacts:
  - path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-pristine-reexec-third-20261121/README.md
    role: source
    note: "対象・固定pin・W構成・stage別結果（gate 87内訳・tamper 3探針表）・battery決定性・実験事実・再現手順・解釈規約（9,671 bytes・SHA-256 8462d51b…・commit 1ca88233…）"
  - path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-pristine-reexec-third-20261121/verify_z17y4v_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed〔監査JSONは全gate通過時のみ書込〕・時刻/絶対path/volatile排除・SHA-256 bfe265b4…・19,086 bytes）"
  - path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-pristine-reexec-third-20261121/audit_z17y4v_third.json
    role: audit
    note: "第三検証harness監査正本（5,444 bytes・gate 87〔pin 24・recon 9・rerun 34・tampers 20〕・all_gates_pass true・解釈ガード5文+unknown guard・SHA-256 a9d310d7…・4 battery byte一致）"
  - path: research/experiments/vertical-fiber-two-token-z17-y4-second-verification-pristine-reexec-third-20261121/reproduction.log
    role: record
    note: "宣言前予備実測+4 battery（B1/B2/B3/B1f）の実行記録（3,353 bytes・SHA-256 8fd4437a…）"
  - path: research/log/2026-11-21-vertical-fiber-z17-y4-second-verification-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit d6858a93…・宣言時HEAD c1a2a333…・受入条件5項目〔battery 3想定に対し実施は4 batteryで上回る満了〕・宣言前予備実測・tamper universe非重複offsetの記載・sha256 e420f3fb… 7,600 bytes）"
  - path: research/log/2026-11-21-vertical-fiber-z17-y4-second-verification-pristine-reexec-third-verification.md
    role: record
    note: "研究log（レーン選定・宣言・battery・出版3部構成・K1195採番の根拠・実験事実）"
---

# K1195（vertical-fiber two-token z17-y4第二検証=K1079のpristine再実行第三検証）

担当: 本レーン（ext2第三検証系列）。単一オーナー宣言（commit `d6858a93679f5ce914f123505702dd4dde760731`・2026-11-21T07:02Z・宣言時HEAD `c1a2a333ea8a18263195ec79e111681643f9d7c4`・受入条件5項目）の下で実施。第二検証出版（pin commit `2339957f76a548e75b23e9b73b3d5b4b172084f6`・2026-11-19T22:24:18Z）から約33時間で第三検証確定。

## 検証対象

K1079「出版済みK1076 z=17・y=4境界切片の独立第二検証」。検体は実験dir `research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/` の5ファイル（report.md `12a937dc…` 7,326 bytes・verify_z17_y4_second.py `83002a3b…` 19,036 bytes・census_z17_y4_second.py `5f84ccbd…` 9,806 bytes・output/audit.json `bfc2fb34…` 1,183 bytes・output/census.txt `48bde24a…` 6,801 bytes）。第二検証はK1076出版検証器（固定ref `412d75b9…`・SHA-256 `a7878b8e…`・git blob `911dc4bf…`）の閉形式ブロック「def odd〜expected_signature」（6,677 bytes・`73435e45…`）をbyte-exact spliceで固定ターゲットとし、当日K1076と独立に構築された複数オラクル（二種の生再帰・第三実装census・第一導出閉形式）で17,254,465照合するもの。検証機は完全自己完結（外部入力なし・stdlibのみ）。これを第三の実行環境が**出版byteのみから再取得してpristine再実行・splice整合の独立検証・tamper・監査byte決定性を検査**する。ext2第二検証ラティス（25実験dir）のうち第三検証未着手だった2枠のうちrefuted50分は他レーンが宣言済み（`236586d0`）で、本レーンは本件を取得した（**これでラティス全枠が着手済みとなった**）。

## 主結果

- pin stage（gate 24）: 検体5ファイルをpin commit `2339957f…` のraw固定URLから再取得しSHA-256+byte数照合・宣言時HEAD `c1a2a333…` の両refでbyte同一を確認。K1079 item・研究logがpin commit/宣言時HEAD/宣言commitの3 ref一致。宣言ノート `e420f3fb…` 7,600 bytesのpin。
- recon stage（gate 9）: K1076検証器が固定ref/HEAD/宣言commitの3 refでbyte同一（SHA `a7878b8e…`・blob `911dc4bf…`）。抽出規約（`def odd(r:`先行〜`@lru_cache(maxsize=None)\ndef raw_recursive`直前の空白行1 byteを除く）で抽出したブロックが6,677 bytes・SHA `73435e45…`で、verify/census両スクリプトのsplice（`PUBLISHED K1076 CLOSED FORMS`〜`END PUBLISHED K1076 BLOCK`マーカー間）とbyte一致。**K1079レーンのbyte-exact splice主張を第三実装で機械確認**。
- rerun stage（gate 34）: verifyを改変なしpristine再実行4回/battery×4 battery（同一cwd 2回・隔離copytree+別cwd+別HOME・隔離+`PYTHONHASHSEED=random`）+宣言前予備1回=計17回。全回 rc=0・`output/audit.json`が**出版正本 `bfc2fb34…`〔1,183 bytes〕とbyte-identical**・同一cwd 2回を含む4出力相互byte同一・1回約31.7秒。censusも同構成17回すべて rc=0・stdout `checks=2961 mismatch=0 status=PASS`・`output/census.txt`が出版正本 `48bde24a…`〔6,801 bytes〕とbyte-identical。**erratumなし（出版監査byte再生成立）**。
- tampers stage（gate 20）: 1 byte XOR 0x01探針3件（offset @{2,257/11,908/3,918}・既知の全レーン探針位置universeのいずれとも別位置・事前byte assert込み・事後W無改変再照合）:
  - t1 verify@2,257（出版ブロック側 g17y3 `odd(r, 1, 19)` '9'→'8'）→ rc=1・stderr末行 `AssertionError: (14, 19, 0)`（check 2 child_anchor_K1067の生再帰照合が検出）・output dir事前事後とも不在。
  - t2 verify@11,908（第一導出オラクル側 cand_pred x==5 `r>=10` '0'→'1'）→ rc=1・stderr末行 `AssertionError: (5, 10)`（check 6 first_derivation_vs_publishedが検出）・output dir不在。
  - t3 census@3,918（census側出版ブロック in_parent_P x==5 `r >= 10` '1'→'0'）→ rc=0・`output/census.txt`書込・**`status=FAIL`・`mismatch_vs_published=5`を記録**（checks=2961不変・byteは出版正本と不一致）。
  - t1/t2のstderr末行はpath非含有で環境非依存（gateは末行文言特定・t36第三 K1192と同じ設計）。t1とt2は異なるオラクル系（生再帰子アンカー vs 第一導出閉形式）が独立して同一改変を捕捉し、t3はcensusの失敗設計としての「検出を記録する」型（fold10 gate-failed監査書込型・resolve7/replace16 SystemExit不書込型・t36 RuntimeError不書込型・refuted50第三ノート掲載の文言入SHA型に続く**5種目の失敗設計実測**）を第三環境から機械記録した。**3探針が3種の独立検出経路で発火**。
- finalize: harness監査正本（**5,444 bytes・gate 87〔pin 24・recon 9・rerun 34・tampers 20〕・all_gates_pass true・解釈ガード5文+unknown guard・SHA-256 `a9d310d7df5ea6cf259ca2319f6323d88941ebf7eb570b928f35b60c232ba3c5`）が**4 battery**（B1 fresh base全stage→B2 同一base全stage再実行〔pin/recon再取得込み〕140秒→B1f fresh base独立capture 137秒→B3 隔離fresh base+`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd 139秒）すべて87/87 PASSで**byte-identical**(`cmp`完全一致)。宣言ノートの受入条件はbattery 3を想定していたが実施は4 batteryで上回って満たしている。

## 実験事実

1. **出版監査byte再生の成立**: verify 17回・census 17回（battery 16回+宣言前予備1回ずつ）すべて出版正本とbyte一致。json sort_keys決定性・lru_cacheのcache_info報告値（`ordered_states` 903,285等）も含め、path・環境・hash seedに非依存な決定性を第三実装・第三実行環境で確認。宣言前にpristine 1回+tamper 3探針を予備実測してbyte再生性を確かめてから受入条件をbyte一致条件として宣言に焼いた（K1191運用の適用・erratumなし）。
2. **splice整合の独立実装検証**: K1076出版検証器（11,517 bytes）からのブロック抽出規約を第三実装で実装し、6,677 bytes・`73435e45…`のブロックが両subjectスクリプトにbyte-exactで埋め込まれていることを機械確認。第二検証の根幹（「固定ターゲットが出版byteそのものである」こと）が第三環境から担保された。
3. **tamperの3経路独立性と5種目失敗設計**: 出版社ブロック側・オラクル側・census側の3点異なる改変が、生再帰子アンカー・第一導出閉形式照合・H3第三実装照合の3独立経路で検出されることを1 battery内で実証。t3により「検出を監査に記録する」型fail-closedの実測例が5種目として加わった。
4. **ext2第二検証ラティスの全枠着手済み**: 25実験ディレクトリ中の第三検証未着手はrefuted50（他レーン宣言済み `236586d0`・受入待ち）と本件の2枠であった。本件の完結で**ラティス上の全枠が第三検証着手済みまたは完了**となった。
5. **K1076 byte-pin不整合は非干渉**: K1079検出報告のK1076パッケージbyte-pin不整合（コミット済み検証器 `a7878b8e…` vs コミット済み監査pin `388e1a47…`）は、検体pinが静的であることを3 ref確認したことで第三検証に影響しない。修正はK1076レーン管轄のまま。

## K番号採番の記録

採番時点（2026-11-21T07:2xZ）の最新main READMEはK1193まで、直近コミットにK1194系なし。refuted50第三検証レーンの宣言ノート（commit `236586d0`・2026-11-21T06:44:52Z）が「K番号はpush直前3点確認で採番・**K1193の次はK1194を想定**」と明記しているため、**本項はK1194を空けてK1195を採番した**（push直前3点確認: README grep・items/直近コミット・本file path 404でK1195は空き）。番号の一意性は保たれ、refuted50レーンのK1194採番と衝突しない。

## 位置づけと限界

本検証はK1079第二検証の再現性・入力pin・splice整合・fail-closed防衛・監査byte決定性の第三検査であり、新しい数学的主張ではない。z=17・y=4切片のGrundy分類の正しさはK1076のx外帰納と全R署名帯表（有限監査はその補強・K1079の位置づけを継承）による。K1076パッケージのbyte-pin不整合の修正はK1076レーン管轄。nodes数・solved数・照合数を勝敗として読まない。z=17・y=5（B=K1076・C=1⊕K1074）とz=18・y=4（B=K1078・C=1⊕K1076）はK1079記載どおり別途単一オーナー宣言が必要な未着手候補。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**REFUTED-D10はLOSS証明ではない。
