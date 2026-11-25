# 2026-11-15：cost67c sweep完了・WIN7証明書2件の抽出・検証・公開（foldは次回）

入力取得時main: `cd6520093a`（cost67c sweep audit着地直後）を起点に、同一セッションでclaimからsweep・証明書抽出・検証・公開・claim v2更新まで実施。実行中に並走レーンのcost-73f claim（`f391d73686`）が着地したが、本レーンの対象ファイルと競合しなかった。規約どおりbranch・PRは作らずmainに直接反映。

## 対象

- 子S6: `00000000000000801202000000202000`（石 13,21,49,57,60,71）、edge cost 67、需要 c1=0, c2=1, c4=1（混合需要: 類2 parent1 `00000000000000801202000000200000` 33/2470 lift石13 ＋ 類4 S5 `00000000000000801002000000080800` 76/5703 lift石57）。
- head 1216時点でparent1の最安未sweep子。重複claim無しをGitHub code searchで事前確認済み。

## sweep（v16 runner, depth 10, cap 1e9, andclose 1）

- 67候補、**WIN7-D10 2件（bits 64, 96）**、65 REFUTED-D10、打切り0、合計 41,942,979 節点（WIN合計 2,368,197: bit64 1,393,667 / bit96 974,530）。全terminal石数範囲 [13,17]。
- pilot管理: 9バッチすべて d6 pilot loss=false nodes=3402 PASS。
- determinism: batch5再実行 8/8 node-exact。
- v15交差検証（別実装 v15 runner, pilot 5949×5）: WIN bits 64/96 loss=true（bit64 5,068,403節点 / bit96 2,436,013節点）、REFUTEDアンカー bits 1/32/116 loss=false、raw判定と完全一致。
- raw batch 1..9（9ファイル）、sweep audit、determinism rerun、v15 crosscheckをすべてpush、raw取得でbyte-exact確認済み。

## WIN7証明書2件（抽出・検証・公開）

抽出は `cert_driver63g.ts`（repo-verbatim extractor、kill table 空、fbt_drops 0）。

| bit | root | rows | bytes | extraction nodes | sub-roots |
|-----|------|------|-------|------------------|-----------|
| 64 | `00000000000000811202000000202000` | 34,583 | 1,249,941 | 7,018,550 | 53 |
| 96 | `00000001000000801202000000202000` | 35,897 | 1,296,064 | 4,536,424 | 53 |

- BigInt独立検証器 `verify_win7_certificate_bigint_independent.mjs` 2/2 PASS（bit64: subroots 53/53, union conflict 0/0, terminal [13,17], visited 72,383 / winner 46,475 / loser 14,045 / loser-reply edges 65,414 / terminal 11,863。bit96: subroots 53/53, union 0/0, [13,17], visited 75,928 / winner 48,819 / loser 14,516 / reply edges 67,109 / terminal 12,593）。
- 第二独立検証（perm-det4 Bareiss 整数4×4行列式）2/2 PASS: root loser mobility 53 = sub_roots_total = len(loser_first_moves)、per-node mobility一致、子がrootのd4 parent orbits（各7軌道）に含まれる。D4正準形は bit64 `00000000000000809102000000080800`、bit96 `00000000040000809002000000080800`。
- GitHub code search: 両root hexとD4正準形は既存公開rootとdisjoint（0 hits、重複公開なし）。
- 公開: 両証明書とも1MB超のためbit113と同じく2分割（part1of2/part2of2）で時計の併合がwholeとmd5一致することを確認してpush。remote git blob sha 4件すべてbyte-exact照合済み。
- 証明書manifest `class2-lane-cost67c-win7-certificates-20261115.json`（totals: 2証明書 / 70,480行 / 2,546,005 bytes / extraction 11,554,974節点 / sub-roots 106 / v15 crosscheck合計 7,504,416 / v16 WIN合計 2,368,197）をpush、byte-exact確認済み。

### push上の事故と復旧

4つのpartファイルを最初に誤ってrepo直下 `output/class2-lane-cost67c-certificates/` にpushしてしまった（正しくは `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/` 配下）。正パスへ再pushした上で誤配置4ファイルを削除コミットで除去し、誤パスのディレクトリはmainから消滅（削除直後のraw 200応答はCDNキャッシュ）。manifestの `controls.misplaced_path_cleanup` に記録。

## claim更新

`class2-lane-cost67c-inflight-20261115.json` をv2へ更新（status `sweep_and_certificates_complete_fold_pending`）。sweep_results・win7_certificates・rebase_target（fold時点の最新canonical headをassertしてからfold。並走のcost-65l foldが先に着地した場合はそのheadにrebase）・next_action（fold script作成→実行→claim retire）を記載。remote blob sha `0b98e003fae000bb663e8b5a4d7f6ad5954cedc3`、API取得でv2着地確認済み。

## foldは次回実行

並走のcost-65l fold（証明書公開中、bits 21/48）が先にheadを進める可能性が高いため、67c foldは次回実行時に最新headへrebaseして行う（63gと同じ手順）。証明書だけではfrontier計数は不変。

## 信頼境界

- WIN7証明書は「個々の7石rootからdepth 10以内の先手勝ち」のみを証明する。REFUTED-D10はWIN7-D10の不在のみを証明し、勝敗（LOSS）判定ではない。solved数はmanifest被覆のみを測る。
- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定も変更しない。

## 再現

```sh
node --experimental-strip-types scripts/class4_child1_runner_v16.ts --child 00000000000000801202000000202000 --bits 64,96 --depth 10 --cap 1000000000 --andclose 1 --out FILE
node --experimental-strip-types scripts/cert_driver63g.ts 00000000000000801202000000202000 64 OUT 0,1,2,...,118  # 53手（second-check-results.json の bareiss_mobility_moves）
node verify_win7_certificate_bigint_independent.mjs CERT 53
```

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、類2・類4はすべて **UNKNOWN**。今回のsweep・証明書公開は勝敗判定を変更しない。
