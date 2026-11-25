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

## 結果: 7×31 witness 発見 (surgery) — witness 帯 m=6..31・M_{7,6} ∈ [32, 862] (2026-11-15 11:58 UTC)

**2 編集 surgery 完全列挙が m=30 witness の 2 石移動で m=31 witness を発見**
(SAT 不使用・決定的構成・**solver-free** で SAT 前線の先の 2 例目・
(6,4) m=46 空列追加に次ぐ (7,6) での初の surgery 構成)。

- **surgery: R = {(19,2), (25,4)} → A = {(27,2), (29,4)}**
  (seed の 2 石を移動。rows は [5,5,5,4,5,5,5] のまま単一欠損・34 石)。
- **完全列挙**: 最終状態場合分け (T 占有 / c4・t=0 1 追加 / c4・t=1・c3 2 追加)
  ・**2,140,633 一意候補**・safe かつ maximal は **1 件のみ** —
  m=30 witness の ≤2 編集近傍には m=31 witness がちょうど 1 つだけ存在
  (m=29→30 の場合は 0 件だったのと対照的)。
- T=(30,3) 曲線センサス: c4 = 2 (直線 y=3・空セル 26、円
  {(22,2),(23,3),(25,4),(28,4)}・空セル 1)・c3 = 11。blocking 曲線は
  (27,2),(29,4) を含む c3 円 (3 seed 石 + 両追加石 = 5) 経由。
- **3 系統検証 PASS**:
  1. `verify_witness.py` (Python Fraction・census 不使用) — ok, 34 石, min_row 4。
  2. `verify_witness_det.js` (純整数 4×4 行列式・自己テスト組み込み) —
     maxLine 5, maxCircle 5, uncovered 0。
  3. `probe_free_column.py` (第三 Fraction 実装) — 7×31 unblocked 0
     (7×32 は (31,3) のみ未遮断 = 次前線の one-stone-short 構造)。
- **負対照 PASS**: 石 (29,4) 除去の摂動配置を py (not-maximal・cells
  [30,3],[0,4],…)・det (uncovered 22) 両系統が検出。
- 備考 (script 開発過程): (1) surgery 初版は除去石セルの再遮断と移動
  (re-add) を含む安全性を统一的に扱っていなかった → 曲線を「盤上全セル」
  表現で |C∩S'| = |st_on−R| + |A∩full| に統一。(2) 直線キーの gcd
  正規化漏れで同一幾何直線が重複 (census 表示の重複・候補数には無影響・
  列挙の完全性にも無影響) → 修正済み。**幾何ルーチンには正規化と
  自己テスト必須**という m=30 レーンの教訓の再確認。

**witness 帯は m=6..31 に延伸し M_{7,6} ∈ [32, 862]**。残る前線は 7×32
(m=31 witness の空列延伸は cell (31,3) 未遮断で失敗 — one-stone-short)。

## 結果: class {3} (7,31,6) SAT — cap 到達 INDET (honest negative)

cap 1800s wall (timeout wrapper) で **INDET (rc=124・SIGTERM)**:
**4,368,709 conflicts / process-time 896.03s** (CNF md5 48eb715f96ac1f0be4a8c5429025483d・
145k 変数・520k 節・再生成バイト一致)。m=30 c3 が 2,670,296 conflicts/497s で SAT した
のに対し 1.64 倍深くても未解決。witness (surgery) は class {3} に属するため
instance は SAT 確定 — INDET は cap 到達であって不在主張ではない。
この時点で CPU を m=32 c3 実行と共有していたため process-time は wall の半分
(逐次実行なら更に深くまで到達したはず)。
**SAT より surgery の方が m=31 を先に解いた** — witness の疎分布と
cap ベース honest negative の解釈境界の実例。

備考: セッション中のサンドボックスリセットにより最初の実行 (~1131s process-time・
5.79M conflicts) は中断。CNF 再生成は md5 同一 (環境リセット横断の決定性確認)・
kissat は同一公式バイナリ (md5 3a5eba830aa6008a604fcc9bbe99a325) で再実行した。
