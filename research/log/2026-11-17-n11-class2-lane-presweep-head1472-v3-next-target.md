# head-1472 next-target presweep census v3 (2026-11-17)

## 背景

cost64h receipt foldの着地（head 1452→**1472**、commit `828c595c`）とcost66i sweep完走
（9 WIN7-D10 + 57 REFUTED-D10・証明書9枚検証済み・foldは76c待ち）を受け、次ターゲット選定のための
presweep census v3をhead-1472で実行した。v1 census（blob `0d9a94a2`）のhead-1452 bit statusを
baselineとし、v2（blob `67d6a5c1`）の64h/76c overlayを継承・全行で再検証した上で、66i overlayと
着地済み64h fold閉鎖20行を反映した。

## 実行

- 3つのverdict mapをraw batchから再構成（全てblob pin照合済み）:
  64h v16 raw 8本（64 bits・WIN 23）・76c v17 raw 10本（76 bits・WIN {61,99}・bit113はv16→v17反転）・
  **66i v17 raw 9本（66 bits・WIN [19,28,29,58,88,90,99,103,112]・REFUTED 57・capped 0・pilot 9×3402）**。
- 66i winner root canonはclaim v5（blob `c69f512e`）のwinner_roots 9/9と一致をassert。
  3 sweep間のcanon重複Verdictはconflict 0（一致のみ）。
- 着地済み64h fold receipt（blob `1633be29`）のclosed_manifest_rows 20行 == preregの20行をassert。
  head 6数値 `[1472, 174, 6376, 504672, 4649, 368586]` をassert。
- family overlayはv2の全行（3 family・39行）について `bits_in_new_sweeps`/`new_win_bits`/
  `new_refuted_bits` をv2と同一のcounting semantics（bit table status=="open"のみ減算）で完全再現。
- 出力2回実行でbyte-identical（md5 `98825403b1677e02bbb61ec26d98ab44`）。

## 結果: 次ターゲット

- **selected: `00000000000000c09002000000001000`（cost 66・parent `00000000000000403800000008000000`
  ・demand c2=2・legal 66 bits・sweep 64 bits + confirmation 2 bits [20, 97]）**。
  66i childが掃引済みになった後のprimary family（18行/1287出現）最安未掃引行。
- runner-up: `00000000000000801282000040000000`（cost 64・55 open・best-coverable family）。
  同familyの第3行 `00000000000000801202000040000400` はSTERILE（71/71 REFUTED-D10）のため
  depth-10 receiptsでは完全閉鎖不能（K0863）のまま、v2から不変。
- 66i overlayの新規効果: primary family内で `00000000000000801206000000080000`（cost 71）が
  66i bit 53 canon経由でpending 66i closeに（ただし64h bit 100で既に着地済み64h fold閉鎖済み）。
  `00000000000000503800000008000000`（cost 71）も着地済み64h fold閉鎖+66i pending併記。
- STERILE行2行（`000000000200000038000000c0000000`/`...80000020`）は「overlay後open 0」で除外
  （v1 harvest由来の既知REFUTEDで全bit既確定・本censusでは新規掃引不要の再確認）。

## 制限

- censusはsearch-plan bookkeeping。engine search・verdict作成・行の閉鎖は本実行には存在しない。
- solved 1472はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。
- REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/next_target_presweep_head1472_v3_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1472-20261117.json`

## 次の一手

- selected行 `00000000000000c09002000000001000` を**cost-66j**としてclaim → sweep
  （v17 engine・64 engine bits + 2 confirmation bits・depth 10・cap 1e9・andclose 1）。
- 76c bit61証明書抽出・76c foldは並走claim済み（着手禁止）。66i receipt foldは76c着地後に再計算。
