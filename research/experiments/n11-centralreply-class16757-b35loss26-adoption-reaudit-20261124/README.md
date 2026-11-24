# n11-centralreply-class16757-b35loss26-adoption-reaudit-20261124 (Part DW)

Part DW (2026-11-24): batch-35 (closure class 16757, Part DV probe drive)
の **26 fresh LOSS行のみ**を canonical exact-S5 chain cache に採用
(loss-only adoption・mixed packet・WIN行は1行も不消費) し、
reaudit (refresh fork + delta extractor) で閉鎖表・根覆盖・update8
要求の変化を fail-closed に機械検証した。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成

- `scripts/make_increments_b35loss26.py` maker (sha `57d276d4…`)
  - b35 kit `research/experiments/n11-centralreply-closure-class16757-batch35-20261124/`
    (MANIFEST `791996c1…` 109 files) を file-by-file sha検証
  - 28キーの two-pass fresh-cold raw 再検証 (`# replay_done` both passes)、
    status.log 30行 honest-history 照合 (first/final/marker 2行pin)、
    raw/batch-keys (legal,lo,hi,s5,mcc) 照合、raw inventory 56 primaries +
    sidecar 0、val-gate 4 molecule x 2 host (published-baseline + dv-host)
    node-exact、採用26キーの BASE 6,547行/quarantine 不在、
    不採用2キー (b032/b048) の BASE 不在、per-pass nodes 67,593,391、
    all-28 73,757,659
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha `90711961…`・
  selftest PASS・3回merge同一sha)
- `scripts/compare_deltas_b35loss26_adoption.py` extractor (sha `d20750fb…`)
- `reaudit/scripts/refresh_adoption_b35loss26.py` refresh fork
  (sha `4aaabcd5…`・DT `5533b3f9…` の fork・docstring と CACHE pin
  `23d40e36…` のみ変更)
- `output/increment-b35loss26-20261124.cache` (sha `10cb8589…`・26行)
- `output/increments-manifest.json` (sha `e925cf0c…`・schema
  b35loss26-increments-manifest-v1・`full_packet_eq_loss_only=false`・
  `win_scenario_exists=true`・unadopted WIN b032/b048・EXHAUSTED 0)
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `a2548c1a…`)
- `output/merged-exact-s5-chain-plus-...-plus-b35loss26-20261124.cache`
  (sha `23d40e36…`・**6,573行・WIN 158 / LOSS 6,415**)
- `output/decomp-deltas-b35loss26-adoption.json` (sha `d952a6cb…`・extractor出力)
- `reaudit/output/refresh-summary.json` (sha `5fe3e5ab…`)
- `reaudit/output/closure-classes.csv` (sha `b7241eb0…`・807行・
  class 16757行 = rank 4 / unknown 3 / groups 5)
- `reaudit/output/per-root-coverage.csv` (sha `f1abcd85…`・root 27 119/119)
- `reaudit/output/probe-worklist.csv` は体積 (~3.7MB) で非出版。
  regen pin sha `86767be9…` (refresh fork 再実行で byte一致をextractorが検証)

## 主要結果 (extractor fail-closed 検証済み)

- class 16757 (Board再生成 49子境界: 19 BASE exact LOSS + 1 update8
  receipt LOSS s5 558600 + 28 batch keys + b018): unknown **29→3**
  (残る3子 = 不消費WIN b018/b032/b048)・rank 7→4・groups_served 5→5。
  **free化も excluded化もされず unknown のまま**
- closure table 807行キープ (left 0 / entered 0)・rank churn 28行・
  unknown変化 micro-class 2件 (30118 55→54 own 1・30484 54→52 own 2)
- update8: resolved 188→214 (+26 = 採用26 s5全て)・remaining 31,671→31,645・
  groups_free_now 131 static・win_hit_groups []
- class_status_counts 完全 static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)
- tamper battery T1-T4 (raw tamper / status tamper / batch-keys tamper /
  merged verdict flip) 全て ABORT・復帰後 kit 109/109 再検証・
  merged cache byte再生成一致

## 不採用 (verdictは一切消費しない)

- WIN b032 (s5 556117) / b048 (s5 558553): scrutiny owner C++ 第二実装
  gate (pin `9193f5b6…`) 通過後のみ採用可 (本環境では実行不能)
- batch-1 WIN b018 (s5 528497): packet 外・引続き不消費
- EXHAUSTED 0

## pins (外部入力)

graph `54f9c364…` / update8 `b658290a…` / independent.py (Board)
`954d3a10…` / s5_evidence_policy.py `78655e94…` / quarantine
`81d23160…` / jsreplay `84585617…` / b35 kit MANIFEST `791996c1…` /
BASE (DT merged) `973bcd19…`
