# 2026-11-15：cost-75d receipts fold — 延期されていたfoldをhead 1290へrebaseして完走 — 第二class-2 target S5が13→11行（head 1290→1296）・bit-92 cross-coverが並走77d child行も閉鎖

開始時main: `e789146b`（cost-77c fold後のcanonical head **1290/6557/517923/4827/381646**・77c head JSON blob `7f2badce…`）。

cost-75d（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-75 child `00000000000040801202000000200000`・stones [21,49,57,60,71,78]・需要 c1=0,c2=1,c4=0・単一開lift親・lift石78）は、sweepとWIN7証明書4件（bits 12/40/92/111・239,868行・8,654,219 bytes・242 sub-roots・第二検証3幾何系PASS済み）が公開済みで、receipts foldのみ実行環境outageで延期されていた（[deferral note](2026-11-15-n11-class2-lane-cost75d-fold-deferral-note.md)）。deferral noteは「77a fold着地済みならそのheadへrebase」と規定しており、実際には77a/77b/77cと78aの4 foldが着地したため、**head 1290へrebase**して実施した（deferral noteの1280予測値 parent1 16/1249→15/1174 は古く、1290では 13/1018→11/866）。

## fold scriptの統制（`recompute_frontier_cost75d_receipts_20261115.py`）

1. **baseline再現**: 77c fold scriptをrunpyで再実行しhead 1290/6557/517923/4827/381646と3出力（head JSON `7f2badce…` 10,558 B・ranking `9ada5dfc…` 7,539 B・top-candidates `8d5583e0…` 7,589 B）をbyte-identical assert。fold済みroot **565個**（553+77b 4+77c 8）。
2. **claim検証 + child genuinely remaining**: claim v1の候補75件・child・edge 75・需要 c1=0,c2=1,c4=0と整合。head 1290で第二target S5はchild行（cost 75）を含む**13行/1018**を保持。6削除軌道は互いにdistinctで、開親はlift 78（第二target）のみ、**他5軌道は閉鎖維持**（remF2に不在をassert）。
3. **sweep再導出**: raw batch 1-10から75候補exactly-once・**WIN7-D10 4件 [12,40,92,111]・71 REFUTED-D10・0 capped・総nodes 143,552,593**・pilot 3402×10・v16 determinism rerun（batch5 bits 44/50/51/52/54/55/56/58）node-exact・v15 pinned record（pilot 5949×3・WIN nodes 1,406,438/7,087,163/16,644,786/10,234,430・REFUTEDアンカー bits 0/2/4/6/86 loss=false）と完全一致。
4. **証明書bytes検証**: 4証明書（bit12 1,126,030 B・bit40 1,885,065 B単一ファイル、bit92 2 parts（1,362,476+1,357,271=2,719,747 B）、bit111 3 parts（975,616+974,906+972,855=2,923,377 B））。part join == whole（bytes・md5・split manifestsのwhole_git_blob_sha）・header・root行・rows sorted-unique・BigInt（union 0/0・subroots 55/60/66/61・terminal [13,17]）・Number Bareiss tsverify（union 0/0・subroots一致・terminal [13,15,17]・consumed distinct == rows 31,181/52,198/75,290/81,199）。合計**239,868行・8,654,219 bytes・242 sub-roots**。
5. **root disjointness**: 4新root vs 565 folded roots、raw-hexとD4正準形の両方で disjoint。4新D4軌道は互いにdistinct。
6. **fold（公開順 [12,40,92,111]）**: childは**bit12**（公開順最初）で閉鎖。総marginal **22**・in-manifest marginal **6**（bit12:2・bit40:1・bit92:2・bit111:1）・zero-mimなし。set等式 `s_after == s_1290 ∪ covers(4 roots)` PASS。

## fold結果 — 新canonical head 1296/6551/517468/4821/381191

- solved 1290→1296・unique 6557→6551・sum_remaining_cost 517,923→517,468・open s6 4,827→4,821・open cost 381,646→381,191。
- **第二target S5: 13行/1018 → 11行/866**。喪失2行 = child行 `00000000000040801202000000200000` に加え、**bit-92 receiptのcross-coverがcost-77行 `00000000100000801202000000200000` を閉鎖**。喪失行はすべてcovers(4 roots)内。
- 出力: head JSON（blob `c801e605…`・8,992 B）・ranking CSV（`25b7fc1b…`・7,538 B）・top-candidates CSV（`d6782837…`・7,416 B）。**3回連続実行byte-identical**。claim v2（completed retire・fold recordに3出力blob sha・再現コマンド・deferred/cross-cover注記）をpush済み。completed claim後の再実行でsection 9がfold record・3出力blobを再assert（実行確認済み）。

## 並走cost-77dへの重要な指摘（warm-hygiene必須）

並走laneがhead 1290でIN FLIGHT claim済みのcost-77d sweep（child `00000000100000801202000000200000`）は、**本foldのbit-92 cross-coverで既にhead 1296で閉鎖済み**。77d foldはcost-70gのwarm-hygiene先例に従うこと（child既閉鎖assert・per-receipt marginalは拡張unionから再導出・需要は開lift親から再導出）。77dのsweep自体は無駄にならない（候補列挙・REFUTED-D10・証明書は独立価値を持つ）が、foldのparent簿記はwarm-hygiene統制が必要。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 第二target S5は残り11行で未解決のまま。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`は引き続き **UNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost75d_receipts_20261115.py
```

77c baselineを再実行し、head 1290のbyte-identical再現から4 receiptsをfoldする。実行時間は約3秒。
