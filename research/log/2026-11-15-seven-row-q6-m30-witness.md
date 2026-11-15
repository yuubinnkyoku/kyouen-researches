# 2026-11-15 seven-row q6 m=30 witness (class-split)

## 作業開始時の状態

- 作業開始時の最新 main: `2d8c18e2f27641f3f4c0ee200d3270f008a1397e` (merge `f358c293` 時点)。
- root `AGENTS.md` と `research/knowledge/README.md` を確認。branch / PR は作らず main へ直接反映する方針を確認した。
- (7,6) 前線は 7×30。着手時点の境界: witness 帯 m=6..29 (m=29 は 34 石 rows [5,5,5,4,5,5,5] の空列延伸・js+py 二系統検証済み)・M_{7,6} ∈ [30, 862] (上界 K0318 substitution U=862)。
- 7×30 の既存記録は honest negatives のみ: rowY=0/1/2 250s INDET 796,125/822,483/847,765・rowY=3 280s INDET 929,785 → 900s INDET 1,569,306 (seven-row-q5-q8-sat-frontier-20261115)。空列延伸は cell (29,3) 未遮断で失敗。2 石 surgery 完全列挙負 (seven-row-q6-m30-surgery-completion-20261115・1,781,021 候補 0 safe-maximal・局所負)。
- 同日 six-row-q7-m22-class-split レーンが 6×22 の困難度較正で CLOSED/pivoted したため、7 行前線で最も抵抗が浅いと較正された (7,6) m=30 の class-split (71 正準欠損クラス・sat3.js・cap 600s・resumable) を不在判定狙いで着手した。

## 経過

1. **driver v1 abort bug**: 初版 sweep30.sh の SAT-abort 判定 `tail -1 records.jsonl | grep SAT` が対照 (7,29,6) の SAT record にも反応し、m=30 掃引開始前に誤終了した (record 無傷・1 クラスも未実行)。v2 で m=30 の record に限定して修正。(4,5) m=21 レーンの driver v2 per-key bugfix と同じ教訓: skip/abort 判定は必ず対象 record に限定する。
2. **対照 PASS (11:22Z)**: (7,29,6) class {3} **SAT 3,074,703 conflicts / 545.5s**。復号 witness 34 石 rows [5,5,5,4,5,5,5]・row 3 石は列 [4,12,26,28] (既刊の空列延伸 witness [3,8,11,27] とは別の m=29 witness)。sat.js verifyConfig + verify_witness.py (Python Fraction) の二系統検証 PASS。class-split 符号化・decode 鎖が (7,6) 家族で実地検証された。参考: 同幅 rowfixed rowY=3 SAT は 442,479 conflicts — class {3} instance の方が約 7 倍深い (6 行を exactly 5 に固定すると探索がむしろ難化する観測)。
3. **7×30 witness 発見 (11:33Z)**: class {3} (7,30,6) **SAT 2,670,296 conflicts / 497.0s** (cap 600 内・CNF md5 `09e969b9461e413551f61f76bff817ce`)。driver v2 が SAT を検出して掃引を即時打ち切り (他 70 クラスは不実施 = 不在主張なし)。**absence 不成立 → witness 帯延伸に転換**。

## witness と検証

**34 石 rows [5,5,5,4,5,5,5]・row 3 の石は列 [12,23,27,29]**。3 連続幅帯延長 m=28→29→30。3 系統検証 PASS:

1. `sat.js verifyConfig` (census) — ok, size 34, rows [5,5,5,4,5,5,5], minRow 4。
2. `verify_witness.py` (Python Fraction・census 不使用) — ok, n 34, min_row 4。
3. `verify_witness_det.js` (第三系統・純整数 4×4 行列式円判定・自己テスト 3 件組み込み・repo コード不使用) — ok, maxLine 5, maxCircle 5, uncovered 0。初版に det4 マイナー項の転写 bug があったが自己テストが検出し修正済み (検証器には自己テスト必須という教訓)。

**負対照 PASS**: 石 (12,3) を除去した摂動配置は py/det 両系統で not-maximal (cells [1,3],[5,3],[11,3],[12,3]) — 検証器が非極大を検出する実地確認。

**toolchain 備考**: sat3.js decode は `Math.max(...lits)` の spread が >65k 変数モデルで RangeError (m=30 は ~128k 変数)。モデル解析は独立 Python パーサ (model → stones) で実施。sat3.js blob 自体は不変。

## 結果と erratum

- **witness 帯 m=6..30 に延伸し M_{7,6} ∈ [31, 862]** (上界 U=862 不変)。7×30 の不在は不成立。
- **erratum 的再分類**: 7×30 の既存 rowY=0/1/2 250s INDET・rowY=3 280/900s INDET は witness 手前の打ち切り (pre-witness cut) だったことが確定。INDET は cap 到達であって不在主張ではないという解釈境界の実例。
- `results/fixed-width/mwq_stabilization.csv` の (7,6) 行を 30..862 → 31..862 に行全体置換で更新 (commit `85f1d441`)。
- 残る前線は **7×31**。

## 成果物と反映

- `research/experiments/seven-row-q6-m30-class-split-20261115/`: README.md (claim・被覆の完全性・手法較正・追記・結果)・classes.txt (71 正準類)・sweep30.sh (v2)・run_one.sh・scripts/ (sat3.js d03f908e・sat2.js 282ae832・sat.js 0cc6021a・verify_witness.py 0530d16 — いずれも既存 blob と同一、verify_witness_det.js は新規第三検証器)・output/ (records.jsonl・c3 witness 一式・対照 ctrl_7x29_c3 一式・raw kissat logs)。
- commits: `1f4ef426` (IN FLIGHT claim) → `b0f8fd5d` (対照 PASS + driver v2 fix) → `edbf0f54` (対照 raw log) → `68fdda6a` (witness 一式 + 第三検証器) → `c3bf6660` (raw log) → `85f1d441` (CSV)。
- 並走レーン (n11 class2、p=6247 整数論、census checkpoint 等) のコミットと merge 衝突なし。

## Not claimed

- 7×31 以遽の幅、(7,q≠6) 家族、7×30 の 71 クラス掃引完了 (c3 SAT で打ち切り・不在判定は不実施)。
- Grundy 値、11×11 空盤・二石 root・S2・class 2・class 4 (いずれも UNKNOWN)。
