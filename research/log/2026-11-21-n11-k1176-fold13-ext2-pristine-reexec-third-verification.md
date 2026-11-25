# K1176（fold13外部第二検証）のpristine再実行第三検証の実施記録（2026-11-21）

## 経緯

- 最新mainを再取得し（宣言時HEAD `0af2ac836a9442e76d1d27cc100ec6243440063c`・K1184 part3 commitを確認）、
  AGENTS.md・research/knowledge/README.md（末尾はK1184まで）・K1176 item・fold13 ext2実験dir・fold13宣言ノート・
  過去の第三検証列（K1165/K1170/K1172/K1174/K1168/K1184第三）を確認した。
  **K1176を対象とする第三検証は先行宣言なし**（log列挙・実験dir列挙・直近コミットの3点で確認）。
  fold14〜16 ext2の第三検証は本実行の対象に含めず、fold13単体に限定した。
- 単一オーナー宣言ノートを先行出版（commit `48c6c2c366c4023279272ced0bf5675726ea5e3d`・宣言 2026-11-21T03:00Z・
  受入条件5項目・fetch-back byte一致）。K番号は新規採番せずpart2のpush直前3点確認により採番した。
- 他レーン宣言済み作業（fold11 ext2 `9be43128`・fold17 `095581932b`・fold18 `c2e8eb09f7`・fold19 `9606203ae`・
  fold23 `90ac8eed`・fold25 `aad3d71ca`・fold26・round-5 refsolve `ace38772d9`・WIN8抽出 `63877ffd2e`・
  WIN8行共有監査 `c403614f`・n9-ge19・n10 witness・five-row q7・four-row q6残・remo survivor・residual23 zero-triple・
  3行q4 `72fdd106`）に重複着手していない。

## 実施（受入条件対照）

1. **pin**（受入条件1）: 出版実験dir 5ファイルをpin commit `51d86169c1af5e7a880261e76c6f43ea7652d4d4` から
   raw固定URLで取得しSHA-256+byte数照合。5/5一致・10 gate・全battery PASS。
2. **recon**（受入条件2）: `reconstruct_fold13_inputs.py` 改変なしで ref_a `0af2ac83`（宣言時HEAD）と
   ref_b `48c6c2c3`（検証時main〔宣言commit〕）の2参照でW再構成。28 pin（12 Git blob + 16 SHA-256）+
   fold11機・fold12機・fold13機の3 chain機・計31ファイル・`diff -r` byte一致・
   fold11機pin（12+10）⊂fold12機pin（12+13）⊂fold13機pin（12+16）の部分集合連鎖の機械確認が両参照で成立。
   api.github.com非依存・待機ゼロ。
3. **rerun**（受入条件3）: `verify_fold13_external_20261121.py` 改変なしpristine 4回/battery・3 batteryで計12回
   （このほか手動試行2回）。全回 rc=0・`ALL 774 GATES PASS`・gate count 774・all_gates_pass true・
   出力監査81,632 bytesが出版正本 `4fe40fa2…` とbyte-identical・battery内でも4回byte一致。
   1回約28.5〜29.1秒（機内のfold13機4回プリ実行・fold11/fold12機独立rerun・機内tamper 2件込み）。
4. **tampers**（受入条件4）: 本レーン選択offsetの1 byte XOR 0x01（worklist `inputs/worklist.csv` @222,999
   〔360,834 bytes中〕・K1108証明書 `k1108/certs/win8-root-00000000000000003800000009840004-20261120.n11` @1,111,444
   〔1,640,220 bytes中〕。出版社試験位置@117,777/@777,777、fold12第三検証レーンの@150,000/@654,321、
   fold20/21/22/24第三検証・fold14-16 ext2各レーンoffset群とすべて別位置）。両者とも隔離copytree W上で rc=1・
   `GATE FAILED [i]: W blob pin inputs/worklist.csv` / `GATE FAILED [i]: W sha256 pin <CERT_REL>`・監査未書込で
   fail-closed捕捉。本番Wは事後に無改変再照合（worklist `6d8a449e…`・証明書 `5b114b9e…`）。
   3 batteryで計6回・手動探針（XOR 0x20）2回も同一メッセージで発火。
5. **finalize/harness監査**（受入条件5）: 時刻/絶対path/volatile排除のbyte決定的harness監査JSON
   （6,668 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・SHA-256 `701bdfeb…`）が
   byte一致。実験dirは自己完結（README・harness・監査正本・reproduction logの4ファイル）。

## 実験事実・教訓

- **実行環境リセット事故と完全再生成**: battery 3巡（監査正本 `701bdfeb…`）完了直後に実行環境がリセットされ、
  pubfetch・W tree・battery成果物・harnessファイルを含む全ローカル成果物を喪失した。harnessを記録済みソースから
  再構成し（byte数照合 18,746 = 18,746・再入力時に紛れ込んだ24 bytesの余分行〔`PARTS.mkdirs = None`〕はbyte数照合が
  捕捉して除去）、battery 3巡をfresh baseでゼロから完全再実行したところ、再生成監査正本はリセット前記録値
  `701bdfeb…` とbyte一致した。**2環境実体・6 finalize監査すべて同一byte**であり、byte決定的設計
  （時刻・絶対path・volatile排除）の交叉環境妥当性が事故を通じて実証された。出版物（part1）は再生成側を正本とした。
- **fold13第二検証batteryはfold12の約2倍・約2.5分/battery**: 検証機gate 774（fold12は655）・1回約29秒
  （fold12機の約2倍）・W 31ファイル・fold13機pin 16個。worklistはfold12と同一seriesファイルの再利用
  （`6d8a449e…`・360,834 bytes）であり、本レーンtamper offset（@222,999）はfold12第三検証レーン（@150,000）と
  衝突しない。
- **出版検証機の内部scratch絶対path**（`/home/user/work/f13ext/runs`）は出版機の設計変更非目標のためそのまま接受し、
  harness側で厳密逐次実行により競合を排除した。隔離実行（r3/r4）でも同一点を用いるが監査byteに影響しないことを
  実測した。
- **api.github.com quota枯渇下でもbatteryは全域raw固定commit URL**: apiは本セッションで403枯渇したが
  （コミット列挙に最小回数のみ使用）、pin・再構成・fetch-backはすべてapi非依存で待機ゼロの冪等運転だった。

## 結果と限界

K1176の外部第二検証battery（出版社監査正本 `4fe40fa2…`・774 gate）がrepo出版byteのみから第三環境で
byte再生可能であることを確定した。これはK1176の第三再現であり、別実装の新しい証明器ではない。

行は1行も新たに閉じない。receipt fold、WIN/LOSS verdict、証明書抽出は行っていない。
WIN8-D10は当該8石rootのゲーム木に限る。REFUTED-D10はLOSS証明ではない。nodes・solved・coverage数を勝敗として読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。**

## 出版

- part1（実験dir `research/experiments/n11-fold13-ext2-pristine-reexec-third-verification-root9840004-20261121/`
  4ファイル・単一push_filesコミット）: commit `7943056f064379a77ce6888c24fd29b8ebacf1fc`・fetch-back 4/4 byte一致。
- part2（本記録とK1185 item・K番号はpush直前にitems/404・README grep 0・コミット列挙の3点確認でK1185取得）。
- part3（knowledge README末尾bullet）は別コミット。
