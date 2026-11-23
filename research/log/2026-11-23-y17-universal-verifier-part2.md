# 2026-11-23 y=17 全称証明 part2（C1d・C11r・フル14チェック・K1240 observed→proved 昇格）

高速レーン（vertical-fiber 系）・[part1 log](2026-11-23-y17-universal-verifier-part1.md)
のレジュームどおり、同一単一オーナー宣言 `b099a974`
（part1 12チェック+part2 昇格を保持範囲と宣言済み・対抗宣言事前確認済み）の
継続工程として実行。別宣言・対抗宣言の追加は不要（宣言ノートの part2 条項が
そのまま適用）。幾何訂正 amendment `03ca97ad`（C2b 掃引行の掃引範囲
x∈{17,22,…,67} 訂正）は本 part2 の着手前に出版済みで、part2 の全工程は
訂正後の正本にのみ触れた。y=13..y=16 part2 と同一手続き。

## 選定（着手前の確認）

- part1 が「昇格判定は part2 に留保」を明記済みで、着手条件（part1 着地・
  3コミット `33e0a062`/`02a95e01`/`83234a16` 出版・fetch-back byte 検証済み）
  を満たしていた。y=13/y=14/y=15/y=16 の part2 前例と同一手続き。
- 最新 main の K1240 item・K1241 item・実験dir は part1 出版時点のまま、
  11×11 系（AX/AY/AV 系）レーンは非接触であることを commit 取得で確認。

## 工程（実行順）

1. **preflight_c1d_y17.py**（SHA-256 `fc1d4ec0…`）: 出版固定 z 切片アンカー
   （z=8: K0999/K1000・z=9: K1001・z=10: K1011・z=15/16/17: K1065/K1077/K1087）
   を出版 verify_y16_universal.py part2 正本（`bdf4fe04…`・commit `b706b214`）
   から verbatim 抽出し、y=17 行を 4方照合（アンカー×H_ordered×H_canonical×
   cand17）z0∈{8,9,10,15,16,17}・x=17..45・R<=x+z0+30 →
   **12,789 点 bad 0**（z別 2,001/2,030/2,059/2,204/2,233/2,262）＋低R単一
   トークン縮約（z0∈{15,16,17}・x=17..159・R<=z+6）**9,438 点 bad 0**。
   約2.8秒・組み込み前 fail-closed ゲート・`output/preflight-c1d-y17.json`
   （SHA-256 `c8e0e0a9…`）。provenance ヘッダは y=17 実測値
   （cand17・12,789/9,438）で count-assert 付き書換。
2. **census_rows.py**（y=17 版・XMIN=17・XMAX=70・RBUF=19・ZHI=80・token
   (x,17)・tail (x+17)%2・SHA-256 `1188bcd1…`）: z=0..79・x=17..70・
   R=0..x+z+19 の **4,320 行 444,960 点**（zero_points 221,578・
   misses 8,725,227・LRU 明示キャップ 1.6M・約17.5秒）の行ごとの
   Thue-Morse 指数・T/P 集合・tail を出力 → `census.txt`
   （817,882 bytes・4,320行+空行80・SHA-256 `597370b4…`）。
   tail アサート R>=x+z+18 全行成立。
3. **検証器 in-place 拡張**: part1 出版 byte（37,970 bytes・SHA-256
   `2110ecbb…`・commit `33e0a062`）に C1d/C11r を追加（51,925 bytes・
   SHA-256 `4253cf29…`）。anchor block は y=16 part2 正本検証器から
   verbatim（provenance ヘッダのみ y=17 実測値 12,789/9,438/cand17 で
   count-assert 付き書換）。check_C1d は y=16 版から掃引範囲を
   count-assert 付き置換（x=17..159・R<=x+61 で 6 z0 合計 127,842 点+
   preflight low-R 9,438 点）、check_C11r は census.txt 全行の cand17 から
   再導出照合（rows==80*54==4,320 機・values range(0,x+z+20)・tail
   (x+17)%2・重複/欠落/終端改行なし FAIL-CLOSED）。12の part1 チェック
   コードは byte 不変（diff 検証済み: 追加は anchor block・check_C1d・
   check_C11r・STAGE docstring・main registry のみ）。part2 組立 script は
   出版しない（y=13..y=16 前例）。py_compile PASS・C11ordered/C11canonical
   を part2 機で再実行し census parts は part1 出版 byte
   （`12234496…`/`1ca205a5…`）と byte 一致。
4. **フル14チェック**（`python3 verify_y17_universal.py C1 C1b C1d C2 C2b C3
   C4 C4t C7 C8 C9 C11 C11r C12`）: **overall PASS・総照合点 6,926,065・
   全14チェック bad 0・型 457,645**（C1d 137,280=掃引127,842+9,438・
   C11r 444,960・merge 1,182,632/tail 193,096 不変 bad 0・C4t clip35 違反
   1,300 (60,98,98) 不変）。35.4 秒。
   audit.json（SHA-256 `fd4b7d8c…`）run1/run2+隔離run3 の 3実行
   byte-identical。
5. **隔離 run3**: 隔離 tree+別cwd+別HOME+env -i（PATH 固定）+
   PYTHONHASHSEED=random。転写検査・preflight・census_rows.py・両 census
   part を隔離側でゼロから再生成（すべて正本 byte と一致）→ フル14チェック →
   audit.json byte-identical。
6. **fail-closed 6 種**（スクラッチ tree `/tmp/y17-fc` で実施・全捕捉・
   baseline 復元確認済み）:
   (1) census part（census-ordered.json）points 改ざん → FAIL-CLOSED。
   (2) census-canonical.json 欠落 → FAIL-CLOSED。
   (3) corollary merge 境界改ざん z-18→z-17（改ざんコピー）→ overall FAIL
   （merge bad 176・rc=1）。
   (4) census.txt P 集合改ざん → C11r bad=1・rc=1（PASS 出力なし）。
   (5) census.txt 欠落 → FAIL-CLOSED。
   (6) census.txt 重複行注入 → FAIL-CLOSED。

## 昇格判定

- **K1240（y=17 族閉形式 cand17・全 z>=0・x>=17・R>=0）を observed→proved
  に昇格**（AGENTS.md「同じ命題は同じ K 項目・新規採番なし」・
  K1141/K1152/K1231/K1233/K1235/K1237 前例と同一手続き・同一宣言 b099a974
  の保持範囲内・幾何訂正 03ca97ad 配下）。
- 系: マージ命題 y=17 版（x<=z-18 → single_token(x+17,z,R)）と tail 値
  (x+17) mod 2 が全称系として確定（**マージ命題は y=1..17 で全称確定**）。
- 横断則の確定: clip 窓 2y+2 tight が **13 族連続確定**（y=5..17・y=17 は
  36・最初違反歩み 5 点 (60,90,90)→…→(60,98,98)）・B子逐語転写構成が
  **8 連**（cand9..cand16 の連鎖で証明済み B子は cand10/cand12..cand16）・
  tail 開始族式 x+z+y+1 が 17 族連続・基底点 y 点仮説が 17 例目・
  box 内マージ 0 行が 3 族連続（y=15/16/17）。
- 2トークン残余ゲームの全称は **y=1..17 で揃った**（y>=18・3トークン以上・
  固定幅・q点版は範囲外のまま）。

## 出版系列（各 push 直前に最新 main 再取得・fetch-back byte検証）

- commit D: 実験dir part2 更新 8ファイル 1コミット（verify_y17_universal.py
  part2 版・census_rows.py・scripts/preflight_c1d_y17.py・output/audit.json
  part2 版・output/census.txt・output/preflight-c1d-y17.json・
  output/published_run.txt part2 版・README part2 節）。
  census-ordered/canonical.json と transcriptions-check は不変。
- commit E: K1240 item を同番号で observed→proved 昇格（status・title・
  aliases・relations〔K1241 depends_on・generalizes K0999/K1001/K1011/K1065/
  K1077/K1087 追加〕・artifacts 再構成・scope/evidence に全称段階記録・
  本文に「全称段階の記録」節）+ K1241 item に part2 実績値・artifacts・
  本文 part2 節追記 + 本 log。
- commit F: knowledge README 末尾 bullet（K1237 昇格 bullet の構造踏襲・
  blob sha1 ガード付き・現 HEAD 待受後に読み取り）。
- knowledge.yml CI step は y=11..y=16 と同様不登録（CI は y=10/K1141 まで）・
  出版 byte を監査正本とする。

## 並走宣言の扱い（誠実記録）

本 part2 の出版直前（2026-11-23T01:26:44Z）に、別実行が
`research/log/2026-11-23-y17-universal-verifier-part2-execution-declaration.md`
（commit `1fec2b1c`・amendment `2a885eca`）を main に出版した。同宣言は
part1 を別系統（builder 主義・37,606 B・SHA-256 `76a73b6e…`・総 6,312,890 点
bad 0）で独立複製して出版機体（本レーンの 6,343,825 点）と交叉検証した上で、
同一の part2 パイプライン（C1d・C11r・K1240 昇格・同一 log path）を
「先行宣言の予約事項を変更なく実行する」として宣言したものである。
本出版は先行単一オーナー宣言 `b099a974`（2026-11-23T01:05Z・保持範囲
part1+part2・本研究セッションが出版し、part1 を同宣言配下で出版済み）の
part2 継続条項を**宣言者自身の実行**として完走したものであり、
y=16（宣言 `432664f7` の part2 を別宣言なしで継続）と同一手続きである。
よって同並走宣言の予約実行系は本出版をもって完結・閉包され、重複出版は
行わない。並走実行の part1 独立複製（点数差 +30,935 は掃引広がりに完全分解・
census part 2 ファイルは両機体で byte-identical・C4t 1,300 違反 first
(60,98,98) 一致）は part1 の第二独立機体による交叉検証として価値があり、
発生順 log 上ここに明記する。双方の実行が本命と同じ結論（14チェック PASS・
K1240 昇格）に達した場合、それ自体が独立検証になる。

## 次回レジューム

- **y=18 fit は別の単一オーナー宣言が必須**（本宣言 b099a974 の保持範囲は
  y=17 の part1+part2 昇格まで。偶数 y 系列の次族 cand18 は seed 法則
  6 連続候補）。横断法則の一般補題化レーン（clip窓 2y+2 tight の全称化・
  tail 開始 x+z+y+1・基底点 y 点・box 内マージ 0 行の条件刻画）は
  y=1..17 の 17 族分の正本が揃った今が着手適期。
