# run log: 7点純三点辺・五本以下 完全族の全長34周期認証（K0684 same-K evidence update）

single-owner 宣言: `research/log/2026-11-25-rooted-core-seven-pure-triple-five-edges-single-owner-note.md`
（commit `b8205166`、宣言時点 HEAD `7e411346`、2026-11-25）。
実行環境: Vibe 高速レーン・クラウドサンドボックス（Python 3.12・標準ライブラリのみ）。
ユーザーの PC には定時実行のため到達不可（全計算はサンドボックス側）。

## 1. 宣言前探査（宣言ノート §6 に開示済みの内容）

1. **前置きレビューで `solve_core.py` の `distinct_initial_types` 集計式の冗長誤記を発見**
   （実質「閉包内 n 頂点状態数」を数えていた）→ 真の初期型数 `len(initial)` に修正
   （修正後 sha256 `35a56325...` を宣言ノートに pin）。6点smokeでは両式が偶然同値
   732 を与えたため smoke 成果物は影響なし。engine.py・再帰・認証規則は不変。
2. **smoke replay（6点×6本以下・出版済み監査の完全再現）**:
   同一パイプライン（solve_core + 出版 engine.py）で raw 60,460・根付き732型を再計算。
   出版 `rooted-core-six-pure-triple-six-edges-20261107/output/audit.json` と
   **全732レコード・全prefix値・joint start 571・needed 1211・jointly_certified=true・
   Grundy最大27・worst entry [6,[7,11,14,19,28,37]] 完全一致**。
   成果物 `output/smoke6_records.json`（sha256 `dd416a01...`）は kit に残置し
   `verify_smoke.py` で常設照合。
   ※検証電池後の再実行（決定論性の追試）でも 39.2秒で再認証・全一致。

## 2. 公式実行

mode: `drive_slice.py <budget> <mode>`（mode≠smoke6 で 7点・E≤5 公式）。maxlen 2200。
毎回の列挙（384,168 mask × 720 perm table 最小化）所要 約135秒・solver 所要 約125秒。

| run | mode | 環境 | 結果 |
| --- | --- | --- | --- |
| 1 | official | 既定 | CERTIFIED 1211 (start 571) ・ elapsed 262.9s |
| 2 | official2 | 既定（新プロセス、checkpoint無し） | CERTIFIED 1211 (start 571) ・ run1 と records byte 一致 |
| 3 | hs_random | `PYTHONHASHSEED=random`（同一cwd） | byte 一致 |
| 4 | hs_one | `PYTHONHASHSEED=1`（同一cwd） | byte 一致 |
| 5 | ety1 | 隔離tree・`env -i` | byte 一致 |
| 6 | ety2 | 隔離tree・`env -i`（2回目） | byte 一致 |

全 run の records が同一 sha256
`5a1efeba3f55dd0a4d82421ecea5b8245f99bf8844c1f1cd53365dfdf9bd1bc2`
（`combine_records.py` の再結合でも再現）。

### 2.1 インシデント記録（正直な障害ログ）

run1/run2 完了後の検証ステップ中にサンドボックス基盤障害（Koyeb remote command 失敗、
約 2026-11-25T17:50Z 頃）で**実行環境がリセットされ、作業ツリー（当時の run1/run2 の
records・検証スクリプト・shard・参照監査のローカルコピー）が全部喪失**した。
喪失はプロセス外領域のみで、**宣言ノート（GitHub push 済み・commit b8205166）は無事**。
対処:
1. engine.py・基底表・6点×6本以下監査・6点全型監査（sha `c39cc86f...`）を GitHub から再取得。
2. `solve_core.py`・`drive_slice.py` を対話記録の全文から再構築 →
   **宣言ノート pin の sha256（`35a56325...` / `d2785476...`）と byte 完全再現**。
3. smoke replay 再実行 → 39.2秒で認証・出版監査と全一致（§1.2）。
4. 公式 run1'〜run3'(hs_random) を新サンドボックスで再実行 →

全て記録済み sha `5a1efeba...` を byte 再現。すなわち**別サンドボックスでの
クロス環境再現性が実証**された（元 run1/run2・新環境 run1'/run2' 計4走一致 + 追い
PYTHONHASHSEED/env -i 系4走一致、計6走）。
run2' 以降＋検証電池は新サンドボックスで実施。shard 6分割化は push サイズ制限
（16MiB メモリ上限）への対応で、単一正規ファイルと再結合で byte 等しいことを確認済み。

## 3. 検証電池（受入条件 §4）

全て新サンドボックスで実行。出力行はいずれも最終行 PASS 判定。

| 検証器 | 内容 | 結果 |
| --- | --- | --- |
| verify_enum.py | E1 raw 384,168（二項恒等式）/ E2 枚挙924型 / **E3 Burnside独立軌道数924** / E4 軌道安定化子総和=384,168 / E5 全型 canonical 固定点・基底表と互いに素 / E6 閉包2,948={2,604新規{6:1,680,7:924}+344既知} / E7 shard 7点レコード=枚挙型集合 | **VERIFY-ENUM: PASS**(2m22s) |
| verify_values.py | V1 再結合sha一致 / V2 閉包・計数 / V3 全2,604レコード×全長一致+prefix_start再現 / V4 窓認証[571,1177]worst破綻570 / V5 基底表344状態の直値+ブロック拡張一致 / V6 301純triple状態が出版6点両監査に全長一致・1,379混在状態が両監査に不在 / V7 pure/mixed計数・Grundy最大33 | **VERIFY-VALUES: PASS**(2m10s) |
| verify_direct.py | 階層化17層×seed 7で400状態×長さ0..6、原始subset mex照合 2,800検査・安全状態922,862 | **VERIFY-DIRECT: PASS**(5s) |
| verify_tamper.py | T0-T3 本物データの不変量成立、T4-T10 構造化改変7種（尾値フリップ・隣接swap・切り詰め・prefix_start汚染・重複・head汚染・計数汚染）全件検出 | **VERIFY-TAMPER: PASS**(3s) |
| verify_smoke.py | smoke6_records.json が出版6点×6本以下監査と全一致 | **VERIFY-SMOKE: PASS** |

追試: verify_smoke/tamper/direct の stdout は `PYTHONHASHSEED=random/1` で複数走
byte 一致（決定性確認）。重い2検証器（values/enum）は上述の別環境再実行そのものが
出力等価の証拠。

## 4. 主結果（有限・完全族の定理）

- **7点・純三点辺・高々5本の完全族**（raw 384,168 labelled ∈ 根付き924型）の全
  残留状態（閉包2,948 = 新規2,604 + 既知344）について、通常Grundy列は
  **全長で L>=571 から周期34**（`jointly_certified=true`、needed=1211）。
- prefix上のGrundy最大 **33**。最大33は二点辺混在の6点残留
  `[6,[3,6,13,24,44]]`（bit_counts [2,2,3,2,3]・argmax L=208）が**唯一**担い、
  7点初期型自身のprefix上最大は27、6点純triple残留も27である
  （二点辺混在族が純三点辺族（全型最大29）を超える Grundy 値を生成する最初の実証）。
- **6点の二点辺混在clutter 1,379状態の初認証**（7点核の着手による退化で出現）。
  純triple残留301状態は出版6点監査と全長完全一致。最悪破綻570を担う
  `[6,[3,13,22,28,49]]` も二点辺混在の新規状態で、6点×6本以下族の開始571と
  同値の開始が別状態により再現される形。
- 924型の型数はBurnside軌道数計算と軌道安定化子総和の二重の独立導出で確認。

## 5. 反例プロトコル・限界（宣言ノート §5 と同一）

有限族の定理であり、7点×6本以上・二点辺混在の7点核・8点以上・無界核（K0684 全称）は
未証明のまま。513基底データの値は K0682 出版済み証明の再利用。11×11 空盤・
二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。

## 6. 出版物

実験ディレクトリ `research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/`
（README.md・proof.md・solve_core.py・drive_slice.py・shard_records.py・combine_records.py・
verify_{enum,values,direct,tamper,smoke}.py・output/smoke6_records.json・
output/shards/part00..05.json・MANIFEST-sha256）。
records 単一正規ファイルは6.93MBのため6シャード構成で出版し、
`combine_records.py` による再結合で sha `5a1efeba...` に戻ることを検証済み
（再結合生成物は repo に格納せず、MANIFEST に hash で記録）。

K0684 knowledge item に artifacts 追記・evidence/限界節更新（same-K・新規採番なし）。

## 7. 次のステップ（このレーンの後継）

- 7点純三点辺の「全型」拡張（E上限撤廃: Σ_{k=0..35} C(35,k)=2^35 labelled は厳しいが
  Burnside型数は有限で確定可能。6本以上の型に限定した増分列挙が実現可能か調査）。
- 7点での二点辺混在核（rank 2/3 混在）の小規模完全族（例: 高々2本の二点辺追加）。
- 8点純三点辺 E≤2〜3 の完全族で開始値の成長傾向（571→?）を観測する価値の検討。
- Grundy最大の伸び（23→27→29→33）が頂点数・辺数のどこで発生するかの構造分析
  （最大33を与える7点型の特定は records から機械的に导出可能）。
