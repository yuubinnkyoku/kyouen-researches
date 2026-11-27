# Three-row q=4, m=26 SAT row-sum partition (P(26) independent second-method cross-check)

単一オーナー宣言 `02307f675`（宣言時 HEAD `07937d7415`・publish-then-execute・
「実行時間が許す限り m=26 以降の増分掃引」条項）の継続実行。
姉妹 kit: `research/experiments/three-row-q4-m25-partition-20261128/`（手法・器材 pin・
較正・split_piece.py の意味論は同一につき本 README では重複記述しない）。

## 主張（有限機械検証の正確な範囲）

1. **P(26) の SAT 行和分割による独立確認**: 3×26・q=4 の行欠損極大 witness の
   非存在を m=24/m=25 と同一の行和 63-triple 分割で掃引し、
   **全63 triple UNSAT・exactly-once 被覆**（`partition_closure_3row.py`・
   decided 63 / pending 0 / uncovered 0 / SAT 0）。P(26) は列挙閉包
   （three-row-q4-enumeration-20261121）で既に確定済みのため、本実行の新規性は
   **P(26) の 2方法化** のみ。**m≥27 の新幅主張はしない。**
2. **決定ピース台帳**（全66件・全 UNSAT・合計 6,538,493 conflicts）:
   - row-k piece 4件: (0,0) 611・(0,1) 75,055・(1,0) 324・(1,1) 82,513。
   - row-sum piece 10件（lex=H）: (0,2,0) 1・(1,2,0) 0・(1,2,1) 890・(2,2,0) 70・
     (2,2,1) 2,866・(2,2,2) 18,195・(3,2,0) 110・(3,2,1) 13,664・(3,2,2) 202,989・
     (2,3,2) 190,769。
   - **(3,2,3) は leftmost-column 26分割で全滅**（合計 2,727,793 conflicts・
     最大片 c07 208,659）。**(2,3,3) も同 26分割で全滅**
     （合計 3,222,643 conflicts・最大片 c07 309,354）。
     分割の意味論・完備健全性は m25 kit の `split_piece.py` と同一
     （ベース片の一体実行は実施せず・分割26片の全 UNSAT で反証）。
   - m=25 との比較: 決定打 (2,3,3) 分割合計は 2,988,508 → 3,222,643（約1.08倍）。
     conflicts の集計和は参考値（非加法）で、UNSAT verdict が反証の本体。
3. **決定性の独立確認**: 代表2件（s233_c07 = 309,354・(2,2,2) = 18,195）の
   再実行で conflicts bit-exact 一致（rc 一致・per-second 表示のみ相違）。
4. **閉包スクリプトの一般化**: `partition_closure_3row.py`（board_tag を引数化・
   m25 台帳を入力として再生成した結果が m25 kit 出版 closure と等価
   〔board_tag/question 以外 byte等価〕を確認済み）。

## 開示

- m=26 CNF メタ (curves 7,258 → m=26 では 8,083・vars/clauses は
  `output/cnf_manifest_m26.txt` 参照) は pinned encoders から決定論的生成。
  較正は m25 kit の (3,23,4) 陽性対照（宣言時開示）を引き継ぎ、本幅では
  追加較正は実施していない（同一 pin 器材・同一符号化の増分適用）。
- 分割片実行は bash 呼び出し cap のため 1回の呼び出しで3-7片を逐次実行
  （タイムアウト 40-70s/片・全片 cap 内で決着・INDET 0）。
- 本レーンは w=3 固定幅で標準 11×11 盤に無関係。**verdict NOT consumed・
  標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN。**

## レジューム（着手前に必ず最新 main 再取得・hourly 並走注意）

1. **m=27**: 分割片が ~2x に漸近（cap 300s に近づく）ため (c1,c2) 対分割への
   拡張が無難。P(27) の2方法化として同じ手順で実行可能。
2. m≥32 は SAT 分割では片当たり数千万 conflicts 見込みで非現実的。
   列挙閉包側の治具拡張（wsearch34.js の m≥32 対応）が本命（K1183 レジューム）。
3. 6x26 四レーン・6x23 sweep・seven-row w70（宣言 5f3fc6901）には不参入。
