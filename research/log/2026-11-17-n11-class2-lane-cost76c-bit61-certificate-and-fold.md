# 2026-11-17：cost76c bit61の証明書抽出・独立検証・head1472 receipt fold

## 開始時点

開始時のmainは 100f875c748262c5312d73a914d026de4e3e7867。AGENTS.md、research/knowledge/README.md、K0023、K0863、K0865、K0868、cost76c v17 claim・raw sweep audit・corrected marginal・head1472 presweep・cost64h fold receipt/auditを確認した。

cost76cは6石child 00000000010000809002000001000000、76候補のv17 sweepが完了しており、WIN7-D10はbit61/99、bit113はREFUTED-D10。bit61が最初の証明書抽出対象だった。cost64h foldは完了済みで、基準headは 1472/174/6376/504672/4649/368586。bit61の実抽出・独立検証・receipt foldは未完了だった。

## bit61の証明書抽出

7石rootは 0000000001000080b002000001000000。Node v22.16.0、Proxmox CT 203上で1 CPU、nice 10として実行した。

- raw rootの合法な防御手を独立に再計算し、55手の昇順一覧を取得。
- legal_candidates.pyの独立列挙とcert_driver76c.ts内のBareiss列挙が55/55で一致。
- 55/55の各防御手がok=true、capped=false。
- 抽出節点 1,325,278、戦略行 30,042、fbt_drops=0、fatalなし。
- 証明書は1,083,833 bytes。1,200,000-byte分割基準未満のため分割せず保存。
- MD5 6a38f91cb3ec26e5bb7dd4fa937c5e42
- SHA-256 91c69354d5f300a367756ca2dd430bc2f093dea8c0a188e7ee5d8b0b749c0f06
- Git blob SHA-1 374e27eb9a23475b84ec0ca5937d9d98e35a6a71

別プロセスで再抽出し、55手それぞれの節点数・終端範囲・行数が一致し、証明書全体もバイト単位で一致した。再抽出は9,447 ms、初回は9,592 ms。

## 独立検証

### BigInt検証器

- root安全性：PASS、7石、合法防御55手。
- 55/55 subrootを検証。
- 30,042/30,042の勝ち局面行を消費。
- union missing/extra = 0/0。
- 訪問状態 67,865、終端 10,187、相手応手辺 62,162。
- 終端石数範囲 [13,17]。

### Bareiss検証器

- root-check：7石、loser mobility 55。
- 55 subrootすべて検証。
- 訪問状態・終端・相手応手辺の合計がBigInt検証器と完全一致。
- 一時的なconsumed一覧は43,837行、重複除去後30,042行。証明書行集合と完全一致し、missing/extra = 0/0。

consumed一覧そのものは1.4MBの中間データであり、再生成可能なので公開物には含めず、件数と集合一致の検査結果を要約JSONに保存した。再現時はverify_bit7_win7_cert.tsのconsumed-outを指定すれば再生成できる。

## head1472へのreceipt再計算とfold

bit61 rootから7つの6石部分集合を取り、D4正準形を独立計算した。7軌道のうち2つは既存被覆、5つが新規。5つはcost64h foldで閉じた20行のいずれとも重ならない。

新規5軌道のうちmanifestに属する未解決行は 00000000010000809002000001000000 の1行。head1472 presweepでも未解決で、cost76c bit61による閉鎖待ちであることを確認した。

bit61をfoldした後のheadは次のとおり。

| 指標 | fold前 | fold後 |
|---|---:|---:|
| solved S6 manifest rows | 1472 | 1473 |
| remaining S5 orbits | 174 | 174 |
| unique remaining S6 | 6376 | 6375 |
| sum remaining edge cost | 504672 | 504596 |
| S6 demand by open classes | 4649 | 4648 |
| open-class demand cost | 368586 | 368510 |

4つのS5 parentに影響し、parent-row incidenceは6、parent-edge cost deltaは458。いずれのS5 parentも閉じていない。WIN/LOSS矛盾は0。

foldは既存のWIN7-D10証明書に基づく簿記であり、新しい探索判定を作るものではない。56項目の検査がすべてPASSし、生成スクリプトを中間consumed一覧なしで再実行してもmanifest・fold・audit・claimのblob SHAが一致した。

## 公開物

- 証明書ディレクトリ：output/class2-lane-cost76c-certificates/
- manifest：class2-lane-cost76c-win7-certificates-20261117.json
- fold：class-frontier-cost76c-receipts-recompute-20261117.json
- audit：class2-lane-cost76c-fold-audit-20261117.json
- 再現スクリプト：scripts/fold_cost76c_verified_receipt_20261117.py
- claim：class2-lane-cost76c-inflight-20261116.json（v8）
- v7入力snapshot：class2-lane-cost76c-inflight-20261116-v7-snapshot.json

## 解釈上の制限と次の作業

bit61証明書が示すのは、この7石rootで先手が深さ10以内に勝つことだけ。REFUTED-D10はLOSS証明ではない。receipt foldはS6 manifestの1行を閉じたが、S5 parentは一つも閉じていない。

次はcost66iの9証明書をhead1473へ再基準化し、marginalとWIN/LOSS矛盾を再計算してからfoldする。head1452時点のmarginalは再利用しない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべて引き続きUNKNOWN。

