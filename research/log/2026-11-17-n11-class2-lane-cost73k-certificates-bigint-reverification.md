# 2026-11-17 n11 class2-lane: cost73k証明書22本 BigInt独立bytes再検証

## Context

本レーンが cost73k (child `00000000000000801206000000000400`, cost 73,
stones [10,49,50,57,60,71], census v7 rank-1 row) の sweep完走 (25
WIN7-D10 + 48 REFUTED-D10, 0 capped, claim v2 git blob `2150277f`,
sandbox reset後のraw再生成・並走record 73/73一致) → 証明書22本 (総rows
**966,535** / 総抽出nodes 155,946,109 / 出版bytes 34,933,538) →
manifest (git blob `0892aed0`, commit `4c383a14`) → claim v3 (git blob
`7f654548`, commit `795e2941`) まで出版済み (band commits
`40f8db4b`..`4c383a14`)。引き続き cost72d/73j と同じ第3実装BigInt
verifierによる独立bytes再検証パターン (commits `a02b8ac0`,
`56ce29e0`) を73kに適用した。

出版時の注記: band最初の2 commitは出版ツールのchunk境界newline混入で
汚染されていたため即座にrepushして修正した (repushが正当なファイル)。
着地は41/41証明書ファイル全てについてローカル抽出md5 vs git blob shaで
byte-exact照合済み。今回の再検証はローカル成果物ではなく
commit固定raw CDNミラーから全ファイルを再取得して行った。

## What was done

1. **ミラー構築** (pin commit `795e2941`): band dir
   `class2-lane-cost73k-certificates/` 105ファイル (manifest + 41 cert
   files [19 split pair + 3 whole (bits 39/41/62)] + 22 rootcheck.json +
   22 subroots.jsonl + 19 README-split) をcommit固定raw CDN URLで取得し、
   GitHub listing (name|sha|size) と **105/105 git blob sha照合 PASS**
   (mismatch 0)。
2. **script** `reverify_cost73k_certificates_bigint_20261117.py`:
   - manifest: schema/child/cost 73 assert。basisのclaim v2 blob
     (`2150277f`) 記載assert。totals再現 (rows 966,535 /
     extraction_nodes 155,946,109 / published_bytes 34,933,538 /
     fbt_drops_total 0 / capped_per_move_total 0)。
   - claim v3 (`7f654548`): mirror blob sha照合、schema v3、
     actual_execution/results/win7_d10_bits == 25 WIN bits (manifest 22
     sweep WIN bits + confirmation bits [14,26,55] は73j/73i/69j証明書で
     被覆)、manifest path・manifest_blob_sha一致、**status文中のmanifest
     blob (`0892aed0`) とmirror manifest実blobの相互照合**。
   - whole file (bits 39/41/62): 「N bytes within the 1200000-byte
     whole-file threshold; published whole」注記のNを実ファイルサイズと照合。
   - split証明書: part1行境界 + split_cut_byte一致 + joined md5/sha256
     両方照合 + README-split (whole bytes/分割境界/md5/root) 照合。
   - **BigInt verifier** (verify_win7_certificate_bigint_independent.mjs,
     blob `62b5d941`, argv[3]=期待mobility) 22本: **22/22 PASS**。
     verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/
     terminal [13,17]/strategy_rows/subroots_passed/root_mobility/
     consumed_winner_rows 全フィールド一致。
   - **sidecar合意**: subroots.jsonl (batched, 最大8 m-key/行) の
     sum(seen)==visited_states_across_subroots・
     sum(terminals)==terminal_count・
     sum(opponentEdges)==loser_reply_edges が22/22で一致。
     m-key総数 **1,257** == subroots_pass == loser_mobility
     (per-bit mobility 63/59/58/62/60/47/51/56/55/51/60/57/61/54/54/56/
     57/61/61/52/59/63)。
   - **独立D4正準化 (第9実装)**: 22件のd4_canon_root全再現、
     raw_is_canon整合、22 canon相互不重複。
   - **cross-batch不交差**: 129 earlier roots (singlefile 43 +
     splitpart bands 18 + sweepbands 24 + 66j/69j 15 + 63cd 2 + 72d 11 +
     **73j 16**、全7ファイルblob pin照合) に対しroot/D4 canon両方で
     重複0。
3. **結果**: 22/22 PASS、file pins 106/106 (105 band + claim v3)、
   manifest md5/sha256 mismatch 0、pin blob sha mismatch 0、
   sidecar cross-agreement fail 0。
4. **決定性**: 2回実行で出力byte-identical (md5 `aa472e1b...`、
   50,977 bytes)。単一実行~35秒/2 worker。

## Interpretation guard

bytes再検証済みpopulationは **327 + 22 = 349 records**。frontier数字は
不変で、いかなるmanifest行も閉じない。73k receipt foldは
76c→66i→66j→69j→71e→72d→73i folds完了まで着手禁止 (並走管理)。
WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10 (73kの48 bit) はLOSS証明ではない。11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はいずれも UNKNOWN のまま。
