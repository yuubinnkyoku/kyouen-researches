# 単一オーナー継続宣言: 3行 q=4 SAT 行和分割レーン m=29 増分（P(29) の第二方法化）

- 宣言時刻: 2026-11-27T22:45Z（本ファイル出版コミット時）
- 宣言時 HEAD: `2691ac04712bb7d3aaa5a3d87701f9f4dda6bccd`（直前再取得・m29 並走なし確認済み）
- 元宣言: `02307f675f4c3c0d2700ca470b173b4c2310fd54`
  （`research/log/2026-11-28-three-row-q4-m25-partition-single-owner-note.md`・
  「実行時間が許す限り m=26 以降の増分掃引」条項）の m=29 増分。
- 前段: m=26 kit（`525a130d` 系）→ m=27（`65e22558`・出版 `ddbe1392`）→
  m=28（`cfcdffde`・出版 kit `three-row-q4-m28-partition-20261128`）。
  本増分は m=28 kit とのファイル非接触（新規 dir
  `research/experiments/three-row-q4-m29-partition-20261128/`）。
- m≥32 列挙閉包レーン（takeover 宣言 `bb563ada` 系・2026-11-27T20:05Z）とは完全分離。
  SAT 分割では m≥32 の片当たり conflicts が cap を超える見込みで不参入。

## 予定する作業（publish-then-execute・本宣言以降に実行）

1. m=29 の 63-triple 行和分割: row-k piece 4件（sat3・rowY×kex・lex=H / H,V）+
   row-sum piece 12件（sat4・rspec 完全指定・lex=H）のうち (3,2,3)/(2,3,3) の2片は
   leftmost-column 29分割（split_piece.py・欠損行 rowY=1 / rowY=0）で決着。
   全片 UNSAT なら P(29) の SAT 側反証空間全滅。
2. P(29) は列挙閉包（three-row-q4-enumeration-20261121・ext28plus）で既に確定済みのため、
   本実行の新規性は **P(29) の 2方法化** のみ。**m≥30 の新幅主張はしない**
   （実行時間が許せば m=30 を別増分として続行する場合も同一宣言系列の増分として扱う）。
3. verdict は閉包機械検査（partition_closure_3row.py・decided 63 / pending 0 /
   uncovered 0 / SAT 0）で締める。SAT triple が1つでも出た場合は witness を
   sat.js verifyConfig + verify34.py の2系統検証して出版（P(29) 不成立・
   witness band m=4..29 拡大）。
4. INDET 片は honest negative として記録し cap 吊り上げ再実行。全片決着まで
   主張しない。

## 較正（宣言前に実施・開示）

- m=28 base 16 CNF を本環境で再生成し出版 `cnf_manifest_m28.txt` と
  **16/16 md5 byte-exact 一致**。
- pinned kissat 4.0.4（md5 `3a5eba830aa6008a604fcc9bbe99a325`）で m=28 代表3片
  （k_r0_1 = 82,598 / s_2-2-2 = 27,560 / s233_c11 = 318,508）を再実行し
  出版 records・raw_decisions と **3/3 conflicts bit-exact 一致**（全 UNSAT）。

## 器材 pin（m28 kit と同一・本環境で md5 再検証済み）

sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js `282ae832efa0080127c6c153e65e1c3c`・
sat3.js `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js `96a84063f77bb45463ba470f05a06d58`・
verify34.py `7b97ef1ac727b0741847a81d4dea9bc8`・
split_piece.py（m28 kit版）`0a6f6db104ab5bde34154d10c25f0799`・
partition_closure_3row.py（m28 kit版）`0d4d837b0f2724bfb47979cdf16154f8`・
kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`
（sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`）。

## 同一性・不参入

- n11 コスト系・ultra-cheap 系・m≥32 jig レーン・6x26 四レーン・n10 safe-set レーンには
  全て不参入（本レーンは w=3 固定幅で標準盤と無関係）。
- **verdict NOT consumed・標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。**
- push 競合・取得失敗時は無理せず記録して次回へ。
