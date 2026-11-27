# 2026-11-28 3行 q=4 m=25 SAT 分割: P(25) 独立第二方法クロスチェック完結

単一オーナー宣言 `02307f675`（宣言時 HEAD `07937d7415`・publish-then-execute）の実行結果。
kit: `research/experiments/three-row-q4-m25-partition-20261128/`。

## 成果

- **P(25) が SAT 行和分割で独立確認**（全63 triple UNSAT・exactly-once 被覆・
  pending 0 / uncovered 0・closure 機械検査 PASS）。P(25) は列挙閉包
  （three-row-q4-enumeration-20261121・ext28plus 前身）で既に確定済みのため、
  本実行の新規性は **2方法一致**（P(24) と同格）と
  **leftmost-column 分割治具 split_piece.py**（重い row-sum piece を
  cap 内で決着させる完備健全 case-split）の2点。
- 較正: (3,23,4) rowY=1 lexH が SAT 471,357 conflicts bit-exact 再現・
  witness 2系統検証 PASS。
- 重い (3,2,3)/(2,3,3) はベース一体実行が呼び出し境界死滅（開示）したため
  25片分割で決着: (3,2,3) 2,468,531・(2,3,3) 2,988,508 conflicts 合計・25/25 UNSAT。
  全64ピース合計 6,014,667 conflicts。代表2件の再実行で bit-exact 同一。
- 誤主張の排除: **m≥26 の新幅主張はしていない**（P(26)..P(31) は列挙閉包既確定・
  m≥32 は未掃引のまま）。K1183 への追記は P(25) の2方法化のみ。

## 教訓

- nohup バックグラウンド kissat はやはり呼び出し境界で死滅（知識の既知事象を再確認）。
  分割治具で cap 内決着に切り替えるのが正解。
- split_piece.py 初版の body 末尾改行欠落で unit 句が連結され parse error
  （fail-closed・kissat が検出）。修正後全片再生成。
- 分割片の conflicts 和は参考値（非加法）で、UNSAT verdict が反証の本体。

## レジューム

m=26 同一分割掃引が次の一手（P(26) の第二方法化）。m=27 以降は (c1,c2) 対分割が
必要見込み。m≥32 は K1183 の指摘どおり列挙閉包側の治具拡張が本命。
6x26 四レーン・6x23 sweep・seven-row w70（宣言 5f3fc6901）には不参入。
標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
全 closure class は全時点 UNKNOWN（verdict NOT consumed）。
