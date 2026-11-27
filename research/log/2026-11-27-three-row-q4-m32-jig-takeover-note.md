# 単一オーナー takeover 宣言: 3行 q=4 列挙閉包レーン m≥32 治具拡張（wsearch35 系・停滞レーンの引継ぎ）

- 宣言時刻: 2026-11-27T20:05Z
- 宣言時 HEAD: `751d904671c89854df9801c32b7aa409eb4ea9bf`
- 引継ぎ元: [2026-11-21-three-row-q4-jig-extension-m32-single-owner](2026-11-21-three-row-q4-jig-extension-m32-single-owner.md)
  （宣言 2026-11-21T10:39Z・wsearch35 two-limb + wsearch35b BigInt 二重機構・
  m=32 family 11/12 chunk a*=0 のまま 2026-11-21 以降停滯・**wsearch35.js / wsearch35b.js
  は出版されず工具が喪失**）。
- 前段の成果はすべて出版済み: ext28plus（宣言 `e9c3cd86`）で P(28)..P(31) が列挙閉包で確定・
  witness-free 幅 {24..31}・M_{3,4} ∈ [24, 69]（K1183）。

## 本 takeover の方針

1. **pinned 原版 7 scripts（wsearch34.js md5 `526cf1c3…`・dx34.js md5 `b02235a9…`・
   sat.js md5 `0cc6021a…` ほか）は 1 byte も変更しない**。本 hostで再取得し md5 gate 済み。
2. 引継ぎ元の工具が出版されていないため、**wsearch35.js（(lo,hi) int32 2-limb）と
   wsearch35b.js（BigInt 版）を pinned wsearch34.js から再構築**し、元宣言の検証バッテリーを
   新規環境で最初からやり直す:
   - 計数等価 wsearch35 ≡ wsearch34: m=4..12 × Y∈{0,1,2}（JSON ms 除き同一）
   - stdout 全行 byte 等価（--examples・ms 正規化）で代表 (m,Y) 13件
   - 陽性対照 m=23 Y=0 全域（configs 3,136,441・a2=2・witness 既刊一致）
   - 大域対照 m=28 Y=0 全域（configs 10,732,176・既刊 ext28plus 正本生 raw と計数一致）
   - wsearch35b ≡ wsearch35（m=23 Y=0 全域）
   - hi-limb 二重機構交差検証（m=32）: Y=0 ia[0,300)・ia[4660,4960)・Y=1 ia[1240,1540)・
     Y=2 の1区間（元宣言の残項目を含む4区間）
3. m=32 family 掃引: nSub = C(32,3) = 4,960 を ia 4 chunk〔0,1240)〔1240,2480)〔2480,3720)
   〔3720,4960) で Y∈{0,1,2} 全 12 chunk を本環境で**全て再実行**（元環境の未出版
   11/12 chunk 観測とは独立に、exactly-once 分割・configs 和 = C(32,3)² = 24,601,600/Y・
   集計器による機械検査つき）。
4. dx34 fast path の m≥32 移植版 **dx35.js**（row mask の BigInt 化）を構築し:
   - battery: m=4..12 selftest ≡ dx34 fast（profiles 全件）・m=13..31 の既刊
     dx_sweep 計数列（dx_sweep_28_31.jsonl 52行 + 既刊 24..27 台帳）との一致
   - m=32 fast 13プロファイル掃引（(3,a,b) 置換 12 + (2,2,2)）
5. closure_check.py の m=32 実行（本 host で既に 41/41 closed を確認済み・算術のみ）。
6. P(32) の主張は family 12 chunk 完了 + fast 13 完了 + closure 41/41 が揃った後に限る
   （元宣言の受入条件 4 を継承）。それ以前は observation のみ。
7. K1183 の更新は P(32) が確定した場合のみ（witness-free 幅 {24..32}・残る 33..68 の 36 幅・
   M_{3,4} ∈ [24,69] 不変・P の幅単調性は未証明の明記）。family のみ完了の場合は
   session log に留める（元宣言の受入条件 5 を継承）。
8. 出版は part 分割・各回 fetch-back byte 照合・append-only。他レーンの並走 push とは
   ファイル非接触で運用し、push 競合・取得失敗時は無理せず記録して次回へ。
   実験 dir は `three-row-q4-m32-jig-20261127/`（元宣言では kit 名未出版のため新規）。
9. frontier レーン（SAT・records.jsonl）には接触しない。標準 11×11 空盤・二石root
   {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。
   configs/safe/deep/計数は bookkeeping であって勝敗ではない。

## 判定規約

- 全 12 family chunk と fast 13 プロファイルがすべて witness 0 の場合:
  **P(32)（m=32 witness-free）が列挙閉包で確定**・witness-free 幅 {24..32}。
- いずれかに witness が発見された場合: witness を復号・検証（sat.js verifyConfig +
  独立整数検証）して出版し、witness band m=4..32 に拡大（P(32) 不成立・M_{3,4} ∈ [33,69]）。
- INDET は本レーンには存在しない（完全列挙）。

