# 2026-11-14 n11 class2-lane cost61d bit30 WIN7証明書 TS独立検証 (PASS, det4共線込み幾何)

## 概要

cost61dレーン bit30 root `00000000000000803202000040000002` (7石 {1,30,49,57,60,61,71}, loser=P2手番) のWIN7証明書 (深さ10以内) をTSサンドボックス独立検証器で検証した。**verdict: PASS**。

## 検証基盤

- 入力: tscompact 2 part (`bit30-root-00000000000000803202000040000002.cert.tscompact.part1of2.b64` / `part2of2.b64`)。meta・fnv1a照合: part1=3e1b8c63, part2=0de3dd87。計23,348行。
- 幾何: **det4 (Bareiss 4x4行列式)==0で共円/共線判定し、3点共線のとき直線上の点も禁止マスクに含める**(repo正本 `scripts/verify_bit7_win7_cert.ts` の forbiddenByTriple と同一仕様)。

## 旧検証失敗の根本原因と訂正

旧TS検証器は3点共線のとき禁止マスクを返していなかった (A=B=C=0 で 0n)。このため:

- root合法手を73と誤計算していた (正しくは44 = repo cost61d log の mobility 44 と一致 = 表8石行44個)
- 深い局面でloserがrepoでは違法な共線手を指して表外に脱出し、even_not_in_table 144,371件の失敗を生んでいた
- 「bit30はrootの73応手のうち33手未カバーの部分証明」という判断も誤りであった。正しくは **rootの全44応手をカバーする完全WIN7証明**

誤検証に基づく旧C1 bitmap (commit 4bc0baab, consumed=1926, fnv1a=211bf294) は廃止し、正検証のbitmapで上書きした (commit a7e8865f)。

## 検証結果 (det4幾何)

- root: 7石、4点共円/共線なし、root合法手44 (det4)
- **44/44サブroot PASS** (C1: 0-21, C2: 22-43)。サブrootは表8石行44個 = rootの全合法手の子。
- nodes=92,969 (C1=48,904, C2=44,065)、terminals=8,468 (C1=4,310, C2=4,158)、max_depth=9
- consumed bitmap: C1 consumed=12,836 (fnv1a=77ee4a0f), C2 consumed=14,724 (fnv1a=ca679c06)
- **union=23,348/23,348行 = 全行フルカバー (missing=0, extra=0)**

## 今後の課題

- bit119 (cost63a)・bit81 (cost73a) は旧(緩い)幾何で検証PASS済み。緩いルールはloserの合法手が多くwinnerにとって条件が厳しいため勝ちの主張は保守的に有効だが、正幾何での全行coverageは未確認。det4版で再検証し、coverage (全行消費 or unreachable rows の記録) を確認する。
- bit94 (root `00000000400000803202000000000002`, 23,982行, mobility=45) → bit74 (root `00000000000004803202000000000002`, 26,090行, mobility=49) をtscompact化→det4版TS検証の順で進める。

## 11x11 status

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。** 本検証は個別7石rootのWIN7証明書の整合性のみを証明する。途中結果から勝敗を断定しない。
