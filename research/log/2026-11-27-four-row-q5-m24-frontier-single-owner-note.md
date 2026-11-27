# 2026-11-27 (4,5) 前線 4×24 class-split 掃引: 単一オーナー宣言 (高速レーン)

- 前線の位置づけ: witness 帯 m=5..20 (K0833)・witness-free {21,22,23}
  (K0857 / K1197 / four-row-q5-m23-class-split-20261121 完了 2026-11-23・全 111
  record UNSAT・coverage audit 済み)。よって **M_{4,5} = 21 または ≥ 25**
  (K0821-audit 規約)。上界 U_{4,5} = 140 (K0318)。
- 本レーンは **(4,24,5) class-split 掃引** (m23 レーンと同一構造の
  9 正準クラス・k∈{0..3}×minpos p∈0..11 sound H-split・k-aware x2 第2石分割・
  piece cap 220s)を単一オーナーで実行する。実験キット:
  [four-row-q5-m24-class-split-20261127](../experiments/four-row-q5-m24-class-split-20261127/)。
- 判定: 全 piece UNSAT なら witness-free 幅集合 {21,22,23,24}・K0821 監査規約により
  **M_{4,5} = 21 または ≥ 26**。SAT なら witness 帯は m=5..24 に拡大し
  **M_{4,5} ∈ [25, 140]**・witness を復号・3 系統検証の上出版する。
- 較正 (本 host・宣言時): 陽性対照 (4,20,5) c0k3p1 CNF md5 `362034b2…`
  byte-exact 再生・kissat **SAT 375,415 conflicts bit-exact** (m21/m22/m23
  交差較正値と同一)。sat.js/sat2.js/sat3.js/sat4.js/verify_witness.py は
  m23 kit 出版 byte (md5 0cc6021a/282ae832/d03f908e/df472efc/0530d16)。
  kissat 4.0.4 md5 `3a5eba83…` 出版 pin 一致。
- records は append-only・増分 push・resumable。INDET は honest negative
  (不在主張ではない)。
- verdict 不消費・11×11 は全時点 UNKNOWN。
