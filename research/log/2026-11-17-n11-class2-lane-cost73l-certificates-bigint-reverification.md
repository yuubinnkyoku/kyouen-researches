# 2026-11-17 n11 class2-lane: cost73l証明書32本 BigInt独立bytes再検証

## Context

本レーンが cost73l (child `00000000000000c09002000000400000`, cost 73,
census v7 rank-1 row) の sweep完走 (34 WIN7-D10 [32 sweep WIN + 2
confirmation transfer 106/110] + 39 REFUTED-D10, 0 capped, claim v2 git
blob `814a0ec6`) → 証明書32本 (総rows **1,693,203** / 総抽出nodes
424,657,112 / 出版bytes 61,171,191) → manifest (git blob `6e0a94ab`,
band commits `3a442e0f`..`a53e768a`) → claim v3 (git blob `39cf0f9b`,
commit `a1e1590b`) まで出版済み。引き続き cost73k と同じ第3実装BigInt
verifierによる独立bytes再検証パターン (commits `a02b8ac0`,
`56ce29e0`, `900c95d4`) を73lに適用した。

claim v3は「a third-implementation BigInt independent re-verification of
this band ... is planned as the next step」と明記しており、本再検証が
その予定工程の実施である。並走の publication-geometry audit
(script blob `8a32f40f`, output blob `e544fb1a`, commit `550f1b0e`)
はroot幾何・D4・mobility・transfer被覆をmanifestから再導出したが、
「32本の戦略行をBigInt verifierで探索していない。bytes-level再検証は
依然pending」と自ら記録していた。本バッチがそのpendingを閉じる。

## What was done

1. **ミラー構築** (band pin `a53e768a`): band dir
   `class2-lane-cost73l-certificates/` 159ファイル (manifest + 62 cert
   files [30 split pair + 2 whole (bits 41/61)] + 32 rootcheck.json + 32
   subroots.jsonl + 30 README-split + stats.json +
   det-reextraction.json) をcommit固定raw CDN URLで取得し、
   **159/159 git blob sha照合 PASS** (mismatch 0)。claim v3は
   commit `a1e1590b` pinから取得し blob `39cf0f9b` 照合。
2. **script** `reverify_cost73l_certificates_bigint_20261117.py`:
   - manifest: schema/child/cost 73 assert。basisのclaim v2 blob
     (`814a0ec6`) 記載assert。totals再現 (rows 1,693,203 /
     extraction_nodes 424,657,112 / published_bytes 61,171,191 /
     fbt_drops_total 0 / capped_per_move_total 0)。全32 rootが
     child|(1<<bit) であることを也算術でassert。
   - claim v3 (`39cf0f9b`): mirror blob sha照合、schema v3、
     actual_execution/results/win7_d10_bits == 34 WIN bits (manifest 32
     sweep WIN bits + confirmation bits [106,110] は73j bit 118/73k bit
     98証明書で被覆)、manifest path・manifest_blob_sha一致、**status文中の
     manifest blob (`6e0a94ab`) とmirror manifest実blobの相互照合**、
     certificates totals == manifest totals、determinism_sample_bits ==
     [1,9,47,61,64,116]。
   - **73l固有の強化**: band dir内の stats.json (32 per-bitの
     root/rows/nodes/md5/sha256/moves) をmanifest全レコードと照合し
     rows・extraction_nodes totalsも再現。det-reextraction.json
     (all_byte_identical, bits [1,9,47,61,64,116]) のmd5/rowsをmanifest
     値と照合 (73j/73kバッチには無かった追加cross-check)。
   - pin表: 出版済み `class2-lane-cost73l-pins-20261117.txt`
     (git blob `f36f9a57`) を自体blob pinで読み、159 pin全件を
     mirror bytesと照合 (159/159) + claim v3で**160/160**。
   - whole file (bits 41/61): 「N bytes within the 1200000-byte
     whole-file threshold; published whole」注記のNを実ファイルサイズと照合。
   - split証明書30本: part1行境界 + split_cut_byte一致 + joined
     md5/sha256両方照合 + README-split (whole bytes/分割境界/md5/root)
     照合。
   - **BigInt verifier** (verify_win7_certificate_bigint_independent.mjs,
     blob `62b5d941`, argv[3]=期待mobility) 32本: **32/32 PASS**。
     verdict/root_hex/stones 7/root_safe/rows sorted-unique/union 0/0/
     terminal [13,17]/strategy_rows/subroots_passed/root_mobility/
     consumed_winner_rows 全フィールド一致。
   - **sidecar合意**: subroots.jsonl (batched, 最大8 m-key/行) の
     sum(seen)==visited_states_across_subroots・
     sum(terminals)==terminal_count・
     sum(opponentEdges)==loser_reply_edges が32/32で一致。
     m-key総数 **1,904** == subroots_pass == loser_mobility
     (per-bit mobility 59/55/62/63/63/58/67/65/62/56/56/55/56/66/56/52/
     62/58/63/58/55/53/55/59/61/54/59/61/63/59/67/66)。visitor合計は
     visited_states 3,599,832 (winner_states 2,314,648 +
     loser_states 671,818)・loser_reply_edges 3,178,030・
     terminal_count 613,366 (いずれも32本合計)。
   - **独立D4正準化 (第10実装)**: 32件のd4_canon_root全再現、
     raw_is_canon整合、32 canon相互不重複。
   - **cross-batch不交差**: 151 earlier roots (singlefile 43 +
     splitpart bands 18 + sweepbands 24 + 66j/69j 15 + 63cd 2 + 72d 11 +
     73j 16 + **73k 22**、全8ファイルblob pin照合) に対しroot/D4
     canon両方で重複0。
3. **結果**: 32/32 PASS、file pins 160/160 (159 band + claim v3)、
   manifest md5/sha256 mismatch 0、pin blob sha mismatch 0、sidecar
   cross-agreement fail 0、stats/det-reextraction cross-agreement
   fail 0。
4. **決定性**: 2回実行で出力byte-identical (md5 `da7896eb338fe5bc9143bf0909399a0f`、
   74,448 bytes)。単一実行~78秒/2 worker。

## Interpretation guard

bytes再検証済みpopulationは **349 + 32 = 381 records**。frontier数字は
不変で、いかなるmanifest行も閉じない。73l receipt foldは
66i→66j→69j→71e→72d→73i→73j→73k folds完了まで着手禁止 (並走管理)。
WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10 (73lの39 bit) はLOSS証明ではない。11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はいずれも UNKNOWN のまま。
