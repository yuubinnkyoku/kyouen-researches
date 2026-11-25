# eight-row-q10-band-closure-26-939-20261115

IN FLIGHT (band sweep in progress). (8,10) の現状: 行欠損極大 witness は m=10..25
（`eight-row-bands-20261114` w8q10 witness-search・m=25 SAT 1,221,994 conflicts・
71石 rows [9,9,9,8,9,9,9,9]）、上界 **U_{8,10}=940**（K0318 曲線パッキング代入・
`seven-row-inband-families-20261114` の w7_upper_bounds.json w=8 行）。
本実験は残る帯 **m=26..939** の掃引に貢献し、**M_{8,10} の完全決着**
（全幅 UNSAT なら M=26・w=8 で初）または帯内 SAT witness の発見を目指す。

## 並走実験との分担（重要）

同じ (8,10) 帯閉包を **`eight-row-q10-band-closure-20261115/`**（並走セッション・
難所帯レーン）も掃引している。両者の claim は同一対象で独立に出された
（本 claim は 461475f4・対側 claim は同日）。現時点の分担:

- **対側（難所帯レーン）**: 難度プローブ、m=26..59 難所帯の長時間 cap 掃引
  （43..60 UNSAT・cap ≤250s、m=42 INDET 250s/6,309,677 conflicts honest negative・
  m=27/28/29/31 プローブ INDET）、サンプル幅 80/100/150/200/300/500/700/939 UNSAT
  （m=939 42s/116,323 conflicts で上限側の直接確認済み）。
- **本実験（連続掃引レーン）**: 易幅帯の連続掃引 — **61..69 UNSAT**（def 62..103s・
  h chunks）・**70..138 UNSAT**（def 13..45s 連続・c chunks）・**501..513 UNSAT**
  （def 22..58s）・53..60 UNSAT（def 112..142s・対側と bit-exact 一致・下記）。

**クロス検証**: m=53..60 の def-mode UNSAT が両セッションで同一 conflict 数
（59: 1,520,195・60: 1,529,015・53: 1,970,208 等・独立実行・同一 CNF md5）を
再現 — kissat 決定性 + genfast3 CNF 同一性の独立確認。

## 手法

- CNF 生成: **genfast3.js**（弦対抽象円 census・q≥w+2 限定・
  `seven-row-q9-band-extension-201-612-20261114` から verbatim・md5 12c2bd9c）。
  (8,10) は q=10 ≥ w+2=10 で適用条件を満たす。
- ソルバ: kissat 4.0.4 official linux-amd64・def 単一節符号化・200s cap。
- スクリプト: `scripts/leanband3.sh`（1 幅）・`scripts/batchband3.sh`（連続・
  wall-clock guard）・`scripts/hardzone.sh`/`scripts/hardbatch.sh`
  （難所帯: def → INDET 時 def+lex=H,V,HV 交差符号化）。
- decode/dual-verify: decode_verify.js + verify_witness.py（SEVEN_SCRIPTS 経由・
  Python Fraction 独立検証・SAT 時全 w8q10 witness と同じ手順）。

## 較正（`output/controls/` に記録・2026-11-14 実施）

- **CNF byte-identity vs genfast.js**: 8x26 def / 8x32 def / 8x32 def+lex=H,V,HV —
  3/3 MATCH（md5 56e792a3 / ad405e97 / 2184f98b・byteid.jsonl）。
- **instance-identity**: 8x26 def meta（vars 8,963 / clauses 32,612 / curves 129）が
  eight-row-bands m=26 frontier record と bit-exact。陽性対照 8x20 def SAT 703
  conflicts・8x25 def SAT 1,221,994 conflicts — eight-row-bands records と bit-exact
  （instance-identity.jsonl + m20/m25 kissat logs）。
- パイプライン smoke: leanband3 8x20 SAT witness decode → jsVerify ok (71 stones,
  rows [9,9,9,9,8,9,9,9]) + pyVerify ok。

## 結果（2026-11-15 時点・records-chunks/ + 対側 records.jsonl 参照）

- **witness-free 連続区間 43..138**（43..60: 対側 + 本レーン 53..60 bit-exact 重複
  確認・61..69: 本レーン h0001/h0002・70..138: 本レーン c chunks）。
- 501..513 UNSAT（本レーン laneB・c0001/c0002 chunks）。
- 対側サンプル 150/200/300/500/700/939 UNSAT。
- **難所フロンティア 26..42 未解決**: m=26 は eight-row-bands の4符号化
  （def/rowY=3/rowY=3lexH/rowY=4）すべて INDET、m=27/28/29/31/42 はプローブ INDET
  （60..250s caps）、m=30/32..41 未掃引。m=31 は本レーン 200s cap でも INDET
  （4,823,685 conflicts・frontier-probes + records c0001）。
- M_{8,10} ∈ [26,940] のまま（前線 26..42 が律速）。

## 進捗・障害記録

- 2026-11-15: IN FLIGHT claim（461475f4）+ 較正完了。
- 2026-11-15: laneA 79..138・laneB 501..513・laneC 61..69・laneD 60..55 掃引、
  chunks c0001..c0004 / h0001..h0003 push（バッチごと即時 push・md5 記録）。
- 2026-11-14T23:05Z 前後: 実行環境障害（2回の sandbox reset + filesystem rollback
  failure）でバックグラウンドレーン死亡。push 済み外の laneA 139..151・
  laneD 52..52 相当は喪失（未 push のため記録対象外・再実行必要）。
  laneD（53..32 方向）は対側難所帯レーンと重複するため廃止（対側が 250s cap で
  上位互換）。再開時は laneA を m=139 から・laneB を m=514 から再開すること。
- 次回: laneA 139..500・laneB 514..939 掃引継続、難所 26..42 は対側レーン
  （rowY 分割・長 cap）または K0818/K0819 型クラス分割で攻略。

## scripts

- `leanband3.sh` / `batchband3.sh` / `hardzone.sh` / `hardbatch.sh`
  （KISSAT_BIN / SEVEN_SCRIPTS / GENFAST3_JS 環境変数でパス上書き可）。
- `decode_verify.js` — verbatim from eight-row-bands-20261114/scripts。
- genfast3.js は複製せず `seven-row-q9-band-extension-201-612-20261114/scripts/`
  （md5 12c2bd9c）を GENFAST3_JS で指定。sat.js / sat2.js / verify_witness.py は
  `seven-row-inband-families-20261114/scripts/` を SEVEN_SCRIPTS 経由で使用。

## 成果物

- `output/q10-band/records-chunks/`: c0001..c0004 + manifest.jsonl
  （records.jsonl は chunk 連結で再構成可能・manifest に md5/行数/m 列挙）。
- `output/q10-hardzone/records-chunks/`: h0001..h0003 + 上記 manifest。
- `output/controls/`: byteid.jsonl・instance-identity.jsonl・frontier-probes.jsonl・
  m20/m25 kissat logs。
