# 2026-11-17 n11 class2-lane: head-1472 presweep census v6 (nine-map overlay) and cost73j claim v1

## Context

長期レーン(n11 class2-lane)セッション。前回までに cost71e (13 WIN) /
cost72d (11 WIN) / cost63cd再生成 / cost72d bytes再検証 を出版済み。
並走レーンは cost73i sweep (12 WIN7-D10 [1,9,11,18,29,38,54,82,97,100,
110,111] + 61 REFUTED-D10, 0 capped, 131,402,821 nodes, commit
05934fc9) を完走したが、73i証明書はまだmain未出版。cost64h receipt
foldは着地済み (head 1452→1472, agreement check 19/19 PASS,
commit 2e1fdd5e) で、76c→66i→66j→69j→71e→72d→73i のfold chainは
並走管理のまま着手禁止。

## What was done

1. **head-1472 presweep census v6** (script
   `next_target_presweep_head1472_v6_20261117.py` + JSON
   `class2-lane-next-target-presweep-1472-v6-20261117.json`):
   published v5 (blob ea85c023) を verbatim に拡張し、完成済みの
   cost71e / cost72d / cost73i の3 verdict map を追加して nine-map
   overlay に更新。全published assert を維持:
   - v1 harvest rebuild: 79 sources / 3,548 canons / 353 WIN /
     3,195 REFUTED / 0 conflicts (v1 census 記録値と完全一致)
   - 71e/72d: audit win bits == claim win bits == manifest (13/13,
     11/11); 73i: audit win bits (12) ⊂ claim v1 open bits (68),
     confirmation bits 5/5 一致 (claim v1 はin-flightのまま、
     証明書未出版であることをfold欄に明記)
   - nine maps: 600 distinct canons, internal conflicts 0,
     harvest cross-agreements 26
   - v1 bit-table children 16件 transition + root_canon check 全PASS
   - family rows 39件をbit-exactに再計算、9つのswept children
     (64h/76c/66i/66j/69j/64a/71e/72d/73i) は全て open 0
   - v5 rankingの非掃引7行は全てv6 top-10に残存 (7/7)
   - 出力は2回実行で byte-identical (md5 6d33e2f6...)
2. **cost73j claim v1**: census v6 選択行 (cheapest remaining)
   `00000000000000403800000408000000` (cost 73, demand c2=2,
   stones [27,34,59,60,61,70]) の fresh 73-bit depth-10 sweep を
   claim。**66 open + 7 confirmation bits**:
   - bit 5 = cost69j bit 34, bit 14 = cost72d bit 34,
     bit 20 = cost64h bit 34, bit 46 = cost73i bit 34,
     bit 97 = cost71e bit 106, bit 103 = cost66i bit 14,
     bit 108 = cost66j bit 106 (全てcanon同一性を独立再計算で
     確認、全てREFUTED-D10転送)
   - legal 73 == edge cost (legal_candidates.py 独立列挙一致)
   - cost73jは本childの最初のclaim (既存cost73/73a-h/73iは別child)

## Findings

- census v6 runner-up: `00000000000000801206000000000400`
  (cost 73, open 67)。v6 top-10のcost帯は73/73/73/74/75/78/79/79/79/80。
- 新3 map による転送で選択行のopenは v5 の69から66へ減少
  (bit 14 = 72d, bit 46 = 73i, bit 97 = 71e が新規転送)。
- RAW_PINS と76c child hexの手転写ミス2件を機械移植・拡散前検出で
  修正 (76d batch7 pin 1文字, 76c hex 9092→9002: 既知の事故パターン)。
  32桁hex/pinの手書き転写禁止の教訓を再確認。

## Interpretation guard

WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明する。
REFUTED-D10はLOSS証明ではない。solved 1472はmanifest被覆の簿記で
ある。census v6とclaim v1はいかなる行も閉じない。receipt foldは
76c→66i→66j→69j→71e→72d→73i の順で並走管理下に保留中。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
いずれも UNKNOWN のまま。
