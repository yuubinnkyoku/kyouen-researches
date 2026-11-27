# six-row q=6 6x26 class {2} minpos-REST lane（2026-11-28）— 宣言 `e61acf82f` の実行 scaffolding

- 本dirは宣言 `e61acf82f`（class {2} krow=2:4 minpos P∈{0..9,14..22}、
  19 probe）の実行用 byte-clone scripts（sat.js `fcc0cfd8…` / sat2.js
  `14ceb854…` / sat3.js `e04581eb…` / verify_frac.py `837fe24b…`、m26 kit
  出典）を保持する。
- 実行は宣言所有者セッションに譲渡した（ドライバdir README 参照）。
  本dir自体の probe 測定は実行していない。
- 本dirの `output/` は、公開対照（6x25 q=6 class{2} krow=2:4 minpos=11
  SAT 3,574,244 conflicts、出版 K1217 値）の**独立再現ログ**を保持する:
  - `rcalib-6x25-c2k4p11_attempt2-bitexact-3574244.txt`: bit-exact 再生
    （完了決定的探索、exit 10）。機械が並走計算で高負荷のため出版時
    （241s）より遅く、cap を 2400s に拡張して完了させた（completed
    search の conflicts 数は機械非依存）。attempt-1（275s cap、743,684
    conflicts で INDET・開示）は `rcalib-6x25-c2k4p11_attempt1-*.txt`。
  - CNF は byte-clone sat3.js から再生成（meta_c25p11: vars 53,532 /
    clauses 187,536、出版値と bit-exact）。
- verdict 不消費・11x11 UNKNOWN。
