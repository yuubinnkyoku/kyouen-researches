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

- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_cache_exclusion_and_mobility_20261119.mjs
  role: verifier
  note: K0863の全133 child universeに49 rootの全削除子D4 orbitを照合し、BigInt Bareiss/Leibnizで次手数を独立計算する再現器
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json
  role: data
  note: 49 rootのcache非所属、唯一のopen bit74照合、合法次手数47〜77、determinant二方式一致
- path: research/log/2026-11-19-n11-49-root-cache-exclusion-and-mobility.md
  role: log
  note: 完全child-universe非所属証明、分岐数の意味と次の探索判断
- path: research/log/2026-11-19-n11-audit-runner-reproduction-and-ci-repair.md
  role: log
  note: 49-root監査の別環境再現、cost63f証明書監査とCI出力差分の再検査

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


## 2026-11-19 追記: head-1608後の5親joint targetをreceipt-awareに再被覆

head-1410の5親joint target 112行を後続receiptに照合すると、head-1589 global foldが13行、cost78c/79c foldが追加2行を閉じており、未閉鎖は97行だった。候補rootの最大被覆数は2行なので下界は49本。31個の公開subset witnessから得た117候補を既知verdictに照合し、既知REFUTED 5本を除外した残余グラフで最大マッチング48、singleton 1本を構成。これにより残97行の最小候補root coverは**49本（48 pair + 1 singleton）**と確定した。49本すべて7石・D4正準・det4非零を独立再検査し、97行を重複なく被覆する。

この照合で利用した既知verdictはREFUTED-D10 236 root、WIN7-D10 156 root（head1476 cost71e、cost73j、cost78c/79cおよびreceipt foldの明示資料）。候補poolとの交差はREFUTED 5、WIN 0。この時点では8,964件のper-root cache全体とのjoinは未完了だったが、後続の候補側非所属監査で49本すべてが公開engine verdict/115 transferに未該当と確認した（48本は全7削除子のD4 orbitが133 child universeに存在せず、残る1本はbit74がopen）。これはraw 1,064ファイルの再走査ではなく、K0863 scanの完全child universeを使う非所属証明である。49本はなお探索候補でありWIN証明書ではない。詳細は[監査ログ](../../log/2026-11-19-n11-five-parent-residual-49-root-cover.md)、[再現スクリプト](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_five_parent_residual_49_cover_20261119.mjs)、[結果JSON](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json)。標準11×11空盤・二石root・S2・class 1/2/4は引き続き **UNKNOWN**。


## 2026-11-19 追記: 49-root候補の既存verdict非所属と次手分岐数

K0863の8,964 engine verdict（REFUTED-D10 8,305・WIN7-D10 659）と115 transfer（全てREFUTED-D10）を含む133個の6石child universeに対し、49本それぞれの7削除子をD4正準形で照合した。48本は該当child orbitなし。残る1本 `00000000000000909002200080000000` はchild `00000000000000801222000000800000` のbit74に対応するが、engine verdictは0件、transfer bitsは55/65/109のみで、bit74はopen。よって49本すべてがこの公開indexでは未判定である。これはraw 1,064ファイルを再走査した結果ではなく、scan生成器が全claims/sweeps/auditsから構成する133 child universeを使った候補側の完全非所属証明である。

同じ49 rootの合法次手数をdet4で再計算した。BigInt BareissとLeibnizの2方式はroot安全性1,715四点組と候補次手153,988判定で完全一致。次手数は47〜77（平均60.918367・中央値62）。最小47のrootは `00000000000000821082000010800000` で2行を被覆する。49本すべてD4 orbit size 8で、root自身の対称性による枝の併合はない。これは分岐構造の測定であって探索node数・費用ではない。再現資料は[監査ログ](../../log/2026-11-19-n11-49-root-cache-exclusion-and-mobility.md)、[スクリプト](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_cache_exclusion_and_mobility_20261119.mjs)、[結果JSON](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json)。標準11×11空盤・二石root・S2・class 1/2/4は引き続き **UNKNOWN**。
