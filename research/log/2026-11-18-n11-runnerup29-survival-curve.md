# 2026-11-18 N11 runner-up parent（29行）最小cover 45.9e15のtop-k ban生存曲線の完全化（k=0..12全13点・厳密）

## 成果

runner-up parent `00000000000000003800000009000000`（29 open non-STERILE行・cost 15 exact・
class-2 ranking 2位）の**総 45,949,721,018,967,524 通りの最小coverのうち、上位k本のrootを
banした（そのrootを1本も使わない）最小coverが何通り残るか**を、**k=0..12の全13点**で
厳密に決定した。出版済みban生存曲線（commit `95b11316`・15 checks・k∈{0,1,2,3,4,5,6,7,8,10,12}
でk=9/k=11が欠落）を完全化するもので、**欠落2点（k=9・k=11）を新規確定し、既出版11点は
total/A/B/memo/gets全フィールドで完全再現、ban順も完全一致**する。ban順は出版membership
降順（tieはroot hex昇順）で上位12本すべてpair root・12 pair typeすべて異なる。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/runnerup29_survival_curve_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-survival-curve-20261118.json`
- **35 checks all PASS・二重実行 byte-identical**（全13点の独立再計算 + assemble済み最終JSONのbyte比較）。

## 生存曲線（surviving = 総数 − kill、naive = 上位k本のmembership単純和）

| k | surviving minimum covers | exact kill | naive単純和 |
|---|---|---|---|
| 0 | 45,949,721,018,967,524 | 0.0000% | 0.0000% |
| 1 | 43,539,706,586,445,092 | 5.2449% | 5.2449% |
| 2 | 41,140,118,223,522,881 | 10.4671% | 10.4703% |
| 3 | 39,008,287,432,534,448 | 15.1066% | 15.6382% |
| 4 | 36,760,423,019,767,177 | 19.9986% | 20.8009% |
| 5 | 34,701,060,306,340,041 | 24.4804% | 25.8229% |
| 6 | 32,629,123,694,539,810 | 28.9895% | 30.8341% |
| 7 | 30,703,672,731,318,656 | 33.1798% | 35.8098% |
| 8 | 28,891,341,236,187,996 | 37.1240% | 40.7839% |
| 9 | 27,080,952,234,392,986 | 41.0639% | 45.7377% |
| 10 | 25,408,316,640,170,202 | 44.7041% | 50.6872% |
| 11 | 23,722,672,563,006,232 | 48.3725% | 55.6270% |
| 12 | 21,963,916,318,152,072 | 52.2001% | 60.5358% |

k=10のnaive 50.6872%は出版top-10 membership単純和50.69%と一致（座標確認）。
新規確定の2点: **k=9 → 27,080,952,234,392,986**（kill 41.0639%・marginal 1.810389001795e15）・
**k=11 → 23,722,672,563,006,232**（kill 48.3725%・marginal 1.685644077163970e15）。

## 方法

出版偶数/奇数r frameworkをban後の重み縮約にそのまま適用: surviving(k) = A2 + B2
（A2 = Σ_s w'(s)·pm(V∖s)、B2 = Σ_d Σ_{a<b} w'(d,a)w'(d,b)pm(V∖{d,a,b})、
pmはban済みrootを除いた重み付き完全マッチング数でPmLazyが供給）。最小coverの
構造（A型 = 14 pair + 1 singleton・B型 = 15 pair・1行二重被覆・maxspan 2）により、
この縮約公式は「ban rootを1本も使わない最小cover」を過不足なく数える。k=0点は
出版総数・A/B（37,317,784,435,384,705 / 8,631,936,583,582,819）のスクラッチ完全再現
であり、実装の第一検証。

- 各k点は独立したPmLazy（state cap 6M・約3.52M状態・約27秒/点）で計算し、
  point modeでcheckpoint化。assemble modeが構造再導入・全35 check・最終JSON化を担う。
- 検証: 出版cost-12 output（blob `c05de9d0`）の全1,151 singleton membershipをPmLazyが
  完全再現（0不一致）・出版runner-up29 membership output（blob `05f54eb5`）との構造全一致
  （rows/candidates/distinct roots/span histogram/pair type/multiplicity/per-row値）・
  **出版ban生存曲線（blob `92db40a2`）の11点全再現**（k=0 total/A/B出版総数と完全一致・
  k=1 marginal==出版membership・k=2 kill==包含排除）。
- 環境制約の記録: 本サンドボックスは長時間バックグラウンドプロセスを数分でkillする
  ため、全点を単一プロセスで回す代わりに「1呼び出しで数点ずつchunk実行 + point file
  checkpoint」方式を取った（cgroup RAM上限約1.09 GBに対しstate cap 6Mで安全圏）。

## 主要な新所見

1. **上位12 root banでも52.20%kill・21,963,916,318,152,072本（47.8%）の最小coverが生存する**。
   cover計画空間の冗長性は極めて高く、上位rootのelimination（REFUTED化）を積み重ねても
   このparentの最小cover計画が尽きる見込みは低い。上位root集中型の証明戦略だけでは
   parent閉鎖に到達しない定量的裏付けである。
2. **naive単純和はkillを過大評価する**: k=12でnaive 60.5358% vs 厳密52.2001%
   （差8.34ポイント = joint重複、絶対値3.83e15 covers）。k=2の差は出版top-2 joint
   （1,493,071,388,910）と厳密一致し、k=1のmarginal kill 2,410,014,432,522,432は
   出版membership（2,410,014,432,522,432）と厳密一致する（恒等式の実測検証）。
   k=2の厳密kill 4,809,602,795,444,643 == m1 + m2 − joint
   （m2 = 2,401,081,434,311,121・出版rank-2 membership）。
3. **ban上位12本はすべてpair rootで、12個のpair type（被覆行対）はすべて異なる**
   （行indexの重複はある: 16を4本・10を7本が含む。 membership上位層の行集中と整合）。
   marginal killはk=1の2.410e15をピークに概ね逓減し、k=11で1.686e15・k=12で
   1.759e15（厳密単調ではない）。各点で marginal kill ≤ 最後にbanしたrootの出版membership
   が成立し、差（= 以前のban rootとの重複cover数）は全点非負。
4. survivalは全点正で、k=12でも半数近くの計画が残る。削除でこのparentのcover空間が
   空になるkはこの範囲に存在しない。

## 解釈上の注意

生存曲線は「banしたrootを使わない最小cover計画の数」の組合せ論である。探索コストでも
verdictでもなく、ban rootをREFUTED化できるかの予測も含まない。REFUTED-D10・STERILEは
LOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
いずれも**UNKNOWN**のまま。
