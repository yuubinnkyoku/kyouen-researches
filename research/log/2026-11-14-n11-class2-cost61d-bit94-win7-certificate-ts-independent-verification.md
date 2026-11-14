# 2026-11-14 n11 class2-lane cost61d bit94 WIN7証明書 TS独立検証 (PASS, det4共線込み幾何)

## 概要

cost61dレーン bit94 root `00000000400000803202000000000002` (7石 {1,49,57,60,61,71,94}, loser=P2手番) のWIN7証明書 (深さ10以内) をTSサンドボックス独立検証器で検証した。**verdict: PASS**。

## 検証基盤

- 入力: tscompact 2 part (`bit94-root-00000000400000803202000000000002.cert.tscompact.part1of2.b64` / `part2of2.b64`, commit f2ddfc88)。meta・fnv1a照合: part1=6ff793b6, part2=a8e3121a。計23,982行。
- 幾何: **det4 (Bareiss 4x4行列式)==0で共円/共線判定し、3点共線のとき直線上の点も禁止マスクに含める**(repo正本 `scripts/verify_bit7_win7_cert.ts` の forbiddenByTriple と同一仕様)。bit30で発見した旧検証器の共線抜けバグは本検証には含まれない。

## 検証結果 (det4幾何)

- root: 7石、4点共円/共線なし、root合法手45 (det4) = repo cost61d log の mobility 45 と一致
- **45/45サブroot PASS** (C1: 0-22の23個, commit 578920d0。C2: 23-44の22個, commit dcd1389d)。サブrootはroot合法手45の全子。
- nodes=57,393 (C1=30,196, C2=27,197)、terminals=7,842 (C1=4,189, C2=3,653)、max_depth=9、終端石数範囲 [13,17]
- consumed bitmap: C1 consumed=14,055 (fnv1a=25136eb4), C2 consumed=14,814 (fnv1a=d05b0942)
- **union=23,982/23,982行 = 全行フルカバー (missing=0, extra=0)**。union fnv1a=9f1e7dbf。重複=4,887行、C1のみ=9,168行、C2のみ=9,927行。

## 意義

- cost61dレーンのbit94について、bit30と同一の独立検証基盤(det4)で証明書の整合性と全行coverageが確定した。
- これにより cost61d の確定済みrootは bit30・bit94 の2つとなる。

## 今後の課題

- bit74 (root `00000000000004803202000000000002`, 26,090行, mobility=49) をtscompact化→det4版TS検証の順で進める。
- bit119 (cost63a)・bit81 (cost73a) は旧(緩い)幾何で検証PASS済み。det4版で再検証し、coverage (全行消費 or unreachable rows の記録) を確認する。

## 11x11 status

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。** 本検証は個別7石rootのWIN7証明書の整合性のみを証明する。途中結果から勝敗を断定しない。
