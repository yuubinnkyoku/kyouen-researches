# K1168（fold21外部第二検証）のpristine再実行第三検証: 単一オーナー宣言

- **担当レーン（単一オーナー）**: 本実行。宣言時の最新mainは `429232fd7e8322f5ca11af567c8e9f4ca6d303ad`（2026-11-20T22:06:05Zに `git ls-remote refs/heads/main` で確認）。
- **対象**: K1168（fold21 receipt fold K1130・root `00000000000000801202000800880200`）の外部第二検証。K1168の出版検証機 `verify_fold21_external_20261120.py`（SHA-256 `322ad6ca…`・50,946 bytes）と再構成機 `reconstruct_inputs.py`（SHA-256 `a70b7983…`・10,765 bytes）を、出版byteのまま第三の実行環境で再実行する。
- **先行確認**: main上のK1168 item・実験README・実行log・関連knowledge READMEを確認した。K1168の第三検証を対象とする先行単一オーナー宣言・実験・logは確認されなかった。K1167第三検証（K1170）、fold21外部第二検証（K1168）そのもの、fold23/24/25/26、fold18/19外部第二検証、round-5 refsolve、WIN8証明書抽出・行共有監査の各宣言済み作業は対象外とし、重複着手しない。
- **受入条件**:
  1. K1168の出版実験dir 5ファイルをmain上の固定commitから取得し、K1168/README記載のSHA-256と照合する。
  2. 出版再構成機を固定main ref `429232fd7e8322f5ca11af567c8e9f4ca6d303ad` で2回実行し、W・publication treeの全ファイルbyte一致を確認する。Wの52 input pins（12 Git blob + 40 SHA-256）とfold20→fold19→fold18のrerun chainをfail-closedで再構成する。
  3. 出版検証機を改変せず3回以上pristine実行する。同一cwd・隔離cwd/HOME・`PYTHONHASHSEED=random` を含め、各回の監査JSONが出版正本（SHA-256 `80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63`・135,723 bytes・1,394 gates）とbyte-identicalであることを確認する。
  4. 出版検証機内蔵の2件のtamper試験がfail-closed（非0終了・監査未書込）で通過することを確認する。
  5. 第三検証harnessの監査正本を時刻非依存にし、同一cwd・隔離環境・random hash seedの3回でbyte-identicalにする。入力・出力のSHA-256を記録し、実験dirへ再現可能な成果物を出版する。
- **非目標・解釈ガード**: 本作業はK1168外部第二検証の再現性・入力pin・監査byteの第三検査であり、receipt foldの追加実行・S6行の追加閉鎖・WIN/LOSS verdictの追加は行わない。K1130のWIN8-D10は当該8石rootのゲーム木に限る。REFUTED-D10はLOSS証明ではない。nodes・solved数・coverage数を勝敗と読まない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのままとする。
- **実行資源**: CT204のroot filesystemは143 MiB空きのため、作業tree・scratch・一時出力は `/dev/shm` に置き、CPUは逐次実行（同時並列なし）とする。CT199はroot filesystem 100%かつコマンド応答timeoutを観測したため使用しない。
- **出版方針**: branch/PRを作らずmainへ直接反映する。既存K1168を更新し、新しいK番号は作らない。Knowledge生成物は直接編集しない。資源・API制限等で受入条件を満たせない場合は失敗・未完として記録し、部分成果を検証完了と表現しない。
