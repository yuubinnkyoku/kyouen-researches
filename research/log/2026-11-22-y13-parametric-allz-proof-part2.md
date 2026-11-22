# y=13 two-token パラメトリック全称証明 — part2（C1d・census・K1231 observed→proved 昇格）

- 日時: 2026-11-22 (UTC)
- 実験dir: `research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/`
- 位置づけ: [part1 出版](2026-11-22-y13-parametric-allz-proof-part1.md)（12チェック
  6,353,143 点・全 PASS・3回 byte-identical・commit ee3b6f73/5014e9d5/c6880c0d）が
  残した part2 工程の実行。単一オーナー宣言は
  [y=13 universal verifier single-owner note](2026-11-22-y13-universal-verifier-single-owner-note.md)
  が保持（宣言 2026-11-22T17:59:40Z・commit 7196cbd5・part1+part2 両段階を保持範囲と
  明示・K1231 fit レーンの宣言〔d3404db8・17:01:05Z〕は fit から全称証明段階まで保持を
  明示済みで自宣言と矛盾なし。着手前に最新 main を再取得し他オーナー着手がないことを確認）。

## 実施内容

1. **C1d アンカーの事前検証（組み込み前・fail-closed）**:
   6つの published uniform closed form（z=8: K0999/K1000・z=9: K1001・z=10: K1011・
   z=15/16/17: K1065/K1077/K1087）のアンカー関数 A8u..A17u を y=12 part2 正本検証器
   （SHA-256 e2092976…・監査 6bca3fa2…）から verbatim で抽出し（`Y` は関数
   ローカル変数のみで cand12/cand13 ブロックと干渉しない）、検証器組み込み前に y=13 行を
   生両エンジンで 4 方照合（各 z0・x=13..45・R<=x+z0+30・計 14,157 点・
   anchor/H_ordered/H_canonical/cand13 全一致・不一致 0・z 別
   2,211/2,244/2,277/2,442/2,475/2,508・約 2.2 秒・
   `scripts/preflight_c1d_y13.py`・`output/preflight-c1d-y13.json`・SHA-256 a9307d33…）。
   低 R 単一トークン縮約 R<=z+6（z=15,16,17・x=13..159）9,702 点も不一致 0・2 回実行
   byte-identical。y=10 の同段階が K1087 転写初稿の評価順バグ 170 点を捕捉した実績に
   対し、本族は y=12 正本からの verbatim 再転写のため事前検証は初めから一致
   （bug 捕捉 0 も実験事実として記録）。z=15/16/17 の (y,d) 過渡セル・S<17/S==17 分岐は
   y=13 で到達不能（S=x+13>=26）。
2. **正本検証器 part2**: verify_y13_universal.py に C1d と C11r を組み込み
   （in-place 拡張・part2 正本 SHA-256 079b49ad…・50,865 bytes・1,314 行・part1 出版正本
   b73d9aaa…・36,457 bytes は実験dir外に参考保持）。全チェック指定実行
   （C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12）:
   **総 6,942,579 照合点・全チェック不一致 0・overall PASS**
   （C1d 139,356 点〔アンカー掃引 129,654 点＋低 R 縮約 9,702 点・C11 は Census
   box z=0..79・x=13..70・R<=x+z+14〕・C11r 450,080 点〔4,640 行〕・C4t clip 27
   再掃引の confluence 違反 2,987〔初違反 (60,90,90)〕は part1 と不変・型総数 234,180・
   merge corollary 1,391,747 点・tail corollary 217,342 点は part1 と不変のまま bad 0）。
   audit.json（3,673 bytes・SHA-256 2f5f56c0…・stage 文言 part2）。
3. **3回実行の byte-identical 確認**: run1（同一cwd）→ run2（同一cwd再実行）→
   run3（隔離 tree/cwd/HOME + PYTHONHASHSEED=random・census_rows.py・preflight・
   両 census part も隔離側で再生成）の 3 実行で audit.json・census.txt・
   census-ordered.json・census-canonical.json・preflight-c1d-y13.json が全て
   byte-identical（census_rows.py は記録時にもう 1 回再実行し 4 回 byte-identical・
   maxrss 556,652KB をその実行で実測）。part1 出版 byte の census part 2 ファイル
   （264d7cd8…/82fb8803…）は part2 実行でも同一 byte を再生成。出版前の fail-closed
   検査として census.txt の P 集合 1 桁改ざん（C11r 行不一致・rc=1・PASS 出力なし）と
   欠落（FAIL-CLOSED 明示）を捕捉・復元で clean PASS・baseline と byte-identical。
4. **census_rows.py y=13 版（第三実装）**: y=5..y=10/y=12 と同型の生 tuple 二重再帰で
   z=0..79・x=13..70・R=0..x+z+15 の 4,640 行（450,080 点・値0点 224,203・
   エンジン状態計算〔LRU misses〕6,630,827・約 15 秒・maxrss 約 557MB）を計算・行ごとの
   Thue-Morse 指数・T/P 集合・tail を抽出（tail アサート R>=x+z+14 の (x+13) mod 2
   全行成立）。census.txt（829,622 bytes・4,640 行＋空行 80・SHA-256 505f05bf…）は
   C11r で閉形式 cand13 から再導出して全 450,080 点を独立照合・不一致 0。本実行
   ホストの 1 GiB cgroup 制約のみ LRU 上限 1,600,000 を明示キャップ（docstring 記載・
   出版 y=5..y=10/y=12 版との差はこの 1 点のみ）。
5. **K1231 observed→proved 昇格**: AGENTS.md「同じ命題は同じ K 項目・新規採番なし」に
   従い item を同番号で proved 昇格（title・status・scope・evidence・relations・
   artifacts を更新）。knowledge README に part2/昇格 bullet を追記（commit C と同じ
   末尾追記方式）。K1232 item には part2 artifacts（verify part2 正本・census_rows.py・
   census.txt・preflight・part2 log）を追記。**knowledge.yml CI step は登録しない**:
   現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）実験機の step が存在
   せず（CI 登録は y=10/K1141 まで）、本実験も出版 byte を監査正本とする直近 2 族と
   同一の扱いとする。

## 昇格で確定した横断観察（y=1..13 全称表から・y=13 が 13 族目）

- 基底点 y 点仮説 {z+1,..,z+2y-1}: y=13 で 13 点が全 z 確定（第13例・y=1..13 連続）。
- tail 開始族式 x+z+y+1 と tail 値 (x+y) mod 2: y=13 版（x+z+14・(x+13) mod 2）が
  全称確定（fit レベルの 12 族連続に全称族が y=13 まで到達）。
- マージ命題 x<=z-y-1 → single_token(x+y,z,R): y=13 版（x<=z-14）が全称確定
  （監査上 1,391,747 点独立照合）。
- clip 窓族式 2y+2: y=5..13 の **9 族連続 tight**（y=13 は clip 27 で 2,987 違反・
  2y+2=28 が tight・part1 C4t）。
- 前倒し pin 格子公式 pin=z+(d+3y)/2: y=5..13 の **9 族統一**（d≡y mod 4（奇z）・
  d≡y+2 mod 4（偶z））。y=13 では奇z 7 行 {-11,-7,-3,1,5,9,13}／偶z 6 行
  {-9,-5,-1,3,7,11}（y 奇族の偶z pin 行数 (y-1)/2 が y=11 の 5 行から 6 行に増えた
  初例が全称確定・y 奇族の pin 行 d は奇数）。
- 「pin スロット=th-1」型（奇z pin 行で pin が off=2k=th-1 をちょうど占有）が
  y=11/y=12/y=13 の 3 族連続で全称確定（K1152 が指名した横断型の問いに全称で回答）。
  偶z側は pin が base 行上端 2k-1 の +2 位置（2k+1）に載る slot 則が 3 族で同一。
- base 行 rank 族式 k(d)=floor((d+3y+1)/4) が y=10/11/12/13 の全 base 行（z 偶奇・
  行型反転込み）で同一。偶z I 帯行 k(d)=floor((d+3y-1)/4) が y=11/12/13 の 3 族同一。
  奇z th 則 2k+1 が奇 y 族 3 例目（y 偶奇が th 則を決める観察が全称側でも維持）。
- 対角行上端格子規則 cap=z+y-[z≡y (mod 2)] が y=13 で全称確定。
- 偶z 対角行 d=-y の値1全欠如: y=8..13 の **6 族連続で全称確定**。最終 pin 行
  d=y の I[2y+z+1) 型が 8 族連続（y=6/8/9/10/11/12/13・y=13 は全称確定）。
- B 子に先行出版族の閉形式を逐語転写する構成: cand9（y=10 の B 子）・cand10（y=11 の
  B 子・K1141 全称）・cand11（y=12 の B 子・K1143）・cand12（y=13 の B 子・K1152 全称）
  で 4 連。

## 未解決（次工程候補）

- 横断法則（基底点・tail 開始・マージ・clip 窓・pin 格子・対角行規則・I 帯 th/shift）の
  y>=14 への一般証明レーン（y<=13 が全称確定したので補題化・一般証明を開く価値が
  さらに上がった。type タイプ空間の有限性と族式の帰納構造が本命）。
- y=14 族の fit（着手時は新しい単一オーナー宣言が必須・y 偶族で pin 行数・th 型
  〔y=10/12 と対置〕の判定材料。y 奇族で観測した偶z pin 行数の増加則が y 偶族で
  どうなるかも判定材料）。
- y=11（K1143）の part2 は y=11 レーン保留中につき本レーンでは着手しない。
- 3トークン以上・y>=14 族・固定幅・q点版安定化長・11×11 は範囲外。

## trust 境界

全称性は選択肢分解の健全性・正確な mex 恒等式・有限型空間の完全性
（raw錨・恒等式グリッド・型 confluence・シェル/多様体/probe・出版切片転写アンカー・
独立 census。K1023→K1152 と同一構成・y=13 は K1232 part1/part2 の同型機）による。
Lean ではない。C1d アンカー切片の正しさは K0999/K1000/K1001/K1011/K1065/K1077/K1087
の主張（y=13 行はその特殊例）。標準 11×11 の空盤勝敗・二石 root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 には一切言及しない（すべて UNKNOWN のまま）。

## 出版物（本コミット列）

- part2-a: 実験dir（verify_y13_universal.py part2 正本・census_rows.py・
  scripts/preflight_c1d_y13.py・output/audit.json〔part2 版 14チェック〕・
  output/census.txt・output/preflight-c1d-y13.json・
  output/published_run.txt〔part2 実行記録追記〕・README.md〔part2 節追記〕）＋本 log。
  1 コミット。
- part2-b: K1231 item observed→proved（同番号更新）＋K1232 item part2 artifacts 追記。
  1 コミット。
- part2-c: knowledge README 末尾 bullet 追記（part1 series の commit C と同一手法・
  push 前に最新 HEAD を取り直し blob sha ロックで競合回避）。
- ※ knowledge.yml への CI step 追加は行わない（実施内容 5 の理由による・
  直近 2 族〔K1143/K1152〕と同一の扱い）。
