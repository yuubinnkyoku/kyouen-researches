id: K1193
title: "candidate-supply whole-record（K1075正本側）独立第二検証のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "candidate-supply whole-record K1075 independent second-verification pristine re-execution third verification"
  - "residual72系第二検証群のcandidate-supply whole-record分第三検証（出版byte 4点pin・W 15点2参照・検証機87 gate pristine 4回/battery×4 battery・harness監査111 gate 4巡byte一致）"
  - "出版監査byte再生成立（erratumなし・K1191運用知見の適用例）・fail-closedはSystemExit不書込型（tracebackなし・stderr文言が入力名決定的）・第三検証harness監査正本 365fbdfc…（gate 111〔pin 12・recon 61・rerun 23・tampers 15〕）"
relations:
  - type: depends_on
    target: K1075
    note: "検証対象の大もと。残余72行のfull cache-join候補供給再構築正本（49b6f85f…・54,282 bytes・25 check全PASS）に対するwhole-record経路の独立第二検証（87 gate: 生probe corpus再構成・dead sweep再構成・resolve6値同一性・fold鎖数値・join統計・phase-2供給解剖・resolve7クロスレーン整合）を第三の実行環境からpristine再実行する。"
  - type: related
    target: K1190
    note: "本レーンの同一手続き系列の先行成果（resolve7=K1072第二検証の第三検証）。本Kで対象検証機のfail-closedが同一のSystemExit不書込型であることを確認。"
  - type: related
    target: K1191
    note: "直前系列のreplace16第三検証。本Kは「rerun受入のbyte再生性は宣言前に予備実測してから課す」運用の適用例（本対象はbyte再生成立・erratumなし）。"
  - type: related
    target: K1192
    note: "本レーンの直前成果（36root-three-ply frontier=K1084第二検証の第三検証）。本KのW 15入力のうちk1075.jsonはK1192のW入力と同一正本・r7second.json（resolve7第二検証正本）はK1190の対象と相互参照。"
  - type: related
    target: K1144
    note: "residual72系の第三検証の先行例（4-sweep re-exec）。本Kの完結で残る未着手枠はrefuted50分のみ。"
artifacts:
  - path: research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-20261121/README.md
    role: source
    note: "対象・固定pin 4点・W入力15点・実施内容と結果（harness 111 gate内訳）・実験事実3項・再現手順・解釈規約（11,008 bytes・commit 4c8c95aa…）"
  - path: research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-20261121/scripts/verify_k1075_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・byte決定的監査JSON出力・合成input_dir方式・SHA-256 14857ca9…・18,523 bytes）"
  - path: research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-20261121/output/k1075-third-harness-audit.json
    role: audit
    note: "第三検証harness監査正本（14,992 bytes・gate 111〔pin 12・recon 61・rerun 23・tampers 15〕・all_gates_pass true・SHA-256 365fbdfc81d4d642a5a047e7cf50a531ebc9ded75a5d0ce778b354f2ce421798・4 battery byte一致）"
  - path: research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-20261121/output/reproduction.log
    role: record
    note: "battery 4巡の実行記録（1,364 bytes・SHA-256 e3f087ec…・B1/B2/B1f/B3所要時間・cmp結果・監査SHA照合4組）"
  - path: research/log/2026-11-21-n11-candidate-supply-whole-record-second-verification-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit 9e7ac2a1…・受入条件5項目・出版監査byte再生性を宣言前に予備実測し受入条件3をbyte一致条件で確定・tamper予備探針の読み取り順文言を宣言時に記載・先行宣言の不在を機械列挙で確認）"
  - path: research/log/2026-11-21-n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-verification.md
    role: record
    note: "研究log（発見順・判断・失敗記録〔B3初回のPATH起 因失敗と再実行〕）"
---

# K1193（candidate-supply whole-record=K1075正本側独立第二検証のpristine再実行第三検証）

担当: n11長期レーン。単一オーナー宣言（commit `9e7ac2a1fe6233ca1913acb4b495f8c5f64b7496`・宣言 2026-11-21T07:xxZ・受入条件5項目・**出版監査byte再生性を宣言前に予備実測して受入条件3をbyte一致条件で確定**・tamper予備探針の文言と読み取り順を宣言時に記載・先行宣言の不在を機械列挙で確認）の下で実施。

## 検証対象

K1075（残余72行のfull cache-join候補供給再構築・出版正本 `49b6f85f…` 54,282 bytes・25 check全PASS）に対する**whole-record経路の独立第二検証**。
出版は commit `3e0d2df9af0361fa73e000724ea5a0c458517250`（2026-11-19T21:55:31Z単一コミット・
実験dir 3ファイル〔README `69db6635…` 9,065 bytes・検証機 `scripts/k1075_second_verification.py` `f808279d…` 35,127 bytes・監査正本 `753f9a07…` 16,462 bytes〕+研究log `9724e961…` 3,331 bytes・87/87 gate全PASS・Publess17に先行する出版社レーンの単一オーナー宣言ノート〔2026-11-20出版〕が存在）。検証機は純stdlibで、生4-worker probe corpusからのK1069 live sweep分類再構成（98行・一意(root,ordering)78対・重複20行のdedup/agreement自前実装で39/39一致）・K1059 dead sweep REFUTED-D10再構成（witness_records 39件のprobe_runsから）・fold鎖/frontier数値（78−4−2=72の集合算術）・join統計の値同一性・phase-2供給解剖（row_demand再集計・witness 36根の72行ちょうど1回被覆でmaximum_matching=36）・resolve7クロスレーン整合を、幾何レーン（44 gate・D4/Bareiss）と非重複の**記録同一性経路**で検査する。
これを出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する**。
residual72系の第三検証は4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweeps・resolve7（K1190）・replace16（K1191）・36root-three-ply frontier（K1192）に続き、**candidate-supply whole-record分の第三検証は本Kが初号**。残る未着手枠はrefuted50分のみ（各レーン個別宣言の対象外）。

## 主結果

- pin stage（gate 12）: 対象4ファイル（README・検証機・監査正本・研究log）をpin commit `3e0d2df9` からraw固定URL取得・SHA-256+byte数照合（4点×2 gate・api.github.com非依存）し、宣言時現main HEAD `5487dad0` の同4ファイルがpin byteと一致することをbyte比較で再確認（4 gate）（計12 gate all PASS）。
- recon stage（gate 61）: W 15入力を2参照（ref_a = 宣言時HEAD `5487dad0…`・ref_b = 宣言commit `9e7ac2a1…`）のraw固定URLから取得し、各SHA-256が検証機内pinと一致・2参照間byte-identical・合成input_dir正規名配置後に再照合（15点×4 gate）+ 検証機本文配置後再照合（1）（計61 gate all PASS）。
- rerun stage（gate 23）: 出版検証機を改変なしpristine再実行4回/battery×4 battery（B1 fresh base・B2 同一base再実行・B1f fresh base独立capture・B3 隔離fresh base+`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd）で計16回。全回 rc=0・stdout `gates 87 all_pass True faithful True`・出力監査が**出版正本 `753f9a07…`〔16,462 bytes〕とbyte-identical**・battery内4回間でもbyte一致（x4 5 gate+相互3 gate・計23 gate all PASS・検証機1回約0.07秒）。**erratumなし（出版監査byte再生成立）**。
- tampers stage（gate 15）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456}/{5,678,9,012}/{51,234,8,765} のいずれとも別位置〔@33,333/@44,456〕）、**監査不在の探針環境**（probe-local出力pathの事前不在+事後不在を両assert）で実施:
  - t1 `sweep39dead.json` @33,333〔38,166 bytes内〕（`sorted(PINS)`読み取り15番目=最終）→ rc==1・stdout空・stderr末行 `pin mismatch for sweep39dead.json`・監査未書込・本番input W無改変。
  - t2 `k1075.json` @44,456〔54,282 bytes内〕（読み取り3番目）→ rc==1・stdout空・stderr末行 `pin mismatch for k1075.json`・監査未書込・本番input W無改変。
  - 2つのstderr文言は互いに異なる入力を特定し、**sweep39dead正本とK1075正本の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-errors`・t1は読み取り15番目〔最終〕・t2は3番目のfailで読み取り順独立性を含む）。検証機は最初のSHA不一致で `raise SystemExit("pin mismatch for <name>")`（tracebackを伴わない）となり監査JSONを一切書かない「監査不書込」型fail-closed（resolve7/replace16と同型）。
- finalize: harness監査正本（**14,992 bytes・gate 111〔pin 12・recon 61・rerun 23・tampers 15〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `365fbdfc81d4d642a5a047e7cf50a531ebc9ded75a5d0ce778b354f2ce421798`）が**4 battery**（B1 fresh base全stage〔1.4s〕→B2 同一base全stage再実行〔pin/recon再取得込み・1.4s〕→B1f fresh base独立capture〔1.5s〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1.4s〕）すべて111/111 PASSで**byte-identical**（`cmp`完全一致・4 capture同一）。

## 実験事実

1. **出版監査byte再生の成立とK1191運用の適用例**: 予備実測1回+本battery 4回/battery×4 battery=16回のpristine再実行すべて出版正本 `753f9a07…` とbyte-identical（**erratumなし**・replace16 K1191の「出版監査byte再現不能」型と対照的）。宣言前のbyte再生性予備実測（K1191で確立した運用）を経て、受入条件3は当初からbyte一致条件で確定した。K1192（t36）とあわせ運用の有効性が2例連続で確認された。
2. **fail-closed設計はSystemExit不書込型（tracebackなし）**: 検証機は `sorted(PINS)` の読み取り順でSHA照合し、最初の不一致で `raise SystemExit("pin mismatch for <name>")` が置き、監査JSONを一切書かない（fold10 gate-failed監査書込型・resolve7/replace16 SystemExit不書込型と同系列・t36のraise RuntimeError traceback型と対照的な「文言のみで終わる」終了型）。stderr文言は入力名で決定的であり、末行特定でgate記録可能。
3. **軽量対象の第三検査コストとW多数入力のrecon完動**: 検証機1回約0.07秒・battery 1巡約1.4〜1.5秒（pin fetch 8点+recon 15点×2参照+rerun 4回+tampers 2探針）。W 15点（正本JSON 11点+生probe記録4点）というresidual72系第三検証最大の入力数でも、reconは2参照×15点のraw fetchで完動し、全gateが機械処理で完結した。第二検証出版（2026-11-19T21:55Z）から約1.6日で第三検証確定。
4. **B3初回のPATH起 因失敗と再実行（battery設計の失敗記録）**: B3（`env -i`隔離実行）の初回は `PATH=/usr/bin:/bin` にpython3が無く `env: 'python3': No such file or directory` で即失敗した。PATHにpython3の実在bin dirを渡して再実行し、所要・byte一致とも受入どおり確定した。隔離batteryの起動はPATHの実在確認を含めて手続き化する（本K以降の隔離実験の運用知見）。

## 位置づけと限界

本検証はcandidate-supply whole-record第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行・幾何レーン（44 gate・D4/Bareiss）の再検査は一切行わない。幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではなく、共有表実装やworker分割変更の正当化ではない。nodes数・solved数・coverage数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。witness根・候補供給は条件付きdepth-10掃引計画で証明書ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
