# n11 class2-lane presweep census v12: 78c行swept化と次ターゲット選定 (2026-11-18)

## 背景

cost78c sweep完了（11 WIN7-D10 / 67 REFUTED-D10 / 0 capped）と全11証明書の出版
（manifest blob `b7fe519e`・claim v4→v5）を受け、head-1473 presweep censusを
v11からv12に更新した。v12はpresweep-1473 bandで初の「WIN付きswept行」を
overlayに取り込む。

## 実行

- スクリプト: `scripts/next_target_presweep_head1473_v12_20261118.py`
  （v11スクリプト blob `afcbe2c8` を基盤に、78c audit / claim v5 /
  batches-1-6 audit / certificate manifest の4入力を追加し、15番目のverdict map
  `cost78c` を構築）。
- 79-source harvest再構築（3,548 canons / win 353 / refuted 3,195 / 0 conflict）は
  v1 censusとbit-exact一致。15 map構築は1,014 distinct canons・内部conflict 0・
  harvestとのcross-agree 36。
- 39 family行を再計算し、v11のpublished counts
  （`newly_covered_by_ten/eleven/twelve/thirteen/fourteen_maps`・
  `open_after_census_v11`）を39/39で再現。差分は78c map由来のみ
  （`open_v12 = open_v11 - 78c新規cover` が39/39で成立）。
- ローカルでcensus v11（blob `afcbe2c8`）をbyte-exact再現できた環境で実行。
  v12出力は再実行でbyte-identical（md5 `8532ec0c…`）。

## 結果

- 78c行（`00000000000000403800000008000008`）をswept扱いのexcluded行として
  記録（open 0・known 78・newly_covered 76）。receipt foldは
  66i/66j/69j/71e/72d/73i/73j/73k/73l fold完了後に実施。
- 次ターゲット: **`00000000000000c09002000200000000`（cost 79・open 68・
  confirmation 11・parent `00000000000000403800000008000000`・demand
  {c1:0, c2:2, c4:0}）**。census v11 runner-up。v11時点のopen 69から
  bit 87（cost78c由来REFUTED-D10）がconfirmation側に移り68になった。
  confirmation 11 bitsの内訳: 10 REFUTED-D10（cost66j/64h/73l/69j/66i/72d/
  78c/73i/73j + pre-64h harvest）+ 1 WIN7-D10（bit 110 = cost73kのcanon。
  該当7石rootの証明書はcost73k bandで出版済み）。
- runner-up: `00000000020000003800400080000000`（cost 79・open 72）。
  ranking top-10はv11の残存9行を全て保持し、新規に
  cost 86 / `00000000020000003800000080000100`（open 78）が入った。
- cross_checks新規: 78c win bits claim/audit/manifest一致 11/11・manifest
  totals（614,003 rows / 77,967,826 nodes / 22,223,603 bytes）・並走
  batches-1-6 audit 54/54一致（blob `7460b42b`）・15 swept children open 0。

## 制限

- 本censusは探索計画bookkeepingのみ。新たなverdictは作っていない。
- 78cの証明書は「個別7石rootからdepth 10以内の先手勝ち」のみを証明し、
  manifest行のreceipt foldは未実施。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- cost 79 sweep（`00000000000000c09002000200000000`）のclaim作成と実行
  （open 68 bits + confirmation 11 bits。bit 110のWIN7-D10はcost73k証明書で
  再確認する）。
- 並走管轄（着手禁止）: 66i/66j receipt fold、73i証明書の出版、cost73k測定系、
  K09xx系。
