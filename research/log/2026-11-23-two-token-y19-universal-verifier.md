# 高速レーン実行log: y=19 two-token 全称検証器（単一機体14チェック版）・K1243 昇格（2026-11-23）

- 単一オーナー宣言 da6c1f5f（検証器実行前に出版・観測HEAD 6f5419b5・
  対抗宣言なしを確認済み）配下で、y=13..y=18 の出版手続き
  （part1 12チェック→part2 C1d+C11r 拡張）を**単一機体単一出版**に
  一体化した変形として実行（宣言の事前登録どおり）: 機体は最初から
  14チェック版（part1相当12チェック + C1d アンカー + census第三実装の
  C11r）として構築し、実行は段階分け
  （転写検査 → C1d preflight → census 生成 → 12チェック電池 →
  14チェック電池）。12チェック電池の audit は
  audit-part1-12checks.json として別正本で保存
  （出版系列の thread-series 比較に使用可能）。

- 機体ビルド: publish-then-execute規約どおり、build_y19.py は
  count-asserted（宣言の機械算出予想点数をビルド時に全文検査）で
  正本を構築。ビルド中の数回の count 修正はすべてビルド段階の
  ローカル作業で出版bytesには含まれない。正本
  verify_y19_universal.py（52,631 bytes・SHA-256 76525717…・14チェック）
  の転写3ブロック（engine 1,957 bytes〔出版y18機part2 d29acbd8・
  8ddd0c2f…から逐語〕・cand18 3,307 bytes〔出版y18機ブロックと出版
  cand18.py fit の二系統 byte-equality・Y→Y18 改名〕・cand19 3,411
  bytes〔出版 cand19.py・K1243 fit 実験 eaea0f6aから逐語〕）を
  scripts/check_transcriptions_y19.py（SHA-256 56a999bd…）が検証:
  **PASS**（engine equal・cand18 二ソース一致 sources_agree・
  cand19 verbatim equal・0.06秒・隔離側でも再生成一致）。

- C1d preflight: scripts/preflight_c1d_y19.py（SHA-256 9bc154ee…・
  anchor block は出版 y18 preflight から byte-verbatim〔y=10/y=12
  連鎖〕・y=19 計測定数のみ適合）が出版6切片アンカー
  （K0999/K1000/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）
  を y=19 行で4方照合（anchor×H_ordered×H_canonical×cand19・
  x=19..45・R<=x+z0+30）: **12,069点 bad 0**（per z 1,890/1,917/1,944/
  2,079/2,106/2,133）+ 低R単一トークン縮約 R<=z+6（z0=15/16/17・
  x=19..159）**9,306点 bad 0**・**PASS**（3.1秒・
  output/preflight-c1d-y19.json SHA-256 1cfabdcf…）。
  y=10 prefight が K1087 初稿の評価順序バグ170点を捕捉した前例どおり
  ゲートは実効した（本族は逐語再転写で初回一致）。

- census第三実装: census_rows.py（SHA-256 e4eed396…・XMIN=19・XMAX=70・
  RBUF=21・ZHI=80・token (x,19)・tail (x+19)%2・LRU cap 1,600,000）
  が census.txt（809,842 bytes・4,160行+空行80・SHA-256 07213ab1…）
  を生成: **440,960点・zero_points 219,556・misses 9,806,027・約21秒**・
  tail assert R>=x+z+20 は全行で成立。C11r（rows==80*52=4,160・
  values range(0,x+z+21)・T/P集合・Thue-Morse index・tail再導出）が
  全行を cand19 から再導出・**bad 0**（重複行・欠落行・rows不一致は
  FAIL-CLOSED〔trailing newline欠落も〕）。census部品
  （C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M・
  分離コマンド）は各engine **436,800点 bad 0**・merge帰結各102,459・
  tail各4,160 bad 0・C11 mode が両部品を fail-closed 検証の上 merge
  （box文字列・cache cap・再計算期待点数 436,800/102,459/4,160）。

- 段階的12チェック電池（宣言の段階実行・part1相当）: **overall PASS・
  総5,627,353点**（C1 24,510 / C1b 44,027 / C1d 136,206 / C2 229,663 /
  C2b 19,580 / C3 1,335 / C4 579,657 / C4t 579,657〔probe・bad集計外〕 /
  C7 200,000 / C8 1,057,317 / C9 897,930 / C12 1,857,471）・
  **全bad 0・型590,877**・37.4秒。merge帰結（この時点）857,191点 bad 0・
  tail帰結 184,200点 bad 0。C4t: **clip 39違反770・最初 (60,102,102)**
  → clip窓 2y+2=40 は **tight・15族連続確定**（y=5..19:
  12/14/…/38/40）・最初違反はband下端とともに歩む系列の**7観測目**
  （y=13..18 の (60,90,90)/…/(60,100,100) に続き (60,102,102)）。
  audit は output/audit-part1-12checks.json（SHA-256 63617241…）として
  退避保存。

- フル14チェック監査: **overall PASS・総照合点 6,941,913**
  （宣言の算術どおり: 12チェック小計 6,364,747 + C1d 136,206 +
  C11r 440,960）・**全bad 0・型590,877**（系列: y=17 457,645 →
  y=18 523,398 → y=19 590,877）・37.1秒/run。
  merge帰結 **1,062,109点 bad 0**・tail帰結 **192,520点 bad 0**。
  C4t は段階実行と同一（clip 39違反770・(60,102,102)）。

- **宣言予想と実測の完全一致（amendment 不用）**: 宣言ノートの
  事前機械算出（predict_y19_counts.py・ループ幾何のみ・ゲーム評価なし
  ・出版y18 part2 auditの14点数を完全一致で再現することでcross-validated）
  は、preflight 12,069+9,306・C1d 136,206・census幾何（4,160行・
  436,800/engine・merge 102,459・tail 4,160）・C11r 440,960・
  12チェック小計 6,364,747・総点 6,941,913・C4t（違反>0・最初違反
  (60,102,102)）・C11r tail反転 probe 4,160 の**すべてが機の実測と
  完全一致**（y18 part1 の merge予測スリップ〔105,651→110,682〕と
 異なり、全段階で訂正は不要だった）。

- 決定性: audit.json（SHA-256 59b6fded…）・census.txt（07213ab1…）・
  preflight-c1d-y19.json（1cfabdcf…）・census両部
  （df767357…/afdf9e60…）・転写検査JSON（8a68ecb4…）の**4実行
  byte-identical**（同一cwd 2回 + 隔離 tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random 2回〔うち1回は転写検査・preflight・
  census_rows・census両部・フル14チェックの完全ゼロ再生成〕）。

- fail-closed 12種（スクラッチtreeで実施・**全捕捉**・各probe後に
  baselineをbuild bytesとcmp検証し復元）: census.txt欠落→FAIL-CLOSED
  「census.txt is missing」・行削除→「census rows 4159 != 4160」
  FAIL-CLOSED・重複行注入→「duplicate census row (0,19)」FAIL-CLOSED・
  P-set改ざん→C11r bad 1・T-set改ざん→C11r bad 1・C11r tail反転
  (x+19)→(x+20)→**bad 4,160（全行・宣言予想どおりrows数）**・
  アンカー誤結合 (16,A16u)→(16,A10u)→**C1d bad 1,743**・lowR参照ずれ
  R→R+1→**bad 9,306（全lowR点が独立に識別する事実の記録）**・
  merge境界 z-20→z-19→merge帰結 bad > 0・clip窓 40,41→38,39→
  **C4 bad 2,520**・in_P19 tail偶奇反転→**C1 bad 2,449・C2 bad 23,478・
  tail帰結 bad 11,466**・in_P19 band_base偶奇改ざん→**C1 bad 935・
  C2 bad 23,211**（12種すべてrc=1で捕捉・正典treeは無傷を確認）。

- **K1243 を observed→proved に昇格**（同一K項目・AGENTS.md規約・
  K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242 前例）。機体は
  **K1245**（仮採番→push前404確認の上で確定。kind: computation /
  status: computed・K1244 と同型）。マージ命題
  x<=z-20 => H == single_token(x+19,z,R) は **y=1..19 で全称確定**、
  tail R>=x+z+20 => (x+19) mod 2、clip窓 2y+2=40 tight は**15族連続**
  （y=5..19: 12/14/…/38/40）・B子逐語連鎖は **cand9..cand18 に拡大**
  （証明済みB子使用は cand10/cand12..cand18）・2トークン族の全称は
  **y=1..19 で完結**。標準11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4 はすべてUNKNOWNのまま。3トークン以上・
  y>=20族・固定幅・q点版安定化長は範囲外。

- 出版: commit A（census.txt 単独・810KB）、commit B（正本検証器・
  census_rows.py・scripts 2点・output 7点・実験README）、commit C
  （本log + K1243 proved昇格編集 + K1245 machine item 新設）、
  commit D（knowledge README bullet）。各push直前にHEAD再取得し
  commit message に「Observed HEAD-before-push <sha>」を記載。

- 次のレジューム: y=19 全称は完結。残る高速レーン候補は
  (a) 横断法則一般補題化レーン（band下端 2y+2 の帰納構造・偶奇分離
  則〔奇y band_base/band_int分離・偶y単一band〕・seed法則8連続目
  候補の y=20 fit は seed候補を y=19 proved 族の機械翻訳外挿で
  検証する予想問題として定式化可能・ただし y=20 fit は別宣言が必要）、
  (b) C1dアンカーのz切片拡張（現行 z∈{8,9,10,15,16,17} の外側の
  出版一様閉形式の有無調査）、(c) 3トークン族への構造則（pin行数則
  (y+1)/2・k=Y飽和3行則など）の予備観察。y=20 族全称は本レーンの
  保持範囲外で本工程の結果のみを受け取る。
