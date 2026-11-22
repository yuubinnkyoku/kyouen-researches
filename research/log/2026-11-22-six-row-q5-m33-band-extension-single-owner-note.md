# 2026-11-22 six-row (6,5) 6x33 band extension (unblocked<=3 bases; bounded-edit + targeted 2R2A/3R2A classes) — single-owner declaration note

- 日時: 2026-11-22T03:10Z付近・宣言時HEAD `97d6dc80edf756ef0d5e0fc7046af32a81d33bb7`
- オーナー: 高速レーン（本セッション・単一オーナー）。
- 前段: 同レーン K1216（6x31 band extension・2026-11-22 01:02Z 宣言 `bc11e28b`）の
  resumeノートが指定する次期課題 (b)「6x33: unblocked_w33.json で c009@off4 等が
  targets 2・config_w33 構築から着手可」。
- 並走との境界: 現行 t2 resume scan（宣言 `b1afb181aa`・02:16Z・6x32 t2 bases 1..23）は
  自宣言で 6x33 を明示的にスコープ外に置いており非接触。本レーンは w32-u3-scan
  出力木には一切書き込まない（tag 分離: w33-u3-scan / w33-scan-cal）。

## 宣言スコープ（claim）

1. **6x33 base 構成**: `_q65-band-m31plus-kit` の unblocked_w33.json（180配置の
   unblocked census・先行セッション作成）のうち unblocked ≤ 3 の 13 base
   （u=2: c009@off3/4/5、u=3: c008@off0..3・c009@off2/6・c011@off4..7）を
   `config_w33_u3.json`（tag w33-u3-scan）として構成する。
2. **編集クラス掃引（base ごと）**:
   - r0s（1..4R0A・complete）・r1a1/r2a1/r3a1/r4a1（kR1A・complete）:
     既刊 w32 battery（`output/w32-bounded-edit-negatives.json` の
     「k<=4R<=1A + 3R2A」近傍）と同一機材・同一意味論。
   - s2（**2R2A targeted-complete・新規**）: D-set 必要条件ペアフィルタ
     （t2 と同一の必要条件論で k に非依存）× C(23,2) 全除去、全候補完全検証。
     K1209/K1211 で witness 量産を行った肥沃級 rem2add2 の本 base への拡張。
     既刊 w32 近傍のスコープ外級であり、陰性でも w32 側とは独立の新規データ点。
   - t2（3R2A targeted-complete）: 既刊と同一。
3. **witness が見つかった場合のみ**: 3系統独立検証
   （surgery_gen.js 整数正準曲線鍵・det_q_verify.py 行列式・append_criterion.py Fraction 出版pin `d08d8fb1…`）
   + tamper/陽性対照を添え、下界更新 **M_{6,5} ∈ [34, 658]** として出版する
   （下界のみの主張・6x33 以降の存在不在は主張しない）。
4. **全 base 陰性の場合**: 6x33 は UNDETERMINED 不変。「13 base の
   bounded-edit 近傍（k≤4R≤1A complete + 2R2A/3R2A targeted-complete）に
   6x33 witness なし」の限定陰性を誠実に出版する（6x33 全配置の不在主張ではない）。

## 受入条件（fail-closed）

- **機材較正ゲート（実行済み・PASS）**: engine core verbatim（scripts/surgery_deep.js
  sha256 `851e5b7b…`）が w32 published anchors を再現:
  c009@off3 unblocked=[[31,5]] 一致、rem1..4add0 候補数 23/253/1771/8855・witness 0 一致、
  D-set pair filter dsizes=[74]・pairs=9731（K1216 出版 t2 アンカーと一致）、
  cal base の s2（2R2A）も 0 witness。
- 各 base: engine 再計算 unblocked が census（Fraction append_criterion 機材）の
  targets と一致すること。不一致なら当該 base は abort・記録。
- 決定性: 完了した s2/t2 base のうち ≥1 で time-budget 境界を跨ぐ resume 再開が
  機能したことを確認、かつ代表 base で再実行の主要数値一致。
- witness の場合は K1216 と同一の 3系統ゲートを全 PASS させてから出版。
- push 前に必ず最新 main を再取得し、fetch-back byte 照合。競合・取得失敗時は
  無理に押さず簡潔に記録して次回へ回す。
- census/pairs/candidates 数を勝敗として読まない。

## 非目標（着他レーンとの境界）

- **6x32 t2 bases 1..23**（宣言 `b1afb181aa`・並走lane所有）。`output/w32-u3-scan/` 非接触。
- (6,6) m26 probe（`05785cdfa5`）、seven/eight-row families（`66e7033b6e`）、
  (6,7) 6x22 rowfixed（`24a98f89d3`）、n11 系全般: 非接触。
- 標準 11x11 空盤・二石root・S2・class 1/2/4: 本レーン非接触で UNKNOWN のまま。
- 4R2A・5RmA などより深い編集クラスは本宣言スコープ外（将来課題として記録する場合あり）。
- 6x33 の SAT/全配置掃引は行わない（OOMレーン・長期レーン管轄）。

## 判定規約

- s2/t2 の targeted-complete の意味は surgery_deep.js docstring と同一の D-set
  必要条件論（k 非依存）: unblocked target u の covering curve は kept ≤ 3 ゆえ
  add を必要とし、covering add は D(u)（u 自身を含む）に属する。フィルタを満たさない
  ペアは witness になり得ないゆえ、列挙は当該クラスについて完全で、陰性の意味は
  「この base の当該クラスに witness は存在しない」。
