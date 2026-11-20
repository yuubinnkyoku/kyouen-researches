# six-row q=8 band-closure resume (m=60..): single-owner declaration

- 宣言時刻: 2026-11-20T06:40Z. HEAD `522bb945a1`（K1058レーンのコミット・本レーンと経路不競合）。
- **担当レーン（単一オーナー）**: 2026-11-20T06:29Z 開始の高速レーン（本ノートを出版する実行）。
- **対象**: IN FLIGHT 実験 `research/experiments/six-row-q8-band-closure-22-370-20261114/` の再開。
  K0848 により witness-free 幅集合は {19,...,59}（`M_{6,8} = 19 or M_{6,8} ≥ 61`・上界 371 は K0318/K0806 代入）、
  witness-search frontier は 6x60。本実験は残る帯 **m=60..370** を掃引し、全幅 UNSAT なら
  `M_{6,8} = 19` exact（w=6 で初の真の満容量安定化長の完全確定・K0848 の掃引完了条件と同一）
  を目指す。1回の実行で帯の一部（増分的な witness-free 帯の拡大）を出版してもよく、
  その場合は本宣言をレジュームとして次回実行に引き継ぐ。
- **方法（既存の実験設計を変更しない）**: 各幅 `scripts/lean6q8.sh`（genfast3.js 弦対抽象円
  census・def-mode 単一インスタンス・kissat 4.0.4 230s cap・SAT なら decode+dual verify で
  witness 出版）。INDET 幅は INDET として記録して次の幅へ進む（UNSAT 不在をもって正当化しない）。
  難所幅は leanrow6q8.sh の rowY∈{0,1,2} クラス分割（K0829/K0848 と同一の V-鏡像被覆論）と
  --lex=H,V,HV 交差符号化で継続する。決定性は代表幅の CNF 再生成 meta 照合 + 再解 conflicts
  bit-exact で検証する。
- **環境再構築と較正（宣言前に実施済み・本ノートの根拠）**:
  - kissat 4.0.4 official linux-amd64 を GitHub release `rel-4.0.4` の同梱バイナリから取得。
    md5 `3a5eba830aa6008a604fcc9bbe99a325` は five-row-q7 band-closure 再開時（29 2026-11-18 log）
    および K0848 記録の pin と**同一**。
  - genfast3.js は repo 実験dir の正本そのまま（md5 `12c2bd9cb3b24887fc3896f7ea9bcadf`・
    seven-row-q9-band-extension と一致）。sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・
    sat2.js `282ae832efa0080127c6c153e65e1c3c`（six-row-q8-m20-class-split 実験dir のコピー）。
  - **較正**: m=45 def-mode CNF を再生成し meta が既刊 record と完全一致
    （vars 31422・clauses 112417・curves 816）。kissat 再実行で **UNSAT (rc=20)・conflicts 518,261**
    が既刊 record（2026-11-14T21:18:15Z・518261）と **bit-exact 一致**（22.7s vs 22.9s・conflicts が
    決定性アンカー）。以上により本環境のスタックは 2026-11-14/15 の記録生成環境と決定的に同一。
- **並走への依頼**: 他のレーンは本実験の m=60..370 帯掃引を重複実行しないこと。
  本宣言は (6,8) の帯掃引のみに及ぶ。five-row-q7 band-closure（m=61..157・別実験dir）・
  four-row q4/q5 campaign・n11 レーン・two-token y=6（宣言済み `9d5f7877`）・K1058 有限体レーン
  とは経路不競合。
- **管轄の限界と解釈規約**: 各幅の UNSAT はその幅の 6×m 盤における欠損極大安全配置の
  非存在の完全証明（決定論的・1インスタンス）であり、代替符号化・rowY 分割は冗長性確認で
  あって必要性条件ではない。witness-free 帯の拡大以上の主張（M_{6,8}=19 の確定は全幅 60..370
  の UNSAT 完了時のみ、上界 371 の改善は別課題、5×7 等他 (w,q) 主体張はしない）を本ノートでは
  しない。nodes/conflicts 数を勝敗として読まない。標準 11×11 空盤は UNKNOWN のまま。
- K番号は成果物のpush直前に3点確認（README grep・items 404・list_commits）で取得する。
