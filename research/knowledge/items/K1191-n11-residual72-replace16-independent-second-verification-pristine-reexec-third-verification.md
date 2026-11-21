id: K1191
title: "replace16（K1089）独立第二検証のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "replace16 K1089 independent second-verification pristine re-execution third verification"
  - "residual72系第二検証群のreplace16分第三検証（出版byte 3点+HEAD照合pin・W 5点2参照+runner blob SHA-1・検証機16 gate pristine 4回×3 battery・監査75 gate 3巡byte一致）"
  - "出版監査jsonのerratum確定（差分正確に2点: gainsHistキー順・最終guard文末句点）・第三検証harness監査正本 569c6bbd…（gate 75〔pin 9・recon 22・rerun 23・erratum 10・tampers 11〕）"
relations:
  - type: depends_on
    target: K1089
    note: "検証対象の大もと。replace16（残余72行の代替16根掃引・出版正本 808fbda1…・16根の32 probe記録）と、それに対する独立第二検証（K1093・commit 45a3f3b2・16 gate全PASS・別実装D4変換と4×4整数行列式で16根1,120四点組・72基底行1,080四点組再検査・監査 1486d35e…）を第三の実行環境からpristine再実行する。"
  - type: related
    target: K1093
    note: "replace16独立第二検証の出版item。本Kでその第三検証（再現性・入力pin・fail-closed・監査byte決定性・出版監査jsonのerratum確定）が完了。"
  - type: related
    target: K1190
    note: "本レーンの直前成果。resolve7（K1072）第二検証の第三検証と同一手続き系列（単一オーナー宣言→pin/recon/rerun/erratum織込み/tampers/finalize→3 battery）。replace16分はresidual72系第二検証群の第三検証2号。"
  - type: related
    target: K1144
    note: "residual72系の第三検証の先行例（4-sweep re-exec）。第三検証未着手枠はcandidate-supply・refuted50・36root-three-plyが残る（各レーン個別宣言対象）。"
artifacts:
  - path: research/experiments/n11-residual72-replace16-independent-second-verification-pristine-reexec-third-20261121/README.md
    role: source
    note: "対象・固定pin・W入力5点・実施内容と結果（erratum 10 gate）・実験事実3項・再現手順・解釈規約"
  - path: research/experiments/n11-residual72-replace16-independent-second-verification-pristine-reexec-third-20261121/scripts/verify_replace16v_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/erratum/tampers/finalize・fail-closed・SHA-256 e8a1431a…・18,919 bytes）"
  - path: research/experiments/n11-residual72-replace16-independent-second-verification-pristine-reexec-third-20261121/output/replace16v-third-harness-audit.json
    role: audit
    note: "第三検証harness監査正本（10,189 bytes・gate 75〔pin 9・recon 22・rerun 23・erratum 10・tampers 11〕・all_gates_pass true・SHA-256 569c6bbda909d4f3993ffaee64395d9a62911e7cddb49added51abb87393e545・3 battery byte一致）"
  - path: research/experiments/n11-residual72-replace16-independent-second-verification-pristine-reexec-third-20261121/output/reproduction.log
    role: record
    note: "battery 3巡の実行記録（1,087 bytes・SHA-256 d3da6e78…）"
  - path: research/log/2026-11-21-n11-replace16-second-verification-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit 19c4eea1…・受入条件5項目・erratum織込み修正版受入条件3・先行宣言の不在を機械列挙で確認）"
  - path: research/log/2026-11-21-n11-replace16-second-verification-pristine-reexec-third-single-owner-note-addendum.md
    role: erratum
    note: "宣言ノートのgainsHist例示値誤記訂正addendum（commit f89d5ae6…・正 {"2":2,"3":11,"4":3}）"
  - path: research/log/2026-11-21-n11-replace16-independent-second-verification-pristine-reexec-third-verification.md
    role: record
    note: "研究log（発見順・判断・失敗記録）"
---

# K1191（replace16=K1089独立第二検証のpristine再実行第三検証）

担当: n11長期レーン。単一オーナー宣言（commit `19c4eea1…`・宣言 2026-11-21T06:2xZ・受入条件5項目・erratum織込み修正版受入条件3・例示値誤記はaddendum `f89d5ae6…`で訂正）の下で実施。

## 検証対象

replace16（K1089・残余72行の代替16根掃引・出版正本 `808fbda1…`）に対する独立第二検証。
K1093出版（commit `45a3f3b2b1394fc259ba3269b0a11b37fab20a57`・2026-11-20T00:44:22Z単一コミット・
実験dir `research/experiments/n11-residual72-replace16-independent-second-verification-20261120/`・
README `e304a654…`〔1,691 bytes〕/検証機 `c43ab3ac…`〔9,270 bytes・純stdlib・16 gate・別実装D4変換と4×4整数行列式で16根1,120四点組・72基底行1,080四点組を再検査〕/
出版監査 `1486d35e…`〔5,728 bytes〕+K1093 item `00d2c4ca…`〔2,311 bytes〕+研究log `ee4d947d…`〔1,177 bytes〕）を、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから再取得してpristine再実行・erratum確定・tamper・監査byte決定性を第三検査する。
residual72系第二検証群の第三検証は4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweeps・resolve7（K1190）に続き、**replace16分の第三検証は本Kが初号**。candidate-supply・refuted50・36root-three-plyの各第三検証は各レーン個別宣言の対象外。

## 主結果

- pin stage（gate 9）: 対象の3機械ファイル（README・検証機・監査）をpin commit `45a3f3b2` からraw固定URL取得・SHA-256+byte数照合（3点とも出版値どおり・api.github.com非依存）し、宣言時現main HEAD `4c3dd3af` の同3ファイルがpin byteと一致することをbyte比較で再確認（計9 gate all PASS）。
- recon stage（gate 22）: W 5入力（K1085 `5fdd342d…`〔39,221 bytes〕・K1086 `3045e152…`〔21,835〕・K1088 `16b38d04…`〔46,123〕・K1089 `808fbda1…`〔17,511〕・runner_v17.ts `19290371…`〔12,481・Git blob SHA-1 `c132cc64…`〕）を2参照（ref_a = 宣言時HEAD `4c3dd3af…`・ref_b = 宣言commit `19c4eea1…`）のraw固定URLから取得し、各SHA-256が検証機内pinと一致・2参照間byte-identical・合成tree正規path配置後に再照合（5点×4 gate）+ runner Git blob SHA-1 pin照合（1）+ 検証機本文配置後再照合（1）（計22 gate all PASS）。
- rerun stage（gate 23）: 出版検証機を改変なしpristine再実行4回/battery×3 battery（同一合成tree 2回・隔離copytree+隔離env PATH/HOME/TMPDIR 1回・隔離+`PYTHONHASHSEED=random` 1回）。全回 rc=0・stdout `PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079`・出力監査が**機械master `1741ca01…`〔5,730 bytes〕**とbyte-identical・4回間でもbyte一致・4出力相互同一（検証機1回約0.2秒・16 gate全PASS）。
- erratum stage（gate 10）: **出版監査 `1486d35e…`〔5,728 bytes〕は出版検証機からbyte再現不能であることを機械確定**。差分は正確に2箇所のみ: (a) `replacement-gains-histogram-reproduces` の `gainsHist` キー順〔出版ソート順 `"2","3","4"` vs 機械挿入順 `"4","3","2"`・値同一 `{"2":2,"3":11,"4":3}`〕・(b) `interpretation_guard` 最終文の文末句点〔出版 ASCII `.` vs 機械 `。` U+3002・それ以外文同一〕。他の全構造〔checks 16 gate・summary・inputs・runner〕が意味完全一致であることをcanonical化比較でassert（計10 gate all PASS）。**検証数値〔16/16・roots=16/rows=49/probes=32/nodes=6,339,079〕はすべて第三環境で同一再現しており、本erratumは監査jsonの同定問題であって検証の失敗ではない**。
- tampers stage（gate 11）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456} のいずれとも別位置〔@5,678/@9,012〕）、監査不在のfresh tree（事前不在をassert後に探針）で実施:
  - t1 `K1086` @5,678 → rc==1・stderr `K1086 SHA-256 mismatch: 28e251b7…`（対象名+改変後SHA-256を特定）・監査未書込・本番tree W無改変。
  - t2 `K1089` @9,012 → rc==1・stderr `K1089 SHA-256 mismatch: afb50484…`・監査未書込・本番tree W無改変。
  - 2つのstderrが互いに異なる入力名・異なる改変SHAを特定し、**K1086/K1089の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-errors`）。readpの最初のSHA不一致でSystemExitする「監査不書込」型強fail-closed（fold10 gate-failed書込型・resolve7と同じ不書込型の3設計目の実測として累積）。
- finalize: harness監査正本（**10,189 bytes・gate 75〔pin 9・recon 22・rerun 23・erratum 10・tampers 11〕・all_gates_pass true・時刻/絶対path/volatile排除・解釈ガード5文+unknown guard**・SHA-256 `569c6bbda909d4f3993ffaee64395d9a62911e7cddb49added51abb87393e545`）が3 battery（B1 fresh base全stage〔1.7秒〕・B2 同一base全stage再実行〔pin再取得込み・1.1秒〕・B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1.3秒〕）でbyte一致（`cmp`完全一致）。

## 実験事実

1. **出版監査jsonのerratum確定（residual72系で初の「byte再現不能」事例）**: replace16第二検証の出版監査は、出版済み検証機+pin済みW入力の正規実行からbyte再現不能（差分正確に2点: gainsHistキー順・最終guard文末句点）。数値・gate・構造は全一致のため検証の信頼性は不変だが、**監査jsonのbyte正本性は保証されず、出版監査はファイナル前ビルドの出力と推定される**（gainsHistが出版側でソート済みな点がその傍証）。第三検証側は機械master `1741ca01…`〔5,730 bytes〕を再現正本として記録した。**「出版監査byte一致」をrerun受入条件に無条件で使う運用は、byte再生性を事前に予備実行で確認してから受入条件に書くべきであるという運用知見**（resolve7 K1190ではbyte一致が成立したが、これは対象ごとに変わる）。
2. **宣言ノートの例示値誤記とaddendum運用**: 宣言ノートのgainsHist例示値 `{"2":2,"3":1,"4":3}` は誤記（正 `{"2":2,"3":11,"4":3}`）で、harnessのerratum assert実装時に出力値を実測して発見した。宣言本文byteは不変のままaddendum（commit `f89d5ae6`）で訂正した（fold10 addendum先例と同じ運用）。
3. **fail-closed設計の累積実測**（3種目: fold10 gate-failed書込型・resolve7不書込型に続きreplace16も不書込型）: 「監査不在のfresh treeで事前不在+事後不在をassertする」ことで、harness自身のtreeがrerun監査を持つ場合でも探針の fail-closed証明が壊れないことを確認（rerun後監査を除去してから探針）。
4. **軽量対象の第三検証運用**（K1189/K1190リコメンドの追試）: 対象検証機1回約0.2秒・battery 1巡約1.1〜1.7秒。第二検証出版（2026-11-20T00:44Z）から約1.2日で第三検証確定。

## 位置づけと限界

本検証はreplace16独立第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性（および出版監査jsonのerratum確定）の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行は一切行わない。nodes数・solved数・coverage数を勝敗として読まない。WIN8-D10 candidateは証明書ではない。REFUTED-D10はLOSS証明ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
