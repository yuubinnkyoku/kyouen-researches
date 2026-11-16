# 2026-11-16：cost-65n IN FLIGHT claim v1の構造的独立検証 — 21/21チェックPASS（manifest cost 65・head-1441でopen・両class-2親保持・legal 65 bits bit-exact・transferred 6 bits canon identity・open 59 bits・8バッチ分割・census v4 first row一致）

開始時main: `fbafd1e1`（本レーン直前のcover-multiplicity監査出版）。対象は並走レーンが08:13:48Zに出版した**cost-65n IN FLIGHT claim v1**（commit `7dcd9767`・対象child `00000000000000801202010000800000`・SH親 `00000000000000003800000008002000`・head 1441のcheapest open行）。本検証はclaimの構造的健全性の独立確認のみを行い、sweep自体は並走が所有（着手禁止・重複sweepなし）。

## 検証内容（出力 `output/class2-lane-cost65n-claim-structure-verification-20261116.json`・schema `...-v1`・git blob `b0dfbef5`・決定性2回byte-identical確認済み・全21チェックPASS）

### 方法
- head-1441 solved集合は本レーンの独立再構成（761 published receipt roots + bit-89 fold receipt root `00000000020100003800000008080000` + winners 498・verbatim移植frontier semantics）でsolved ∩ manifest = 1441をassert済みのものを使用。
- 候補列挙はrepo収載 `legal_candidates.py`（Bareiss 4×4整数行列式・過去5 sweepでbit-exact検証済み）を再実行。

### 検証結果（21/21 PASS）
1. **child `00000000000000801202010000800000`**: manifest内・cost 65・D4自己canon（canon(child)==child）。
2. **head-1441でopen**: 独立再構成solved集合（1441 orbit）に含まれない。
3. **保持親構造**: remaining frontierでchildを保持するs5行は2行 — SH `00000000000000003800000008002000`（class-2・fold後29 rows/2017）と第2親 `00000000000000801202010000000000`（class-2・fold後48 rows/3498）で、per-class open-parent demand **c1=0, c2=2, c4=0** がclaim・census v4と完全一致。64g foldで第2親からは2行・SHからは1行が失われた後の構造と整合。
4. **合法候補65 bits**: `legal_candidates.py` 再列挙がclaimの `legal_candidates` と**bit-exact一致**（candidate_count 65）。child stones [23,40,49,57,60,71]も一致。
5. **転送済みREFUTED-D10 6 bits [35,50,51,55,64,109]**: 各bitについて **canon(child|1<<bit) == claimのroot_canon** が6/6一致（D4-canonical root identityの独立検証）。全bitsがlegal candidatesの部分集合。
6. **open 59 bits**: legal 65 − transferred 6 = 59がclaimの `open_candidates_to_sweep` と**bit-exact一致**。planned 8バッチ [1,3,6,8,9,10,11,12]…[118,119,120] が59 open bitsを過不足なく disjoint 分割。
7. **census v4整合**: `cheapest_open_rows_ranking[0]` がこの行（cost 65）・chain_head 1441/174/6407/506945/4680/370859・claimの `chain_head_at_claim` も同headを正しくpin（stale-baselineなし・fold receipt blob `aff79002` pin）。

## 意義

1. **並走が着手したcost-65n sweepの入力（child・候補・転送・バッチ構成）が第三者実装で全数一致** — sweepの前提に構造的誤りがないことをsweep実行前に独立確認。以後のraw batch・claim v2着地時は本検証（blob `b0dfbef5`）を入力健全性のpinとして使用できる。
2. 転送6 bitsのD4-canonical root identityが独立canon実装で6/6一致 — harvest転送の正確性をsweep前に事前確認。
3. 本検証は並走sweepと完全に独立（bookkeepingのみ・engine未実行・verdict作成なし・着手禁止の尊重）。

## 解釈境界（重要）

- 本検証はclaimの簿記検証のみで、いかなるverdictも作らない。cost-65n sweepは並走がIN FLIGHTで所有。
- REFUTED-D10はLOSS証明ではない。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。

## 今後

- 並走のcost-65n sweep完走（claim v2・raw batches・証明書）着地時は、(1) raw batchの独立再パース照合、(2) bit89のときと同様の独立fold投影・一致検証を実施する。
- WIN7が出た場合のfold投影候補（このchildの親2行と、候補rootのcoversが被覆する行）は本JSONのholder/demand情報から即座に計算可能。
