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


## 欠損行クラス分割の独立監査

`python3 scripts/verify_classes.py --output output/class-partition-audit.json` を実行し、`classes.txt` の行反射軌道分割を独立に再構成した。

- 非空の欠損行集合: 127 個。
- 行反射 `y ↦ 6−y` で固定される非空集合: 15 個（4つの反射軌道の非空和集合）。
- 残る112集合は56組の二元軌道。
- Burnsideの補題による軌道数: `(127+15)/2 = 71`。
- 掲載代表: 71個、重複行0・重複軌道0・欠落軌道0・非正準代表0。

したがって `classes.txt` は、127個すべての非空欠損行集合を行反射で割った71軌道を、ちょうど一度ずつ覆う。これはクラス分割の完全性監査であり、SAT符号化・ソルバ結果・幾何配置の正しさを検査するものではない。

さらに幅を一般の $w\ge1$ とすると、行反射の行軌道は $\lceil w/2\rceil$ 個である。反射で固定される部分集合はそれらの軌道の和集合なので、空集合を含め $2^{\lceil w/2\rceil}$ 個。非空部分集合 $2^w-1$ 個にBurnsideの補題を適用すると、反射で割った非空部分集合の軌道数は

\[
N_w=\frac{(2^w-1)+(2^{\lceil w/2\rceil}-1)}2
=2^{w-1}+2^{\lceil w/2\rceil-1}-1.
\]

これはSAT探索前に必要な正準クラス数を見積もる一般式である。検証器は全部分集合の直接軌道列挙と閉形式を $w=1,\ldots,12$ で照合し、全て一致した（この有限照合は証明の代替ではなく、証明は上のBurnside計算による）。


- 検証器: `scripts/verify_classes.py`
- 結果: `output/class-partition-audit.json`


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

## Not claimed

- 7×30 以外の幅、(7,q≠6) 家族、Grundy 値、
  11×11 空盤・二石 root・S2・class 2・class 4 (いずれも UNKNOWN)。
