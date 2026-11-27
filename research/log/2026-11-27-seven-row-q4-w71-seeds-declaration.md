# Seven-row q=4, width 71 + advanced-seed completion: single-owner declaration (2026-11-27)

高速レーン・単一オーナー宣言（publish-then-execute）。

- 宣言時 HEAD: 最新 main（本宣言の直前 commit）。先行レーンの幅70 出版
  (`de598d32` = `seven-row-q4-w70-holes-two-edit-20261127`) と本宣言の閉鎖ノートを確認済み。
- **対象 (frontier breadth 拡大・K0827 追記の次課題)**:
  1. **幅 71 holes two-edit**: published 199 基底 (`seven-row-q4-w69-two-edit-negative-20261127/output/w69/bases.json`,
     sha256 `d8e977ec…`, byte-clone) の 7x71 盤における完全 two-edit 近傍
     (≤2 除去・≤2 追加・追加は除去位置の埋め戻しを許容 = fresh の上位集合・最終 20 石 rows {3,3,3,3,3,3,2})
     を holes mode で完全掃引する。
  2. **advanced-seed 補完**: 199 基底プールに含まれない上位 witness seed 3件
     (w67 witness ×2 = `chain/witness_67.json`・w68 witness ×1 = `output/w68/witnesses_68.json` sha256 `d031e5b3…`) の
     two-edit 近傍を **幅 69/70/71 の各幅で fresh+holes 両 mode** で掃引する。
     (幅 69 fresh は witness-band lane の stats_69 で既に 3/3 記録済み・holes と幅 70/71 は未走査。
     D4 鏡像は盤の x/y 鏡像不変性により dx=0 で暗黙被覆・並進は census が別途扱う。)
- **機械**: `enum_two.js` byte-clone (sha256 `ab58c34a…` = 出版 pin) + width-71 driver
  (`sweep71hrun.js` = 出版 `sweep70hrun.js` の width 71 適応) + seed 補完 driver。整数幾何のみ。
- **宣言前較正（開示）**: 本 host で (a) base53 @ 7x57 fresh = 1,436,643/60,921/2、
  (b) 出版 w68 witness @ 7x69 fresh = 2,141,205/199,290/0 (出版 stats_69 一致)、
  (c) 陽性対照 23 w65 基底 @ 7x68 fresh = 3 producer × exactly-1 すべて出版 w68 witness と一致、
  (d) 幅70 holes 全 199 基底コールド再走 = 出版総計 448,782,213/48,971,845/0 と完全一致
  (先行レーンとの独立再現・本宣言直前の閉鎖ノートに記載)、を確認済み。
  公式の幅71 掃引・seed 補完・決定性・tamper は本宣言の出版後に実行する。
- **終了条件**: 幅71 holes 199/199 + seed 補完 3 seed × 3 幅 × 2 mode = 18 走の完了。
  witness 発見時は独立検証 (安全・行欠損・極大) を通るまで下界主張しない。
- **不在主張の界限**: 負でも幅 69..71 全域の witness 不在は主張しない (既知基底・既知 seed の
  two-edit 近傍内のみの局所負)。M_{7,4} ∈ [69,1929] は本レーン単独では不変。
- **並走注意**: 他セッションはこの幅71+seed 補完掃引に着手しないこと。
- 標準 11x11 空盤・二石 root・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
  candidates/safe/maximal 計数は bookkeeping。
