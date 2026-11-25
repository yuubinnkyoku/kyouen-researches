# 2026-11-20 six-row q5/q6 frontier — 単一オーナー宣言（高速レーン）

- 2026-11-20 13:25Z: (6,5) 6×20・(6,6) 6×16 の行欠損極大 SAT 前線掃引
  （sat2.js def-mode + kissat 4.0.4・rowY 分割含む・延伸幅含む）を
  research/experiments/six-row-q5-q6-frontier-20261120 で着手する。
  repo検索（README・log・experiments・直近commits）時点で未着手・未宣言を確認。
  他レーンは 4×22（m22 batchD/E・four-row-q5-m22-class-split）を所有中であり、
  本レーンはそれに触れない。
- 現在の境界: M_{6,5} ∈ [20, 658]（K0808・U=658 は K0318 代入）・
  M_{6,6} ∈ [16, 495]。
- 着手時点の観測最大K番号: K1145（最終K番号はpush直前に3点確認で採番）。
- 2026-11-20 15:0Z頃: 掃引完了・成果を main に出版。
  - **(6,5) q=5**: def-mode m=19..27 全SAT（conflicts 261/750/985/657/15,541/
    17,610/19,169/20,212/89,830・0.2〜38.9s）。m=28 は def-mode 240s INDET
    （894,706）→ rowY=0 行固定分割で SAT（464,040 conflicts・146.1s）。
    **witness帯 m=8..28・M_{6,5} ∈ [29, 658]**（着手時 [20, 658]）。
    m=29（現前線）: rowY=0 220s INDET（720,202）・rowY=1/2 --sat 130s INDET
    （502,044/469,125）— 未解決記録で不在主張ではない。
  - **(6,6) q=6**: def-mode m=16..24 全SAT（conflicts 46/451/312/590/14,808/
    10,066/277,198/919,243/889,446・0.1〜134.2s）。**witness帯 m=8..24・
    M_{6,6} ∈ [25, 495]**（着手時 [16, 495]）。m=25（現前線）: def 140s INDET
    （857,314）・rowY=0 140s INDET（860,873/838,046〔--lex=H〕/1,014,217〔--sat〕）・
    rowY=1/2 --sat 130s INDET（951,654/929,165）— 未解決記録で不在主張ではない。
  - **K0808 の greedy 未解決2ケースはいずれも witness 存在で決着**:
    (6,5) 6×20（750 conflicts・0.6s・23石）・(6,6) 6×16（46 conflicts・0.1s・29石）。
    greedy非発見が不在を意味しないことの鮮明な実例（K0808の明記通り）。
  - 副次成果: (6,19,5) def SAT witness は 22石深欠損（rows [4,4,4,2,4,4]）で
    K0808 greedy min 23 を改善（m=19 最小石数 ≤ 22）。(6,20,6) は 28石
    （rows [5,3,5,5,5,5]）。いずれも最小性の主張ではない。
  - 検証: SAT witness 全て3系統（sat.js verifyConfig・Python Fraction・純TS/BigInt）。
    較正: K0808 出版 witness（6×19q5・6×15q6）の3系統再検証全PASS。
    実行環境リセット2回を跨いだ def-mode conflicts の bit-exact 再現
    （m=20..27・750/985/657/15,541/17,610/19,169/20,212/89,830）。
  - 成果物: experiments/six-row-q5-q6-frontier-20261120/（README・scripts/run65.sh・
    scripts/{jsverify.cjs,pyverify.py,tsverify.mjs,recorder.py}・
    output/records.jsonl 29レコード）。
