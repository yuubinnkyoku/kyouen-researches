# n11 class2: cost69f残り4証明書の第二独立検証

2026-11-15 JST。最新mainのK0783、cost69fの9件統合記録、split certificate 8 part、receipt fold、cost65j/cost69gのinflight claimを確認した。cost69fの4証明書（bits 2/94/109/119）は既に別レーンで公開・検証済みだったため、本レーンでは重複探索をせず、公開Git blobから証明書本体を再取得して第二の検査を行った。

## 第二検査の結果

**4/4 PASS。** 各証明書はpart1+part2を連結し、公開BigInt独立検証器と同じゲーム木検査を別V8実行で再現した。solver、探索器の判定cache、探索結果は読み込んでいない。さらに、根局面の合法手数は別実装の4×4整数行列式（24項の置換展開）で再列挙し、3×3余因子展開の検証器と一致することを確認した。

| bit | 行数 | 根の合法手数 | 訪問局面 | 終局数 | v15 anchor節点 |
|---:|---:|---:|---:|---:|---:|
| 2 | 69,879 | 58 | 142,740 | 22,921 | 16,285,738 |
| 94 | 53,449 | 56 | 120,250 | 20,161 | 15,200,842 |
| 109 | 71,485 | 60 | 153,920 | 26,397 | 13,955,169 |
| 119 | 67,423 | 61 | 143,363 | 23,779 | 13,661,829 |
| **計** | **262,236** | **235** | **560,273** | **93,258** | **59,103,578** |

4件すべてで、rootは7石かつ安全、strategy行は辞書順・重複なし、全sub-root通過、union missing/extra=0/0、終局石数13〜17。別実装の4×4行列式で得た合法手数は58/56/60/61で一致した。

### 内容・保存の照合

- 4件の連結後MD5・SHA256・総byte数は class2-lane-cost69f-win7-certificates-2-20261115.json と完全一致。
- 8個すべてのpartについて、Git blob SHA1を blob <size>\0<content> から再計算し、manifestのblob SHAと一致。
- 各partのbyte数・行数・MD5もmanifestと一致。
- 4 rootのD4正準化した7個の6石親集合を再導出し、frontier foldが新規被覆とした親軌道が実際に各rootの親集合に含まれることを確認。

第二検査の合計は、証明書262,236行・抽出90,446,193節点・検証訪問560,273局面。これらは探索節点と証明書検証局面を区別した値である。

## frontierへの反映

元のreceipt foldは書き換えず、全9 receiptの certified=true を確認した派生出力を作成した。baseline 1,154から1,163へのcost69f増分+9は、これで全て独立検証済み証明書に裏付けられた。

- 解消済みS6 manifest軌道: **1,163**
- 残りS6軌道: 6,684
- 残り七石目費用: 527,280
- open class需要: 4,954軌道 / 391,003費用
- 残りS5軌道: 175
- 最良class2 S5 00000000000000809102000000000000: **7軌道 / 519費用**

bit2証明書が対象S6 child 00000000000000809102000000000008 を証明書レベルで閉じた。ただし親S5は7軌道残っており、まだ閉じていない。frontierの数値は変わらず、証拠の確度がraw-onlyから証明書済みに上がった成果である。

## 並行作業との重複回避

cost69gは別レーンが 00000000000000809102000000002000（費用69、合法候補69）をclaim済みなので、探索を重ねていない。cost65j bit113候補の7石rootはcost69f bit2 rootと同じS6親軌道を1件共有するが、S7のD4軌道は別。bit2が証明済みになったため、将来bit113がWIN7証明書化されても、この親軌道の被覆を二重計上してはならない。cost69g claimではcost65j child自体もcanonical headで既被覆と記載されているため、cost65j作業の再開時には最新frontierで再判定が必要。

## 再現

node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_second_independent_verification_20261115.mjs

- [第二独立検証JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost69f-second-independent-verification-20261115.json)
- [証明書済みfrontier派生JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69f-certificate-backed-recompute-20261115.json)

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続きUNKNOWN。**