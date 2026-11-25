# 実行 log: K1313 下帯頂行崩壊 (T-BB) — 高速レーン 2026-11-25

前回 (K1313 セッション前半): compaction 後の引き継ぎで、K1311 OBS-BBL watershed の
説明候補として発見された下帯頂行 k=z+n−3 の単一座標 (E,z) 崩壊が、宣言前探索
explore_k1313.py (X1..X10・全波 bad 0・凍結) と型付き子 6 区域 mex の手証明骨格
まで進んでいた。本 log は機体実装から出版までの後半の記録。

## チェーン (publish-then-execute)

1. **機体実装** `verify_k1313.py`: K1312 と同一構造 (engine 埋込み・startup sha
   ゲート pin bd5f22e4…・12 電池・変異 13 種)。
   - 初回ローカル実行は D12 ランダム掃引 (山上限 20, n≤7) の状態空間爆発で
     OOM kill (rc=137)。宣言前に山上限を n 比例 ({2:14,…,7:6}) に減量。
   - 減量後 1 走 3.3 s・12 電池 28,024 点 bad 0・OBS-BBL 凍結表 7 行の正確な
     再現 (naive 不一致 (80,80,68),(80,56,47),…,(80,0,0) + 同ドメイン PB bad 0)。
   - predry 4 走 (cwd random/1 + 隔離 tree env -i 99/7): 全 rc0・stdout
     byte-identical sha256 a634658cd7baa418b2474e4793700aca2b8d7b8e2b652d7be312a31b89c4b78e。
   - 変異 13 種の bad 配列を実測 (ty [1440,2646,2970,…], h2 [98,…], in [286,…],
     wl [0,0,0,1768,…], tt 4509, lm 4200, ps 3742, ce 542, ob 1, db 1766,
     zz 1968, rs 700, engine rc2 mutated sha 0ea47a80…)。
2. **採番確認**: `K1313 repo:yuubinnkyoku/kyouen-researches` commit 検索 total 0
   (push 直前にも再確認)。着手時 HEAD 6247d6a5、宣言直前 HEAD 8440276e
   (Part EA 11×11 レーンの直交 commit 群のみ)。
3. **宣言ノート出版**: 単一オーナー宣言ノート
   `research/log/2026-11-25-belowband-toprow-single-owner-note.md`
   (§1 主張 T-BB/L-BR1/typed 子・§2 手証明全文・§3 凍結探索・§4 機体宣言・
   §4.5 主張の区別・§5 open 登録・§6 honest 経緯)。
   - **インシデント**: 最初の宣言 commit 0c8f5873 で宣言本文の埋め込みに失敗し、
     プレースホルダ 8 バイトのみが出版された。kit 13 ファイルの fetch-back
     byte 照合 (宣言 + kit 同時実施) で即時検出。本文全文を verbatim 再出版
     (881d8b42)、さらに §6 に当該インシデントと D12 docstring の既知不整合
     (減量前の「heaps<=20」記載が docstring に残存・コードは宣言どおり) を
     honest 記録として追記して最終化 (66916e87)。以後の push は件数・バイト長の
     事前機械検査を徹底。
4. **kit 出版** `research/experiments/belowband-toprow-20261125/` (13 ファイル:
   README.md・verify_k1313.py・engine_block.py・explore_k1313.py/.out・predry 4 走
   (+.info)) commit ab9e4f05。fetch-back 13/13 byte 一致。
5. **公式 4 走** (kit bytes から): 同一 cwd×2 (PYTHONHASHSEED random/1) +
   隔離 tree env -i×2 (99/7)。全 rc0・stdout byte-identical・宣言 predry sha
   と同一 (a634658c…)。約 3.2–3.4 秒/走。
6. **変異電池公式 13 種**: 全モード宣言どおりの bad 配列・rc (engine rc2・
   他 12 種 rc1)。D9 の 'ob' 破損テストは凍結 z=3 行 1 件の不一致を正確に検出。
7. **detcheck.json**: 宣言 counts/bad・engine pin・4 走 sha・変異 13 種 bad 配列
   をすべて検査後に書き出し。verdict **OFFICIAL-PASS** (assertion_errors [])。
8. **成果物出版**: output/official_run1-4.out+.info・tamper レコード 13・
   detcheck.json・MANIFEST-sha256 (22 行・自己除外) commit afeccb95。
   fetch-back 23/23 byte 一致。

## 成果の要約

- **T-BB (定理)**: 全 n≥2・全 z≥0・全多重集合 X の下帯頂行 k=z+n−3 で
  u := E+z+n−4 として H = [E odd]/2/1−[E odd]。単一座標 (E,z) 崩壊。
  n≥3 で E は下に非有界 → 2 の線・flip 領域は無限半直線。
- **手証明**: L-BR1 (公刊閉形式のスライス) + 型付き子 (A-a/A-b/B/C、全子が R−1)
  + 6 区域 mex (U1/U2/H/I1/I2) + 単一 R 強帰納で完結。
- **意味**: tail (K1312) + 境界 (K1311) + 頂行 (本次) で全多重集合 n≥2 の
  k≥z+n−3 が完全確定。O-BBL 頂行層を解決、残余 open は k≤z+n−4 (O-BBL2)。
- **系**: n=2 で K1310 印刷定数 (bed 定数・g*≤0 極) を再現、壁行 (z=0,k=−1) を
  新規に閉じた。OBS-BBL watershed は完全説明。

## 主張の区分

- 定理: T-BB・L-BR1 (手証明が正本・宣言ノート §2)。
- census 28,024 点 (D1–D4, D8, D10–D12) は機械的一貫性検査で証明の代替ではない。
- D5 typed 4,509 点は帰納段 mex の機械再現。D7 公刊アンカーは転写検査。
- 11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。

## 次課題

1. k=z+n−4 行 (n=3: k=z−1) の (E,z) 崩壊有無の X2 型 census (O-BBL2 入口)。
2. O-DB2 ボトムアップ工具の実装 (plane z+1 の (n−1) 面頂行値から)。
3. K0832 conjecture C (n=3, k=z が今回閉じた) の主張値照合。
