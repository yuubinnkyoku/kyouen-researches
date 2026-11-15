# 2026-11-15：published fold-chain監査v5・agreement v2のfresh mirror再現性検証 — main単独から3 script全統制PASS・3出力ともpublished JSONとbyte-identical

背景: canonical head **1306/6541/516711/4811/380434**（cost-82c receipts fold）。同日にpublished fold-chain全root監査の第一実装v5・第二実装v5・dual implementation agreement v2が着地済み（[第一実装v5 log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v5-first-implementation.md)・[第二実装v5 log](./2026-11-15-n11-class2-lane-published-chain-roots-audit-v5-second-independent.md)・[agreement v2 log](./2026-11-15-n11-published-fold-chain-dual-implementation-agreement-v2-82c-pair.md)）。本記録は**現main単独からの第三者再現性**（repoに存在するファイル以外を一切使わない再実行）を検証する。

## 手法

codeload tarball（`https://codeload.github.com/yuubinnkyoku/kyouen-researches/tar.gz/refs/heads/main`・3,282,135,196 bytes・md5 `b3cb07ff…`・取得時点のmain HEAD = agreement v2コミット `e26aa75e`）を隔離ディレクトリに全体展開し、published 3 scriptを依存関係追加なしにそのまま実行:

1. `audit_published_chain_roots_second_independent_v5_20261115.py`（第二実装・82c endpoint）
2. `audit_published_chain_roots_independent_20261115.py`（第一実装・v5 in-place版・82c endpoint）
3. `audit_dual_implementation_agreement_20261115.py`（機械照合・v2 in-place版・3 endpoint pair）

## 結果 — 全統制PASS・3出力ともpublished JSONとbyte-identical

| script | 判定 | 出力 | publishedとの照合 |
|---|---|---|---|
| 第二実装v5 | AUDIT PASSED（96 pins 26+52+18・592 roots/581 orbits/11 twins・receipt 469/group 40/anomalies 0・arith 74 heads anomalies 0・child-closure 29・canonical 1233..1306 mim 73/distinct 73/multi 0） | `class2-lane-published-chain-roots-second-independent-audit-v5-20261115.json` | **cmp byte-identical**（md5 `63cbcf95…`） |
| 第一実装v5 | AUDIT PASSED（100 pins 26+52+22・bit-78 exactly-once統制込み・他は第二実装と同一数値） | `class2-lane-published-chain-roots-independent-audit-v5-20261115.json` | **cmp byte-identical**（md5 `8c3cdf03…`） |
| agreement v2 | AGREEMENT CONFIRMED（75d 569/1296 mim 63・80d 587/1305 mim 72・82c 592/1306 mim 73・全pairでbit-78 root同一） | `class2-lane-published-fold-chain-dual-implementation-agreement-v2-20261115.json` | **cmp byte-identical**（md5 `fcb4304a…`） |

両実装は互いのscriptを一切参照せず（published-files-only・純stdlib）、agreement scriptは6つのpublished audit JSONのgit blob pin（v3 `9ae57954`・v2 `db0916c0`・v4first `c3df2d1e`・v4second `e3a0b7da`・v5first `d648ed70`・v5second `af86251a`）を最初にassertするため、fresh mirrorでのbyte-identityは**corpus全体の着地整合と3出力の再現性を同時に保証**する。

## 解釈境界（重要）

- 監査の一致・再現は**簿記・証明書整合の一致**であり、いずの局面のgame-theoretic値も意味しない。solved 1306はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 並走laneのcost-83a sweep IN FLIGHT着地後は、head 1306 baselineでfold→第二独立検証→両実装v6拡張→agreement v3拡張→本再現性検証（fresh mirror 3 script再実行）を同一パターンで適用できる。
