# 2026-11-28 three-row q=4 m=27 SAT 行和分割 完了ログ（高速レーン）

単一オーナー宣言 `65e225583992c529dda764704ddfa8f69899b114`
（`2026-11-28-three-row-q4-m27-partition-continuation-note.md`・publish-then-execute）の
実行完了記録。出版 commit `ddbe1392`。本記録は同 kit の出版破損検出と
8コミットにわたる修復確定を含む完了ログである。

## 実行概要

- 目的: P(27)（3×27・q=4 行欠損極大 witness 非存在・列挙閉包で既確定）の
  SAT 行和分割による独立確認 = 2方法化。m≥28 の新幅主張なし（m=28 は
  並走の cfcdffde レーンが完了済み）。
- 器材: m25/m26 kit と同一 pin（sat.js/sat2.js/sat3.js/sat4.js/verify34.py・
  split_piece.py・partition_closure_3row.py〔board_tag=m27〕・kissat 4.0.4 公式
  linux-amd64・Node v22.20.0）。

## 本番実行（m=27）

- CNF 生成: cnf27/ 14件（row-k 4 + rspec 10）+ split323 27片 + split233 27片。
- 決定: **全68実行 UNSAT・INDET 0・呼び出し cap 超過片 0**
  （最大片 s233_c05 311,137 conflicts / wall 35s）。
- 台帳合計: **7,236,053 conflicts**（参考値・非加法）。
  row-k: (0,0) 573・(1,0) 393・(0,1) 76,386・(1,1) 89,809。
  row-sum: (0,2,0) 1・(1,2,0) 0・(1,2,1) 963・(2,2,0) 87・(2,2,1) 6,528・
  (3,2,0) 106・(3,2,1) 14,888・(2,2,2) 17,659・(3,2,2) 224,135・(2,3,2) 228,502。
  split: (3,2,3) 27片合計 2,882,830（max c06 232,947）・
  (2,3,3) 27片合計 3,693,193（max c05 311,137）。両家族の c26 は 0 conflicts
  （leftmost stone = 最右列は lex 制約で即時 UNSAT）。
- 閉包: `partition_closure_3row.py output/records_m27.jsonl m27` が
  **decided 63 / pending 0 / uncovered 0 / SAT 0**（exit 0）。
- 決定性: 再実行で conflicts bit-exact 一致（rc も一致）。
- 較正: m=26 全16 CNF を再生成し m26 kit 出版 manifest と **16/16 md5 byte-exact 一致**。

## 出版破損の検出と修復（正直開示）

- `ddbe1392` の push で kit 8ファイル中5ファイルしか作成されず、その5ファイルも
  原本と byte 不一致だった: (1) push 側で base64 復号を UTF-8 でなく
  1バイト1文字の JS 文字列化した二重エンコード mojibake、(2) 巨大 base64 の
  手写し転写損傷、(3) ledger_m27.jsonl と scripts 2件は出版自体が失敗（raw 404）。
- 検出: commit-pinned raw CDN fetch-back の crc32/長さ検査で全ファイル不一致を確認。
- 修復（各コミットで破損・原因・修復を開示・push 前 chunk-CRC 検証・
  push 後 commit-pinned fetch-back byte 検証）:
  - `5e03ad29` scripts/split_piece.py（m25 kit 版と byte-identical・crc32 572108556・1782B）
  - `07d32e0e` scripts/partition_closure_3row.py（m26 kit 版と byte-identical・crc32 831386518・2812B）
  - `751d9046` output/ledger_m27.jsonl（crc32 2287673564・7601B・68 runs rc=20）
  - `3e83f45b` output/cnf_manifest_m27.txt（crc32 1440482048・4176B・70 CNF md5）
  - `dfc8b856` output/records_m27.jsonl（crc32 2976458296・4483B・16 records）
  - `2fe61d9e` output/m27_partition_closure.json（crc32 3422606768・7522B・
    verified 16 records から decide() 語義を JS 再実装で決定論的再生成し原正本と
    crc 一致・これは意味論的独立検証も兼ねる）
  - `98f9bcd2` output/raw_decisions_m27.txt（crc32 4240742457・14318B・
    68 run 表から決定論的再生成・全272行 per-line CRC 検証）
  - `d4979501` README.md（crc32 3482239289・4855B・UTF-8 roundtrip 検証）
- 修復後、kit 全8ファイルが commit-pinned fetch-back でローカル正本と
  byte-identical であることを確認済み。なお fetch-back 検証には
  認証済み GitHub contents API を用いた（raw CDN 経由のテキスト抽出は
  長行折り返しの artifact があり byte 検証には不向きであることを本件で確認）。

## 正正直開示

- (3,2,3)/(2,3,3) のベース片一体実行は実施していない（m25 lane の教訓により
  分割片の全 UNSAT で反証する方式を継承）。
- verdict NOT consumed。本レーンは w=3 固定幅で標準 11×11 盤に無関係。
  **標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・conflicts は bookkeeping。**

## 意味

P(24), P(25), P(26), P(27), P(28) が SAT 分割・列挙閉包の2方法一致となった
（P(29..31) は列挙閉包単独のまま）。M_{3,4} ∈ [24,69] 不変・
witness-free 幅 {24..31} 不変・m≥32 は open（wsearch34.js 治具拡張が本命）。

## 成果物

- kit: `research/experiments/three-row-q4-m27-partition-20261128/`
  （README・scripts 2件・output 5件〔cnf_manifest_m27.txt・records_m27.jsonl・
  m27_partition_closure.json・raw_decisions_m27.txt・ledger_m27.jsonl〕・全8ファイル修復検証済み）
- K1183: artifacts・scope・追記4 を更新（commit `c39bc022`）。
