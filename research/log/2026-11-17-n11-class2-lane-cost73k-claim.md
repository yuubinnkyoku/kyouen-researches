# 2026-11-17 n11 class2-lane: cost73k claim v1 (census v6 runner-up)

## Context

長期レーン(n11 class2-lane)セッション。前回までに cost71e / cost72d /
cost63cd再生成 / cost72d bytes再検証 / cost72d証明書11本のBigInt独立
再検証 (commit a02b8ac0) を出版済み。並走レーンは census v6
(commit 5ea4def9) → cost73j claim v1 (460fbfc0) → cost73j sweep完走
(8484b092: 16 WIN7-D10 + 57 REFUTED-D10, 0 capped, 168,445,380 nodes)
まで出版済みで、73j証明書は抽出中 (main未出版)。cost73i証明書も
引き続きmain未出版。cost64h receipt fold着地済み (head 1452→1472) で、
76c→66i→66j→69j→71e→72d→73i→73j のfold chainは並走管理のまま
着手禁止。

## What was done

1. **census v6 script の独立再現**: published census v6 script
   (blob 91c89fa4) を92入力ファイル (79 harvest sources + 20 raw
   batch pins + 13 direct load_out pins、全blob sha照合) と共に
   ローカルでverbatim実行し、全published assert がPASS、
   出力がpublished v6 JSON とbyte-identical (md5 6d33e2f6...) である
   ことを確認。
2. **cost73k claim v1**: census v6 runner-up
   `00000000000000801206000000000400` (cost 73, demand c2=2,
   stones [10,49,50,57,60,71]) の fresh 73-bit depth-10 sweep を
   claim。**67 open + 6 confirmation bits**:
   - REFUTED-D10転送予測: bit 23 = pre-64h harvest,
     bit 34 = cost72d, bit 53 = cost66i, bit 107 = cost71e
   - **WIN7-D10転送予測 (2件)**: bit 26 = cost73i,
     bit 55 = cost69j — 本familyで初めてWIN転送を含むconfirmation
     batch。root_canonは全6件独立再計算で確認
     (bit 26 canon `00000000000000801206000004000400` = 73i bit 110
     のWIN、bit 55 canon `00000000000000801286000000000400` = 69j
     bit 110 のWIN)
   - legal 73 == edge cost (legal_candidates.py 独立列挙一致)
   - cost73kは本childの最初のclaim (既存cost73/73a-h/73i/73jは別child、
     raw-CDN probeでcost73kファイル群は全て404)

## Findings

- census v6 ranking は cost 73/73/73/74/75/78/79/79/79/80。
  選択行73jは並走がclaim済みのため、runner-upの73kが本レーンの
  最安未掃引未主張行。
- 73kの6 confirmation bitsのうち2 bits (26, 55) はWIN7-D10転送で
  ある。この2 rootの証明書は転送元lane (73i/69j) のfold待ちで
  あるため、本レーンのsweep後の証明書抽出対象は「open bits由来の
  WIN bits + confirmation再実行でWINとなった2転送bit」となり、
  重複証明書を避けるためmanifestでは転送元とcanon照合を行う。

## Interpretation guard

WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10はLOSS証明ではない。solved 1472はmanifest被覆の簿記で
ある。claim v1はいかなる行も閉じない。receipt foldは
76c→66i→66j→69j→71e→72d→73i→73j の順で並走管理下に保留中。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
いずれも UNKNOWN のまま。
