# 2026-11-16：post-cost-66c上位候補sterility監査 — head 1450でbest coverable class-2 S5が全行sterile確定、実効次ターゲットは76d/77e fold待ちと第三S5

開始時main: `194c35cc62b372abc2aea8ec7bd43bfb2cff09b6`（cost-66c fold着地・claim v4修正・cross-row D4監査着地後）。

## 目的

cost-66c fold着定後の新正準head `1450/174/6398/506297/4671/370211` で、上位coverable class-2 S5の残行が「depth-10 WIN7 receiptで閉じられるか、sweep済みでfold待ちか、IN FLIGHTか、未着手か」を、定理適用性スキャン（theorem-applicability-scan-20261116.json, git blob `24f214e6a9dd721ef95ac97d6b84cf34af33b14b`、第二独立検証 VERIFICATION PASSED, git blob `65e3e822a390ee945f632d07e80c95049985078c`、scan landing commit `2d090b491c069d6cbe42f3f1c1cff99144b6f176`）の正準root verdict corpusと突き合わせて確定させ、次に計算を割り振るべき対象を誤読なしで定める。

## 手法

出版済みcost-66c fold scriptの全工程を全pin再assert付きで再実行した（764-root基盤の独立再構築、66候補sweep再導出、claim v4再assert、head-1441 census v4、7証明書のbyte再検証・BigInt/Bareiss検査、66軌道conflict census、7 receipt fold、head 1450再現）。続いて、head 1450の上位5 coverable class-2 S5の全残行をverdict corpus（engine verdict、verdict転送、open候補数、claims）と照合し、5分類（sterile_unclosable_by_win7_d10 / win7_d10_receipts_swept_fold_pending / partially_determined_open_candidates_remain / determined_mixed / unswept_unclaimed）で確定した。fold出力4ファイル（fold JSON・2 CSV・claim v4）は本監査では書き換えず、出版git blobを末尾で再assertした。全assert PASS、所要は1実行あたり約2分。

## 結果

1. **best coverable class-2 S5 `00000000000000801202000000200000`（3行/209）は全行sterile。** 3残行（children `00000000020000801202000000200000` / `00000000000000801282000000200000` / `00000000000000889002000000000800`、edge cost 65/70/74）の合法第7石候補計209個すべてが出版sweep（cost-65k / cost-70d+70j / cost-74h）でREFUTED-D10、WIN7-D10 0・capped 0・open 0。よってこの親は、どの残行もdepth-10 WIN7 receiptでは閉じられない。66cに続く「同型66d / cost-65p系」の経路はこの時点で確定的に不可。
2. 第二S5 `00000000000000801202000040000000`（5行/364）: rows 64/71（cost-64a / cost-71d）sterile、row 76 child `00000000010000809002000001000000` はcost-76c IN FLIGHT（61 open、15転送REFUTED-D10）、rows 76/77 children `00000000040000003800080008000000` / `00000000040000809002000000004000` はcost-76d / cost-77eでsweep済み、WIN7-D10各2本 → **fold待ち**。
3. 第三S5 `00000000000000403800000008000000`（18行/1287）: **全行unswept unclaimed** → 実効次sweep対象。
4. 第四S5 `00000000000000003800000008002000`（25行/1748）: 2行sterile（cost-64c行、およびtop S5と共有のcost-65行 `00000000020000801202000000200000`）、1行はcost-69a IN FLIGHT（66 open）、残り22行未着手。top S5とのcost-65行の共有は新規cross-incidence記録。
5. 第五S5 `00000000000000003800000009000000`（29行/2203）: 全行unswept unclaimed。

## 実効次ターゲット（この監査に基づく更新）

- cost-76d / cost-77eのWIN7-D10 receipt各2本のfold（着手前に両laneのclaim・証明書の出版状況を最新mainで確認すること。prereg → fold → agreement の3点セット標準プロトコル）。
- 第三S5（18行/1287）のsweep。
- cost-76c・cost-69aは他セッションIN FLIGHTのため着手禁止。完了時はverdict転送またはWIN/LOSS conflict調査が必要。
- cross-row watch（既存）: cost-66c bit83正準形 `00000000000000a09002080080000000` == cost-65o bit43候補（REFUTED-D10転送必須、WIN7-D10が出た場合は矛盾調査）。

## 成果物

- 監査スクリプト: [audit_post_cost66c_top_candidates_20261116.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_post_cost66c_top_candidates_20261116.py)
- 監査結果: [class2-lane-post-cost66c-top-candidates-sterility-audit-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-post-cost66c-top-candidates-sterility-audit-20261116.json)（git blob `9f1c35267607da732b34ed908784df97e782c522`、29,255 bytes）

全入力はGit blob SHAで固定。claimは最新mainのv4（git blob `5e89637b748cbc70838723edbbfeda907af78da5`、v3全フィールドはfold.v3_fieldsに保存）を再assertした。長時間探索は起動していない。

## 解釈境界

STERILEは行ごとの「depth-10 WIN7 receiptによる閉鎖不可」の簿記事実であり、LOSS証明でもゲーム理論的値の決定でもない。REFUTED-D10は個別rootのWIN7-D10不在のみを意味する。solved 1450はmanifest被覆の簿記である。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
