# n11 head-1410 receipt-unclosability census（2026-11-16）

## 目的

head-1410（cost-60c fold 後の正準 head）で残る 174 個の open S5 parent それぞれについて、残存 S6 行のうち何個が STERILE（K0863: D10 receipt では閉鎖不能）かを D4 orbit レベルで全数調査し、coordinator の実効ワークリスト（effRem = rem − STERILE refs）を作る。あわせて、完了済み cost-62b child から open 70j 行への cover set を独立再導出する。

## 方法

- 入力: MS5 S6 manifest part1〜6（7867 行）、open S5 ranking CSV（174 行）、theorem-applicability scan（STERILE 35 行）、cost-60c recompute、65j marginals、cost-62b claim v2。sha256 pin は census JSON の inputs 欄。
- サンドボックス内 JavaScript による独立再導出。D4 正準化（8 変換、4×32bit word mask）、Bareiss 4×4 による legality（整数厳密）、orbit レベル relatedness（∃σ∈D4: σ(P) ⊂ R）。engine 不使用、浮動小数点演算なし。
- S5↔S6 行の親子関係は D4 orbit レベルで判定する。raw hex subset join では 65k/74h 行の class-1 demand が出版値と不一致になるため、orbit join が正しい semantic であると特定した。60c fold の lost_rows_per_parent 6 ペア全件が orbit-related であることで検証（control CC）。
- 計算は2段階（census 段階が sha256 pin 付き digest を書き出し、出版段階が cover precheck を再導出して digest と照合）。python 再現は bash 利用可能な環境が復旧した後に実施する。

## 結果

- unclosable（残行すべて STERILE）: 3 parent。
  - 00000000000000801202000000200000 (class 2, rem 3, cost 209; rows 00000000020000801202000000200000:65, 00000000000000801282000000200000:70, 00000000000000889002000000000800:74)
  - 00000000000000809082000000000000 (class 3, rem 10, cost 698; rows 00000000000000809082000000020000:65, 00000000000000809082000004000000:66, 00000000000000809082000020000000:66, 00000000000000809082000000400000:69, 000000000000008090c2000000000000:69, 00000000000000809082000000000001:70, 00000000000000809082000000000040:73, 00000000000000809082000000000080:73, 00000000000000809082000200000000:73, 00000000000000809082000100000000:74)
  - 00000000020000003800000080000000 (class 4, rem 18, cost 1460; rows 000000000200000038000000c0000000:73, 00000000020000003800000080000020:74, 00000000020000003800000088000000:74, 00000000020000003800020080000000:75, 00000000020000003800000880000000:79, 00000000020000003800400080000000:79, 00000000020000003800000180000000:80, 00000000020000003800200080000000:80, 00000000020000003800000080008000:81, 00000000020000003800000080000800:82, 00000000020000003800000090000000:82, 00000000020000003800000080000400:84, 00000000020000003800000080000100:86, 00000000020000003800000080004000:86, 00000000020000003800000280000000:86, 00000000020000003800100080000000:86, 00000000020000003840000080000000:86, 00000000020000003800000080000004:87)
  これらは K0863 により、自前行の D10 WIN7 receipt では一切閉じられない。cross-cover か depth 10 を超える証拠が必要。
- partial: 57 parent。実効トップは 00000000000000801202000040000000（class 2, rem 5 − 2 = effRem 3, effCost 229; STERILE 済み行 cost 64/71）。
- 計: 残存行参照 12274 のうち 91 が STERILE 参照（0.74%）、実効 effRem 合計 12183。
- pending 65j fold は 54 参照に効く。単独で閉じる parent はない。
- 70j cover precheck: 62b child の 62 合法手（bit 集合が出版 claim の legal_candidates と完全一致）のうち 70j 行を cover するのは bit 21 と bit 109 のみで、両方 REFUTED-D10（cover root hex も出版 claim 記載と一致する独立再導出）。
- 62b 行の census-derived demand {c1:1, c2:1, c4:0} が出版 claim v2 の demand と完全一致した。

## 検証コントロール

- CA: manifest 7867 行、cost 総和 615497、D4 canon 重複なし（7867/7867）。
- CB: open S5 174、canon 重複なし。
- CC: 60c fold の lost_rows_per_parent 6 ペアすべて orbit-related ✓（semantic 検証）。
- CD: 62b 行について、出版 claim が挙げる S5 parent は census の open parents に全件含まれ、demand も完全一致。
- CE: 既知 anchor 3 件（rem 3/209・10/698・18/1460）が出版値と精密一致（sterileCost == remCost）。
- CF: sterile_refs > rem 違反 0。CG: pending 65j 34 orbit、STERILE との重複なし。
- CI: 62b/70j の合法手数 62/70 が scan と一致、cover bits {21,109} が出版値と一致。

## 解釈上の注意

- STERILE は「自前行の D10 WIN7 receipt では閉じられない」ことであり、その局面の LOSS 証明ではない。
- receipt-unclosable は「D10 receipt 体系で閉鎖不能」であって勝敗の判定ではない。cross-cover や depth > 10 の証拠の可能性は残る。
- 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN。
