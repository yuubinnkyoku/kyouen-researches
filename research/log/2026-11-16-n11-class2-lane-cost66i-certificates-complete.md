# 2026-11-16：cost66i WIN7証明書 残り4件出版・**9 WIN全証明書完走**（bits 29/90/58/112）

batch2（`research/log/2026-11-16-n11-class2-lane-cost66i-certificates-batch2.md`）に続き、残り4 WIN root [29, 90, 58, 112] のblind証明書抽出・独立検証・出版を行い、**cost66i sweepの9 WIN7-D10 root全てに独立検証済み証明書が揃った**。

## 実行・検証（全コントロール合格、防御は生rootで列挙）

| bit | 生root (=証明書root) | D4 canon | rows | 抽出nodes | sub-roots | union |
|-----|----------------------|----------|------|-----------|-----------|-------|
| 29 | 00000000000000801226000020000000 | （raw==canon） | 28,713 | 2,236,573 | 51/51 PASS | 0/0 |
| 90 | 00000000040000801226000000000000 | …c89002000040000000 | 26,733 | 3,021,234 | 44/44 PASS | 0/0 |
| 58 | 00000000000000801626000000000000 | （raw==canon） | 37,807 | 9,045,947 | 53/53 PASS | 0/0 |
| 112 | 00010000000000801226000000000000 | …c89002000000000100 | 42,908 | 8,073,039 | 54/54 PASS | 0/0 |

- 全件 fbt_drops 0、capped 0、terminal範囲は全sub-rootで[13,17]内。
- 独立検証: `verify_bit7_win7_cert.ts`。root-check stones=7・loserMobility 51/44/53/54 は `legal_candidates.py` と一致、union 0/0両方向。
- 決定再実行: 全4件で新規プロセス盲再抽出がbyte-identical。
- さらに**出版済み証明書をraw CDNから再ダウンロードして再検証**（bit103/99/88/28で実施、bit19はbatch1で実施済み）し、出版バイトそのものが独立検証を通ることを確認。

## 出版物（commits `2d098c74`〜`f27f251e`）

- 証明書: bit29(1,037,699 B)・bit90(964,973 B)は単一ファイル、bit58(1,366,065 B)・bit112(1,548,417 B)は2分割+各README。
- record JSON v3: 9 entry完走、schema `n11-class2-lane-cost66i-win7-certificates-20261116-v3`。
- claim v5: schema `...-v5`、certificate phase complete、previous_version = v4 blob `e4f3e1b6f091cd653e9494c6f93d39966a74d8b5`。

## まとめ（cost66i lane全体）

- sweep: 66 bits fresh、WIN7-D10 9 / REFUTED-D10 57 / capped 0（決定再実行・v15交差・独立監査合格済み）。
- 証明書: **9/9 完走**。総rows 359,441、総抽出nodes 70,735,308、全件 union 0/0・fbt_drops 0・決定再実行byte-identical。
- この結果、当該childの全WIN rootが独立検証可能な証明書で担保された。ただし**これは9個の7石rootのdepth-10内先手勝ちの証明にすぎない**。

## 未完了（次回以降）

- receipt fold（64h/76c fold着地まで着手禁止）。
- 次ターゲット選定（head-1452 census v2のrunner-up `00000000000000801282000040000000` cost 64・55 open、または64h/76c fold着地後の再census）。

## 解釈上の注意

**11x11空盤はUNKNOWNのまま**。REFUTED-D10はLOSS証明ではない。二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
