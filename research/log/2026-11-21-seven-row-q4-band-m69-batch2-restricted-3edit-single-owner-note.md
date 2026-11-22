# 単一オーナー宣言: 7行 q=4 幅69 restricted 3-for-3 近傍（追加バッチ・batch 2）

- 宣言時刻: 2026-11-21T21:00Z
- 宣言時 HEAD: `b1f82cc3ef72a590b6be5724e20522e3e0fdc28c`
- レーン: 高速レーン（自実行）・batch 1（`2026-11-21-seven-row-q4-band-m69-single-owner-note.md`）の
  直接の続きであり、batch 1 の受入条件に沿った追加範囲の宣言（batch 1 は 3-for-3 を対象外としたため、
  ここで明示的に取得する）。

## 対象・手段（すべて有限的な witness 存在探索のみ）

1. **restricted 3-for-3 近傍**: 既刊基底（優先順: 幅65チェーン基底〔w68 witness の3親を含む〕→
   幅66・幅67チェーン基底 → anchors pool（base53/B59/w57_0/w57_1/sa42..50/w60_a..d）→ 幅68 witness）に対し、
   「3石除去 + 3石追加（final 20石・fresh cell のみ・追加セルは列 x ≥ xMin の窓内）」の
   3-for-3 置換を**窓内で完全列挙**する。final shape は exactly [3,3,3,3,3,3,2]。
   安全性は完全（単独追加 vs 残存三つ組・追加対 vs 残存対・追加三つ組 vs 残存単独の全検査）。
   極大判定は全欠損行空セルの3石曲線被覆。
2. 窓幅は tier 順（xMin=52 → 48 → 必ずしも全域でなく tier で誠実記載）。**窓外の追加・19石型・
   holes 再充填・4編集以上は本バッチの対象外**（honest scoping）。
3. 発見 witness は batch 1 と同じ受入条件（独立2系統検証〔正規化整数直線・円方程式 Python + 素朴4x4行列式〕・
   負対照・浮動小数点不使用）まで満たして初めて K0827 更新・knowledge README 更新を行う。
   不発の場合は本実験 dir（batch 2 セクション追加）と session log に honest negative として記録する。

## 受入条件

batch 1 の受入条件 1..7 を全部継承する（pinned 原版 byte 不変・新規ファイルは
`research/experiments/seven-row-q4-witness-band-69plus-20261121/` のみ・不存在主張なし・
上界 1929 不変・push 直前最新 main 再取得・fetch-back byte 照合・
標準 11×11 は無関係で UNKNOWN のまま）。追加して:
- 3-for-3 列挙器の較正: (a) 2-for-2 に縮退する自明でない方法がないことを単体テストで確認
  （まず単体テスト: 既知 witness の近傍で 2-for-2 結果と整合する制御）、
  (b) 小盤での全列挙対照（brute 4x4 行列式第三系による代表候選の独立再判定）。
- M_{7,4} 区間は witness 発見時のみ [70,1929] に更新。不発なら [69,1929] のまま。
