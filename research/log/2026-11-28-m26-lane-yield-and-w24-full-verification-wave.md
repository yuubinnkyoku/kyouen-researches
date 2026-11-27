# 2026-11-28 第66ラウンド: 6x26 SAT レーン譲渡と W_24 s=7 全数検証ウェーブ

このラウンドは並行ハーネス（別セッション）と同じ repo を同時作業したため、
判断・失敗・引き継ぎをこの log に集約する。

## 1. 6x26 SAT レーンの実行試行 → 譲渡

- 宣言 `a9dde1d30`（class {0}）/ `f9a982d2b`（class {1}）/ `e61acf82f`
 （class {2} minpos-REST）/ `9e703319b`（deep-deficiency）の 4 レーンの
 実行を担った。kissat 4.0.4 公式 linux-amd64（zip `63282e51…` / binary
 `21da5d98…`、sha 検証済み）を導入し、エンコーダ決定性統制
 （meta_c25p11: vars 53,532 / clauses 187,536、出版値と bit-exact）を確認。
- 陽性対照（6x25 class{2} krow=2:4 minpos=11）: attempt-1 は 275s cap で
 機械高負荷（並走全数計算で約 4.8 倍減速、2,884 conflicts/s）により
 743,684 conflicts で INDET（開示として生ログ出版）。attempt-2 は cap を
 2400s に拡張して完了させ、**SAT 3,574,244 conflicts — 出版 K1217 値と
 bit-exact**（完了決定的探索の conflicts 数は機械非依存）。生ログは
 `research/experiments/six-row-q6-m26-class2-rest-lane-20261128/output/`。
- 実行開始後、宣言所有者セッションが class {0} を自ら完了・出版
 （`b3c2d6dce`、全 12 probe INDET honest negative、対照 bit-exact 241.07s）。
 単一オーナー規約に従い、本セッションの重複実行は**全停止・譲渡**し、
 部分出力は削除。scaffolding（byte-clone scripts、driver run_lane.py、
 82 probe の spec、譲渡記録 README）のみ保持
 （`six-row-q6-m26-driver-20261128` + 4 レーン dir）。
- 残り class {1} / class {2} minpos-REST / deep-deficiency の実行は
 宣言所有者セッションに委ねる。

## 2. incident 79ad283a（本セッションの失敗）と教訓

- 本セッションの通常 `git add` + `git commit`（`79ad283ae`）が、並行
 ハーネスが staging していた大量削除を巻き込んでコミットした。ハーネスは
 これを「incident 79ad283a」として CSV 等を修復（`941034718`、
 RESTORE chunk 系列で復元進行中）。
- **教訓**: 共有 worktree では通常の add/commit を使わない。本セッションの
 以降の全コミットは temp-index の plumbing（read-tree origin/main →
 update-index --cacheinfo → write-tree → commit-tree → update-ref → push）
 で行い、index / worktree には一切触れない。リモートが進んでいる場合は
 fetch → 再 graft → push をリトライする。

## 3. W_24 s=7 全数検証ウェーブ（本ラウンドの主要成果）

並行ハーネスが K1348（ドデカッド 3 層）・K1349（層マップ）を出版したため、
サブエージェント 2 本は未着手領域に差し替えて実行:

- **W1（`w24-s7-13cap-dodecad-structure-20261128`）**:
  - 各極大 13-cap はドデカッドをちょうど 1 個含む（30,912/30,912 全数）。
  - 各ドデカッドはちょうど 12 個の極大 13-cap に含まれる（2,576/2,576）。
  - 66/12 分割を全 30,912 cap で全数確認。非 d11 2,040,192 個は重複ゼロ、
    全数 DP で**すべて G=2**（4 shard × 510,048）。
  - 拡大プロファイル（極大 12-拡大 6、13-cap 親 1）が**全 2,040,192 個で
    一様**（従来はサンプル）。
  - 純粋証明: 「高々 1 ドデカッド」は Golay 線形性 + 最小重み 8 から
    従う（|D1∩D2| ≥ 11 → D1+D2 は重み ≤ 2 の符号語で矛盾）。
  - K1347 を computation/computed → **proposition/proved** に昇格。
- **W2（`w24-s7-size-ladder-20261128`）**:
  - k=0..13 全層の D_k/T_k 対応表を全数 census + 全数 DP で確定
    （6,661,168 局面、GSIZE 公式値と全 k 完全一致）。
  - 「サイズ ≤ 11 の全キャップは極大 13-cap に含まれる」を全数確立。
    k=12 の T_12 = 373,520 は非極大 12-cap とちょうど一致。
  - d11 → 極大 13-cap 拡大 {13:12} を全 30,912 個で全数化
    （K1349 のサンプル主張を昇格）。
  - **訂正**: dodecad は s=7 では**非極大 G=1**（12 個の合法手はすべて
    極大 13-cap、全 2,576 個の全数 DP）。K1348 の k=12 行と K1342
    evidence の「ドデカッド 2,576 を含む」を修正（K1350 が訂正根拠）。
  - 新規 K 項目 **K1350**（computation/computed）。

## 4. 統合状態

- check.py: 本ウェーブのファイルはエラー・警告ゼロ（worktree baseline
  375 エラー / clean tree 744 エラーは並行ハーネスの再構成起因の
  既存 broken link で、本ラウンドでは触れない）。
- build.py: origin/main ツリーからの再生成結果は出版済み generated と
  完全一致（ハーネス側で既に再生成済み）。`git diff --exit-code`
  相当 PASS。
- unittest（tools/knowledge/tests、clean tree・36 tests / 660s）:
  **35/36 PASS、1 失敗 = `test_canonical_items_validate`**。失敗の内容は
  main 上の既存状態（check.py 744 broken links と、K1036 の YAML 崩れ
  「note:抽出driver。」の行）で、本ウェーブのファイルは誤りリストに
  含まれない。K1036 YAML 修復・link 修復は再構成の所有者セッションの
  修復ループ（c6f7f4d7a・62fc2b412 の前例）に委ねる。

## 5. 次の一手（引き継ぎ）

1. 残り 6x26 レーン（class {1} / minpos-REST / deep-deficiency）の
   宣言所有者による実行。
2. サイズ 12 非極大 373,520 = 370,944 + 2,576 の構造的意味、
   極大 12-cap 1,020,096 のドデカッド交差プロファイル分解。
3. 「サイズ ≤ 11 の全キャップは極大 13-cap に含まれる」の数学的証明
   （現在は全数有限計算）。
4. 極大 12-cap 拡大数プロファイル（{12:180} 等）の全数検証は
   並行ハーネスが 84/84 PASS を報告 — 本セッション K1350 の「限界」節と
   整合確認を推奨。
