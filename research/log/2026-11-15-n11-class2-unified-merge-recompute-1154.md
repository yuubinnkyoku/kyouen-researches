# 2026-11-15 class2-lane: unified merge of the three divergent folds — chain head 1154; third class-2 target 8 orbits / 588

Long-term lane session (2026-11-15 JST). This session executed the published
unified-fold specification
([class2-lane-unified-fold-reconciliation-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-unified-fold-reconciliation-20261115.json))
— 現行main版（correction_20261115_b入り、git blob sha
`de112d9e…`。初版を取得後に同版へ更新し、その版の制御条件に従って実行した）—  and merged
all three folds over the common 1109 baseline into the single canonical
chain head
[class-frontier-unified-merge-recompute-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-unified-merge-recompute-20261115.json).

## 実行環境の再構築とchain再現

実行環境がセッション中にリセットされ、ローカル作業treeが消失した。mainの
codeload tarball（約3.1GB、実験dir 506MBを選択抽出）と、スナップショット後
にpushされたファイル（cost-69f raw batch 1–9/sweep-audit/determinism/v15、
merged multiband2+68dhyg recompute一式）のraw fetchで再構築した。そのtreeから
chain全体（cost73a基底 → 1109 → 1117/1140/1148）がbyte-identicalに再現され、
並走レーンのmerged 1148 recompute（commit 19bb2abc）の再現も同時に確認された
（chain出力のmd5全件不変）。ローカル消失前の成果はすべてmainにpush済みで
あったため、再構築による損失は0件。

## cost-70c warm 6証明書の独立検証

- 対象: cost-70c child `00000000000000803242000000000000` のWIN7 bits
  105/92/40/24/11/8（並走レーンがmainへpush済み、どのheadにも未fold）。
- byte: main tarball + raw fetch交叉確認。GitHub dir listingのgit blob sha1
  との照合で **14/14 entry byte-exact**（part 11件 + 単一ファイル3件）。
- 各証明書を `verify_win7_certificate_bigint_independent.mjs`（BigInt 3×3
  余因子展開、探索器・cache・浮動小数点なし）で検証: root 7石・安全、行は
  厳密増加・一意、全sub-root PASS == 独立交差の合法初手列挙（51/58/53/55/54/60）、
  戦略/消費行和集合 0/0 双方向、終局石数13〜17。
- rows/sub_roots/md5/bytesは公開reconciliation JSON記録と全件一致
  （33,992 / 52,755 / 36,406 / 43,005 / 39,873 / 47,165行）。
- 記録: [class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json)。
- 既にchain基準内でfold済みのmanifest証明書 bits 94/20/23も同様に再検証し、
  merged集合に対してmarginal 0（正の重複照合）をassertした。

## unified merge

[recompute_frontier_unified_merge_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_unified_merge_20261115.py):

0. runpy merged recompute
   `recompute_frontier_merged_after_multiband2_68dhyg_20261115.py`: **公開
   merged 1148 head（1148/6699/528423/4969/392146、commit 19bb2abc）を
   byte-identicalに再現**（再生成frontier JSONのmd5 `4a3a8693…` をmain値と
   照合）し、`s_1148 == s_1117 | s_1140` のunion恒等式をassert。spec
   version-bの「reproduce the merged 1148 endpoint byte-identically」制御を
   直接満たす。
1. runpy cost-68d recompute: 1109基準 + 1117 endpoint、13 receiptを公開順で
   fold（記録・sweep再集計・determinism・v15 anchorは同スクリプトが全件
   self-assert）。
2. runpy warm multiband2 recompute: 1140 endpoint（31記録をself-assert）。
3. 50 receiptのthree-way root disjointnessをassert（68d群は重複対
   71b-1 == 61d-22を除く12 root + 31 + 6）。
4. 31 multiband2 receiptを公開記録順で1117の上にfold。各記録の
   marginal-in-manifest hex集合が公開multiband2 additionと全件一致
   （batch2×68dのmarginal disjointnessの再確認）: +31。fold後の集合が
   merged 1148 headと集合として一致することもassert（独立再導出）。
5. cost-70c warm 6 receiptをgreedy順 105, 92, 40, 24, 11, 8 でfold
   （reconciliation JSON × 独立BigInt検証 × ローカルbyteの三重assert）: +6。
6. set-equality制御 `s_merged == s_1117 | s_1140 | covers(6)` と
   `s_merged == s_1148 | covers(6)` の両方をassert。
   solved == **1154** == 1109 + 8 + 31 + 6。

2回実行でbyte-identical（frontier JSON md5 03706c32…、ranking CSV
6443e049…、top-candidates CSV d91935ff…。CSV 2件は拡張前の実行時点と
同一byte）。

## unified frontier

- **解消S6 1,154 / 残り 6,693 / 費用 527,949 / open需要 4,963 / 391,672**
- 第三class-2 coverableターゲット S5 `00000000000000809102000000000000`:
  12軌道・871（1140時点）→ **8軌道・588**。
- audit-blocked class2 `00000000000000809082000000000000` は不変（10軌道・698）。
  best class4 `00000000020000003800000080000000` も不変（18軌道・1,460）。

## cost-69f raw sweepの独立再集計（未fold・次回統合対象の前倒し監査）

並走レーン公開のcost-69f raw batch 1–9を独立再集計し、sweep-audit記録と
完全一致を確認: 69候補、9 pilot（全3,402 nodes）、**WIN7-D10 9件（bits
2/20/44/68/69/94/109/118/119）+ REFUTED 60 + capped 0、候補節点
112,752,229**。対象child `00000000000000809102000000000008`（cost 69）は
第三class-2ターゲットの最安未sweep子（demand c1=0,c2=2,c4=0、1140時点の
top-candidates表で会員性を再導入済み）。証明書抽出・foldは69fレーンが
公開するまで未fold。この9 receiptがfoldされると第三ターゲットはさらに
縮小する見込み。

## 未完・次回

- cost-69f: 9 WIN7証明書の抽出・検証・foldは69fレーン（公開後に次の
  unified mergeへ統合）。本セッション終了時点で
  `class2-lane-cost69f-certificates/` にはbit20の1件のみ公開済み
  （9件の途中）。全件公開後の次のunified mergeでfoldする。
- cost-70c: WIN7 bits 3/42/86/103 が未認証（warm rebuild候補）。
- cost-65h/67b/68c warm候補とin-flightのcost-65j sweepは並走レーンの
  バンド（marginal一覧は class2-lane-warm-candidate-ranking2 JSON）。

## 同時実行（collision記録）

本セッションのpush（625b0e0c、20:51:40Z）の約4分前に、並走レーンが同一の
fold仕様を独立実行して同一パスへpush済みだった
（7aaa7d83、20:47:56Z、log
[2026-11-15-n11-class2-unified-merge-50-receipts.md](2026-11-15-n11-class2-unified-merge-50-receipts.md)）。
push前のcollision確認listが7aaa7d83より古かったため、本pushは同一パスの
4ファイル（スクリプト・frontier JSON・CSV 2件）を上書きした。両実装は
同一fold順・同一制御・同一endpoint **1,154/6,693/527,949/4,963/391,672**
に到達しており、2実装一致はfold算術の正の交叉検証である。現行mainの
ライブファイルは本push版（merged 1,148 head byte-identical再現制御と
cost-70c warm6独立検証JSONを追加で含む）。詳細と教訓はK0783の
2026-11-15 collision記録節に記載。

## 次回fold予測（69f・70c残り、1154 headに対する事前測定）

[predict_next_fold_marginals_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/predict_next_fold_marginals_20261115.py)
が、chain head 1154に対して未fold群のmanifest内marginalをcovers()から再導出
（記録: [class2-lane-next-fold-marginal-prediction-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-fold-marginal-prediction-20261115.json)）:

- **cost-70c残り bits 3/42/86/103: すべてmanifest内marginal 0**（bits 3/103は
  完全被覆済み・bits 42/86は非manifest軌道のみ）。抽出してもfrontierは
  進まない（band認証 13/13 完成の帳簿価値のみ）— gain-0 warm候補。
- **cost-69f 9 bits: growing-union fold順（bit順）のシミュレーションで
  distinct manifest 9 hex、bit20はchild既被覆でmarginal 0（正の重複）**。
  予測: 証明書全件公開・独立検証後にfoldされれば
  **1154 → 1,163/6,684/527,280/4,954/391,003**。
  第三class-2ターゲット S5 `00000000000000809102000000000000` は
  **8軌道・588 → 7軌道・519**（sweep済みchild `…0008` がremainingから離脱し、
  次の最安未sweep子は `00000000000000809102000000002000` cost 69・
  c1=0,c2=2,c4=2）。audit-blocked（10/698）とbest class4（18/1,460）は不変。
- 予測は69f証明書の公開・独立検証を条件とする帳簿算術であり、勝敗の主張を
  含まない。

## 勝敗に関する明記

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、class 4
はすべてUNKNOWNのままである。**WIN7証明書は個別7石rootの深さ10以内のWIN
のみを証明し、solved数（1,154）はmanifest被覆の帳簿上の前進であり、空盤や
二石rootの勝敗・距離を意味しない。
