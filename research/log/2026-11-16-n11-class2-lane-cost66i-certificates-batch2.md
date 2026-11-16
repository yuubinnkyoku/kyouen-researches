# 2026-11-16：cost66i WIN7証明書 4件追加出版（bits 103/99/88/28）+ 座標規約の重要発見（canon防御を生rootに適用するとbogus証明書になる）

前回のbit19証明書（`research/log/2026-11-16-n11-class2-lane-cost66i-bit19-certificate.md`）に続き、marginals順 [103, 99, 88, 28] の4 WIN rootのblind証明書抽出・独立検証・出版を行った。**9 WIN中5件の証明書が出版済み**（残り [29, 90, 58, 112]）。

## 座標規約の発見（本ログの最重要プロセス成果）

- 抽出driverのroot行は**生の child|bit**（D4非正規形を含む）。防御列挙も**生root**に対して行う必要がある。bits 19/28/29/58 は raw==canon だが、**bits 88/90/99/103/112 は raw≠canon**。
- 最初のbit103実行でcanonical rootの防御リストを生rootに適用したところ `fatal:21`（bogus防御で抽出器が閉じられない）。kill探索（44応手全失敗）とdepth-8 probe（canon防御21の後に10個の勝利応手 [24,32,41,47,78,86,92,96,101,113] を確認）を行った後、**防御リストの座標ズレが原因と判明**。生root防御53件で再実行したら完全成功。bit99も同様にcanon防御でのbogus証明書（48,289行）がverifierのroot-header検査で棄却され、生root再実行で完全成功。
- 教訓: **証明書の座標系（raw child|bit）とmanifest/claimの座標系（D4 canon）を混ぜない**。両hexをrecord JSONに明記する運用にした。

## 実行・検証（各root、全コントロール合格）

| bit | 生root (=証明書root) | D4 canon | rows | 抽出nodes | sub-roots | union |
|-----|----------------------|----------|------|-----------|-----------|-------|
| 103 | 00000080000000801226000000000000 | …c89002000000020000 | 31,276 | 3,834,589 | 53/53 PASS | 0/0 |
| 99 | 00000008000000801226000000000000 | …c89002000000200000 | 41,402 | 5,788,340 | 55/55 PASS | 0/0 |
| 88 | 00000000010000801226000000000000 | …c89002000100000000 | 61,820 | 9,480,796 | 62/62 PASS | 0/0 |
| 28 | 00000000000000801226000010000000 | （raw==canon） | 47,847 | 18,054,620 | 54/54 PASS | 0/0 |

- 全件 fbt_drops 0、capped 0、terminal範囲は全sub-rootで[13,17]内。
- 独立検証: `verify_bit7_win7_cert.ts`（engine-free・Bareiss 4x4）。root-check stones=7・loserMobility 53/55/62/54 は `legal_candidates.py` の独立列挙と一致。consumed union = 証明書row集合（missing 0 / extra 0 両方向）。
- 決定再実行: 全4件で新規プロセス盲再抽出が**byte-identical**（同一md5・同一node合計）。

## 出版物（commits `2f99d8ba`〜）

- 証明書: `output/class2-lane-cost66i-certificates/` に bit103は単一ファイル(1,128,141 B)、bit99/88/28はpart1of2+part2of2分割（各READMEに結合法・md5/sha256記載）。
- record JSON v2: `output/class2-lane-cost66i-win7-certificates-20261116.json`（5 entry、d4_canon_root欄追加、座標規約をmethodに記載）。
- claim v4: `output/class2-lane-cost66i-inflight-20261116.json`（previous_version = v3 blob `232262879ee820048915ba1bc9d4a328323f982c`、coordinate_convention欄追加）。
- scripts: `kill_search66i.ts`（fatal調査用のkill探索driver、探索専用で最終抽出には非適用の旨をコメント記載）。

## 未完了（次回以降）

- 残り4 WIN root [29, 90, 58, 112] の証明書抽出（bit29/58はraw==canon、bit90/112はraw≠canonにつき防御は生rootで列挙）。
- receipt foldは64h/76c fold着地まで保留（着手禁止維持）。

## 解釈上の注意

各証明書は該当7石rootのdepth-10内先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。**11x11空盤はUNKNOWNのまま**。二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4もすべてUNKNOWN。
