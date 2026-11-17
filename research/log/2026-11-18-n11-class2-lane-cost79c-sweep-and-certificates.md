# 2026-11-18 n11 class2-lane cost79c: fresh v17 sweep完了 + 19 WIN7証明書の抽出・独立検証・出版 (2026-11-18)

## 背景

cost79c claim v1（`class2-lane-cost79c-inflight-20261118.json`・blob `6e1f2c90`・preflight監査は
`f947def0`・census v12は`8e64d552`）は、census v12 rank-1行
`00000000000000c09002000200000000`（S6・石bits [33,49,60,63,70,71]・edge cost 79・
demand {c1:0, c2:2, c4:0}・法候補79 == edge cost）のfresh 79-bit depth-10 sweepを
計画していたが、claim作成セッションは実行環境を持たずbatches_run=0のままだった。
長期レーンがこのclaimを引き継ぎ、sweep・監査・証明書bandを一気に完走した。

## 実行1: fresh v17 depth-10 sweep（commit `26a10ac5`・監査commit `50133985`）

- 68 open bits（7×9+1×5の8バッチ）+ 11 confirmation bitsの9バッチ。engine v17
  （blob `c132cc64`）・depth 10・cap 1e9/bit・andclose 1・pilot_d6管理。
- 79/79 verdicts確定: **20 WIN7-D10** bits
  [1,2,17,21,26,28,29,30,31,47,58,62,91,96,100,109,110,113,117,120]・
  59 REFUTED-D10・0 capped。candidate nodes 206,090,979 + pilot 9×3,402。
- 確認batch 9はcensus v12 overlay予測と完全一致（10 REFUTED + WIN bit 110、衝突0）。
  bit 110はcost73k bit 87とcanon等価（証明書はcost73k bandで出版済み）。
- 決定性: det1/det8再実行はmsのみ差でfield同一。
- 生バッチ監査（`audit_cost79c_raw_batches_20261118.py`・blob `133f2230`）:
  19/19 checks PASS（形状/open68+確認11完全一致/79 canon一意/pilot全3402/
  andclose全true/capped 0/terminal[13,17]/node合計/det一致/v15a一致/census v12
  selection一致）。二重実行byte同一（md5 `a3966a8d`）。
- v15 cross-engine: 確認batch 11/11（pilot 5,949・blob `2d7dc9b9`）+ heavy open chunk
  bits [116,92,117] 3/3（pilot 5,949・blob `8efee514`）。**14/14一致・衝突0**。

## 実行2: 19新規WIN bitの盲証明書抽出・独立検証・出版（本band）

- 抽出: `extract79c_all_20261118.sh`（root = child|1<<bit を`legal_candidates.py`に通し、
  `cert_driver78c.ts`がrepo-verbatim `extractor_exact_ms23`（MS=1<<23・engine v15内蔵・
  kill table空）で抽出。bit毎fresh process・行は重複排除してsort。
- 全19 bitで fbt_drops=0・fatalなし・per-move cappedなし。抽出node数合計
  **339,101,130**・行数合計 **1,106,127**・出版bytes合計 **39,877,889**。
- 検証: `verify_cost79c_one.sh`が`verify_bit7_win7_cert.ts`（Bareiss 4x4・engine不使用）で
  (1) root-check（stones=7・loser mobilityが独立`legal_candidates.py`列挙と一致・
  52〜68手）、(2) 全loser初手指しをbatchでsub-root検証、(3) consumed winner-state unionと
  証明書行集合の両方向比較、を実施。**19/19でPASS: union 0 missing / 0 extra**。
- 第三実装: `verify_win7_certificate_bigint_independent.mjs`（BigInt 3x3余因子展開・
  solver/verdict cache/repo verifier importなし）がbits [21, 30, 117, 120]でPASS
  （独立consumed-union会計で0 missing / 0 extra。記録
  `class2-lane-cost79c-bigint-third-impl-verify-20261118.json`）。
- 決定性: bits 30（最小・1,294,259 bytes）・117（最大・2,914,821 bytes）をfresh processで
  再抽出しbyte-identical（md5 `760993f6` / `b9c887ce`）。
- 出版: band commits `462448cd`..`d9a9b575`。41 part files（16二分割 + 3三分割、行境界
  分割、part1に証明書ヘッダ）+ 19 README-split + 19 rootcheck + 19 subroots。
  **全41 partをraw CDNでbyte-exact着地確認**。manifest
  `class2-lane-cost79c-win7-certificates-20261118.json`（blob `e904a376`）にper-bit明細
  （rows/extraction nodes/md5/sha256/D4 canon root/分割）を記録。
- claim v2（blob `d16d7b1a`）でsweep+証明書の完了状態を記録
  （batches_run 9・actual_execution・confirmation_outcome・certificates）。

## 制限

- 証明書が証明するのは「個別7石rootからdepth 10以内の先手勝ち」のみ。
  REFUTED-D10はLOSS証明ではない。manifest行は本bandでは閉じない。
  receipt foldは66i(残8)/66j/69j/71e/72d/73i/73j/73k/73l fold完了後。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census側でcost79c行をswept（20 WIN7-D10・証明書出版済み・59 REFUTED-D10）として
  扱える状態になった。次ターゲット選定はcensus v12 rankingに従う。
- 並走管轄のまま手を出さないもの: 66i receipt fold残8、73i証明書出版、
  cost73k測定系、receipt fold本体。
