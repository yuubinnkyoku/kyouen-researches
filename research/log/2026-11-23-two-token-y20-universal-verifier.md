# 高速レーン実行log: y=20 two-token 全称検証器（単一機体14チェック版）・K1246 昇格（2026-11-23）

- 単一オーナー宣言 c1987caa（検証器実行前に出版・観測HEAD-before-push
  69f76309・対抗宣言なしを確認済み）配下で、y=19 の出版手続き（K1245・
  単一機体単一出版）を y=20 定数に適合して実行（宣言の事前登録どおり）:
  機体は最初から14チェック版（part1相当12チェック + C1d アンカー +
  census第三実装のC11r）として構築し、実行は段階分け
  （転写検査 → C1d preflight → census 生成 → 12チェック電池 →
  14チェック電池）。12チェック電池の audit は
  audit-part1-12checks.json として別正本で保存。

- 機体ビルド: publish-then-execute規約どおりビルド段階のローカル作業を
  経て正本を確定。正本 verify_y20_universal.py（53,146 bytes・
  SHA-256 1e2a519f…・14チェック）の転写3ブロック
  （engine 1,957 bytes〔出版y19機 blob c0cec1d5 から逐語〕・
  cand19 3,501 bytes〔出版cand19.py〔fit eaea0f6a blob cb05633f〕と
  出版y19機ブロックの二系統 byte-equality・Y→Y19 改名〕・cand20 3,212
  bytes〔出版 cand20.py〔7a2d3f9a blob a54cfb40〕から逐語〕）を
  scripts/check_transcriptions_y20.py（SHA-256 82420958…）が検査:
  **PASS**（engine equal・cand19 二ソース一致 sources_agree・
  cand20 verbatim equal・隔離側でも再生成一致）。
  A子 H(R-1;(x-1,20);z)〔x==20 行は合流子 {19,20}≡{20,19} で
  cand19(z,20,R-1)〕・B子 出版 cand19 逐語転写・C子 1 xor
  cand20(z-1,x,R-1)・型機械 clip 2y+2=42・番兵 43。

- C1d preflight: scripts/preflight_c1d_y20.py（SHA-256 3e9932d7…・
  anchor block は出版 y19 preflight から byte-verbatim・y=20 計測定数
  のみ適合）が出版6切片アンカー
  （K0999/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）を
  y=20 行で4方照合（anchor×H_ordered×H_canonical×cand20・x=20..45・
  R<=x+z0+30）: **11,700点 bad 0**（per z 1,833/1,859/1,885/2,015/
  2,041/2,067）+ 低R単一トークン縮約 R<=z+6（z0=15/16/17・x=20..159）
  **9,240点 bad 0**・**PASS**（3.3秒・output/preflight-c1d-y20.json
  SHA-256 d2aabc6e…）。アンカーは組み込み前 fail-closed ゲートを通過。

- census第三実装: census_rows.py（SHA-256 af93fcc7…・XMIN=20・XMAX=70・
  ZHI=80・token (x,20)・tail (x+20)%2・LRU cap 1,600,000）が
  census.txt（801,508 bytes・4,080行+空行80・SHA-256 b858c496…）を生成:
  **438,600点・zero_points 219,325・misses 10,354,827・hits 20,284,849・
  約20秒**・tail assert R>=x+z+21 は全行で成立。C11r
  （rows==80*51=4,080・values range(0,x+z+22)・T/P集合・
  Thue-Morse index・tail再導出）が全行を cand20 から再導出・**bad 0**
  （重複行・欠落行・rows不一致は FAIL-CLOSED〔trailing newline欠落も〕）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・
  LRU 1.6M・分離コマンド）は各engine **434,520点 bad 0**・merge帰結各
  94,380・tail各 4,080 bad 0・C11 mode が両部品を fail-closed 検証の上
  merge（box文字列・cache cap・再計算期待点数）。

- 段階的12チェック電池（宣言の段階実行・part1相当）: **overall PASS・
  総5,640,320点**（C1 25,080 / C1b 44,758 / C1d 135,660 / C2 233,877 /
  C2b 19,668 / C3 1,365 / C4 574,040 / C4t 574,040〔probe〕 / C7 200,000 /
  C8 1,078,938 / C9 895,302 / C12 1,857,592）・**全bad 0・型658,978**・
  38.9秒。merge帰結（この時点）814,607点 bad 0・tail帰結 184,094点
  bad 0。C4t: **clip 41違反570・最初 (60,104,104)** → clip窓 2y+2=42 は
  **tight・16族連続確定**（y=5..20: 12/14/…/40/42）・最初違反はband下端と
  ともに歩む系列の**8観測目**（y=13..19 の (60,90,90)/…/(60,102,102) に
  続き (60,104,104)）。audit は output/audit-part1-12checks.json
  （SHA-256 ff347b9c…）として退避保存。

- フル14チェック監査: **overall PASS・総照合点 6,947,960**（宣言の算術
  どおり: 12チェック電池 5,640,320 + C11 869,040 + C11r 438,600）・
  **全bad 0・型658,978**（系列: y=17 457,645 → y=18 523,398 →
  y=19 590,877 → y=20 658,978）・39.5秒/run。merge帰結
  **1,003,367点 bad 0**（census幾何では z>=41 で初めて非空）・tail帰結
  **192,254点 bad 0**。C4t は段階実行と同一（clip 41違反570・
  (60,104,104)）。

- **宣言予想と実測の完全一致（amendment 不用）**: 宣言ノートの事前機械
  算出（出版y19 auditの14点数を完全一致で再現して cross-validated）は、
  preflight 11,700+9,240・C1d 135,660・census幾何（4,080行・
  434,520/engine・merge 94,380・tail 4,080）・C11r 438,600・
  12チェック小計 6,373,700 = 5,504,660 + C11 869,040・総点 6,947,960・
  C4t（違反>0・最初違反 (60,104,104)）・C11r tail反転 probe 4,080 の
  **すべてが機の実測と完全一致**（全段階無修正）。

- 決定性: audit.json（SHA-256 a09cad0e…）・census.txt（b858c496…）・
  preflight-c1d-y20.json（d2aabc6e…）・census両部
  （ed073fa8…/1f420269…）・転写検査JSON（db16070a…）の**4実行
  byte-identical**（同一cwd 3回 + 隔離 tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random 1回〔隔離側は転写検査・preflight・census_rows・
  census両部・フル14チェックの完全ゼロ再生成で census engine states
  まで同一: misses 10,354,827 / hits 20,284,849〕）。

- fail-closed 12種（スクラッチtreeで実施・**全捕捉**・各probe後にbaseline
  をbuild bytesとcmp検証し復元）: census.txt欠落→FAIL-CLOSED「census.txt
  is missing」・行削除→「census rows 4079 != 4080」FAIL-CLOSED・重複行
  注入→「duplicate census row (0,20)」FAIL-CLOSED・P-set改ざん→C11r
  bad 1・T-set偽member注入→C11r bad 1・C11r tail反転 (x+20)→(x+21)→
  **bad 4,080（全行・宣言予想どおりrows数）**・アンカー誤結合
  (17,A17u)→(17,A10u)→**C1d bad 14,666**・lowR参照ずれ R→R+1→
  **bad 9,240（全lowR点が独立に識別する事実の記録）**・merge境界
  z-21→z-20→merge帰結 **bad 7,528**・clip窓 42,43→40,41→**C4 bad 1,881**・
  in_P20 tail偶奇反転→**C1 bad 4,898・C2 bad 24,024**・in_P20 band偶奇
  改ざん→**C1 bad 1,763・C2 bad 24,451**（12種すべてrc=1で捕捉・正典tree
  は無傷を確認）。探針(4)(8)の初回はprobe harness自体のno-op
  （sed pattern不一致）として正直記録し、有効な改ざん版で即再検出した。

- **K1246 を observed→proved に昇格**（同一K項目・AGENTS.md規約・
  K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243 前例）。機体は
  **K1249**（宣言で仮採番・push前に404確認の上で確定。kind: computation /
  status: computed・K1245 と同型）。マージ命題
  x<=z-21 => H == single_token(x+20,z,R) は **y=1..20 で全称確定**、
  tail R>=x+z+21 => (x+20) mod 2、clip窓 2y+2=42 tight は**16族連続**
  （y=5..20: 12/14/…/40/42）・B子逐語連鎖は **cand9..cand19 に拡大**
  （証明済みB子使用は cand10/cand12..cand19）・2トークン族の全称は
  **y=1..20 で完結**。誠実記録: fit項K1246のK1243関係ノートの合流子の
  帳簿記載「y=19族x=19行」は機体の実装どおり「y=19族x=20行」
  （A = cand19(z,20,R-1)・C3/C1b raw照合で検証済み）の誤記で、
  昇格編集で訂正した（実効的内容は不変）。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべてUNKNOWNのまま。
  3トークン以上・y>=21族・固定幅・q点版安定化長は範囲外。

- 出版: commit A（実験dir正本一式・census.txt 801KB 含む）、commit B
  （本log + K1246 proved昇格編集 + K1249 machine item 新設）、commit C
  （knowledge README bullet 追記）。各push直前にHEAD再取得し commit
  message に「observed HEAD-before-push <sha>」を記載。

- 次のレジューム: y=20 全称は完結。残る高速レーン候補は
  (a) y=21 族の全称（fit は既に K1248 で observed 出版済み・全称には
  別の単一オーナー宣言と cand20→cand21 の逐語転写が必要・本レーンの
  手続きと機体構成〔preflight anchor block の byte-verbatim 連鎖・
  census第三実装・C4t 歩み予想〕をそのまま適用可能）、
  (b) 横断法則一般補題化レーン（band下端 2y+2 の帰納構造・偶奇分離則・
  seed法則9連続目の検証は y=21 fit が受け持ち）、
  (c) C1dアンカーのz切片拡張（現行 z∈{8,9,10,15,16,17} の外側の出版
  一様閉形式の有無調査）、(d) 3トークン族への構造則（pin行数則の
  極限挙動・k=Y飽和3行則など）の予備観察。
