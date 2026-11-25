# 2026-11-20 n11 残余72行 4掃引 depth-10 probe全件再実行による独立第二検証

## 着手判断

最新main（着手時 `cd7e9652ed`）・`AGENTS.md`・`research/knowledge/README.md`・
K1085〜K1102の残余72行レーンと11/20のsingle-owner noteを確認した。
現在進行中の並走案件はいずれも他レーンが単一オーナー宣言済みであり着手しない:

- fold26 WIN8 receipt fold root `0000000800000000380000000810000a`
  （commit `ba659878`/`e53cc60c`/`23bffdd4e4` 宣言）
- 残余23行のgreedy9根depth-10掃引 replace9
  （宣言ノート `2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md`）
- 36witness depth-10掃引（宣言済み）・residual23 lower-boundレーン（12:11Z出版）

既存の第二検証を点検したところ、K1093（replace16幾何・台帳）・K1102（K1097計画簿記）・
whole-record検証（K1075）はいずれも「DFPNエンジンの再実行は対象外」と明示している。
第1〜4ラウンド代替根掃引計132 probeのうち、出版機自身の再実行は各3件のspot-checkのみ
であり、**全件再実行による第二検証は存在しない**。そこで本レーンは単一オーナー宣言ノート
（commit `259e4019db88395a1b8ca48fda9d0b842665653a`・先行出版）で着手権を確定し、
検証機を実装して実施した。

## 方法

- 入力は4正本のrecord JSONとprobe-records JSONL、計8ファイルをSHA-256 pinで
  fail-closed読み出し（K1086 `3045e152…`/`773fef42…`・K1089 `808fbda1…`/`75fda6ad…`・
  K1091 `edd7ac84…`/`47165331…`・K1095 `335eca5e…`/`89e2c30d…`）。
  runner v17はgit blob SHA-1 `c132cc6425eee3feaeef1d697dd74f968cfedb59` で固定し、
  実験dir内pinned copyを起動ごとにblob照合した。
- 各recordからchild指定ルール（child = root − 最小セットビットのhex）を再導出して
  台帳と照合（root popcount 8・child popcount 7全件確認。raw child hexは識別簿記で
  engineには同一の石集合が渡る）。protocol定数（depth 10・cap 30,000,000・
  timeout 280秒・両AND順序・全probeのpilot_d6 control）を132 record全件で検査した。
- 出版内部整合を2段階で検査: probe-records JSONL値 vs 正本per_root表の全132 probe
  照合、正本classification pin（WIN8-D10 candidate 7/3/3/3根・REFUTED-D10 16/13/12/9根・
  nodes総計 18,032,471/6,339,079/7,383,022/5,700,222・capped 0・error 0）の再導入照合。
- **pass A**: このtree内で132 probe全件をrunner v17で再実行（resume-safe設計、
  budget 240秒、実行約117秒、error 0・timeout 0・capped 0）。
- **pass B**: 実験dirと4掃引dirの複製を別cwd・別HOMEに隔離し、pinned入力も隔離側
  複製（SHA-256再照合）から読んで132 probe全件を再実行（実行約119秒、error 0・timeout 0・
  capped 0）。
- **assemble**（6 gate、fail-closed）: runner blob pin・出版内部整合・出版classification pin・
  passA-vs-出版全132 probe全field一致・passB-vs-出版同様・passA-vs-passB全field一致。
  決定論的比較fieldはnodes・loss・capped・terminalStoneRangeで、wall_s等の計時値は除外。
  監査JSONは同一cwd 2回＋隔離cwd/HOME 1回の3実行でbyte-identicalを確認した。

## 結果（6/6 gate PASS・3実行byte-identical）

- **132 probe × 2 pass = 264回の再実行で出版記録と全件完全一致**（不一致0・欠落0・
  timeout 0・capped 0）。両passともnodes総計 37,454,794で4掃引の出版nodes総計
  （18,032,471+6,339,079+7,383,022+5,700,222）と正確に一致した。
- 再導入分類も出版と一致: WIN8-D10 candidate 7+3+3+3=16根・REFUTED-D10 16+13+12+9=50根・
  ordering衝突0。全probeのpilot_d6 controlが両pass同一（nodes 3,402・loss=false・uncapped）。
- これにより第1〜4ラウンド掃引の判定根拠（K1093の除外対象REFUTED-D10 50根と
  K1097以降のpool P構築の源流となったWIN8-D10 candidate 16根）が「出版時実行」
  「同一tree再実行」「隔離tree再実行」の3独立実行で支持された。K1092/K1094/K1097系
  のrefsolve（K1088/K1090/K1094の本体再実行）とfold26/replace9の着手には影響しない。
- 監査正本は3実行でbyte-identical
  （SHA-256 `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637`）。
  pass A生記録 SHA-256 `1ade916b…`、pass B生記録 SHA-256 `e351f6cc…`。

## 解釈規約

本検証は出版probe事実の再実行検査であり、行を1つも閉じない。`loss=true`（未打切り）は
当該8石rootのWIN8-within-depth-10 candidateを意味するのみで、行の閉鎖には別の証明書
抽出・三重検証・receipt foldが必要。REFUTED-D10はどの前段局面のLOSS証明でもなく、
代替プールの浸食にしか寄与しない。capped/timeoutは証拠にならないコスト下界（本検査では
0件）。node数・solved数を勝敗として読まない。信任境界は出版corpusと同一
（engine depth-10 verdict健全性）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
残余72→23行レーンの全行open。**

## 成果物

- `research/experiments/n11-residual72-verdict-sweeps-reexec-second-verification-20261120/`
  （README・scripts/verify_sweeps_reexec_20261120.py・pinned runner_v17.ts・
  output/verdict-sweeps-reexec-second-verification-20261120.json・
  passA/passB生probe-records JSONL）
- `research/knowledge/items/K1144-n11-residual72-verdict-sweeps-reexec-second-verification.md`
- 単一オーナー宣言ノート（commit `259e4019db`・先行出版済み）
