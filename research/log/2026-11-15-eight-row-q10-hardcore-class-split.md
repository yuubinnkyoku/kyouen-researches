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
