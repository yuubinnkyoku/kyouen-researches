# 2026-11-15：cost-65k sterile sweep完了 — 65 REFUTED-D10・WIN7-D10不在・frontier不変1199・11×11はUNKNOWN

開始時main: `1b814444`（並走レーンのcost-63g証明書14/14出版・sweep 63/63完了直後。chain head 1199/6648/524616/4918/388339 掲載済み）。head-1199のtop-candidatesで未sweepだった **cost-65 child `00000000020000801202000000200000`**（第2 coverable class-2 target S5 `00000000000000801202000000200000` のS6行・stones [21, 49, 57, 60, 71, 89]・lift stone 89）をcost-65kとして取得（cost-65b–65jは他行で使用済み）。

## claim前検証（head 1199基準）

- `legal_candidates.py`（exact Bareiss）: 65 legal candidates、manifest edge cost 65とbit-exact一致。
- D4 demand検証: 子の6個の一石削除を照合 → 開いている親は2個ともclass 2（第2target 38 orbits/2837〔stone 89削除〕・`00000000000000003800000008002000` 53 orbits/3698〔stone 21削除〕）→ c1=0, c2=2, c4=0。
- IN FLIGHT claimを先にpushしてからsweep着手（前セッション・remote blob sha照合済み）。

## sweep結果（v16 engine・depth 10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）

**65/65候補・WIN7-D10 0件・65 REFUTED・0 capped・総nodes 32,457,462**。STERILE（負の実験事実）: 証明書抽出対象なし。

- terminal stone range: 64候補は [13,17]、bit 9のみ [13,15]（全ライン早期終端・63fとは異なる正当値。監査assertは固定値比較から深さ10境界検査〔[0]≥7・[1]≤17〕に修正し `distinct_terminal_ranges` を記録）。
- 統制: batch 6（bits 74,75,76,77,79,83,84,86）determinism rerunはnode-exact一致（`class2-lane-cost65k-v16-determinism-rerun-20261115.jsonl`）。v15交差エンジン（`class4_child1_runner.ts`）でアンカーbits 7/86/118はloss=false（nodes 125301/2037455/5749144・pilot 5949）（`class2-lane-cost65k-v15-crosscheck-20261115.jsonl`）。

## 独立監査（全assert合格・2回実行byte-identical）

`audit_cost65k_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が10 rawファイルから全件再導出: 候補65はclaim列挙とbit-exact・各bit 1回ずつ・pilot 3402×8・batch-6再現一致・v15アンカー一致・D4 canonical重複0（published manifest roots 151個との比較込み・59 manifest走査）。監査JSON `class2-lane-cost65k-sweep-audit-20261115.json`（再実行byte-identical・md5 `85502aa91ed5260c536db4f24631521c`）。

## 出版上の注記（アーティファクト完全性）

raw 10ファイルの出版では、base64一括転写方式が2回失敗したため、整数compact-table（bit, nodes, ms, terminal range）からの確定的なJSONL行再生方式に切り替えた。ローカルで「table→JSONL再生→実ファイルとのbyte-exact比較」を検証（全10ファイル True）後にpushし、remote取得ファイルとローカルファイルの全件 `cmp` 一致を確認（raw 10ファイル・監査script・監査JSON・claimともbyte-exact・blob sha照合済み）。転写不良はいずれもpush前に検出済みで、不完全な中間状態はrepoに残っていない。

## 解釈上の注意

REFUTED-D10はLOSS証明ではない。**STERILE: WIN7-D10 receiptが存在しないためfold材料なし・canonical chain head 1199/6648/524616/4918/388339は不変**。child `00000000020000801202000000200000` はparent1（第2target）の未解決S6行のまま（38行/2837）。この行を反証で閉じるには深さ>10の証拠（65個の7石root各々について深さ>10の反証または不変量）が必要。代わりにparent1の他の子行からのWIN7 receiptのfoldで閉じることもできる。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 成果物

- completed claim: [class2-lane-cost65k-inflight-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65k-inflight-20261115.json)
- raw batches 1–8・determinism rerun・v15 crosscheck: 同output/ `class2-lane-cost65k-raw-batch{1..8}-20261115.jsonl` ほか
- sweep audit: [class2-lane-cost65k-sweep-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65k-sweep-audit-20261115.json)（再現: [audit_cost65k_raw_sweep_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65k_raw_sweep_20261115.py)）
