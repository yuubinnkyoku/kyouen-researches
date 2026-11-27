# Seven-row q=4, width 70 two-edit extension: single-owner declaration (2026-11-27)

高速レーン・単一オーナー宣言（publish-then-execute）。

- 宣言時 HEAD: `06aa055da4975468788091332e18749a107c92e4` (2026-11-27T18:13:38Z)。
- **対象**: (7,4) 前線幅 70。published 199 基底
  (`seven-row-q4-w69-two-edit-negative-20261127/output/w69/bases.json`, sha256 `d8e977ec…`, byte-clone)
  の **7x70 盤における完全 two-edit 近傍**（≤2 除去・≤2 追加・最終 20 石 rows {3,3,3,3,3,3,2}）を
  fresh mode と holes mode（追加が除去位置を埋め戻すことを許容する上位集合）の両方で完全掃引する。
  併せて D4 鏡像×並進 census (`census_translate.py`, target 70) を再実行し
  出版 census 記録（最大被覆幅 67）を再現する。
- **機械**: `enum_two.js` byte-clone（sha256 `ab58c34a…` = 出版 pin）+ width-70 drivers
  (`sweep70run.js` / `sweep70hrun.js` = 出版 `sweep69run.js`/`sweep69hrun.js` の width 70 適応・
  盤幅と出力 path 以外 byte 同一）。整数幾何のみ。
- **宣言前較正（開示）**: 宣言 push 前に本 host で
  (a) base53 @ 7x57 fresh = 1,436,643 / 60,921 / 2（出版値一致）、
  (b) 出版 w68 witness @ 7x69 fresh = 2,141,205 / 199,290 / 0（出版 stats_69 一致）、
  (c) 陽性対照: 23 w65 基底 @ 7x68 fresh = 3 producer × exactly-1 maximal、
  すべて出版 w68 witness (`witnesses_68.json` sha256 `d031e5b3…`) と石集合一致、
  を確認済み。公式の幅70 掃引・決定性・tamper は本宣言の出版後に実行する。
- **終了条件**: fresh 199/199 と holes 199/199 の両完了。witness 発見時は即時出版し
  M_{7,4} 下界を更新する審査に回す（witness は 7x70 で safe・行欠損・極大であることを
  独立検証器でも確認するまで下界主張しない）。
- **不在主張の界限**: 結果が負でも「7x70 全域で witness 不在」は主張しない
  （two-edit 近傍内のみの局所負）。M_{7,4} ∈ [69,1929] は本レーン単独では不変。
- **並走注意**: 同一 hourly lane の他セッションはこの幅70 two-edit 掃引に着手しないこと。
  6x26 各 class-split lane・three-row m=25・n11 twelfth-cost には触れない。
- 標準 11x11 空盤・二石 root・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
  candidates/safe/maximal 計数は bookkeeping。
