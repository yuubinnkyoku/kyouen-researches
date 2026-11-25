# 2026-11-16：cost-65n / cost-65o / cost-66c のD4横断監査 — bit83↔bit43の単一重複を独立再導出、cost-65oの残探索を59→58候補へ

開始時main: `b41027e1cebdb391ecb0a02d0911bb8988f12ddf`（cost-66c fold完了・claim v4修正後）。

## 発見

cost-66cの66候補と、並走中のcost-65oの65候補を、別実装のD4正準化で全件突き合わせた。交差は**1軌道だけ**で、cost-66c bit83とcost-65o bit43が一致する。

- 正準形: `00000000000000a09002080080000000`
- cost-66c bit83: raw batch4で `loss=false`、269,856節点、打切りなし。したがってREFUTED-D10。
- cost-65o bit43: 現行claim v1では未転送・未探索候補に残っている。
- cost-66cの7本のWIN7-D10 receipt rootは、cost-65oの65候補と交差0。
- cost-65nの2本のWIN receiptもcost-65o候補と交差0。cost-65nとcost-66cのWIN receipt同士も交差0。

よって現在の証拠から必要なのは、cost-65o bit43を**REFUTED-D10として転送**すること。これでcost-65oは65合法候補のうち既知転送7件、未探索58件となる。既存の8バッチ計画からbit43だけを除くと、バッチ数は維持されサイズは `8/8/7/8/8/8/8/3`。ただしcost-65oは別セッションの予約中なので、このclaim自体は変更していない。既にbit43を実行済みなら冗長な照合記録として残し、WIN7-D10が出た場合は即時に矛盾調査する。

## cost-66c foldの独立整合監査

head 1444から7本のreceiptをfoldした公開結果を、事前登録JSONと投影JSONの双方に照合した。

| 指標 | 結果 |
|---|---:|
| 新規receipt | 7本 |
| receiptの総marginal | 35 |
| manifest内の新規閉鎖行 | 6 |
| manifest外のmarginal | 29 |
| 閉鎖した親行の延べ数 | 8 |
| 影響を受けた親 | 6 |
| 親 incidence 重み付きedge cost減 | 596 |
| 一意な6行のedge cost減 | 449 |

新しい正準headは `1450/174/6398/506297/4671/370211`。S5 orbit数は174のまま、open classが必要とするS6行は6減り、必要edge costは449減った。延べ8 incidenceと一意6行の差2は、同じmanifest行が複数親に属するためである。重複行のedge costは69と78、合計147で、596−147=449が全体の減少量と一致する。

7本それぞれについて、D4正準形と7個の一石除去cover集合を再計算し、事前登録・投影・実foldの三者で照合した。marginal集合は35件すべて相異なり、manifest marginal 6件はfoldの閉鎖行一覧と一致。親ごとの行数・費用差も6親すべて一致した。

## claimの記録修正

cost-66c claim v3では、最上位statusとfold欄は完了を示す一方、`results.row_result` と `results.certificates_status` が「証明書抽出待ち」の旧文言を残していた。claim v4でこの2項目とcross-row注意を現在の状態へ修正し、v3復元用の全変更フィールドを `fold.v3_fields` に保存した。旧v3 blob `6dd3091362dc3d11febd1be020e173fb6df21173` は監査スクリプトでbyte-exact復元を検査する。

## 成果物

- 監査コード: [audit_cost65n_cost65o_cost66c_crossrow_fold_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65n_cost65o_cost66c_crossrow_fold_20261116.py)
- 監査結果: [class2-lane-cost65n-cost65o-cost66c-crossrow-fold-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65n-cost65o-cost66c-crossrow-fold-audit-20261116.json)
- 対象fold: [cost-66c fold log](2026-11-16-n11-class2-lane-cost66c-fold.md)

全入力はGit blob SHAで固定。監査はD4交差・cover集合・fold出力の整合を独立に再計算したが、深さ10探索、11.2MBの証明書本文の再検証、764-root基盤全体の再構築は行っていない（それらは既存fold logの独立検証記録に委ねる）。長時間探索は起動していない。cost-65oのclaimは並走予約中のため変更していない。

## 解釈境界

REFUTED-D10はLOSS証明ではない。個別7石rootのWIN7-D10証明書は、そのrootの勝利だけを証明する。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
