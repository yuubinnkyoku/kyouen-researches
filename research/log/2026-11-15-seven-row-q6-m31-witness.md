# 2026-11-15 (7,6) m=31 witness surgery セッションログ

- 着手時点の main: 01cc386d (自レーンの IN FLIGHT claim 直後)。境界:
  witness 帯 m=6..30 (m=30 は 34 石 rows [5,5,5,4,5,5,5]・row 3 石 [12,23,27,29]・
  class {3} class-split SAT・3 系統検証済み)・**M_{7,6} ∈ [31, 862]**。
- 発見順:
  1. **空列延伸 probe** (probe_free_column.py・純 Fraction・自己テスト 5 件):
     m=30 witness の 7×30 極大性を再現 (unblocked 0・det 検証器と一致) の上、
     **7×31 では唯一の未遮断セルは (30,3)** (one-stone-short・m=29→30 の (29,3) と
     同型)。7×32 以降は (30,3),(31,3),… と増加。空列延伸は失敗。
  2. **2 編集 surgery 完全列挙** (surgery_m31.py・seed = m=30 witness・T=(30,3)):
     最終状態場合分け (T 占有 / c4・t=0 の 1 追加 / c4・t=1 と c3 の 2 追加) は完全
     (c5 の T 曲線は存在しない・除去は遮断曲線を作らない)。
     **2,140,633 一意候補・safe かつ maximal はちょうど 1 件**:
     R={(19,2),(25,4)} → A={(27,2),(29,4)} (34 石・rows [5,5,5,4,5,5,5] のまま
     単一欠損)。m=29→30 の (≤2,≤2) 近傍では 0 件 (1,781,021 候補・3 系統合意)
     だったのと対照的で、≤2 編集近傍における witness の疎分布の例。
  3. T=(30,3) センサス: c4=2 (直線 y=3・空セル 26 と円
     {(22,2),(23,3),(25,4),(28,4)}・空セル 1)・c3=11。遮断曲線は (27,2),(29,4) を
     含む c3 円 (3 seed 石 + 両追加石 = 5 石) 経由。
- **3 系統検証 PASS**: verify_witness.py (Python Fraction)・verify_witness_det.js
  (純整数 4×4 行列式・maxLine 5 / maxCircle 5 / uncovered 0)・probe_free_column.py
  (第三 Fraction 実装・7×31 unblocked 0)。**負対照 PASS**: 石 (29,4) 除去の摂動配置を
  py (not-maximal)・det (uncovered 22) 両系統が検出。
- **M_{7,6} ∈ [31,862] → [32, 862]**・witness 帯 m=6..31・**前線 7×32**
  (m=31 witness の空列延伸は cell (31,3) 未遮断で失敗・one-stone-short)。
  solver-free で SAT 前線の先を構成した 2 例目 ((6,4) m=46 空列追加に次ぐ)。
- 幾何ルーチンの転写 bug 3 件 (すべて自己テスト・対照実験で検出・修正):
  (1) probe 初版の外心 uy 公式の a² 項 ((cx−bx) のべき所で (cy−by)) —
  m=30 極大性と矛盾する偽の未遮断 15 セルを報告。(2) det4 マイナー項 (m=30
  レーンで検出済み)。(3) 直線キーの gcd 正規化漏れ (同一幾何直線の重複・
  census 表示のみ影響で候補数 2,140,633 は修正前後で同一・完全性に無影響)。
  さらに surgery 初版は除去石セルの再遮断と移動 re-add の扱いが非統一だった →
  曲線を「盤上全セル」表現で |C∩S'| = |st_on−R| + |A∩full| に統一。
  **幾何ルーチンには正規化と回帰自己テスト必須**の再確認。
- class {3} (7,31,6) SAT (sat3.js class-split・kissat 4.0.4・cap 1800s・~135k 変数)
  はバックグラウンド並走中。witness は class {3} に属するため SAT で確定するはず。
  INDET なら cap 到達の honest negative として記録 (不在主張ではない)。
  sat3.js decode は >65k 変数で spread overflow のため、SAT 時は独立 Python
  パーサでモデル復号 (m=30 と同じ運用)。surgery 結果の正当性は SAT 結果に依存しない。
- 反映 (main へ直接): 886f5c49 (実験 9 ファイル・README 結果セクション完成版)・
  aa44e925 (mwq_stabilization.csv (7,6) 行全体置換)・315a9d82 (K0827 5 箇所編集 +
  追記 + refresh-knowledge-generated.yml trigger)。
- 次候補: (a) 7×32 への 2 編集 surgery (m=31 witness を種に T=(31,3)・BX=32 への
  移植)・(b) class {3} (7,32,6) SAT・(c) kissat 終了後の raw log + records push。
- 並走状況: 同時刻の main は n11 class2-lane (cost-79a/80d/80d/82c) と素数
  センサス checkpoint (498c03d5)。ファイルは衝突なし。

- 第2セッション（7×32 two-edit surgery 完全負記録）: surgery_m32.py
  （surgery_m31.py の 7×32 移植・seed は m=31 witness・T=(31,3)）で
  **2,224,675 一意候補**を完全列挙し **0 safe-maximal**。T センサス c4=1
  （直線 y=3）・c3=10（m=31 を遮断した c4 円は (31,3) を通らない）。
  同一コードの m=30 seed レプリカ（control_m30seed_replica.py）が m=31 記録を
  完全再現（2,140,633・unique witness・end-to-end 陽性対照）。
  局所負記録・M_{7,6} ∈ [32,862] 不変・前線 7×32。
  反映: seven-row-q6-m32-surgery-negative-20261115（README・2 scripts・4 outputs）・
  K0827 追記 + refresh trigger。
- 次候補（更新）: (a) class {3} (7,31,6) SAT の終了確認と (7,32,6) c3 への
  継続・(b) 3 編集 surgery・(c) 別 seed（クラス {3} 以外の欠損行配置）。

- 第3セッション (class {3} (7,31,6) SAT 実行・INDET・環境リセット): 最初の実行は
  ~1131s process-time / 5.79M conflicts でサンドボックスリセットにより中断。
  raw CDN から scripts・kissat 公式バイナリ (md5 3a5eba83…) を再取得し再実行
  (CNF 再生成 md5 48eb715f… 同一・環境リセット横断の決定性確認)。
  **結果: INDET (cap 1800s wall・rc=124 SIGTERM・4,368,709 conflicts / process-time
  896.03s)**。m=30 c3 (2,670,296 conflicts/497s SAT) の 1.64 倍深でも未解決・
  witness (surgery) は class {3} に属するため instance は SAT 確定 — cap 到達の
  honest negative (不在主張ではない)。CPU を (7,32,6) c3 と共有したため
  process-time は wall の半分。**SAT より surgery が m=31 を先に解いた**。
- 反映: m31-frontier README 結果セクション・output/records.jsonl (c3_7x31 INDET)・
  output/c3_7x31.raw.txt・scripts/parse_model.py (SAT 時のモデル復号用・m=30/m=29
  公開 witness で較正済み)。
- 継続中: class {3} (7,32,6) SAT (cap 3600s・md5 bc10c516…) と (7,5) m=38 class {0}
  SAT (cap 3600s・md5 b050817d…) がバックグラウンド実行中。
