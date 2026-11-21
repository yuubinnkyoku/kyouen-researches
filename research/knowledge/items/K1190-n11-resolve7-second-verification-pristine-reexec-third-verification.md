id: K1190
title: "resolve7（K1072）第二検証のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "resolve7 K1072 second-verification pristine re-execution third verification"
  - "residual72系第二検証群のresolve7分第三検証（出版byte 4点pin・W 12点2参照・検証機76 gate pristine 4回×3 battery・監査90 gate 3巡byte一致）"
  - "第三検証harness監査正本 0797c44e…（gate 90〔pin 6・recon 48・rerun 25・tampers 11〕）・出版社監査正本 42861008…（21,842 bytes）の3実行byte一致"
relations:
  - type: depends_on
    target: K1072
    note: "検証対象の大もと。resolve7（残余72行のpost-fold witness再照合・出版正本 207f4094…・27 gate）と、それに対する独立第二検証（K番号なし・commit e836dd12・76 gate全PASS・route A〜Dの4独立経路+r7全フィールド照合・監査正本 42861008…）を第三の実行環境からpristine再実行する。"
  - type: related
    target: K1189
    note: "本レーンの直前成果。fold10（第17 WIN7 receipt fold）ext2第三検証と同一手続き系列（単一オーナー宣言→pin/recon/rerun/tampers/finalize→3 battery）。t1のfail-closed挙動の対照点（fold10第二検証機は31 gate走行後に監査gate-failed書込、resolve7第二検証機は最初のpin不一致でSystemExit・監査不書込）。"
  - type: related
    target: K1144
    note: "residual72系の第三検証の先行例（4-sweep re-exec第二検証の第三検証）。本Kでresidual72系第二検証群のresolve7分の第三検証が確定。"
  - type: related
    target: K1075
    note: "残余72行への候補供給（candidate-supply cache-join再構築）。resolve7の供給ゼロ確定の対応物で、その正本の第三検証は次候補（本Kの対象外）。"
artifacts:
  - path: research/experiments/n11-resolve7-second-verification-pristine-reexec-third-20261121/README.md
    role: source
    note: "対象・固定pin・W入力12点・実施内容と結果・実験事実3項・再現手順・解釈規約"
  - path: research/experiments/n11-resolve7-second-verification-pristine-reexec-third-20261121/scripts/verify_resolve7v_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 9d755780…・14,754 bytes）"
  - path: research/experiments/n11-resolve7-second-verification-pristine-reexec-third-20261121/output/resolve7v-third-harness-audit.json
    role: audit
    note: "第三検証harness監査正本（11,948 bytes・gate 90〔pin 6・recon 48・rerun 25・tampers 11〕・all_gates_pass true・SHA-256 0797c44e1df1ce7bbc16873da335e888110b3db2a0822d152a5f28074fecfdee・3 battery byte一致）"
  - path: research/experiments/n11-resolve7-second-verification-pristine-reexec-third-20261121/output/reproduction.log
    role: record
    note: "battery 3巡の実行記録（972 bytes・SHA-256 b5bd7d35…）"
  - path: research/log/2026-11-21-n11-resolve7-second-verification-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit 86c6d546…・受入条件5項目・先行宣言の不在を機械列挙で確認）"
  - path: research/log/2026-11-21-n11-resolve7-second-verification-pristine-reexec-third-verification.md
    role: record
    note: "研究log（発見順・判断・失敗記録）"
---

# K1190（resolve7=K1072第二検証のpristine再実行第三検証）

担当: n11長期レーン。単一オーナー宣言（commit `86c6d546…`・宣言 2026-11-21T06:10Z・受入条件5項目・先行宣言の不在を機械列挙で確認）の下で実施。

## 検証対象

resolve7（K1072・残余72行のpost-fold witness再照合・出版正本 `207f4094…`・27 gate）に対する独立第二検証。
K番号をもたないext2出版（commit `e836dd127a90e520d8e2801e62b59eb4966f0ed8`・2026-11-19T21:33:29Z単一コミット・
実験dir `research/experiments/n11-residual72-resolve7-second-verification-20261120/`・
README `2a9405aa…`〔5,772 bytes〕/検証機 `695e56d7…`〔29,959 bytes・純stdlib・76 gate・route A〜Dの4独立経路（生probe記録からの39/39分類再構成・39-root割当3ソース一致・fold鎖78→74→72のリンクごと集合算術・fold10第二検証正本との閉鎖3行一致）+r7全フィールド照合〕/
出版監査正本 `42861008…`〔21,842 bytes〕+研究log `0659272d…`〔4,378 bytes〕）を、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する。
residual72系第二検証群では4-sweep re-exec（K1144）・replace9 sweep/whole-record・verdict-sweepsの第三検証が確定済みで、**resolve7分の第三検証は本Kが初号**。replace16・candidate-supply・refuted50・36root-three-plyの各ext2の第三検証は各レーン個別宣言の対象外。

## 主結果

- pin stage（gate 6）: 対象ext2の3機械ファイル（README・検証機・監査正本）をpin commit `e836dd12` からraw固定URL取得・SHA-256+byte数照合、3点とも出版値どおり（api.github.com非依存）。
- recon stage（gate 48）: W 12入力（fold10 `bed7d331…`〔12,918 bytes〕・fold10second `a62d6d50…`〔5,410〕・fold9 `24db2352…`〔24,399〕・probes-w{0..3}.jsonl `6b045eae…`/`4aaa4d0a…`/`2d4ff7dd…`/`e04e20bd…`〔13,206/13,221/11,266/10,293〕・resolve6 `e85d4bfb…`〔34,984〕・resolve7 `207f4094…`〔19,817〕・roots `9f0161a8…`〔9,231〕・sweep39 `22953ae1…`〔5,097〕・sv17 `c1073bae…`〔9,713〕）を2参照（ref_a = 宣言時HEAD `12eefdeae…`・ref_b = 宣言commit `86c6d546…`）のraw固定URLから取得し、各SHA-256が検証機内pinと一致・2参照間byte-identical・入力dir正規名配置後に再照合（各入力4 gate×12=48 gate all PASS）。probes-w*/roots.jsonのsnapshot pin（main@`ba5f9f4aad`基準）は宣言時点mainで12点すべてbyte一致（append-resume corpusの現況安定を第三環境から確認）。
- rerun stage（gate 25）: 出版検証機を改変なしpristine再実行4回/battery×3 battery（同一cwd 2回・隔離copytree cwd+`env`隔離HOME/TMPDIR 1回・隔離+`PYTHONHASHSEED=random` 1回）。全回 rc=0・出力監査JSON（gates_total 76・all_pass true・resolve7_record_faithful true）が出版正本 `42861008…`（21,842 bytes）とbyte-identical・4回間でもbyte一致・4出力相互同一（検証機1回約0.07秒・n11検証ラティス最小級〔PRISTINE予備実行0.07秒で出版監査正本とbyte一致〕）。
- tampers stage（gate 11）: 本レーン選択offsetの1 byte XOR 0x01（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{96,300,456,789} のいずれとも別位置）:
  - t1 `sweep39.json` @2,345 → rc≠0・stderr `pin mismatch for sweep39.json`（対象を正しく特定・監査未書込）・W復帰後byte無改変。
  - t2 `resolve6.json` @23,456 → rc≠0・stderr `pin mismatch for resolve6.json`・監査未書込・W復帰後byte無改変。
  - 2つのstderrが互いに異なる入力名を特定し、**2種の入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-gates`）。
- finalize: harness監査正本（**11,948 bytes・gate 90〔pin 6・recon 48・rerun 25・tampers 11〕・all_gates_pass true・時刻/絶対path/volatile排除・解釈ガード5文+unknown guard**・SHA-256 `0797c44e1df1ce7bbc16873da335e888110b3db2a0822d152a5f28074fecfdee`）が3 battery（B1 fresh base全stage・B2 同一base全stage再実行〔pin再取得込み〕・B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`）でbyte一致（battery 1巡約1.1秒）。

## 実験事実

1. **resolve7第二検証機のfail-closedは「監査不書込」型**: pin loopの最初の不一致でSystemExitし監査JSONを一切書かない。fold10第二検証機（31 gate走行後に障害gateのみ失敗・監査gate-failed書込）と対照的な2種目のfail-closed設計であり、両方とも第三環境から指定挙動どおりに作動した（n11検証ラティス内の設計多様性の実測）。
2. **snapshot pinの現況安定**: probes-w{0..3}.jsonl/roots.json（main@`ba5f9f4aad`基準のsnapshot pin）は宣言時点mainで成長せず、2参照byte一致が成立（append-resume corpusの静止を第三環境から確認。resolve7第二検証出版時に観察された15→20重複記録の成長はその後停止している）。
3. **最小級第三検証コスト**: 対象検証機1回約0.07秒・harness battery 1巡約1.1秒で、76 gateの独立再現・12入力の2参照固定・pin独立性・監査byte決定性を第三実装で検証可能（fold10 ext2第三検証の0.9秒と同水準・fold12〜16第三検証の14.4〜215.3秒と対照）。

## 位置づけと限界

本検証はresolve7第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行は一切行わない。nodes数・solved数・coverage数を勝敗として読まない。WIN7/WIN8-D10証明書は当該rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
