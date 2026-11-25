# 単一オーナー宣言: 3行 q=4 列挙閉包レーン m≥28 掃引（extension）

- 宣言日時: 2026-11-21T08:38Z
- 宣言時 HEAD: `f57060f840850c7372c9db7d1d4e0a364ed0dbc6`（main）
- レーン: `research/experiments/three-row-q4-enumeration-20261121/` の拡張。
  既存の出版 scripts / output は一切変更せず、追加の出力ファイル
  （`output/ext28plus/`）のみを出版する。
- 目的: 3×m・q=4 def-mode の m=28 以降を、part1-10 で確立したのと同じ
  列挙閉包 63 プロファイル 3 分割（family 9 = wsearch34.js 構造完全探索 /
  fast 13 = dx34.js fast circle-class 列挙 / lemma 41 = crossing-supply
  補題の算術キル〔m≥22 で自動〕）で掃引し、witness-free 幅集合を
  {24,25,26,27} から順に拡大する（掃った幅についてのみ事実を記述）。
  本実行の目標幅は m=28..31（wsearch34.js の `4 <= m <= 31` チェックが
  上限。m≥32 はスクリプトの 31-bit mask 制限のため本レーンの対象外と明記）。
- 先行宣言の不在確認: 宣言時点の main（HEAD f57060f8）に m≥28 を掃引した
  出版・宣言なし。宣言ノート系のコミットは 07:59Z の本レーン part10 が最後
  （08:28Z s11・08:35Z m22 はいずれも非接触レーン）。前宣言 7b5bdfec の
  受入条件どおり「m≥28 は未掃引で一切主張なし」とされてきた状態を継承。
- 陽性対照: 掃引開始前に pinned wsearch34.js（md5 `526cf1c3…`）で
  m=23 family Y=0 を再実行し、出版済み witness 2 件（a=2）・configs 3136441
  を再発見することを確認済み（本環境・2026-11-21T08:38Z・26.5s）。

## 受入条件

1. **器材は pin のまま**: 7 scripts の md5（wsearch34.js `526cf1c3…`・
   dx34.js `b02235a9…`・sat.js `0cc6021a…`〔frontier レーン pin〕・
   closure_check.py `cafc3978…`・crossval_summary.py `8ae34f3d…`・
   verify_witness.js `06bead66…`・witness_check.py `e48f9bf2…`）が一致する
   byte そのままで実行する。既存出版 output（brute_3x{4..8}・selftest・
   wsearch_crossval・closure_check_13_27.jsonl・dx_sweep_13_23.jsonl・
   dx_sweep_24_27.jsonl・family_sweep_23_27.jsonl・crossval_summary.json・
   m23 witness 系・md5s.txt）は一切変更しない。本拡張の出力は
   `output/ext28plus/` 配下の新規ファイルのみ。
2. **主張の正確な言葉遣い**: 出版するのは「掃引した幅の witness-free」のみ。
   掃引幅が m=28..X に達した場合、witness-free 幅集合 {24..X}（ただし
   M_{3,4}∈[24,69] は不変・下界 24 は witness band 23 終端由来・上界 69 は
   K0024 由来・P の幅単調性は未証明・m>X は未掃引）と記述する。
   witness が発見された場合は増分 witness として別件出版する。
3. **検証チェーン**: 既出版の交差検証チェーン（dx34 direct≡brute_3x{4..8}・
   wsearch≡brute family 15 実行・m=23 陽性対照・closure_check の
   m=4..12 全数列挙との矛盾 0）を継承し、本拡張では pinned script の
   同一 byte 再実行と m=23 陽性対照の再発見をもって環境較正とする。
   掃引結果 JSONL は（m, Y, profiles）全件を機械出力のまま出版する。
4. **既有 K 項目の同一命題更新**: K1183（3行q=4 witness band / witness-free
   幅）を更新し、knowledge README の K1183 bullet を更新する。
   新規 K 番号は採番しない。
5. **並走への配慮**: frontier レーン（SAT・records.jsonl）には触れない。
   m22 / s11 など他レーンのファイルには接触しない。push 競合・HEAD 不一致・
   取得失敗が生じた場合は残 part を次回実行へ繰り越す（無理に押し進めない）。

以上の条件で本レーンの m≥28 掃引を開始する。
