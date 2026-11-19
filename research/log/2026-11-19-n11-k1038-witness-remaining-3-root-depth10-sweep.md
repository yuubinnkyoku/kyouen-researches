# 2026-11-19 n11 K1038未試験witness残り3 rootのdepth-10判定（K1040）

## 目的

K1039（HEAD 51f47414）でK1038の26-root witnessのうち23 rootを判定した残りの
未試験3 rootを同protocolで判定し、K1038 witness全rootのdepth-10判定を完了させて
witness候補枯渇の情報を確定させる。

## 手順

1. **対象**: K1038
   `refuted-excluded-cover-refold-after-fourth-receipt-20261119.json`
   （HEAD d3a6e69f）の `witness_sweep_plan.untested_witness_roots` 26 rootから
   K1039判定済み23 rootを除いた3 root:
   - `00000000000000403800000008100020`（singleton、被覆1行）
   - `00000000020000801202000100100000`（matched、被覆2行）
   - `00000000000000889002000080100000`（matched、被覆2行）
   K1038 root_checksで全root stones 7・D4 canonical・unsafe_quadruples 0。
2. **engine**: runner v17 `class4_child1_runner_v17.ts`、git blob
   c132cc6425eee3feaeef1d697dd74f968cfedb59、depth 10。
3. **probe driver**（`scripts/probe_driver3.py`）: K1039のprobe_driver28.pyと同一
   protocol。両順序（andclose1/andclose0）・cap 30,000,000均一・resumable・
   各probe直前のpilot_d6制御（loss=false・3,402 nodes）・7石hex assert。
4. **入力pin**: K1038 refold resolve（HEAD d3a6e69f）・K1039 sweep json
   （git blob a4e5d6f8…）・K1039 probe records（git blob 9a1765ef…）・
   K1033 cover resolve（git blob 600b23d3…）。

## 結果

6 probe（3 root×2順序）すべて未打切り、capped 0、順序矛盾 0、pilot_d6 6/6 PASS。

| root | andclose1 nodes | andclose0 nodes | 判定 |
|---|---|---|---|
| `00000000000000403800000008100020` | 254,303 | 565,069 | REFUTED-D10 |
| `00000000020000801202000100100000` | 126,480 | 354,926 | REFUTED-D10 |
| `00000000000000889002000080100000` | 173,945 | 582,210 | REFUTED-D10 |

nodes総計: andclose1 554,728・andclose0 1,502,205（msは観測値としてのみ記録）。

**3 rootすべてREFUTED-D10**（両順序でuncapped loss=false）。

## K1038 witness 26 root合算

K1039（WIN 2〔第5root・第6root、証明書K1036〕・REFUTED 21）と本sweep
（REFUTED 3）の合算で、**K1038 witness 26 root全rootのdepth-10判定が完了**:

- WIN7-D10: 2（いずれも出版証明書つき・foldは未実施）
- REFUTED-D10: 24
- CAPPED: 0

## 構造的帰結

K1038 witness 26 rootの被覆49行のうち、証明書つき2 WIN rootが担う2行
（`00000000000000805202000001000000`・`00000000020000809002000040000000`）を
除く残47行は、この26-root witnessプール内のいかなる7石rootのdepth-10 WIN7
receiptでも閉じられない（候補枯渇の体系的情報であり数学的閉鎖不能証明ではない）。

eligible 60候補のうちwitness外34候補は未試験のまま、プール外候補・depth>10
receiptの可能性は排除しない。次の再解決（resolve2/3）で代替候補評価を行う。

## 解釈上の注意

- REFUTED-D10は7石root単位の判定（そのrootからdepth-10以内に先手勝ちなし、
  cap未到達）であり、それ以前の局面（親行・親parent）のLOSS証明ではない。
- 本sweepはreceipt fold・frontier簿記・再解決を行わない。K1038の簿記
  （frontier 6,226行/492,970・solved 1,622・5親target 23/112・stranded 40）は不変。
- 二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・標準11×11空盤は
  いずれもUNKNOWN。

## 次の接続

1. 第5・第6レシートfold（K1036の2証明書をK1038のfold連鎖にjoin。
   幾何forecastでは2行閉鎖、5親target 25/112）
2. resolve2/3（K1039 REFUTED 23＋本sweep REFUTED 3＋K1038計画42行の代替
   provider評価・stranded/plan-dependent再分類）
3. eligible 60のwitness外34候補の評価方針（depth-10 probeか候補拡張かの
   測定的判断）

主要成果物:
- `research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/output/k1038-witness-remaining-3-root-depth10-sweep-20261119.json`
- `research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/output/k1038-witness-remaining-3-root-depth10-probe-records-20261119.jsonl`
- `research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/scripts/probe_driver3.py`
- アイテム `research/knowledge/items/K1040-n11-k1038-witness-remaining-3-root-depth10-sweep.md`
