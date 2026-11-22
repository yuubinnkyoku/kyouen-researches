# 単一オーナー宣言: s_12/s_13 近傍の SAT による両側判定レーン（n=12 k≤10 / n=13 k≤11）

- 宣言日時: 2026-11-22T03:10Z
- 観測 HEAD-before-push: `74f3c4bdcb`（最終取得 2026-11-22T03:10Z・push直前再取得は/74f3c4bd 以降の最新を記録）
- branch / PR: なし（main 直接）

## スコープ（claim 対象）

標準 q=4 共円（正方形 n×n 盤・禁止四点組=共線または共円の4点）の最小極大安全サイズ s_n について、

1. **n=12・at-most-10**: 充足可能なら s_12≤10 の安全極大 witness（新規、K1206 の「s_12≤10 witness は発見できず」を更新）。UNSAT 完了なら s_12=11（K0320/K1206 の s_12≤11 と合わせて精確値）。
2. **n=13・at-most-11**: 充足可能なら s_13≤11 の witness（新規）。UNSAT 完了なら s_13=12（精確値）。
3. **時間制限内に決着しない場合**: honest bounded negative（cap 到達 UNKNOWN）としてのみ記録し、不在・非存在は一切主張しない。

## 使用機材と符号化

- 禁止四点組カタログ: `_s1213-lane-kit/scripts/census.mjs`（K0057 アンカー gate: F_n, D_n, C_n, lines, circles 全一致検証を起動ごとに fail-closed で実施）。
- SAT エンコーダ（本レーンで新規作成）:
  - v1（enc_sat.mjs）: safety 4リテラル節 / t_q 一方向被覆 / Sinz one-way at-most-k。
  - v2（enc_sat2.mjs）: v1 の t_q を z_{q,e} 完全 Tseitin 等価（伝播強化）に置換し、D4 8対称の lex-leader 境界（ hashtable: 7非自明変換× A≤lex g(A)、等号許容）を追加。同等性は実験READMEで証明。
- ソルバ: kissat 4.0.4（`_q66-m24-lane-kit` 出版 pin と同一バイナリ、sha256 実行前に記録）。
-Witness 判定の独立検証: 既刊検証器 verify_witness.py（Python 整数順列 4x4 行列式・空点ごと証人）、verify_witness.mjs（Node BigInt Bareiss・列順序相違）、check_model2.mjs（census カタログ系 State 相当）の3系統+tamper 陰性対照。
- barge 予算: bash 1呼び出し ≒280s 上限のため kissat は1ショット --time=270 前後。累積 resume 不可（honest negative には cap 明記）。

## 受入条件

1. 較正ラダー: 既刊精確値 s_7=7 (K0031) / s_8=8 (K0032) / s_9=9 (K0033) / s_10=10 (K0034) について、k=s_n−1 で UNSAT・k=s_n で SAT が再現されること（コントロールとしてのみ使用し、n≤10 の値主張は更新しない）。完了した UNSAT のみ精確値に寄与する主張に使う。
2. 決定性: CNF は (n,k,shuffle seed) から byte 再現可能（sha256 記録）。kissat 出力は model/v行を含め生ログ保存。SAT witness は2回目の独立した符号化（--shuffle=異種子）でも充足的に再導出可能であることが望ましい（UNSAT の場合は shuffle 版との2ショット一致を必須とする）。
3. SAT witness の検証: 3系統検証 + 最大性 tamper対照（石移動/除去で FAIL）。
4. 値更新は下界または上界の片側のみに留め、K 項目・CSV 更新は repo 先例に従う。
5. 誤り検出時は本章の訂正コミットとして明記する。

## 非目標（non-goals）

- **n=11 は全面非接触**（s_11 は K0312/a45a626d レーン所有・8≤s_11≤10 の決定はそちら）。
- n≤10 の s_n 値は既刊精確値の再現確認のみで、いかなる新主張もしない。
- 決着しなかった場合の不在主張、mother群の s_14/s_15 への拡張、11×11 空盤・二石 root・S2・class 1/2/4 はすべて本レーン非接触。
- mwq_stabilization.csv には触れない（s_n は別集計）。

## 並走との disjointness 確認（宣言時点）

- `b1afb181aa` 6x32 t2 resume scan・`29c44cc53a` (6,5) 6x33 band extension（双方、six-row 系の占有）: path 無衝突、本レーンは w,q 直交族の band に触れない。
- `66e7033b6e` 七行/八行 census+surgery: K1218 (7,4) w65-01 として着岸済み・8行側が継続していても本レーンと無関係。
- n11 系（closure class 16757/23963, central-reply refresh, IF-ADOPTED, sixth-cost 等）: n=11 盤面を扱うため本レーンの n=12/13 と無関係。
- 既刊 s_12/s_13 lane（`593a567a` / K1206）: 完了済み。本レーンは K1206 が「本レーンの非目標」と明示した UNSAT 側を SAT 機材で試みるもの。

## この宣言のスコープ内で実行する成果物の置き場所

- 実験: `research/experiments/s12-s13-sat-stabilization-20261122/`（README・scripts〔enc_sat.mjs, enc_sat2.mjs, check_model*.mjs, decode_model.mjs, census.mjs 出典明記〕・meta・生ログ・CNF は sha256 のみ刊行〔決定的再生成可〕）
- ログ: `research/log/2026-11-22-s12-s13-sat-stabilization-session-log.md`
- K 項目: 決着した claim がある場合のみ作成（1実験1Kを作らない規約に従い、s_12側とs_13側は同一の K に統合してよい）
