# (4,4) 4×35 bounded-edit surgery — m=34 witness 両埋め込みからの完全列挙負 (2026-11-15 高速レーン)

## 位置づけ

`M_{4,4} ∈ [35, 237]` (witness 帯 m=4..34、上界 K0068 T_4=237、K0833)。
前線 m=35 の決着を担う完全分解掃引は
[four-row-q4-m35-class-split-20261115](../four-row-q4-m35-class-split-20261115/) (IN FLIGHT)。
本実験はその補助レーンとして、既知 witness (m=34) の近傍だけを高速に完全列挙し、
「m=35 witness が m=34 witness の小修正で得られるか」に答える。

## status

**COMPLETE (有限完全列挙・局所負。4×35 witness 全体の不在主張ではない)**

## claim

m=34 witness (rows [3,3,2,3]、11石、K0833 帯・seed は `scripts/seed34.json`) を
4×35 盤に2通りに移植 (offX=0: 右端に空列を追加 / offX=1: 全体を1列右シフト) し、
追加 ≤2石・除去 ≤2石・最終石数 ≤11 (targetMax=11 = 単一欠損 witness サイズ w(q−1)−1)
の編集を**完全列挙**した。左記の種の移植で未遮断のまま残る空点は
offX=0 では T′={(34,2)}、offX=1 では T′={(0,2)} の1点のみ。

結果 (どちらも witness 0件・すべての最終状態葉は safe):

| 埋め込み | T′ | nP | nPpruned | nRmLeaves (=nSafe) | nMaximal | nWitness | unblocked_Tprime | unblocked_hole | unblocked_exposed | unsafe |
|---|---|---|---|---|---|---|---|---|---|---|
| offX=0 | {(34,2)} | 8,385 | 3,785 | 20,277 | 0 | 0 | 560 | 2,210 | 158,474 | 0 |
| offX=1 | {(0,2)} | 8,385 | 3,240 | 21,824 | 0 | 0 | 4,488 | 1,655 | 167,017 | 0 |

**系 (有限・局所)**: m=34 witness の両水平埋め込みから
(追加2・除去2 石以内の編集距離で) 到達できる 4×35 の ≤11石 witness は存在しない。
連続幅間の witness jump が大きいという先行観察
((5,6) m=22→23 sd≥7 完全負・(7,5) m=33→34 2石移動で解決という対比)
と整合する。4×35 全体の不在決着は本実験の範囲外。

## census 完全性修正 (surgery4.js の本体)

従来の surgery.js (eight-row-q9-m29-surgery-20261115 版・md5 94baa517、
five-row-q6-m22-surgery-20261115 が verbatim 再利用) の chord-pair census は
q > w では完全だが **q ≤ w では不完全**: 非行の直線 (対角線など) と、
(1点,1点,1点) 型・(2点,1点) 型の行分布を持つ円が抜ける。
(4,35,4) は q=w=4 なので該当する。

`surgery4.js` は列挙コア (枝刈り補題 L1/L2/L3・DFS・最終検査・emitWitness) を
surgery.js から verbatim 移植し (空白正規化後の一致を機械検証済み)、
census 生成 `buildCensus4` だけを差し替えた:

- (L) sat.js `lineABC` による全直線 (行直線の上位集合)、
- (E-a) 3行から1点ずつ通る全円 (各行 ≤1点の円をすべて被覆)、
- (E-b) 1行の2点 + 別行の1点を通る全円 (2点行をちょうど1つ持つ円を被覆)、
- chord-pair ポートは verbatim (2点行を2つ以上持つ円を被覆)。

任意の (w,q) で円は1行あたり ≤2 窓点を持つため、
2点行が0個 → (E-a)、1個 → (E-b)、≥2個 → chord-pair で全列挙される
(非行直線は (L))。

**census 完全性検査** (`census4_check.js`): buildCensus4(w,m,q) が
sat.js 全三つ組 buildCensus(w,m,q) と点集合族として完全一致するかを検査。
**8/8 PASS** (output/census4_check_output.txt):

| (w,m,q) | sat.js 曲線数 | buildCensus4 曲線数 | 一致 |
|---|---|---|---|
| (4,8,4) | 485 | 485 | PASS |
| (4,20,4) | 7,689 | 7,689 | PASS |
| (4,35,4) | 41,607 | 41,607 | PASS |
| (5,12,4) | 2,875 | 2,875 | PASS |
| (6,10,4) | 2,735 | 2,735 | PASS |
| (3,24,4) | 6,413 | 6,413 | PASS |
| (4,10,5) | 89 | 89 | PASS |
| (4,20,5) | 491 | 491 | PASS |

(4,35,4) の 41,607 曲線は class-split 掃引の sat.js census とも一致。
q=5 (w=4) でも PASS しており、(4,5) m=21 surgery への適用も正当化される。

## 手法と provenance

- usage: `node surgery4.js <w> <q> <m> <seed.json> <maxP> <maxRm> <targetMax> [offX]`
- 決定的 (census・列挙とも純 JS 整数演算・並走なし)。offX=0 elapsed 3.5s / offX=1 3.9s。
- 依存: `sat.js` (K0810 verbatim・md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c)。
- md5: surgery4.js `7dc40fc0f08150692d64241d0c6c4029` /
  census4_check.js `dadbeae1b02ad2a9650c6ce86021fb9c` /
  seed34.json `98069f5e9d47c1fa8397a3042b96be33`。
- 出力: `output/surg_m35_off0.jsonl` / `output/surg_m35_off1.jsonl`
  (summary 1行ずつ・census 内訳 nEa/nEb を含む)。

## files

- `scripts/surgery4.js` — surgery machine v2 (census 完全性修正版)
- `scripts/census4_check.js` — census 完全性検査器
- `scripts/sat.js` — K0810 検証器 (依存)
- `scripts/seed34.json` — m=34 witness
- `output/surg_m35_off0.jsonl`, `output/surg_m35_off1.jsonl` — 実行 summary
- `output/census4_check_output.txt` — 完全性検査 8/8 PASS 出力

## 次課題

- (4,5) m=21 surgery (m=20 witness seed・q=5 でも census 完全性は検査済み) — 別レーン frontier IN FLIGHT との重複に注意。
- m=34 witness からの 3石編集 (sd≤6) 拡張は (5,6) 5×23 と同様に構成数が急増するため、class-split 掃引の進展を待って価値判断。
