# 高速レーン session log: n7 k=8 行判定（2026-11-22、第2セグメント）

前半（5×5/6×6 全行較正・K1225・README bullet）は
[n56 rows calibration session log](2026-11-22-n56-rows-calibration-session-log.md) 参照。

## 前セグメント仕上げ（08:10-08:14Z）

- 前セッションの未確認 push（determinism.json + session log）は着岸していなかったことが
  判明 → 同一 payload を再 push、`423ff804` で着岸。
- fetch-back照合: 刊行ファイル115件を commit 固定 raw URL + sha256sum で全件照合、
  114件 byte一致。`classify_summary_n6_k10.json` の1件だけ刊行漏れ（NON-publish事故）
  を検出 → 補 fill commit `9559640e` で全件一致になった。
- K1225 item を `research/knowledge/items/K1225-small-board-maximal-rows.md` に刊行
  （`a0f00185`）。knowledge README 末尾に K1225 bullet を追記（`6ac64c39`・create_or_update_file
  に blob sha `0d41899f…` ロック・push後 commit 固定 URL で 793,758 byte 完全一致。
  refs/heads/main の生 fetch は CDN キャッシュで旧サイズを返すため commit 固定 URL 必須）。
- 途中で1回 fast-forward race（push_files が「not a fast forward」）→ 最新 main を
  取り直してretryで解決（並走の class1518 part 4 と K1058 レーンが同時刻に push）。

## n7 k≥8 行（単一オーナー宣言 `08:16:56Z`・HEAD `d9c59583`）

1. **動機**: 残未着手領域のうち最安価で情報価値が高いのは7×7の k=8 行
   （「7×7のk=8行・8×8のk=9行は未着手」の前者）。7石行カタログ（K1224）が
   lex-leader 2モデル確定済みで、at-most-k+leaderブロックで行判定が閉じる。
2. **方式の壁と回避**: enc_sat2 の Sinz カウンタは one-way なので
   「C(N−1,k) 単位節で exactly-k」は**不健全**（逆方向が偽の充足を許す）。
   代わりに既知 leader 2モデルのブロック節方式（README の健全性議論）。
   構造補題（反鎖）は使わない設計にした。
3. **較正**（受入条件1）: ブロックなし at-most-7 SAT → O1 そのもの（24.8s）。
   O1+O2 ブロック付き at-most-7 → **UNSAT 51.8s**（≤7石モデルが O1/O2 のみの再導出）。
4. **k=8 行判定**: default 0.37s で **SAT**。witness
   `[[3,2],[5,2],[1,3],[5,3],[6,3],[0,4],[2,4],[3,4]]`。
   shuffle=42 ショットも同一 witness（0.39s）→ **M_7 ≥ 8**。
5. **検証**: pinned verify_witness.py SAFE+MAXIMAL rc=0（41/41 blocked・証人明示）。
   1石除去 tamper 8/8 すべて SAFE かつ NOT-MAXIMAL。
6. **bounded census**: leader ブロック反復で331軌道（230秒予算打ち切り）。
   331/331 独立検証 PASS（幾何・indicator-lex-min・重複ゼロ・O1/O2包含0）。
   先頭20反復の決定性スポット検査 PASS。
   **初の安定化群位数2の8石配置 `[3,6,14,19,29,34,42,45]`**（180°回転不変）・
   **trip=0（三点共線なし）の8石配置が2軌道**（7石行の全16配置が三点共線を持つ
   ことと対照的）。
7. **toast**: verify_census8.py の初版は「ソート済み石リスト最小」を lex-min と
   誤実装 → indicator-vector 辞書式（0<1）に修正して全リーダー PASS。
   幾何 oracle の単体検査（円・直線・非共円・正方形＝共円）を通してから使用。

## 刊行

- 実験: `research/experiments/n7-rows-k8plus-sat-20261122/`（README・MANIFEST・
  scripts 3・pinned 4・output 24）
- 単一オーナー宣言: `research/log/2026-11-22-n7-rows-k8plus-sat-single-owner-note.md`
- knowledge item + README bullet: 別コミット。

## 残件

- 8石行の完全 census（打ち切り331軌道・推定数千規模・別セッションで resume 参照:
  census8.mjs は state file 付きで中断再開可）。
- k=9..13 行の判定は8石行の完全リーダー census が前提（leader blocking ladder）。
  alternatively 両方向 counter の健全版（iff-counter を独立実装+検証）で直接
  exactly-k を作る道があるが本セッションでは実施しない。
- n=8 の k=9 行（予算内の stretch として残置。51リーダーの導出は
  K0032 出版カタログから計算可能）。
- CNF 本体は非刊行・sha256 ピン（determinism.json）。
