# 2026-11-18 n11 cost76c parent-B amendmentの検証側クロスチェック（修正値全確認・amendment本文の親帰属誤りを検出）

## 背景

amendment commit `c4ab218965` が歴史fold記録 `class-frontier-cost76c-receipts-recompute-20261117.json` に top-level `amendment_20261118` ブロックを追加した（元fieldは一字も変更しないtextual insert）。対象は fold-chain ledger crosscheck（`aa3af62b`）が検出した parent B（`00000000000000801202000000040000`）エントリの77e行二重計上。検証側として本amendmentを独立再計算で確認した。

入力は全て git blob pin: worklist `2fee1d07` / K0865 census `9c251da3` / fold-chain ledger `e8785d50` / per-parent bookkeeping crosscheck `ed98c01429` / amendment後記録 `cb875a1d`。

## 確認結果（40/40 checks all PASS・二重実行byte-identical）

1. **textual insert検証**: amendment後ファイルの2..16行目（amendmentブロック）を除去すると、残りは元記録（git blob `953beaea054989e8b1de33f48b1f2ebc13ae7e11`）と byte-exact 一致。元の誤記entry（B: rows_after 69 / edge_cost_after 5725 / lost 77e行）も verbatim 保存されている。
2. **B chain-correct値の独立再導出**: head-1410 join 74行 / cost 6,113。閉鎖史は cost64d 2行（153）→ cost76d77e 77e行（77）→ cost64h 1行（81）で、cost76c foldの閉鎖行はBに0行。76c通過後の状態 = **70行 / 5,802**。amendmentの corrected_entry（lost 0 / rows_after 70 / edge_cost_after 5,802 / lost_edge_cost 0）と完全一致。
3. **元entryの誤りの機構**: Bのbaseline（post-cost64h・70行/5,802）は head-1452 の cost76d77e foldで閉鎖済みの77e行を既に除外しており、それをlostとして再適用したことが69/5,725の二重計上の本体。
4. **aggregate field**: 元 458/6 = 76+77+229+76 / 1+1+3+1。修正 record-total **381/5** = 76+229+76 / 1+3+1 を確認（amendmentの数値と一致）。
5. **他3 entryのchain整合**: P（`00000000000000003800000208000000`）join 65/5,358・76d行閉鎖 → 64/5,282。rank-1 parent（`00000000000000801202000040000000`）join 5/364・3行（76+77+76）→ 2/135。E（`00000000000000801202000100000000`）join 71/5,912・baseline 69/5,758（cost66cで2行/154閉鎖済み）・76c行閉鎖 → 68/5,682。全て記録のafter値と一致。
6. **大域head算術**: frontier_after_cost76c 1473/6,375/504,596 は ledger chain と一致（amendmentは大域fieldに触れない）。

## 新規所見: amendment本文の親帰属誤り

amendmentのfinding textは「The cost76c WIN row is a D4 child of parents P and E only」とし、P を `00000000000000003800000208000000`、E を `00000000000000801202000100000000` と明記している。174 open S5 parent全てについて直接再計算した結果:

- **76c行 `00000000010000809002000001000000` のD4親は rank-1 parent `00000000000000801202000040000000` と E `00000000000000801202000100000000` のみ**。
- `00000000000000003800000208000000` は76c行ではなく **76d行 `00000000040000003800080008000000` のD4親**。
- **根因**: 我々の fold-chain ledger finding（`aa3af62b`）がhexを付けず「parents P and E only」と記載した。per-parent crosscheck（`376e4f44`）の文字慣行では P = rank-1 parent（join 5/364）を指すが、amendment作成時にこの文字が join 65/5,358 の parent に解決された。amendment logの「ledger crosscheckの直接計算による」の出典確認は文字レベルでは正しく、hex解決で誤った。
- **影響**: 修正値には影響なし。Bはどちらの親集合にも含まれず、したがってB修正（lost 0）は正当。
- **補足**: amendmentの「chain-correct cost76c marginal per-parent values are 381 and 5」は corrected record-total としては正しいが、76c fold自体の厳密なchain marginalは **2 parent incidences / 152 edge delta**（閉鎖は76c行1行・cost 76×2親）。この区別を result JSON の findings 節に明記した。

## 成果物

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost76c_parent_b_amendment_20261118.py`（git blob `caf20323b7309f01390eaae23aad9e2ceba7e91e`）
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost76c-parent-b-amendment-crosscheck-20261118.json`（git blob `ddc6005d6702a4cfcdbf38e2b9a08ed9a9eefa3b`・二重実行byte-identical）

## 解釈境界

engine実行なし・新規verdict/receipt fold/S5 closureなし。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
