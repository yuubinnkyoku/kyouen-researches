# head-1473 next-target presweep census v10 (2026-11-17)

## 背景

cost74i sweep完走（**0 WIN7-D10 / 74 REFUTED-D10 / 0 capped**・56,125,895 nodes・
raw audit blob `e5c803ed` + claim v2 blob `d915e120`）の着地を受け、次ターゲット
選定のためのpresweep census v10をhead-1473で実行した。headは不変
（`1473/174/6375/504596/4648/368510`）。74i行は勝ち7手目が1つも存在しなかった
ため、**証明書もreceipt foldも不要のままaudit強度で完全確定**した
（64a以来の全滅行・WIN転送bitなし）。v9（blob `af1d6094`）の12 verdict map状態
を継承し、**74i mapを13番目のverdict mapとして追加**した。

## 実行

- v10スクリプトはv9の機械拡張（74i完了検査block・74i map追加・v9 families rows
  を正本化して74i分だけ差分計数）。79 source harvest rebuildはv1値と完全一致
  （3,548 canons・353/3,195・conflict 0）。
- 13 map構築: distinct canons 873・内部conflict 0・harvestとのcross-agree 32・
  矛盾0。
- twin計算は3本化: pre-73k twin（v7再現・73k/73l/74i除外）・pre-73l twin
  （v8再現・73l/74i除外）・pre-74i twin（v9再現・74i除外）。
- 全39 family行をbit-exactに再計算し、v9出版値
  （newly_covered_by_ten/eleven/twelve_maps・open_after_census_v9）を39/39で
  再現。open_v10 = open_v9 - 74i map新規被覆のみ、を全行で検証。
  v9 ranking上位9行はすべてv10 top-10に残留（9/9）。
- 74i行をswept除外（0 WIN7-D10 + 74 REFUTED-D10・0 capped・証明書/receipt fold
  不要・audit強度で完全確定）。
- 出力2回実行でbyte-identical（md5 `76254925fe71234c57562f58e9cd7185`・
  git blob `fc2509f0`）。
- 2026-11-17 push直前の最新main `e0c13af3`（並走・cost73k測定系の着地）を
  確認。本censusの3成果物・load pinsはすべて無衝突。

## 結果: 次ターゲット

- **selected: `00000000020000003800020080000000`（cost 75・parent
  `00000000020000003800000080000000`・legal 75 bits・sweep 71 open bits +
  confirmation 4 bits [27, 90, 93, 115]）**。v9 censusのrunner-up行。
  74i mapがこの行にbit 27 / 93の2新規被覆を与えたためopen 73 → 71。
  v9 rank-1（74i行）のswept除外により繰り上がり。
- confirmationの内訳: 27 = cost74i bit 27・93 = cost74i bit 93・90 = pre-64h
  harvest・115 = pre-64h harvest。全4 bitともREFUTED-D10のため、証明書抽出の
  対象は新しいWIN bitのみでよい（confirmation batchはcontrols）。
- runner-up: `00000000000000403800000008000008`（cost 78・open 66）。
- 以降のrank: cost 79 open 69 `00000000000000c09002000200000000`、cost 79 open 74
  `00000000020000003800400080000000`、cost 79 open 75
  `00000000020000003800000880000000`。

## 制限

- censusはsearch-plan bookkeeping。engine search・verdict作成・行の閉鎖は本実行
  には存在しない。
- solved 1473はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player
  win（depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1473_v10_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1473-v10-20261117.json`

## 次の一手

- selected行を**cost-75f**としてsweep（v17 engine blob `c132cc64`・71 engine
  bits + 4 confirmation bits・depth 10・cap 1e9・andclose 1・per-batch pilot_d6
  3402・fresh engine per bit）。75ラベルのb/c/d/eは使用済みのためf。
- 並走管轄のまま手を出さないもの: 66i receipt fold（head1473 marginals・bit19
  次位）、73i証明書の出版、cost73k hybrid seed union measurement（claim
  COMPLETED着地済み）・cost73k 8-way worker split memo merge measurementの
  追従作業。
