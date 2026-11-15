# (4,5) 4×21 bounded-edit surgery — m=20 witness 両埋め込みからの完全列挙負 (2026-11-15 高速レーン)

## 位置づけ

`M_{4,5} ∈ [21, 140]` (witness 帯 m=5..20、上界 K0318 U_{4,5}=140、K0833)。
前線 m=21 は def-mode OR 210s INDET (3,296,257 conflicts) ・
2クラス被覆 (lex=H rowY=0/1) 600s INDET (6,924,496/7,286,846 conflicts) で未決着
(four-row-q4-q5-frontier-20261115)。本実験は m=20 witness の近傍だけを
高速に完全列挙し、「m=21 witness が m=20 witness の小修正で得られるか」に答える。
absence-capable な完全分解掃引は
[four-row-q5-m21-class-split-20261115](../four-row-q5-m21-class-split-20261115/) (IN FLIGHT)。

## status

**COMPLETE (有限完全列挙・局所負。4×21 witness 全体の不在主張ではない)**

## claim

m=20 witness (rows [4,4,4,3]、15石、sat2-rowY3 SAT 600,345 conflicts・jsVerify/pyVerify 済。
seed は `scripts/seed20.json`) を 4×21 盤に2通りに移植 (offX=0: 右端に空列追加 /
offX=1: 全体を1列右シフト) し、追加 ≤2石・除去 ≤2石・最終石数 ≤15
(targetMax=15 = 単一欠損 witness サイズ w(q−1)−1) の編集を**完全列挙**した。
種の移植で未遮断のまま残る空点は offX=0 では T′={(20,3)}、offX=1 では T′={(0,3)} の1点のみ。

結果 (どちらも witness 0件・すべての最終状態葉は safe):

| 埋め込み | T′ | nP | nPpruned | nRmLeaves (=nSafe) | nMaximal | nWitness | unblocked_Tprime | unsafe |
|---|---|---|---|---|---|---|---|---|
| offX=0 | {(20,3)} | 2,415 | 1,269 | 12,754 | 0 | 0 | 1,584 | 0 |
| offX=1 | {(0,3)} | 2,415 | 1,272 | 12,816 | 0 | 0 | 2,311 | 0 |

census 542 曲線 (circles 538, nEa 4,024, nEb 5,584) は sat2.js def-mode (4,21,5)
の記録曲線数 542 (q5-w4-def-search records) と一致。
surgery4.js の buildCensus4 q≤w 完全性検査は 8/8 PASS 済みで (4,10,5)/(4,20,5) を含む
(four-row-q4-m35-surgery-20261115)。offX=0 elapsed 363ms / offX=1 381ms・決定的。

**系 (有限・局所)**: m=20 witness の両水平埋め込みから 2+2 石編集以内に
到達できる 4×21 の ≤15石 witness は存在しない。すべての最終状態葉は safe (unsafe=0)
だが最大化は全敗 (fail の主因は T′ 未遮断 1,584/2,311、次いで unblocked_exposed)。
連続幅間の witness jump が大きい先行観察
((4,4) m=34→35 surgery 完全負・(5,6) m=21→22 sd≥7 完全負) と整合する。
4×21 全体の不在決着は本実験の範囲外。

## 手法と provenance

- usage: `node surgery4.js 4 5 21 scripts/seed20.json 2 2 15 [offX]`
- 決定的 (census・列挙とも純 JS 整数演算・並走なし)。
- 依存: sat.js (K0810 verbatim)。
- md5: surgery4.js `7dc40fc0f08150692d64241d0c6c4029`
  (four-row-q4-m35-surgery-20261115 と同一 blob) /
  sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c` /
  seed20.json `bb5eb46356728a5a4b7d7c26b7a0f2b0`。

## files

- `scripts/surgery4.js` — surgery machine v2 (census 完全性修正版・q=5 でも 8/8 PASS)
- `scripts/sat.js` — K0810 検証器 (依存)
- `scripts/seed20.json` — m=20 witness (sat2-rowY3 SAT・2系統検証済み)
- `output/surg_m21_off0.jsonl`, `output/surg_m21_off1.jsonl` — 実行 summary

## 次課題

- absence の決着は class-split 掃引 (four-row-q5-m21-class-split-20261115) が担う。
- 3石編集 (sd≤6) 拡張は (5,6) 5×23 と同様に構成数が急増するため、掃引結果を見てから判断。


## 追記: sd≤6 (追加3・除去3) 拡張 — こちらも完全列挙負

同じ seed・同じ targetMax=15 で編集上限を (2,2) → (3,3) に拡張した
(`node surgery4.js 4 5 21 scripts/seed20.json 3 3 15 [offX]`)。
構成数は (5,6) m=22 surgery の (3,3) と同規模で、両埋め込みとも
~8秒・決定的に完了。

| 埋め込み | nP | nPpruned | nRmLeaves (=nSafe) | nMaximal | nWitness | elapsed |
|---|---|---|---|---|---|---|
| offX=0 | 54,809 | 20,478 | 1,250,587 | 0 | 0 | 8,033ms |
| offX=1 | 54,809 | 20,619 | 1,256,103 | 0 | 0 | 8,024ms |

**系 (有限・局所・強化)**: m=20 witness の両水平埋め込みから
3+3 石編集以内 (sd≤6) で到達できる 4×21 の ≤15石 witness は存在しない。
fail 内訳は offX=0 が unblocked_hole 718,846・T′ 未遮断 52,521、
offX=1 が unblocked_hole 633,894・T′ 未遮断 219,916 で、
safe でも maximality が全域で失敗する構造は (2,2) と同一。
(4,4) m=35 は (2,2) で止めたが、本幅は (3,3) まで完了済み。
(4,4) m=35 の (3,3) 実施可否は class-split 掃引の進展と合わせて判断する。


## 追記: 独立検証 (2026-11-15・TS sandbox 第2実装) — (2,2)/(3,3) 全カウンタ EXACT 一致

surgery4.js と独立の第2実装 (センサスは三重計数ベース・chord-pair/L/E-a/E-b 不使用、
列挙も独自 DFS) を TS sandbox で実行し、本実験の全カウンタを再現した
(Node 移植版: `scripts/surgery_verify5.js`・再実行可能):

| instance | nP | nPpruned | nRmLeaves | nWitness | T′ |
|---|---|---|---|---|---|
| (2,2) offX=0 | 2,415 | 1,269 | 12,754 | 0 | {(20,3)} |
| (2,2) offX=1 | 2,415 | 1,272 | 12,816 | 0 | {(0,3)} |
| (3,3) offX=0 | 54,809 | 20,478 | 1,250,587 | 0 | {(20,3)} |
| (3,3) offX=1 | 54,809 | 20,619 | 1,256,103 | 0 | {(0,3)} |

全カウンタが本 README 記録と EXACT 一致 (nEmpty 69・seed safe check・T′ も一致)。

- **陽性対照 (4×20)**: seed = 既知 m=20 witness −{(4,2),(14,2)} (13石) で (2,2)/15 を
  走査し、既知 witness (rows [3,4,4,4]) をちょうど1件再発見
  (nMaximal = nWitness = 1・full verify: safe + maximal + minRow 3)。
  witness 検出経路の end-to-end 実証 (本実験の4走査は witness 0 のため
  検出経路が未行使だった)。
- **L2 補題の独立確認**: r∈Rm の穴は F でちょうど4石の曲線 c′∋r で再ブロック
  される必要があり、c′ は cnt(c′)+|c′∩P| = 4+|c′∩Rm| ≥ 5 (赤字正) を満たす
  → Rm ⊆ 赤字曲線上の石。cands 制限の健全性を証明レベルで再確認した
  (非赤字除去を許す「ギャップ領域」の追加列挙は不要と判断した根拠)。
- **センサス相互検証**: 三重計数 (非共線三重 89,228・円 538 = 5:180/6:340/8:18
  + 行4 = 542 曲線) は sat2.js def-mode 記録・sa21.js census と一致。
  4×20 は 491 曲線 (円 487・非共線 76,932)。
- 決定的 (RNG 不使用・純整数演算)。実行環境は依然全面停止のため TS sandbox で
  実施し、Node 版スクリプトを同時 push (復旧後に bit 再現確認可)。
- **位置づけ**: 本追記は sd≤6 主張の独立性検証を強化するもので、
  4×21 全体の不在決着は従来どおり class-split 掃引
  (four-row-q5-m21-class-split-20261115・c0k3p0/p1) が担う。


## 追記2: 第3の水平配置 offX=−1 の走査と剛体配置全12通りカバー (2026-11-15)

seed (列幅 x∈[1,19]) は 4×21 に水平 3通り (offX∈{−1,0,1}) で置けるが、
従来走査は offX∈{0,1} のみだった。offX=−1 (空列が両方右側: 列19,20) は
σ が H/V 対称でないため鏡映では既存走査から導けず、独立に走査した
(検証済み第2実装 surgery_verify5.js と同じ TS sandbox 実装・CLI は負の offX も可):

| 埋め込み | T′ | nP | nPpruned | nRmLeaves | nMaximal | nWitness |
|---|---|---|---|---|---|---|
| offX=−1 (2,2) | {(19,3),(20,3)} | 2,415 | 1,277 | 12,588 | 0 | 0 |
| offX=−1 (3,3) | {(19,3),(20,3)} | 54,809 | 20,811 | 1,252,862 | 0 | 0 |

- offX=−1 では T′ が 2点 (空2列とも未遮断・row 3) で、offX=0/1 の 1点より厳しい。
  それでも maximality 全敗・witness 0。決定的・census は同一 (542曲線)。

**等変性補題 (証明)**: 盤面対称 ρ ∈ D₂ (H/V/HV 鏡映) に対し、
surgery 球 {F : sd(F,S)≤6, |F|≤15} は ρ で球 {F : sd(F,ρS)≤6} に全単射され、
safety・maximality・石数・行欠損 (minRow・行多重集合は置換のみ) はすべて保存される
(円・行の census 族は ρ 不変・sd は細胞全単射で保存)。
よって witness は ρ(S) でも witness。

**系 (配置完全カバー・有限・局所)**: 水平 3走査 (offX=−1/0/1) と等変性補題により、
m=20 witness の剛体配置全 12通り (水平 3通り × 面内対称 4像・すべて相異なる:
σ の H/V 対称性は機械検査で否定済み) の sd≤6 球は空。
「両水平埋め込み」条件は全剛体配置に強化された。


## 追記3: 列挿入埋め込み族 (内部分割を含む全21位置) の走査 (2026-11-15)

剛体配置に加え、4×20 witness を 4×21 へ「列挿入」で埋め込む族
(新列を位置 c∈{0..20} に挿入: x<c の石はそのまま・x≥c の石は +1 シフト) を
全位置 safe 判定した (第2実装と同一 TS sandbox 機械・census 542曲線共通):

- **safe**: c ∈ {0,1,3,4,6,8,15,16,17,18,19,20} (12位置・6 distinct 配置:
  c=0/1 ≡ 剛体 offX=1、c=20 ≡ 剛体 offX=0、
  c=3/4 (13石移動)・c=6 (10石)・c=8 (7石)・c=15..19 (1石 [19,3]→[20,3]))
- **unsafe**: c ∈ {2,5,7,9..14} (9位置・いずれも 5石円の出現。
  c=14 のみ unsafe 円2本、他は1本)

つまり witness の左〜中央の密な領域では列分割が即座に安全性を破壊するが、
特定の隙間 (3/4, 6, 8) と右端石の手前〜右端 (15..20) では分割が許容される。

**4つの新規 safe 分割配置の surgery 走査** (targetMax=15・決定的):

| seed | T′ | nP | nPpruned | nRmLeaves | nWitness |
|---|---|---|---|---|---|
| split c=3 (2,2) | 7 | 2,415 | 1,282 | 11,320 | 0 |
| split c=6 (2,2) | 11 | 2,415 | 1,286 | 10,360 | 0 |
| split c=8 (2,2) | 10 | 2,415 | 1,285 | 11,067 | 0 |
| split c=15 (2,2) | 4 | 2,415 | 1,278 | 12,431 | 0 |
| split c=15 (3,3) | 4 | 54,809 | 20,761 | 1,271,303 | 0 |
| split c=3 (3,3) | 7 | 54,809 | 20,832 | 1,252,781 | 0 |
| split c=6 (3,3) | 11 | 54,809 | 20,836 | 1,247,430 | 0 |
| split c=8 (3,3) | 10 | 54,809 | 20,835 | 1,274,014 | 0 |

- split c=15 (剛体 offX=0 から石1個の移動・sd=2) は (3,3) まで完全列挙負。
  T′=4 (未遮断4点) が (2,2)/(3,3) ともに maximality 全敗の主因。
- **系 (有限・局所・族完全)**: 列挿入埋め込み族の safe 6配置
  (剛体2 + 分割4) の sd≤6 球は**すべて空** ((2,2) は全6配置・(3,3) も全6配置で
  完全列挙済み・witness 0)。追記2の剛体配置全12通り (等変性込み) と合わせ、
  「m=20 witness を列挿入で 4×21 に埋め込んだ全配置からの sd≤6 到達可能性」は
  完全に否定された (≤15石 witness は存在しない)。
- offX=−1 (追記2) は列挿入族の外 (witness 自身の空列0の削除に相当) で、
  こちらも (3,3) まで完全列挙負。
- 陰性対照として unsafe 位置 (c=2 など) では seed safe check が発火し
  機械が即座に reject することも確認 (機械の防御検査が実働)。
