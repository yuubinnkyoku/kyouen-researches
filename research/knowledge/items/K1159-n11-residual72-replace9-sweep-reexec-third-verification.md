---
id: K1159
title: "残余72行 代替9根掃引再実行第二検証（K1149）のpristine再実行第三検証（出版pin 13点一致・pass Aとpass Bで合計36 probeのDFPN探索を新規再実行しそのnodes総計3,574,172が出版値と一致・assemble出力が出版監査とbyte-identical 24/24 gate・1 byte tamperをfail-closed捕捉）"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - "third verification (post-publication independent re-execution) of K1149 nine-root replace9 depth-10 sweep re-exec second verification（published machine verify_replace9_reexec_20261120.py 77cdd9e3 and published audit 27fc420c (11,242 bytes) fetched from pinned commit 87f56932 with staged runner git blob c132cc64, published sweep machine d163b2a1, published volume e8f5d674, published probe-records bdacf0e7 and upstream originals k1085 5fdd342d, k1086 3045e152, k1089 808fbda1, k1091 edd7ac84, k1095 335eca5e, k1097 2896deb0）"
  - "publish-record machine pass structure（pin gate 13 points double-checked against the machine-internal fail-closed pins, pass A fresh re-run of all 18 probes in this tree with 4 workers in 12.8s giving nodes sum 3,574,172 equal to the published value with root 00000000010000809002000040002001 loss=true in both AND orders at 608,293/691,784 nodes and the other 8 roots 16 probes loss=false, pass B fresh re-run in isolated tree/cwd/HOME identical, pristine sweep reassemble byte-identical to the published volume, assemble output byte-identical to the published audit across all 24 gates also under PYTHONHASHSEED=random, tamper at input k1097.json offset 500 caught fail-closed with returncode 1 and no output written, harness audit byte-identical across 2 same-cwd and 1 isolated-cwd/isolated-HOME run）"
  - "no residual row closed; loss=true uncapped probes reproduce depth-10 within-depth forced-loss probe facts and give no certificate-extraction eligibility (extraction is declared by another lane 63877ffd2e), loss=false uncapped probes reproduce REFUTED-D10 facts and are not LOSS proofs"
relations:
  - type: verifies
    target: K1149
    note: 残余72行 代替9根掃引再実行第二検証（出版 commit 7ab77aa1・検証機 77cdd9e3・監査正本 27fc420c）の出版byte一式の、出版後の別実行者によるpristine再実行第三検証。同系譜第三検証（K1153・K1155・K1157）が出版記録機の再実行だったのに対し、本検証は出版されたDFPN probe事実そのもの（9根×両AND順序×2パス=36 probe実行）を最初から再計算した
artifacts:
- path: research/experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/README.md
  role: document
  note: 実験README（pin表13点・harness仕様・pass A/pass B・pristine再assemble・assemble・tamper・再現コマンド・解釈規約・実験dir自体がstaging root）
- path: research/experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/scripts/verify_k1149_reexec_third_20261120.py
  role: verifier
  note: 第三検証harness（Python stdlib＋Node.js runner・fail-closed・乱数・時刻・wall時間を監査JSONに含まない・検証機・runner git blob・掃引機・出版監査・出版volume・出版records・上流6正本の独立pin 13点内蔵・pass A/pass B新規再実行＋pristine再assemble＋assemble 2環境＋tamper・SHA-256 ec55f78a2a109a60d295569aa856a9c01764859c64655ed6aae405d678234979・18,525 bytes）
- path: research/experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/scripts/verify_replace9_reexec_20261120.py
  role: verifier
  note: K1149出版検証機（staging・SHA-256 77cdd9e3450aed9d2c900475f15d9e09367985b909027c50e485995737252db4・41,175 bytes）
- path: research/experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/sweep/scripts/replace9_d10_sweep_20261120.py
  role: data
  note: K1146出版掃引機（staging・SHA-256 d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41・33,969 bytes）
- path: research/experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json
  role: data
  note: 監査正本（SHA-256 7e0824cc11c997882d6b01f528b0ac53205de3ce95891c901bf9da6eb29b7e43・7,700 bytes・pin 13/13・pass A/pass B・pristine_reassemble 1/1・assemble 2/2・tamper 1/1のgate 7種 all true・interpretation_guard 5文言同梱・同一cwd 2回+隔離cwd/隔離HOME 1回の3実行byte一致・status k1149-reexec-third-verification-passed）
- path: research/log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification.md
  role: log
  note: 実行記録（最新main確認→採番紆余曲折→単一オーナー宣言→staging→全gate→part1出版・fetch-back→引継ぎ）
- path: research/log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit c3c4dd28b48ccf4f5782ddb9f1a81e46d24e4787・2026-11-20T16:01:30Z宣言・先行出版）
scope: >-
  K1149（残余72行 代替9根掃引再実行第二検証・出版 commit 7ab77aa1）の出版byte一式の pristine 再実行第三検証。
  出版pin 13点（検証機・runner git blob・掃引機・出版監査・出版volume・出版probe-records・上流6正本）のSHA照合、
  pass A（本tree・18 probes全件新規再実行）と pass B（隔離tree/cwd/HOME・入力複写・18 probes全件新規再実行）の
  決定性字段照合、出版掃引機のpristine再assembleと検証機assemble（PYTHONHASHSEED=random含む）の出版監査との
  byte一致、1 byte tamper（input/k1097.json offset 500）のfail-closed捕捉、第三検証harness自身の3実行byte一致、
  part1出版（17ファイル）のfetch-back照合までを含む。WIN8-D10証明書抽出（root 00000000010000809002000040002001・
  別レーン宣言 63877ffd2e）・残余20行のrefsolve第5ラウンド（ace38772d9）・fold26（23bffdd4e4）・他レーン成果の
  検証・既存文書の改変は含まない。行は1行も閉じない。
evidence: >-
  （1）出版byte完全性: 検証機 verify_replace9_reexec_20261120.py（77cdd9e3…・41,175 bytes）・
  runner v17固定コピー（git blob c132cc64…・12,481 bytes）・出版掃引機（d163b2a1…・33,969 bytes）・出版volume
  （e8f5d674…・15,403 bytes）・出版probe-records（bdacf0e7…・10,567 bytes）・上流6正本（39,221/21,835/17,511/
  17,963/16,605/43,540 bytes）・出版監査（27fc420c…・11,242 bytes）をpinned commit 87f56932… のraw CDNから取得し
  pin 13点全一致（harness側独立pin＋検証機内部fail-closed pinの二重照合）。実験dir自体がstaging rootを兼ね、
  --root . で再現可能。（2）pass Aとpass B: 本treeで18 probes（9根×両AND順序）を4 workersで12.8秒で新規再実行し
  18/18完走・nodes総計 3,574,172 == 出版値・00000000010000809002000040002001 が両AND順序で loss=true
  （608,293/691,784 nodes）・他8根16 probeは loss=false・capped/timeout/error 0。隔離tree/cwd/HOMEのpass Bも
  18/18同一・nodes総計一致（約12.9秒）。（3）pristine再assembleとassemble: 出版掃引機を隔離treeで出版probe-records
  に入力して再実行し出力SHA-256 e8f5d674… が出版掃引正本とbyte-identical。fresh passA/passB/pristine volumeから
  検証機assembleを実行し出版監査 27fc420c… とbyte-identical（24/24 gate PASS）。PYTHONHASHSEED=randomの
  assemble再実行もbyte-identical。（4）tamper gate: 複写treeで input/k1097.json のoffset 500の1 byteをXOR 0x01
  （改変後 SHA-256 7cc71c5f…）で改変すると検証機は run mode で returncode 1・probe records未書込のfail-closed終了。
  （5）harness決定性: 第三検証harness（ec55f78a…・18,525 bytes）の監査JSON（7e0824cc…・7,700 bytes）は同一cwd 2回＋
  隔離cwd/隔離HOME 1回の3実行でbyte-identical（sorted keys・時刻・実行時間を含まない）。harness全体は1実行約25.4秒。
  （6）出版とfetch-back: part1（実験dir 17ファイル）を commit 76ef33b2…（16:11:16Z）で出版し、同commitのraw CDN
  から再取得して17ファイルともcmp byte一致。出版byteをGitHubから再取得するだけで出版監査がpin+入力+新規DFPN再計算
  のみから再生成できることを、出版後の第三者が確定した。（7）採番: 単一オーナー宣言（c3c4dd28…・16:01:30Z）が先着。
  当初仮番号K1158で臨んだがK1147外部第二検証レーンが16:06:42ZにK1158を取得したため、AGENTS.md後着優先規則により
  K1159へ再採番した（push直前3点確認: knowledge README grep items/K1159- 0件・item path 404・list_commits 0件）。
  本検証は残余行を1行も閉じない。WIN8-D10 candidateは証明書ではない（抽出は別レーン宣言 63877ffd2e の管轄）。
  REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。残余20行（pool P⁗ 120,416根）
  は全行open。
---

## 詳細

単一オーナー宣言ノート（commit `c3c4dd28b48ccf4f5782ddb9f1a81e46d24e4787`・2026-11-20T16:01:30Z・先行出版）の下で、
[K1149 再実行第二検証実験](../../experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120/README.md)（出版 commit `7ab77aa1`）に対して第三検証層を追加した:
出版byte 13点pin照合・pass Aとpass Bによる36 probe実行の新規再実行・pristine再assemble・assemble 2環境byte一致・
1 byte tamperのfail-closed捕捉・第三検証harness自身の3実行監査byte一致、である。

本検証の個性は、K1153/K1155/K1157が**出版記録機（監査JSONを書く機械）のpristine再実行**だったのに対し、
K1159は**出版されたDFPN probe事実そのもの（9根×両AND順序×2パス=36 probe実行・合計約715万nodes）を新規に再計算する**
この系譜で最も重い第三検証である点にある。nodes総計 3,574,172 がpass A・pass Bとも出版値と一致し、
WIN8-D10 candidate root `00000000010000809002000040002001` の両AND順序 loss=true（608,293/691,784 nodes）と
他8根の loss=false が第三者環境で成立した。さらに出版掃引機のpristine再assembleが出版volume `e8f5d674…` と
byte一致し、assemble出力が出版監査 `27fc420c…` と24/24 gateでbyte一致したことで、
出版byte（GitHubから再取得するだけで手に入る）から出版監査がpin+入力+新規計算のみから再生成できることを、
輸送・転写・ローカル記憶を介さず出版後の第三者が確定した。

WIN8-D10証明書の抽出（root `00000000010000809002000040002001`）は別レーン宣言 `63877ffd2e` の管轄で本検証の範囲外であり、
本検証は抽出の資格を与えない。fold26（`23bffdd4e4`）・refsolve第5ラウンド（`ace38772d9`）も他レーン宣言済みで未着地。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[実験](../../experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/README.md)・
[第三検証harness](../../experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/scripts/verify_k1149_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual72-replace9-sweep-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification.md)・
[単一オーナー宣言](../../log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification-single-owner-note.md)。
