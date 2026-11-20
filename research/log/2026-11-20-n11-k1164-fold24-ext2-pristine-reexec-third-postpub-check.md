# K1165第三検証の出版後再現確認（2026-11-20）

本ノートは K1165（fold24外部第二検証＝K1164のpristine再実行第三検証・
part1 `1c1d97aac7`・part2 item/log `de2bb04f`・part3 README bullet `7de429b22`）の出版後に、
**出版byteをGitHubから取得し直して**第三者が同じbatteryを走らせられることを
実機で確認した記録である（出版前のローカルbyteではなく、push後のrepo byteのみを使用）。

実施内容（19:34-19:38Z）:

1. part1 commit `1c1d97aac7` から実験dirのstaged 12点とharness
   （`f45aa1ac1d022c6517dd49f5e9bf151c0834ea82545410349fccb41d1ccd6d31`）を再取得。
   `diff -rq` で出版stagedが出版前のローカルstagedと完全一致。
2. 出版済み `staged/k1140/reconstruct_inputs.py`（`f4e1fa8e…`）でWを**3回目**として
   再構成（固定Git参照 `b91e85a9…`・61 pin fail-closed検証込み）。
   `diff -rq` でW-A（battery当時の再構成）と完全一致。
3. 出版harness＋出版staged＋(W-A, W-PUB) でbatteryを1回実行:
   `{"audit_sha256": "efffaab8ad5693afe432fe6f66abea30ffd1eb2b7a3e524af65718057bda327e",
     "gate_count": 66, "status": "PASS", "tamper_cases": 3, "verifier_runs": 4}`
   （実測3m17.4s・検証機4回の監査JSONは出版正本 `c7e10332…` とbyte-identical・
   harness tamper 3件fail-closed）。出力監査JSONが出版harness監査正本
   `efffaab8…`（`output/harness-audit.json`）とbyte-identical。

結論: K1165実験は**repoの出版byteのみから**（Wは出版reconstruct_inputs.pyと固定Git参照
・それ以外は実験dir内のbyte）、第三者が同一の監査正本をbyte再生できる。
セッション全体での検証機fresh実行は計17回（smoke 1＋battery 3×4＋post-publication 4）＝
fold24出版機68回のfresh再実行（fold23隔離rerun chain込み）・同梱独立監査17回の再実行に相当。

運用上の注記: 本確認で1回、中間生成物（`pubrepo/`のharness取得物）を誤って
`rm -rf pubrepo`で消し、harnessのみ再取得してやり直した（計算には無影響・記録として残す）。
行は1行も閉じない。残余20行・pool P⁗ 120,416根は不変。
REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
