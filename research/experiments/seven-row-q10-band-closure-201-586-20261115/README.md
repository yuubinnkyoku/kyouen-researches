# seven-row-q10-band-closure-201-586-20261115

IN FLIGHT (claim). K0820 (7,10) witness-free band is 19..200 (m=19..100 by
`seven-row-q9-q10-bands-20261114`、m=101..200 by
`seven-row-q9-q10-band-extension-101-200-20261114`)。本実験は残る幅
**m=201..586** を掃引し、K0318 substitution 上界 U_{7,10}=587 と組み合わせて
**M_{7,10} = 19 の完全決着**（または帯内 SAT witness の発見・その場合は
M_{7,10} の下界更新と witness dual-verify）を目指す。

(7,9) の閉包 m=201..612 は `seven-row-q9-band-extension-201-612-20261114`
が IN FLIGHT（52fd92c1・genfast3 開発元）。本実験は **q=10 のみ**を対象とし、
同レーンが genfast3.js として commit 済みの chord-pair census 生成器を
**再利用**する（下記較正）。

## 手法

- 生成器: `seven-row-q9-band-extension-201-612-20261114/scripts/genfast3.js`
  （md5 12c2bd9cb3b24887fc3896f7ea9bcadf・chord-pair abstract-circle census・
  q >= w+2 限定 — q=10 >= 9 は要件を満たす）。CNF バイト一致較正は
  同フォルダの `controls_genfast3.json`（genfast.js 13 サンプル）に加え、
  本実験側で q=10 に特化した下記の較正を記録する。
- ソルバ: kissat 4.0.4 official linux-amd64・200s cap・def 単一節符号化
  （「ある行が q-1 石以下の極大安全配置が存在」の完全符号化・K0820 と同一）。
- スクリプト: `scripts/leanband3.sh`（1 幅: genfast3 生成 + kissat + JSONL
  record + SAT 時 decode/dual-verify）・`scripts/batchband3.sh`
  （wall-clock guard 付き連続実行）。

## 本実験側の較正（q=10）

- **CNF byte-identity vs genfast2.js**（cmp・同一 CLI オプション）:
  7x110 q10 def / 7x150 q10 def / 7x200 q10 def / 7x200 q10 --lex=H,V,HV —
  全 4 サンプル **MATCH**（genfast2.js は m=101..200 の q10 帯で
  実績のある生成器・`controls_byteid.json` で genfast.js と一致検証済み）。
- **instance-identity control**: leanband3.sh m=200 の再実行が
  band-extension レーンの record m=200 と bit-exact 一致
  （vars 36315 / clauses 132264 / curves 393 / kissat UNSAT 2941 conflicts）。

## スコープ

有限機械検証（census 完全性 — genfast3.js は chord-pair census で
q >= w+2 の全 q 点円を列挙（二重行 2 つから (v, ρ²) が u 非依存に決まる）・
CNF byte-identity で genfast2.js と一致 — とソルバ正確性まで）。
m=201..586 の各幅 UNSAT はその幅の行欠損極大非存在の完全証明。
全幅 UNSAT の場合、witness 幅集合 {10..18}（K0820）・witness-free 19..200
（K0820 + band-extension）・m >= 587 の持続性（K0318 substitution U=587）と
合わせ **M_{7,10} = 19 が exact に決着**する。

## 結果 (2026-11-15 完走)

**m=201..586 全 386 幅 kissat 4.0.4 def-mode UNSAT・SAT 0・INDET 0**
（conflicts 1,324..4,623・solve ≤1.0s/幅・200s cap 内完走・3 バッチ実行）。
生成は genfast3（m=586 で 1.0s・O(C(w,2)·m²·w) 弦対census）。

これにより **(7,10) の witness-free 帯は 19..586 に完全閉包**し、
K0318 substitution U=587（proved・m >= 587 で witness 不可能）と合わせて
**M_{7,10} = 19 が exact に決着**した（w=7 では初・w >= 6 でも初の完全決着。
CSV: exact-threshold 8 → 9 件）。

### 検証プロトコル（全て output/controls/ に記録）

- genfast3 vs genfast2 CNF byte-identity: 4/4 サンプル MATCH（上記較正）。
- instance-identity: leanband3 m=200 再実行 = band-extension レーン record と
  bit-exact（vars 36,315 / clauses 132,264 / curves 393 / UNSAT 2,941 conflicts）。
- 決定性: m=300 再生成・再解 = batch 記録と bit-exact（2,608 conflicts）。
- 別符号化交差確認: def+lex=H,V,HV が m=201 (2,076) / m=400 (9,841) /
  m=586 (7,652) すべて UNSAT。
- 着地検証: records.jsonl 386 行が remote で md5 f5e5fa78 で byte-exact
  （初回 push で read_file の 64KB トランケーションにより 328 行着地した
  欠陥を検出・再 push で修復）。生ログ 386 幅（output/q10-band/raw-logs/）・
  うち9幅（チャンク末尾）の末尾改行喪失を検出・修復（q9 レーンの 5590f225
  と同一の輸送アーティファクト・現状は全 386 ローカルとサイズ一致）。

### 成果物

- `output/q10-band/records.jsonl`: 386 records（m=201..586・全 UNSAT）
- `output/q10-band/raw-logs/`: 386 per-width kissat logs
- `output/controls/`: byteid JSON + 較正・交差確認ログ一式
- `scripts/leanband3.sh` / `scripts/batchband3.sh`: 実行スクリプト
  （genfast3.js は seven-row-q9-band-extension-201-612-20261114 から再利用・md5 12c2bd9c）
