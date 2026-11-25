# 2026-11-14 n11 class2-lane cost61d bit74 WIN7証明書 TS独立検証 (PASS, det4共線込み幾何)

## 概要

cost61dレーン bit74 root `00000000000004803202000000000002` (7石 {1,49,57,60,61,71,74}, loser=P2手番) のWIN7証明書 (深さ10以内) をTSサンドボックス独立検証器で検証した。**verdict: PASS**。

## 検証基盤

- 入力: tscompact 2 part (`bit74-root-00000000000004803202000000000002.cert.tscompact.part1of2.b64` / `part2of2.b64`, commit 8a0f072e)。meta・fnv1a照合: part1=59ef9f19, part2=6f6a68b7。計26,090行。
- 幾何: **det4 (Bareiss 4x4行列式)==0で共円/共線判定し、3点共線のとき直線上の点も禁止マスクに含める**(repo正本 `scripts/verify_bit7_win7_cert.ts` の forbiddenByTriple と同一仕様)。旧検証器(onCircle)のFn項符号バグは本検証には含まれない。

## 検証結果 (det4幾何)

- root: 7石 {1,49,57,60,61,71,74}、4点共円/共線なし、root合法手49 (det4) = repo cost61d log の mobility 49 と一致
- **49/49サブroot PASS** (C1: 0-24の25個, commit b470f0c0。C2: 25-48の24個, commit 513e4d50)。サブrootはroot合法手49の全子。
- nodes=58,734 (C1=29,363, C2=29,371)、terminals=8,321 (C1=4,105, C2=4,216)、max_depth=9、終端石数範囲 [13,17]
- consumed bitmap: C1 consumed=14,553 (fnv1a=3255f5e1), C2 consumed=15,172 (fnv1a=c6e3ac7a)
- **union=26,090/26,090行 = 全行フルカバー (missing=0, extra=0)**。union fnv1a=3c5b8403。重複=3,635行、C1のみ=10,918行、C2のみ=11,537行。

## 意義

- cost61dレーンのbit74について、bit30・bit94と同一の独立検証基盤(det4)で証明書の整合性と全行coverageが確定した。
- これにより cost61d の確定済みrootは bit30・bit74・bit94 の3つとなる。

## 今後の課題

- bit119 (cost63a)・bit81 (cost73a) は旧(緩い)幾何で検証PASS済み。det4版で再検証し、coverage (全行消費 or unreachable rows の記録) を確認する。
- 残り cost61d WIN7 bits (2,8,22,23,53,75,84,102,114,116,119) はwarm certificate-rebuild候補。

## 11x11 status

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。** 本検証は個別7石rootのWIN7証明書の整合性のみを証明する。途中結果から勝敗を断定しない。
