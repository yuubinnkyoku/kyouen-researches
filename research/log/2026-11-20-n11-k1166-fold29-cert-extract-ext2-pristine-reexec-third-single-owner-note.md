# K1166（fold29証明書抽出・外部第二検証）のpristine再実行第三検証: 単一オーナー宣言

- **担当レーン（単一オーナー）**: 本実行（n11長期レーン）。宣言時の最新mainは `1c42dcf25c78540033c5ec08c00952e4a939a8ee`（2026-11-20T22:56Zに確認）。
- **対象**: K1166（K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証・root `00000000000000043800000008180010` / `00000000000200003800200008180000` / `0000000800000000380000000810000a`）。K1166の出版harness `verify_cert_extract_ext_second_20261120.py`（SHA-256 `ca662e57053f504684c8dcc44f66c182d338978a3b9b70369a40754d9c59b276`・30,141 bytes・gate 43）と取得器 `fetch_master.py`（`c3c4c9ffef5132e1657470d84b296b499ecd421b0342404ae32b0fd3ee64a114`）・pin表 `pin-manifest.json`（`949868e21fdc124058c608925c101468622acca17702e159f99fb03df09d3ae8`）を、出版byteのまま第三の実行環境でstage分割実行する。
- **先行確認**: main上のK1166 item・実験README・post-publication記録（commit `7c1e765d88`）・knowledge READMEを確認した。**K1166を対象とする第三検証の先行単一オーナー宣言・実験・logは確認されなかった**（直近200 commitに第三検証着手を示すcommitなし）。出版社自身のpost-publication reproduction runは同レーンによる自家記録であり、第三の実行環境によるpristine再実行としては出版されていない。fold18/fold19外部第二検験（`c2e8eb09f7`/`9606203aec`）・fold23/fold25/fold26・round-5 refsolve・WIN8証明書抽出（`63877ffd2e`）・WIN8証明書行共有監査（`c403614f`）・n9-ge19（`21f8610464d2`）・y13 two-token（`4bdff59be8`）・K1168第三検証（完了済み）の各宣言済み・完了済み作業は対象外とし重複着手しない。
- **受入条件**:
  1. K1166の出版実験dir（`research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/`）のbyte 4点（README・fetch_master.py・pin-manifest.json・harness）と監査正本 `output/harness-audit.json`（SHA-256 `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`・15,549 bytes・gate 43・status PASS）をmain固定commitから取得し、SHA-256照合する。
  2. `fetch_master.py` を改変せず実行し、pin commit `28d223a2dd254b8a85cc342dff3f4bd801d1b31f` から出版社3実験dir全61ファイルを再構成し、git blob SHA照合 61/61 を確認する。
  3. 出版harnessを改変せずstage分割（pin → root k1136 → root k1137 → root k1139 → tampers → finalize・各stageは1コマンド300秒上限内）でbattery 1巡を実行し、監査JSONが出版正本 `cf6a26ab…` とbyte-identicalであることを確認する。
  4. harness内蔵の3件tamper（出版社未試験offset・証明書本文300007・pin入力1111・fresh nodes 2757→2758）がいずれもfail-closed（returncode≠0・harness監査未書込）で通過することを確認する。
  5. batteryをもう1巡（隔離cwd・隔離HOME・`PYTHONHASHSEED=random` を含む別環境）実行し、両巡の監査JSONが互いにbyte一致し出版正本ともbyte一致することを確定する。pin・新規実行の入出力SHA-256を記録し、実験dirに再現可能な成果物（第三検証harness・reproduction log・監査正本）を出版する。
- **非目標・解釈ガード**: 本作業はK1166第二検証の再現性・入力pin・監査byteの第三検査であり、証明書の再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes・solved数・coverage数を勝敗と読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
- **実行資源**: 本sandbox（python3.12・node v22.20.0〔`--experimental-strip-types`〕・2コア・harness内並列度2固定・raw.githubusercontent.com経由の出版byte取得）。CPU並列はharness既定の2に抑え、大量中間ファイルはpublishしない。
- **出版方針**: branch/PRを作らずmainへ直接反映する。第三検証実験dir・研究log・K item（採番はpush直前3点確認）・knowledge README末尾bullet の順で出版する。受入条件を満たせない場合は失敗・未完として記録し、部分成果を検証完了と表現しない。
