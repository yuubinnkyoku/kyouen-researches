# 2026-11-22 y=16 全称証明 part2（C1d・C11r・フル14チェック・K1237 observed→proved 昇格）

高速レーン（vertical-fiber 系）・[part1 log](2026-11-22-y16-universal-verifier-part1.md)
のレジュームどおり、同一単一オーナー宣言 `432664f7`
（part1 12チェック+part2 昇格を保持範囲と宣言済み・対抗宣言事前確認済み）の
継続工程として実行。別宣言・対抗宣言の追加は不要（宣言ノートの part2 条項が
そのまま適用）。y=15 part2（`c34a19ff` 配下・2026-11-22 同日着地）と同一手続き。

## 選定（着手前の確認）

- part1 が「昇格判定は part2 に留保」を明記済みで、着手条件（part1 着地）を
  満たしていた。y=10/y=12/y=13/y=14/y=15 の part2 前例と同一手続き。
- 最新 main の K1237 item・K1239 item・実験dir は part1 出版時点のまま、
  11×11 系（AX/AY/AV 系）レーンは非接触であることを commit 取得で確認。

## 工程（実行順）

1. **preflight_c1d_y16.py**（SHA-256 `6a3094c1…`・12,817 bytes）: 出版固定 z 切片
   アンカー（z=8: K0999/K1000・z=9: K1001・z=10: K1011・z=15/16/17:
   K1065/K1077/K1087）を出版 verify_y15_universal.py part2 正本
   （`a39e7ab1…`・commit 0bf18752）から verbatim 抽出し、y=16 行を
   4方照合（アンカー×H_ordered×H_canonical×cand16）z0∈{8,9,10,15,16,17}・
   x=16..45・R<=x+z0+30 → **13,140 点 bad 0**（z別 2,055/2,085/2,115/2,265/
   2,295/2,325）＋低R単一トークン縮約 R<=z+6（z0∈{15,16,17}・x=16..159）
   **9,504 点 bad 0**。about 3秒・2回実行（同一cwd+隔離側）byte-identical・
   `output/preflight-c1d-y16.json`（SHA-256 `efb24340…`・744 bytes）。
   provenance ヘッダは y=16 実測値（cand16・13,140/9,504）で count-assert 付き書換。
2. **census_rows.py**（y=16 版・XMIN=16・XMAX=70・RBUF=18・token (x,16)・
   tail (x+16)%2・SHA-256 `76e89fe9…`・3,808 bytes）: z=0..79・x=16..70・
   R=0..x+z+18 の **4,400 行 446,600 点**（値0点 223,295・misses 8,193,227・
   LRU 明示キャップ 1.6M・約20秒）の行ごとの Thue-Morse 指数・T/P 集合・tail を
   出力 → `census.txt`（817,944 bytes・4,400行+空行80・SHA-256 `f0b1a960…`）。
   tail アサート R>=x+z+17 全行成立。3回実行 byte-identical
   （同一cwd 2回＋隔離側再生成）。
3. **検証器 in-place 拡張**: part1 出版 byte（37,042 bytes・SHA-256 `79e21b2d…`）に
   C1d/C11r を追加（51,691 bytes・SHA-256 `bdf4fe04…`）。anchor block（A8u..A17u）
   は y=15 part2 正本検証器から verbatim 抽出・provenance ヘッダのみ y=16 実測値
   （13,140/9,504/cand16）で count-assert 付き書換。check_C1d/check_C11r は y=15
   版から count-assert 付き置換（C1d 掃引 x=16..159・R<=x+61〔6 z0 で 128,304 点〕
   +lowR 9,504・C11r は census.txt 全行の cand16 から再導出照合・rows==80*56・
   重複/欠落/終端改行なし FAIL-CLOSED）。12の part1 チェックコードは byte 不変。
   part2 組立 script は出版しない（y=13/y=14/y=15 前例）。py_compile PASS・
   C11ordered/C11canonical を part2 機で再実行し census parts は part1 出版 byte
   （`fd94dda3…`/`3934307f…`）と byte 一致。
4. **フル14チェック**（`python3 verify_y16_universal.py C1 C1b C1d C2 C2b C3 C4
   C4t C7 C8 C9 C11 C11r C12`）: **overall PASS・総照合点 6,916,256・
   全14チェック bad 0・型 394,686**（C1d 137,808・C11r 446,600・merge 1,243,466/
   tail 193,300 不変 bad 0・C4t clip33 違反 1,638 (60,96,96) 不変）。
   35.5 秒（run1）/36.0 秒（run2）。audit.json（SHA-256 `9748ff5c…`・3,618 bytes）
   run1/run2+隔離run3 の 3実行 byte-identical。
5. **隔離 run3**: 隔離 tree+別cwd+別HOME+env -i（PATH 固定）+PYTHONHASHSEED=random。
   preflight・census_rows.py・両 census part を隔離側でゼロから再生成
   （すべて正本 byte と一致）→ フル14チェック → audit.json byte-identical
   （36.0 秒）。
6. **fail-closed 6 種**（スクラッチ tree で実施・全捕捉）:
   (1) census part（census-ordered.json）points 改ざん 442,200→442,201 →
   FAIL-CLOSED。
   (2) census-canonical.json 欠落 → FAIL-CLOSED。
   (3) corollary merge 境界改ざん x<=z-17→z-16（改ざんコピー・C2のみ）→
   overall FAIL（fake C2・merge 16,218点 bad 200・rc=1）。
   (4) census.txt P 集合 1桁改ざん（z=0 x=16 行・最初の値 1→2）→
   C11r bad=1・rc=1（PASS 出力なし）。
   (5) census.txt 欠落 → FAIL-CLOSED。
   (6) census.txt 重複行注入（z=0 x=16 行の複製）→ FAIL-CLOSED。
   (3) は改ざんコピーでの probe で main tree 無接触・(1)(2)(4)(5)(6) は
   復元後に baseline cmp 全ファイル byte 一致（main-tree の audit.json は
   一切の probe に触れていない）。

## 昇格判定

- **K1237（y=16 族閉形式 cand16・全 z>=0・x>=16・R>=0）を observed→proved
  に昇格**（AGENTS.md「同じ命題は同じ K 項目・新規採番なし」・
  K1141/K1152/K1231/K1233/K1235 前例と同一手続き・同一宣言 432664f7 の
  保持範囲内）。
- 系: マージ命題 y=16 版（x<=z-17 → single_token(x+16,z,R)）と tail 値
  (x+16) mod 2 が全称系として確定（**マージ命題は y=1..16 で全称確定**）。
  y=16 は fit probe box 内マージ 0 行の初族で、part1 の merge corollary
  1,243,466 点が初の全域生エンジン錨止めだった点も part2 で boxed 逆演算
  から確認される回帰ゼロと整合。
- 横断則の確定: clip 窓 2y+2 tight が **12 族連続確定**（y=5..16）・
  B子逐語転写構成が **7 連**（cand9..cand15 の B子連鎖で全称証明済み族は
  cand10/cand12..cand15 の 5 リンク）・tail 開始族式 x+z+y+1 が 16 族連続・
  基底点 y 点仮説が 16 例目。
- 2トークン残余ゲームの全称は **y=1..16 で揃った**（y>=17・3トークン以上・
  固定幅・q点版は範囲外のまま）。

## 出版系列（各 push 直前に最新 main 再取得・fetch-back byte検証）

- commit A2: 実験dir part2 8ファイル（verify_y16_universal.py part2 版・
  census_rows.py・scripts/preflight_c1d_y16.py・output/audit.json part2 版・
  output/census.txt・output/preflight-c1d-y16.json・output/published_run.txt
  part2 追記・README part2 節）。
- commit B2: K1237 item を同番号で observed→proved 昇格（status・relations
   〔K1239/generalizes K0999-K1087 追加〕・artifacts 再構成・本文に part2 根拠
  ・昇格判定節）+ K1239 item に part2 artifacts・本文 part2 節追記 + 本 log。
- commit C2: knowledge README 末尾 bullet（K1235 昇格 bullet の構造踏襲・
  blob sha1 ガード付き）。
- knowledge.yml CI step は y=11..y=15 と同様不登録（CI は y=10/K1141 まで）・
  出版 byte を監査正本とする。

## 解釈規約

- 有限照合は有限観察の機械的証拠で、trust 境界（選択肢分解の健全性・mex
  恒等式・有限型空間の完全性）は y=5..16 系列と同一の機械分類に依存。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。本項は残余ゲーム族の数学的構造の機械検証であり
  標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=17 族・固定幅・q点版安定化長は範囲外。

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

- y=16 全称完結済み。次の最有力候補:
  (a) **横断法則の一般補題化レーン**（y=1..16 全称が揃い、merge 命題・
  tail 族式・clip 窓 2y+2・基底点 y・pin 格子族式の帰納一般化の証明価値が
  最高・y=16 の「box内マージ0行」初例は一般化の境界事例として重要）。
  (b) y=17 族 fit（奇数 y・band_base/band_int 分離の帰納検査・seed 法則
  5 連続目テスト）。いずれも新規単一オーナー宣言が必要。
