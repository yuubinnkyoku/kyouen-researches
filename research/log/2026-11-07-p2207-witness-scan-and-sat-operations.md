# 2026-11-07 p=2207 の等号証人探索（d 走査）の状態と SAT 求解の運用知見

- 対象: `Q_p` の等号 `A(p)=(p+3)/2`（K0097/K0101）の残る未発見素数 **2207**。
  2003..2477 のうち証人が得られていないのは 2207 のみ（他 63 素数は保存・独立検証済み）。
- 方法: `clauses_for_pair(p, edges, d)` の signed NAE3/4＋原点節 CNF を、d を h=(p-1)/2 から降順に解く。
  `d` ごとに独立な CNF なので、試行済みの d をログから読み飛ばして再開できる（`scan_deep_d.py`）。

## 走査状態

- 既定設定の cadical（WSL）で **d = h..h-120（= 1103..982）を全数**: 120 UNSAT・1 タイムアウト（初期走査）。
- `scan_deep_d.py` で **d = 461..335 を含む d = 1103..335 を走査**: 本記録時点で全件 UNSAT
  （総計 768 個の d が UNSAT、SAT 未発見）。残りは d <= 334。
- すべての UNSAT は「その d では充足解なし」のソルバ主張であり、DRAT 証明の保存はしていない。
  全 d が UNSAT になれば等号不成立の候補になるが、本記録時点では未確定である。

## SAT 求解の運用知見（この repo の他の SAT 作業にも効く）

1. **既定設定で詰まる UNSAT 寄り/難問には SAT 向け設定が効く**: p=2351, d=h の CNF は
   既定設定で 240 秒タイムアウトしたが、`cadical --quiet --sat -L1000 -t 30` が **4.6 秒**で SAT 解を返した
   （`-L` は初期局所探索回数、`--sat` は SAT 向け内部設定）。既定→タイムアウト時に SAT 向けで再試行する
   二段構えを `probe_driver.py` に実装済み。
2. **WSL 経由の cadical 呼び出しはまれにセッションごと停止する**（数百分の一程度）。
   呼び出しごとに `-t`（cadical 自身の壁時計制限）を渡し、外側にもタイムアウトを置き、
   停止したらプロセスを落として再開する運用が現実的。生成器と cadical の出力はファイルへ逃がす
   （ジョブ実行環境では pipe を残さない。
3. **pysat の CaDiCaL ラッパは `interrupt()` 非対応**（`NotImplementedError: Limited solve is currently
   unsupported by CaDiCaL.`）。時間制限には使えず、代わりに `conf_budget(N)`＋`solve_limited()` が使える
   （True=SAT/False=UNSAT/None=予算超過）。ただし `bootstrap_with` と Python 側の制約構築が GIL で
   直列化するため、WSL の cadical 実行より遅い（同 CNF で 1 件 2-3 秒 vs 5-9 秒）。
   `Minisat22`/`Glucose4` は `interrupt()` 対応だが、この CNF 族では cadical より遅い。
4. **10×10 の 20 石 SAT**（K0141）も並行に試した: `forbidden_n10.cpp` で 54,441 個の禁止四点を 0.4 秒で再生成し
   （K0057 の記録と一致）、`sat_n10.py`（100 変数・57,581 節・at-least 20 seqcounter）を Cadical195 の
   200 万衝突予算で解いたが **UNKNOWN（228 秒）**。証人なし。非存在の証拠ではない。

## 次

- 2207 の d <= 334 の走査を完走する（SAT なら証人保存・独立検証、全滅なら等号不成立の候補として
  DRAT 証明つきの再確認が必要）。
- `d=h` 例外（h-1 が主、1861 は h-66）の特徴づけ。
