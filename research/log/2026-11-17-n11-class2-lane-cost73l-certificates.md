# cost73l 証明書 32 枚の抽出・検証・出版完了（2026-11-17）

## 背景

cost73l（child `00000000000000c09002000000400000`・cost 73・parent
`00000000000000403800000008000000`・demand c2=2）の fresh v17 depth-10 sweep は
claim v2（commit `8f74c6cd`）で完走済み（34 WIN7-D10 / 39 REFUTED-D10 / 0 capped）。
本セッションは 32 個の sweep WIN root（転送 106/110 は 73j bit 118 / 73k bit 98
の出版証明書で被覆済み）の blind 証明書抽出・独立検証・main 出版を完遂した。

## 実行

- **抽出**: `class4_child1_cert_extractor_exact_ms23.ts`（repo verbatim
  extractor_exact の MS=1<<18 → 1<<23 単行置換・engine v15 inlined・空 kill
  table・bit ごと fresh process）+ `cert_driver73l.ts`。**32/32 完了**、
  fbt_drops 0、fatal なし、capped per-move なし。総計 **1,693,203 rows /
  424,657,112 extraction nodes / 61,171,191 published bytes**。最重は bit 116
  （22,587,921 nodes / 73,217 rows）、次いで bit 64・bit 47。
- **独立検証**: `verify_cost73l_one.sh` + `verify_bit7_win7_cert.ts`
  （Bareiss 4x4・engine-free）。**32/32 PASS**: rootcheck stones=7・loser mobility
  が RAW root 上の独立 legal_candidates.py 列挙と一致・全 sub-root PASS・
  terminal stone range [13,17]・consumed-winner-state union vs 証明書行集合が
  0 missing / 0 extra（双方向）。
- **決定論性（同一環境）**: 6 bit [1,9,47,61,64,116] を fresh process で再抽出し
  **全 6 bit byte-identical**（md5: bit1 `114b255f`・bit9 `807c0aed`・
  bit47 `8d5d143c`・bit61 `1391b4c4`・bit64 `9bf9a00a`・bit116 `1dec0c4b`）。
  最重 bit 116 を含む。
- **決定論性（クロス環境）**: 抽出・検証実行中に実行環境全体が wipe され
  `/home/user/kr` が全消滅した。repo tarball から必要パスのみを選択展開して
  ワークスペースを復旧し、73l スクリプト群を再構築して抽出・検証をやり直した。
  wipe 前後で **bit 61（nRows=28,229・sum=3,775,056）・bit 1（md5 `114b255f`）・
  bit 9（md5 `807c0aed`）が全て同一**。別 sandbox インスタンス間で抽出が
  byte-identical であることを示す追加証拠となった。
- **stats/manifest**: `build_cost73l_cert_stats_20261117.py`（summary JSON が
  undefined の fatal キーを落とす問題へ `s.get("fatal") is None` で対応）で
  stats.json を構築し、`build_cost73l_cert_manifest_20261117.py` で manifest
  `class2-lane-cost73l-win7-certificates-20261117.json`（blob
  `6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4`・全 assertion PASS）を構築。
  30 bit は 1,200,000 byte 超で split（`.cert.part1of2/.part2of2`・
  README-split 30 本）、bit 41・bit 61 は whole。

## 出版

- **スクリプト 7 本**（extractor/driver/extract-all/verify-one/stats/det/manifest）:
  アーカイブコミット `37c5c311`..`e0b50e8c` で先行出版、blob sha 照合 7/7。
- **証明書 62 ファイル**（30 bit × 2 part + bit41/bit61 whole）: 1 ファイル
  1 コミット、band `3a442e0f`..（bit 1 part1of2）..bundle 3/3 `a53e768a`。
- **bundle 3 コミット**: (1) manifest + stats.json + det-reextraction.json +
  README-split 30 本、(2)(3) bit ごと rootcheck.json + subroots.jsonl 計 64 本 +
  `scripts/verify_cost73l_worker.sh`。
- **最終監査**: 出版後に remote の `output/class2-lane-cost73l-certificates/`
  全 159 ファイルの git blob sha を取得し、ローカル計算値（`blob <size>\0<bytes>`
  の sha1）と全件照合 → **159/159 一致・0 mismatch・0 missing・0 extra**。
  worker スクリプトは scripts ディレクトリ側で別途照合（blob `5768103d`、
  アーカイブ済み 7 本含め 8/8 一致）。**計 160/160 byte-exact**。
- **claim v3**: `update_claim73l_v3_20261117.py`（入力 blob `814a0ec6` を
  検証して v2 → v3）を同梱し、claim 本体を in-place 更新して出版
  （commit `a1e1590b`）。

## 出版 tooling の挙動（正直な記録）

- 並走レーンとの non-fast-forward が 2 回発生、いずれも 6 秒待ち retry で解決。
- run_typescript sandbox の 16 MiB メモリ上限により、最大の bit 116 両 part
  （各 ~1.32 MB）の push 呼び出しは MemoryLimitError を出したが、
  `push_files` 自体は完了しており、着地後に blob sha 照合で byte-exact を
  確認済み。chunked read 組立の length 検証は全ファイルで実施。
- push transport がバイナリを破壊した実績（K0900 の .gz）に対しては、
  本 band は全て ASCII text であり、blob sha 全件照合で破壊なしを確認。

## 制限

- WIN7-D10 証明書は個別 7 石 root の depth 10 以内の先手勝ちのみを証明する。
- REFUTED-D10 は LOSS 証明ではない。solved 数は manifest 被覆の簿記である。
- 本 band は manifest 行を 1 つも閉じない。receipt fold は 66i/66j/69j/71e/72d/
  73i/73j/73k fold の後ろで pending（並走管轄の fold には手を出していない）。
- **11x11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はいずれも
  UNKNOWN のまま**。

## 次の一手

BigInt 第三実装による 32 証明書の独立再検証（`reverify_cost73j_certificates_
bigint_20261117.py` を 73l manifest 形式へ適応: band 内 manifest・per-bit
rootcheck/subroots・既存 BigInt 検証済み root との cross-batch disjointness）。
その後も本行の receipt fold は上記 fold chain の後ろで保留。
