# 4行 q=6/q=7 witness band・witness-free 掃引（2026-11-21 高速レーン実行）

単一オーナー宣言（[2026-11-21T00:45Z](2026-11-21-four-row-q6-q7-witness-frontier-single-owner-note.md)・commit 528ec960）に続く同一レーンの掃引実行記録。成果は K1177 に昇格済み。

## やったこと

1. **較正**: pinned kissat 4.0.4（md5 3a5eba83…）で (6,16,6) 陽性対照を再現（CNF md5 `22dd41bae3f…` 一致・conflicts 46 bit-exact・0.11s・29石）。sat.js/sat2.js は K1134/K0827 lane と同一 md5 pin。
2. **q=6 掃引（witness band）**: m=6..15 すべて SAT（石数 14..19・3系統検証 PASS）。行型は概ね [4,5,5,5]/[5,5,5,4] 型（m=6,7 は行長制約で [1,3,5,5]/[1,4,5,5]）。
3. **q=6 掃引（witness-free band）**: m=16..27 すべて UNSAT（conflicts 1.42M..3.70M・52..220s/幅・INDET 0）。時間は幅とともに増大、外挿で m=28 は ~280s 以上。
4. **q=7 掃引（全面）**: m=7..12 SAT（witness・19..23石）→ m=13 で UNSAT（5,446 conflicts・0.12s）→ m=14..72 まで 60幅すべて UNSAT（conflicts ほぼ非増加・0.04..0.13s/幅）。witness band と witness-free の境界は幅 12/13 で完全に確定。
5. **capacity（満容量存在側）**: sat5.js 符号化（core + 全行 >= q−1 unit）で (4,16,6) 20石 全行5・(4,13,7)/(4,16,7) 24石 全行6 が SAT。verify_witness.py/verify3.py に --capacity モードを追加し、3系統で 安全+極大+全行 q−1 を検証。
6. **交差符号化**: (4,16,6) と (4,13,7) の def-mode + --lex=H が双方 UNSAT（1,351,887 conflicts@45.6s・4,599@0.12s）。境界幅の符号化独立性を確認。

## 主張（K1177 昇格）

- **M_{4,6} = 16 or M_{4,6} >= 28**（witness band {6..15}・witness-free {16..27}・U_{4,6}=103 は K0318 引用値）
- **M_{4,7} = 13 or M_{4,7} >= 73**（witness band {7..12}・witness-free {13..72}・U_{4,7}=81）

被覆論は K1134 と同一: m >= q では行cap=q−1 なので「不満容量 ⟺ 行欠損」が def-mode 単一節と一致し、極大安全配置の存在（貪欲拡張）と合わせて def-UNSAT ⟺ P(m)。

## ツール面の修正・失敗

- runner.js cap モードは当初、capacity 配置（行欠損でない）を deficient 検証器の基準で判定して FAIL としていた（検証器側の契約と設定セマンティクスの不一致）。verify_witness.py・verify3.py に --capacity モード（安全+極大+全行 q−1）を追加し、runner cap の判定条件を修正後に再実行して全系統 PASS を確認した。失敗レコードは records から排除済み（修正後に再生成）。
- q=6 m=28 は未着手（外挿 ~280s+/幅で INDET の可能性大・残実行時間との兼ね合いで見送り）。

## 観察・予想（未証明）

- q=7 の witness-free UNSAT が幅非依存に高速であることから、m >= 13 全幅で成り立つ局所障害（ブロッキング計数）が存在する可能性。**M_{4,7} = 13 全称予想**として K1177 に記録。証明候補: 欠損行の各空点は >= 5 石を含む census 曲線で被覆される必要があり、使用可能石数 <= 23 のもとで幅 >= 13 の空点全体を被覆できない、という計数。

## 次回レジューム

- q=6: m=28 以降の掃引（280s cap・INDET なら rowY 分割）。witness-free band 延伸で主張の ">= 28" 部分を改善。
- q=7: 全称予想の定式化（ブロッキング計数の有限窓化: 欠損行の空点を被覆する曲線はその行の石と隣接行に集中するか？）、または m=73.. の追加掃引。
- 実験 dir: `research/experiments/four-row-q6-q7-frontier-20261121/`（runner.js は tag 冪等なので records.jsonl を壊さず追記掃引可）。
