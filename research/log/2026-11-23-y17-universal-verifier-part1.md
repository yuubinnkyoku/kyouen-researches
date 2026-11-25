# 高速レーン実行log: y=17 two-token 全称検証器 part1（2026-11-23）

- 単一オーナー宣言: `2026-11-23-y17-universal-verifier-single-owner-note.md`
  （commit b099a974・push 2026-11-23T01:05:46Z・宣言時点観測 HEAD 3efab5b9・
  検証器実行前に事前出版・対抗宣言 grep clean〔search_commits "y=17 universal" 0件・
  proof実験dir不在〕）+ 幾何訂正 amendment（commit 03ca97ad・push 2026-11-23T01:08:08Z・
  C2b掃引行 x=17..66 → x∈{17,22,…,67}〔y16 part1 range(16,71,5) の同形平行移動〕・
  他幾何は不変）。宣言ノートの事前横断予想（clip 36 tight・census幾何・型総数5点目）
  はすべて宣言通り。前回レジューム（K1240 y=17 fit・commit 6ca80e0e）が指名した
  最有力課題「y=17 全称（part1 12チェック+part2 C1d/C11r・K1240 昇格）」を実行
  （9be89aa9 を含め宣言系2 commitはいずれも本レーンの同一宣言出版）。

- 選定理由: y<=16 は全称確定済み・y=17 fit は observed（K1240）・clip窓 2y+2=36 の
  13族tight判定と seed法則5連続族 y=17 の全称データ点が空白で、独立完結かつ
  昇格レーン（part2込み）として情報価値最大と判断。

- 機械: verify_y17_universal.py（part1・12チェック・37,970 bytes・SHA-256 2110ecbb…）を
  y=16 出版正本（verify_y16_universal.py part2正本・SHA-256 bdf4fe04…・commit b706b214）から
  族定数適合で構造転写（A子 x==17 合流子 cand16(z,17,R-1)〔{16,17}≡{17,16}〕・
  x>=18 は cand17(z,x-1,R-1)・B子 出版 cand16 逐語〔Y→Y16 改名のみ〕・
  C子 1 xor cand17(z-1,x,R-1)・CLIP/SENT=36/37・census z=0..79・x=17..70・
  R<=x+z+18〔80*54=4,320行〕・merge x<=z-18・宣言amendment幾何
  （C2b x∈{17,22,…,67}）適用済み・
  tail (x+17)%2・C7 seed 20261172・C8 の x=16 行は拡張整合行としてのみ）。
  転写は二重正本方式: scripts/check_transcriptions_y17.py（SHA-256 ac40c03c…）が
  @@TRANSCRIPTION marker 3ブロックを出版bytesと照合（engine 1,957 bytes が
  y16機同一ブロックとbyte一致・cand16 3,298 bytes が出版y16機ブロックと出版cand16.py
  〔commit 33e1c22e〕の2ソースとも改名差分なしで一致・cand17 3,379 bytes が
  出版cand17.py〔commit 6ca80e0e・fit driver省き〕とbyte一致）→
  output/transcriptions-check-y17.json overall PASS・隔離側再実行もPASS。
  part2は C1d/C11r を in-place 拡張（y=13..y=16 と同一手続き・part1の12チェック
  本体byte不変）。組み立てscriptは出版しない。

- 結果（part1・overall PASS・約35秒）: 総照合点 **6,343,825・全bad 0**・型 457,645
  （C1 23,370 / C1b 42,565 / C2 221,235 / C2b 19,404〔amendment幾何 x∈{17,22,…,67}〕 /
  C3 1,275 / C4 590,634 / C4t 590,634〔probe〕 / C7 200,000 / C8 1,014,174 /
  C9 903,114 / C11 881,280 / C12 1,856,140）・型総数系列5点目
  （y13 234,180 → y14 281,912 → y15 335,658 → y16 394,686 → y17 457,645）。
  **C4t: clip 35（2y+1）違反 1,300・最初 (60,98,98) → clip 2y+2=36 は tight・
  tight 13族連続確定（y=5..17: 12/14/…/34/36）**で「最初の違反がband下端
  R-z=2y+2 と歩む」則は5点観測（(60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→
  (60,98,98)・宣言の事前予想どおり違反>0でtight確定）。merge帰結
  x<=z-18 → single_token(x+17,z,R) 1,182,632点 bad 0（宣言どおり z>=35 で
  census merge行が初めて非空・y=15/y=16 に続き3族連続のbox外全域raw anchor）・
  tail帰結 R>=x+z+18 → (x+17)%2 193,096点 bad 0。

- census（C11）: 両エンジン各440,640点 bad 0（merge 119,025・tail 4,320・約17秒/engine）。
  本host（Vibe remote sandbox・~1.0GiB cgroup）は unbounded raw掃引OOMのため
  y=12..y=16 と同一設計の bounded-memoization twin（LRU cap 1,600,000）で
  C11ordered/C11canonical 別コマンド実行・C11モードで部品検証（points改ざん・
  欠落とも FAIL-CLOSED）の上で期待値幾何再計算と merge。

- 決定性: audit.json SHA-256 301f7690…・census-ordered 12234496…・
  census-canonical 1ca205a5… の3実行 byte-identical（同一cwd 2回 + 隔離tree/cwd/HOME
  + env -i + PYTHONHASHSEED=random・census部品は隔離側で再生成しbyte一致）。
  出版treeで正典runを実行（output/published_run.txt: 転写検証→census両部→
  フル12チェック rc=0・audit byte一致）。

- fail-closed 6件（スクラッチtreeで実施・全捕捉）: T1 Y定数 17→16 → bad 1,243(rc=1)・
  T2 pin mod4類改ざん → bad 28(rc=1)・T5b 真の合流順序バグ cand16(z,16,·)
  〔多重集合{16,16}〕→ bad 2,209(rc=1)・T3 census部品points改ざん →
  FAIL-CLOSED(rc=1)・T4 census部品欠落 → FAIL-CLOSED(rc=1)。**誠実記録: T5設計初案
  （合流子を cand17(z,16,·) に置換）は bad 0 で検証器を捕捉しなかった**。これは
  機械の欠陥ではなく、cand17 の x=16 拡張行と cand16 の x=17 行が同一多重集合
  {16,17}（S=33）を記述する拡張整合性（C8 の x=16 拡張行が依存する性質そのもの）
  の観察として実験READMEに記録した。真の順序バグ（T5b）では 2,209 bad を捕捉。

- 解釈規約（宣言どおり）: part1 は K1240 全称の機械的証拠の構成であり status は
  observed のまま。昇格判定は part2（C1d 出版固定z切片アンカー〔preflight fail-closed〕
  + census_rows.py 第三実装 y=17 版〔XMIN=17・RBUF=19〕+ C11r・同一単一オーナー宣言の
  継続）で行う。11×11標準盤・二石root・S2・class 1/2/4 は UNKNOWNのまま、
  照合点数を勝敗として読まない。3トークン以上・y>=18族・固定幅・q点版安定化長は非接触。

- 次のレジューム: part2着手（part1着地済み・同宣言継続）。preflight_c1d_y17.py
  （出版 verify_y16 正本から anchor block 逐語抽出・y=17 行4方照合
  x=17..45・R<=x+z0+30〔z0∈{8,9,10,15,16,17}〕+ 低R単一トークン縮約
  R<=z+6〔z0∈{15,16,17}・x=17..159〕・出力 output/preflight-c1d-y17.json）→
  census_rows.py y=17版（XMIN=17・XMAX=70・RBUF=19・ZHI=80・token (x,17)・
  tail assert R>=x+z+18・出力4,320行）→ 検証器14チェック化（check_C1d掃引
  x=17..159・R<=x+61・check_C11r: values range(0,x+z+20)・tail=(x+17)%2・
  rows==80*54=4,320）→ 3回byte-identical + fail-closed電池6種 →
  **K1240 observed→proved 昇格**（同一K項目・K1237前例）・K1241 part2追記・
  part2 log・README bullet。次族 y=18 fit は別宣言必要。
