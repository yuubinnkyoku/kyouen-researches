# n11 class2: cost72b bit85証明書によるcost74d foldの証明裏付け

2026-11-15 JST。cost74dの74候補raw sweepと15 receipt foldはmain `392197b7` で完了済み。今回、そのfoldに含まれるbit91 receiptが、独立検証済みのcost72b bit85証明書とD4同値であることを確認し、証明書付き被覆の下限を再計算した。

## D4再利用

- cost72b bit85 root: `00000000002000809102000002000000`
- cost74d bit91 root: `00000000080000809102020000000000`
- D4変換: `(x,y) -> (x,10-y)`（index 5）
- 共通canonical root: `00000000000080811202000020000000`
- 7個のS6親軌道集合は完全一致

cost72b bit85証明書は40,352行、55/55 sub-root PASS、missing/extra 0/0、Git blob SHA `c99ef87964f4770e7dab365ea42ad070b8c6495d`。cost74d bit91のv15照合はloss=true、5,415,122節点。

## 証明書で裏付けられる新規S6軌道

bit85証明書が覆う7親軌道のうち、次の3つはmanifestにあり、cost74d foldの新規16軌道にも含まれる。

1. cost72b child `00000000000000809102000002000000`
2. cost74d child `00000000000000809102020000000000`
3. `00000000000080003800000028000000`

foldの内訳では、bit91 receiptが1と3を新規追加し、bit2 receiptが2を新規追加している。したがってbit85証明書はこの3軌道を独立検証可能な証拠で裏付ける。bit91の証明書を別に抽出する必要はない。

cost74d bit118にも独立検証済み証明書（28,719行・50 sub-root）があるが、fold上のmanifest marginalは0で、新規S6軌道を追加しない。

## frontierの区別

cost74d receipt fold後は解消S6 1,179、残り6,668、残り費用526,075、開いた類の必要S6 4,938、必要費用389,798。これはreceipt frontierであり、全1,179件が証明書付きという意味ではない。

baseline 1,163が証明書付きであることに、bit85証明書が裏付ける新規3軌道を加えると、証明書付き被覆の確認済み下限は **1,166**。残りの新規receipt軌道は、この監査では証拠の帰属を確定していない。

## 並走cost72b laneへの指示

cost72bの13証明書は公開済みだがfoldは未完了。cost74d foldでcost72b childは既にbit91 liftにより閉じているため、**13証明書のfoldはhead 1,179を基準に再実行する**。head1,163からの旧計画を使うとcost72b childを二重計上する。bit85とbit91は同じD4 root軌道なので一度だけ数え、他の12証明書の限界寄与を拡大和集合から再導出する。

K0783の知識索引・生成物検査はこの実行環境では未実施。実験ログと両lane claimを先にmainへ反映した。

成果物:
- [証明書付きfrontier監査JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-bit85-cost74d-certificate-backed-frontier-audit-20261115.json)
- [再現スクリプト](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost72b_bit85_cost74d_certificate_backing_20261115.py)
- [cost74d fold記録](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost74d-receipts-recompute-20261115.json)

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はUNKNOWN。**
