# head-1473 next-target presweep census v9 + cost74i claim (2026-11-17)

## 背景

cost73lのsweep完走・証明書32本の出版・BigInt第三実装独立再検証32/32 PASS
（reverification blob `547fe617`・BigInt検証済み証明書population 381）の着地を
受け、次ターゲット選定のためのpresweep census v9をhead-1473で実行した。headは
不変（`1473/174/6375/504596/4648/368510`）。73l receipt foldは66i/66j/69j/
71e/72d/73i/73j/73k foldsに続きpendingのため未着地。v8（blob `2542914e`）の
11 verdict map状態を継承し、**73l mapを12番目のverdict mapとして追加**した
（34 WIN7-D10 + 39 REFUTED-D10・0 capped・raw audit blob `f2ea2044` + claim v3
blob `39cf0f9b` + manifest blob `6e0a94ab`・32 certificates / 1,693,203 rows /
424,657,112 extraction nodes / 61,171,191 bytes・2 WIN転送bit 106/110は73j bit 118 /
73k bit 98の出版証明書で被覆）。

## 実行

- v9スクリプトはv8の機械拡張（73l完了検査block・73l map・BigInt再検証pin・
  v8 families rowsを正本化して73l分だけ差分計数）。79 source harvest rebuildは
  v1値と完全一致（3,548 canons・353/3,195・conflict 0）。
- 12 map構築: distinct canons 800・内部conflict 0・harvestとのcross-agree 28・矛盾0。
- twin計算の修正: v9ではpre-73k twin（v7計数再現用）が73l mapを含まない
  よう、twin除外条件を73k/73l両mapに拡張した（v8では73l mapが存在しなかった
  ため自明に正しかった。これを最初の実行がassertで捕捉した）。
- 全39 family行をbit-exactに再計算し、v8出版値（newly_covered_by_eleven_maps・
  open_after_census_v8）を39/39で再現。open_v9 = open_v8 - 73l map新規被覆のみ、
  を全行で検証。v8 ranking上位9行はすべてv9 top-10に残留（9/9）。
- 73l行をswept除外（34 WIN7-D10 + 39 REFUTED-D10・0 capped・32証明書出版済み・
  BigInt再検証32/32 PASS・receipt fold pending）。
- 出力2回実行でbyte-identical（md5 `025c526b1e3273dee1f34716b2afcc39`）。

## 結果: 次ターゲット

- **selected: `00000000020000003800000088000000`（cost 74・parent
  `00000000020000003800000080000000`・demand {c1:0, c2:1, c4:2}・legal 74 bits・
  sweep 69 open bits + confirmation 5 bits [30, 71, 72, 90, 115]）**。v8 censusの
  runner-up行。73l mapはこの行に新規被覆がないためopen 69は不変。v8 rank-1
  （73l行）のswept除外により繰り上がり。
- confirmationの内訳: 30 = pre-64h harvest（cost73f）・71 = pre-64h harvest
  （cost58b）・90 = pre-64h harvest（cost73f）・115 = pre-64h harvest
  （cost63d + cost74f）・72 = cost71e bit 107。全5 bitともREFUTED-D10のため、
  証明書抽出の対象は新しいWIN bitのみでよい（confirmation batchはcontrols）。
- runner-up: `00000000020000003800020080000000`（cost 75・open 73）。

## 制限

- censusはsearch-plan bookkeeping。engine search・verdict作成・行の閉鎖は本実行
  には存在しない。
- solved 1473はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player
  win（depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1473_v9_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1473-v9-20261117.json`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74i-inflight-20261117.json`（claim v1・2026-11-17 push直前のmain head `b8c76a4d`時点で同childのclaim/raw batch/audit/censusなしを確認済み）

## 次の一手

- selected行を**cost-74i**としてsweep（v17 engine blob `c132cc64`・69 engine
  bits + 5 confirmation bits・depth 10・cap 1e9・andclose 1・per-batch pilot_d6
  3402・fresh engine per bit）。
- 並走管轄のまま手を出さないもの: 66i receipt fold（head1473 marginals・bit19
  次位）、73i証明書の出版、cost73k hybrid seed union measurement、cost73k
  8-way worker split memo merge measurement。
