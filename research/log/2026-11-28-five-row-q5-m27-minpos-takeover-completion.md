# 2026-11-28 five-row q5 5x27 minpos sweep takeover 完了 — (5,5) witness 帯 m=5..27・M_{5,5} ∈ [28, 336]

高速レーン (自実行・ユーザーPC到達不可・GitHub API 出版のみ)。

## 成果

- 停滞レーン `research/experiments/five-row-q5-m27-minpos-sweep-20261115/`
  (2026-11-15 IN FLIGHT・実行環境喪失で p1..p3 のみ出版・13日停滞) を
  宣言 `24736c72` (publish-then-execute・単一オーナー・HEAD pin 88a24418) で takeover。
- **(5,5) 前線 5×27 class {0} krow=0:3 minpos=9 は SAT**:
  kissat 4.0.4 **1,556,533 conflicts / 169.09s**・19石 witness rows [3,4,4,4,4]
  (row0 x=[9,19,21]・row1 [11,18,20,22]・row2 [14,17,18,19]・row3 [10,15,16,17]・row4 [7,11,13,14])。
  2系統検証: sat3.js decode → sat.js verifyConfig (census 不使用) ok・
  verify_frac.py (独立 Fraction 実装) safe+maximal ok (max_curve_stones=4・unblocked=[])。
  cold pair 再実行: conflicts bit-exact・v-line 同一 (raw md5 差は timing 行のみ・開示)。
- **witness 帯 m=5..27・M_{5,5} ∈ [28, 336]** (着手前 [27, 336]・上界 K0318 U=336 不変)。
  **前線は 5×28 へ。** mwq_stabilization.csv (5,5) 行 27..336 → 28..336 更新・K0833 更新。
- 5 ファミリー ((4,4)(4,5)(5,5)(5,6)(5,7)) で揃っていた witness jump (≥3石移動)
  の構造観察に対し、5×26 witness との幾何比較は今回の witness が minpos=9
  (row0 最左 x=9) であることから次の調査課題 (seed からの石距離未測定・主張なし)。

## 掃引記録 (全て宣言後実行)

- 較正 (宣言前実施・宣言で開示): CNF md5 5件 bit-exact・5×25 c0 SAT 35,972 conflicts
  (出版値 bit-exact)・5×26 c0 SAT 1,631,556 conflicts / 204.22s (出版値 bit-exact)。
- p4..p8: cap 285s INDET (2,290,237 / 2,255,250 / 2,526,618 / 2,423,463 / 2,525,494
  conflicts・honest negatives・不在主張ではない)。旧レーン手記値 p4/p5 は本再実行で置き換え。
- p1..p3: 旧レーン出版値のまま (再実行せず)。
- **p10..p13 は未掃引 (WIN-stop)**・k=0..2・他の正準欠損クラスも残る
  (5×27 全体の不在主張ではない)。
- cap は停滞レーン計画の 400s から 285s に変更 (実行環境の呼び出し上限・宣言で開示)。

## 出版鎖 (全て main 直接・fetch-back byte 一致)

- 宣言 `24736c72` (publish-then-execute・HEAD pin 88a24418・宣言前較正は全て宣言内で開示)。
- kit part 1 `6104a00f` (README COMPLETED・records.jsonl 増分・witness 2件)。
- kit part 2 `c699191f` (raw logs p4..p8)。
- kit part 3 `78b139b5` (raw logs p9・p9.p2・較正 5×25/5×26)。
- csv+K `ea25c21a` (mwq_stabilization.csv (5,5) 行 28..336・K0833 title+追記+artifact)。
- fetch-back: csv blob sha 0431253455fbed154dfdcd6c096f9e3a55bef2db・
  K0833 blob sha 4ffe639d542d5bc05afd4352409594905f0ecdde ともにローカルと byte 一致。
  raw logs は API listing size がローカル byte 数と完全一致
  (368,277 / 368,285 / 265,367 / 344,011 / p4..p8 各 75,106..77,348)。
- 開示: kit part 3 の push 後に実行 block が memory limit (16 MiB) に到達したが
  push 自体は完了しており commit 78b139b5 として着地 (API listing で検証)。
  p4..p9 の INDET 実行の rc は kissat --time 到達時 0 + `s UNKNOWN` 行
  (旧レーン記録の rc=124 は SIGTERM 時の shell 値・意味は同じ cap 到達)。

## 次の一手

- (5,5) 前線 5×28 (class-split krow/minpos 分解・重い cap か別分解が必要な場合は宣言を新規に)。
- (5,6) 前線 5×23 (five-row-q6-m23-longcap-20261115 は 2026-11-15 から IN FLIGHT 停滞・takeover 候補)。
- p10..p13・k=0..2・残りクラスの掃引 (不在確定には 19 正準類の完全掃引が必要)。

標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
