# 2026-11-15：cost-70e receipts fold 完成（chain head 1227 → 1233）と baseline 1227 の runpy 非依存再構成

開始時main: cost-69h fold 済みの canonical head `1227/6620/522561/4890/386284`。AGENTS.md、research/knowledge/README.md、cost-70e関連のclaim・manifest・audit、直近の11×11実験・logを確認した。

## 成果1：baseline 1227 の独立再構成（runpy鎖に依存しない純幾何再現）

本セッション冒頭に、runpy実行鎖（1227 headを直接再実行する方法）の代わりに、**52個の公開head JSON**（constants.pyの51 + merged head `294c4ed3`）から各chain rootsを抽出し、`covers()` / `canon()` 純幾何で1227 headを再構成する方式を確立した。

- 402 unique chain roots。staged controls 638/657/665/814 すべてPASS。
- merged CSV（`4eeca6155838169050804eb31a34db4a0681ec05` / `0f9905fcb9190cbbda3b6581466b50373308fe60`）がmain掲載版とbyte-identicalに再生成。
- これにより以後のfoldは「再帰的なrunpy依存」から解放され、入力のgit blob sha照合＋純幾何だけでhead検証が可能になった。

## 成果2：cost-70e 5-receipt fold 完成

`scripts/recompute_frontier_cost70e_receipts_20261115.py`（66,894 bytes、remote blob `df5be7fefce1f28e5798a5903660799575c86b66`）で、cost-70e sweep の証明書付きWIN7-D10 receipts 5件（bits 0/8/24/66/79）を1227 headにfoldした。

**新canonical chain head: `1233/6614/522131/4884/385854`**（`class-frontier-cost70e-receipts-recompute-20261115.json`、remote blob `a0171d4bb839aeb813d231c7d879d6a89452359f`）。

- publication order [0, 8, 24, 66, 79]、total marginal 26 / marginal_in_manifest 6、per-bit marginal 5/5/6/6/4、in-manifest 1/1/2/2/0。**bit0 receiptが子orbit `00000000000000801202000000200004` 本体を閉鎖**。
- parent1 `00000000000000801202000000200000` は 31 rows / 2334 → **28 rows / 2119**、parent2 `00000000000000003800000008400000` は 49 rows / 3625 → **45 rows / 3340**。両open parentからchild行が落ちたことをbit-exactで検証。
- solved 1227 → 1233。hist c2=2,c4=0 は 965 → 959。
- 統制: 117入力ファイルのgit blob sha照合、sweep再導出（70候補、5 WIN7-D10 / 65 REFUTED / 0 capped、nodes 83,656,928、win sum 11,657,011）、det rerun batch5 node-exact、v15 cross-engine anchors（win sum 27,246,682、refuted anchors 75/86/113、pilots 5949×2）、証明書5件のparts-join-whole再検証（md5×sha256×git blob、236,784 rows、280 sub-roots、d4 parent orbits == covers() 7軌道each、BigInt union 0/0）、第三独立audit PASS cross-check、root disjointness（5 roots vs 492既fold roots）、set-equality + reverse-order replay PASS。
- fold後のfrontier: best coverable class-2 は第3target `00000000000000809102000000000000`（2/143）、second は parent1（28/2119）。best class-4 18/1460 不変、audit-blocked 10/698 不変。
- push: script（`a65067e1`）、head JSON（`c6986ee1`）、ranking CSV `33fe27c1e2664ac7644a1eff00df649cb38efe1c`、top-candidates CSV `4561af13ce0dd743051e5f3485ea040438a3d908`（1ファイル409競合したがretryで着地。並走five-row-q7との衝突だった）。

## 成果3：claim v3 retire（blob `9c27cff582e84159aace369b60cfe4543e788bbf`）

`class2-lane-cost70e-inflight-20261115.json` をv2 → v3へ更新した。schema v3、top-level `fold` レコード（chain_head_before/after、publication order、per-bit marginal/in-manifest、child_orbit_closed_by_bit、parents_after、output blob shas、fold script blob）、`win7_certificates.fold` の PENDING テキストを COMPLETED に置換。

## 並走状況

- **cost-65l receipts fold IN FLIGHT**（fold-inflight claim `1e1499a120f75a5967ba238b6e4a3e44826e77bc`）: 2 WIN receipts（bits 21/48）をhead 1227ベースで折ろうとしている並走。65l foldが着地すると1227ベースのforkが発生するため、**次回は78a+69h merged foldと同じmerge/rebaseパターンでhead統合が必要**になる可能性が高い。
- cost-82b・cost-84 sweep はSTERILE（REFUTEDのみ、receiptsなし）。class4-lane cost-86d sweep IN FLIGHT。
- five-row-q7・six-row・A(p)研究などが並走で活発にpush中。push前の最新main再取得と409時のretryを徹底する。

## 勝敗status

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1、class 2、class 4 はすべて **UNKNOWN**。本foldはmanifest被覆のbookkeepingであり、いかなる局面のgame-theoretic valueも確定しない。REFUTED-D10 sweepはWIN7-D10不在のみを証明し、WIN7証明書は個々の7石rootからdepth 10以内の勝ちのみを証明する。
