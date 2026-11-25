# n11 class2: cost-72bの13 WIN7-D10全証明書化・独立検証・公開（証明書636,225行）

2026-11-15 JST。cost-72b子sweep（`class2-lane-cost72b-sweep-20261115.json`、13 WIN7-D10探索候補・証明書未抽出）の13 root `child 00000000000000809102000002000000 | 1<<bit` すべてにrepo形式の戦略証明書を抽出し、汎用独立検証器で全件PASS、公開した。**chain head 1,163へのfoldは未実施**（次の必要作業）。

## 抽出

- engine: repo-verbatim `class4_child1_cert_extractor_exact.ts`（FBS 1<<20・fbtDrops計数・drop時はfatalでrows不書き出しの自己防護付き）、1 bit = 1 nodeプロセス、敵初手は `legal_candidates.py`（独立Bareiss 4x4）の全合法手。
- 敵初手数（= sub-root数）: bits 2/11/21/30/31/36/47/66/85/95/97/100/106 に対し 62/52/61/55/51/51/57/58/55/56/47/60/64（root-checkと全件一致、計729）。
- **13/13抽出成功・fbt_drops全件0・全敵初手ok・終局石数[13,17]**。kill tableはrepo CLI既定のKILL_BIT7 pref hints（一致する敵初手のみ探索順に影響、verdict cache不使用。正しさは抽出の自己検査と独立検証で担保）。

## 検証（verify_bit7_win7_cert.ts: 整数Bareiss 4x4・engine不使用・cache不使用）

- **13/13 PASS**: root安全性（7石・共円4点なし）、全sub-rootの完全戦略リプレイ（敵は全合法手展開）、消費行union = 証明書行集合（**missing 0 / extra 0 全件**）、行sorted-unique、終局石数13〜17。
- 合計 **636,225戦略行・729 sub-root・訪問1,378,650局面・終局224,802・敵応答edge 1,241,817**（winner 889,294 + loser 264,554 + terminal 224,802 = visited、全bitで整合）。
- 抽出節点合計 **200,029,509**。v15 cross-engine anchor 13/13 loss=true（計132,170,428節点）とv16決定性再実行13/13 node-exactはsweep record由来。

## 公開と検証

- 13証明書（1.13〜2.52MB）のうち6件（bits 2/21/66/95/100/106）はrepo慣例の2分割（行境界・連結md5==全体md5検証済み）、7件は単一ファイル。**19 partを1コミット1 part、(1/19)..(19/19) でpush**。
- push直前のcollision checkでtarget dir不在を確認。push後、**19 remoteファイル全件をraw fetchしてgit blob sha照合、19/19 byte-exact**。
- 事故記録: sandbox memory limit (16 MiB) が5件のpushプログラム（bit30/31/36/47/85）でpush_files実行後にabortしたが、いずれも着地済みでremote照合で問題なし。切り分けのためmanifestのincident_noteに記録。

## 意味と境界

- 13 rootはこれで「探索候補」から「独立検証済み証明書付きWIN7-D10」へ確定した。root恒等式 `root == child | 1<<bit` は全件で照合済み。
- **S6 frontierへの寄与はまだ0**: 子軌道 `00000000000000809102000002000000` の被覆と交差軌道liftのfold（chain head 1,163基準のrecompute）が次の必要作業。69fと同様、13 receiptはsweep+v15 anchorで既にfold可能な材料である。
- WIN7証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。六石子・S5親・S2 {59,60}・空盤の勝敗は確定しない。

## 成果物

- [証明書manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-win7-certificates-20261115.json)
- [証明書ディレクトリ](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-certificates/) — 19 files
- [pipeline script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cost72b_cert_pipeline_20261115.sh)

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続きUNKNOWN。**
