# 2026-11-28 (5,4) 5x47 前線 SAT 攻撃 — 単一オーナー宣言 (publish-then-execute)

- Task: `(5,4)` 固定幅族の前線 **5x47 witness 存在判定**。
  現状 `M_{5,4} ∈ [47, 567]` (下界は five-row-q4-band-45-46-surgery-20261121 の
  m=45/46 witness によるもの。上界 T_5=567 は K0068)。m=47 は同実験の
  surgery budget 2/3 scoped negative のみで **UNDETERMINED**・SAT 未攻撃。
  SAT なら witness 帯 m=5..47・`M_{5,4} ∈ [48, 567]`。piecewise UNSAT は
  honest negative として記録し、完全被覆が揃うまで不在主張はしない。
- Method:
  - 生成器: `sat3.js` streaming rowfixed 版 (six-row-q4-m47-rowY0-oom-20261115
    kit 出版 byte・sha256 `aa9a0f38…`) + core `sat.js` (sha256 `fcc0cfd8…`)。
    q=4 ≤ w=5 の all-triples census を streaming で通す (sat2 直系は 5x39 でも
    heap OOM)。CNF 生成は決定的。
  - ソルバ: kissat 4.0.4 static linux-amd64 (sha256 pin `21da5d98…`・
    `_m26c1` 出版 pin と同一バイナリ)。
  - 分解: rowfixed `--rowY=Y`。V (行 0↔4・1↔3・2 固定) により single-deficiency
    の rowY クラスは {0,1,2} の3類で全 single-deficiency を被覆。
    まず rowY=1 (m=45/46 witness species はすべて rows [3,2,3,3,3] 型・
    欠損行 = row 1)。次いで rowY=0/2。抵抗時は class/krow/minpos 追分解を
    amendment で宣言後に追加する。
  - lex について: m=40 rowY=1 の先行記録と同じ `--lex=H,V,HV` をまず使う
    (SAT 側には常に sound)。UNSAT/INDET を absence 証拠に使う場合は
    V/HV が rowY ピンを保存しない点を考慮し、lex 無しまたは lex=H の
    sound 符号化で再実行する。
- Calibration (宣言前 scratch・開示): 同一 generator/solver で
  **5x39 rowY=1 lex=H,V,HV は SAT・conflicts 21,147 = 出版値 (197.1s) と
  bit-exact** (本環境 212s・host 差のみ)。CNF md5 `150e4a17…`・生成決定性確認。
  また 5x39 rowY=1 lex 無しも SAT 13,787 conflicts (対照)。
- Pre-declaration 事実確認: 最新 main HEAD `b841063a` (2026-11-28T08:13Z 再取得)。
  (5,4) m=47 は現時点で未着手・宣言なし (five-row-q4 系の最後の commit は
  2026-11-21/22)。n11 系・AG/PG q=7 double-blocking 系・(8,9) 8x29 系は
  他レーン宣言済みで非衝突。
- Execution plan (この宣言の出版後):
  1. 5x47 rowY=1 lex=H,V,HV (cap 600s) → SAT なら decode + verifyConfig +
     独立 Python Fraction verifier の二重検証 (陽性・陰性 tamper 対照)。
  2. INDET なら rowY=1 lex 無し / lex=H、rowY=0/2、cap 段階引き上げ、
     必要なら class/krow/minpos 追分解 (amendment 出版後に実行)。
  3. 結果は experiment kit (`research/experiments/five-row-q4-m47-frontier-sat-20261128/`)
     + 完了 log + (SAT の場合) csv (5,4) 行更新で出版。records は
     append-only jsonl・再実行時は既存 key を再実行しない。
- 注意: verdict 不消費。標準 11x11 空盤・19 central-reply roots・二石 root
  {60,27}・第三手 {100,108}・全 closure class は全時点 UNKNOWN。
