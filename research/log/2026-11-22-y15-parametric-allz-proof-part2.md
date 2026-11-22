# 2026-11-22 y=15 全称証明 part2（C1d・C11r・フル14チェック・K1235 observed→proved 昇格）

高速レーン（vertical-fiber 系）・[part1 log](2026-11-22-y15-universal-verifier-part1.md)
のレジュームどおり、同一単一オーナー宣言 `c34a19ff`（part1 12チェック+part2 昇格を
保持範囲と宣言済み）の継続工程として実行。別宣言・対抗宣言の追加は不要
（宣言ノートの part2 条項がそのまま適用）。

## 選定（着手前の確認）

- 最新 main の K1235 item・K1236 item・実験dir は part1 出版時点のまま
  （実験dir に触れた commit は 45f3ccfd のみ・K1235 は 6cd72dd1 のみ・
  K1236/part1 log は e8559457 のみ）。並走 AX/AY レーン（11×11 系）は
  非接触。
- part1 が「昇格判定は part2 に留保」を明記済みで、着手条件（part1 着地）
  を満たしていた。y=10/y=12/y=13/y=14 の part2 前例と同一手続き。

## 工程（実行順）

1. **preflight_c1d_y15.py**（SHA-256 `fdc4ca86…`）: 出版固定 z 切片アンカー
   （z=8: K0999/K1000・z=9: K1001・z=10: K1011・z=15/16/17: K1065/K1077/K1087）
   4方照合（アンカー×H_ordered×H_canonical×cand15）z0∈{8,9,10,15,16,17}・
   x=15..45・R<=x+z0+30 → **13,485 点 bad 0**（z別 2,108/2,139/2,170/
   2,325/2,356/2,387）＋低R単一トークン縮約 R<=z+6（z0=15/16/17・x=15..159）
   **9,570 点 bad 0**。約3秒・2回実行（同一cwd+隔離側）byte-identical・
   `output/preflight-c1d-y15.json`（SHA-256 `cd67d3fe…`）。y=10 でこの段階が
   K1087 転写初稿の評価順バグ 170 点を捕捉した実績に対し、本族はアンカーが
   y=14 part2 正本からの verbatim 再転写で 4方照合初回から全一致。
2. **census_rows.py**（y=15 版・XMIN=15・XMAX=70・RBUF=17・token (x,15)・
   tail (x+15)%2・SHA-256 `28e84955…`）: z=0..79・x=15..70・R=0..x+z+16 の
   4,480 行（448,000 点・値0点 223,127・misses 7,666,827・hits 15,021,674・
   15.7-16.3 秒・maxrss 639,524KB・LRU 上限 1.6M 明示キャップ）の行ごとの
   Thue-Morse 指数・T/P 集合・tail を出力 → `census.txt`
   （824,466 bytes・4,480行+空行80・SHA-256 `1465a011…`）。tail アサート
   R>=x+z+16 全行成立。3回実行 byte-identical（主tree 2回＋隔離側再生成）。
3. **検証器 in-place 拡張**: part1 出版 byte（942行）に C1d/C11r を追加
   （1,313 行・SHA-256 `a39e7ab1…`）。anchor block（A8u..A17u）は y=14 part2
   正本検証器（`6ac219cf…`）から verbatim 抽出・provenance ヘッダのみ y=15
   実測値（cand15・13,485/9,570）で count-assert 付き書換。check_C1d/
   check_C11r は y=14 版から count-assert 付き置換（C1d 掃引 x=15..159・
   R<=x+61〔6 z0 で 128,760 点〕+lowR 9,570・C11r は census.txt 全行の
   cand15 から再導出照合・rows==80*56・重複/欠落/終端改行なし FAIL-CLOSED）。
   12の part1 チェックコードは byte 不変。part2 組立 script は出版しない
   （y=13/y=14 前例）。1箇所だけ意図的に "y=10/y=12/y=13/y=14 part2 C1d"
   の前例引用が残存。py_compile PASS・C11ordered/C11canonical を part2 機で
   再実行し census parts は part1 出版 byte（`50819ab3…`/`64b006a3…`）を再生成。
4. **フル14チェック**（`python3 verify_y15_universal.py C1 C1b C1d C2 C2b C3
   C4 C4t C7 C8 C9 C11 C11r C12`）: **overall PASS・総照合点 6,935,639・
   全14チェック bad 0・型 335,658**（C1d 138,330・C11r 448,000・merge
   1,304,870/tail 195,917 不変 bad 0・C4t clip31 違反 2,030 (60,94,94) 不変）。
   34.8 秒（run1・maxrss 473,520KB）/34.3 秒（run2）。audit.json
   （SHA-256 `401be383…`）run1/run2+隔離run3 の 3実行 byte-identical。
5. **隔離 run3**: 隔離 tree+別cwd+別HOME+env -i（PATH 固定）+
   PYTHONHASHSEED=random。preflight・census_rows.py・両 census part を
   隔離側でゼロから再生成（すべて正本 byte と一致）→ フル14チェック
   → audit.json byte-identical（計時再実行 34 秒）。
6. **fail-closed 5 種**（スクラッチ tree で実施・全捕捉）:
   (1) census part points 改ざん 443,520→443,521 → FAIL-CLOSED。
   (2) census-canonical.json 欠落 → FAIL-CLOSED。
   (3) corollary merge 境界改ざん x<=z-16→z-15（改ざんコピー・C2のみ）→
   overall FAIL（merge bad 223・y=15 で再測定）。
   (4) census.txt P集合 1桁改ざん（z=0 x=15 行・17→18）→ C11r bad=1・rc=1。
   (5) census.txt 欠落 → FAIL-CLOSED。各後復元・最終 baseline cmp 全文件
   byte 一致。

## 昇格判定

- **K1235（y=15 族閉形式 cand15・全 z>=0・x>=15・R>=0）を observed→proved
  に昇格**（AGENTS.md「同じ命題は同じ K 項目・新規採番なし」・
  K1141/K1152/K1231/K1233 前例と同一手続き・同一宣言 c34a19ff の保持範囲内）。
- 系: マージ命題 y=15 版（x<=z-16 → single_token(x+15,z,R)）と tail 値
  (x+15) mod 2 が全称系として確定（**マージ命題は y=1..15 で全称確定**）。
- 横断則の確定: clip 窓 2y+2 tight が **11 族連続確定**（y=5..15）・
  B子逐語転写構成が **6 連**（cand9..cand14・全称証明済み族を B 子に使うのは
  cand10/cand12/cand13/cand14 の 4 例）・tail 開始族式 x+z+y+1 が 15 族連続・
  基底点 y 点仮説が 15 例目。
- 2トークン残余ゲームの全称は **y=1..15 で揃った**（y>=16・3トークン以上・
  固定幅・q点版は範囲外のまま）。

## 出版系列（各 push 直前に最新 main 再取得・fetch-back byte検証）

- commit A: 実験dir part2 8ファイル（verify_y15_universal.py part2 版・
  census_rows.py・scripts/preflight_c1d_y15.py・output/audit.json part2 版・
  output/census.txt・output/preflight-c1d-y15.json・output/published_run.txt
  part2 追記・README part2 節）。
- commit B: K1235 item を同番号で observed→proved 昇格（status・relations・
  artifacts・本文に part2 根拠追記）+ K1236 item に part2 artifacts 追記 +
  本 log。
- commit C: knowledge README 末尾 bullet（K1233/K1234 昇格 bullet の構造踏襲）。
- knowledge.yml CI step は y=11..y=14 と同様不登録（CI は y=10/K1141 まで）・
  出版 byte を監査正本とする。

## 解釈規約

- 有限照合は有限観察の機械的証拠で、trust 境界（選択肢分解の健全性・mex
  恒等式・有限型空間の完全性）は y=5..15 系列と同一の機械分類に依存。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。本項は残余ゲーム族の数学的構造の機械検証であり
  標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=16 族・固定幅・q点版安定化長は範囲外。

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

- y=15 全称完結済み。次の最有力候補:
  (a) **横断法則の一般補題化レーン**（y=1..15 全称が揃い、merge 命題・
  tail 族式・clip 窓・基底点・pin 格子族式の帰納一般化の証明価値が最高）。
  (b) y=16 族 fit（偶数 y・「出版最終構造 seed 法則」の 4 連続目テスト・
  cand14→cand16 外挿）。いずれも新規単一オーナー宣言が必要。
