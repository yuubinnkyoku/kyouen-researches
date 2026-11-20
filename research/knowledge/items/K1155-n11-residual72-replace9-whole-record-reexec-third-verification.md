---
id: K1155
title: 残余72行 replace9 whole-record第二検証（K1151）のpristine再実行第三検証: 出版pin 2/2+入力10件一致・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random計4実行byte-identical・1 byte tamperをfail-closed捕捉
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - third verification (post-publication independent re-execution) of K1151 replace9 whole-record second verification: published machine e92fb755 and audit 5888afb3 (115,002 bytes) fetched at pinned commit f7aa541f with 10 input snapshots staged from the same pinned tree, machine pristine-re-executed 4 times (2 same-cwd, isolated tree/cwd/HOME, isolated + PYTHONHASHSEED=random), all outputs byte-identical to the published audit 5888afb3 across all 334 gates
  - tamper test: 1-byte input mutation (.input-replace9.json offset 7701, XOR 0x01, mutated sha 74e25aa4) fails closed with returncode 1 and no output written; the published machine's fail-closed pins catch transport/tampering; third-verification harness audited deterministically (audit byte-identical across 2 same-cwd + 1 isolated-cwd run, sha 6e06f12ad)
  - no new search computation, no residual row closed; every gate parses the published audit bytes rather than re-deriving game-theoretic values; nodes/solved counts are re-read from the pinned record, never interpreted as win/loss
relations:
  - type: verifies
    target: K1151
    note: 残余72行 replace9 whole-record第二検証（出版commit f7aa541f342d67b33f34fee2df5e31c262cb0691）の実験一式13ファイル（検証機・10入力snapshot・監査正本）の、出版後の別実行者によるpristine再実行第三検証。出版レーン自身の環境に加え、第4〜7環境相当（同一cwd 2回・隔離tree/cwd/HOME・隔離+PYTHONHASHSEED=random）で出版監査 5888afb3 とbyte一致した
artifacts:
- path: research/experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/README.md
  role: document
  note: 実験README（pin表・harness仕様・4実行手順・tamper・再現コマンド・解釈規約）
- path: research/experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/scripts/verify_k1151_reexec_third_20261120.py
  role: verifier
  note: 第三検証harness（stdlibのみ・fail-closed・乱数・時刻・環境依存出力なし・検証機+出版監査2 pin内蔵・10入力snapshot stage・4回pristine再実行+1 byte tamper・監査JSONはsorted keysで実行時間を含まない・SHA-256 cf1ae8ba390faf74fe149015777e46f8502a7fa23c9db35b17c7a3a1ff161f70・11,144 bytes）
- path: research/experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json
  role: data
  note: 監査正本（SHA-256 6e06f12ad311ef1bc568dc775a39b6edb72e43f7696fab874b2755d5c3f0986a・5,024 bytes・pin gate 2/2+10入力sha・run gate 4/4・tamper gate PASS・interpretation_guard 5文言同梱・同一cwd2回+隔離cwd1回の3実行byte一致・status k1151-reexec-third-verification-passed）
- path: research/log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification.md
  role: log
  note: 実行記録（staging→事前probe→単一オーナー宣言→harness修正→全gate→part1出版・fetch-back→引継ぎ）
- path: research/log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit f3097440c0ca5021018c0f4fdbb55cb2fb2fee09・2026-11-20T15:06:08Z宣言・先行出版）
scope: >-
  K1151（残余72行 replace9 whole-record第二検証、出版 commit f7aa541f342d67b33f34fee2df5e31c262cb0691）
  の実験一式13ファイルの pristine 再実行第三検証。出版byte（検証機 e92fb755…・出版監査 5888afb3…・
  115,002 bytes）の SHA-256 pin 確認、10入力snapshotのpinned取得とfail-closed照合、出版機の
  pristine 再実行 4 回（同一cwd 2回・隔離tree/cwd/HOME 1回・隔離+PYTHONHASHSEED=random 1回）の
  出力 byte 一致、1 byte tamper の fail-closed 捕捉、第三検証harness自身の決定性 3 実行 byte 一致、
  part1出版のfetch-back検証までを含む。334 gate の内容の新規再導入・残余72行の閉鎖・
  18 probeの再実行（K1149レーン管轄）・他レーン成果の検証・既存文書の改変は含まない。
evidence: >-
  （1）出版byte完全性: pinned commit f7aa541f342d67b33f34fee2df5e31c262cb0691 の raw CDN から検証機
  verify_replace9_whole_record_20261120.py（SHA-256 e92fb755…）・出版監査
  replace9-whole-record-second-verification-20261120.json（5888afb3…・115,002 bytes）を取得し pin 一致。
  10入力snapshot（.input-k1085/k1086/k1089/k1091/k1095/k1097/cover-decision/probe-records-replace9/
  k1147-external-audit + .jsonl）も同 commit から取得し、検証機内部のfail-closed入力pinが全件照合。
  （2）pristine再実行 4 回: 1 byte も改変していない出版機と10入力を、各実行前に監査を同stageから除いた
  新規treeで、同一cwd 2 回（ambient・PYTHONHASHSEED unset）・隔離tree複写+隔離cwd+隔離HOME 1回・
  隔離+PYTHONHASHSEED=random 1回で実行し、全4回とも returncode 0・334 gate all_pass=True・
  出力 SHA-256 5888afb3… 115,002 bytes で出版監査と byte-identical。1実行あたり0.2秒未満。
  事前 probe 1 回（0.16秒・byte一致・334 gate PASS）は兵站的事実として宣言ノートに記録。
  （3）tamper gate: 入力 .input-replace9.json の offset 7701 の 1 byte を XOR 0x01 で改変した偽入力
  （改変後 SHA-256 74e25aa4…）に対して出版機は returncode 1・出力を書き込まず fail-closed 終了。
  出版機の入力pinが1 byte 改ざんを確実に捕捉することを第三者が確認した。
  （4）harness決定性: 第三検証harness（verify_k1151_reexec_third_20261120・cf1ae8ba…・11,144 bytes）の
  監査JSONは同一cwd 2回＋隔離cwd/隔離HOME 1回の 3 実行で byte-identical（SHA-256 6e06f12a…・
  5,024 bytes・sorted keys・時刻・実行時間を含まない）。監査は pin gate 2/2+10入力sha記録・
  run gate 4/4・tamper gate PASS・status k1151-reexec-third-verification-passed。
  （5）出版とfetch-back: part1（実験dir 3ファイル）を commit d6832fc58524e97dde889efe0d20f7cec71e91df
  （2026-11-20T15:07:32Z）で出版し、同 commit の raw CDN から再取得して harness・監査のSHA-256が
  staging正本とcmp全一致（harness cf1ae8ba…・監査 6e06f12a…・curl+sha256sum照合）。
  （6）採番: 単一オーナー宣言（f3097440c0…・15:06:08Z・K1155を最初に要求）が先着。part1出版時点の
  main（d6832fc585）で K1155 は空き。K1150=general-multiset mergeレーン先着・K1151=自レーン・
  K1152=y12 two-token再採番・K1153=自レーン（zero triple provider reexec・K1148検証）・
  K1154=remo K0919周期特徴付け（14:50:48Z宣言→remoが自ら後着規則で再採番）の後の次の空き番号。
  本検証は残余72行のどの行も閉じない。334 gate はs5/s4記録の整合照合であり勝敗の新規計算ではない。
  nodes/solved数を勝敗として読まない。REFUTED-D10 は LOSS 証明ではない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

---

## 詳細

単一オーナー宣言ノート（commit `f3097440c0ca5021018c0f4fdbb55cb2fb2fee09`・2026-11-20T15:06:08Z・宣言時刻・先行出版）の下で、
[K1151 whole-record第二検証実験](../../experiments/n11-residual72-replace9-whole-record-second-verification-20261120/README.md)（出版 commit `f7aa541f`・2026-11-20T14:41:19Z）に
対して第三検証層を追加した: 出版byte 2 pin+入力10件確認・出版機の pristine 再実行 4 回（PYTHONHASHSEED=random 隔離環境含む）の
全 byte 一致・1 byte tamper の fail-closed 捕捉・第三検証 harness 自身の 3 実行監査 byte 一致、である。

本検証の個性は、K1151 の実験dirが検証機・10入力snapshot・出版監査を単一dirに含む自己完結型である点を利用し、
**出版byteをGitHubから再取得するだけで、181,000 bytes超の監査正本がpinと入力のみから新規に再生成できること**
（輸送・転写・ローカル記憶を介さない独立検証可能性）を、出版レーン自身ではなく別実行者の立場で確定した点にある。
334 gate のgame-theoretic内容（s5 verdict cache・s4 certificate manifest・残余連鎖再導入・census・pool照合）は
出版機の再実行によってのみ再現され、本レーンは再導入を行っていない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/README.md)・
[検証機](../../experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/scripts/verify_k1151_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual72-replace9-whole-record-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification.md)・
[単一オーナー宣言](../../log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md)。
