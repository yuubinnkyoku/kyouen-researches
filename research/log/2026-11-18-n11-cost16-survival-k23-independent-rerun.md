# 2026-11-18 N11 31行cost-16 parent 生存曲線 k=23: 並走実行衝突の記録と相互検証、正本復元（independent rerun）

## 経緯（同一時限タスクの並走衝突）

同一の時限タスク（長期レーン）の2実行が、同じ週の同時間帯に互いを知らずに同一の k=23 拡張に着手した。

- **先行レーン**: commit `c0179112`（10:52:34）で k23 script・JSON・JSONL・log の4ファイルを出版。続いて commit `caa7fb00`（10:54:16）で crosscheck script（`cost16_survival_k13_k14_crosscheck_20261118.py`）を k13..k23 に拡張し、k23 JSON の pin（blob `fc60c3660c42e71a92ddf2964d11656b9aa263c9`）を確定済みだった。
- **当レーン**: 同一の k23 計算を独立に完了（下記）したが、main 取得が先行出版と僅差だったため同一pathの出版に気づかず、10:55 に script+JSON+log（commit `32887705`）と JSONL（commit `be0366ac`）を同一pathにpushし、先行レーンの4ファイルを上書きしてしまった。

本logは、(1) 当レーンが完了した独立再計算の記録、(2) 両レーンの値レベル完全一致の交叉検証結果、(3) 正本を先行版に復元した決定とその根拠、を残すものである。

## 当レーンの独立計算（要約）

k22 script（K22_JSON_PIN=`c1e9598b…`・commit `d9d48bd6`）を2段階の機械変換で k23 script に生成し、全計算を実行した。変換後の残存grep（旧IDX・旧ファイル名）で変換漏れを確認してから本番計算に移った。候補roots JSONLは同梱scriptから決定論再生成（6,337行）した。

- **新規確定値**: kill(23) = 2,135,949,407,628,857,856（72.0035%）・kill_A(23) = 1,648,890,715,408,782,870・kill_B(23) = 487,058,692,220,074,986・A_survive = 656,896,575,885,151,518・B_survive = 173,604,358,166,471,982（5.8523%・初の6%割れ）・marginal kill = 45,964,554,161,430,525。
- **構造**: 新pair 22本（shared 5 / disjoint 17）・新triple 231本（b_only 147 / zero 22 / disjoint 62）・新quad 1,540本（b_only 636 / zero 904 / disjoint 0）・全 C(23,5)=33,649 個の 5-subset が構造的ゼロ（I-E quad打ち切り10度目）・triple census C(23,3)=1,771 = b_only 1,120 / zero 388 / disjoint 263。
- **検証**: 27 checks all PASS・finalize二重実行が byte-identical（当レーンJSON sha256 `7133be0d…`）・JSONL 1,797 records（pair 22 + triple 231 + quad 1,540 + cross 4）・cross mismatches 0。

## 交叉検証: 2つの完全独立実行の一致

当レーンの計算と先行レーンの計算は、別sandboxでの2つの完全独立実行である（script生成からfinalizeまで独立）。両者の全出力を比較した結果:

- **JSON**: 数値・構造・checks フィールドは全点完全一致。差異は title 行1行のみ（当レーン: `(6,15)`、先行版: `(6,15) on row 15` の表記差）。
- **JSONL**: 1,797/1,797 record で key set・順序が同一。**値差分 0・memo_states 差分 0**。差異は wall-clock の `sec` field 136件のみ（計算機時間差であり意味のある差ではない）。
- kill・kill_A・kill_B・survive・marginal・全census数が完全一致。

独立実装経路（script生成の変換経路も独立）による2実行が全値で一致したことは、k23 曲線（rank-23 root `(6,15)` の A型3-way項・B型4-way項機構、全 5-subset 構造的ゼロ判定）に対する強い相互検証となる。

## 正本復元の決定

上書きされた先行レーンの4ファイルを**正本として復元**した。理由:

1. 先行出版（10:52 vs 10:55）であり、当レーンの計算は独立再計算に相当する。
2. 先行レーンが拡張した crosscheck script の pin `fc60c3660c42e71a92ddf2964d11656b9aa263c9` は先行版JSONを指す。published verification artifact の pin を書き換えるより、元データ（k23正本4ファイル）を復元する方が低侵襲で、28 checks構成を不変に保てる。
3. 先行版logには crosscheck k13..k23 拡張（network/local両modeで 28 checks, 0 failures）の追記まで含まれており、単一の正本として完全な状態である。

復元した正本のblob sha1（復元時に再確認）:

- script `46374ca45d0753180cf03f556f12f9295cd898e4`（33,751B）
- JSON `fc60c3660c42e71a92ddf2964d11656b9aa263c9`（148,790B・**crosscheck pinと一致**）
- JSONL `8636eb7ea76e1bf622c0c1fde7d9a81e5132d896`（240,723B）
- log `060d962ab60267959c215f5379bd573965102e89`（8,172B）

当レーンの独立再実行の識別子（本logの記録用・正本とは別物）:

- script sha256 `abfcb2af…`（33,576B・git blob `3157c740…`）
- JSON sha256 `7133be0d…`（148,780B・git blob `c6fc7899…`）
- JSONL sha256 `e1d5eb1f…`（240,723B・git blob `64ace97c…`）

## 運用上の教訓

同一時限タスクが毎時運行されて他の実行と並走するため、**push直前の最新HEAD再取得で同一path重複を判定しないと今回の衝突は避けられない**。当レーンはmain取得後に完了まで計算を続け、取得時点には存在しなかった先行出版（取得の僅後に着地）をpush時に握りつぶした。今後は: (a) 計算着手前に同題材の出版有無を確認、(b) push直前にHEADを再取得し同一pathの出版があれば値照合の上、先行版を正本とし後続は**新pathで rerun記録を出版**する（本logがその実例）、(c) crosscheck pin等の published verification artifact は編集しない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。
