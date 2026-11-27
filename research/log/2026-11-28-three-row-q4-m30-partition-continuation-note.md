# 単一オーナー継続宣言: 3行 q=4 SAT 行和分割レーン m=30 増分（P(30) の第二方法化）

- 宣言時刻: 2026-11-27T23:40Z（本ファイル出版コミット時）
- 宣言時 HEAD: `314e260f80c3a899cac54a06408a636bc9802675`（直前再取得・m30 並走なし確認済み）
- 元宣言: `02307f675f4c3c0d2700ca470b173b4c2310fd54`（m=26 以降の増分掃引条項）。
  m=29 増分は宣言 `400f7e862c81628f850f8ab599a7b4067dc1076f`（kit 出版 `8240cfb3`・
  K1183 addendum `314e260f`）で完結済み。本増分は m=29 kit とファイル非接触
  （新規 dir `research/experiments/three-row-q4-m30-partition-20261128/`）。
- m≥32 列挙閉包 jig レーン（takeover 宣言 2026-11-27T20:05Z）には不参入。

## 予定する作業（publish-then-execute・本宣言以降に実行）

1. m=30 の 63-triple 行和分割: row-k piece 4件 + row-sum piece 12件
   （(3,2,3)/(2,3,3) は leftmost-column 30分割で決着）。全片 UNSAT なら
   P(30) の SAT 側反証空間全滅。
2. P(30) は列挙閉包（ext28plus）で既に確定済みのため、新規性は
   **P(30) の 2方法化** のみ。**m≥31 の新幅主張はしない。**
3. verdict は partition_closure_3row.py の閉包機械検査で締める。
   SAT triple が出た場合は witness 2系統検証のうえ出版。

## 較正（宣言前に実施・開示）

- m=29 base 16 CNF を本環境で再生成し出版 `cnf_manifest_m29.txt` と
  **16/16 md5 byte-exact 一致**（本 session 中に実施・m29 kit 出版値と同一器材）。
- pinned kissat で m=29 代表2片（s:2,2,2 = 18,695・s233_c12 = 298,432）を
  再実行し出版 raw_decisions と bit-exact 一致（決定性確認として実施済み・開示）。

## 器材 pin（m28/m29 kit と同一・md5 再検証済み）

sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js `282ae832efa0080127c6c153e65e1c3c`・
sat3.js `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js `96a84063f77bb45463ba470f05a06d58`・
split_piece.py（m28 kit版）`0a6f6db104ab5bde34154d10c25f0799`・
partition_closure_3row.py（m28 kit版）`0d4d837b0f2724bfb47979cdf16154f8`・
kissat 4.0.4 linux-amd64 md5 `3a5eba830aa6008a604fcc9bbe99a325`。

## 同一性・不参入

- n11 コスト系・ultra-cheap 系・m≥32 jig レーン・6x26 四レーン・n10 safe-set レーンには不参入。
- **verdict NOT consumed・標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。**
- push 競合・取得失敗時は無理せず記録して次回へ。
