# y=14 two-token パラメトリック全称証明 — part2（C1d・census・K1233 observed→proved 昇格）

- 日時: 2026-11-22 (UTC)
- 実験dir: `research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/`
- 位置づけ: [part1 出版](2026-11-22-y14-universal-verifier-part1.md)（12チェック
  6,377,860 点・全 PASS・3回 byte-identical・commit 677ced40/94069d48/9050d4f6）が
  残した part2 工程の実行。単一オーナー宣言は
  [y=14 universal verifier single-owner note](2026-11-22-y14-universal-verifier-single-owner-note.md)
  が保持（宣言 2026-11-22T19:08:21Z・commit 24e418a9・part1 12チェック+part2昇格を
  保持範囲と明示・part1 着地済みで part2 着手条件は充足。着手前に最新 main を再取得し
  （HEAD 59644c09・直前は対抗レーンの |capT| 分解系列と n11 系）y=14 全称段階への
  他オーナー着手がないことを確認）。

## 実施内容

1. **C1d アンカーの事前検証（組み込み前・fail-closed）**:
   6つの published uniform closed form（z=8: K0999/K1000・z=9: K1001・z=10: K1011・
   z=15/16/17: K1065/K1077/K1087）のアンカー関数 A8u..A17u を y=13 part2 正本検証器
   （SHA-256 079b49ad…・監査 2f5f56c0…）から verbatim で抽出し（`Y` は関数
   ローカル変数のみで cand13/cand14 ブロックと干渉しない）、検証器組み込み前に y=14 行を
   生両エンジンで 4 方照合（各 z0・x=14..45・R<=x+z0+30・計 13,824 点・
   anchor/H_ordered/H_canonical/cand14 全一致・不一致 0・z 別
   2,160/2,192/2,224/2,384/2,416/2,448・約 2.4 秒・
   `scripts/preflight_c1d_y14.py`・`output/preflight-c1d-y14.json`・SHA-256 c7369b4c…）。
   低 R 単一トークン縮約 R<=z+6（z=15,16,17・x=14..159）9,636 点も不一致 0・2 回実行
   （同一cwd＋隔離側）byte-identical。y=10 の同段階が K1087 転写初稿の評価順バグ
   170 点を捕捉した実績に対し、本族は y=13 正本からの verbatim 再転写のため事前検証は
   初めから一致（bug 捕捉 0 も実験事実として記録）。z=15/16/17 の (y,d) 過渡セル・
   S<17/S==17 分岐は y=14 で到達不能（S=x+14>=28）。
2. **正本検証器 part2**: verify_y14_universal.py を part1 出版 byte から in-place に
   拡張し C1d と C11r を組み込み（part2 正本 SHA-256 6ac219cf…・51,537 bytes・1,317 行。
   anchor block の provenance ヘッダは y=14 行向けに事前検証実測値で書き換えのみ・
   置換は count-assert 付き。y13 part2 と同一手続きで part2 用組み立てスクリプトは
   出版しない〔part1 出版の scripts/build_verify_y14.py は part1 byte の正本として
   そのまま〕。part1 出版 byte 4ecdec11… は実験dir外に参考保持）。全チェック指定実行
   （C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12）:
   **総 6,965,866 照合点・全チェック不一致 0・overall PASS**
   （C1d 138,846 点〔アンカー掃引 129,210 点＋低 R 縮約 9,636 点・C11 は census
   box z=0..79・x=14..70・R<=x+z+15〕・C11r 449,160 点〔4,560 行〕・C4t clip 29
   再掃引の confluence 違反 2,480〔初違反 (60,92,92)〕は part1 と不変・型総数 281,912・
   merge corollary 1,370,848 点・tail corollary 212,713 点は part1 と不変のまま bad 0）。
   audit.json（3,674 bytes・SHA-256 b91e88a0…・stage 文言 part2）・実行 約 35 秒。
3. **3回実行の byte-identical 確認**: run1（同一cwd）→ run2（同一cwd再実行・
   約 34 秒）→ run3（隔離 tree/cwd/HOME + PYTHONHASHSEED=random・census_rows.py・
   preflight も隔離側で再生成・フル14チェック約 34 秒）の 3 実行で audit.json・
   census.txt・census-ordered.json・census-canonical.json・preflight-c1d-y14.json が
   全て byte-identical（census_rows.py は記録時にもう 1 回再実行し 4 回 byte-identical・
   maxrss 639,424KB をその実行で実測。C11ordered/C11canonical も part2 セッションで
   再実行し part1 出版 byte〔6bb64b3c…/f31a990e…〕を再生成）。
   出版前の fail-closed 検査として census part 3 種（point 改ざん 444,600→444,601・
   merge corollary 改ざん・ordered part 欠落）を part2 セッションの scratch tree で
   再実施し同一メッセージで捕捉、census.txt の P 集合 1 桁改ざん（C11r 行不一致・
   rc=1・PASS 出力なし）と欠落（FAIL-CLOSED 明示）を捕捉・復元で clean PASS・
   baseline と byte-identical（計 5 種）。
4. **census_rows.py y=14 版（第三実装）**: y=5..y=10/y=12/y=13 と同型の生 tuple 二重再帰で
   z=0..79・x=14..70・R=0..x+z+16 の 4,560 行（449,160 点・値0点 224,566・
   エンジン状態計算〔LRU misses〕7,146,027・約 14.2 秒・maxrss 約 625-640MB）を計算・
   行ごとの Thue-Morse 指数・T/P 集合・tail を抽出（tail アサート R>=x+z+15 の
   (x+14) mod 2 全行成立）。census.txt（824,003 bytes・4,560 行＋空行 80・
   SHA-256 baad513c…）は C11r で閉形式 cand14 から再導出して全 449,160 点を独立照合・
   不一致 0。本実行ホストの 1 GiB cgroup 制約のみ LRU 上限 1,600,000 を明示キャップ
   （docstring 記載・出版 y=5..y=10/y=12/y=13 版との差はこの 1 点のみ）。
5. **K1233 observed→proved 昇格**: AGENTS.md「同じ命題は同じ K 項目・新規採番なし」に
   従い item を同番号で proved 昇格（title・status・scope・evidence・relations・
   artifacts を更新・fit 段階の誠実記録と独立第二検証の記述は保持）。
   knowledge README に part2/昇格 bullet を追記（part1 の commit C と同じ末尾追記方式）。
   K1234 item には part2 artifacts（verify part2 正本・census_rows.py・census.txt・
   preflight・part2 log）を追記。**knowledge.yml CI step は登録しない**:
   現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）・y=13（K1231）実験機の
   step が存在せず（CI 登録は y=10/K1141 まで）、本実験も出版 byte を監査正本とする
   直近 3 族と同一の扱いとする。

## 昇格で確定した横断観察（y=1..14 全称表から・y=14 が 14 族目）

- 基底点 y 点仮説 {z+1,..,z+2y-1}: y=14 で 14 点が全 z 確定（第14例・y=1..14 連続）。
- tail 開始族式 x+z+y+1 と tail 値 (x+y) mod 2: y=14 版（x+z+15・(x+14) mod 2）が
  全称確定（fit レベルの 13 族連続に全称族が y=14 まで到達）。
- マージ命題 x<=z-y-1 → single_token(x+y,z,R): y=14 版（x<=z-15）が全称確定
  （監査上 1,370,848 点独立照合・マージ命題は y=1..14 で全称確定）。
- clip 窓族式 2y+2: y=5..14 の **10 族連続 tight**（y=14 は clip 29 で 2,480 違反・
  2y+2=30 が tight・part1 C4t）。
- 前倒し pin 格子公式 pin=z+(d+3y)/2: y=5..14 の **10 族統一**（d≡y mod 4（奇z）・
  d≡y+2 mod 4（偶z））。y=14 では奇z 7 行 {-10,-6,-2,2,6,10,14}／偶z 7 行
  {-12,-8,-4,0,4,8,12}（偶 y 族式 y/2=7 の両偶奇 7 行初例が全称確定・
  y=12 の d≡0 から d≡2 への mod 4 クラス回転が偶数 y 族で成立した初例も確定）。
- 「pin スロット=th-1」型（奇z pin 行で pin が off=2k=th-1 をちょうど占有）が
  y=11/y=12/y=13/y=14 の **4 族連続で全称確定**（K1152 が指名した横断型の問いに全称で
  回答）。偶z側は pin が base 行上端 2k-1 の +2 位置（2k+1）に載る slot 則が 4 族同一。
- base 行 rank 族式 k(d)=floor((d+3y+1)/4) が y=10/11/12/13/14 の全 base 行（z 偶奇・
  行型反転込み）で同一（5 族）。偶z I 帯行 k(d)=floor((d+3y-1)/4) が y=11/12/13/14 の
  4 族同一。奇 z 連続整数掃引 th=2k+[d≡y mod 4] が偶数 y 族 2 例目
  （y=12 に続き全称確定）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=14 で全称確定。
- 偶z 対角行 d=-y の値1全欠如: y=8..14 の **7 族連続で全称確定**。最終 pin 行
  d=y の I[2y+z+1) 型が 9 族連続（y=6/8/9/10/11/12/13/14・y=14 は全称確定）。
- B 子に先行出版族の閉形式を逐語転写する構成: cand9（y=10 の B 子）・cand10（y=11 の
  B 子・K1141 全称）・cand11（y=12 の B 子・K1143）・cand12（y=13 の B 子・K1152 全称）・
  cand13（y=14 の B 子・K1231 全称）で 5 連（全称証明済み族を B 子に使うのは
  cand10・cand12・cand13）。
- 初稿一発一致が y=11/13/14 の 3 例（y=12 は 240 点修正・y=10 は手順外）。偶数 y 族でも
  出版最終構造 seed の Y+2 外挿が一発一致するという工芸的観察が全称確定を経て
  証拠の裏付けを得た。

## 未解決（次工程候補）

- 横断法則（基底点・tail 開始・マージ・clip 窓・pin 格子・対角行規則・I 帯 th/shift）の
  y>=15 への一般証明レーン（y<=14 が全称確定したので補題化・一般証明を開く価値が
  さらに上がった。type タイプ空間の有限性と族式の帰納構造が本命）。
- y=15 族の fit・全称（着手時は新しい単一オーナー宣言が必須・y 奇族で pin 行数・th 型
  〔y=11/13 と対置〕の判定材料。y 奇族の偶z pin 行数 (y-1)/2 の増加則が y=15 で 8 行に
  伸びるかも判定材料）。
- y=11（K1143）の part2 は y=11 レーン保留中につき本レーンでは着手しない。
- 3トークン以上・y>=15 族・固定幅・q点版安定化長・11×11 は範囲外。

## trust 境界

全称性は選択肢分解の健全性・正確な mex 恒等式・有限型空間の完全性
（raw錨・恒等式グリッド・型 confluence・シェル/多様体/probe・出版切片転写アンカー・
独立 census。K1023→K1231 と同一構成・y=14 は K1234 part1/part2 の同型機）による。
Lean ではない。C1d アンカー切片の正しさは K0999/K1000/K1001/K1011/K1065/K1077/K1087
の主張（y=14 行はその特殊例）。標準 11×11 の空盤勝敗・二石 root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 には一切言及しない（すべて UNKNOWN のまま）。

## 出版物（本コミット列）

- part2-a: 実験dir（verify_y14_universal.py part2 正本・census_rows.py・
  scripts/preflight_c1d_y14.py・output/audit.json〔part2 版 14チェック〕・
  output/census.txt・output/preflight-c1d-y14.json・
  output/published_run.txt〔part2 実行記録追記〕・README.md〔part2 節追記〕）。
  1 コミット。
- part2-b: K1233 item observed→proved（同番号更新）＋K1234 item part2 artifacts 追記＋
  本 log。1 コミット。
- part2-c: knowledge README 末尾 bullet 追記（part1 series の commit C と同一手法・
  push 前に最新 HEAD を取り直し blob sha ロックで競合回避）。
- ※ knowledge.yml への CI step 追加は行わない（実施内容 5 の理由による・
  直近 3 族〔K1143/K1152/K1231〕と同一の扱い）。
