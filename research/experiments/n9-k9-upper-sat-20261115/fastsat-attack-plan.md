# ge19 (K_9 上界) fastsat 攻撃計画 — 2026-11-15

本実験フォルダの at-least-19 CNF (1,449 vars / 34,525 節, FNV e7dfa0c0c01cbf81) を
sat-fastcdcl-20261114 の fastsat.js (DIMACS入出力) で直接攻撃する計画。
2026-11-15 第3実行は sandbox 予算枯渇と bash 停止で実行に至らず、接続と判定規約を記録して次回に回す。

## 実行手順 (bash 復旧時)

1. gen_n9_cnf.mjs で ge19 DIMACS を生成 (FNV 照合) し、fastsat.js に入力:
   node scripts/gen_n9_cnf.mjs && node ../../sat-fastcdcl-20261114/scripts/fastsat.js <dimacs> --ncells 81 --cellphase=0 --cellboost
2. 設定: fastsat 報告書の難度非単調性の教訓より、vdecay=0.95/base=512 と
   vdecay=0.995/base=8192 の2設定 + seed 2-3本の portfolio を推奨。

## 判定規約 (K0029 の trust 境界と同じ)

- UNSAT: K_9 <= 18 の repo 内証明候補。fastsat は DRAT proof を出力するので
  チェッカ検証が理想。kissat (bash) 追試を主証明とし fastsat+DRAT を併記。
- SAT: model から19石 witness を復号し、censusA (F_9=29,152) の全禁止四点組検証 +
  3x3 行列式の独立検証で確認できたら K_9 >= 19・先行上界の反証として新K項目。
- INDET/TIMEOUT: 抵抗の記録のみ。上界主張は一切しない。

## 第3実行メモ (自作コンパクトCDCL整備)

watched literals + 1UIP + 線形EVSIDS のコンパクトCDCLを別系統で整備し、
乱数3-SAT 14題 vs 全列挙 (nv=16, m=72) 14/14 一致、PHP(6,5)/(7,6)/(8,7) すべて正しく UNSAT
(809/3,062/9,980 conflicts) で中核動作を検証。ただし fastsat が既存のため
本計画では第三実装 (cross-check 用) のみとし、主攻撃は fastsat に一本化 (重複回避)。
整備中に捕捉したバグクラス (将来のNode CDCL保守用メモ):
(a) unit/長さ1節をDBに入れたまま watch に付けると lit(ci,1) が次節のリテラルを読む
(fastsat 報告書 (b) と同根)、(b) propagate の衝突分岐で衝突節を watch リストから
除去すると再衝突時に BCP が盲になり偽SAT、(c) 1UIP 学習節には節リテラルをそのまま
push すべき所、否定を push すると恒真化学習節で偽UNSAT、(d) heap 枯渇後の pick は
線形フォールバック必須 (backtrack で未割当に戻った変数が heap から失われる)。
