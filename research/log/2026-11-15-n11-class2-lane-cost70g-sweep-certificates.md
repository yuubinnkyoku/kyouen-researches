# 2026-11-15：cost-70g sweep 完成（8 WIN7-D10 / 62 REFUTED）と全8証明書の blind 抽出・独立検証・push

開始時main: cost-70e receipts fold 済みの canonical head `1233/6614/522131/4884/385854`（claim `class2-lane-cost70g-inflight-20261115.json` は本セッション前半で IN FLIGHT push済み、sweep 9バッチ完了・v16 determinism rerun 済みの状態から再開）。AGENTS.md、research/knowledge/README.md、11×11関連claim・logを確認した。

## 成果1：v15 cross-engine anchors 11/11 判定一致

repo-verbatim `class4_child1_runner.ts`（v15、remote blob `8744fc65b6b7cac6bd561403ce4c749e01c51359`、ローカルコピーをgit blob shaでbyte-exact検証）を child `00000000000100809002000000000800` に depth 10 / cap 5e7 で実行した。

- **全8 WIN7 bits（9/20/29/34/62/70/76/119）が v15 でも loss=true**。v15 nodes: bit9 10,273,907 / bit20 1,523,082 / bit29 10,750,468 / bit34 10,250,857 / bit62 4,821,985 / bit70 1,408,183 / bit76 9,482,275 / bit119 7,787,565。
- **最重REFUTED 3アンカー（bits 6/86/98）も v15 で loss=false**（12,630,899 / 13,387,147 / 10,102,917 nodes）。**11/11 verdicts が v16 と一致**。
- pilot d6 control（loss=false @ 5,949 nodes）11回すべて PASS。terminal stone range [13,17] 全行一致。v15総nodes 92,419,285。
- 出力 `class2-lane-cost70g-v15-crosscheck-20261115.jsonl` をpush。

## 成果2：raw batches・determinism rerun の repo 反映

- `class2-lane-cost70g-raw-batch{1..9}-20261115.jsonl`（9 batches 8×8+6、pilot 3402 PASS ×9）をpush。総nodes 63,592,195、WIN8件（win-node sum 15,922,270）、REFUTED 62、capped 0。
- `class2-lane-cost70g-v16-determinism-rerun-20261115.jsonl`（batch5の別プロセス再実行、WIN bit62含む全8 bit + control node-exact PASS）をpush。
- batch6–8のpushは一時的に502となったが即時retryで着地。

## 成果3：sweep record JSON と claim 更新

- `class2-lane-cost70g-sweep-20261115.json`（v1→v2）を作成・push: 8 WIN7-D10（bits 9/20/29/34/62/70/76/119）+ 62 REFUTED + 0 capped、heaviest bits 6/9/34/86/98/1、determinism rerun、v15 crosscheck、**duplicate_root_check: 8 WIN7 root hexのGitHub code search 8/8 で 0 hits（新規coverage）**、fold PENDING明記。
- `class2-lane-cost70g-inflight-20261115.json` をv2（sweep completed）→v3（sweep + certificates completed、fold pending）へ更新。

## 成果4：全8 WIN7 root の証明書 blind 抽出・独立検証・byte-exact push

- extractor: repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`（remote blob `5518d375fc6b4a7a14c22a1a65586f0c1c5731c0`、ローカルgit blob sha一致）。driver: `cert_driver70g.ts`（`cert_driver70e.ts` blob `085fe754404f2df3abe8affc50a53e03395f8d7d` のimport行とコメント3行のみ差分）。
- root loser手は BigInt 3×3 余因子展開で独立列挙（mobility 60/46/54/63/51/49/55/56）。**blind（空kill table）抽出、FBS 1<<20、全root fbt_drops 0、fatal なし**。
- 証明書: bit9 51,456 rows / bit20 16,902 / bit29 44,195 / bit34 56,345 / bit62 26,591 / bit70 19,456 / bit76 45,917 / bit119 41,408。**総 302,270 rows / 31,812,232 extraction nodes**。
- 独立検証: `verify_win7_certificate_bigint_independent.mjs`（remote blob `62b5d9413daafb172f6e10249976ee6808f7b454`）で**8/8 PASS**。root stones=7 + safe、loser mobility一致、全sub-roots PASS（=root mobilityと一致）、union missing/extra 0/0、rows sorted unique、terminal range [13,17]。
- push: `class2-lane-cost70g-certificates/bit{B}-root-{HEX}.cert` 8件、**全8件のremote blob shaがローカルgit hash-object と byte-exact 一致**（bit20 `b2a83239…`、bit70 `d522d9eb…`、bit62 `1c023a37…`、bit119 `b5a42979…`、bit29 `bab4338b…`、bit76 `63a6c8b4…`、bit9 `1877c1c6…`、bit34 `e95fcaf5…`）。目安として 1.5–2MB ファイルのpushはread_file 1500行 pagingで実施（run_typescriptの16MiB記録制限により、push自体は実行完了後にプログラムエラーとなる場合があるが、着地はディレクトリlistingのblob sha照合で確認する運用を確立）。
- サマリー `class2-lane-cost70g-win7-certificates-20261115.json`（per-bit rows/nodes/mobility/verify詳細、blob shas、総計）をpush。

## 並走状況（本セッション終了時点）

- **cost-70f**（child `00000000000000801202000002200000`、round 2並走）: raw batch 1–9 + determinism rerun がmainに着地済み。sweep record JSON・証明書はまだ未着地。
- **cost-65l receipts fold**: 依然 IN FLIGHT（head-1227ベース）。bit21/48の証明書抽出サマリー・verify JSONは着地済み。
- **cost-71c**: 別並走のraw batch 1–9着地済み。**cost-72b**: sweep・証明書・fold（receipts-recompute・after-72b CSV）まで着地済みの模様。head統合の状況は次回必ず確認する。
- **cost-70g fold は意図的に未実施**: 70f sweep record と 65l fold の着地待ち。両open class-2 parent（`00000000000000801202000000200000` 28 rows / 2119 と `00000000000000801202010000000000` 60 rows / 4342）を同時に進めるreceiptsが確定している。

## 勝敗status

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1、class 2、class 4 はすべて **UNKNOWN**。REFUTED-D10 はWIN7-D10不在のみを証明し（LOSS証明ではない）、WIN7証明書8件は個々の7石rootからdepth 10以内の勝ちのみを証明する。いかなるfrontier数も本sweep・証明書だけでは変化しない（fold待ち）。
