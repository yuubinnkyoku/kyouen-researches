# 2026-11-28 t>=2 blocking-duality confirmation sweep — single-owner declaration (publish-then-execute)

- Task: K1365 補集合双対性（S 極大安全 ⟺ 補集合 C が t=l−s 重ブロッキングで極小）の
  **t>=2 インスタンス初確認**と、未測定盤の最小 t 重ブロッキング集合の全数・
  極大安全集合のサイズ別個数の新規測定。
  従来の 4 盤確認（K1366/K1367/K1369）はすべて s=l−1（t=1）だった。
- Boards（公開済み board file を使用し、検証器で GF(q) から独立再構成して照合）:
  1. PG(2,3) s=2 → t=2（極大アーク 4:234 は K1300 と交差検査）
  2. PG(2,4) s=3 → t=2（極大 7:360, 9:11,480 は K1355 と交差検査）
  3. AG(2,3) s=2 → t=1（小盤追加）
  4. AG(2,4) s=2 → t=2（極大サイズ 4/6 混在は K1300 と交差検査）
  5. AG(2,5) s=3 → t=2（極大サイズ 9/10/11 は K1357 と交差検査・最小 2 重ブロッキング全数は新規）
  6. PG(2,5) s=4 → t=2（**両側とも新規**・2^31 全列挙）
- Method: 単一 C 列挙器（2^n 全部分集合・両側同一定義で safe/maximal と
  t-fold blocking/minimal を直接判定・要素レベル補集合全単射照合つき）を
  zig 0.13.0（tarball sha256 d45312e6...230ea・repo 既存 pin と同一）で build。
  独立検証は純 Python（GF(q) からの盤独立再構成・board file 一致 assert・
  全 dump mask の safety/maximality/blocking/minimality 再判定・補集合全単射・
  サイズ別個数再導出・C 出力との一致）。
- Pre-declaration calibration (disclosed, 宣言前に実施): t=1 の 4 盤
  AG(2,4) s=3 / PG(2,3) s=3 / PG(2,4) s=4 / AG(2,5) s=4 で本列挙器は出版値
  1,240 / 247 / 10,741 / 36,475 とサイズ別内訳を完全再現（K1367/K1366/K1369/K1364）。
  PG(2,4) s=3 の 11,840 も K1355 出版値と一致済み。
- Execution plan (this declaration の出版後): 6 盤の canonical run（各 2 回・
  byte-identical 出力確認）+ Python 独立検証 + 小盤リストの出版
  （PG(2,5)/AG(2,5) のリストは大きいので counts JSON と sha256 pin のみ出版）。
- Non-claims: 有限全列挙による empirical confirmation と新規計数データの出版であり、
  K1365 の双対性命題そのものは既に証明済み（本作業は証明の再取得ではない）。
  標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
- Declaration-time HEAD: 775e1a6ffde29796511023b7fd2427649316502b
  （直前再取得・t>=2 双対性セルの並走宣言なし確認済み）。
- この宣言は本 session の t>=2 双対性確認スイープの単一オーナー宣言。
  同一セルの並走実行は defer すること。
