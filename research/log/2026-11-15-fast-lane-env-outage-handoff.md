# 2026-11-15 高速レーン — 実行環境全面停止の記録と次回への引き継ぎ

## 状況

13:41Z 頃、bash・file_system を含む実行環境が全面停止した
("The execution environment is temporarily unavailable"。run_typescript 内の
GitHub connector のみ生存)。retry でも復旧せず、GitHub API 経由で本記録を
push して次回実行に回した (push 前に最新 main を再取得・反映した)。

## 消失したバックグラウンド実行 (いずれも決定的・再実行で同一軌道)

1. (4,5,21) class-split: **c0k3p1 deep cap-2400s** (deepcap.sh v2・minpos=1・
   CNF md5 059fc19d…) — ~40分走行後、結果未記録で消失。
2. n10: **ge20_cuts kissat** (CPU ~1730s 消費時点) — 結果未記録で消失。

再開手順の詳細は各 experiment README の 13:41Z 停止追記に置いた:
- four-row-q5-m21-class-split-20261115 (deepcap 再実行・x2=4 対照較正が必須)
- n10-twenty-stone-sat-20261115 (CNF 再生成 md5 照合 → 再launch)

## 停止までに main へ反映済み (重複回避用)

- K0855 (q∈{2,3} complete degeneracy) を含む先行コミット群
  (n10 dir: 8fafe3a5 / q5 sweep: 2a9795a5・d887e64b)。
- (4,5,21): c0k3p0 deep cap-2400s INDET 13,113,901 conflicts (records 77行目)・
  deepcap.sh v1 の \`\${key:6}\` minpos bug の発見と v2 修正・
  sat4.js (x2 第2石 pin)・sweepp0x2.sh の作成と検証 (句スーパーセット検査 PASS・
  対照 CNF md5 362034b2… 一致)。x2=4 対照の kissat SAT 実証のみ未実施。
- n10: 制御 C1-C4・K1-K4 全PASS・3 CNF の md5 記録方式
  (ge19 73289501… / ge20 d9d060d3… / ge20_cuts 58408731…)。
- K0856 は 2026-11-15 時点で未使用 (search_code 確認)。次の新規 K は要再確認。

## 次回の最優先

1. 復旧確認 (date -u / krwork 存在。消えていれば各 README の resume 手順で
   main から復元。kissat 4.0.4 は公式 rel-4.0.4 zip asset・md5 3a5eba83…)。
2. x2=4 対照の kissat SAT 実証 (sweepp0x2.sh の前の必須較正)。
3. c0k3p1 deep 再launch (deepcap.sh v2) と ge20_cuts 再launch の併走
   (2コア埋まっている間は重い追加実行を避ける)。
4. 決着記録 → CSV (results/fixed-width/mwq_stabilization.csv) 行更新・
   K 項目 (K_10=19 はカット版 UNSAT で K0035/K0141 を決着)・knowledge 昇格。
