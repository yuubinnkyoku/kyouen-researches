# 高速レーン実行log: y=22 two-token 全称検証器（単一機体14チェック版）・K1256 昇格（2026-11-23）

- 単一オーナー宣言 e1e60cd4（検証器実行前に出版・観測HEAD-before-push
  db195667〔2026-11-23T12:05:59Z・experiments: Part BV commit A scaffold〕・
  対抗宣言なしを確認済み）配下で、y=21 の出版手続き（K1255・単一機体単一出版）を
  y=22 定数に適合して実行（宣言の事前登録どおり）: 機体は最初から14チェック版
  （part1相当12チェック + C1d アンカー + census第三実装のC11r）として構築し、
  実行は段階分け（転写検査 → C1d preflight → census 生成 → 12チェック電池 →
  14チェック電池）。12チェック電池の audit は audit-part1-12checks.json
  として別正本で保存。

- **y=22 は全称確定済み範囲〔y<=21・K1248 proved〕の外の最初の族**であり、
  B子は出版 cand21（K1248 proved・y=21 機 K1255 で全称確定）の逐語転写
  （**系列初の全称確定済み B-child**）。実行・出版とも本実行が単一オーナー・
  単一出版である（commit A 6360bb32・fetch-back byte 検証で 12 ファイル中
  8 ファイルを cmp で byte 同一確認・残り4ファイルも fetch-back 内容一致）。

- 機体: verify_y22_universal.py（53,422 bytes・SHA-256 96d9787f…・14チェック）
  の転写3ブロック（engine 1,957 bytes〔出版y21機 git blob ca5e8284 から逐語〕・
  cand21 3,502 bytes〔出版 verify_y21_universal.py の cand21 ブロックと出版
  cand21.py〔git blob 38613e92〕の二系統 byte-equality・block-local Y→Y21
  改名・sources_agree〕・cand22 3,212 bytes〔出版 cand22.py〔K1256 fit 実験・
  git blob fd50358e〕から逐語〕）を scripts/check_transcriptions_y22.py
  が検査: **PASS**（engine equal・cand21 二ソース一致 sources_agree・
  cand22 verbatim equal・隔離側でも再生成一致）。
  A子 x==22 行は合流子 {21,22}≡{22,21} で cand21(z,22,R-1)〔y=21族x=22行と
  同一状態〕・B子 出版 cand21 逐語転写〔x>=22 行は定義域 x>=21 の内側〕・
  C子 1 xor cand22(z-1,x,R-1)・型機械 clip 2y+2=46・番兵 47。

- C1d preflight: scripts/preflight_c1d_y22.py（anchor block は出版 y21
  preflight から byte-verbatim・y=22 計測定数のみ適合）が出版6切片アンカー
  （K0999/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）を y=22 行で
  4方照合（anchor×H_ordered×H_canonical×cand22）: **12,012点 bad 0**
  （per z 1,885/1,911/1,937/2,067/2,093/2,119）+ 低R単一トークン縮約
  R<=z+6（z0=15/16/17・x=22..159）**9,108点 bad 0**・**PASS**
  （output/preflight-c1d-y22.json SHA-256 a65b967d…）。機内 C1d 掃引
  （アンカー掃引 125,442 + lowR 9,108）は **134,550点 bad 0**。

- census第三実装: census_rows.py（XMIN=22・XMAX=70・ZHI=80・RBUF=24・
  token (x,22)・tail (x+22)%2・LRU cap 1,600,000・約65秒）が census.txt
  （791,080 bytes・3,920行+80空行区切り・SHA-256 3275cc74…・本editionでは
  実験dirに同梱せず生成器+SHA pinで再現する体裁〔y=21 editionと同一〕）を生成:
  **433,160点・zero_points 216,626・misses 11,469,227・hits 22,466,349**・
  tail assert R>=x+z+23 は全行で成立。C11r（rows==80*49=3,920・全行を
  cand22 から再導出・T/P集合・Thue-Morse index・tail）が **bad 0**
  （重複行・欠損行・rows不一致・trailing newline欠落も FAIL-CLOSED）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M・
  分離コマンド）は各engine **429,240点 bad 0**・merge帰結各 78,750・tail各
  3,920 bad 0（census幾何では x<=z-23 は z>=45 で初めて非空）・C11 mode
  が両部品を fail-closed 検証（engine field・box string・cache cap・再計算
  期待値 429,240/78,750/3,920）の上で merge。

- 段階的12チェック電池（宣言の段階実行・part1相当）: **overall PASS・
  総5,664,680点**（C1 26,220 / C1b 46,220 / C1d 134,550 / C2 242,305 /
  C2b 19,844 / C3 1,425 / C4 562,559 / C4t 562,559〔probe〕 / C7 200,000 /
  C8 1,122,279 / C9 889,974 / C12 1,856,745）・**全bad 0・型797,559**・
  42.0秒。merge帰結（この時点）729,700点 bad 0・tail帰結（この時点）
  183,318点 bad 0。audit は output/audit-part1-12checks.json
  （SHA-256 1d434dbd…）として退避保存。

- フル14チェック監査: **overall PASS・総照合点 6,956,320**（宣言の算術
  どおり: 12チェック電池 5,664,680 + C11 858,480 + C11r 433,160）・
  **全bad 0・型797,559**（系列: y=17 457,645 → y=18 523,398 → y=19 590,877 →
  y=20 658,978 → y=21 727,229 → y=22 797,559）・約41.5秒/run×3。
  merge帰結 **887,200点 bad 0**（C2/C7/C8/C12 呼び出し点 729,700 +
  両census engine 2×78,750・census幾何では z>=45 で初めて非空）・tail帰結
  **191,158点 bad 0**（R>=x+z+23 => (x+22) mod 2）・C4 in-box 登録型数は
  clip 46/番兵 47 で **448,494**（y=21 機の clip 44 で 429,397 を更新）。
  C4t: **clip 45違反280点・最初 (60,108,108)** → clip窓 2y+2=46 は
  **tight・18族連続確定**（y=5..22: 12/14/…/44/46）・最初違反はband下端
  R-z=2y+2=46 とともに歩む系列の**10観測目**
  （(60,90,90)→(60,92,92)→…→(60,106,106)→(60,108,108)・宣言の事前横断予想
  〔違反>0・(60,108,108)〕と完全一致）。audit.json（SHA-256 41813df3…・
  verifier self-hash 96d9787f…）が正本。

- **宣言予想との完全一致（amendment 不用）**: 宣言ノートの事前機械算出
  （predict_y22_counts.py・ループ幾何のみ・出版y19/y20/y21 の3機体 audit の
  14点数ずつを完全一致で再現して cross-validated・数値は stdout から機械転写）
  は、preflight 12,012+9,108・C1d 134,550（125,442+9,108）・census幾何
  （3,920行・429,240/engine・merge 78,750・tail 3,920）・C11r 433,160・
  12チェック電池 5,664,680（小計 6,388,610）・総点 6,956,320・merge帰結
  887,200・tail帰結 191,158・C4t（違反>0・最初違反 (60,108,108)）・C11r
  tail反転 probe bad 3,920 の**すべてが機の実測と完全一致**
  （全段階無修正・散文内転置もなし。y=21 宣言の 86,436→86,469 転置の
  再発防止規約〔数値の機械転写〕が機能した）。

- 決定性: 同一cwd 3回＋隔離 tree/cwd/HOME+env -i+PYTHONHASHSEED=random 1回
  （隔離側は転写検査・preflight・census_rows・census両部・12チェック・
  フル14チェックの完全ゼロ再生成・census engine states まで同一: misses
  11,469,227 / hits 22,466,349）で **4実行 byte-identical**（7出力すべて・
  バイトコードキャッシュ衛生: __pycache__ purge・PYTHONDONTWRITEBYTECODE=1）。

- fail-closed 12種（スクラッチtreeのみ・各probe後にbaselineをbuild bytesと
  cmp検証・正典treeは無傷・**全捕捉 rc=1**）: census.txt欠落→FAIL-CLOSED・
  行削除→「census rows 3,919 != 3,920」FAIL-CLOSED・重複行注入→
  「duplicate census row (0,22)」FAIL-CLOSED・P-set改ざん→C11r bad 1・
  T-set偽member注入→C11r bad 1・C11r tail反転 (x+22)→(x+23)→**bad 3,920**
  （全行・宣言予想どおりrows数）・アンカー誤結合 (17,A17u)→(17,A10u)→
  **C1d bad 14,869**・lowR参照ずれ R→R+1→**bad 9,108**（全lowR点が独立に
  識別）・merge境界 z-23→z-22→merge帰結 **bad 59**〔初回の探針はharnessの
  no-op（境界編集が不発効で未改ざんコピーが PASS）でありharness側の誤りと
  して正直記録し有効版で即再検出〕・clip窓 46,47→44,45→**C4 bad 945**・
  in_P22 tail偶奇反転（x%2==1→==0）→**C1 bad 4,898・C2 bad 24,024**・
  band偶奇改ざん（off%2==0→==1）→**C1 bad 1,763・C2 bad 24,451**。

- **K1256 を observed→proved に昇格**（同一K項目・AGENTS.md規約・
  K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249/
  K1255 前例）。機体は **K1257**（宣言で仮採番・push前に items dir 個別
  パス fetch で 404〔不存在〕を確認の上で確定。kind: computation /
  status: computed・K1255 と同型）。マージ命題
  x<=z-23 => H == single_token(x+22,z,R) は **y=1..22 で全称確定**、tail
  R>=x+z+23 => (x+22) mod 2、clip窓 2y+2=46 tight は**18族連続**（y=5..22）・
  **2トークン族の全称は y=1..22 で完結**（y=1..12 は旧来の単族証明・
  y=13..22 は機械検証の逐語連鎖）・B子逐語連鎖は **cand9..cand21 に拡大**
  （証明済みB子使用は cand10/cand12..cand21・cand21 が系列初の全称確定済み
  B-child として使用された）。標準11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4 はすべてUNKNOWNのまま。3トークン以上・y>=23族・
  固定幅・q点版安定化長は範囲外。

- 出版（本実行・単一出版・**単一ホストの正直記録**）: commit A（実験dir正本
  12ファイル・6360bb32・census.txtは同梱せず生成器+SHA pin・push直前の
  観測HEAD f687fa73・fetch-back byte検証済み）、commit B（本log + K1256
  proved 昇格編集 + K1257 machine item）、commit C（knowledge README bullet
  2件追記）。各push直前にHEAD再取得し commit message に「observed
  HEAD-before-push <sha>」を記載。**y=21 edition と異なり、出版時点で
  兄弟実行による独立ビルド・第二ホストでの出版bytes再現はまだ存在しない**
  （単一ホストでの4実行 byte-identical + 隔離ゼロ再生成 + fail-closed 電池が
  昇格の根拠）。並走する毎時実行が宣言レシピから独立に機体をビルドし全数値を
  再現・出版bytesを第二ホストで再現するのが、次回実行の最優先の裏付け課題。

- 次のレジューム: y=22 全称は完結。残る高速レーン候補は
  (a) **兄弟実行による独立再現**（宣言 e1e60cd4 のレシピから独立ビルド・
  AST同一確認・全数値再現・main から出版 corpus 12ファイルを再取得しての
  第二ホスト段階再実行〔census.txt は生成器+SHA pin 3275cc74… で再現〕・
  y=21 の第2実行がやった体裁の y=22 版）が最優先、
  (b) y=23 族 fit（seed cand21〔K1248 proved〕・奇数y型・本レーン手続きの
  再適用・fit→全称で2単一オーナー宣言が必要・K採番は K1257 使用済みの次の
  空き番）、
  (c) 横断法則一般補題化レーン（band下端 2y+2 の帰納構造・偶奇分離則・
  pin行数則 (y+1)/2 上限の一般化・型系列 457,645→…→797,559 の階差構造）、
  (d) C1dアンカーのz切片拡張（現行 z0∈{8,9,10,15,16,17} の外側の出版
  一様閉形式の有無調査）。
