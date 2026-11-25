# K1173（fold20 receipt fold・外部第二検証）のpristine再実行第三検証: 研究log

実験日: 2026-11-20〜21
担当レーン: n11長期レーン（単一オーナー）
宣言: `research/log/2026-11-20-n11-k1173-fold20-ext2-pristine-reexec-third-single-owner-note.md`（commit `1d68addb`・2026-11-20T23:45:26Z・受入条件5項目）
item: K1174

## 時系列（UTC）

- 2026-11-20T23:44Z: 最新main（`992851e2`）・AGENTS.md・knowledge README（末尾bullet K1173まで）・K1173 item/part1-3 commit列を確認。K1173第三検証の先行宣言・実験・logなしを確認（他レーン宣言済み: fold11/fold17/fold18/fold19/fold23/fold25 ext2・fold26 receipt・round-5 refsolve・WIN8証明書抽出・WIN8行共有監査・n9-ge19・n10 witness。完了済み: K1166第三〔K1172〕・K1168第三）。
- 2026-11-20T23:45:26Z: 単一オーナー宣言ノートをmainへ出版（commit `1d68addb`・fetch-back byte一致・SHA-256 `b2e6f065…`）。push直前HEAD `992851e2`。
- 2026-11-20T23:46-23:48Z: K1173出版実験dir 5ファイル（part1 `f2213982`・監査正本は修正commit `cf453602`）をpinned byteから取得しSHA-256照合（5点とも出版値と一致）。
- 2026-11-20T23:49Z: 再構成機を改変なしで2参照実行（ref_a `992851e2`〔宣言時HEAD〕→W_A・ref_b `bb4d147b`〔検証時main〕→W_B・各49 pin + chain機4台・53ファイル・`diff -r` byte一致・fold19機入力pinの49 pin部分集合性）。
- 2026-11-20T23:50Z: 出版検証機の予備pristine再実行4回（同一cwd 2回・隔離copytree W/cwd/HOME〔`env -i`〕・隔離+`PYTHONHASHSEED=random`）がすべて rc=0・`ALL 1317 GATES PASS`・出力監査JSONが出版正本 `5a9bb98f…` とbyte-identical・gate count 1,317・4回間byte一致。予備tamper 2件（worklist@7777・K1121証明書@500000・本レーン選択offset）は rc=1・I-section pin gate fail・監査未書込でfail-closed捕捉・本番W無改変を事後再照合。
- 2026-11-20T23:56-00:01Z: 第三検証harness（stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）を起案・battery運用開始。開発中に2件の不具合を自レーンで捕捉: (1) FILES表の出版監査正本SHA-256に1文字誤挿入（`…ff277f4dc…`・正 `…ff27f4dc…`）→ pin stageの取得byte実測照合が即 `STAGE FAILED [pin]` で捕捉。(2) 初版finalizeがpartsを丸ごとauditに写し、毎回変動する `wall_ms_not_in_audit` が監査JSONに混入して3実行byte一致を壊す設計 → finalizeに再帰的な `*_not_in_audit` 除外を追加。いずれも出版前に捕捉・修正し、batteryを最初からやり直した。
- 2026-11-20T23:57Z: battery 2巡目の recon ref_b で `HTTP Error 403: rate limit exceeded`（api.github.com無認証quota・共有IP枯渇・core remaining 0）。K1167第三検証レーンの21:45Z枯渇と同じ失敗モード。固定refのため再実行は冪等。
- 2026-11-21T00:02Z: quota復旧待ちのpolling呼び出しが300秒bash上限を超過し、sandbox実行環境がリセット。出版前の作業dir一式（予備4回・隔離実行・tamper・draft・battery 1巡分）が消失。宣言ノートは出版済み（repoが正本）のため無被害。batteryは固定refから全成果を再取得・再実行する設計なので、復旧後に最初からやり直した。
- 2026-11-21T00:04:03-00:09:16Z: battery 3巡を完走:
  - battery 1（base b1・素環境・全stage再実行）: pin 10 gate → recon 12 gate（両参照53ファイル・diff clean）→ rerun 19 gate（4回とも `ALL 1317 GATES PASS`・監査SHA `5a9bb98f…`・4回間byte一致）→ tampers 8 gate（2件fail-closed・本番W無改変）→ finalize（gate 49・audit SHA `24fac0b9…`）。
  - battery 2（同一base b1で全stage再実行）: 全stage PASS・audit byte-identical（cmp）。
  - battery 3（隔離base + 隔離cwd/HOME/TMPDIR〔`env -i`〕+ `PYTHONHASHSEED=random`・battery全体実測約91秒）: 全stage PASS・audit byte-identical（cmp）。
  - 3巡のharness監査正本SHA-256 `24fac0b91c6e0e15a12a9f9a36b4b9f684dac7d25503801ceef3f45e0296834c`（6,213 bytes・gate 49・all_gates_pass true・時刻/絶対path/volatile排除）。
- 2026-11-21T00:11Z: part1出版（実験dir `research/experiments/n11-fold20-ext2-pristine-reexec-third-verification-root08d10000-20261120/` 4ファイル〔README `f7c965b0…` 8,616 bytes・harness `9cf2e6f9…` 17,424 bytes・harness監査正本 `24fac0b9…` 6,213 bytes・reproduction.log `6ccf0ac7…` 4,813 bytes〕・commit `a853b533`・fetch-back 4/4 byte一致）。push直前HEAD `92722ac3`（five-row q7 band-closureレーンの宣言ノート・自path非接触）。
- 2026-11-21T00:1xZ: part2出版（K1174 item・本log・fetch-back 2/2 byte一致）。K番号はpush直前3点確認（item path 404・直近commit列挙でK1174言及0件・knowledge READMEのK1174出現0件/最大K1173）で取得。

## 受入条件対照（宣言5項目）

1. **出版byte 5点のpin照合**: pin stage 10 gate PASS（SHA-256+byte数・fail-closed・3巡とも）。
2. **再構成機2参照実行・49 pin部分集合性**: recon stage PASS（両ref rc=0・`RECONSTRUCTED W`・12 blob行+41 sha256行・subset-check・`diff -r W_A W_B` 完全byte一致・53ファイル・3巡とも）。
3. **出版検証機pristine 4回**: rerun stage PASS（全回 rc=0・`ALL 1317 GATES PASS`・監査SHA `5a9bb98f…`・gate count 1,317・出版正本とbyte-identical・run間byte一致・3巡で計12回の pristine再実行）。
4. **本レーンoffset tamper 2件fail-closed**: tampers stage PASS（worklist@7777 blob pin gate・K1121証明書@500000 sha256 pin gate・いずれも rc=1・監査未書込・本番W事後無改変再照合〔worklist `6d8a449e…`・証明書 `8513e366…`〕・3巡とも）。
5. **harness監査の3実行byte一致・成果物出版**: finalize PASS（gate 49・all_gates_pass true）・battery 3巡の監査正本がbyte-identical・実験dir自己完結4ファイルをpart1で出版済み。

## 教訓

- 待機pollingは240秒以内に区切る（300秒超過で環境リセットを喰らい作業dirを失う。成果物はrepo出版が正本）。
- push_filesへのcontentはfile_system.read_fileの直読みで渡す（今回part1・宣言ともタイポ無し・訂正commit不要）。
- volatileフィールドは `_not_in_audit` 接尾辞の命名規約+finalizeでの再帰的除外で監査byte決定性を機械保証するのが有効。
- api.github.com quota枯渇は固定refの冪等再実行で復旧する（電子成果物に影響させない運用はK1167レーンと同じ）。

## 解釈規約

本検証はK1173第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
