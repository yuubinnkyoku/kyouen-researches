# seven-row-q4-band-42-56-20261115 — (7,4) witness 帯を m=56 まで延長

Date: 2026-11-15  
Lane: 高速レーン（seven-row-q4-band-41-20261115 の続き）  
Status: COMPLETED

## 結果

**7×42..7×56 の全15幅で、20石の行欠損極大安全配置を確認した。**

q=4、7行盤の満容量は 7(4-1)=21 石。各 witness は20石で、行数は常に一行が2石、残り六行が3石である。したがって各幅で行欠損がある。

| 幅 | witness の基礎幅 | 作り方 |
|---:|---:|---|
| 42 | 42 | seeded SA |
| 43 | 42 | 空列追加 |
| 44 | 44 | seeded SA |
| 45 | 45 | seeded SA |
| 46 | 45 | 空列追加 |
| 47 | 47 | seeded SA |
| 48–49 | 47 | 空列追加 |
| 50 | 50 | seeded SA |
| 51–52 | 50 | 空列追加 |
| 53 | 53 | seeded SA |
| 54–56 | 53 | 空列追加 |

6つの基礎 witness（m=42,44,45,47,50,53）は、既存の7×41 witnessを種にした決定的な乱数列付き貪欲極大化・焼きなまし探索で得た。空列追加の各段階は、新列の全7セルが既存の3石直線または3石円に載ることを整数演算で確認した。

よって、既存の上界 \(M_{7,4}\le1929\)（K0068/K0318）と合わせて、

\[
\boxed{57\le M_{7,4}\le1929}
\]

となる。これは有限幅の witness 存在による下界更新であり、M の確定ではない。

## 独立検証

verify_witnesses.py は探索器を使わず、Python の任意精度整数演算だけで各幅を再検査する。

- 安全性: どの直線・円にも4石以上載らない（最大直線点数3、最大円点数3）。
- 極大性: 盤上の全空きセルが、3石を含む直線または円に載る。
- 行欠損: 20石、行数の最大3・最小2。

**m=42..56 の15/15幅で safe + maximal + row-deficient が PASS**。各幅の曲線数・空きセル数・行数は output/verification.json に保存した。output/witnesses.json は6つの基礎配置、output/records.jsonl は15幅の対応関係を持つ。

## m=57 の探索

m=57 は別seed・別初期配置で30秒と20秒の2回を試したが、どちらも最良21石にとどまった。これは焼きなまし探索の未発見記録にすぎず、欠損極大配置の不存在を意味しない。前線は7×57。

## 再現

実験ディレクトリから:

- node scripts/search_seeded.js 7 42 4 20261115 10000 ../seven-row-q4-band-41-20261115/witnesses/s7x41q4.witness.json
- python3 scripts/verify_witnesses.py

m=44,45,47,50,53 は output/witnesses.json を初期配置ファイルに指定し、末尾に基礎幅キーを渡す。各seed・反復数・実行時間は output/search_runs.json。

## ファイル

- output/witnesses.json — 6つの基礎 witness
- output/records.jsonl — m=42..56 の15レコード
- output/verification.json — 独立検査結果
- output/search_runs.json — seed、探索量、m=57の未発見記録
- scripts/search_seeded.js — seeded SA・貪欲極大化
- scripts/verify_witnesses.py — census不使用・整数演算の独立検証器
