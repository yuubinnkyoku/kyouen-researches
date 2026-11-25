# 2026-11-16：cost66i bit19証明書 抽出・独立検証・出版（WIN7-D10 9 bitsの第1号、marginals順）

前回のraw sweep（`research/log/2026-11-16-n11-class2-lane-cost66i-raw-sweep.md`）とmarginals監査（commit `e6a851bf`）に続き、抽出優先順位1位の **bit 19 root `00000000000000801226000000080000`** のblind証明書抽出を行い、独立検証・決定再実行コントロールを全て確認して出版した。

## 抽出

- extractor: repo-verbatim `class4_child1_cert_extractor_exact.ts`（FBS=1<<20、probe96）、kill table空。driver `cert_driver66i.ts`（`scripts/`に配置、importは同ディレクトリのextractorを指す）。
- root合法手52件は独立の `legal_candidates.py` 列挙（52 legal）をdriverのstdinに供給。
- 結果: **rows 40,935**（dedup+sort済み）、抽出nodes **11,200,170**、fbt_drops 0、52/52のloser防御全てok、capped 0、約21秒。terminal範囲は全sub-rootで[13,17]内（per-move範囲は[13,15]/[15,15]/[15,17]を含む）。

## 独立検証（全て本セッションで再実行）

1. **verify_bit7_win7_cert.ts**（engine-free、Bareiss 4x4 cofactor）: root-check stones=7・loserMobility=52（legal_candidates.pyの独立列挙と一致）、52/52 sub-roots PASS（rc=0）。
2. **union両方向比較**: verifierが消費したwinner stateのunion（40,935）と証明書row集合（40,935）が完全一致、**missing 0 / extra 0**。
3. **決定再実行**: 新規プロセスで盲再抽出したところ**byte-identical**（md5 `084bc1f4d0244ca1fc1ee769977060fd`、sum/nRows/fbt_drops全て同一）。検証統計（per-move seen/terminals/opponentEdges/range）も前回実行と完全一致。

## 出版物

- 証明書: `output/class2-lane-cost66i-certificates/n11_s7_00000000000000801226000000080000.cert`（1,478,743 bytes。単一run輸送限界超過のため `part1of2` 739,395 + `part2of2` 739,348に分割、`README-split-bit19.md`に結合法とmd5/sha256記載。sha256 `f87df551ab38f73fb34d756fc4be287de42f1538735e7daf6006deb05749b0ac`）。
- record JSON: `output/class2-lane-cost66i-win7-certificates-20261116.json`（cost67 recordと同構造）。
- driver: `scripts/cert_driver66i.ts`。
- claim v3: `output/class2-lane-cost66i-inflight-20261116.json`（schema v3、v2 blob `738443c0d1076115d723029edac2de3cb67c3e86`をprevious_versionに明記、certificate_extraction欄を更新）。

## marginals順の残り

抽出順位は[19, **103, 99, 88, 28, 29, 90, 58, 112**]（marginals監査より）。bit19で4 manifest行（64h/76c pending fold重複除き3行）の証拠が揃った。残り8 rootは各個に抽出・検証する。

## 未完了（次回以降）

- 残り8 WIN rootの証明書抽出（marginals順）。bit103はroot `00000000000000c89002000000020000`。
- receipt foldは64h/76c fold着地まで保留（着手禁止維持）。

## 解釈上の注意

本証明書はbit 19 root（7石）のdepth-10内先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。**11x11空盤はUNKNOWNのまま**。二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
