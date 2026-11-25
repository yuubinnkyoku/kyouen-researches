# Part EI 完了: b39loss46 (batch-39 honest-label 46 LOSS行) loss-only canonical adoption + reaudit 完了 (2026-11-25)

単一オーナー Part EI・publish-then-execute。batch-39 盤面 (closure
class 30484 rank-20 fresh-frontier) の honest-label exact-LOSS 46行
aj001..aj050 (aj030/aj039 EXHAUSTED 除外・aj049/aj050 probe-level
WIN 除外) を canonical exact-S5 chain cache に採用し、reaudit
(refresh + delta extractor) まで完了した。

| wave | 内容 | commit |
|---|---|---|
| 1a | kit scripts: maker `ff96435a…` + pinned merger byte-clone `90711961…`・push 前 git blob sha1 gate 2/2 一致 | `7400d708` |
| 1b | reaudit refresh fork `1bcf1972…`・blob gate 一致 | `cb93eb9a` |
| 1c | delta extractor `5433c4c2…`・blob gate 一致 | `29d0a0ff` |
| 2 | outputs 10 files (increment/manifest/merged cache/merge-audit ×3/decomp/closure/prc/refresh-summary)・push 前 blob gate 10/10 一致 | `cbe900bc` |
| 3 | README.md (7,667B) + MANIFEST-sha256.txt (14 entries) | `fd29f7db` |
| 4 | 本完了log | (本 commit) |

## 出版経路の正直な記録

- 前セッション末に発行された wave 1a 相当の push は結果確認が
  できぬままコンパクションした。本セッションで最新 main を取り直し
  (observed HEAD `f547c174`)、EI dir が main 上に存在しないことを
  get_file_contents で確認したのち、4 script を改めて実ファイルから
  byte 読み出し→JS 実装の git blob sha1 事前検証 (maker
  `1b4387a8…`・merger `a01ec2dc…`・refresh `857a675d…`・extractor
  `53603448…`, 各 sha256 pin `ff96435a…`/`90711961…`/`1bcf1972…`/
  `5433c4c2…` と一致) を通してから push した (1a〜1c)。以後の全
  push (10 outputs・README/MANIFEST) も同じ blob sha1 gate を
  push 前に pass している (表示経路の低頻度文字化け対策として、
  読み出しは tool→tool バイト経路で行い sha1 が不一致なら abort)。
- 実行環境のリセット事故: wave 1 push 完了直後に実行環境がリセット
  され、作業用ミラー (`/home/user/kr`) が消去された (lightweight
  sandbox の既知の制約・実験事実として記録)。ただし wave 1 はこの
  時点で出版済みだったため、main の tarball (3.4GB) を clean fetch
  し必要な 4 実験dir + quarantine を抽出・全 pin 再照合のうえ
  maker → merger ×3 → refresh → extractor の全成果物を再生成し、
  宣言済み pin と全 byte 同一であることを確認してから wave 2 を
  push した。結果として wave 2 は**出版バイトのみ**からなる
  完全な post-publication clean-room 実行になった (publish-then-
  execute の意図そのもの)。不足していた 4 依存ファイル
  (dependency-graph `54f9c364…`・repaired-joint-plan-update8
  `b658290a…`・independent.py `954d3a10…`・s5_evidence_policy
  `78655e94…`) は raw fetch し pin 照合で補充した。
- unauthenticated GitHub API の rate limit (60/h) に当セッション中
  に到達した。publish は全て authenticated github_app push_files
  で実施しており影響なし・fetch は raw.githubusercontent (CDN) に
  切り替えて継続した。簡潔に記録して次回に引き継ぐ。

## 採用結果 (honest label・verdict は 46 LOSS行のみを消費)

- 採用 46行 = Part EH batch-39 probe (178-file kit MANIFEST
  `52b69c04…`・two-pass fresh-cold node-exact @15M/order 0・
  MISMATCH 0・whole-packet nodes/pass 177,032,132 中の
  140,162,086)。maker は kit 178 file を file-by-file で byte
  検証し、status.log 54行・batch-audit `5a2b67cb…`・batch-keys
  `5e25b550…`・100 raws を pin 照合、46 キーの BASE 不在・
  quarantine 不在・prior-probe-universe 不在 (fresh gates) を
  fail-closed で検証した上で increment を emit した。
- increment `output/increment-b39loss46-20261125.cache` (3,310B)
  sha256 `a2b24baa…` (46行)。manifest `output/increments-manifest.json`
  (21,646B) sha256 `6ae4058b…` (schema b39loss46-increments-manifest-v1・
  full_packet_eq_loss_only=false・win_scenario_exists=true・
  adopted_table_digest `a7ef2336…`)。
- merged canonical
  `output/merged-exact-s5-chain-plus-b39loss46-20261125.cache`
  (279,805B) sha256 `73482be0…` = **BASE (Part EE `fc3e4ac9…`
  6,666行・WIN 158 / LOSS 6,508) + fresh 46行 = 6,712行・
  WIN 158 / LOSS 6,554** (unique・dup_elided 0・3回 merge 同一
  bytes・merge-audit ×3 同一 sha `387010c5…`)。
- **不消費の明示**: probe-level WIN 2行 {aj049 (nodes 4,998,452),
  aj050 (1,871,594)} は scrutiny owner C++ 第二実装 gate pin
  `9193f5b6…` 専権のまま本 Part では 1行も消費しない。EXHAUSTED
  2行 {aj030, aj039} は honest UNKNOWN (同一 15M 条件での再 probe
  禁止)。claim-reserved dual-class batch-38 2キー {ai044, ai048}
  は pair level で採用対象外 (Part EF in-flight single-owner・
  一切触れていない)。

## reaudit 機械導出の確定値 (extractor fail-closed 検証・全 byte 再現)

- **class 30484**: unknown **52→6**・rank **20→9**・groups_served 4
  static・**NOT freed・NOT excluded**。残 6子 = 2 EXHAUSTED {aj030,
  aj039} + 2 不消費 WIN {aj049, aj050} + 2 claim-reserved {ai044,
  ai048}。children_total_raw 54 (base known-loss 2・receipt 0・
  non-s5 0)。
- **class 30118**: secondary dual-class owner・unknown **54→52**
  (own adopted 2)・rank 39→21。
- class 16371 / 20421 / 34908: 全面 byte-static (採用キーは各 Board
  境界外・left/entered 交換なし)。
- closure表 (807行): fully_stable 776 + rank churn 29行 (rank 列の
  み。left/entered 空)。update8: 完全 byte-static (resolved 259 /
  remaining 31,600 / groups_free_now 131・newly_resolved []・全採用
  46 s5 index は凍結 baseline 要求の外側)。class_status: excluded
  390 / excluded_now 23 / free_now 39 / unknown 34,497 で不变。
  Board 検証 free 候補 39/39 verified・reject 0。
- metrics (bookkeeping・決して verdict ではない): joint greedy
  union 36,508→36,505 (unique_groups 2,115 static)・worklist
  64,414→64,366・known_universe 845→891・cache_in_universe
  822→868・root0 greedy 3,003→3,001 (free 7/7・uncovered 112/112)・
  root24 greedy 2,827→2,782 (free 12/12・uncovered 107/107)・
  root27 119/119・**free/uncovered は全 root で完全同一 (= 何も
  free 化していない)**。
- decomp `output/decomp-deltas-b39loss46-adoption.json` (10,309B)
  sha256 `6b8b3e7d…`。reaudit outputs: closure-classes.csv
  (807行) `e12bf328…`・per-root-coverage.csv `2525f306…`・
  refresh-summary.json `414314eb…`。probe-worklist.csv は**出版
  しない** (3,721,259B・size policy)・regen pin `98529a8d…` を
  MANIFEST ヘッダに記載 (出版 refresh fork + cache pin から誰でも
  再生成可能・clean-room 再実行で byte 同一確認済み)。

## 解釈ガード

- **標準 11×11 空盤は UNKNOWN。19 central-reply root も全て
  UNKNOWN。二石root も class 1/2/4 も全て UNKNOWN。**
- nodes は bookkeeping であり勝敗・距離の主張ではない。pn/dn
  ではない。solved 数は勝敗ではない。
- loss-only adoption は class を free化も excluded化もしない
  (class 30484 は残 6子のため unknown のまま・reaudit の機械導出
  で確定済み)。
- class 30484 の残 6子の扱い: (a) scrutiny gate 通過後の WIN 行
  採用 Part (C++ 環境専権)・(b) EXHAUSTED 2行の異条件 budget
  ladder (同一 15M 条件の再 probe は禁止)・(c) その他 fresh 最上位
  class からの新規 batch probe。claim-reserved {ai044, ai048} は
  Part EF 完結まで触れない。最終選定は次 Part の宣言が fail-closed
  maker で行う。

## 実験dir・正本

- `research/experiments/n11-centralreply-b39loss46-adoption-reaudit-20261125/`
  (README 7,667B・MANIFEST-sha256.txt 14 entries = scripts 3 +
  reaudit script 1 + outputs 7 + reaudit outputs 3・README/MANIFEST
  self-exclusion)
- 依存 byte (Part EH batch-39 kit): MANIFEST `52b69c04…` (178
  files)・status.log `08d70bb7…` (54行)・batch-audit `5a2b67cb…`・
  batch-keys `5e25b550…`・jsreplay `84585617…`・runbatch
  `f591f8c2…`・EE BASE cache `fc3e4ac9…`・quarantine
  `81d23160…`・graph `54f9c364…`・update8 `b658290a…`・board
  `954d3a10…`・policy `78655e94…`。
- hourly 並走があるため、各 wave の push 直前に必ず最新 main を
  取り直した (wave 1a 前 HEAD `f547c174`→push 後 `7400d708`、
  wave 2 前 `29d0a0ff` 一致確認、wave 3 前 `cbe900bc` 一致確認)。
  競合・同時書き込みは今 Part では発生していない。
