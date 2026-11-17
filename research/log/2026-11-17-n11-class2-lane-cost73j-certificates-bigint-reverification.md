# 2026-11-17 n11 class2-lane: cost73j証明書16本 BigInt独立bytes再検証

## Context

並走laneが cost73j (child `00000000000000403800000408000000`, cost 73,
stones [27,34,59,60,61,70]) の sweep完走 (16 WIN7-D10 + 57 REFUTED-D10,
0 capped) → 証明書16本 (総rows **726,778** / 総抽出nodes 166,238,087 /
出版bytes 26,236,851) → manifest (git blob `e88710b5`) → claim v3
(git blob `74fc3417`) まで出版済み (commits `b91143cb`..`e6406ff2`,
`3b8d9043`)。本レーンは cost72d と同じ第3実装BigInt verifierによる
独立bytes再検証パターン (commit `a02b8ac0`) を73jに適用した。

## What was done

1. **ミラー構築** (pin commit `8803a3b0`): band dir
   `class2-lane-cost73j-certificates/` 77ファイル (manifest + 30 cert
   files [14 split pair + 2 whole (bits 69/82)] + 16 rootcheck.json +
   16 subroots.jsonl + 14 README-split) をcommit固定raw CDN URLで取得し、
   GitHub contents API listing (name|sha|size) と **77/77 git blob
   sha照合 PASS** (mismatch 0)。
2. **script** `reverify_cost73j_certificates_bigint_20261117.py`:
   - manifest: schema/child/cost 73 assert。basisのclaim v2 blob
     (`8324f1d8`) 記載assert。totals再現 (rows 726,778 /
     extraction_nodes 166,238,087 / published_bytes 26,236,851 /
     fbt_drops_total 0 / capped_per_move_total 0)。
   - claim v3 (`74fc3417`): mirror blob sha照合、schema v3、
     win7_d10_bits == manifest bits [0,1,6,29,44,49,52,69,74,82,87,91,
     98,100,110,118]、manifest path一致、**status文中のmanifest blob
     (`e88710b5`) とmirror manifest実blobの相互照合**。
   - 73jのwhole fileはcertificate_split注記がnullでなく
     「N bytes within the 1200000-byte whole-file threshold; published
     whole」形式 → Nを実ファイルサイズと照合する新checkを追加。
   - split証明書: part1行境界 + split_cut_byte一致 + joined md5/sha256
     両方照合 + README-split (whole bytes/分割境界/md5/root) 照合。
   - **BigInt verifier** (verify_win7_certificate_bigint_independent.mjs,
     blob `62b5d941`, argv[3]=期待mobility) 16本: **16/16 PASS**。
     verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/
     terminal [13,17]/strategy_rows/subroots_passed/root_mobility/
     consumed_winner_rows 全フィールド一致。
   - **sidecar合意**: subroots.jsonl (batched, 最大8 m-key/行) の
     sum(seen)==visited_states_across_subroots・
     sum(terminals)==terminal_count・
     sum(opponentEdges)==loser_reply_edges が16/16で一致。
     m-key総数 **907** == subroots_pass == loser_mobility
     (per-bit mobility 58/56/54/59/62/56/62/51/57/48/62/51/62/53/59/57)。
   - **独立D4正準化 (第8実装)**: 16件のd4_canon_root全再現、
     raw_is_canon整合、16 canon相互不重複。
   - **cross-batch不交差**: 113 earlier roots (singlefile 43 +
     splitpart bands 18 + sweepbands 24 + 66j/69j 15 + 63cd 2 + **72d 11**、
     全6ファイルblob pin照合) に対しroot/D4 canon両方で重複0。
     73jの16 WIN canonは全て新規 (census v1でopen 73/0 harvestedと整合)。
3. **結果**: 16/16 PASS、file pins 78/78 (77 band + claim v3)、
   manifest md5/sha256 mismatch 0、pin blob sha mismatch 0、
   sidecar cross-agreement fail 0。
4. **決定性**: 2回実行で出力byte-identical (md5 `9afeb213...`、
   38,712 bytes)。単一実行~30秒/4 worker。

## Interpretation guard

bytes再検証済みpopulationは **311 + 16 = 327 records**。frontier数字は
不変で、いかなるmanifest行も閉じない。73j receipt foldは
76c→66i→66j→69j→71e→72d→73i folds完了まで着手禁止 (並走管理)。
WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10 (73jの57 bit) はLOSS証明ではない。solved 1452/1472は
manifest被覆の簿記である。11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はいずれも UNKNOWN のまま。
