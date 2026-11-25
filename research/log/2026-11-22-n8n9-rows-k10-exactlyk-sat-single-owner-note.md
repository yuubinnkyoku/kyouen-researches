# 単一オーナー宣言: n=8 k=10 行 / n=9 k=10 行の exactly-k SAT 判定（2026-11-22）

- 観測 HEAD-before-push: `9e10cd0636a2f849cb480d09f61a370cc85d9e50`（2026-11-22T13:03:15Z・レビュー済み50コミットに本スコープの対抗宣言なし・K1226明示の「M_8上界（k=9..13行）・n≥9盤面は未着手」を確認）。
- レーン: 高速レーン（自実行）。K1226（n7k8/n8k9行・2026-11-22）の残課題のうち、最初の2セル **8×8 k=10行・9×9 k=10行の非空虚判定** を着手する。
- K番号は仮（publish時に最新main 404照合で確定）。

## スコープ

- 対象: 標準共円盤（q=4）の n=8, k=10 行 / n=9, k=10 行の非空虚判定（exactly-k）。
  予算が許せば n=9 k=9（較正・s_9=9 既知値への照合）、n=8 k=11、n=9 k=11 に拡張する。
- n9石数行・n8 k=10..11行の既存実験Dir・K項は启動前に直接grep済みで未着手（K1226・K1225・K1224の範囲外）。
- 標準 11×11 空盤・二石 root・S2・closure class は本レーン非接触。UNKNOWN のまま。

## 方式と受入条件

- 符号化: 出版正本 enc_sat2.mjs v2.1（S1安全 + Z完全Tseitin + LX完全二方向lex-leader鎖 + S4 Sinz at-most-k・byte同一ピン）をそのまま使用し、
  **at-least-k のみを新規リフト**（双対Sinz: ¬x_i に対する at-most-(N−k) 逐次カウンタ）で exactly-k を実現する。
  unit節によるexactly-k化は既刊の不健全方式のため使用しない。
- 較正（受入条件1・4/4 direct hit を要求）:
  1. n=6, k=11 → SAT（K1225完全2重走行の出版行 464 に合致: witness は SAFE+MAXIMAL の11石）
  2. n=6, k=12 → UNSAT（K1225出版の零行の再導出）
  3. n=7, k=6 → UNSAT（K1224出版の k=3..6 全負の再導出）
  4. n=7, k=8 → SAT（K1226出版行の水準: witness は SAFE+MAXIMAL の8石）
- 本番判定: default と --shuffle=42 の2ショット一致（受入条件2）。
- SAT witness: 出版正本 verify_witness.py（整数4×4行列式）で SAFE+MAXIMAL・1石除去 tamper がすべて SAFE かつ NOT-MAXIMAL（受入条件3）。
- UNSAT判定: 較正4/4合格後の2ショット一致 UNSAT のみを行 emptiness として記録する（kissat・符号化のtrust込み・形式証明ではない）。
- CNF本体は非刊行・sha256 を determinism.json にピン。kissat 4.0.4 は公式 linux-amd64 binary を md5 `3a5eba830aa6008a604fcc9bbe99a325` でピン（repo内再出版なし・n7カタログ実験と同一binary・K1224規約）。
- 実験ディレクトリ: research/experiments/n8n9-rows-k10-exactlyk-sat-20261122/
- 本番が INDET のみに終わった場合は新成果としては報告しない（honest negative の実験記録はRepo方針に従い出版する）。

## 運用メモ

- 並走（同一タスクの hourly 実行）は本宣言以後、このスコープ（n8k10/n9k10・k11拡張）に着手しないこと。宣言時刻は本コミットのcommitter date参照。
- push競合・sha衝突・取得失敗時は押し進めず状況を簡潔に記録して引き上げる（次回実行へ回す）。
