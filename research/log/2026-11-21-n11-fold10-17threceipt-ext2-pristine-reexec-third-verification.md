# fold10（第17 WIN7 receipt fold・外部第二検証）pristine再実行第三検証 研究log

## 経緯

- 2026-11-21 の本長期レーン実行は、K1188（fold16 ext2第三検証）出版後のmain（HEAD `dcc5b96238…`・05:40Z）から再開した。
  未着手枠の選定にあたり、最新mainの第三検証の確定状況を機械列挙した: fold12〜16（K1184〜K1188）・fold20（K1174）・
  fold21（K1168第三）・fold22（K1170）・fold24（K1165）・fold29 cert-extract（K1172）・residual23系は第三検証確定済み、
  fold11/17/18/19/23/25/26 ext2は宣言済み他レーン（着手禁止）、fold27以降はround-5 refsolve系の供給待ち。
  **WIN7 receipt fold系（第1〜17 receipt）は外部第二検証体制が確立したfold10（第17 receipt）のみが
  第二検証出版済み（commit `452af0c5…`・31 gate）で、第三検験が未着手・宣言もないことを確認**し、
  この単体を本レーンの枠として取得した。
- 単一オーナー宣言ノートを先行出版（commit `4987c2b7…`・受入条件5項目・Wは出版artifact 3点のraw pinned再取得のみ、
  検証機1回約1秒を見込む軽量battery設計）。
- **宣言ノート初版の受入条件4 t1予測の誤り**: battery前の予備探針で、fold10正本（12,918 bytes）@12,345 が
  メタデータ文字列 `_against_published_verdict_uni…` の内部であり、1 byte XORではJSON parseが生存することが判明。
  出版検証機はparse死せず31 gateを走行し、**ちょうどfold10正本SHA-256 pin gate 1件のみが失敗**（他30 gate全pass）して
  rc≠0・監査は `gate-failed` で書込まれる。初版予測（「json load失敗でrc≠0・監査未書込」）と異なるため、
  誤った予測のままbatteryを実施せず、**所有者addendum（commit `274e3e28…`）で予測を修正してから全batteryを実施**した
  （宣言ノート本体byteは不変。宣言後・battery前の修正であり、修正後のbatteryだけを正本とする）。
- harness `verify_fold10ext2_third_20261121.py`（19,782 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・
  fail-closed・byte決定的監査）を構築。開発中の軽微バグ（stage_pin の未使用書込行・gate名prefixの `rererun/` 誤字・
  r1/r2の同一cwd化）はpy_compile+初回探針でそれぞれ捕捉修正し、全gateが指定挙動をassertする形に固めた。

## 結果

- **3 batteryすべて `all-gates-pass`（gate 56〔pin 6・recon 15・rerun 24・tampers 11〕）・監査JSON byte-identical**
  （`cmp` 完全一致・SHA-256 `2a97d052bd1f0de95331f6d2b62322b61b38af326743a3dc244e4064a9abd7aa`・10,980 bytes）。
  B1 fresh base・B2 同一base全stage再実行〔pin再取得込み〕・B3 隔離base+全体 `env -i` 隔離HOME/TMPDIR+
  `PYTHONHASHSEED=random`。battery 1巡約0.9秒（n11検証ラティス最小級）。
- rerun: 出版検証機のpristine再実行4回/battery×3（同一cwd 2回・隔離copytree cwd 1回・隔離+PYTHONHASHSEED=random 1回）で
  全回rc=0・出力監査が出版正本 `a62d6d50…`（5,410 bytes）とbyte-identical。
- tampers: t1 fold10正本 @12,345・t2 第17証明書 @1,234,567 の1 byte XOR 0x01が、いずれもrc≠0・
  それぞれ対象入力のSHA-256 pin gateを**単独で**失敗させfail-closed捕捉（他30 gateは全pass・W復帰後byte無改変）。
  offsetは既知の全レーン探針位置（fold12〜16第三・fold20/21/22/24第三・出版社試験位置）とすべて別位置。

## 実験事実・知見

1. **入力pin gateの独立性実証**: 選定offsetが文字列値の内部に当たった場合、出版社の検証機はparse死ではなく
   「対象入力のSHA-256 pin gate単独失敗」でfail-closedする。t2とあわせ、2種の入力pin gateが互いに独立して
   発火することを1 battery内で実証した（fail-closed防衛の設計どおり）。
2. **予測誤りの扱い**: 宣言ノートの予測がbattery前に誤りと判明した場合、誤ったまま受入判定せず
   addendumで修正してからbatteryを実施する運用が機能した（K1181の「出版前機械草案の未出版破棄」と同じ
   「battery前に自分の誤りを正す」パターン）。
3. **軽量第三検証対象の拖延コスト低さ**: 当該ext2は出版から第三検証まで約1.5日の空白があったが、
   battery 3巡で約3秒・作業全体で宣言からpart3まで約1時間で完了。軽量対象ほど第三検証を早期に潰す運用が合理的。

## 解釈規約（不変）

- 本検証はfold10外部第二検証の再現性・入力pin・fail-closed防衛・監査byteの第三検査であり、
  receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない。
- WIN7-D10証明書は当該7石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
- nodes数・solved数・coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- 残る第三検証未着手の候補（residual72系第二検証群・vertical-fiber系・class2-lane fold系の各ext2など）は、
  最新mainの宣言状況を確認のうえ各レーン個別宣言で着手する。fold17〜19/23/25/26 ext2は他レーン完了待ち。
