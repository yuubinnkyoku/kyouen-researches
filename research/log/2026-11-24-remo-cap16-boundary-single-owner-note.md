# 単一オーナー宣言 K1307(仮): 3枝REMO決定性の cap≤16 r=3 完全スイープ・定理H16候補 (publish-then-execute)

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは publish-then-execute の単一オーナー宣言。
- 作業: REMO計数ゲーム3枝 profitable-Delta列挙（K0862系 direct_constrained 正準列挙）の cap≤16 境界スイープ。正準プロファイル D_16 = 285,252 個（Burnside: fix_id=1,624,314 / fix_trans=28,770 / fix_cyc=444 / orbits=285,252・既にローカル再現済み）× r=3 の完全決定性計算。K0886（定理H15）が「枝サイズ≥16（16≡1 (mod 3)で未観察剰余での新キー族）」を明示残課題として残した列。定理H16の候補: 新キー族の出現・非出現と剰余類 16≡1 (mod 3) の下での分布。
- 手段: K0886 出版 engine (mask_engine_fast.js, sha256 136ca8809f3b8c2c41ccb82ae0e3687888982dcd2e1548fa8dd79d321a9309fd) を append式チャンク実行で使用。事前探査: D_16 先頭 3,000 プロファイルを 14.97 秒で完了（約 5 ms/件）、全スイープは約 1,425 秒・240 秒以内のチャンク約 6 回で実行可能な規模と判明。packed 形式 [i, sv_mask, fl_mask, states] は行境界分割 (part1ofN..partNofN) で出版。
- 受入条件: sweep 完了後、新検証器が (a) Burnside orbit 計数 285,252 の機械検査、(b) D_15⊂D_16 正準列挙の順序保存部分列性による K0886 出版 r=3 packed レコード 189,864 件（join sha256 7c44da46…・3 part ピン照合）の全件 byte 一致回帰、(c) 定理H15の 110 キー per-key 分割の不変性、(d) 補題FL (first_losers == {C_i mod 3}) 全プロファイル検査・違反 0、(e) センサス（一様決定/一様非決定/mixed）・mixed キー多重集合・γ窓・剰余類別計数の機械抽出、(f) 監査JSON二重生成 byte 同一 + live checks（cap≤7 全域 verbatim、層化サンプル、K0862 witness 再実行）、すべてを満たした場合のみ出版する。
- 既存の検証済み境界列（cap≤15 r=3、cap≤12 r=2..11、cap≤10 の広いr）は再計算しない。branch も PR も作らない。r≥4×枝サイズ13..16・枝サイズ≥17・順位決定性はスコープ外。
- 同一命題への他オーナーの先行宣言は observed HEAD 47dfbb72005aac18fc46f878f3e3c3e43f07285f において確認していない（当日コミット列点検・commit search "cap16" 0 件・knowledge items K13xx 空洞確認済み）。K1306 は SLB/L/E 梯子前線パッケージで別命題・別領域。
- 結果は知識 item に昇格し、research/knowledge/README.md の K0886 bullet 直後に追記する。標準11×11空盤・二石root {49,60}/{59,60}・S2・class 1/2/4 は本レーン非接触で全時点 UNKNOWN・verdict 不消費のまま。