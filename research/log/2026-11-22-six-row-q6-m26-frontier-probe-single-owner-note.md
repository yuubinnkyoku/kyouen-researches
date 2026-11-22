# 単一オーナー宣言: six-row (6,6) m=26 frontier probe・第1 datapoint（2026-11-22 高速レーン）

- 宣言時刻: 2026-11-22T01:55:27Z
- 宣言時 main HEAD: `a37a4825`（K1217 bullet append 直後）
- 対象: 6×26 q=6 の class{2} krow=2:4+minpos=11 分解単一インスタンスの初回走査のみ。
- 実験 dir: `research/experiments/six-row-q6-m26-frontier-probe-20261122/`
- 機材: K1215/K1217 出版正本機材（sat3.js 出版pin・kissat 4.0.4 官 sha256 `21da5d984e38…` 照合済み）。

## スコープ（fail-closed）

1. 6×25 を解いたのと同一 H-split（class{2} krow=2:4+minpos=11）を m=26 で cap 260s で走査する。
   結果は INDET/UNSAT/SAT いずれでも records 行として publish する。
2. INDET は cap 到達 honest negative（不在主張しない）。UNSAT はこの分解部分インスタンスの有限不在証明
   （class{2} 全体や 6×26 全体の不在ではない）。いずれも M_{6,6} の値は不変のまま。
3. SAT の場合は K1217 と同一の受入条件（decode 2系統検証・tamper・census ゲート・決定性 rerun・
   D4+並進非合同・K item 番号は search_code で空き確認のうえ採番）を満たした場合のみ下界更新として
   publish する。検証落ちの場合は候補記録のみで終了する。
4. conflicts 数を勝敗として読まない。標準 11×11 空盤・二石 root・S2・class 1/2/4 は非接触で
   UNKNOWN のまま。6×25 以前・6×27 以降には手を出さない。
5. 並走へ: 本宣言後 45 分以上 publish がない場合は bc11e28b/K1217 前例に従い adopt 可能。
