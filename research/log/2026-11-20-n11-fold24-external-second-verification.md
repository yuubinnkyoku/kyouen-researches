# fold24 receipt fold（K1140）の外部第二検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T18:12:30Z）**: fold24外部第二検証の単一オーナー宣言ノートを
  [単一オーナー宣言ノート](2026-11-20-n11-fold24-external-second-verification-single-owner-note.md)
  （commit `434d53f3e3`）として先に出版した。宣言時点のmain HEADは `9d708fa430` で、
  fold24外部第二検証の先行宣言なし。fold25外部第二検証は別レーンが宣言済み（`aad3b71ca3`）のため
  対象外とした。受入条件は7項目を定めた（出版byte pin照合・W再構成・出版機pristine再実行4回・
  同梱監査再実行・別実装による全再導出・tamper 2件・監査正本3実行byte-identical）。
- **出版byte pin照合**: fold24出版実験dir（単一コミット `fc4c18fdddb4072667ad019d3218a066e313ff4e`）の
  receipt・機械・同梱監査・再現log・reconstruct_inputs.pyの5点をGitHubから取得し、
  宣言ノート記載のSHA-256と照合した。
- **W再構成**: 出版済み `reconstruct_inputs.py`（SHA-256 `f4e1fa8e…`）を固定Git参照
  `b91e85a99f0480f084835bdff51533d0cf5feaa8` で実行し、61入力pin
  （12 Git blob pin + 49 SHA-256 pin）を再構成した。
- **手動確認段階**: 出版機をpristine再実行4回（同一cwd 2回・隔離tree/cwd/HOME・隔離+PYTHONHASHSEED=random）。
  全実行のreceiptが出版正本 `c4ab76d3…` とbyte-identical。各実行はfold23機の隔離pristine rerunを含む。
  同梱独立監査機の再実行は46/46 checks・出版監査正本 `49f330c6…` とbyte-identical。
  tamper検査として、worklist（offset 777）とK1136証明書（offset 12345）の1 byte XORを試験し、
  2件ともreturncode 1・正本未書込でfail-closed捕捉を確認した。
- **テンプレ執筆と外部検証機化**: 上記手動確認を一括する第三実装の検証機を執筆した。
  機の打鍵定数はテンプレート `verify_fold24_external_20261120.py.tpl`（プレースホルダ `__PINS__`/`__PIN256__`）に
  pins.jsonの12/49定数を注入して生成する方式とし、手書き転写を排除した。
- **pin定数typoの捕捉**: 生成した初版で実行すると、K1091掃引pin定数のSHA転写にtypo
  （`deda…`→正 `ded0…`）があり、検証機自身のfail-closed pin gateが実行前に捕捉した。
  修正して再実行したところ全gate PASS。第三検証系のK1158（K1102 pin・`f268`→正 `f262`）・
  K1160（runner ts pin誤り）と同じ防御パターンが本レーンでも有効だったことを記録する。
  なおtypoはテンプレート注入部分ではなくpin定数書き起こし由来であり、
  テンプレ化の意義はむしろ再生成の決定性にある。

## 結果

検証機 `verify_fold24_external_20261120.py`（SHA-256 `9bc24e38…`・55,555 bytes）は
出版機・同梱監査機と実装を共有しない第三実装で、stdlibのみを使い、
D4座標変換・4×4 incidence行列の余因子展開・親行対応・frontier統計を明示的座標写像から再実装した。
fail-closedで、出力はソート済みkey・時刻なしの決定論的監査JSON 1点。

監査正本 `output/external-audit.json`（36,605 bytes・SHA-256 `c7e10332…`）の主要な内容:

- gate 800全PASS（P pin 5・I入力 65・X機械再実行 20・V同梱監査 4・C再導出 545・T tamper 6・E guard 155）。
- 出版機pristine再実行4回: 全実行receipt SHA-256が出版正本と一致（fold23 rerun chain込み）。
- 同梱独立監査再実行: 46/46・byte-identical。
- 全chain再導出: base 6,438行→fold23 frontier 6,126/485,438。C(8,6)=28部分幾何のD4正準行は
  2方法（C(8,2) 2石除去×8 D4像の完全合成28・部分集合のD4正準化28・合成ops 224）で一致。
  主張3行・closed edge cost 225・余剰0行。親delta 4親・class 2・計6。
  frontier_after: manifest 1,725・残S6 6,123・残cost 485,213・needed 4,431/351,661・incidence 11,660。
  五親target 86/112・残余26行。root 8石・universal modeのため再導出mobility 50・unsafe quads 0。
  全fieldが出版receipt正本の該当fieldと一致。
- tamper 2件（worklist offset 777・K1136証明書 offset 12345・1 byte XOR 0x01）: fail-closed捕捉。

監査正本は同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` 1回の3実行でbyte-identical
（`c7e10332…`・36,605 bytes）。出版直前に既定環境で4回目を再実行し、同一SHA-256・実測49.5秒を再確認した。
実行記録は[実験dir](../experiments/n11-fold24-external-second-verification-root438000000818-20261120/)の
`output/reproduction.log` に置いた。

## 出版

3部構成でmainに直接出版した（AGENTS.mdに従いbranch/PRは作らない）:

- part1: 実験dir 4ファイル（README・検証機・監査正本・実行記録）。
- part2: K1164 item ＋ 本logの前段として単一オーナー宣言ノートと本log。
- part3: knowledge README末尾へのK1164 bullet追記。

K番号はpart2 push直前に3点確認（item 404・README bullet・code search）で空きを確認した。

## 解釈上の制限

本検証で行を1行も閉じない。fold24 receiptが3行を閉じたのは出版社の成果簿記であり、
本レーンの成果はその外部第二検証の成立である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
