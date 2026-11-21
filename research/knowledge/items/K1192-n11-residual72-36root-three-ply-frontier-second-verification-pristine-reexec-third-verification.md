id: K1192
title: "36root-three-ply frontier（K1084）独立第二検証のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "36root-three-ply frontier K1084 independent second-verification pristine re-execution third verification"
  - "residual72系第二検証群のt36分第三検証（出版byte 3点+HEAD照合pin・W 2点2参照・検証機19 gate pristine 4回/battery×4 battery・harness監査56 gate 4巡byte一致）"
  - "出版監査byte再生成立（erratumなし・K1191運用知見の適用第1号）・fail-closed設計4種目（raise RuntimeError traceback型・監査不書込・末行メッセージ特定gate）・第三検証harness監査正本 407d649d…（gate 56〔pin 9・recon 9・rerun 23・tampers 15〕）"
relations:
  - type: depends_on
    target: K1084
    note: "検証対象の大もと。residual72の36-root三手先D4重複census（K1075候補供給正本による36 fresh-safe 7石rootの三手先幾何census）に対する独立第二検証（commit 67766eac…・19 gate・Python 3.13純stdlib・整数放物面持ち上げ (x²+y²,x,y) の3次元外積・内積で4点行列式零判定・三点組132,291個・点判定16,007,211回・root安全性四点組1,260個）を第三の実行環境からpristine再実行する。"
  - type: related
    target: K1075
    note: "W入力の一方。候補供給正本 49b6f85f…（54,282 bytes）は本第三検証のreconで2参照取得・SHA-256 pin照合し、tamper t1（@51,234 XOR 0x20）の検出対象。"
  - type: related
    target: K1190
    note: "本レーンの同一手続き系列の先行成果（resolve7=K1072第二検証の第三検証）。本Kはその次の採番で、手続き系列（単一オーナー宣言→pin/recon/rerun/tampers/finalize→battery→part1-3出版）を踏襲。"
  - type: related
    target: K1191
    note: "直前成果（replace16=K1089第二検証の第三検証・出版監査erratum確定）。本KはK1191で確立した「rerun受入のbyte再生性は宣言前に予備実測してから課す」運用の適用第1号（本対象はbyte再生成立・erratumなし）。"
  - type: related
    target: K1144
    note: "residual72系の第三検証の先行例（4-sweep re-exec）。第三検証未着手枠はcandidate-supply・refuted50が残る（各レーン個別宣言対象）。"
artifacts:
  - path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-pristine-reexec-third-20261121/README.md
    role: source
    note: "対象・固定pin・W入力2点・実施内容と結果（harness 56 gate内訳）・実験事実3項・再現手順・解釈規約（9,514 bytes・commit 1b19e7fc…）"
  - path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-pristine-reexec-third-20261121/scripts/verify_t36v_third_20261121.py
    role: verifier
    note: "第三検証harness（stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・byte決定的監査JSON出力・ROOTを検証機fileのparents[4]から解決する合成tree方式・SHA-256 cf5b5f47…・15,153 bytes）"
  - path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-pristine-reexec-third-20261121/output/frontier-third-harness-audit.json
    role: audit
    note: "第三検証harness監査正本（7,729 bytes・gate 56〔pin 9・recon 9・rerun 23・tampers 15〕・all_gates_pass true・SHA-256 407d649dde8e791447d160dab39ebc71f50ea2aed704e7b145153b494c7b6156・4 battery byte一致）"
  - path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-pristine-reexec-third-20261121/output/reproduction.log
    role: record
    note: "battery 4巡の実行記録（1,323 bytes・SHA-256 930b5552…・B1/B2/B1f/B3所要時間・cmp結果・監査SHA照合3組）"
  - path: research/log/2026-11-21-n11-36root-three-ply-frontier-second-verification-pristine-reexec-third-single-owner-note.md
    role: declaration
    note: "単一オーナー宣言ノート（commit ffba7985…・受入条件5項目・出版監査byte再生性を宣言前に予備実測し受入条件3をbyte一致条件で確定・tamper予備探針の予測を記載・先行宣言の不在を機械列挙で確認）"
  - path: research/log/2026-11-21-n11-residual72-36root-three-ply-frontier-second-verification-pristine-reexec-third-verification.md
    role: record
    note: "研究log（発見順・判断・失敗記録・part1 README再実行回数文言の数え誤り機械確定）"
---

# K1192（36root-three-ply frontier=K1084独立第二検証のpristine再実行第三検証）

担当: n11長期レーン。単一オーナー宣言（commit `ffba7985…`・宣言 2026-11-21T06:5xZ・受入条件5項目・**出版監査byte再生性を宣言前に予備実測して受入条件3をbyte一致条件で確定**・tamper予備探針の挙動を宣言時に記載・先行宣言の不在を機械列挙で確認）の下で実施。

## 検証対象

residual72の36-root三手先D4重複census（K1075候補供給正本による36 fresh-safe 7石rootの三手先幾何census）に対する**独立第二検証**。
K1084出版（commit `67766eac2f30c856543a1319cdfc5d1458382c73`・2026-11-19T23:25:16Z単一コミット・
実験dir 3ファイル〔README `bbc9b255…` 2,782 bytes・検証機 `scripts/verify_frontier.py` `d8876e5b…` 14,671 bytes・監査正本 `output/independent-second-verification-20261120.json` `a6272056…` 55,614 bytes〕+
K1084 item 3,253 bytes+研究log 2,743 bytes・19 gate・Python 3.13純stdlib独立実装〔元JSをimport・実行せず、整数放物面持ち上げ (x²+y²,x,y) の3次元外積・内積で4点行列式零判定・D4 8変換は座標写像の直接列挙〕・三点組132,291個・点判定16,007,211回・root安全性四点組1,260個・監査に時刻/絶対path/volatileを含まないbyte決定構造）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する**。
residual72系の第三検証は4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweeps・resolve7（K1190）・replace16（K1191）に続き、**36root-three-ply分の第三検証は本Kが初号**。残る未着手枠はcandidate-supply分・refuted50分（各レーン個別宣言の対象外）。

## 主結果

- pin stage（gate 9）: 対象の3機械ファイル（README・検証機・監査正本）をpin commit `67766eac` からraw固定URL取得・SHA-256+byte数照合（3点×2 gate・api.github.com非依存）し、宣言時現main HEAD `3ba28e88` の同3ファイルがpin byteと一致することをbyte比較で再確認（3 gate）（計9 gate all PASS）。
- recon stage（gate 9）: W 2入力（K1075候補供給正本 `49b6f85f…`〔54,282 bytes〕・先行三手先census正本 `94fdb0c6…`〔53,914 bytes〕）を2参照（ref_a = 宣言時HEAD `3ba28e88…`・ref_b = 宣言commit `ffba7985…`）のraw固定URLから取得し、各SHA-256が検証機内pinと一致・2参照間byte-identical・合成tree正規path配置後に再照合（2点×4 gate）+ 検証機本文配置後再照合（1）（計9 gate all PASS）。
- rerun stage（gate 23）: 出版検証機を改変なしpristine再実行4回/battery×4 battery（B1 fresh base・B2 同一base再実行・B1f fresh base独立capture・B3 隔離fresh base+`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd）で計16回。全回 rc=0・stdout JSON `status=second-verified・check_count=19・all_pass=true`・出力監査が**出版正本 `a6272056…`〔55,614 bytes〕とbyte-identical**・battery内4回間でもbyte一致（x4 5 gate+相互3 gate・計23 gate all PASS・検証機1回約16秒）。
- tampers stage（gate 15）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456}/{5,678,9,012} のいずれとも別位置〔@51,234/@8,765〕）、**監査不在のfresh tree**（rerun後監査を除去し事前不在をassert後に探針）で実施:
  - t1 K1075候補供給正本 @51,234〔54,282 bytes内〕→ rc==1・stdout空・stderr末行 `RuntimeError: K1075 source SHA-256 mismatch`・監査未書込・本番tree W無改変。
  - t2 先行census正本 @8,765〔53,914 bytes内〕→ rc==1・stdout空・stderr末行 `RuntimeError: published frontier SHA-256 mismatch`・監査未書込・本番tree W無改変。
  - 2つのstderr末行は互いに異なる入力を特定し、**K1075供給正本とcensus正本の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-errors`・t1は読み取り1点目・t2は2点目のfailで読み取り順独立性を含む）。
- finalize: harness監査正本（**7,729 bytes・gate 56〔pin 9・recon 9・rerun 23・tampers 15〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `407d649dde8e791447d160dab39ebc71f50ea2aed704e7b145153b494c7b6156`）が**4 battery**（B1 fresh base全stage〔1m4.9s〕→B2 同一base全stage再実行〔pin再取得込み・1m2.7s〕→B1f fresh base独立capture〔1m2.9s〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1m3.3s〕）すべて56/56 PASSで**byte-identical**（`cmp`完全一致・4 capture同一）。

## 実験事実

1. **出版監査byte再生の成立と事前実測運用の適用第1号**: 本対象のpristine再実行（宣言前予備1回+本battery 4回/battery×4 battery=16回）はすべて出版正本 `a6272056…` とbyte-identicalで**erratumなし**（replace16 K1191の「出版監査byte再現不能」型と対照的）。K1191で確立した「rerun受入のbyte再生性は宣言前に予備実測してから課す」運用を本対象で先に適用し、宣言ノート受入条件3は当初からbyte一致条件で確定した。運用の有効性を実証。
2. **fail-closed設計4種目の実測（raise RuntimeError traceback型・監査不書込）**: pin loop読み取り直後の不一致でRuntimeError（Python traceback）となり監査JSONを一切書かない（fold10 gate-failed監査書込型・resolve7 SystemExit不書込型・replace16 SystemExit不書込型に続く4種目）。tracebackは実行file絶対pathを含むため非byte決定的だが、**末行メッセージは入力名で決定的**であり、第三検証gateは末行特定で機械記録可能（stderr全文byte一致は要求しない設計を宣言ノートに明示）。
3. **中堅規模の第三検査コスト**: 検証機1回約16秒・battery 1巡約63〜65秒（pin/recon fetch+rerun 4回+tampers 2探針）。第二検証出版（2026-11-19T23:25Z）から約1.6日で第三検証確定。
4. **part1実験READMEの再実行回数文言の訂正（機械確定・出版byteは不変）**: part1 README実験事実1・3の「本battery 12回」「12回のrerun」は数え誤り。harness監査のrerun gate構成（r1〜r4×4 battery・各captureの56 gateがrerun 23 gateを含む）とbattery所要時間（各巡約63〜65秒 ≒ rerun 4回×約16秒+fetch/tampers）から、**正しくは4回/battery×4 battery=16回**。監査byte一致・全gate PASSは回数に依らず成立しており検証の信頼性への影響はないが、第三検証記録（本item・研究log）で機械確定し、part1 README本文の遡及修正は行わない（K1191のerratum運用と同じ扱い）。

## 位置づけと限界

本検証は36root-three-ply frontier第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行・36-root depth-10 sweep（別単一オーナーレーン所属）の起動・変更は一切行わない。幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではなく、共有表実装やworker分割変更の正当化ではない。nodes数・solved数・coverage数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。36 rootは候補rootであってWIN証明書ではない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
