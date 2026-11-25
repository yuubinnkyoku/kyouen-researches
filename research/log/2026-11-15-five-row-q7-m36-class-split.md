# 2026-11-15 five-row q=7 m=36 class-split sweep（高速レーン・単一連続実行で完走・band-closure レーンとの交叉確認）

## 概要

K0849（5×35 完走）の次幅。**5×36 は band-closure レーン
（five-row-q7-band-closure-35-157-20261115・IN FLIGHT）の def-mode UNSAT で
既に決着済み**のため、本レーンは同 README の並走協調ノートに従い
**独立符号化での交叉確認**として class-split 63 deciding instances を完走した。
すべて UNSAT・**両符号化は一致し 5×36 は二重決着**（5×35 に続き2幅目）。
K0850。単一連続実行（リセットなし）。

## 実施

- 着手前に最新 main で m=36 class-split 未着手を確認（実験dir・log・
  IN FLIGHT claim とも不存在）。IN FLIGHT claim + scripts を先に push
  （b32dffa1）。スクリプトは m=35 レーンから移植（sat.js/sat2.js/sat3.js
  byte-identical・blob sha 6c3262d6 / edfae1d2 / 6dfa7db3 照合）。
  mkcnf.sh/qrun.sh/mkrecords5735→5736 は m=35→m=36 に移植
  （minpos ループは 0..17 据え置き — floor((36−1)/2)=17・旧識別子の
  残留なしを grep で push 前検証）。CNF 66件（17直接 + 46分解 + 2 lex +
  対照）を生成し、sweep 前に対照 5×18 {0} 343,134 を再現（**15度目の
  cross-lane 対照の較正**・対照 CNF md5 0bb6187d36e537a170e4fb451359bb94）。
- 17 直接クラスすべて UNSAT（batch-1・最難 {0,1} **257,251 conflicts** —
  m35 対応 252,381 より **+1.9%** と m36 で唯一の局所的非漸減・直接合計
  **1,535,197** は m35 の 1,636,361 より **6.2%減**・直接合計系列は
  5,256,816 → … → 1,743,108 → 1,636,361 → 1,535,197）+ lex=H 交差確認
  {0,1}/{2} UNSAT（196,313/97,192）。batch-1 ログ20件（対照込み）を即 push
  （b93a7336）。
- 陽性対照 5×18 {0} SAT 343,134 が **K0821..K0849 14レーン対照と bit-exact
  （15度目の cross-lane 再現）**・verifyConfig PASS（29石 rows 5,6,6,6,6）。
- {0},{1} krow k=0..4 すべて UNSAT（batch-2・最難 {1} k=4: 221,525 — m35
  対応 352,023 より **37.1%減** / {0} k=4: 149,006 — m35 対応 207,921 より
  **28.3%減**・krow 合計 **524,103** — m35 の 729,321 より **28.1%減** で
  m35 の krow 合計系列初の非漸減（+0.4%）は一時的と確定）。
  push（4d1fb868）。
- {0} k=5 × minpos=0..17 すべて UNSAT（batch-3・18点×2クラス・m=36 でも
  minpos の健全上限は floor((36−1)/2)=**17 のまま**（columns 0..35 で
  min(x_min, 35−x_max) ≤ 17）。{0}k5p 合計 **1,177,015** — m35 の
  1,246,094 より5.5%減・最難 0k5p0 **298,680/10.69s** — m35 対応
  338,617 より **11.8%減**）。push（bd2d9c3d）。
- {1} k=5 × minpos=0..17 すべて UNSAT（batch-4・{1}k5p 合計 **1,775,171**
  — m35 の 1,811,248 より2.0%減・最難 1k5p0 **492,545/18.36s** — m35
  対応 496,388 より **0.8%減**）。push（544f5381）で全63 deciding CNF の
  UNSAT が確定し **5×36 witness-free CONFIRMED（class-split）**。
- deciding 63 例合計 **5,011,486 conflicts**（17直接 1,535,197 + 10 krow
  524,103 + 36分解 2,952,186）・INDET 0・SAT 0。lexH込み **5,304,991**
  （=total_conflicts_36）・records 66件総計 5,648,125。
- 難度: deciding 合計 m23→m36 で 20,916,467 → … → 5,928,015 →
  5,423,024 → **5,011,486**（事前予想 ~5.1M は0.2%誤差で的中）。m36 の
  局所的非漸減は direct-hardest {0,1} +1.9% のみで、m35 の krow 系
  非漸減（{1}k4・{0}k4・krow合計）はすべて強い漸減に解消。
- 生ログ66件は batch ごとに push し、**remote blob sha をローカル sha1 と
  全件照合（66/66 OK）**。
- records/summary は mkrecords5736.js で生成（m36 用に claim・
  total_conflicts_36・対照15度目・交叉確認記述を更新・push 前に node で
  records.jsonl を独立再計算し集計を検証: 直接 1,535,197 + krow 524,103 +
  k5p 2,952,186 = deciding 5,011,486）。実験dir一式（README COMPLETE・
  report.md・records・summary）を push（fe66ed5b）。

## 交叉確認（band-closure レーンとの一致）

- band-closure レーン（genfast3 弦対抽象円 census・def-mode 1インスタンス）
  の m=36 UNSAT と本レーン（sat3 census・class-split 63インスタンス）の
  m=36 全 UNSAT が**独立な符号化で一致**。5×35（K0849 + def-mode）に続き
  2幅目の二重決着。
- 同レーンは m=37 と m=40..49 も def-mode UNSAT 済み（IN FLIGHT・知識統合
  は同レーンで実施予定）。**残る前線 m=38, 39, 50..157 は同レーンの領域
  であり本レーンは着手しない**。

## 境界の更新

- (5,7): {19,…,35},36..158 → **{19,…,36},37..158**（K0850・class-split 系）。
  集合形式 M∈{19,…,36} または ≥37。鋭い形（K0821 監査規約を拡大集合に
  適用）: **M=19 または ≥38**（M=37 は検証済み witness-free 幅 36 の
  witness を要求するため不可）。上界 158（K0332 代入）は不変。
  witness 探索の前線（class-split 系）は 5×37（ただし band-closure レーン
  の def-mode 記録では m=37 は既に witness-free・同レーンの統合待ち）。

## 備考・レジューム

- 次回の class-split 候補は **5×37 の交叉確認**（着手前に最新 main で
  m37 実験dir・band-closure レーンの統合状況を確認のこと・m=37 では
  minpos の健全上限は floor((37−1)/2)=**18 に増加**・19点×2クラス・
  CNF 総数は 17直接 + 2 lex + 10 krow + 38分解 = 68（対照込み69）・
  mkrecords5736→5737・claim/total_conflicts_36→37・対照16度目・
  deciding 見込み ~4.7M conflicts・sed は `5 36 7→5 37 7`・
  `c5x36q7→c5x37q7`・`r5x36q7→r5x37q7`(/g必須)・minposループ 0..17→**0..18**・
  cdパス `/home/user/kr37/w5x37`）。ただし band-closure レーンが帯掃引を
  進めているため、**交叉確認の情報価値と帯掃引の進捗を比較して次の作業を
  選ぶこと**（m=38 以降の帯は同レーンの領域）。
- **push時の fast-forward 競合は list_commits で最新 main を明示的に再取得
  してから再pushすれば解消**。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class2・class4は
  いずれもUNKNOWN**。
