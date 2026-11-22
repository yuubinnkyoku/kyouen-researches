# s_12/s_13 SAT両側判定レーン・セッションログ（2026-11-22）

- 実行者: 高速レーン（単一オーナー宣言 `71408dda54` 対応、宣言ノート: [2026-11-22-s12-s13-sat-stabilization-single-owner-note](../log/2026-11-22-s12-s13-sat-stabilization-single-owner-note.md)）
- 対象: n=12 at-most-10 / n=13 at-most-11 のSAT両側判定と較正ラダー
- 成果アーカイブ: [s12-s13-sat-stabilization-20261122](../experiments/s12-s13-sat-stabilization-20261122/README.md)
- K項目: K1220（十石witness 5類・s_7再導出）、K1221（lex-leader軌道被覆機械検査規約）

## 実行順序と摘要

1. 機材作成: v1（t_q一方向）→ kissat対照 → v2 draft（z完全Tseitin + D4 lex-leader鎖 draft版）。
   v1は n7k6・n12k11 で 240秒級 UNKNOWN（符号化トーンの対照記録）。
2. draft UNSAT 2ショット（n7k6 default 70.23s・sh42 90.59s）を「s_7>=7再導出」候補として得たが、
   **出版前の自家機械検査（lexchain_orbit_check.mjs）で鎖の受理言語が A<=lex g(A) と一致しないことを発見**。
   小盤全列挙で棄却ベクトル（n=4で36,808対）と軌道完全遮断（n=4で8,548中3,195軌道）を定量化し、
   draft UNSAT全件を取り下げ（erratum-2）。
3. 修正版v2.1（完全二方向Tseitin鎖）を作成。修正過程3件のミス（subsumption・否定向き・符号）を
   検査がそれぞれ捕捉。最終版でP1〜P5全PASS（d鎖全列挙照合6,300対0不一致・受理言語全列挙両方向一致・
   遮断軌道0・lex-min代表全受理）。
4. v2.1で較正チェーン実行（各 --time=270, 単発・逐次）: n7k6 UNSAT(13.56s) → sh42 UNSAT(15.35s) →
   n7k7 SAT(24.09s) → n8k8 SAT(27.27s) → n9k9 SAT(33.87s) → n10k10 SAT(4.37s) → n10k10sh7
   UNKNOWN(261.68s) → n12k10 UNKNOWN(265.39s)。
5. 全witness（draft 5件・v2.1 4件）をdecode→3系統検証（py/mjs/census直結）+tamper陰性対照。
   分類の結果、10×10十石witnessの格子同型類が2類→5類へ（新3類: span 10×9・7×7・10×4）。
   n7 witnessはK0031合同（陽性対照）、n8/n9は互いに非合同の検証済み2例ずつ。
6. s_12/s_13本体: v2.1 n12k10とdraft n13k11（279.51s）ともcap内 INDET。既知witness再探索
   （n12k11 3ショット・n13k12 1ショット）も未達。不在は主張しない。

## 事故・訂正

- erratum-1: 初回 n10k9/n9k8 を --time なし（SIGTERM）で実行し、統計として使えない状態で
  「UNKNOWN」と数えかけた。n9k8は135秒capで正常終了版に差し替え、n10k9は破損セッション（SIGTERM）
  としてラン表で無効明示（v2n10k9.log）。再実行はv2.1側の難度記録で代替。
- erratum-2: 上記のdraft鎖瑕疵。draft UNSAT（n7k6 2ショット）の取り下げとREADME・本ログへの
  明記で対応。SAT側modelは幾何独立検証で成立するため影響なし。
- cnf-sha256.txt追記時にn7k6/n7k6sh42のハッシュ転記ミス（2件）→ ファイル再照合ループで検出・訂正済み
  （「記録→機械照合→訂正」の規約に沿って全件OKを確認）。

## 保持した非主張

- gap-1（n8k7・n9k8・n10k9）と n>=12 の全UNSAT/未達: honest bounded negative のみ。
- 11×11空盤・二石root・S2・class 1/2/4: 非接触・不変。
- 十石witness全体の分類ではなく既知明示例の最小計数（5）。

## 次回への引き継ぎ

- v2.1符号化+軌道被覆検査済み鎖は以後のSATレーンの基礎機材（K1221規約）。
- n>=12のSAT側には行ごとの分解（K1217式）かresume型の積み増しが必要（難度曲線はラン表参照）。
- 10×10十石witness類の蓄積は「類構造の法則性」仮説形成（類数の増大傾向・spanの多様性）に使える。
- UNDONE検討: K0032の全408カタログとのn8 witness照合、K0320 n12/n13 witness周辺の
  SAT探索（K1206のSLS近傍結果とSAT側の接続）。
