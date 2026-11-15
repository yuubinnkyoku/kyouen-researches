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
