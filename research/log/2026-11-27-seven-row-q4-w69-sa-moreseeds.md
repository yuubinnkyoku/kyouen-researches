# 七行 q=4 幅69 seeded SA 追加seed負記録 (2026-11-27)

幅69 two-edit 掃引キットの SA 負記録（w68 witness seed）の追試として、
異なる seed family（w65 チェーン witness の D4/並進像のうち欠損行被覆
最大の2つ・ともに幅67被覆）で published `search_seeded.js`
（byte-clone・sha256 `c4b5e904...`・改変なし）を 7×69 で 230 秒×2 走:

- seed 11 / seed 13 とも best **21 石**・improve event 0・rejects 0。
- curve census 1,161,122 は 2 走とも出版値と完全一致（エンジン pin）。
- いずれの seed family も maximalize 後ちょうど 21 石で安定し、
  20 石への降下なし。ヒューリスティック負記録のみ・7×69 witness の
  不在主張ではない。M_{7,4} ∈ [69, 1929] 不変。

kit: `research/experiments/seven-row-q4-w69-sa-moreseeds-20261127/`
（README・stdout 2走・seed 2件）。

次の実行可能課題: 3-for-3 近傍（重い・長期レーン候補）・SAT/kissat に
よる 7×69 直接評価（six-row レーンの class-split 手法の移植）・
frontier breadth 拡大。

**標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手
{100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。**
