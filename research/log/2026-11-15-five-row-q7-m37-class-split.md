# 2026-11-15 five-row q=7 m=37 class-split sweep（高速レーン・単一連続実行で完走・band-closure レーンとの交叉確認）

## 概要

K0850（5×36 完走）の次幅。**5×37 は band-closure レーン
（five-row-q7-band-closure-35-157-20261115・IN FLIGHT）の def-mode UNSAT で
既に決着済み**のため、本レーンは同 README の並走協調ノートに従い
**独立符号化での交叉確認**として class-split 65 deciding instances を完走した。
すべて UNSAT・**両符号化は一致し 5×37 は3幅目の二重決着**
（5×35 K0849・5×36 K0850 に続き）。K0851。単一連続実行（リセットなし）。

## 実施

- 着手前に最新 main で m=37 class-split 未着手を確認（実験dir・log・
  IN FLIGHT claim とも不存在・K0851 番号の空きも確認）。IN FLIGHT claim +
  scripts を先に push（8736dc61）。スクリプトは m=36 レーンから移植
  （sat.js/sat2.js/sat3.js byte-identical・blob sha 6c3262d6 / edfae1d2 /
  6dfa7db3 照合）。mkcnf.sh/qrun.sh は m=36→m=37 に移植
  （minpos ループは 0..17→**0..18 に増加** — floor((37−1)/2)=18・
  旧識別子の残留なしを grep で push 前検証）。CNF 68件（17直接 + 48分解 +
  2 lex + 対照）を生成し、sweep 前に対照 5×18 {0} 343,134 を再現
  （**16度目の cross-lane 対照の較正**・対照 CNF md5
  0bb6187d36e537a170e4fb451359bb94・decode verifyConfig PASS 29石 rows
  5,6,6,6,6）。
- 17 直接クラスすべて UNSAT（batch-1・最難 {0,1} **223,591 conflicts** —
  m36 対応 257,251 より **13.0%減** で m36 の直接最難非漸減〔+1.9%〕は
  一時的と確定・直接合計 **1,480,209** は m36 の 1,535,197 より **3.6%減**）
  + lex=H 交差確認 {0,1}/{2} UNSAT（200,526/98,758）。batch-1 ログ20件
  （対照込み）を即 push（dd717220・fast-forward競合1回は最新main再取得で解消）。
- {0},{1} krow k=0..4 すべて UNSAT（batch-2・最難 {1} k=4: 172,488 — m36
  対応 221,525 より **22.1%減** / {0} k=4: 133,829 — 10.2%減・krow 合計
  **467,058** — m36 の 524,103 より **10.9%減**）。push（3343286f）。
- {0} k=5 × minpos=0..18 すべて UNSAT（batch-3・19点×2クラス・{0}k5p合計
  **1,149,751**・0k5p0 **345,111/10.5s** は m36 対応 298,680 より
  **+15.6% で m37 で唯一の局所的非漸減**・新 minpos=18 点は 5,019）。
  push（9aff2907）。
- {1} k=5 × minpos=0..18 すべて UNSAT（batch-4・{1}k5p合計 **1,632,290**・
  1k5p0 **472,443/18.82s** は m36 対応 492,545 より4.1%減・新 minpos=18 点は
  6,218）・**5×37 完走確定**。push（5c48968f）。
- deciding 65例合計 **4,729,308 conflicts**（= 直接 1,480,209 + krow 467,058 +
  分解 2,782,041・node 独立再計算済み）・INDET 0・SAT 0。lexH込み
  **5,028,592**（=total_conflicts_37）・records 68件総計 **5,371,726**。
  deciding合計系列 m23→37: 20,916,467 → … → 5,423,024 → 5,011,486 →
  **4,729,308**（事前予想 ~4.7M は0.6%誤差で的中）。
- records/summary は mkrecords5737.js で生成。**mkrecords5737.js の訂正**:
  claim 時版の k5p レコードリストから minpos '18' が欠落（sed のアンカー
  不一致・閉じ括弧を閉じ括弧で狙った）していたのを、records 生成前の
  node 独立再計算（66件 vs 期待68件）で発見・修正し、実験dir コミット
  （4756a5a3）で差し替え。CNF・生ログには影響なし（mkcnf.sh の minpos
  ループは最初から 0..18 で68 CNF が正生成済み・qrun も19点ずつ完走）。
  実験dir一式（README COMPLETE・report.md・records.jsonl 68行・summary.json・
  修正済み mkrecords5737.js）を push（4756a5a3）。生ログ68件の remote blob
  sha をローカル git-hash と全件照合（**68/68 OK**）。

## 交叉確認（band-closure レーンとの一致）

- band-closure レーン（genfast3 弦対抽象円 census・def-mode 1インスタンス）
  の m=37 UNSAT と本レーン（sat3 census・class-split 65インスタンス）の
  m=37 全 UNSAT が**独立な符号化で一致**。5×35（K0849）・5×36（K0850）に
  続き**3幅目の二重決着**。
- 同レーンは m=40..49 も def-mode UNSAT 済み（IN FLIGHT・知識統合は同レーン
  で実施予定）。**残る前線 m=38, 39, 50..157 は同レーンの領域であり本レーン
  は着手しない**。class-split レーンは m=37 まで band-closure の決着記録に
  完全に追いついた（次の class-split 交叉確認候補は同レーンの統合状況次第）。

## 境界の更新

- (5,7): {19,…,36},37..158 → **{19,…,37},38..158**（K0851・class-split 系）。
  集合形式 M∈{19,…,37} または ≥38。鋭い形（K0821 監査規約を拡大集合に
  適用）: **M=19 または ≥39**（M=38 は検証済み witness-free 幅 37 の
  witness を要求するため不可）。上界 158（K0332 代入）は不変。

## 備考・レジューム

- class-split レーンの次の交叉確認候補は band-closure レーンが決着済みの
  m=40..49 だが、**同レーンの知識統合（K項目化）が先に行われるべき**で、
  交叉確認の情報価値は帯掃引（m=38, 39, 50..157）の進捗と比較して選定する
  こと。m=38 以降の帯は同レーンの領域（着手禁止）。
- **push時の fast-forward 競合は list_commits で最新 main を明示的に再取得
  してから再pushすれば解消**（batch-1・batch-3 で計2回発生しいずれも解消）。
- **mkrecords 移植時は minpos リストの sed 置換を grep で検証する**
  （今回の '18' 欠落はリスト末尾の閉じ括弧アンカー不一致が原因。
  records 件数の期待値〔65 deciding + 2 lex + 1 対照 = 68〕を push 前
  node 再計算で必ず照合することで検出された）。
- **K項目を push したら必ず workflow トリガー行も push**。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class2・class4は
  いずれもUNKNOWN**。
