# seven-row-q6-m32-class-split-20261118

高速レーン。**IN FLIGHT claim (2026-11-18 07:20 UTC)**。

## Claim

- 本レーンは **(7,6) 前線 7×32 の class {3} class-split SAT witness 探索**を着手する
  (sat3.js `--class=3`・kissat 4.0.4・cap 5400s・resumable・records 増分 push)。
- 着手時点の境界: witness 帯 m=6..31 (m=31 は 34 石 rows [5,5,5,4,5,5,5] の
  surgery 構成・3 系統検証済み・seven-row-q6-m31-frontier-20261115)・
  **M_{7,6} ∈ [32, 862]** (上界 K0318 substitution U=862)。
- m=32 の既存 honest negatives: m=31 witness を種にした **2 編集 surgery 完全列挙
  は 2,224,675 一意候補・safe-maximal 0 件** (seven-row-q6-m32-surgery-negative-20261115・
  局所負記録・T=(31,3) センサス c4=1 直線 y=3 のみ・31s)。
  空列延伸は cell (31,3) 未遮断で失敗 (one-stone-short)。
  class {3} (7,31,6) SAT は cap 1800s で INDET 4,368,709 conflicts/896s process
  (witness は class {3} に属するため instance は SAT 確定・記録は m31-frontier)。
  2026-11-15 セッションで (7,32,6) c3 の並行実行が言及されたが record なし
  (環境リセットで喪失したものと解釈・本 dir が再着手)。
- **SAT ⟹ witness 帯 m=6..32 に延伸し M_{7,6} ∈ [33, 862]**。
  UNSAT ⟹ class {3} では 7×32 に witness なし (**7×32 全体の不在主張ではない**・
  他 70 正準クラス・3 編集 surgery・別 seed が残る)。
- 探索成功時は追加で空列延伸 probe (7×33 以降)・可能なら追加幅の
  witness 探索も同セッションで実施する。

## 手法・較正

- 生成器: sat3.js (md5 `d03f908ea99ba819caee2a6fbb471c1b`・
  seven-row-q6-m30-class-split-20261115 と同一 blob・`--class=D` で D 内の行を
  ≤4 石・D 外の行を exactly 5 石に固定)。sat.js `0cc6021a…`・
  verify_witness.py `0530d16…`・verify_witness_det.js も同レーン pin と一致確認済み。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  (md5 `3a5eba830aa6008a604fcc9bbe99a325`・rel-4.0.4 asset)。
- 対照: **(7,30,6) class {3} の再実行で SAT 2,670,296 conflicts の bit-exact 再現**
  (出版 record c3_7x30・cnf_md5 `09e969b9461e413551f61f76bff817ce`・
  witness row 3 石 [12,23,27,29] の復号まで含む end-to-end 制御)。
- sat3.js decode は >65k 変数で spread overflow するため (m=32 は ~150k 変数)、
  SAT 時のモデル復号は独立 Python パーサで実施する (m=30/m=31 と同じ運用)。
- CNF 生成は決定的 (同一引数 → 同一 md5)。cap 内完了インスタンスの conflicts は
  kissat 決定性により bit-exact 再現可能。cap 打ち切りの conflicts は実行速度依存
  (bit-exact 主張はしない)。
- witness は 3 系統検証 (sat.js verifyConfig・verify_witness.py Python Fraction・
  verify_witness_det.js 純整数 4×4 行列式) + 負対照 (1 石除去摂動が
  非極大と検出されること) を要求する。

## Not claimed

- 7×32 全体の不在 (class {3} の UNSAT は不在主張ではない)・7×33 以降の不在、
  (7,q≠6) 家族、Grundy 値、
  11×11 空盤・二石 root・S2・class 2・class 4 (いずれも UNKNOWN)。

## files / resume

- `run_one.sh` — 単一インスタンス runner (records.jsonl 増分記録・resumable・
  seven-row-q6-m30-class-split-20261115 の runner と同一構造・KS path のみ環境差し替え)。
- `scripts/` — 上記 pin 済み 6 file + probe_free_column.py
  (seven-row-q6-m31-frontier-20261115 と同一 blob)。
- `output/records.jsonl` — 1 インスタンス 1 行・増分 push。
- resume: 本 dir を作業 dir に展開し
  `KEY=c3_7x32 CAP=5400 nohup setsid bash run_one.sh c3_7x32 7 32 3 > output/c3_7x32.launch.log 2>&1 < /dev/null &`
  (起動前/proc 走査で二重起動防止。環境リセット後は kissat を rel-4.0.4 asset
  から再取得・md5 照合)。
