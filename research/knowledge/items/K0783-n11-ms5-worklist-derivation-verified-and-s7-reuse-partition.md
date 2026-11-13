---
id: K0783
title: n11 S2{59,60} milestone-5のS7候補全15,072件と公開表8,763件の欠落監査（K0675条件下）
kind: proposition
status: computed
topics: [verification, certificates, provenance, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0675
  note: 94オラクル位置（78 FW + 16 SW）と14 LOSS sweep鍵が導出の全入力
- type: depends_on
  target: K0672
  note: focus2154の62証明書（27 WIN7 + 35 LOSS7）が再利用分類の入力
artifacts:
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_candidates_part1.csv
  role: data
  note: 候補S7表 s7_hex,s6_hex,move,cat（1=既知LOSS子、2=プール候補）。part1..3で計8,763行
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_stats.json
  role: manifest
  note: 導出anchor・md5一致・再利用分類の全計数
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ms5_s7_reuse_analysis.ts
  role: source
  note: コメントのみで実行本体は未公開。再導出・再分類の再現器としては使用できない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_candidates.py
  role: verifier
  note: 公開行の安全性・親子関係・件数を独立検査。候補の完全性や分類の正当性は検査しない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/published-candidates-audit.json
  role: data
  note: 公開行の限定監査結果とmove座標の注意
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_completeness.py
  role: verifier
  note: 公開オラクル94位置の全対称像からS6ワークリスト上の合法な補完候補を全列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_completeness_independent.py
  role: verifier
  note: 4点部分集合の逆引きと行列式による別実装で全親子対を照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_additional_geometry.py
  role: verifier
  note: 追加候補の安全性を独立な行列式判定で確認
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/candidate-completeness-audit.json
  role: data
  note: 全15072件と公開表に欠ける6309件の集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/additional-candidates.csv.gz
  role: data
  note: 追加6309件。moveは正規化されたs6の座標
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_classification.py
  role: verifier
  note: 既存の条件付きLOSS6と証明書監査記録に照らし全候補を分類
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/candidate-classification-audit.json
  role: data
  note: 条件付き先手LOSSと未確定候補の内訳
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/classified-candidates.csv.gz
  role: data
  note: 全候補の照合結果。possible_first_winは証明済み勝利ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_win7_reuse.py
  role: verifier
  note: 公開WIN7監査記録を全S6ワークリストと照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_reused_witnesses.py
  role: verifier
  note: 抽出された勝ち子の合法性と証明書監査記録を個別照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/win7-reuse-audit.json
  role: data
  note: 534証人対・498親と削減後の件数・コスト
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/win7-reuse-hits.csv.gz
  role: data
  note: 各親の勝ち手・子・証明書監査記録の所在とハッシュ
- path: research/log/2026-11-13-n11-ms5-reproducer-source-audit.md
  role: log
  note: 再導出プログラムの実行本体が欠けることの監査
- path: research/log/2026-11-13-n11-ms5-worklist-derivation-and-s7-reuse-partition.md
  role: log
  note: 経緯と再現上の注意（メモリ上限・実装上の修正点）
scope: n11 S2 {59,60} milestone-5のワークリストとS7証明書再利用。局所S6の条件付き勝敗は含むが、二石rootや空盤の勝敗は含まない。
evidence: 公開manifestの辞書順md5は0e95a438dbcb486368393de9c73fc21e。94オラクルの全744対称像を使い公開7867親から合法な補完候補15072件を独立列挙。公開WIN7監査記録4052鍵と照合し、534親子対・498親に勝ち子を確認。証明書本体は再監査していない。
---

## 主張

1. milestone-5のS6ワークリスト7,867行（鍵・classes・cost全部門）が、K0675オラクル入力からの独立再導出と全行バイト一致したと報告されている（md5 0e95a438dbcb486368393de9c73fc21e、辞書順）。ただし当該再導出の実行本体は公開されておらず、報告自体は現checkoutから再実行できない。
2. 公開ワークリストS6からのoracle補完候補S7（|O\S6|=1かつx合法）は、94オラクルの全対称像を考慮すると **15,072件**。従来公開表8,763件はこの部分集合であり、**6,309件が未掲載**。候補のある親は7,256個、ない親は611個。全列挙は公開ワークリストとオラクルを入力とする有限検査であり、ワークリスト自体の完全性や候補の勝敗分類は検査していない。
3. 既知の14個のLOSS6の合法子とfocus62監査記録から、公開8,763件中396件・追加6,309件中229件が **条件付き先手LOSS7**、残る公開8,367件・追加6,080件がスイープ上の勝ち子と照合可能な候補である。この時点の候補分類そのものは先手WIN7を意味しない。LOSS7/WIN7は元の先手の勝敗であり、七石位置の手番側から見た勝敗と区別する。
4. 公開されている3系統のWIN7証明書監査記録4,052鍵をS6ワークリスト7,867親と照合すると、**534親子対・498親**にWIN7子がある。従って公開監査記録を前提に498親は先手WINと判定できる。残りは **7,369親**で、manifestの合法子コスト合計は615,497から **577,110** となる。証明書本体は別保管で、本照合では再検証していない。

欠落例として、公開親 `0000000000000000380000000000002c` に座標51を加えた局面は合法で、オラクル `00000000000000003800800000000080` の対称像 `00000000000000003808000000000008` を含む。子の正規形 `000000000000000038008000000001a0` は元の公開表にない。

## 帰結

- 公開manifestの鍵集合・classes列・cost列の3系統一致は記録上の結果であり、独立再導出の実行本体の復元が必要。
- WIN7監査記録との照合は公開データのみで498親を解消する。追加分を含む候補のうち既知の条件付きLOSS7は625件。補完候補がない親は611個であり、別の勝ち手の可能性を排除しない。

## 限界

- 全てのwin/loss記述はK0675オラクル（78 FW + 16 SW）の条件付き。オラクルが崩れれば本項も崩れる。
- **11x11空盤・二石root {49,60}・S2 {59,60}はいずれもUNKNOWNのまま。**本項は勝敗を一切確定させない。
- possible-win-poolは「 witness候補」であって証明済みWIN7ではない。hitしたものだけが閉鎖になる。
- CSVの `s7_hex` と `s6_hex` はそれぞれ対称性で正規化された局面だが、`move` は `s6_hex` の座標に直接対応するとは限らない。公開8,763行中7,158行は直接適用しても同じ子に到達せず、うち119行では既に石のある座標を指す。親の8個の対称像を試し、空き座標 `move` を加えた後の正規形が `s7_hex` と一致する像を選ぶこと。全行でそのような像の存在を検査した。
- 候補CSVのヘッダーはpart1にのみある。part2とpart3をそれぞれヘッダー付きCSVとして読み込むと、各パートの先頭データ行が失われる。
