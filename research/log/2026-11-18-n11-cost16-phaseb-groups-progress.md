# 2026-11-18 N11 cost-16 parent phase B groups 進捗記録（394/425 type・実行環境障害で中断）

## 背景

本セッション開始時のmainは `f9d6c6f9bcb5`。レジューム対象は31行cost-16 parent `00000000000000003800000008001000` の phase B groups runner（`cost16_phase_b_groups_20261118.py`・425 pair type・設計log `2026-11-18-n11-cost16-phaseb-groups-design.md` の13値が権威ある出力）。

## 進捗（中断時点）

- canonical runner（STATE_CAP 12M）で先頭type群を再計算し、`(0,3)` の a=78,573,131,321,269,652 / b=24,092,183,905,989,464 が設計logの13値表と完全一致することをコンソール出力で直接確認した。`(0,1)`/`(0,2)` の再計算値はJSONLに記録済みで、次回の全数照合で確認する。
- canonical 12M capは (5,9) 帯の木探索中に memo 10,611,712 + seen > 12M で発火し、425 type全体の共用memoとしては不足した。設計logの「飽和10.3M」は先頭帯域（(0,*)〜(4,*)系）の計測であり、(5,*)以降の各帯は概ね9.2M状態規模の新たな木を要求する（帯ごとの初回木探索 約60〜110秒・以降は0.05秒/type級）。cap 16M に上げた単一変更のlocal variant（`cost16_phase_b_groups_cap16m_20261118.py`・provenanceヘッダコメントのみ追加・それ以外はcanonicalと同一）で帯 (0,*)〜(21,30) まで計算した。
- **ホストのfilesystem rollbackが1回発生し作業dirごと消失した**（設計log記載の障害と同種。消失時点で385/425 type分を計算済み）。6入力pin再取得+候補JSONL再生成（約1分）で復旧し、全typeを最初から再計算した。**再計算は消失前の記録と数値完全一致**（観測範囲: (6,30) a=87,975,370,636,514,815 / b=26,795,220,943,048,878、(7,30) a=83,718,883,920,813,75 / b=25,539,171,744,658,212 ほか帯末尾全点）。値の決定性を環境リセット横断で再確認した。
- 中断時点: **394/425 type 完了**（残り約31 type・帯 (22,*)〜(30,*)）。JSONL snapshotは本レーンの実行環境の知識領域 scratch（knowledge/kyouen-research/_scratch/cost16phaseb/cost16-b-groups-20261118.jsonl・394 records）に退避済みで、環境リセットを生き延びる。

## 実行環境の実測（今回の障害の記録）

- フォアグラウンド・プロセスのkill窓は約2.1〜3.5分（変動）。nohupバックグラウンドは起動したbashコマンド終了時に消滅し実用不可。
- 2-way並列（213+213 typeの分離スライス・約1.1GB×2）は両プロセスとも約2分でkillされ効率化に失敗（RAM 3.2GB天井との兼ね合いが疑われるが原因未確定）。
- セッション終盤に**bash実行環境全体が "temporarily unavailable" となり約50分間復旧しなかった**ため、残31 type・aggregate検証・出版は次回実行に回す。JSONL snapshotの取り込みもfile読み取り経路が同じ障害に含まれるため本logは進捗の数値詳細を最小限に留めた。

## 並走laneのB型総数確定と本laneの役割変更

セッション中に並走が **B16 = 660,663,050,386,546,968**（A16 = 2,305,787,291,293,934,388・最小cover総数 A16+B16 = 2,966,450,341,680,481,356）を31 d-slice共用memoで確定出版した（commit `1bcd465815af`・log `2026-11-18-n11-cost16-parent-shared-memo-crosscheck.md`・census pin splice修正のamendment `b10b397cd25e`・amendment後output blob `41d37ed8…`・18/18 checks）。checkpoint `d2901d15` の31独立fresh-memo slice計算とも一致している。

よってgroups runnerの役割はB総数の初回確定ではなく、**per-pair-type分解による全425 pair root membership（A/B splitつき）とその独立照合**に変わった。aggregate mode の恒等式 sum(a_part)==15*A16・sum(b_part)==16*B16 が、per-pair-type分解とper-doubled-row B_d分解（並走）の二経路一致検証となる。

また設計logの観察「(0,2)と(0,3)のb_part一致（行2・行3のD4対称性の候補・要確認）」は、並走出版データで強く支持された: 行2・行3（さらにrow 13も）は pm(V∖{s}) = 1,415,501,771,326,047・B_d = 23,477,541,507,703,040・pair degree 30 が全て同一（amendment済crosscheck outputの A16_per_row_pm / B_by_doubled_row）。行2/行3はparent構造の対称類と考えられる。

## 次回の作業（優先順位）

1. 作業dir復旧（6入力pin再取得+候補JSONL再生成）→ knowledge scratch から394-record JSONLを復元 → 残り約31 type（帯 (22,*)〜(30,*)）を cap16m variant で計算（kill窓内に1〜2帯/実行・invocationごとにscratchへsnapshot）。
2. canonical runner の aggregate mode（恒等式検証・B = sum(b_part)/16 が並走の B16 = 660,663,050,386,546,968 と一致することを確認）。
3. 13値表の全数照合（JSONL vs 設計log表の13 type）。
4. 出版: JSONL（425 records + summaries）+ aggregate output JSON + cap16m variant（provenanceヘッダつき）+ 検証log。payloadが実用上限（約400KB/push）を超える場合は2コミット分割。
5. 続く未完項目: top-10 joint membership・ban生存曲線（29行runner-upと同じ手法の31行版）。

## 解釈上の注意

membershipは最小cover計画の組合せ数であり探索コストでもverdictでもない。REFUTED-D10・STERILEはLOSS証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
