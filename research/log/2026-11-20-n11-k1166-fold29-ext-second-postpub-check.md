# K1166外部第二検証の出版後再現確認（2026-11-20）

本ノートは K1166（K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証・
part1 `80ce56914d`・part2 item/log `d63055f6f0`・part3 README bullet `f55ac313b4`）の
出版後に、**出版byteをGitHubから取得し直して**第三者が同じbatteryを走らせられることを
実機で確認した記録である（出版前のローカルbyteではなく、push後のrepo byteのみを使用）。

実施内容（20:26-20:31Z）:

1. 最新main HEAD pin `f55ac313b4a358019cdbc89ab091a063a045725a` から実験dir
   `research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/`
   の全44ファイル（harness `ca662e57…`・取得器 `c3c4c9ff…`・pin表 `949868e2…`・
   監査正本 `cf6a26ab…`・3根fresh記録39点）をraw URLで再取得。
   harness・取得器・pin表・監査正本は出版前ローカルbyteと `cmp` 完全一致。
2. 出版済み `fetch_master.py` で master/ をpin commit `28d223a2d…` から再構成
   （実測13.0秒・61ファイル全git blob pin fail-closed検証込み・all_blob_pins_ok true）。
3. 出版harness＋再構成masterのみでbattery 1巡を `run/` に新規生成:
   pin PASS 61/61 → root k1136 13 gates PASS（90.0秒）→ root k1137（52.8秒）→
   root k1139（112.2秒）→ tampers 3 gates PASS（8.9秒）→ finalize。
   計43 gates PASS・出力 `run/harness-audit.json`（SHA-256
   `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`）が
   出版監査正本 `output/harness-audit.json` と**byte-identical**。
   証明書組立・BigInt・Bareiss・出版監査機pristine再実行（r1/r2/r3＋fresh記録差し替え）
   は本batteryでも全gate PASS（出版正本3点 `d0653834…`/`dafa177b…`/`e706ca6f…` とbyte一致）。

fail-closedの追加実測: master/未構成のまま `--stage pin` を実行すると
`mismatch_or_missing: 61` で即FAILし（masterをsudo的に読み替えない・
既存成果物を再利用しない）、fail-closed pin gateが出版byteの再取得を
強制することを確認した（計算には無影響・記録として残す）。

結論: K1166実験は**repoの出版byteのみから**（masterは出版fetch_master.pyと
pin表・それ以外は実験dir内のbyte）、第三者が同一の43 gate監査正本をbyte再生できる。
セッション全体では同batteryを4巡（出版前3巡＋出版後1巡）実行し、
4巡すべての監査正本がbyte一致した。

行は1行も閉じない。残余20行・pool P⁗ 120,416根は不変。
REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
