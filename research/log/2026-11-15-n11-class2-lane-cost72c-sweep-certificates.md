# 2026-11-15：cost-72c sweep 完成（9 WIN7-D10 / 63 REFUTED）と9証明書の blind 抽出・二重独立検証・byte-exact push・manifest破損の検出と修復

開始時main: HEAD `c18ee6f5`（71c receipts fold・parabola census・70e証明書着地後）。canonical baseline head `1235/6612/521988/4882/385711`（`class-frontier-cost71c-receipts-recompute-20261115.json`・blob `61af2eb3…`）。AGENTS.md、research/knowledge/README.md、11×11関連claim・log・knowledgeを確認してから再開した。

## 対象選定

- 第三coverable class-2 target S5 `00000000000000809102000000000000` の残2行（cost-69/74）は**並走laneがcost-69g/74eとしてIN FLIGHT主張済み**のため衝突回避で放棄。
- cost 50-64の安い行は開親が30行超で戦略価値が低い。
- parent1 `00000000000000801202000000200000`（第二coverable class-2 target・head-1235で26行/1976）の各行を精査し、65k（sterile済み）・65l（fold IN FLIGHT）・70f・70g（証明書済み・fold未）を除く最安の未sweep行として **cost-72 child `00000000000000801202000000220000`**（レーン名 cost-72c。72・72b使用済み）を選んだ。
- child: 石 [17,21,49,57,60,71]・safe・edge cost 72（= legal 72とbit-exact一致）・需要 c1=0,c2=2,c4=0。開親は2つともclass-2: del17 = parent1 bit-exact（26行/1976）・del21 → D4正規化で `00000000000000083800000008000000`（55行/4111）・残り4削除（49/57/60/71）は閉行。**両開親がclass-2の需要行**である点がこの行の価値。

## 成果1：v16 sweep 完走と二重engine統制

- claim v1（IN FLIGHT・head 1235 baseline・manifest edge cost 72）をpush（`aa7e7cdc`）。
- v16 runner（blob `0a4a86f6…`）で9バッチ×8 = 72候補をsweep: **WIN7-D10 9ビット [1,7,24,39,59,64,67,72,96]・REFUTED 63・capped 0・総nodes 61,297,942**・pilot 3402×9 PASS。batch5 determinism rerun は node-exact。
- v15 cross-engine（blob `8744fc65…`）で12アンカー全一致: 9 WIN は loss=true、REFUTEDアンカー bits 0/43/117 は loss=false、pilot 5949×3。
- raw 13ファイル（9 batch JSONL + determinism rerun + 3 crosscheck JSONL）をpush（`76b22be3`、末尾改行1件修正 `b679fb5f`）、着地byte-exact確認済み。

## 成果2：9証明書の blind 抽出と二重独立検証

- repo-verbatim extractor（blob `52bcaf50…`）+ `cert_driver72c.ts` で9 WIN rootの証明書を blind 抽出（pref=null・空kill table）: **総extraction nodes 41,346,462・総strategy rows 321,781・fbt_drops 0**・loser mobility 61/47/59/46/53/52/53/47/56（bits 1/7/24/39/59/64/67/72/96）。
- BigInt検証器 `verify_win7_certificate_bigint_independent.mjs`（blob `62b5d941…`）: 9 rootすべて union missing/extra 0/0・terminal [13,17] PASS。
- Python/Bareiss検証器 `verify_cost72c_win7_bareiss_independent.py`（stdlibのみ・Bareiss 4×4整数行列式・全loser応手展開・戦略行集合の厳密閉包）: 9 rootすべて union 0/0・terminal stone range {13,15,17} PASS。
- 16MiB push制限のため各証明書を行境界で2分割し、**18パートを1ファイルずつpush**（`3899ae43`〜`06312327`）。join md5 = 全体md5 を全9件で検証し、remote md5照合も18/18 OK。

## 成果3：独立 raw-sweep 監査

`audit_cost72c_raw_sweep_20261115.py`（71c監査の定数差し替え・Python stdlibのみ・Bareiss整数行列式・repo solver不使用）を書いて実行し、全assert PASS:

- 72候補を独立再列挙しclaim列挙とbit-exact一致。child stones [17,21,49,57,60,71]・child safe・batch bitsはclaimのengine計画と完全一致。
- aggregate再導出: WIN7-D10 9・REFUTED 63・capped 0・総nodes 61,297,942（raw 13ファイルから）。
- 一石削除 D4 lift: del17 = parent1 bit-exact・del21 → `00000000000000083800000008000000`・残4削除はhead-1235 ranking CSVに存在しない閉行。head-1235 ranking（175開行）・top-candidates CSVのparent行・需要行（c1=0,c2=2,c4=0・edge cost 72）cross-check PASS。
- D4 duplicate scan: **67個の公開 win7-certificates manifest・192 canonical rootsと比較して0重複**（9 WIN rootはすべて新規coverage）。

## 成果4：claim v2・manifest・README・検証記録のpush

claim v2（schema v2・sweep+証明書+監査完了・**fold PENDING**明記）・sweep audit JSON・win7-certificates manifest・certificates README・18件のverify records・cert_driver72c.ts・Bareiss検証器・監査スクリプトを1コミット（`d68f490d`）でpushした。

## 成果5：manifest内容破損の検出と修復（運用インシデント記録）

`d68f490d` の着地byte-exact検証で2件の不一致を検出し、いずれもpush側の問題だった:

1. **manifest破損**: `class2-lane-cost72c-win7-certificates-20261115.json` が誤って26行の内容（marker captureの解析ずれでbit1 BigInt検証recordの内容が流れ込んだもの）で着地していた。正しい593行内容を `2877a710` で再pushし、remote md5照合でbyte-exactを確認。
2. **監査スクリプト誤path**: 内容はbyte-exactだったが `output/scripts/` に着地していた（相対OUT解決も壊れる）。`2877a710` で慣行の `scripts/` に再pushし、誤pathコピーを `89d748be` で削除。

これにより**本レーンの25ファイルすべてがbyte-exact着地検証済み**。教訓: 多ファイル一括content captureの終端marker解析はずれることがあり、以後は単ファイルの直接読み取りpushに切り替える（今回の修復pushで実践）。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。63 REFUTEDはchild S6行を閉じない。
- 9つのWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。**本レーンのreceiptsはfold前のため、本レーンの成果だけではfrontier数を変えない**（なお本session中に並走laneの70f foldが着地し、canonical headは1235 → 1239/6608/521701/4878/385424に移動した）。両開class-2 S5親（parent1 24行/1836〔70f fold後〕・`00000000000000083800000008000000` 55行/4111）もどちらも解決していない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- foldは次回session: 9 receipts（bits 1/7/24/39/59/64/67/72/96）をfold。**本session中に並走laneのcost-70f foldが着地し、canonical baselineは71c head 1235から `class-frontier-cost70f-receipts-recompute-20261115.json`（head 1239/6608/521701/4878/385424・同じ71c鎖上の伸長でmerge不要）に移動した**。72c foldはこの新baselineに対して行うこと（fold scriptは71c版の定数差し替え）。
- 70f foldの影響: parent1 `00000000000000801202000000200000` は 26行/1976 → **24行/1836**（70f child `00000000000000801202000002200000` 行を喪失）。72c child `00000000000000801202000000220000` は新baselineでも残存・未解決。fold時にchildの残存と parent1 24行/1836・parent2 `00000000000000083800000008000000` 55行/4111 を再assertすること。
- fold前に必ず最新mainを再取得し、**並走laneのpending folds（70g 8証明書・65l・72c〔本レーン〕・in-flight 69g/65j/74e）の着地状況を確認**すること。着地済みの場合は併合が必要になる。

詳細: [sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-sweep-audit-20261115.json)、[certificate manifest](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-win7-certificates-20261115.json)、[claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-inflight-20261115.json)、[certificates README](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-certificates/README.md)、[sweep audit script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost72c_raw_sweep_20261115.py)。
