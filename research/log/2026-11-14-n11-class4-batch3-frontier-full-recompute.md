# 2026-11-14 class4-batch3 後の manifest-level frontier 完全再計算（第20セッション）

- 目的: batch3 追加証明書（bit37・child#3/#4×3・child#5×4・child#7×5）を含む
  **全公表 WIN7 レシート**を 08e060f0 時点の入力から独立に再集計し、
  スナップショット値（baseline 638 / after_batch1 657 / after_batch2 665）を
  **前提でなく制御（assert）として再現**した上で batch3 効果を測る。
  スクリプト: `scripts/recompute_frontier_full.py`（audit_class_frontier.py
  論理の段階制御付き完全再実装）。
- 制御: baseline 638/7208/565500・batch1 657/7189/564070・batch2
  665/7181/563509/5398/423516 — 公表値と完全一致。
  batch2 duplicate-audit 決着: newly_solved は **8個の相異なるキー**（重複なし）。
  bit37 covers は証明書自身の `frontier_effect.covers_canonical_s6`（7 orbit）と完全一致。
- batch3 追加効果: bit37 covers 7・marginal_in_manifest 4、child34 16/7、
  child5 22/8、child7 28/6 — 計 **25個の新規 manifest S6 解消**。
- **frontier after batch3**: solved_s6_in_manifest **690**、unique_remaining
  **7156**、sum_cost **561764**、open 5373/421771。
  best class-4 blocker S5 `00000000020000003800000080000000` が **43→24 orbit・cost 1934**
  に低下。class-2 best `00000000000000003802000008000000` は 32/2206 不変。
  次の未sweep最安: cost 74 `00000000020000003801000080000000`（c4=3）と
  `00000000020000003800000080000020`（c1=2,c4=3）。cost 73 orbit（…c0000000）は
  child#6 sweep済みで WIN7-D10-sterile。**class-2側に未sweepの cost-60 orbit
  `00000000000000801a02000020000000`（c2=2）を発見**（どのsweep recordにも未登場）。
- 成果物（いずれも独立検証済み）:
  - `output/class4-batch3-frontier-full-recompute-20261114.json`（コミット b86d7025）
  - `output/class-frontier-top-candidates-s6-after-batch3.csv`（コミット f3914f64）
  - `output/class-frontier-s5-ranking-after-batch3.csv`（コミット 8870bda6）
  - 検証: 修復版スクリプト（コミット b9a908b9）を公開入力のみで再実行すると
    JSON は意味的に完全一致、top-candidates CSV は byte-identical、
    ranking CSV は push 後の remote と byte-identical（md5 28dbea05…）。
- トランスポート知見: (1) create_or_update_file の content にバックスラッシュ
  エスケープ（U+005C を2文字重ねた形）を含めると実改行へ二重デコードされる —
  改行リテラルは `chr(10)` を使う。
  (2) 17KB級base64の手転記で1文字欠落が起きた — 手転記は禁止し、
  ローカルファイルから `tools.file_system.read_file` 経由で直接渡す。
  (3) push直後の raw.githubusercontent は CDN 遅延がある — commit sha 指定の
  immutable raw URL で検証する。
- 解釈ガード: 本再計算は**公表レシート上の bookkeeping のみ**で新しい勝敗判定を含まない。
  REFUTED-D10 は「深さ10以内のWIN7の否定」のみ。
  **class 4・class 2・S2 {59,60}・二石 root {49,60}・11×11 空盤はいずれも UNKNOWN**。
- レジューム: (1) cost-60 class-2 orbit `00000000000000801a02000020000000` の sweep
  （class-2 lane で最安の未sweep）。 (2) cost-74 class-4 `00000000020000003801000080000000`。
  いずれも並走レーンの最新mainを取り直してから。
