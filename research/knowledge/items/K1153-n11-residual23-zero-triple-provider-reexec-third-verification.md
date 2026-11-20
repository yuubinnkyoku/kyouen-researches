---
id: K1153
title: "残余23行 zero triple provider 第三幾何（K1148）のpristine再実行第三検証: 出版pin 3/3一致・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random計4実行byte-identical・1 byte tamperをfail-closed捕捉"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - "third verification (post-publication independent re-execution) of K1148 residual23 zero-triple-provider third geometry: three published files fetched at pinned commit 6564fded75 and byte-matched against their SHA-256 pins, machine pristine-re-executed 4 times (2 same-cwd, isolated tree/cwd/HOME, isolated + PYTHONHASHSEED=random), all outputs byte-identical to the published audit 526eada2c9"
  - "tamper test: 1-byte fixture mutation (offset 1552, XOR 0x01, mutated sha dd3f3c48) fails closed with returncode 1 and no output written; the published machine's fail-closed pin catches transport/tampering; third-verification layer audited deterministically (harness audit byte-identical across 2 same-cwd + 1 isolated-cwd run, sha 312966e89)"
  - no new geometric computation, no row closed; K1148's zero rows and safe/unsafe census re-derived nowhere outside the published machine's own pinned-byte re-execution
relations:
  - type: verifies
    target: K1148
    note: 残余23行 zero triple provider 第三幾何（出版commit 6564fded75）の実験一式（検証機・fixture・監査正本）の、出版後の別実行者によるpristine再実行第三検証。出版レーン自身の3環境実行に加え、第4〜7環境相当（同一cwd 2回・隔離tree/cwd/HOME・隔離+PYTHONHASHSEED=random）で出版監査 526eada2c9 とbyte一致した
artifacts:
- path: research/experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/README.md
  role: document
  note: 実験README（pin表・harness仕様・4実行手順・tamper・再現コマンド・解釈規約）
- path: research/experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/scripts/verify_k1148_reexec_third_20261120.py
  role: verifier
  note: 第三検証harness（stdlibのみ・fail-closed・乱数・時刻・環境依存出力なし・3出版pin内蔵・4回pristine再実行+1 byte tamper・監査JSONはsorted keysで実行時間を含まない・SHA-256 6f016cd14fad787b7f6b1b5e8acb72b5da3625ed4b2a3d79d2f8bd989c0e7662）
- path: research/experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json
  role: data
  note: 監査正本（SHA-256 312966e890c800e9326d0c05d243ac13a3b9bf161237a2e1571f711d51a8f3dd・3,613 bytes・pin gate 3/3・run gate 4/4・tamper gate PASS・interpretation_guard 5文言同梱・同一cwd2回+隔離cwd1回の3実行byte一致）
- path: research/log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification.md
  role: log
  note: 実行記録（宣言参照・採番経緯・実行時間・fetch-back検証・引継ぎ）
- path: research/log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 75fde9d82854a1ff7b5b9ce09ff1956a3544c67f・2026-11-20T14:53:03Z宣言・先行出版）
scope: >-
  K1148（残余23行 zero triple provider 第三幾何、出版 commit 6564fded75038c887c095873c5d3e5633c4fcd35）
  の実験一式の pristine 再実行第三検証。出版byte 3ファイル（検証機 cb8c95c87・fixture 51e7a4651・
  出版監査 526eada2c）の SHA-256 pin 確認、出版機の pristine 再実行 4 回（同一cwd 2回・隔離
  tree/cwd/HOME 1回・隔離+PYTHONHASHSEED=random 1回）の出力 byte 一致、1 byte tamper の
  fail-closed 捕捉、検証 harness 自身の決定性 3 実行 byte 一致までを含む。幾何の新規計算・
  残余行の閉鎖・他レーン（K1146/K1147/K1149/K1151）成果の検証・既存文書の改変は含まない。
evidence: >-
  （1）出版byte完全性: pinned commit 6564fded75038c887c095873c5d3e5633c4fcd35 の raw CDN から
  検証機 audit_zero_triple_providers.py（SHA-256 cb8c95c8799e6c12bbc7fdb2cc9b6236f664724f29827e56d2e75de62a084892・
  14,225 bytes）・入力 residual23-provider-input.json（51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822・
  3,105 bytes）・出版監査 third-geometry-audit.json（526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573・
  4,418 bytes）を取得し、3 pin が全て一致（輸送破損なし）。
  （2）pristine再実行 4 回: 1 byte も改変していない出版機を、同一cwd 2 回（ambient・PYTHONHASHSEED unset）・
  隔離tree複写+隔離cwd+隔離HOME 1回・隔離+PYTHONHASHSEED=random 1回で実行し、全4回とも returncode 0・
  出力 SHA-256 526eada2c9… 4,418 bytes で出版監査と byte-identical（parsed object でも一致）。
  マシン1実行あたり約4.2秒。出版レーンの3環境実行に加え、隔離treeとhash randomizationを含む
  第4〜7環境相当で決定性を追加確認した。事前 probe 1 回（約4.2秒・byte一致）も兵站的事実として
  宣言ノートに記録。
  （3）tamper gate: fixture offset 1552 の 1 byte を XOR 0x01 で改変した偽入力（改変後 SHA-256
  dd3f3c48e69bd74359b6c0653d591277237963724789d4cbaaeea3bef348c3bf）に対して出版機は returncode 1・
  出力を書き込まず fail-closed 終了。出版機の fixture pin が1 byte 改ざんを確実に捕捉することを
  第三者が確認した。
  （4）harness決定性: 検証harness（verify_k1148_reexec_third_20261120・SHA-256 6f016cd1…）の監査JSONは
  同一cwd 2回＋隔離cwd/隔離HOME 1回の 3 実行で byte-identical（SHA-256
  312966e890c800e9326d0c05d243ac13a3b9bf161237a2e1571f711d51a8f3dd・3,613 bytes・sorted keys・時刻・
  実行時間を含まない）。監査は pin gate 3/3・run gate 4/4・tamper gate PASS・
  status k1148-reexec-third-verification-passed。
  （5）出版とfetch-back: part1（実験dir 3ファイル）を commit 760c506230e7fee39b0d08591a7bb3d267d1c5e2 で出版し、
  同 commit の raw CDN から再取得して harness・audit の byte 一致を確認（harness 6f016cd1…・
  audit 312966e8…・cmp 全一致）。
  採番注記: 本項は K1153 を使用（K1150=general-multiset merge レーン先着 14:39:25Z・K1151=replace9
  whole-record 第二検証・K1152=y12 two-token レーン再採番 commit 855d7d98cd が既に取得済みのため
  次の空き番号）。K1149 二重採番（replace9 reexec 先着 14:30:20Z vs six-row 後着 14:31:45Z）は
  未解消のまま本レーンの管轄外。本レーンのpart2出版直前の main（e635b55dec・remo K0919実験dir出版）
  でも K1153 は空き。
  本検証は行を1行も閉じない。zero rows の列挙は残余行の勝敗決着ではない。nodes数・solved数を
  勝敗として読まない。REFUTED-D10 は LOSS 証明ではない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

---

## 詳細

単一オーナー宣言ノート（commit `75fde9d82854a1ff7b5b9ce09ff1956a3544c67f`・2026-11-20T14:53:03Z・宣言時刻・先行出版）の下で、
[K1148 第三幾何実験](../../experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/README.md)（出版 commit `6564fded75`・2026-11-20T14:28:01Z）に
対して第三検証層を追加した: 出版byte 3 pin 確認・出版機の pristine 再実行 4 回（PYTHONHASHSEED=random 隔離環境含む）の
全 byte 一致・1 byte tamper の fail-closed 捕捉・検証 harness 自身の 3 実行監査 byte 一致、である。

出版レーンは 3 環境（実行環境リセット跨ぎを含む）で出版正本の決定性を確認済みであり、本検証の個性は
（a）出版後の別実行者が pinned byte を取得してのみ再現した点、（b）hash randomization 明示環境を含む
第4〜7環境相当の追加、（c）tamper（1 byte 改ざん）が確実に fail-closed で捕捉される点の第三者確認にある。
幾何の内容（candidate root classes 423・safe 316・excluded_safe 19・unsafe 107・eligible triple providers 297・
zero_union_roots 8・zero rows 3・checks 12 PASS）は出版監査の再実行によってのみ再現され、新規の再導入は行っていない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/README.md)・
[検証機](../../experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/scripts/verify_k1148_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual23-zero-triple-provider-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json)・
[研究ログ](../log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification.md)・
[単一オーナー宣言](../log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md)。
