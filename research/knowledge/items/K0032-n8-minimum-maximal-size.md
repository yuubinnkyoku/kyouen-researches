---
id: K0032
title: 8×8の最小極大安全サイズs_8=8
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-BF
- B091
relations:
- type: depends_on
  target: K0026
  note: ''
artifacts:
- path: research/experiments/original-claims/output/round70_scope_catalogue_check.json
  role: data
  note: 全408八石極大の安全性・極大性と原文B371–B375/B378の再検算
- path: research/experiments/original-claims/scripts/round70_scope_catalogue_check.py
  role: verifier
  note: 完全カタログから正しいD4・三点方向・削除後合法点数を再計算
- path: research/experiments/original-claims/reports/round70-b301-b400-original-scope-audit.md
  role: source
  note: 旧有限族の分類をs8の根拠とともに保持
- path: research/experiments/original-claims/reports/round46-small-saturation-and-window-reduction.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round46_sat_atmost8.json
  role: data
  note: SAT証人の独立検査と有限範囲
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/data/s8_exact.json
  role: data
  note: 7石完全排除記録
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 8×8の最小極大安全サイズs_8=8

k≤4は三点補完上界、k=5,6,7は各完全探索で排除。安全8石極大の存在と合わせs_8=8。全408安全8石極大が列挙済み。

打切り不発見を非存在証明にせず、完了フラグと幾何の独立検算を根拠とする。9×9の窓還元にもこの完全カタログを用いる。

この完全有限族の特徴をRound70で再検算した。全408が三点共線を持つ（B371）。一方向だけの配置は24個なので異なる二方向必須は偽（B372）。一辺だけ接触する配置は72個なので二辺必須も偽（B373）。角なしは312個（B374）で、既知Wと異なる名前付きD4点軌道占有ベクトルを持つ例がある（B375）。一石削除で元の空点が新しく合法になる最小個数は2で、ちょうど1となる例は存在しない（B378）。削除場所そのものを新生空点へ数えない。

正しいD4分類は51軌道、全配置の安定化群位数1。旧報告の309軌道・安定化群0という値は使用しない。この特徴検算は既存完了列挙を入力とする有限計算であり、新しい全探索完了や一般盤の幾何定理ではない。
