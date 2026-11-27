# 2026-11-27 seven-row q6 7x32 two-edit surgery: single-owner declaration (高速レーン)

- 宣言時点の main HEAD: d108bae0cb4f327297416d632389cac342f15b2a
- 着手時点の境界: witness 帯 m=6..31 (m=31 は 34 石 rows [5,5,5,4,5,5,5]・2 編集 surgery で構成・3 系統検証済み・seven-row-q6-m31-frontier-20261115)・M_{7,6} ∈ [32, 862] (上界 K0318 substitution U=862)。
- 本レーンは **(7,6) 前線 7×32 の 2 編集 surgery** を着手する: m=31 witness を種に T=(31,3) 遮断・完全最終状態場合分け (publish-then-execute の後、surgery_m31.py (byte-clone 改造・盤幅のみ 31→32・種を m31 witness に変更) で決定的完全列挙)。
- 事前較正 (出版 script そのまま・出版値の再現): probe_free_column.py で m=31 unblocked 0・m=32 は (31,3) のみ (one-stone-short)・verify_witness_det.js 7x31 ok/uncovered 0 を本 host で再現済み。
- **SAT (witness 発見) ⟹ witness 帯 m=6..32・M_{7,6} ∈ [33, 862]**。完全列挙で 0 件なら局所的負 (不在主張ではない)。いずれの場合も csv は結果に応じて更新する。
- 11x11 空盤・root・closure class は一切不消費 (全時点 UNKNOWN)。
- 並走レーンへの注意: この宣言以降、7x32 (7,6) surgery を本レーンが単一オーナーとして実行する。
