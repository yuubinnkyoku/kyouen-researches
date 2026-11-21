---
id: K1205
title: 既刊s_n witnessのD4・平行移動全配置走査: より大きいホスト盤（12..15）ではどの等長配置も最大性を失う（min uncovered 4/10/9/8）、uncovered 0は自己盤のD4像のみ
kind: computation
status: computed
topics: [maximal-safe, geometry]
aliases: ["witness transplant non-transfer", "s12/s13 lane transplant scans"]
relations:
- type: related
  target: K0320
  note: "n=11..15のn−1石構成witness 5件（およびK0031 n=7・K0038 n=10）のホスト12..15への全D4像×全収まる平行移動走査。いずれの等長配置もホスト盤では非極大（min uncovered 4/10/9/8: 11→12, 12→13, 13→14, 14→15で単調に悪化しない）。安全性は平行移動・鏡映で保存されるため全配置がsafeのまま、最大性だけが失われる。K0320の本文・status不変"
- type: related
  target: K0149
  note: "本項はs_nの単調性を支持も反証もしない有限観測。『既刊witnessをそのまま大きい盤へ置いてもs_12≤10・s_13≤11相当の上界は出ない』という構成的ルートの下位互換性の欠如を記録するのみで、他の配置による証明の可能性は排除しない"
artifacts:
- path: research/experiments/s12-s13-upper-witness-20261121/records/transplant_host12.json
  role: data
  note: "ホスト12×12: K0031/K0038/K0320(n=11)の全配置とuncovered個数ヒストグラム・最小配置"
- path: research/experiments/s12-s13-upper-witness-20261121/records/transplant_host13.json
  role: data
  note: "ホスト13×13: 上記+K0320(n=12)、min uncovered 10"
- path: research/experiments/s12-s13-upper-witness-20261121/records/transplant_host14.json
  role: data
  note: "ホスト14×14: さらにK0320(n=13)、min uncovered 9"
- path: research/experiments/s12-s13-upper-witness-20261121/records/transplant_host15.json
  role: data
  note: "ホスト15×15: K0320(n=14)も含む、min uncovered 8。自己盤15×15上のK0320(n=15)はD4像8件がuncovered 0（較正アンカー）"
- path: research/experiments/s12-s13-upper-witness-20261121/scripts/hunt.mjs
  role: verifier
  note: "transplant モード: D4像×全fitting平行移動をセル集合で重複排除して全列挙、State機械でuncovered計数（安全性は不変量として主張時検査）"
- path: research/experiments/s12-s13-upper-witness-20261121/README.md
  role: source
  note: "走査規模・解釈規約（等長配置の完全走査であって、大手の非存在陳述ではない）"
---

# 既刊witnessのホスト盤12..15への全等長配置走査

## 有限計算の内容

K0031（7×7, 7石）・K0038（10×10, 10石）・K0320（11..14盤, n−1石）の各witnessについて、ホスト盤m∈{12,13,14,15} × m 全体に対し、witnessのD4像8種のそれぞれを盤内に収まる全平行移動で走査した（セル集合の同一視で重複排除、タスク規模は各recordsのplacements欄）。判定はquartetカタログState機械（censusはK1204のアンカー全一致ゲート通過後のもの）で行い、全配置のuncovered空点数・ヒストグラム・最小配置の空点リストを機械可読で保存した。

結果:

- **どのsource×hostの組でも uncovered 0（=ホスト盤でそのまま極大）は存在しない**。uncovered 0の配置はsourceがその自己盤上に置かれた場合のD4像（代表点で8件、運搬元では最大8件の重複排除済み像）のみ。
- K0320 witnessの最小uncoveredは 11→12で4、12→13で10、13→14で9、14→15で8。「大きい盤に移すと少なくとも4〜10個の追加攻撃（＝1〜数石相当）が必要」であり、K0320のn−1構成が盤ステップごとにちょうど1石追加するパターンと整合する。
- 安全性: 平行移動・D4鏡映は共線・共円の検出行列式を不変に残すため、すべての配置がsafeであることは予定通りであり、全走査でviol>0は0件（不変量検査として機械が表明）。

## 限界（解釈規約）

- 完全なのは「既刊witnessの等長コピー」の範囲のみ。ホスト盤上のまったく別のk石配置の可能性には一切触れない（ゆえにs_16≤14などの主張はここから出ない。n≥14の上界主張は本レーンの非目標）。
- uncovered 0 copiesが自己盤のみ、という観測は「s_n witnessは一般に大きい盤のwitnessを兼ねない」ことの3+証拠点（各ホストの表が11→12等の組ごとにある）であって、全称命題ではない。
- 本項からK0149（単調性）への影響は一切ない。上位数列の下から押し上げにも上から押さえにも使えない有限観測であり、構成ルートの探索的手がかり（各witnessの次盤平均何Attack損か）としてのみ位置づける。
