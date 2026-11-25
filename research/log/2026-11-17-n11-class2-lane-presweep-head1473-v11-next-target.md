# head-1473 next-target presweep census v11 (2026-11-17)

## 背景

cost75f sweep完走（**0 WIN7-D10 / 75 REFUTED-D10 / 0 capped**・76,432,898 nodes・
raw audit blob `0951327a` + claim v2 blob `6df1e54d`）の着地を受け、次ターゲット
選定のためのpresweep census v11をhead-1473で実行した。headは不変
（`1473/174/6375/504596/4648/368510`）。75f行は勝ち7手目が1つも存在しなかった
ため、**証明書もreceipt foldも不要のままaudit強度で完全確定**した
（74iに続き**2行連続の全滅行**）。v10（blob `fc2509f0`）の13 verdict map状態
を継承し、**75f mapを14番目のverdict mapとして追加**した。

## 実行

- v11スクリプトはv10の機械拡張（75f完了検査block・75f map追加・v10 families rows
  を正本化して75f分だけ差分計数）。79 source harvest rebuildはv1値と完全一致
  （3,548 canons・353/3,195・conflict 0）。
- 14 map構築: distinct canons 946・内部conflict 0・harvestとのcross-agree 34・
  矛盾0。
- twin計算は4本化: pre-73k twin（v7再現・73k/73l/74i/75f除外）・pre-73l twin
  （v8再現・73l/74i/75f除外）・pre-74i twin（v9再現・74i/75f除外）・pre-75f
  twin（v10再現・75f除外）。
- 全39 family行をbit-exactに再計算し、v10出版値
  （newly_covered_by_ten/eleven/twelve/thirteen_maps・open_after_census_v10）を
  39/39で再現。open_v11 = open_v10 - 75f map新規被覆のみ、を全行で検証。
  v10 ranking上位9行はすべてv11 top-10に残留（9/9）。
- 75f行をswept除外（0 WIN7-D10 + 75 REFUTED-D10・0 capped・証明書/receipt fold
  不要・audit強度で完全確定）。75fの4 confirmation転送（bits 27/90/93/115）は
  すべてcanon等価検証済み（bit 27 = cost74i bit 41 raw-identical）。
- 出力2回実行でbyte-identical（md5 `78a38f441c059d0c96d2ecd6ae4d2748`・
  git blob `1e2b6a2b`・77,869 bytes）。
- 2026-11-17 push直前の最新main `2ead47be`（並走・cost73k worker-split memoの
  docs着地）を確認。73i証明書はv11計算時点でもmain未出版を再確認、新規の
  receipt fold着地なし（head 1473不変）。本censusの3成果物は無衝突。

## 結果: 次ターゲット

- **selected: `00000000000000403800000008000008`（cost 78・parent
  `00000000000000403800000008000000`・legal 78 bits・sweep 66 open bits +
  confirmation 12 bits [5, 13, 14, 20, 34, 46, 97, 103, 108, 110, 115, 118]）**。
  v10 censusのrunner-up行。75f mapはこの行に新規被覆を与えないためopen 66不変。
  74i/75f両swept行の除外により繰り上がり。
- confirmationの内訳: 5 = cost69j・13/115 = pre-64h harvest・14 = cost72d・
  20 = cost64h・34 = cost73j・46 = cost73i・97 = cost71e・103 = cost66i・
  108 = cost66j・110 = cost73k・118 = cost73l。全12 bitともREFUTED-D10のため、
  証明書抽出の対象は新しいWIN bitのみでよい（confirmation batchはcontrols）。
- runner-up: `00000000000000c09002000200000000`（cost 79・open 69）。
- 以降のrank: cost 79 open 72 `00000000020000003800400080000000`、cost 79
  open 74 `00000000020000003800000880000000`、cost 80 open 72
  `00000000020000003800000180000000`。

## 制限

- censusはsearch-plan bookkeeping。engine search・verdict作成・行の閉鎖は本実行
  には存在しない。
- solved 1473はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player
  win（depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1473_v11_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1473-v11-20261117.json`

## 次の一手

- selected行を**cost-78c**としてsweep（v17 engine blob `c132cc64`・66 engine
  bits + 12 confirmation bits・depth 10・cap 1e9・andclose 1・per-batch pilot_d6
  3402・fresh engine per bit）。78ラベルのa/bは使用済み（class2-lane 78a・
  class4-lane 78b）のためc。
- 並走管轄のまま手を出さないもの: 66i receipt fold、73i証明書の出版、
  cost73k測定系（worker-split memo・hybrid seed union）の追従作業。
