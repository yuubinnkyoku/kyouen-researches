# 2026-11-19 n11 head-1410 28-root witnessの全面depth-10判定（K1039）

## 目的

K1033のcover resolveが選定した28-root witness（53行）の全rootをrunner v17で
両AND順序・cap 30M均一で完全判定し、同日のK1038 refold（出版HEAD d3a6e69f）が
残した未試験witness 26 rootの実質解消を図る。

## 手順

1. **pinned入力**（全てmain出版blobをsha1 pin、`/home/user/work/repofetch/`）:
   - coverResolve 600b23d39888ea0e693742da4b2ae937a9faf0（K1033実験、witness 28 rootと53行の選定）
   - sweep48 37aba599d0b69275225bf231d56cb18feed14090（48-root sweep、旧簿記）
   - k1035_probes 9cfb5c9c5d8d857b46bd147a68f9795d0a3c59b1（先行3候補判定とroot C証明書）
2. **engine**: runner v17 `class4_child1_runner_v17.ts`、git blob
   c132cc6425eee3feaeef1d697dd74f968cfedb59、depth 10。
3. **probe driver**（`scripts/probe_driver28.py`）: 28 root全てにinline Witness、
   各root×両順序（andclose1/andclose0）・cap 30,000,000均一・resumable。
   各probe直前にpilot_d6制御（root Cにd6誤りを注入、正解 loss=false・3,402 nodes）
   を実行しengine健全性を各レコードに記録。安全root assertつき。
4. **両順序の意味**: 同じrootをAND節のclose順序だけ変えて2回探索し、
   WIN/REFUTEDが順序で反転しないことを全rootで確認。
5. **K1038突き合わせ**: K1038の
   `refuted-excluded-cover-refold-after-fourth-receipt-20261119.json`
   （blob は K1038 実験dir）の `witness_sweep_plan.untested_witness_roots`
   26 rootと本sweepの28 rootをhex左ゼロ正規化（lstrip('0')）で比較
   （K1038側の表現は先頭ゼロ埋め長が異なるため）。

## 結果

56 probe（28 root×2順序）すべて未打切り、capped 0、順序矛盾 0。総nodesは
andclose1=47,142,180・andclose0=120,224,379（msは観測値としてのみ記録）。

判定（classification_rule: 両順序でuncapped loss=true → WIN7-D10、
両順序でuncapped loss=false → REFUTED-D10）:

- **WIN7-D10: 3** root（いずれも証明書出版済み・root HexとSHA-256で一致）
  - `00000000000000801202060001000000`（root C、K1035）
  - `00000000000000805202080001000000`（第5root、K1036）
  - `00000000040000801202000080100000`（第6root、K1036）
- **REFUTED-D10: 25** root（うち2 rootはK1035の先行判定の再現、23 rootが新規除外）
- **CAPPED: 0**

## 決定性アンカー照合

| アンカー | 今回の値 |
|---|---|
| root C andclose1/andclose0 nodes | 3,294,339 / 3,953,563（K1035出版値） |
| `00000000000000003800000008001021` andclose1 nodes | 926,192（K1035 probe_runs） |
| `00000000020000801222000000100000` andclose1 nodes | 261,501（K1035 probe_runs） |

（cap 30Mは後者2rootの非cap要件を満たすため uncapped として同一判定。）

## 構造的帰結

### K1033簿記に対して

28-root witnessの53行のうち、証明書つき3 WIN rootがcover主張で構造的に宣言する行は
ユニーク4行。残49行はこの28-rootプール内のどの7石rootのdepth-10 WIN7 receiptでも
閉じられない（候補枯渇の体系的情報であり、数学的閉鎖不能証明ではない）。

### K1038 refold witnessに対して（出版後の突き合わせ）

K1038（12:13出版・HEAD d3a6e69f）のrefold resolveはfold前簿記
（5親target 23/112・残余89行・eligible 60候補）に基づき26 rootの
未試験witnessを選定した。hex左ゼロ正規化で突き合わせた結果:

- **26 root中23 rootが本sweepで判定済み**:
  - WIN 2（第5・第6root、証明書つき・foldは未実施）
  - REFUTED 21（eligibleプール内候補としての除外確定）
- **未試験残りは3 rootのみ**:
  `00000000000000403800000008100020`（singleton 1行）・
  `00000000020000801202000100100000`（matched 2行）・
  `00000000000000889002000080100000`（matched 2行）の計画被覆5行。
- 21 REFUTED rootがK1038計画で被覆する予定だった42行（2行×21）は本プール内の
  providerを失う。行ごとの代替eligible候補の評価は未実施で、次回の再解決
  （resolve3）で処理する。K1033の53行judgeと同様、これは候補枯渇の情報であって
  数学的閉鎖不能証明ではない。
- plan-dependent行 `00000000000040809002000000100000` のeligible provider 2件の
  うち `00000000000040889002000000100000` を本sweepがREFUTED-D10で除外した
  （残るprovider `00000010000000801202040000000400` は未試験）。
- 本項ではreceipt fold・frontier簿記・再解決を実施しない。K1038の簿記
  （frontier 6,226行/492,970・solved 1,622・5親target 23/112・stranded 40）は不変。

なお、突き合わせに際しK1038側のroot表現は本sweepの32-hex表現と先頭ゼロの
長さが異なる場合があるため lstrip('0') 正規化で比較した
（例: 本sweep `0000000a000000003800000008100000`＝K1038
`0000000000a000000003800000008100000`）。

## 解釈上の注意

- REFUTED-D10は7石root単位の判定（そのrootからdepth-10以内に先手勝ちなし、cap未到達）で
  あり、それ以前の局面のLOSS証明ではない。
- 二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・標準11×11空盤はいずれもUNKNOWN。

## 次の接続

1. 第5・第6レシートfold（K1036の2証明書をK1038のfold連鎖にjoin。
   幾何forecastでは 00000000000000805202000001000000 と
   00000000020000809002000040000000 の各1行、5親target 25/112）
2. resolve3（本sweepの21 REFUTED＋2件のwitness外REFUTED（00000000000040889002000000100000・00000000010000809003000080000000）を反映した再解決。
   42行の代替provider評価とstranded/plan-dependent再分類を含む）
3. 未試験3 root（5行）のdepth-10 probe

主要成果物:
- `research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-sweep-20261119.json`
- `research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-probe-records-20261119.jsonl`
- `research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/scripts/probe_driver28.py`
- アイテム `research/knowledge/items/K1039-n11-witness-28-root-full-depth10-sweep.md`
