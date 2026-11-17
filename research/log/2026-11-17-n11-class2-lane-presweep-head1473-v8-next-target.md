# head-1473 next-target presweep census v8 + cost73l claim (2026-11-17)

## 背景

cost73kのsweep完走・証明書22本の出版・BigInt独立bytes再検証の着地、およびcost76c bit61
receipt foldの着地（canonical head 1472→**1473**、`1473/174/6375/504596/4648/368510`、
fold receipt blob `953beaea`・fold audit blob `de79a3a7`）を受け、次ターゲット選定のための
presweep census v8をhead-1473で実行した。v7（blob `68246f32`）の10 verdict map状態を継承し、
**73k mapを11番目のverdict mapとして追加**した（25 WIN7-D10 + 48 REFUTED-D10・0 capped・
73/73 bit・raw audit blob `85f4f73f`〔第三独立再実行・concurrent recordと73/73 per-bit同一〕
+ claim v3 blob `7f654548` + manifest blob `0892aed0`・22 certificates / 966,535 rows /
155,946,109 extraction nodes / 34,933,538 bytes・3 WIN転送bit 14/26/55は73j bit 110 /
73i bit 110 / 69j bit 110の出版証明書で被覆）。

## 実行

- v8スクリプトはv7の機械拡張（73k完了検査block・73k map・76c fold receipt pin・
  v7 families rowsを正本化して73k分だけ差分計数）。79 source harvest rebuildは
  v1値と完全一致（3,548 canons・353/3,195・conflict 0）。
- 11 map構築: distinct canons 733・内部conflict 0・harvestとのcross-agree 27・矛盾0。
- 全39 family行をbit-exactに再計算し、v7出版値（newly_covered_by_ten_maps・
  open_after_census_v7）を39/39で再現。open_v8 = open_v7 - 73k map新規被覆のみ、を全行で検証。
- 73k行をswept除外・76c行をfold landed（head 1473）として除外表記を更新。
- 出力2回実行でbyte-identical（md5 `d49722012847a649ccbd769a6a7f033f`）。

## 結果: 次ターゲット

- **selected: `00000000000000c09002000000400000`（cost 73・parent
  `00000000000000403800000008000000`・demand c2=2・legal 73 bits・sweep 66 open bits +
  confirmation 7 bits [65, 86, 90, 94, 97, 106, 110]）**。v7 runner-upの行で、73k mapにより
  bit 110が確定（WIN転送）したためopen 67→66。
- confirmationの内訳: 65 = cost69j bit 118・86 = cost72d bit 118・90 = cost76c bit 48・
  94 = cost73i bit 118・97 = pre-64h harvest（以上REFUTED-D10）・**106 = cost73j bit 118
  (WIN7-D10)・110 = cost73k bit 98 (WIN7-D10)**。両WIN転送rootは出版済み証明書で
  被覆済みのため、証明書抽出は新しいWIN bitのみでよい。
- runner-up: `00000000020000003800000088000000`（cost 74・open 69）。

## 制限

- censusはsearch-plan bookkeeping。engine search・verdict作成・行の閉鎖は本実行には存在しない。
- solved 1473はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player win
  （depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1473_v8_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1473-v8-20261117.json`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73l-inflight-20261117.json`（claim v1・2026-11-17T06:30Z時点でmainに同childのclaimなしを確認済み）

## 次の一手

- selected行を**cost-73l**としてsweep（v17 engine・66 engine bits + 7 confirmation bits・
  depth 10・cap 1e9・andclose 1・per-batch pilot_d6 3402）。
- 並走管轄のまま手を出さないもの: 66i receipt fold（head1473 marginal rebase済み・bit19次位）、
  73i証明書の出版。
