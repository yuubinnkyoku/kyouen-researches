# seven-row-q6-m32-class-split-20261118

高速レーン。**IN FLIGHT claim (2026-11-18 07:20 UTC) — 対照 PASS・本命 c3_7x32 未決**
(2026-11-18 09:35 UTC 更新)。

## Claim

- 本レーンは **(7,6) 前線 7×32 の class {3} class-split SAT witness 探索**を着手する
  (sat3.js --class=3・kissat 4.0.4・cap 6000s・resumable・records 増分 push)。
- 着手時点の境界: witness 帯 m=6..31 (m=31 は 34 石 rows [5,5,5,4,5,5,5] の
  surgery 構成・3 系統検証済み・seven-row-q6-m31-frontier-20261115)・
  **M_{7,6} ∈ [32, 862]** (上界 K0318 substitution U=862)。
- m=32 の既存 honest negatives: m=31 witness を種にした **2 編集 surgery 完全列挙
  は 2,224,675 一意候補・safe-maximal 0 件** (seven-row-q6-m32-surgery-negative-20261115・
  局所負記録・T=(31,3) センサス c4=1 直線 y=3 のみ・31s)。
  空列延伸は cell (31,3) 未遮断で失敗 (one-stone-short)。
  class {3} (7,31,6) SAT は cap 1800s で INDET 4,368,709 conflicts/896s process
  (witness は class {3} に属するため instance は SAT 確定・記録は m31-frontier)。
  2026-11-15 セッションで (7,32,6) c3 の並行実行が言及されたが record なし
  (環境リセットで喪失したものと解釈・本 dir が再着手)。
- **SAT ⟹ witness 帯 m=6..32 に延伸し M_{7,6} ∈ [33, 862]**。
  UNSAT ⟹ class {3} では 7×32 に witness なし (**7×32 全体の不在主張ではない**・
  他 70 正準クラス・3 編集 surgery・別 seed が残る)。
- 探索成功時は追加で空列延伸 probe (7×33 以降)・可能なら追加幅の
  witness 探索も同セッションで実施する。

## 経過 (2026-11-18 09:35 UTC 時点)

1. **対照 PASS — (7,30,6) class {3} end-to-end bit-exact 再現** (完了 08:34 UTC):
   - CNF 再生成 md5 `09e969b9461e413551f61f76bff817ce` — 出版 pin と byte-exact。
   - kissat **SAT・conflicts 2,670,296** — 出版 record (c3_7x30・2,670,296/497.0s) と
     **conflicts が bit-exact 一致** (本環境の所要 1051.4s・cap 2400s。
     実行環境が異なるため wall time は bit-exact 主張外)。
   - モデル復号 (parse_model.py) → **34 石 rows [5,5,5,4,5,5,5]・row 3 石 [12,23,27,29]** =
     出版 m=30 witness (seven-row-q6-m30-class-split-20261115/output/c3.witness.json) と同一配置。
   - 2 系統検証 PASS: verify_witness.py (Python Fraction) ok:true・
     verify_witness_det.js (純整数 4×4 行列式) ok:true・maxLine 5・maxCircle 5・uncovered 0。
   - `output/records.jsonl` に ctrl_c3_7x30 record・`output/ctrl-verification.json` に
     検証 summary。**本レーンの toolchain (encoder→CNF→kissat→decode→verify) は較正完了**。
2. **本命 c3_7x32 (7,32,6) class {3} は未決 — 2 回とも実行環境障害により中断**
   (いずれも kissat の判定によるものではない・honest record):
   - run-1 (07:16Z 開始・cap 5400s): CNF md5 `bc10c516134c8fff56a20f42f0bf6d61` byte-exact。
     最終確認進捗 **10,985,236 conflicts @ 2890.0s** → 実行環境リセットで喪失 (~07:36Z 障害)。
   - run-2 (08:15Z 開始・cap 6000s): 同一 CNF md5 byte-exact。
     最終確認進捗 **12,414,117 conflicts @ 2772.3s** → 実行環境障害で喪失 (~09:03Z 障害)。
   - 決定性の交差確認: 両 run の progress line が同一 conflicts 値 (例 2,168,884) を
     通過 — 同一決定的経路上にあったことの確認。両 run とも runner の record は
     未記録 (kissat 終了前にプロセスごと中断)。
   - 深度較正: class {3} の既知 depth は m=29 SAT 3,074,703・m=30 SAT 2,670,296・
     m=31 INDET 4,368,709。**m=32 は 12.4M+ で未決** — 直前 3 幅より有意に難化。
   - resume は初回から (kissat 決定性・CNF 再現済み)。**cap は 6000s 以上を推奨**
     (12.4M 到達でも未決のため)。実行環境の安定性が主リスク
     (約 2 時間のセッションで 2 回の環境障害を観測)。
3. 正直な記録: 上記 2 回の障害で作業 dir・進行中 kissat プロセス・中間 log を喪失。
   残存成果は本 push の 4 file (README・records.jsonl・ctrl-verification.json・run_one.sh)。
   M_{7,6} ∈ [32, 862] は本経過では不変。

## 手法・較正

- 生成器: sat3.js (md5 `d03f908ea99ba819caee2a6fbb471c1b`・
  seven-row-q6-m30-class-split-20261115 と同一 blob・--class=D で D 内の行を
  ≤4 石・D 外の行を exactly 5 石に固定)。sat.js `0cc6021a…`・
  verify_witness.py `0530d16…`・verify_witness_det.js も同レーン pin と一致確認済み。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  (md5 `3a5eba830aa6008a604fcc9bbe99a325`・rel-4.0.4 asset)。
- 対照: (7,30,6) class {3} の再実行で SAT 2,670,296 conflicts の bit-exact 再現 —
  **完了・PASS** (経過 1)。
- sat3.js decode は >65k 変数で spread overflow するため (m=32 は ~150k 変数)、
  SAT 時のモデル復号は独立 Python パーサで実施する (m=30/m=31 と同じ運用)。
- CNF 生成は決定的 (同一引数 → 同一 md5)。cap 内完了インスタンスの conflicts は
  kissat 決定性により bit-exact 再現可能。cap 打ち切りの conflicts は実行速度依存
  (bit-exact 主張はしない)。
- witness は 3 系統検証 (sat.js verifyConfig・verify_witness.py Python Fraction・
  verify_witness_det.js 純整数 4×4 行列式) + 負対照 (1 石除去摂動が
  非極大と検出されること) を要求する。

## Not claimed

- 7×32 全体の不在 (class {3} の UNSAT は不在主張ではない)・7×33 以降の不在、
  (7,q≠6) 家族、Grundy 値、
  11×11 空盤・二石 root・S2・class 2・class 4 (いずれも UNKNOWN)。
- c3_7x32 の SAT/UNSAT/INDET 判定 (未決・上記経過 2)。

## files / resume

- `run_one.sh` — 単一インスタンス runner (records.jsonl 増分記録・resumable・
  seven-row-q6-m30-class-split-20261115 の runner と同一構造・KS path のみ環境差し替え
  `KS=` 行を実行環境に合わせること)。
- `scripts/` — push 時点では未格納。pin 済み同一 blob を既存 dir から取得する:
  seven-row-q6-m30-class-split-20261115/scripts/ の
  sat.js・sat2.js・sat3.js・verify_witness.py・verify_witness_det.js と
  seven-row-q6-m31-frontier-20261115/scripts/ の parse_model.py・probe_free_column.py
  (md5 pin は手法・較正のとおり・parse_model.py は `c1cef8f8…`)。
- `output/records.jsonl` — ctrl_c3_7x30 のみ (本命は未決・record なし)。
- `output/ctrl-verification.json` — 対照の検証 summary。
- resume: scripts を配置し
  `KEY=c3_7x32 CAP=6000 nohup setsid bash run_one.sh c3_7x32 7 32 3 > output/c3_7x32.launch.log 2>&1 < /dev/null &`
  (起動前 /proc 走査で二重起動防止。環境リセット後は kissat を rel-4.0.4 asset
  から再取得・md5 照合)。


## 再開宣言 (2026-11-20 高速レーン・単一オーナー)

- 2026-11-20 19:0xZ (実行時刻は commit 時刻参照): 高速レーンが c3_7x32 の resume を
  単一オーナーとして着手する。cap 14400s・kissat 4.0.4 デフォルトオプション
  (既知 12.4M conflicts 経路からの決定性維持)・CNF md5 `bc10c516…` byte-exact
  再生成済み・kissat md5 `3a5eba83…` rel-4.0.4 asset 照合済み。
- 状態確認: 2026-11-18 09:31Z の ctrl push 以後この dir への commit なし
  (resume は 11-18 の 2 中断以後まだ行われていない)。
- 判定 (SAT/UNSAT) または cap 到達 (INDET) 時に本 dir と K0827 へ結果を追記する。
  環境障害で中断した場合は正直に中断 record のみ残す。

## 経過 (2026-11-20 再開 — run-3 中断と run-4 relaunch)

- **run-3 (2026-11-20 19:01Z 開始・cap 14400s・単一): 実行環境障害により中断** (~19:42-19:46Z 障害)。
  最終観測進捗 **6,783,075 conflicts @ 1398.2s** (19:42Z 前後の poll による最後の観測値・
  障害直前の正確な最終 progress line は環境消失により記録できず、上記は下界)。
  C++/Python での検証前・判定なし。runner record なし (kissat 終了前中断)。
- 環境リセットにより作業 dir・kissat プロセス・中間 log を喪失。再構築後、
  scripts・kissat (md5 3a5eba83…)・CNF (md5 bc10c516…) を再取得・再生成して
  **md5 はすべて再一致を確認** (cross-reset 決定性を再度実地確認)。
- **run-4 を relaunch** (cap 14400s・同条件下)。判定または cap 到達時に結果を追記する。
  並行して (7,5) 前線 7×38 class {0} class-split も着手
  (seven-row-q5-m38-class-split-20261120)。

## 経過 (run-4 中断 — 実行環境 3 回目の障害・セッション打ち切り)

- run-4 (19:47:30Z relaunch・cap 14400s): **決定性の交差確認** — run-3 最終観測
  6,783,075 conflicts を同一決定経路で通過 (20:39Z 頃)。その後
  **7,398,742 conflicts @ 1687.3s (20:44Z poll)** まで観測。
- **~20:47Z に 3 回目の実行環境障害で中断** (本セッションで 19:42Z と 20:47Z の
  2 回・通算で 11-18 を含め計 4 回)。判定なし・runner record なし。
  既知の 12,414,117 watermark (11-18 run-2) には未到達 — 本中断による
  新規情報の損失はなし (再 cover するだけの deterministic re-tread)。
- 障害後に実行環境が持続的に利用不可となったため本セッションは打ち切り。
  実行環境が安定するまでの resume 推奨: cap 14400s 以上・単一インスタンス
  (同時 2 実行で両者の rate が ~10% 低下する観測あり)。
  CNF md5 bc10c516… の再現性は 3 回のリセットを通じて確認済み。
