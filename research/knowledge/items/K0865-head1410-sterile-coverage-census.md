---
id: K0865
title: "head-1410 receipt-unclosability census — 174 個の open S5 parent 全数の STERILE 被覆分類（3 parent が残行すべて STERILE で D10 receipt 閉鎖不能・57 partial・orbit-level join）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases: [head1410 sterile-coverage census, receipt-unclosability census]
relations:
- type: depends_on
  target: K0863
  note: 閉鎖不能分類は K0863（STERILE 行は自前行からの depth-10 WIN7 receipt を持たない）の適用
- type: depends_on
  target: K0783
  note: manifest・receipt の簿記規約
artifacts:
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json
  role: data
  note: 174 parent 全数の census。コントロール CA〜CI と sha256 入力 pin を含む
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/cover-precheck-70j-vs-62b-20261116.json
  role: data
  note: 完了済み 62b child からの 70j 行 cover set {21,109} の独立再導出
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/report.md
  role: log
  note: census の方法・結果・検証境界
scope: "2026-11-16に算出した n11 class-lane の post-cost-60c 正準 head 1410 に対する履歴スナップショット（174 open S5 parent、MS5 S6 manifest 7867 行・orbit 重複なし、35 STERILE 行）。cost-65j fold は後続作業として head 1410 から 1419 へ適用済みであり、本 census の基準 head は 1410 のまま。"
evidence: "orbit-level census: 全 174×7867 ペアで ∃σ∈D4: σ(P) ⊂ R を判定。コントロール: CA manifest 7867 行・cost 総和 615497・orbit 重複なし、CB 174 S5 canon 重複なし、CC cost-60c fold の parent-row 6 ペア全件 orbit-related、CD 62b 行の出版 claim 記載 parent が census の open parents に全件含まれ demand {c1:1,c2:1,c4:0} も完全一致、CE 既知 anchor 3 件（rem 3/209・10/698・18/1460）が出版値と精密一致、CF 違反 0、CG pending-65j 34 orbit が STERILE と非交差、CI cover precheck bits {21,109}・62 合法手 bit 集合・両 cover root hex が出版 claim v2 と一致"
---

## 主張

head-1410 の 174 個の open S5 parent のうち、

- 00000000000000801202000000200000（class 2, rem 3, cost 209; 残行 = 65k/70j/74h 行）
- 00000000000000809082000000000000（class 3, rem 10, cost 698）
- 00000000020000003800000080000000（class 4, rem 18, cost 1460）

の 3 parent は、残存するすべての S6 行が STERILE である。よって K0863 により、これらの parent は自前行のどの D10 WIN7 receipt によっても閉じられない（receipt-unclosable）。さらに 57 parent が部分 STERILE（effRem = rem − STERILE refs > 0）で、残存行参照 12274 個のうち 91 個（0.74%）が実効的に閉鎖不能、effRem 合計は 12183 である。

## 補足

- S5 parent と S6 行の関連は D4 orbit レベルで判定する必要がある（raw hex subset join では 65k/74h 行の class-1 demand が出版値と不一致になる）。cost-60c fold の parent-row 6 ペア全件が orbit-related であることで検証した。
- 完了済み cost-62b child（STERILE, 62/62 REFUTED-D10）からの 70j 行の cover set は bit 21 と bit 109 のみで、両方 REFUTED-D10。出版 claim v2 の記述（合法手 bit 集合・cover root hex・demand）と独立に完全一致する。
- head 1410 時点の pending 65j fold は 54 個の行参照に効くが、単独で閉じる parent は存在しない。後続の cost-65j fold は head 1419 へ9行を閉じた。

## 境界

STERILE は「その行自身からの D10 WIN7 receipt では閉じられない」ことであり、その局面の LOSS 証明ではない。receipt-unclosable も勝敗の判定ではなく、cross-cover（隣接 child 経由）や depth 10 を超える証拠の可能性は残る。solved head 1410 は manifest 被覆の簿記である。11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
