---
id: K0420
title: 初手49のWIN側frontierは第7次再被覆で1,932証人・6.8k AND幅・未閉鎖1,745
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0417
  note: LOSS側共同frontier 31,546と個別上界（49:2055）の比較基準
- type: depends_on
  target: K0371
  note: 元先手固定のAND/OR伝播（S4=OR・S5=AND、終局偶数LOSS）
- type: depends_on
  target: K0416
  note: S5の全子閉包が必要なことと未閉鎖根の前例
artifacts:
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/s4_win_polarity.py
  role: source
  note: K0371極性の単一真実源（free/open/dead分類）
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/test_s4_win_polarity.py
  role: verifier
  note: K0414 S4のdead・WIN子free・UNKNOWN・終局・frontier照合の回帰5件
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/win_side.py
  role: source
  note: 応手軌道縮約・S4分類・証人被覆のWIN側依存分析（初手49で約45分）
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/win_witness_masks.py
  role: verifier
  note: 証人被覆の幾何再検証（正準・未cache・被覆成立・総数一致）
- path: research/experiments/n11-proof-cost-comparison-20261012/scripts/measure_overlap.py
  role: source
  note: LOSS共同計画との極性衝突測定とパイロット再生成
- path: research/experiments/n11-proof-cost-comparison-20261012/output/win-side-analysis.json
  role: data
  note: 65応手軌道の閉鎖性・証人数・AND幅（schema v2、極性訂正済み）
- path: research/experiments/n11-proof-cost-comparison-20261012/output/win-witness-masks.json
  role: certificate
  note: 検証済み証人1,945マスク（正準・未cache・被覆成立）
- path: research/experiments/n11-proof-cost-comparison-20261012/output/overlap-and-pilots.json
  role: data
  note: 極性衝突29件・legal分布・最安10件
- path: research/experiments/n11-proof-cost-comparison-20261012/output/superseded-polarity-bug-20261012/README.md
  role: manifest
  note: 極性誤りの旧出力3件の履歴化と新旧対応
- path: research/experiments/n11-proof-cost-comparison-20261012/README.md
  role: source
  note: 証明戦略比較の全体記録（課題1〜5、主軸判断と実探索条件を含む）
- path: research/experiments/n11-s5-s6-quotient-20261013/output/pilot-209644-terminal-verification.json
  role: certificate
  note: 保存WIN証人集合の1件が終局DAGで独立閉鎖したreceipt
- path: research/experiments/n11-night-plan-update7-20261015/output/win-side-reanalysis7.json
  role: data
  note: 第7次再被覆（pool 1,932・未閉鎖1,745・AND幅6,812・ranking照合込み）
scope: 初手49の全65応手軌道（安定化群でD4縮約）・各119 third手・全fourth手S4の既存cache分類と楽観的WIN証人被覆。solver探索なし。
evidence: 現行の保存1,945証人集合はK0423により1件（209644）が独立終局閉鎖、未閉鎖1,944。全応手閉鎖や被覆再最適化は未実施。極性訂正時の測定として共有モジュールでK0371極性を適用し直した。到達133,924 S4中free 98・dead 3・open 133,823で、65応手軌道すべてにviable thirdがある（無料閉鎖0・証人要65）。AND境界は7,519 S4分岐、楽観的証人は1,945相異なるS5で、被覆検証器が正準性・未cache・被覆成立・総数一致を通過した。各証人は全S6先手WINの閉包が別途要る。LOSS側共同要求集合との重なり29件は両側が逆極性で要求する衝突点であり、共有資産ではない（旧「両用16件」は極性誤りの産物）。frontier legal手数は60〜116手。
---

初手49の先手WIN証明は、応手側に障害ゼロ（65/65閉鎖可能）でfrontier 1,945・AND幅7.5kという有限規模に収まる。ただし証人1個あたりの全S6先手WIN閉包費は未測定のため、frontier規模の比較は証明費用の比較ではない。

訂正記録：本項目の初版はS5 LOSS子をWIN証人とする極性誤りで65/65・無料5・証人約1.74k・AND幅7,503・両用16件を報告していた。K0371との照合で誤りを確定し、旧出力3件を履歴化して全結果を再計算した。free/open/deadの定義と証人の意味（S5 WIN化の楽観的前線）が変わり、重なりの解釈は共有から衝突へ反転した。

測定に基づく方針判断（証明ではなく方針）：主軸は後手WIN側共同計画を維持し、先手WIN側は証人パイロット閉包で単価実測する。パイロットは極性衝突29件（どちら側にも決定的）を最優先し、次に最安10件で閉包単価を測る。パイロット成功なしに大量探索を開始しない。

## 独立終局パイロットの追加

K0423で極性衝突候補209644（S={49,55,60,65,71}）の元先手WINをtrusted葉0の終局DAGで独立証明した。
保存された1,945証人集合のうち1件が閉鎖され、この固定集合の未閉鎖は1,944件。
全65応手が実際に閉鎖されたわけではなく、WIN側の被覆を再最適化した数ではない。
旧LOSS共同との29衝突候補のうち1件がWIN側に決着した。もう一つのパイロット558600 LOSSは旧共同側の要求で、WIN証人集合には含まれない。

## 夜間バッチ反映（2026-10-14・K0424）

夜間適応探索でWIN 6件の確定とLOSS 6件（新規3＋昇格3）の除外を保存poolに反映し、
再被覆・再検証した現行値は使用可能証人1,933・未閉鎖1,746・AND幅6,812・
closable 59軌道・unclosable [1,2,4,15,79,101] の6軌道。新規証人の創作はなし。
上記の1,945／1,944はK0423時点の履歴値。詳細はK0424と
`research/experiments/n11-night-plan-update6-20261014/output/win-side-reanalysis6.json` を参照。

## 第7次計画更新（2026-10-16・update7）

162106 WINとS6由来LOSS 3件（381840 / 402066 / 550881）を反映した再被覆の現行値:
使用可能証人 **1,932**（保存1,945から層別14件のうちpool内13 maskを除外。S6 LOSS 3 maskは
保存pool外のため縮小に寄与せず）・未閉鎖 **1,745**・AND幅 **6,812**・closable **59**・
unclosable `[1,2,4,15,79,101]` の6軌道（いずれも第6次から不変）。
chosen third は全59軌道で同一、cover差分は r=59 のwitness_count 25→24 のみ。
162106により保存chosen thirds内で18分岐がFREE化（純増12、r=59/60/71。rankingの
if_win_newly_free_branches=18と一致）、dead fourthによるthird失格は0。
第6次の1,933／1,746／AND幅6,812は履歴値。詳細は
`research/experiments/n11-night-plan-update7-20261015/output/win-side-reanalysis7.json` を参照。
