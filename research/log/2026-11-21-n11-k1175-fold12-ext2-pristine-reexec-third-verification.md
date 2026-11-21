# K1175（fold12外部第二検証）のpristine再実行第三検証の実施記録（2026-11-21）

## 経緯

- 最新mainを再取得し（宣言時HEAD `91f2f0f13164bfe3bd4734f907d5ea3fd27e1c7c`・3行q4 m=23 SAT subproblem commitを確認）、
  AGENTS.md・research/knowledge/README.md（末尾はK1183まで）・K1175 item・fold12 ext2実験dir・fold12宣言ノート・
  過去の第三検証列（K1165/K1170/K1172/K1174/K1168第三）を確認した。
  **K1175を対象とする第三検証は先行宣言なし**（log列挙2026-11-19以降・実験dir列挙・直近コミットの3点で確認）。
  fold13〜16 ext2の第三検証は本実行の対象に含めず、fold12単体に限定した。
- 単一オーナー宣言ノートを先行出版（commit `4c7a12f1aed44205f20824be024a382d161a7a4c`・宣言 2026-11-21T02:50Z・
  受入条件5項目・fetch-back byte一致）。K番号は新規採番せず次part2でpush直前3点確認により採番することを宣言どおり実施。
- 他レーン宣言済み作業（fold11 ext2 `9be43128`・fold17 `095581932b`・fold18 `c2e8eb09f7`・fold19 `9606203ae`・
  fold23 `90ac8eed`・fold25 `aad3d71ca`・fold26・round-5 refsolve `ace38772d9`・WIN8抽出 `63877ffd2e`・
  WIN8行共有監査 `c403614f`・n9-ge19・n10 witness・five-row q7・remo survivor・residual23 zero-triple・3行q4）に
  重複着手していない。

## 実施（受入条件対照）

1. **pin**（受入条件1）: 出版実験dir 5ファイルをpin commit `adb1e8f605b6903f6a671d9447c001b79f401398` から
   raw固定URLで取得しSHA-256+byte数照合。5/5一致・10 gate・3 batteryすべてPASS。
2. **recon**（受入条件2）: `reconstruct_fold12_inputs.py` 改変なしで ref_a `91f2f0f1`（宣言時HEAD）と
   ref_b `4c7a12f1`（検証時main〔宣言commit〕）の2参照でW再構成。25 pin（12 Git blob + 13 SHA-256）+
   fold11機・fold12機・計27ファイル・`diff -r` byte一致・fold11機pin（12+10）部分集合性機械確認が両参照で成立。
   api.github.com非依存・待機ゼロ。
3. **rerun**（受入条件3）: `verify_fold12_external_20261121.py` 改変なしpristine 4回/battery・3 batteryで計12回。
   全回 rc=0・`ALL 655 GATES PASS`・gate count 655・all_gates_pass true・出力監査70,149 bytesが出版正本
   `c309d693…` とbyte-identical・battery内でも4回byte一致。1回約14〜15秒（機内のfold12機4回プリ実行・fold11機
   独立rerun・機内tamper 2件込み）。
4. **tampers**（受入条件4）: 本レーン選択offsetの1 byte XOR 0x01（worklist `inputs/worklist.csv` @150000〔360,834 bytes中〕
   ・K1106証明書 `k1106/certs/win8-root-00000000000000003800000008005021-20261120.n11` @654321〔945,298 bytes中〕・
   出版社試験位置@96,300/@456,789 およびfold20/21/22/24第三検証・fold13-16 ext2各レーンoffset群とすべて別位置）。
   両者とも隔離copytree W上で rc=1・`GATE FAILED [i]: W blob pin / W sha256 pin …`・監査未書込でfail-closed捕捉。
   本番Wは事後に無改変再照合（worklist `6d8a449e…`・証明書 `69f32661…`）。3 batteryで計6回の再試験。
5. **finalize/harness監査**（受入条件5）: 時刻/絶対path/volatile排除のbyte決定的harness監査JSON
   （6,587 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 `06750caa…`）が
   3実行（同一base 2巡は全stage再実行・第3巡は隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で
   byte一致。実験dirは自己完結（README・harness・監査正本・reproduction logの4ファイル）。

## 実験事実・教訓

- **転写誤りをfail-closed pin gateが捕捉**: 初版harnessのFILES表で検証機SHA-256に1文字誤植
  （`…31d5f73185…`↔正 `…31d5d73185…`）。pin stageが実測値照合で即捕捉・part file書込前に終了。
  打鍵定数はfail-closed pinで防ぐパターン（K1158/K1160/K1164/K1170/K1174）の再実証。
- **fold12第二検証は検証ラティス中最軽量級**: 検証機1回約14〜15秒・W 27ファイル・1 battery約60秒。
  今後のfold13-16単体ext2第三検証もほぼ同規模と見込まれる（fold13は検証機29秒・W 28 pin・fold14は処理53秒・
  fold15は105秒・fold16は1 batteryあたり数分と、検証機実行時間の Serializer 増分を除き同一手続きで適用可能）。
- **出版検証機の内部scratch絶対path**（`/home/user/work/f12ext/runs`）は出版機の設計変更非目標のためそのまま接受し、
  harness側で厳密逐次実行により競合を排除した。隔離実行でも同一点を用いるが、監査byteに影響しないことを
  実測した（r3/r4 の監査もbyte一致）。
- 本batteryは全段api.github.com非依存（raw固定commit URLのみ）。他レーンのquota枯渇の影響を受けない。

## 結果と限界

K1175の外部第二検証battery（出版社監査正本 `c309d693…`・655 gate）がrepo出版byteのみから第三環境で
byte再生可能であることを確定した。これはK1175の第三再現であり、別実装の新しい証明器ではない。

行は1行も新たに閉じない。receipt fold、WIN/LOSS verdict、証明書抽出は行っていない。
WIN8-D10は当該8石rootのゲーム木に限る。REFUTED-D10はLOSS証明ではない。nodes・solved・coverage数を勝敗として読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。**

## 出版

- part1（実験dir `research/experiments/n11-fold12-ext2-pristine-reexec-third-verification-root8005021-20261121/`
  4ファイル・単一push_filesコミット）: commit `bf5041351b21946b167531af9c2a045651b2a6c0`・fetch-back 4/4 byte一致。
- part2（本記録とK1184 item・K番号はpush直前にitems/404・README grep 0・コミット列挙の3点確認でK1184取得）。
- part3（knowledge README末尾bullet）は別コミット。
