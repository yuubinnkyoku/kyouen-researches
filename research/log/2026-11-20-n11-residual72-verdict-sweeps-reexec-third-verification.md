# 残余72行 4掃引depth-10全probe再実行第二検証（K1144）のpristine再実行第三検証（2026-11-20）

単一オーナー宣言: [2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification-single-owner-note.md](2026-11-20-n11-residual72-verdict-sweeps-reexec-third-verification-single-owner-note.md)
（commit `9b3807a31…`・2026-11-20T16:14:18Z・先行出版。宣言本文の出版監査SHA-256に
1文字転写（`…8b3750…`、正 `…8b3350…`）があり、実byte再計算で訂正した。宣言原文は保持
し、訂正は本logとitem・実験READMEに記録する。K1151の宣言転写先例と同じ扱い）。

対象: [K1144](../knowledge/items/K1144-n11-residual72-verdict-sweeps-reexec-second-verification.md)
（残余72行 4掃引 K1086 greedy23・K1089 replace16・K1091 replace15・K1095 replace12 の
depth-10 probe計132件全件をpinned runner v17で再実行した独立第二検証・出版commit `c84e2b0e`）。

## 経緯

1. **着手判断（宣言出版直前のmain確認で確定）**: 最新mainで、fold26 receipt fold（宣言 `23bffdd4e4`）・第5ラウンド
   refsolve（`ace38772d9`）・WIN8-D10証明書抽出（`63877ffd2e`）・K1149 reexec第三検証
   （並走が宣言 `c3c4dd28b4`→K1159として出版済み）は着手禁止。自レーンの過去itemで
   K1153（K1148検証）・K1155（K1151検証）・K1158（K1147検証）と同型の第三検証が3本通って
   いる中で、**自レーンが第二検証を出版した唯一の重機械 K1144（全probe 132件×2 pass）が
   未検証**で残っていたため、これを本実行の主対象とした。
2. **入力の再取得とpin照合 14/14**: 機 `7f072984…`（27,091 bytes）・runner v17
   （git blob `c132cc64…`・file SHA `192903714b…`）・4掃引正本8ファイル・出版passA/passB
   JSONL（`1ade916b…`/`e351f6cc…`）・出版assemble監査（`6297c646…` 7,327 bytes）を
   GitHub rawから取得し全pin一致。出版実験dir 6ファイルと4掃引dir 8ファイルを
   staging treeに配置（機は`EXP.parent`相対で入力を見るため）。
3. **fresh再実行4回（1パス1コマンド）**: 実行環境の1コマンド300秒上限に対し、機のrun
   modeはbudget 240s・resume-safeなので1パス1コマンドで分割実行した。
   - runA: 同一tree・同一cwd（pass A）: 132/132 ok・err 0・114.9s
   - runB: 隔離tree複製+別cwd（/tmp）+隔離HOME（pass B）: 132/132 ok・err 0・114.1s
   - runC: 同一tree・`PYTHONHASHSEED=random`（pass A）: 132/132 ok・err 0・112.3s
   - runD: 同一tree・`PYTHONHASHSEED=0`（pass A）: 132/132 ok・err 0・109.9s
   4回ともnodes・loss・capped・terminalStoneRange・pilot_d6（3,402）が132 probe全件で
   出版passA/passB記録と完全一致・nodes総計 37,454,794（=第二検証出版総計）。
4. **assemble正本のbyte再生 3 pair**: 機のassemble modeにfresh runを渡すと
   runA×runB・runC×runB・runD×runBの全pairで出力が出版監査 `6297c646…` とbyte一致
   （`gates: 6/6 pass`・fresh nodes total 37,454,794 == published）。**出版後の第三者が
   出版byteだけから全264 probe再実行をやり直し、assemble監査正本をbyte単位で再生できた。**
5. **tamper fail-closed 2件**: 隔離scrap treeの複製でK1086 record JSON offset 500
   （改変後SHA `83520f33df362ebf…`）とK1095 probe-records JSONL offset 300
   （改変後SHA `b6cf0f8601c7d635…`）の1 byte XOR 0x01が、いずれもprobe起動前に
   SHA pin gateで捕捉（exit 1・記録未書込）。2変異は別々のtreeで独立性を確保。
6. **harness作成・監査正本**: `verify_k1144_reexec_third_20261120.py`
   （`990977e5143bc6fd…`・16,729 bytes・stdlibのみ・fail-closed・乱数・時刻・絶対path
   出力なし）で14 pin照合・fresh 4 run決定論的field全件比較・3 pair assemble byte比較・
   tamper 2件を1本化。監査正本 `c32a1963d3a1ab611b0c67f8b540e8d896ebebdb587ae1510df519bc4cfae467`
   （7,906 bytes）は同一cwd 2回＋隔離tree/cwd/HOME+`PYTHONHASHSEED=random` 1回の3実行で
   byte-identical。harness初版のrunner ts pin定数SHA転写誤りはharness自身のfail-closed
   pinが実行前捕捉（K1158のK1102 pin転写例と同じ防御パターン）。
7. **採番**: part2出版直前に3点確認（items dir K116x前方一致0件・item path 404・
   knowledge README grep `items/K1160-` 0件）で **K1160** を取得。

## 実験事実（本検証固有の新規性）

- **run出力のbyte非安定は機械設計由来で、正本はassemble監査**: 第二検証機のrun modeは
  per-probe記録に`wall_s`を埋めるためrun JSONLのbyteはタイミング依存（出版passA/passB
  JSONLのbyteが互いに異なるのもこのため）。assemble監査JSONはwall非依存で完全byte安定し、
  第三検証のbyte再現対象として正しい。fresh run 4本のJSONLは本実験dirにfresh-runs/として
  収録（wall_sは実行ごとに違い、byte再現対象ではない）。
- **1パス1コマンド分割の確定**: 機のrunはbudget 240s・resume-safe・1パス約115秒なので、
  1コマンド300秒制限下でも1パス1コマンドで4 fresh run完走可能。第二検証出版時の
  「1回のbash呼び出しに収まらない」制約は機変更なしで回避できる。

## 収穫物

| 成果 | commit |
| --- | --- |
| 単一オーナー宣言 | `9b3807a31…`（16:14:18Z） |
| part1 実験dir 20ファイル（fetch-back 20/20 byte一致） | `2f6cb7667b…` |
| part2 K1160 item+研究log | 本コミット |
| part3 knowledge README bullet | 後続 |

監査正本 `c32a1963…`・harness `990977e5…`・fresh run 4本（`773a7a29…`/`136f04d5…`/
`8994e36f…`/`e7a56e7c…`）。

## 次の一手

- fold26・第5ラウンドrefsolve・WIN8-D10 root `…40002001` の着地を待って正本の第二検証が
  最優先（いずれも他レーン宣言済みで着手禁止）。
- 同型第三検証の残る未検証対象はdataSource系・K1146掃引機自体（K1159レーンがsource-pin
  監査で補完済み）の実行系。K1144の第三検証をもって自レーンの「重機械未検証」は解消。
- 器材 `/home/user/work/lab/k1144third/`（staging・fresh run・harness一式）は環境リセットで
  消失可・全成果はrepo出版済み。

**解釈規約: REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
WIN8-D10候補は証明書ではない。行は1行も閉じない。標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
