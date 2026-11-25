# 高速レーン実行log: y=16 two-token 全称検証器 part1（2026-11-22）

- 単一オーナー宣言: `2026-11-22-y16-universal-verifier-single-owner-note.md`
  （commit 432664f7・push 2026-11-22T22:49:53Z・宣言時点観測 HEAD 76abc080）。
  対抗宣言チェック: search_commits "single-owner" 直近（Part BB dafe9651・even-y template
  e083ac28・y=16 fit e0fbd99d・いずれも全称段階を含まない）・search_code "verify_y16" 0件・
  proof実験dir不存在を確認してから着手。前回レジューム（K1237 fit + K1238 統一テンプレート）が
  指名した最有力課題「y=16全称」を実行。

- 選定理由: y<=15 は全称確定済み・y=16 fit は observed・clip窓 2y+2=34 の 12族tight判定と
  pin格子統一式・偶y族式系列の y=16 全称データ点が空白で、独立完結かつ昇格レーンとして
  情報価値最大と判断（横断法則一般補題化レーンは本結果を待つ方が収束が速い）。

- 機械: verify_y16_universal.py（part1・12チェック・37,042 bytes・SHA-256 79e21b2d…）を
  scripts/build_verify_y16.py で組み立て（出版 verify_y15_universal.py part2正本
  SHA-256 a39e7ab1…〔cpy commit 0bf18752〕+ 出版 cand16.py〔SHA-256 1fc9d22b…・
  commit 33e1c22e〕の2本をpinned sourceとして実験dir内に同梱）。cand15 B子ブロックは
  y=15正本から Y→Y15 改名のみ（102行・改名を除きbyte照合）・cand16ブロックは出版
  cand16.pyからfit driver省き逐語（92行byte照合）・builder再生成2回byte-identical。
  y=15機からの機械的な族定数変換（x=16合流子 (15,16)≡(16,15)・B子 cand15(z,x,R-1)・
  C子 1 xor cand16(z-1,x,R-1)・census z=0..79 x=16..70 R<=x+z+17〔80*55=4,400行〕・
  merge x<=z-17・tail x+z+17 → (x+16)%2・C7 seed 20261162・C8 x=15行は拡張行のみ）。

- 結果（part1・overall PASS）: 総照合点 **6,331,848・全bad 0**・型 394,686（4点目データ:
  y13 234,180 → y14 281,912 → y15 335,658 → y16 394,686）・merge帰結 1,243,466点・
  tail帰結 193,300点 bad 0・census 442,200点/engine（merge 127,464・tail 4,400）bad 0。
  **C4t: clip 33 違反 1,638・最初 (60,96,96) → clip 2y+2=34 tight・12族連続**
  （最初の違反がband下端と歩く則も y=15 (60,94,94) から +2 で継続）。

- 決定性: audit.json SHA-256 7b5acc8c…・census-ordered fd94dda3…・census-canonical
  3934307f…の3実行byte-identical（同一cwd 2回 + 隔離tree/cwd/HOME +
  PYTHONHASHSEED=random・census部品は隔離側再生成しbyte一致）。
  fail-closed 6件全捕捉（census部品points改ざん・部品欠落・merge corollary bad改ざん・
  box field改ざん→FAIL-CLOSED、Y 16→17→C1 903 bad、Y15 15→16→C1b 777 bad）・復元byte確認。

- 事故の誠実記録: 出版前の初回 C11ordered が 147,972 bad（442,200点中）を自報告。
  原因は census の rawエンジンtupleが族15 (x,15) のまま（builder rename未到達の末尾リテラル）。
  bad分布の族バイアスで診断 → builder count-asserted修正 → byte再生成 → census全面再実行
  bad 0。badバイトは未出版。y=10 preflightのK1087初稿バグ発見と同型の「raw anchorが
  転写slipを捕捉する」事故として published_run.txt・実験README・K item に記録した。
  なお本host（Vibe remote sandbox）は y=15 host よりメモリ制約が強く、
  z=40..79 の unbounded raw掃引はOOM停止 → census は全て bounded twin 経由で
  実行・y=12..y=15 と同一設計の LRU cap 1,600,000。

- 解釈規約（宣言どおり）: part1 は K1237 全称の機械的証拠の構成であり status は
  observed のまま。昇格判定は part2（C1d出版切片アンカー + census_rows.py 第三実装 + C11r・
  同一単一オーナー宣言の継続）で行う。11×11標準盤・二石root・S2・class 1/2/4 は
  UNKNOWNのまま、nodes/照合点数を勝敗として読まない。3トークン以上・y>=17族・
  固定幅・q点版安定化長は非接触。

- 次のレジューム: part2着手（part1着地済み・同宣言継続）。preflight_c1d_y16.py
  （出版 verify_y15 正本からanchor block逐語抽出・y=16行4方照合+z0∈{15,16,17}低R縮約）→
  census_rows.py y16版（XMIN=16・XMAX=70・RBUF=18）→ 検証器14チェック化 →
  3回byte-identical + fail-closed → K1237 observed→proved 昇格・K1239 part2追記。
