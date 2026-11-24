# 2026-11-24 pre-diag 双生児 z7/z8 全称確定 (K1294) — 実行 log

## 時系列履歴

1. **着手・repo 状態確認**: 実行開始時 (2026-11-24T15:31Z 頃) の観測 HEAD
   `739e8428` (K1293 YAML fix)。Knowledge (高速レーン第 34 後継) の
   レジュームどおり最初に採番チェック: 最新 K item = K1293 であり
   (design-kyouen-witt レーンが K1291/K1292 を moment-polynomial
   certificate・K1293 を Witt/affine Steiner 3-design として取得済み・
   いずれも本領域と直交)、**K1294 が空き**であることを確認。
   取得領域: K1290 §5 O9′ (T-PDT7/T-BDT7・T-PDT8/T-BDT8)。
2. **宣言前探索 (single-owner 確保前)**: explore_k1294.py (X1–X4:
   z7/z8 band・beds の (R,δ) 表・mixed cell 0・R 例外層厚み 8 の特定
   (R=0..7 が 2·[R odd])・R=8 seam 行 (z7 all 1 / z8 all 0)・核 cell 発現。
   X5/X6: L-BU7G/L-BU8G 発現 w≤30 bad 0。X7: sharpened C-PSF′ probe
   z=0..10 bad 0。**X8: typed 子 self-check (申立テーブル + closed form
   のみから子構成した mex vs 申立 vs engine) 3,878+228 点 bad 0** —
   手証明 §2 構文を宣言前に機械検証) + explore2_k1294.py (Y1/Y2: 主張
   wide census 8,928×2・360×2 bad 0。Y3–Y5: z9/z10 OBS (band 4,500×2・
   beds 120×2・far-row 216×2・low-R hist {0:346,2:340}×2) bad 0。
   Y6: ordered engine 交差 z=7..10。Y7: L-BU7G/L-BU8G w≤40 + L-BU9G/
   L-BU10G 発現 (token plane 10/11) bad 0。Y8: T-TWIN・dedup z=0..12
   (C-PSF′ 観測を plane 12 まで拡張))。
3. **宣言ノート出版**: 最新 main 再取得 (`a461445f` @ 15:35:17Z・
   design-kyouen-witt レーンの証跡追記・非接触) → K1294 空き・対抗宣言
   なしを確認 → 単一オーナーとして宣言ノートを push (**commit
   `8dce7a3d` @ 15:45:09Z・fetch-back sha256 `968998ae…` 30,928B byte
   一致**)。主張は §1 (T-PDT7/T-BDT7/T-PDT8/T-BDT8・L-BU7G/L-BU8G・
   C1 K1290 O9′ z7/z8 部分解決・C2 sharpened C-PSF′ w=7,8・C3 L-BUzG
   9 枝)、§2 typed 証明全文 (z7 band/bed の場合表・z8 band/bed・層域
   横断 R=7 cell の導出・L-BU 補題の閉形式導出・well-founded 性)、
   §4 機体宣言 (counts 80,059 bad 0・4 走 byte-identical・変異電池 5/5
   fail-closed を事前宣言)、§5 open 登録 (O9″/O10″/O11/O12/O13)、
   §6 主張の区別。
4. **キット出版**: verify_k1294.py (sha256 `b3974b63…`・engine pin
   `bd5f22e4…` startup ゲート・--tamper-engine/--tamper=z7s/z7b/z8s/z8b)・
   engine_block.py (`582c93c1…`, K1282–K1290 kit と byte-identical)・
   explore 2 本 (+.out)・predry/ 4 走 (sha `c424a680…` byte-identical) を
   push (commit `9421cbc2`)。**fetch-back 15/15 byte 一致**。
5. **公式 4 走 (fetch-back bytes から)**: rc=0 全、stdout sha
   `c424a680…` byte-identical (fetchback cwd×2 PYTHONHASHSEED random/1 +
   isoA/isoB 独立 tree env -i PYTHONHASHSEED 99/7・各 ~10 秒)。counts
   [8928,360,8928,360,1939,114,1939,114,39671,1516,16190]
   **総計 80,059 bad 0**: D1/D3 z7/z8 band census (m≤14 g≤25 k≥−30)、
   D2/D4 bed census、D5–D8 typed slice/bed (申立テーブルからの子 mex ×
   claim×engine 二重照合)、D9 anchors (L-BU7G/L-BU8G w≤30、K1290 z5/z6、
   K1289 z3/z4、K1288 z1/z2、K1286 z0、sharpened C-PSF′ identity sweep
   w=0..8 (9 面 21,105 点)、T-TWIN identity、閉形式×両 engine z∈2..9、
   B-exit w=1 edges)、D10 cross-engine、D11 OBS (z9/z10 band・L-BU9G/
   L-BU10G discovery sweep z=10,11・dedup sweep z=0..12)。
6. **変異電池**: 5/5 fail-closed。--tamper-engine rc=2 (mutated sha
   `0ea47a80…` ≠ pin・K1282–K1290 と同一変異)、z7s 8,928 bad / z7b
   360 bad / z8s 8,928 bad / z8b 360 bad 各 rc=1。宣言通りの挙動。
7. **成果物出版**: audit_run1-4.out+.info・tamper 5 種×2・detcheck.json
   (OFFICIAL-PASS)・MANIFEST-sha256 (34 entries) を push (commit
   `6be78993`)。**fetch-back 20/20 sha256 一致**・tamper_engine.info
   remote size 0 照合・MANIFEST 34 entries 全件 remote 実在確認。
8. **採番衝突の発見と解決 (統合時)**: 出版直前の main items ツリー
   再取得で、moment-polynomial レーンが宣言ノート (15:45:09Z) の
   **21 秒前に 2702e06a (15:44:48Z)** で
   `K1293-second-moment-multiplier-s-arc-bounds.md` と
   `K1294-moment-relaxation-exact-lp-optimum.md` を出版していたことが
   判明 (Witt レーンの `K1293-design-kyouen-witt.md` (7a1e183c 15:25:20Z)
   との二重採番も含む)。本レーンの push 直前 vacancy 確認 (手順 3) は
   refetch 時点でこれを捉えられなかった (採番レース)。
   その後の経過を追跡したところ、moment レーン自身が衝突を解消していた:
   **4a2ad69e (15:53:12Z)** で自 2 item を K1295/K1296 に再採番し、
   さらに **c6edfe14 (15:55:36Z)** で「他レーンが 1294/1295 を in-flight
   中に出版した」として K1296/K1297 に移動し、**K1294 を本レーンの
   package に明け渡し**。統合時点で main 上の items に K1294/K1295 は
   実在しないこと (直接 path probe・items ツリー commit history で確認)、
   したがって AGENTS.md の統合時再採番規則 (main 衝突時に限る) は不発動
   であることを確認。本 package は宣言ノート・kit・audit 成果物と
   端末間で整合する **K1294 のまま**出版する (採番経緯は K item の
   aliases NUMBERING RESOLVED に記録・K1296 への relation 追加)。
9. **K item・README bullet 出版**: K item
   (`research/knowledge/items/K1294-prediag-twins-z7-z8.md`) +
   research log (本ファイル) + knowledge README bullet append
   を 1 commit で出版。

## 受入判定

- 4 走 byte-identical・開示データ総計 80,059 bad 0・変異電池 5/5
  fail-closed → OFFICIAL-PASS。手証明 (宣言ノート §2) <-> 機体照合の
  一致で T-PDT7/T-BDT7/T-PDT8/T-BDT8/L-BU7G/L-BU8G を全称定理として受入。
- K1290 O9′ の **z7/z8 部分解決**・sharpened C-PSF′ 全称 w=0..8・
  L-BUzG 族 9 枝・層域横断 2 型 (横断型 R=7 / 横断ゼロ型) の確定。
- ただし census は定理の照合であり全称性の主張ではない (§主張の区分)。
- verdict 不消費・11×11 空 (2 石 root {49,60}/{59,60}・sc {59,60}・
  S2 {59,60}) UNKNOWN 維持。

## 次課題

- T-PDT9/T-BDT9・T-PDT10/T-BDT10 (O9″): z9/z10 typed 全称。層厚 10。
  C 子は本項の z7/z8 定理を全 R 参照可能なため同構文で証明可能な見通し。
  横断列は z9 で 2 列 (C 子 budget 8,9 が z8 主則域)・z10 は横断ゼロ。
- sharpened C-PSF′ の w 帰納 (O9″): 横断型/横断ゼロ型の w 偶奇交互
  (奇数世代横断 1 列・偶数世代横断ゼロ) として定式化する見取り
  (宣言ノート §2.6・§5 O11)。
- L-BUzG 族の一般 w 全称形 (O10″): L-BU9G/L-BU10G の w≤40 OBS が入力。
- SLB2/SLB3・L/Am frontier (K1287 O1 残部, O13) は次単一オーナー候補。
