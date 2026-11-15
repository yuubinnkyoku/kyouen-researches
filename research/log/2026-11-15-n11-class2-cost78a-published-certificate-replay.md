# 2026-11-15：cost-78a公開証明書2件（bit20・bit36）の独立再生監査 — PASS・frontier不変1195・11×11はUNKNOWN

開始時main: `997254d5`（cost-76a receipts fold head `1195/6652/524884/4922/388607` 掲載済み）。並走cost-78aレーンの公開状況（sweep audit・raw batch 1–10・v15 crosscheck・det-rerun・claim、証明書2/5）を確認した上で、確立済みの「公開証明書の独立再生監査」パターン（cost-74d/72bの先行監査と同じ形式）を78aに適用した。

## 対象

cost-78a sweep（child `00000000000000809102000000400000`、edge cost 78、78候補・184,253,822節点・5 WIN7-D10 bits 8/20/29/36/109・73 REFUTED・0 capped）のうち、mainに公開済みの2証明書:

- **bit36** `00000000000000809102001000400000.cert`（単一ファイル 1,833,561 B・blob `ea30ad28…`）
- **bit20** `…00500000.cert.part1of2/part2of2`（1,020,151 + 1,019,023 B・blob `feedb02d…`/`84d59223…`）

bits 8/29/109は並走が公開中（未公開のため監査対象外）。

## 監査結果（すべてPASS）

`audit_cost78a_published_certificate_replay_20261115.py`（scripts/）:

1. **入力6ファイルがmainとbyte-exact**（sweep audit・v15 crosscheck・claim・bit20両part・bit36のgit blob SHA照合）。
2. **bit20 part再連結**: part1は行境界終端、連結2,039,074 B・md5 `348871fd605dedeb34b5a4c4ad6f518c` == claimの `joined_md5_equals_whole_md5`。
3. **BigInt独立検証**（`verify_win7_certificate_bigint_independent.mjs`・3×3余因子展開・engine不使用）: bit20は**64 sub-roots** == loser mobility == sweep `opponent_legal_replies`・56,452行sorted-unique・consumed union 0/0・終局石数[13,17]。bit36は**59 sub-roots**・50,711行・同じく全管理PASS。claim記載のrows・md5・v15 anchor nodes（9,116,968/6,829,497）・v16 sweep nodes（2,523,199/1,435,988）と全件一致。
4. **root == child | 1<<bit** のbit検算、**D4正準形**がsweep auditの `d4_canonical_hex` と一致、**親lift再導出**: 両rootの7石から1石を除いた6親をD4正準化し、child軌道が含まれることを確認（証明書がchildを被覆する構造の検証）。
5. **head 1195 tie-in**: head-1195のtop-candidates CSVから第3class-2 target S5 `00000000000000809102000000000000` の残り行が{69, 74, 78}=221で、**child（cost 78）は依然remaining**であることを確認。よって本監査はfrontier計数を一切変更しない（`s6_frontier_contribution: 0`）。

計107,163戦略行・訪問230,062状態（重複込み）・終局37,779。

## 解釈上の注意

WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明し、78合法手の6石親は閉じない。REFUTED-D10はLOSS証明ではない。**cost-78a receipt foldは並走担当・新head 1195へのrebase必須**（1188基準のままfoldしないこと）。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 成果物

- 再現スクリプト: [audit_cost78a_published_certificate_replay_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost78a_published_certificate_replay_20261115.py)
- 監査JSON: [cost78a-published-certificate-replay-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost78a-published-certificate-replay-20261115.json)
