# 2026-11-15 (8,10) 難所帯 class-split 突破・CSV (8,9) 下界修正（高速レーン）

## 目的

M_{8,10} の完全決着に向けて律速要因の難所帯 m=26..42 を攻略する。def-mode
OR 符号化が抵抗する幅を K0818/K0819 型 class-split（row-mirror 正準欠損行
クラス分割）で分解して閉じる。実験 dir: `eight-row-q10-band-closure-20261115/`。

## 実施内容

1. **難所帯 def-mode 直接掃引（43..59 全幅 UNSAT）**: 43-45 は 250s cap・
   4.21M-5.00M conflicts・46-50 は 104-147s・51-59 は 55-82s・60 は 54s。
   m=46-50 は環境 reset 後の再実行で conflicts bit-exact 再現（決定性確認）。
   honest negatives: m=27/28 (270s・3.45M/3.61M)・29 (250s・6.01M)・
   31 (240s・5.87M)・41 (250s・6.44M)・42 (250s・6.31M)。いずれも INDET で
   non-absence ではない。m=29 では --counter=totalizer も試したが sat2.js は
   per-curve sequential counter 固定で CNF 不変（records note 参照）。
2. **class-split 突破 — m=40, 41, 42 完全決着（UNSAT）**: 並走の予言通り
   「def-mode INDET の幅はクラス分割で落ちる」が w=8 でも成立。
   - 符号化: sat3.js（`six-row-q8-m19-class-split-20261114/scripts/`・
     md5 d03f908e）再利用 + classfast.js（genfast3 の chord census を
     S.buildCensus に patch する wrapper・byte-identity を 8x28 class{3}・
     8x30 class{1,5} で確認済み）。135 = 8行の非空部分集合を鏡像 r↦7-r で
     割った正準クラス数（(2^8+2^4)/2 − 1 = 135・空集合は欠損行なしで不適）。
   - **各幅 135/135 クラス UNSAT・0 INDET・0 SAT** → def-mode UNSAT 確定。
     難クラスは {3} と {3,4}（行3 が鏡像不動点に近い中心行）: m=41 {3}
     1,798,460 / m=42 {3} 1,787,366・{3,4} 1,700,318 / m=40 {3} 2,222,035・
     {3,4} 1,760,053 conflicts。クラス単位では最大 100s cap で完結し、
     def-mode OR（6.31-6.44M conflicts）より2-3桁易しい。難クラスの
     conflicts は m 減少で増加傾向（{3}: 1.80M@41 → 2.22M@40）→
     m≈30-35 では 3-5M、cap 100-240s で対応可能な見込み。m=26..28 は
     最難関候補（sat3.js の --krow/--minpos 分解を併用する想定）。
   - 解決行は records.jsonl に統合済み（74e8997e）。m=41 の per-class 詳細は
     `output/q10-band/class-splits/classes-8x41q10.jsonl`。m=42/40 の
     per-class 詳細（classes-8x42/40q10.jsonl・計~3MB）は環境障害中に
     ローカル喪失のリスクがあり、resolutions-pending-merge に要約を push。
     classsweep.sh は決定的（resume-safe）なので再生成可能。
3. **CSV (8,9) 下界修正 27→29（重要な事実修正・3ba20de2）**: 並走レーンの
   CSV 統合は (8,9) を 27..984 としたが、`eight-row-bands-20261114` の w8q9
   records.jsonl には **m=27/28 の rowY=3 witness**（63石 rows
   [8,8,8,7,8,8,8,8]・154,022 / 3,049,989 conflicts・js+py 二重検証済み）が
   あり、正しくは **M_{8,9} ∈ [29, 984]**（frontier 8x29）。行を修正し、
   (8,10) 行も witness-free 40..138 連続（class-split 解決含む）に更新。

## 現在の状態

- **witness-free 連続: 40..138**（40-42: class-split・43-60: 本レーン 250s cap・
  61-138: 並走レーン・53..60 はクロス bit-exact 検証済み）+ 501..513 +
  サンプル 150/200/300/500/700/939（m=939 116,323 conflicts で上限側は閉鎖）。 
- 残る未解決: **26..39**（26: 4符号化 INDET・27-31: プローブ INDET・
  30, 32..39: 未掃引）。並走が 139..500 / 514..938 を継続中。
- M_{8,10} ∈ [26, 940] のまま。全幅閉包なら **M_{8,10} = 26 exact**。

## 障害

- 2026-11-14T23:05Z 以降ローカル bash 環境が "temporarily unavailable"
  （filesystem rollback failure）で継続中。m=32..39 の classsweep.sh 掃引は
  bash 復帰後に実施する予定（README IN FLIGHT に明記済み）。本ラウンドは
  GitHub API のみで統合・修正・文書化を実施。

## 次の一手

1. bash 復帰時: m=39→32 を classsweep.sh で掃引（`./classsweep.sh 8 M 10 100 280`・
   決着ごとに records.jsonl へ resolution 行追加 + 即時 push）。
2. INDET クラスは --krow/--minpos 分解（K0821 型）。m=26..28 は最難関候補。
3. 26..39 全解決 + 並走の 139..500/514..938 完了後: M_{8,10}=26 exact として
   K item（最新 main で番号衝突確認・K0833 まで既存確認済み）+ CSV
   exact-threshold 行化 + 本 log への追記。

## 追記（第3ラウンド・2026-11-15 API-only・census 完全分類）

bash 環境が引き続き利用不能のため、run_typescript 内の独立 TS 実装で
(8,10) 禁止曲線 census を完全再実装し、以下を確定して push した:

1. **独立検証**: m=10..60 全幅の census を genfast3 と独立に再計算し、
   比較可能な全25幅（26,27,28,29,31,41..60）で records と bit-exact 一致。
2. **線形則 curves(m) = 9m−105（m ≥ 23）を m ∈ [23,60] の38幅で機械検証**。
   （実装中に early-exit の残り行数オフバイワンで 10-11 点円を取りこぼすバグが
   あったのを発見・修正 — 修正前は十二点ファミリー系 2m−14 個のみが数えられて
   いた。修正後が正しい。）
3. **10ファミリー完全分類**（(2x−u)²+(2y−2b)²=R・u 奇数・R ∈ {50,130,170,650}・
   各族の u 区間は m の線形関数・個数式 3(m−7)+2(m−11)+2(m−13)+2max(0,m−23)+2）。
   → `output/q10-band/census-structure/` に README・families-m43.json・sweep-m10-60.json。
4. **(8,11)/(8,12) への系**: ≥11点円は十二点ファミリーのみ（m ∈ [8,60] 完全列挙+単調性）。
   sampled m≤100 主張の m ≤ 60 部分を完全列挙に強化し、CSV 両行に付記。全 m での
   一般化閉包は数学的課題として明記（P(8)=12 (K0765) は ≥13点円を全 m で除去済み）。
   8x26 での行2,5 被覆計数トリム（⌈(m−8)/2⌉ 個）は行2,5 の円数 3m−25 ≫ なので
   **何も刈らない** — 135クラスすべてが本物であることの構造的説明として記録（honest negative）。

K item 昇格（census 分類の知識化）は tools/knowledge/build.py・check.py がローカル環境
必須のため bash 復帰後に実施する。census README の L2 は (8,9) レーン（frontier 8x29・
修正後の下界29）設計時の注意も兼ねる（弦対 census は q=9 では不完全）。

## 追記（第4ラウンド・2026-11-15 API-only・(8,9) census 完全分類）

前ラウンドの q=10 census 独立実装を q=9（≥9点円・9点円は複点行+第3点ループで
完全捕捉）に拡張。m=9..27 は genfast.js all-triples w8q9 records と全19幅
bit-exact、m=28..40 を追加掃引して以下を確定・push した
（census-structure/q9-census.md・q9-sweep-m9-40.json）:

1. **curves9(m) = 9m−97（m ≥ 23）を m ∈ [23,40] の18幅で機械検証**
   （分解: 8 水平線 + 9m−113（10族） + 8（9点端部メンバー））。
   m=22 は 99・m ≤ 21 は q=10 と同一（9点円 0 個）。
2. **9点円の完全分類**: F8/F9 幾何（R=650）の盤面端切断メンバーのみ
   （b=25/2 rows{0,1,3,4,7}・b=−11/2 rows{0,3,4,6,7}・
   u ∈ {19,21,2m−23,2m−21}・m=22 では {19,2m−21}）。m ≥ 23 で常に 8 個・
   点数構造は 4複点行+1単点行。
3. **L2-prime**: 「1複点行+7単点行=9点」型は m ∈ [9,40] で不存在 →
   chord-pair census は q=9 でも m ≤ 40 で完全（9点円 8 個の追加で q=9 符号化
   が構成できる。m > 40 は型閉合リスクを明記して使う）。CSV (8,9) 行に
   census 情報を付記。これで (8,9) レーン（frontier 8x29・M ∈ [29,984]）の
   符号化設計の基盤が完成。

K item 昇格（q9/q10 census 分類の知識化）は引き続き bash 復帰後に実施。

## 追記（第5ラウンド・2026-11-15 API-only・w=8 strip 分類で census 全称閉包）

K0830（7行版）の探索機械を w=8 に移植し、(8,9)/(8,10) census を帯全域で全称化
して push した（eight-row-strip-classification-20261115/）:

1. **新補題 L0（v₀ 整数性）**: d ≥ 5 → v₀ ∈ ℤ。鳩の巣で8行中5行に連続複点行対が
   あり v₀ ∈ ¼ℤ（v₀ = g/4）。g 奇数なら (8y−g)² mod16 の偶奇分離で複点行が
   同一偶奇に制限され d ≤ 4。g ≡ 2 (mod 4) なら弦差 ≡ 2Δ (mod 4) が完全平方差の
   mod4 値と矛盾して d ≤ 4。よって d ≥ 5 → g ≡ 0 (mod 4)。整数 Z 列挙は d ≥ 5 を
   逃さない。一般 w では連続対の存在は d > ⌈w/2⌉ で保証。
2. **弦上界 L2 + k2 ≥ 3（L1）**: k2 行弦 ≤ m−1、K0765 接点補題で接点なし・
   mod9 で d ≤ 6 → 2k2+k1 ≥ 9 ∧ k2+k1 ≤ 6 → k2 ≥ 3（「1複点行+7単点行」型の
   不可能性の根拠）。遠方ケース B ≤ ((m−1)²−16)/16 → 任意窓行弦
   c*² ≤ 4.5(m−1)²+308 → m ≤ 984 で c* ≤ 2085 < UMAX=2100。
3. **完備列挙**: 半レンジ Z ∈ [−1102502,−2]（鏡映 v₀ → 14−v₀ で半減）+
   対称対 A′ + 鏡映閉包。SPF sieve 1,102,503・Case A 1,101,450 ペア +
   A′ 2,100・4チャンク分割実行（チャンク1–3 該当なし・チャンク4 で13構成）。
   **13構成 = census の9窓構成（F1–F9 と完全一致・UMAX=23 再現検証で行
   プロファイル一致）+ K0830 例外円 R=2353705250 の8行窓版**（v₀ ∈ {48515,48517}
   + 鏡像・5二重行・弦 {5,623,763,985,1079}・弦平方直接算術検証済み）。
   例外は盤内9点に m ≥ 986（10点に m ≥ 1080 = K0830 の7行結果と一致）を要し
   m ≤ 984 に出現しない → **Theorem A: 盤内 ≥9点円は m ≤ 984 で F1–F9 の
   配置メンバーに限る**。
4. **族配置解析**（**帯全域 m ∈ [9,984] 全976幅の数値完備検証・0失敗**。16幅
   サンプル + m=41..43 直接計算 + m=9..40 は q9/q10 census 完全列挙と bit-exact。
   左端部は m ≥ 44 で m 非依存・内部は全行収容 9m−113・右端部は鏡像）→
   **curves9(m) = 9m−97 が m ∈ [23,984] 全幅、curves10(m) = 9m−105 が
   m ∈ [23,940] 全幅で全称成立**（exactly9 = F8/F9@{19,21,2m−23,2m−21} のみ・
   全幅で集合として厳密検証・m ≥ 23 で8個・m=22 で4個・m ≤ 21 で0個）。
   ≥11点円は F1 のみ（全 m ≤ 984・m−7 個）→ (8,11)/(8,12) の行2,5 強制満杯が
   帯全域で全称化。実装バグ2件（u 偶数列挙・盤内点数式のミス）は修正済み。
5. **K0765 clarification**: サイズ定理 {7,8,10,12} は窓（帯）ベースの解釈が正しい。
   盤内点数として読むと m ≥ 22 で F8/F9 端部9点円が反例。K item 文言修正は
   bash 復帰後に提案。
6. **11×11 長期レーンへの接続**: L0・弦上界の枠組みは一般 w に移植可能
   （d > ⌈w/2⌉ で連続対の存在を保証）。
7. **CSV 破損の修復（重要・インフラ）**: 並走の push により mwq_stabilization.csv
   に行内改行が混入していた（(8,10) 行は2箇所断裂 "lowe|r: defi|cient"・
   (8,12) 行は kind 語途中 "bound|s"・separation-band 4箇所 "separat|ion"・
   (6,5)/(6,8)/(7,6)/(7,8)/(8,11) 各行の途中断裂など。row が kind プレフィックス
   で始まらない断片列として機械検出）。kind 語プレフィックス断片は次行と、
   それ以外の断片は前行と再結合する機械的修復を適用。検証: 116行・全行 kind
   プレフィックス・全行クォート偶数・33777bea（破損前のクリーン版）との差分が
   正当更新3行（(4,4)/(5,4)/(6,4)・band-extension 系の並走成果・(5,4) M 列
   37→40・(6,4) 32→41 を含む）のみであることを確認。**併せて重要: 前回の修復
   検証時には差分5行（(7,4) width59-two-swap・(7,5) witness-surgery の要約
   更新を含む）だったが、現 main では (7,4)/(7,5) 行が 33777bea 版へ戻っており
   これらの要約更新が消失している（並走の stale fetch 上書きと推定）。
   seven-row レーンでの CSV 要約復元を次回実行に依頼する。** 並走の push
   パイプラインに行折り返し系バグが疑われるため、次回実行でも CSV 完全性
   （行数116・クォート偶数・kind プレフィックス）を最初に確認すること。

census-structure README・q9-census.md のスコープを「予測」から「全称成立」に格上げ、
CSV 4行（(8,9)/(8,10)/(8,11)/(8,12)）に strip 分類の情報を反映。K item 昇格
（Theorem A + census 全称昇格）は bash 復帰後（tools/knowledge/build.py・
check.py 必須・K番号は最新 main で衝突確認）。

## 追記（第5ラウンド補足・(7,4)/(7,5) CSV 要約の復元）

第5ラウンド item 7 で記録した消失（(7,4) width59-two-swap・(7,5)
witness-surgery の CSV 要約）について、成果ファイル自体は main に残っていたため
（research/experiments/seven-row-q4-width59-two-swap-20261115/・
seven-row-q5-witness-surgery-20261115/・各 README が完全な検証記録を保持）、
両 README から CSV 要約を復元して反映した:

- **(7,4)**: M ∈ [60, 1929]（下界 57→60。幅53証人への 2-for-2 two-swap 完全列挙で
  7×57 の witness 2個・うち1個が空列延伸で 7×59 まで有効。width-60 の近傍列挙は
  0 = not absence）。
- **(7,5)**: M ∈ [35, 1142]（下界 34→35。m=33 witness への witness surgery
  （depth-1/depth-2 石移動）で 7×34 の 27石 witness 2個（winA/winB）。純TS完全検証
  済み・js+py 交叉検証は bash 復帰後 pending と CSV にも明記）。

seven-row レーンの次回実行はこの復元を確認されたし（重複反映防止）。K0827 および
固定幅 README への反映状況は seven-row レーン側で確認すること。
