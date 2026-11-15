# seven-row-q6-m31-frontier-20261115

高速レーン。**IN FLIGHT claim (2026-11-15 11:44 UTC)**。

## Claim

- 本レーンは **(7,6) 前線 7×31 の witness 探索**を着手する。
  着手時点の境界: witness 帯 m=6..30 (m=30 は 34 石 rows [5,5,5,4,5,5,5]・
  row 3 石 [12,23,27,29]・class {3} class-split SAT・3 系統検証済み・
  seven-row-q6-m30-class-split-20261115)・**M_{7,6} ∈ [31, 862]**
  (上界 K0318 substitution U=862)。
- 手法 (困難度順):
  1. **空列延伸 probe** (構的・ Fraction 演算・自己テスト組み込み):
     m=30 witness を 7×31 以降にそのまま載せて極大性を検査。
  2. **class {3} (7,31,6) SAT** (sat3.js class-split・kissat 4.0.4・cap 1800s):
     m=30 で 2,670,296 conflicts/497.0s で SAT した同一符号化・同一欠損クラス
     (row 3 のみ欠損 = m=30 witness と同型) の直接延長。
  3. **2 編集 surgery** (m=30 witness を種に T=(30,3) 遮断・完全最終状態場合分け):
     SAT が cap で INDET の場合の構成ルート。
- **SAT ⟹ witness 帯 m=6..31・M_{7,6} ∈ [32, 862]**。INDET は honest negative
  (不在主張ではない)。

## 空列延伸 probe 結果 (着手直後・確定)

`scripts/probe_free_column.py` (純 Fraction・census 不使用・自己テスト 5 件組み込み):
m=30 witness の 7×30 極大性を再現 (unblocked 0・det 検証器と一致) の上、
**7×31 では唯一の未遮断セルは (30,3)**・7×32 以降は (30,3),(31,3),… と増加。
**空列延伸は失敗** (m=29→30 の (29,3) と同じ one-stone-short 構造)。
備考: probe 初版の外心 uy 公式に転写 bug (a² 項が (cx−bx) のべき所で (cy−by)) があり
m=30 極大性と矛盾する偽の未遮断 15 セルを報告した。自己テストで検出・修正済み
(det4 マイナー項転写 bug と同じ教訓: 幾何ルーチンには回帰自己テスト必須)。

## 手法・較正

- 生成器: sat3.js (md5 `d03f908ea99ba819caee2a6fbb471c1b`・
  seven-row-q6-m30-class-split-20261115 と同一 blob)。
  sat.js `0cc6021a`・sat2.js `282ae832`・verify_witness.py `0530d16`・
  verify_witness_det.js も同レーンと同一 blob。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  (md5 `3a5eba830aa6008a604fcc9bbe99a325`・rel-4.0.4 asset)。
- sat3.js decode は >65k 変数で spread overflow するため (m=31 は ~135k 変数)、
  SAT 時のモデル復号は独立 Python パーサで実施する (m=30 と同じ運用)。

## files / resume

- `scripts/probe_free_column.py` — 空列延伸 probe (自己テスト組み込み)。
- `output/probe-m30-witness-free-column.txt` — probe 記録。
- `run_one.sh` — 単一インスタンス runner (records.jsonl 増分記録・resumable)。
- `output/records.jsonl` — 1 インスタンス 1 行。

## Not claimed

- 7×32 以降の幅、(7,q≠6) 家族、7×31 の不在 (いずれのクラスも不在主張なし)。
- Grundy 値、11×11 関連 (すべて UNKNOWN)。
