# 高速レーン実行log: y=21 two-token 全称検証器（単一機体14チェック版）・K1248 昇格（2026-11-23）

- 単一オーナー宣言 a0519efe（検証器実行前に出版・観測HEAD-before-push
  77d3cadf〔2026-11-23T08:51:03Z〕・対抗宣言なしを確認済み）配下で、
  y=20 の出版手続き（K1249・単一機体単一出版）を y=21 定数に適合して実行
  （宣言の事前登録どおり）: 機体は最初から14チェック版（part1相当12チェック +
  C1d アンカー + census第三実装のC11r）として構築し、実行は段階分け
  （転写検査 → C1d preflight → census 生成 → 12チェック電池 →
  14チェック電池）。12チェック電池の audit は audit-part1-12checks.json
  として別正本で保存。

- 並走と役割分担の記録: 毎時運行の並走により、**第1実行**が宣言の下で
  機体ビルドから段階実行・決定性4回・fail-closed 12種・昇格判定・
  実験dir正本12ファイルの出版（commit 8960e633・2026-11-23T09:47:25Z）
  まで完了していたのを、第2実行が最新 main 取得時に確認した。知識側反映
  （本log・K1248 昇格編集・K1255 機体item・README bullet）は未着手だった
  ため、**第2実行**（本log作成側）が独立再現・第二ホスト検証を実施して
  から知識側の出版を担った。機体の単一出版規約は守られている: 実験dir
  正本は第1実行の出版 8960e633 が唯一の正本であり、第2実行はそれを一切
  改変せず、検証のみを行った。

- 第2実行の独立再現（要約）:
  - 同一宣言の機体レシピから独自ビルドした**第2機体**
    verify_y21_universal.py（53,197 bytes・SHA-256 fb84f369…）は、
    出版機体（53,269 bytes・SHA-256 0ab841d9…）と**実行可能コードについて
    AST 同一**（docstring・コメントを除去した構文木が完全一致・差分は
    すべて非実行テキスト）。
  - 第2機体で全段階パイプライン（転写検査→preflight→census→両census部→
    12チェック→フル14チェック）を自前実行し、全数値が第1実行の出版記録
    （published_run.txt・README）と完全一致。なお census_rows.py は
    両ビルドで byte 一致。
  - 決定性: 自前監査（audit.json SHA-256 a0b23fb3…）は同一cwd 3回 +
    隔离 tree/cwd/HOME+env -i+PYTHONHASHSEED=random 1回（隔離側は
    full-pipeline 完全ゼロ再生成）で **byte-identical**・検証台帳
    census.txt は自前生成が出版 pin d63141b7… と byte 同一。
  - fail-closed 電池12種を自前でも実施し**全捕捉**（下記・探針(2)の
    初回 no-op を正直記録し有効版で再検出）。
  - **出版 bytes の第二ホスト再現**: main から 8960e633 の corpus 12ファイル
    を再取得し段階再実行（転写検査→preflight→census 生成→両 census 部→
    12チェック→14チェック）して、**全7出版出力**
    （census.txt d63141b7…・audit.json c039ca73…〔出版機体の
    self-hash 0ab841d9… を含む〕・audit-part1 dab3dc53…・
    census-ordered 30279436…・census-canonical b88e3ddc…・
    preflight 57897cfd…・transcriptions-check 79007127…）
    が**すべて byte 一致**で再現されることを確認した。

- 機体（出版正本・8960e633）: verify_y21_universal.py（53,269 bytes・
  SHA-256 0ab841d9…・14チェック）の転写3ブロック
  （engine 1,957 bytes〔出版y20機 git blob 170f3346 から逐語〕・
  cand20 3,308 bytes〔出版cand20.py〔git blob a54cfb40〕と
  出版y20機ブロックの二系統 byte-equality・Y→Y20 改名〕・cand21 3,412
  bytes〔出版 cand21.py〔git blob 38613e92〕から逐語〕）を
  scripts/check_transcriptions_y21.py が検査: **PASS**
  （engine equal・cand20 二ソース一致 sources_agree・cand21 verbatim
  equal・隔離側でも再生成一致）。
  A子 H(R-1;(x-1,21);z)〔x==21 行は合流子 {20,21}≡{21,20} で
  cand20(z,21,R-1)・y=20族x=21行と同一状態〕・B子 出版 cand20 逐語転写
  〔x>=21 行は定義域 x>=20 の内側〕・C子 1 xor cand21(z-1,x,R-1)・
  型機械 clip 2y+2=44・番兵 45。

- C1d preflight: scripts/preflight_c1d_y21.py（anchor block は出版 y20
  preflight から byte-verbatim・y=21 計測定数のみ適合）が出版6切片アンカー
  （K0999/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）を
  y=21 行で4方照合（anchor×H_ordered×H_canonical×cand21）:
  **11,856点 bad 0**（per z 1,859/1,885/1,911/2,041/2,067/2,093）+
  低R単一トークン縮約 R<=z+6（z0=15/16/17・x=21..159）**9,174点 bad 0**・
  **PASS**（output/preflight-c1d-y21.json SHA-256 57897cfd…）。
  アンカーは組み込み前 fail-closed ゲートを通過。機内 C1d 掃引
  （アンカー掃引 125,934 + lowR 9,174）は **135,108点 bad 0**。

- census第三実装: census_rows.py（XMIN=21・XMAX=70・ZHI=80・RBUF=23・
  token (x,21)・tail (x+21)%2・LRU cap 1,600,000・census_rows.py 自身は
  両ビルド byte 一意）が census.txt（800,318 bytes・4,000行+80空行区切り・
  SHA-256 d63141b7…・本editionでは実験dirに同梱せず生成器+SHA pinで
  再現する体裁〔y=20 editionは同梱・第2実行が第二ホストで生成byte一致を
  確認〕）を生成: **436,000点・zero_points 217,061・misses 10,909,227・
  hits 21,370,154・約21-26秒**・tail assert R>=x+z+22 は全行で成立。
  C11r（rows==80*50=4,000・values range(0,x+z+23)・T/P集合・Thue-Morse
  index・tail 再導出）が全行を cand21 から再導出・**bad 0**
  （重複行・欠落行・rows不一致・trailing newline欠落も FAIL-CLOSED）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・
  LRU 1.6M・分離コマンド）は各engine **432,000点 bad 0**・merge帰結各
  86,469・tail各 4,000 bad 0・C11 mode が両部品を fail-closed 検証の上
  merge。

- 段階的12チェック電池（宣言の段階実行・part1相当）: **overall PASS・
  総5,652,761点**（C1 25,650 / C1b 45,489 / C1d 135,108 / C2 238,091 /
  C2b 19,756 / C3 1,395 / C4 568,340 / C4t 568,340〔probe〕 / C7 200,000 /
  C8 1,100,592 / C9 892,650 / C12 1,857,350）・**全bad 0・型727,229**・
  52.4秒。merge帰結（この時点）771,114点 bad 0・tail帰結（この時点）
  184,053点 bad 0。
  audit は output/audit-part1-12checks.json（SHA-256 dab3dc53…）として
  退避保存。

- フル14チェック監査: **overall PASS・総照合点 6,952,761**（宣言の算術
  どおり: 12チェック電池 5,652,761 + C11 864,000 + C11r 436,000）・
  **全bad 0・型727,229**（系列: y=17 457,645 → y=18 523,398 →
  y=19 590,877 → y=20 658,978 → y=21 727,229）・約53秒/run×3。
  merge帰結 **944,052点 bad 0**（C2/C7/C8/C12 呼び出し点 771,114 +
  両census engine 2×86,469・census幾何では z>=43 で初めて非空・
  **8族連続のbox内マージ0行の族的持続**）・tail帰結 **192,053点 bad 0**
  （R>=x+z+22 => (x+21) mod 2）・C4 in-box 登録型数は clip 44/番兵 45 で
  **429,397**（y=20 機の clip 42 で 408,708 を更新）。
  C4t: **clip 43違反408点・最初 (60,106,106)** → clip窓 2y+2=44 は
  **tight・17族連続確定**（y=5..21: 12/14/…/42/44）・最初違反はband下端
  R-z=2y+2=44 とともに歩む系列の**9観測目**
  （(60,90,90)→(60,92,92)→…→(60,104,104)→(60,106,106)）。
  audit.json（SHA-256 c039ca73…・verifier self-hash 0ab841d9…）が正本。

- **宣言予想と実測の完全一致（amendment 不用）**: 宣言ノートの事前機械
  算出（出版y19とy20の両auditの14点数を完全一致で再現して
  cross-validated）は、preflight 11,856+9,174・C1d 135,108・
  census幾何（4,000行・432,000/engine・merge 86,469・tail 4,000）・
  C11r 436,000・12チェック小計 6,381,653（C1dを除く12チェック+C11）・
  段階電池 5,652,761・総点 6,952,761・merge帰結 944,052・tail帰結
  192,053・C4t（違反>0・最初違反 (60,106,106)）・C11r tail反転
  bad 4,000 の**すべてが機の実測と完全一致**（全段階無修正）。
  唯一の差異は宣言散文内の per-engine merge領域の**転置1件**（宣言記載
  86,436 → 機械算出 86,469・同一宣言の合計 944,052 は
  771,114 + 2×86,469 と自己整合）で、宣言noteを日付付き一次資料として
  改稿せず、実験README・run transcript・K1255 item・K1248昇格編集に
  訂正記録した。

- fail-closed 12種（両実行がそれぞれ実施・スクラッチtreeのみ・各probe後に
  baseline を build bytes と cmp 検証・正典treeは無傷・**両実行とも全捕捉
  rc=1**）: census.txt欠落→FAIL-CLOSED「census.txt is missing; run
  census_rows.py first」・行削除→「census rows 3999 != 4000」FAIL-CLOSED・
  重複行注入→「duplicate census row (0,21)」FAIL-CLOSED・P-set改ざん→
  C11r bad 1・T-set偽member注入→C11r bad 1・C11r tail反転 (x+21)→(x+22)→
  **bad 4,000（全行・宣言予想どおりrows数）**・アンカー誤結合
  (17,A17u)→(17,A10u)→**C1d bad 14,769**・lowR参照ずれ R→R+1→
  **bad 9,174（全lowR点が独立に識別する事実の記録）**・merge境界
  z-22→z-21→merge帰結 **bad>0**（第1実行は 806,178点中 bad 7,435・
  第2実行は C2 絞り実行で bad 82・いずれも overall FAIL）・
  clip窓 44,45→42,43→**C4 bad 1,360**・in_P21 tail偶奇反転→
  **C1 bad 2,449・C2 bad 23,478**（両実行で同一値・第2実行は
  tail帰結 bad 11,466 も同時検出）・in_P21 band偶奇改ざん→
  **第1実行は両band行改ざんで C1 bad 1,692・C2 bad 24,431・
  第2実行は band_base 単独で C1 bad 935・C2 bad 23,211**。
  harness no-op の正直記録: 第1実行の探針(4)(5)の初回は
  改ざん正規表現が ASCII 括弧集合構文 `[...]` にマッチして台帳の
  brace 集合 `T={} / P={...}` を編集できない no-op（AttributeError で
  編集前に中断・未改ざんコピーは PASS）であり、有効版（P={1,...}→P={4,...}
  ・T={}→T={5}）で即再検出した。第2実行の探針(2)の初回は末尾の空行区切り
  1行削除（台帳は4,000行のまま有効・no-op）をデータ行削除と取り違えた
  harness 側の誤りとして正直記録し、最後の非空行=データ行削除で再発行し
  「census rows 3999 != 4000」を検出した。

- コメントレベル瑕疵の正直記録（すべて非実行コード・数値・検証内容への
  影響なし・AST同一性で実行面の同一性は保証済み）:
  出版機体側: cand21 転写ブロック直上 docstring の cand21.py SHA-256 表記
  が1文字欠落（63桁・正しくは 64桁
  10d8e495…c9823…）・fail-closed 探針コメント "(CLIP=41)" が y=20 機の
  まま未更新（実行は CLIP=43 で正しく動作・C4t チェック自体は正常）・
  anchor block 由来コメントが chain-head を 99b7e070 と誤表記
  （実際は 8960e633 時点の d29acbd8・git blob 表記は正しい）。
  第2機体側: 同コメントが「y=19 machine's anchor block」のまま
  （直接の転写元が出版 y20 機であることを明示せず）。出版にあたって
  これらを K1255 item と本log に記録して正本（8960e633）は無改造で
  そのまま採用した。

- **K1248 を observed→proved に昇格**（同一K項目・AGENTS.md規約・
  K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243/K1246 前例）。
  機体は **K1255**（宣言で仮採番・push前に items dir 個別パス fetch で
  404〔不存在〕を確認の上で確定。kind: computation / status: computed・
  K1249 と同型）。マージ命題
  x<=z-22 => H == single_token(x+21,z,R) は **y=1..21 で全称確定**、
  tail R>=x+z+22 => (x+21) mod 2、clip窓 2y+2=44 tight は**17族連続**
  （y=5..21: 12/14/…/42/44）・**2トークン族の全称は y=1..21 で完結**
  （y=1..12 は旧来の単族証明・y=13..21 は機械検証の逐語連鎖）・
  B子逐語連鎖は **cand9..cand20 に拡大**（証明済みB子使用は
  cand10/cand12..cand20）。標準11×11空盤・二石root・S2 {59,60}・
  class 1/2/4 はすべてUNKNOWNのまま。3トークン以上・y>=22族・
  固定幅・q点版安定化長は範囲外。

- 出版: commit A（第1実行・実験dir正本12ファイル・8960e633・出版済み）、
  commit B（本log + K1248 proved 昇格編集 + K1255 machine item）、
  commit C（knowledge README bullet 2件追記）。各push直前にHEAD再取得し
  commit message に「observed HEAD-before-push <sha>」を記載。並走実行
  与りの同時書き込み・HEAD変化があれば無理に押し進めず記録して次回へ
  回す規約どおりに対応する。

- 次のレジューム: y=21 全称は完結・2トークン族の全称は y=1..21 で完結。
  残る高速レーン候補は
  (a) y=22 族の fit + 全称（本レーン手続きの再適用・B子転写源は
  cand21〔proved・git blob 38613e92〕・seed法則は y=21 の次の偶数y、
  fit→全称で2単一オーナー宣言が必要）、
  (b) 横断法則一般補題化レーン（band下端 2y+2 の帰納構造・偶奇分離則・
  pin行数則 (y+1)/2 上限の一般化・型系列 457,645→523,398→590,877→
  658,978→727,229 の階差構造）、
  (c) C1dアンカーのz切片拡張（現行 z0∈{8,9,10,15,16,17} の外側の出版
  一様閉形式の有無調査）、
  (d) 3トークン族への構造則（pin行数則の極限挙動・k=Y飽和形状など）
  の予備観察（K1247 仮採番レーン）。
