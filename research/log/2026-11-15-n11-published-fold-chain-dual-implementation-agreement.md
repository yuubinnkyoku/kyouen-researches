# 2026-11-15: 双実装published fold-chain監査の機械照合(第三script) — 75d/80d両endpointで全統制一致を機械固定・bit-78 root同一性も固定

開始時状況: canonical head **1305/6542/516793/4812/380516**(cost-80d receipts fold・blob `289c9337`)。同日に第一実装(v1系)の80d追従拡張([第一実装v4 log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-first-implementation.md)・AUDIT PASSED)が完了し、published fold-chain全root監査は双実装(v1系v3/v4・v2系v2/v4)が揃った。これまでの双実装一致の主張は両auditの出力数値を人の手で突き合わせた表だったため、**第三の照合scriptで機械固定**した。

## 成果: `audit_dual_implementation_agreement_20261115.py` — AGREEMENT CONFIRMED

4つのpublished audit JSON(blob pin: v3 `9ae57954`・v2 `db0916c0`・v4first `c3df2d1e`・v4second `e3a0b7da`)を再読込し、両endpoint pair(75d: v3 vs v2・80d: v4first vs v4second)で以下を機械assert:

- **cumulative_by_post70e_head**: head列と全per-headフィールド(roots_in_head・new_orbits_added・両累積・own-branch baseline・published own claim・matches_published)が完全一致 — **75d pair 17 heads・80d pair 21 heads**(実装が独立であるにもかかわらず、fork topologyのown-branch計算・document order累積・bit-78重複の扱いまで全行一致)
- **D4 orbit構造**: 75d 569/558/11・80d 587/576/11
- **per-record geometry**: receipt records 434(75d)/464(80d)・group records 40・anomalies 0・hex errata同一(70f 1件)
- **head arithmetic**: 69 heads(75d)/73 heads(80d)・classification counts・quote status counts・anomalies 0・quote errata・pointer-differs全一致
- **canonical line exactly-once**: 75d 1233..1296 mim 63/distinct 63・80d 1233..1305 mim 72/distinct 72・multi 0
- **convention-external receipts**: full record一致(75c cost72_foldの1件・両pair同一)
- **child-closure bookkeeping**: 24 heads(75d)/28 heads(80d)・全record一致
- **base/chain/baseline inventory**: 194 distinct base roots(重複1件のfull record一致)・402 chain distinct・overlap 104・inventory@1233=497
- **endpoint head records**: 75d・80dの全数値record一致(solved・remaining・cost・receipts・child closed bit・blob sha)
- **bit-78 duplicate-root bookkeeping**(80d): root hex `00000000100040801202000000200000`が両実装で同一
- **pins**: base 26・chain 52は等値要求。post70eの差(75d pair: 17 vs 13・80d pair: 21 vs 17)は第一実装のみpinするv2 pin proposals(71c/70f/73g/70g)4件と**正確に一致**することをassert — 監査corpusのendpointは両者同一

出力: [agreement JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-fold-chain-dual-implementation-agreement-20261115.json)(**AGREEMENT CONFIRMED**・2回実行byte-identical・md5 `d8878a85…`・8,900 bytes)。

## 意義

- 双実装一致が人手の表から**機械検証可能な第三script**に固定された。今後のfold着地時に両実装を追従させた後、このscriptのpin差替(+cumulative/endpointの期待値)だけで一致確認が再実行できる。
- 特に75d pairのcumulative 17行の完全一致は今回初めて機械確認された(これまでは80d pairの数値一致が主だった)。
- fork topology(77d lane-local・bit-78重複・merged rebase)という非自明な簿記構造を、独立に書いた2実装が同一に導出していることが全行単位で確認された。

## 解釈境界(重要)

- solved 1305はmanifest被覆の簿記であり、いずの局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。WIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineはhead **1305**。並走laneのcost-82cがIN FLIGHT(`class2-lane-cost82c-inflight-20261115.json`・fold: null・claim時head 1305)でsweep実行中。着地後は(1)両監査実装の82c追従(pins・own_claim・CANONICAL_LINE・ENDPOINT_CHECKS)(2)本照合scriptの拡張(82d pair追加)を同時に実行できる。
- 82c着地の回収は次回実行で行う(claimの`chain_head_at_claim`が1305を指しているため、着地判定は容易)。

詳細: [照合script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_dual_implementation_agreement_20261115.py)、[agreement JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-fold-chain-dual-implementation-agreement-20261115.json)、[第一実装v4 log(同日)](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-first-implementation.md)、[第二実装v4 log(同日)](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-second-independent.md)。
