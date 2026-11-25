# seven-row-q6-m30-class-split-20261115

高速レーン。**IN FLIGHT claim (2026-11-15 11:15 UTC)**。

## Claim

- 本レーンは **(7,6) 前線 7×30 の 71 正準欠損クラス完全掃引**を着手する
  (sat3.js class-split・cap 600s・resumable・records 増分 push)。
  対照として先に (7,29,6) class {3} を実行する。
- 着手時点の境界: witness 帯 m=6..29 (m=29 は 34石 rows [5,5,5,4,5,5,5] の空列延伸・
  js+py 二系統検証済み)・**M_{7,6} ∈ [30, 862]** (上界 K0318 substitution U=862)。
- m=30 の既存 honest negatives: rowY=0/1/2 250s INDET 796,125/822,483/847,765・
  rowY=3 280s INDET 929,785 → 900s INDET 1,569,306
  (seven-row-q5-q8-sat-frontier-20261115)。空列延伸は cell (29,3) 未遮断で失敗。
  2石 surgery 完全列挙負 (seven-row-q6-m30-surgery-completion-20261115・
  1,781,021 候補 0 safe-maximal・局所負)。
- **全 71 クラス UNSAT ⟹ 7×30 欠損極大不在が確定し M_{7,6} = 30 or ≥ 32**
  (K0821-audit 規約)。**SAT ⟹ witness 帯は m=6..30 に延伸し M_{7,6} ∈ [31, 862]**。
- INDET クラスは cap 到達であり不在主張ではない。INDET クラスは
  k/minpos 分解 (k∈0..4 × p∈0..14・sound H-split: min(x₁, 29−x_k) ≤ ⌊(m−1)/2⌋ = 14)
  または krow pin で追分解する (run_one.sh に extra を渡す・新キー)。
- repo 検索時点で 7×30 class-split 掃引は未着手・未 claim
  (six-row-q7-m22-class-split-20261115 は 6×22 で pivoted-away・別家族)。

## 被覆の完全性

- 欠損クラス = 石数 ≤ q−2 = 4 の行の集合。safe な行は ≤ q−1 = 5 石なので、
  各行は FULL (5) か欠損 (≤4) のいずれか。
- 行ミラー V (行 i ↔ 6−i) で類別すると非空正準クラスは **71 個**
  (4 singleton {0},{1},{2},{3} + 67 multi)。classes.txt が全列挙。
- 任意の欠損極大配置の欠損行集合 D ≠ ∅ は V-mirror でちょうど 1 つの正準類に
  落ちる (V は盤の対称で SAT/UNSAT を保存する)。71 クラス全 UNSAT ⟹ 不在。
- sat3.js `--class=D` は D 内の行を ≤4、D 外の行を exactly 5 に固定
  (rowGe 単位制約)。census core は sat2.js (K0810)。

## 手法・較正

- 生成器: sat3.js (md5 `d03f908ea99ba819caee2a6fbb471c1b`・
  four-row-q5-m21-class-split / five-row-q5-m26-extend と同一 blob)。
  sat2.js `282ae832efa0080127c6c153e65e1c3c`・sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・
  verify_witness.py `0530d166572987988a01ec40dee12d4c`
  (seven-row-q7-witness-search-20261114/scripts の各 blob と一致を確認済み)。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  (md5 `3a5eba830aa6008a604fcc9bbe99a325`・rel-4.0.4 asset)。
- 対照: (7,29,6) class {3} — m=29 witness rows [5,5,5,4,5,5,5] を含むため
  **SAT でなければならない**。SAT 復号 witness は sat3.js decode verifyConfig +
  verify_witness.py (Python Fraction) の二系統検証。
- CNF 生成は決定的 (同一引数 → 同一 md5)。cap 内完了インスタンスの conflicts は
  kissat 決定性により bit-exact 再現可能。cap 打ち切りの conflicts は実行速度依存
  (bit-exact 主張はしない)。

## files / resume

- `classes.txt` — 71 正準類 (witness-regime 順: {3} → singletons → multi)。
- `sweep30.sh` — driver (SAT で即時打ち切り・band 延伸を最優先)。
- `run_one.sh` — 単一インスタンス runner (escalation にも使用)。
- `output/records.jsonl` — 1 インスタンス 1 行・増分 push。
- resume: 本 dir を作業 dir に展開し
  `nohup setsid bash sweep30.sh > output/sweep30.log 2>&1 < /dev/null &`
  (起動前/proc 走査で二重起動防止。環境リセット後は kissat を rel-4.0.4 asset
  から再取得・md5 照合)。

## 追記: driver v1 abort bugfix (2026-11-15)

初版 sweep30.sh の SAT-abort 判定 `tail -1 records.jsonl | grep SAT` が対照
(ctrl_7x29_c3・m=29) の SAT record にも反応し、m=30 クラス掃引開始前に即
aborted した (誤終了・record は無傷・1 クラスも未実行)。
**v2 では m=30 の record に限定**した (`'"m":30'` と `'"result":"SAT"'` の両方を
要求)。(4,5) m=21 レーンの driver v2 per-key bugfix と同じ教訓: skip/abort
判定は必ず対象 record に限定する。

## 追記: 対照 (7,29,6) class {3} PASS (2026-11-15 11:22Z)

**SAT 3,074,703 conflicts / 545.5s (cap 900 内)**。
復号 witness 34石 rows [5,5,5,4,5,5,5]・row 3 の石は列 [4,12,26,28]
(既刊の空列延伸 witness [3,8,11,27] とは**別の m=29 witness**。
sat3.js decode verifyConfig PASS + verify_witness.py Python Fraction PASS の
二系統検証)。class-split 符号化・decode 鎖が (7,6) 家族で実地検証された。
参考: 同幅の rowfixed rowY=3 SAT は 442,479 conflicts
(seven-row-q5-q8-sat-frontier-20261115) — class {3} instance の方が約 7 倍
深い (6行を exactly 5 に固定すると SAT 探索がむしろ難化する観測)。

## 結果: 7×30 witness 発見 — witness 帯 m=6..30・M_{7,6} ∈ [31, 862] (2026-11-15 11:33Z)

**class {3} (7,30,6) SAT: 2,670,296 conflicts / 497.0s (cap 600 内・cnf_md5
`09e969b9461e413551f61f76bff817ce`)**。driver v2 が SAT を検出して掃引を即時
打ち切り (SWEEP_SAT_ABORT・他 70 クラスは不実施 = 不在主張なし)。

**witness: 34石 rows [5,5,5,4,5,5,5]・row 3 の石は列 [12,23,27,29]**
(3 番目の連続幅帯延長 m=28→29→30)。**3 系統検証 PASS**:

1. `sat.js verifyConfig` (census) — ok, size 34, rows [5,5,5,4,5,5,5], minRow 4。
2. `verify_witness.py` (Python Fraction・census 不使用) — ok, n 34, min_row 4。
3. `verify_witness_det.js` (第三系統・純整数 4×4 行列式円判定・自己テスト
   3 件組み込み・repo コード不使用) — ok, maxLine 5, maxCircle 5, uncovered 0。

**負対照 PASS**: 石 (12,3) を除去した摂動配置は py/det 両系統で not-maximal
(cells [1,3],[5,3],[11,3],[12,3]) — 検証器が非極大を検出する実地確認。
**toolchain 備考**: sat3.js decode は `Math.max(...lits)` の spread が
>65k 変数モデルで RangeError (m=30 は 123,533→128k 変数系)。モデル解析は
独立 Python パーサ (output/c3.model.txt → c3.stones.json) で実施。
sat3.js blob 自体は不変 (他レーンの較正に影響しない)。

よって **witness 帯 m=6..30 に延伸し M_{7,6} ∈ [31, 862]** (上界 K0318
substitution U=862 不変)。7×30 の不在は不成立 — rowY=0/1/2 の既存 250s
INDET と rowY=3 の 900s INDET は witness 手前の打ち切りだったことが確定。
残る前線は 7×31。

## Not claimed

- 7×30 以外の幅、(7,q≠6) 家族、Grundy 値、
  11×11 空盤・二石 root・S2・class 2・class 4 (いずれも UNKNOWN)。
