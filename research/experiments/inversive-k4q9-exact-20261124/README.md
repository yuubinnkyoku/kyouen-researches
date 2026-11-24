# s-弧上界の第2乗数族と 3-モーメント法の厳密最適性（2026-11-24）

## 目的

反転平面 `M(q)` の `s`-弧（各円と高々 `s` 点で交わる点集合）の最大サイズ `K_s(q)`
について、K1291 の 3-モーメント証明を **乗数の取り替え**で改善できるかを決める。
併せて、3-モーメント緩和が「どの `n` まで許すか」を有理数で厳密に計算し、
この手法の限界（これ以上改善できない点）を確定する。

## 主結果

- **定理 1**: `5 ≤ s ≤ q−1`, `q ≥ 9` で
  `K_s(q) ≤ min((s−2)q, n₂(s,q))`。
  `P2_s(r) = −(r−(s−4))(r−(s−3))(r−s)` による上界で、`q ≥ 11`, `s ≥ 6` で
  K1291 の `(s−2)q` を厳密に改善する（`K_9(25) ≤ 161`（旧 175）など）。
- **系 1**: `limsup K_s(q)/q ≤ s−2−d*(s)`、`d*(s) → 2/3`。
  漸近定数が `s−2` から最大 `2/3` 下がる。
- **手法の限界（有限計算）**: 3-モーメント緩和の LP 最適値は、検査した格子で
  `min(P1,P2)` に一致。とくに `s=4` はちょうど `2q+1` で、K1291 の定理 A は
  この方法の最適である。`q ≥ 19, s ≥ 8` では第 3 の乗数がさらに強い（3 例外）。

## 成果物

| path | 役割 |
|---|---|
| `report.md` | 定理・証明・数値表・検証・限界の本文 |
| `scripts/build_board.py` | 円族の構成（出版済み `inversive_fast` を SHA-256 で固定）と設計検査 |
| `scripts/moment_lp.py` | 3-モーメント緩和の厳密 LP 実行可能性（Carathéodory で 4 列列挙） |
| `scripts/moment_p2_bound.py` | 第2乗数族の上界、K1291 の再現、実盤面での恒等式照合 |
| `scripts/moment_certificate.py` | 明示的 Farkas 乗数（`Fraction`）の抽出と再検査 |
| `scripts/local_search.py` | 反復貪欲＋強制挿入による大 `s`-弧探索（`K_4(9)` の下界側） |
| `scripts/sat_arc.py` | `n`-点 `s`-弧の存在 SAT（2 種の円符号化、3 点対称性破り） |
| `scripts/verify_arc.py` | SAT 非依存の証人検査（円族を自前で再構成） |
| `output/board_q{9,11,13,16}.json` | 盤面（点・円・設計検査・`∞,0,1` の添字・SHA-256） |
| `output/moment_p2.json`, `output/moment_p2_large.json` | 上界表（LP 最適値との比較込み） |
| `output/moment_lp_s4.json`, `output/moment_lp_general.json` | LP 最適値 |
| `output/moment_certificates.json` | 乗数証明書（全件 `certificate_ok`） |
| `output/identity_checks.json` | 実 `s`-弧での `ΣP t_r = Y_P` 照合 |

## 状態

- 定理 1・系 1 は証明済み（`K1295`）。
- LP 最適値の格子計算は完了（`K1296`）。第 3 乗数の閉形式は未同定。
- `K_4(9) ∈ [16,19]` は **未確定**。局所探索は 300 秒・45 万反復でも 16 止まり、
  SAT `n=17` は 3 回起動して判定に至らず（§7 に試行内容と失敗理由を明記）。
  上限側の証拠は無い。

## 再現

`report.md` §9 を参照。SAT はリポジトリ外の一時 venv の `python-sat`
（1.9.dev25）を使い、`uv.lock` は変更していない。LP・上界・恒等式の検査は
標準ライブラリのみ（`int`/`Fraction`）で動く。
