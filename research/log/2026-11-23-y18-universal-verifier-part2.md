# 高速レーン実行log: y=18 two-token 全称検証器 part2・K1242 昇格（2026-11-23）

- 単一オーナー宣言 1d46f883 の継続として part2 を実行（part1 commit
  9f3d5764・K1244 の引き継ぎどおり。手続きは y=13..y=17 の part2 と同一）。
  part1出版物（audit SHA c090be81…・census両部 af284ab7…/9c817177…・
  転写検査 83c60e89…）は part2セッションの再実行でも再現し不変。

- C1d 事前検証: scripts/preflight_c1d_y18.py（SHA-256 1d21c6ab…・出版y17
  part2正本（commit ab23d120・4253cf29…）のanchor block逐語・
  provenance headerのみy=18計測値へ書換・他は出版y17 preflightの
  定数適合〔count-asserted〕）が、出版6切片アンカー（A8u..A17u・
  K0999/K1000/K1001/K1011/K1065/K1077/K1087）を y=18行で4方照合
  〔anchor×H_ordered×H_canonical×cand18・x=18..45・R<=x+z0+30・
  z0∈{8,9,10,15,16,17}〕: **12,432点 bad 0**（per z 1,946/1,974/2,002/
  2,142/2,170/2,198）+ 低R単一トークン縮約 R<=z+6〔z0∈{15,16,17}・
  x=18..159〕**9,372点 bad 0**・PASS（2.9秒・3実行byte-identical
  〔同一cwd2回+隔離1回〕・output/preflight-c1d-y18.json SHA-256 89cb9541…）
  を組み込み前 fail-closed ゲートとして通過後に anchor block を機へ
  in-place 組み込み（機内C1d掃引 x=18..159・R<=x+61 の**136,746点 bad 0**
  ・うち lowR 9,372点）。y=10 prefight がK1087初稿の評価順序バグ170点を
  捕捉した前例どおりゲートは実効した（本族は逐語再転写で初回一致）。

- census第三実装: census_rows.py（SHA-256 1cd71004…・XMIN=18・XMAX=70・
  RBUF=20・ZHI=80・token (x,18)・tail (x+18)%2・LRU cap 1,600,000）が
  census.txt（810,453 bytes・4,240行+空行80・SHA-256 8e239f52…）を生成:
  **443,080点・zero_points 221,548・misses 9,262,827・約18秒**・
  tail assert R>=x+z+19 は全行で成立。C11r（rows==80*53=4,240・
  values range(0,x+z+21)・T/P集合・Thue-Morse index・tail再導出）が
  全行を cand18 から再導出・**bad 0**（重複行・欠落行・rows不一致・
  trailing newline欠落は FAIL-CLOSED）。

- 検証器 part2化: verify_y18_universal.py を part2正本（SHA-256 8ddd0c2f…
  ・52,177 bytes・14チェック）へ in-place 更新。**part1 12チェック本体は
  byte不変**（builderがtoplevel defsを全比較・diffはanchor block・
  check_C1d/check_C11r・STAGE docstring・C1b/C1d/C11r docstring行・
  main() registry/dispatch のみ）。転写検査は part2 bytesでもPASS
  （transcriptions-check-y18.json は part1出版bytesと同一・83c60e89…）。

- フル14チェック監査: **overall PASS・総照合点 6,934,616**（part1 6,354,790+
  C1d 136,746+C11r 443,080）・全bad 0・型523,398・36.1秒/run。
  merge 1,121,822・tail 192,210・C4t clip 37違反1,012 (60,100,100) は
  part1から不変。C11ordered/C11canonical は part2セッションで再実行しても
  part1出版bytesと byte一致。

- 決定性: audit.json（a636c187…）・census.txt（8e239f52…）・
  preflight-c1d-y18.json（89cb9541…）・census両部・転写検査JSON の
  3実行 byte-identical（同一cwd2回+隔離tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random・隔離側は転写検査・preflight・census_rows・
  census両部・フル14チェックをゼロから再生成）。

- fail-closed 8種（スクラッチtreeで実施・全捕捉・各probe後にbaselineを
  build bytesとcmp検証し復元）: census.txt欠落→FAIL-CLOSED「census.txt is
  missing」・行削除→「census rows 4239 != 4240」FAIL-CLOSED・重複行注入→
  「duplicate census row (0,18)」FAIL-CLOSED・P-set改ざん→C11r bad 1・
  T-set改ざん→C11r bad 1・C11r tail反転 (x+18)→(x+19)→**bad 4,240（全行）**
  ・アンカー誤結合 (16,A16u)→(16,A10u)→**C1d bad 1,756**・lowR参照ずれ
  R→R+1→**bad 9,372（全lowR点が独立に識別する事実の記録**・改ざん8種は
  すべてrc=1で捕捉）。

- **K1242 を observed→proved に昇格**（同一K項目・K1240/K1237前例・
  AGENTS.md規約）。マージ命題 x<=z-19 => H == single_token(x+18,z,R) は
  **y=1..18で全称確定**、tail R>=x+z+19 => (x+18) mod 2、clip窓 2y+2=38
  tight は**14族連続**（y=5..18: 12/14/…/36/38）・B子逐語連鎖は
  cand9..cand17 に拡大（証明済みB子は cand10/cand12..cand17）。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべてUNKNOWNのまま。3トークン以上・y>=19族・固定幅・q点版安定化長は
  範囲外。

- 出版: commit A（census.txt 単独・810KB）、commit B（part2正本検証器・
  census_rows.py・preflight・output〔audit/preflight JSON/published_run
  part2版〕・実験README part2追記）、commit C（K1242 proved昇格編集+
  K1244 part2追記+本log）、commit D（knowledge README bullet）。各push直前に
  HEAD再取得し commit message に「Observed HEAD-before-push <sha>」を記載。

- 次のレジューム: y=18 全称は完結。残る高速レーン候補は
  横断法則一般補題化レーン（band下端 2y+2 の帰納構造・seed法則6連続目
  〔cand16→18ふくむ偶y系列〕の構造補題化）。y=19 fit は並走レーンの
  単一オーナー宣言済み（非接触・y=19全称はy=19 fit・出版を待って別宣言）。
