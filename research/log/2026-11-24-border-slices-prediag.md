# K1286 実行 log — 境界スライスと対角下バンドの全称確定（T-PD0・T-B0・T-Z1/T-B1・T-Z2/T-B2・系 C1–C5）

- 日付: 2026-11-24（Vibe 高速レーン・定時自律実行）
- 対応宣言ノート: `research/log/2026-11-24-border-slices-prediag-single-owner-note.md`
  （出版 f6db3f33・観測 HEAD 5b9c6231・K1286 空き・対抗宣言なし）
- 対応機体: `research/experiments/border-slices-20261124/`
  （出版 ccf48d10・公式成果物 a92dcc12）
- K item: `research/knowledge/items/K1286-border-slices-prediag-collapse.md`

## 内容（成果サマリ）

1. **T-PD0（主定理・z0 対角下バンド一次元崩壊則）**: ペア (m, m+g)・
   δ := R − 2m に対し H(R; (m, m+g); 0) = f0(R−2m)
   （∀m>=1, g>=1, 0 ≤ R ≤ 2m+g）。f0(δ) = 2 (δ=1); [δ odd]
   (δ≤0); [δ even] (δ≥2)。**値は m・g を経由せず δ のみに依存**し、
   対角下バンド全域（k ∈ [−2m−g, 0]・R=0 まで）が δ の一次元関数
   に崩壊。帰納は 2 選択肢 mex{ f0(δ+1), f0(δ−1) } の 8 行ケース
   表で閉じる（下側 fall/B 子 → f0(δ+1)、上側 compress/corner 子
   → f0(δ−1)、m=1 の B 子は L-BU0 で同一値）。
2. **T-B0**: z0 床 b0(j) = f0(j)（j ≤ 0・m 非依存）。
3. **T-Z1/T-B1**（z1 境界）: 境界スライス k∈{−1,0,1} の Z1 表
   （k=0: g=1→2, g≥2→[g odd]・k=±1: g=1,2 前置 + [g even] tail）と
   床 j∈{−1,0,1}（b1(0)=1・b1(−1)=0 (m≥2) / 2 (m=1)・b1(1)=0 は
   公刊前線の再掲・照合用）。
4. **T-Z2/T-B2**（z2 境界）: 境界スライス k∈{0,1,2} の Z2 表
   （k=0,2: g=1→1, g=2→0, g=3→2, g≥4→[g even]・k=1: [g odd]
   clean）と床 j∈{0,1,2} → 0, 2, 0。
5. **系 C1–C5**: K1285 OBS-D9 境界三角形 4 脚（z0-k0 = f0(g)・
   z1-k1 = Z1(1,g)・z2-k2 = Z2(2,g)・z2-k1 = [g odd] clean）の
   **全称昇格 = K1285 未来課題 F1 の完了**。F1 が想定した
   「z1-k0 → z0-k(−1)」カスケードは T-PD0 の δ 座標で一挙に解消。
   z1-k0/k(−1)・z2-k0 は従来観測なしの新規確定領域（C5）。
   **ペア z0/z1/z2 面で未確定は遠方内面 k ≥ 4/2/3 のみ**。
6. **構造的発見（型付き子 mex + B-uniformity）**: fall / B / compress
   / corner / C の全子が予算 R−1 に落ち、面間参照（z2→z1→z0）も
   下位予算のみ。**L-BU0/1/2**: m=1 の B 手子 v(g+1, z+1, R−1) が
   K0832 閉形式の直接計算として fall 子の表（f0 / Z1(k,·) / Z2(k,·)）
   を正確に再生する。よって主張面上で m の場合分けが不要になり、
   全主張が R に関する単一の強帰納で同時確立（§2.5 well-founded）。
   D2/D3/D4/D5/D6 typed 電池は、申立テーブル**のみ**から子の値を
   構成して mex を取り、主張値とエンジン値の双方と照合する
   （証明の mex 算術の有限機械照合・証明の代替ではない）。
7. open 登録（有限観測のみ・§5）: **O1** z1 pre-diag (k≤−2) は
   δ-1D でない（z1-k(−2) の m=1,g=1 核〔値 2〕と m≥2 行の
   2 段構え・z1 床 j≤−2 の m 分裂 → **F1′**）。**O2** z2-k(−1)
   m 非依存候補 (0,1,0,2,[g odd] g≥5) と z2-k(−2) の g=5 突起 →
   **K1287 目標 z2 pre-diag 崩壊**（C 子が O1 に依存）。
   **O3** F2 spread web（F_d/G_d・d∈{1,2,3}）の c≥2 列は
   m 非依存（288 点・D10 登録・spread 理論への入力）。
   **O4** z1 床 j≤−2・z2 床 j≤−1 の m 分裂構造（E3・主張せず・
   typed Beds 拡張候補）。
8. **宣言前探索（E1–E6・explore_border.py/out）**:
   E1 境界スライス census（有効 cell のみ・R<0 除外）で z0 は
   k∈[−8..0] 全 m 一致・z1/z2 は主張 k 行のみ一致を確認。
   E2 δ 崩壊候補の直接検証（z0 帯 m≤12・g≤21・k∈[−26..0] の有効
   5,585 cell 全一致）。E3 床 census（z×j・m≤14）。E4 Z1/Z2 法則表
   882+882 cell ミスマッチ 0。E5 F2 web census 288 点。E6 核生成
   census（z1-k(−2)・z2-k(−1)/(−2)・m≤10）。広域ローカル照合:
   z0 帯 17,220 点 f0 bad=0・typed proofcheck 6,514 + 追加 662 bad=0。

## 出版・監査の記録（publish-then-execute）

1. 最新 main 確認: HEAD 着手時観測 405da370 → push 直前再取得
   5b9c6231（いずれも Part DF/DG/DL/DJ solver 第三実装・
   bookkeeping レーン・非接触）。K1286 空きを items dir のコミット
   履歴で直接確認（最新 K item = K1285 = 6703e506・K1286 取得
   コミットなし）。対抗宣言なし。
2. **commit f6db3f33**: 宣言ノート先行出版（宣言ノート = 証明全文
   §1–§5 + honest 記録・機体 sha 13ec8f7b…・公式 4 走の期待
   stdout sha256 ac7d104d…・counts 期待値を宣言時に確定）。
3. **commit ccf48d10**: 機体キット出版 13 ファイル
   （README・verify_k1286.py〔sha256 13ec8f7b…・engine pin
   bd5f22e4… ゲート内蔵〕・engine_block.py〔582c93c1…・K1282/
   K1283/K1284/K1285 kit と同一 bytes〕・explore_border.py/.out
   〔E1–E6〕・output/dryrun1-4 + .info〔宣言前 dryrun・4 走
   byte-identical sha ac7d104d… 確認済み〕）。
   **fetch-back**: 13 ファイル全 sha256 byte 照合
   （verify 13ec8f7b…・engine_block 582c93c1…・explore_border.py
   4aac4ebb…・explore_border.out 10e2c5c4…・dryrun1-4.out 全
   ac7d104d…・dryrun .info・README d32e6668…・完全一致）。
4. **公式実行（fetch-back 検証機体バイトから）**:
   - 4 走すべて rc=0・stdout byte-identical・sha256
     `ac7d104d8a70b69c37ae354d98048fcc07c69ca836cb482166c22ba1864967e9`
     （同一 cwd PYTHONHASHSEED=random/1 ×2 + 隔離 tree
     env -i PYTHONHASHSEED=99/7 ×2・/usr/local/bin/python3 3.12・
     ~0.7-0.8s/走）。宣言ノート §4 の宣言値と完全一致。
   - counts `[6719, 3470, 882, 42, 882, 42, 152, 2910, 2353, 666]`・
     総計 18,118 点・bad 0・engine_gate PASS・D1 f0 class hist
     {0: 3251, 1: 3174, 2: 294}・D8 公刊アンカー 2,910 点再照合・
     D9 交差エンジン（canonical vs ordered）一致 + K1285 OBS
     パターン関数同一性 800 点 drift なし。
   - 変異電池 6/6 期待どおり fail-closed・rc-exact:
     --tamper-engine → rc=2（mutated sha 0ea47a80… ≠ pin・
     mismatch 出力）。--tamper=f0 → D1 bad=6719 + D7 bad=152
     （全点 bad・rc=1）。--tamper=z1 → D3 bad=882。--tamper=z2 →
     D5 bad=882。--tamper=bed1 → D4 bad=42。--tamper=bed2 →
     D6 bad=42（すべて rc=1・宣言値と一致）。
5. **commit a92dcc12**: 公式成果物出版 22 ファイル
   （output/audit_run1-4.out+.info・output/tamper_{engine,f0,z1,z2,
   bed1,bed2}.out+.info 12 ファイル・detcheck.json〔verdict
   OFFICIAL-PASS〕・MANIFEST-sha256 34 entries）。
6. **publish (D)**: 本 run log・K item（items/K1286-border-slices-
   prediag-collapse.md）・knowledge README 末尾 bullet
   （fresh fetch 1,023,527B ベースに純 append・push 後
   fetch-back 照合）。

## 受入判定

OFFICIAL-PASS。宣言した全期待値（stdout sha ac7d104d…・counts
18,118 点・変異電池 6 種の挙動と rc）が fetch-back で byte 照合した
機体バイトからの公式実行で再現され、証明は宣言ノート §2 に全文収録・
typed 6,514 + 18,118 点の機械照合が bad 0。K1285 未来課題 F1
（境界三角形の全称化）が完了し、z0 対角下バンドの δ 一次元崩壊という
新構造補題を得た。ペア低 z 面の未確定領域は遠方内面のみに縮小。

## 規約・11×11 への接続

- verdict 不消費・11×11 空盤の UNKNOWN は不変・Part DF/DG/DL/DJ
  レーン（solver 第三実装・bookkeeping・b28/b31 系）と完全非接触。
- T-PD0 によりペア z0 帯全域（k ≤ 0）が δ の O(1) 即値評価可能と
  なり、K1285 の枝刈り格子が境界側に拡張された。巨大レーンへの
  採用判断は巨大レーンオーナーに委ねる（接続の記録のみ）。

## 次課題

1. **F1′（K1287 前段）**: z1 床 j ≤ −2 の m 分裂構造（E3 の行:
   j=−2 は m=1→0, m≥2→1 等）の全称化。z1 pre-diag の typed 証明の
   前提。
2. **z2 pre-diag 崩壊（K1287 本命）**: O2 の z2-k(−1) m 非依存候補
   表 (0,1,0,2,[g odd] g≥5) と z2-k(−2) の g=5 突起・m=1/g=1 分裂の
   typed 証明。C 子が z1-k(−2) を要求するため F1′ に依存。
3. **spread 理論（K1285 F2）**: O3 の F_d/G_d c≥2 列 m 非依存データ
   （288 点・D10 登録済み）を入力に c 方向帰納。F(1,c≥2)=0・
   G(1,c≥3)=2・G(d,c≥2) の全称化。
4. **typed Beds 拡張（O4）**: z1/z2 床の負 j 側の全称化
   （z2 床 j=−1: m=1→2 / m≥2→1 等）。

## honest 記録

- 宣言・キット・成果物の各 push に fast-forward 競合なし
  （毎回 push 直前に HEAD・K1286 空き・対抗宣言を再取得確認し、
  非接触を確認してから push）。
- 本実行は compaction を跨いだ継続実行である: 宣言ノート・キット・
  dryrun は宣言前に作成・dryrun 4 走 byte-identical を確認済みの
  状態で、push（A: 宣言ノート f6db3f33・B: キット ccf48d10）から
  fetch-back 照合・公式 4 走・変異電池・成果物出版（a92dcc12）・
  K item/run log/README bullet までを本セッションで実行。
- 宣言ノート本文の転送は base64/JSON リテラル経由を試みたが
  エスケープ破損が発生したため、file_system.read_file による直接
  byte 転送に切替えて push した（fetch-back sha256 照合で本文
  完全一致を確認・宣言値への影響なし）。
- dryrun1-4 は宣言前のローカル 4 走で byte-identical（sha
  ac7d104d…）を確認済みで、公式 4 走と同一の stdout。
- 公式 4 走・変異電池は fetch-back sha256 全文照合済みの機体
  バイトから実行（隔離 tree 2 走含む）。explore_border の E1–E6
  出力は seed 非依存で決定的。
