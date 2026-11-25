---
id: K1161
title: "残余23行 零triple-provider禁止円 D4軌道構造解析（16:41Z追加出版）のpristine再実行第三検証（出版pin 4/4・fresh 4実行byte-identical・出版社未検証offsetのtamper 2件fail-closed捕捉・harness監査3実行byte一致）"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - "third verification (post-publication independent re-execution) of the residual-23 forbidden-circle D4-orbit structure post-analysis (published commit 3ccde3e385137b1a51cd2821a078ede38a2b3dfb, 2026-11-20T16:41:05Z)"
  - "published bytes (verifier derive_forbidden_circles.py 45e5d7d6, published audit 0e16f29b 9,730 bytes, K1156 fixture 51e7a465, K1156 direct-fourth audit c4e55dbe) fetched from the pinned commit and pinned 4/4; verifier pristine-re-executed 4 times (runA/runB same cwd, runC isolated tree/cwd/HOME with copied inputs, runD same isolation plus PYTHONHASHSEED=random), all four outputs byte-identical to the published audit"
  - "tamper tests at offsets the publisher README did not test (fixture offset 200 mutated sha f5c6a73d, K1156-audit offset 150 mutated sha 954843ee) both fail-closed with returncode 1 and no output written; third-verification harness audit canonical byte-identical across 2 same-cwd runs plus 1 isolated-tree/cwd/HOME run with PYTHONHASHSEED=random (sha f12abd19, 3,321 bytes)"
  - "no row closed, no DFPN probe, no certificate, no fold; the post-analysis classifies the 10 unsafe occurrences into 2 D4 circle orbits both passing through board center (5,5); safe-candidate exclusion relies on pinned REFUTED-D10 facts, not geometry"
relations:
  - type: verifies
    target: K1156
    note: "K1156第四幾何の後解析として16:41Zに追加出版された禁止円 D4軌道構造解析（実験dir n11-residual23-zero-triple-forbidden-circle-structure-20261121・検証器 derive_forbidden_circles.py・監査正本 forbidden-circle-structure.json）の、出版後の別実行者によるpristine再実行第三検証。本体第四幾何はK1157で第三検証済みだが、本追加解析の検証器・監査は新規byteで未検証だった"
artifacts:
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/README.md
  role: document
  note: "実験README（対象・pin表・4 fresh run・tamper 2件・harness決定性・再現コマンド・解釈規約）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/scripts/verify_reexec_third.py
  role: verifier
  note: "第三検証harness（stdlibのみ・fail-closed・時刻・乱数・パスを監査に含めない・pin 4点内蔵・fresh-run 4回・tamper 2件・監査JSON sorted keys生成・workdirを掃除して繰り返し実行で冪等）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/stage/derive_forbidden_circles.py
  role: data
  note: "出版byte複写（SHA-256 45e5d7d61781e96e1e0afff8f457f06ff69a00a2b5e6777dc03d710e2a122951・16,831 bytes・commit 3ccde3e385）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/stage/forbidden-circle-structure.json
  role: data
  note: "出版監査正本複写（SHA-256 0e16f29b259eac1864ce826324f5a51dfe4d5bd5946a0ea5ef7998daaf39c638・9,730 bytes）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/stage/residual23-provider-input.json
  role: data
  note: "K1156 fixture複写（SHA-256 51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822・3,105 bytes）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/stage/k1156-direct-fourth-audit.json
  role: data
  note: "K1156第四幾何監査複写（SHA-256 c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f・7,627 bytes）"
- path: research/experiments/n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120/output/third-verification-audit.json
  role: data
  note: "第三検証監査正本（SHA-256 f12abd19d0171977a65e403ef6a73257c0fac3d0e8be9ffedf0d9a8483904520・3,321 bytes・gate g1 pin 4/4・g2 fresh 4/4 byte-identical・g3 tamper 2/2 fail-closed・interpretation_guard 5文言同梱・3実行byte一致）"
- path: research/log/2026-11-20-n11-residual23-forbidden-circle-structure-reexec-third-verification.md
  role: log
  note: "実行記録（最新main確認→宣言→stage→全gate→part1出版・fetch-back 7/7→採番→part2）"
- path: research/log/2026-11-20-n11-residual23-forbidden-circle-structure-reexec-third-verification-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit b7d2880cdf66b2a30ad3e5cc8ebe36481ea8eba3・2026-11-20T16:58:00Z宣言・先行出版）"
scope: >-
  commit 3ccde3e385137b1a51cd2821a078ede38a2b3dfb（2026-11-20T16:41:05Z）で出版された
  残余23行 零triple-provider候補の禁止円 D4軌道構造解析（実験dir
  n11-residual23-zero-triple-forbidden-circle-structure-20261121・K1156追加分）の pristine
  再実行第三検証。出版byte（検証器 derive_forbidden_circles.py 45e5d7d6…・出版監査
  forbidden-circle-structure.json 0e16f29b… 9,730 bytes・K1156 fixture 51e7a465…・K1156
  第四幾何監査 c4e55dbe…）の pin 4/4照合、検証機の pristine 再実行 4回（同一cwd 2回・
  隔離tree/cwd/HOME 隔離+入力複写 1回・隔離+PYTHONHASHSEED=random 1回）の出力 byte 一致、
  出版社が検査していない offset（fixture 200・K1156 監査 150）の 1 byte tamper の fail-closed
  捕捉、第三検証harness自身の決定性（監査JSON 3実行 byte 一致）、part1・part2・part3出版の
  fetch-back 検証までを含む。行の閉鎖・DFPN probe・証明書・fold・他レーン成果の検証
  （fold26・round-5 refsolve・WIN8-D10 root 00000000010000809002000040002001 証明書抽出の
  各先行レーン工程）は範囲外。
evidence: >-
  （1）出版byte完全性: 対象出版物の pinned commit 3ccde3e385… から検証器
  derive_forbidden_circles.py（SHA-256 45e5d7d6…・16,831 bytes）・出版監査正本
  forbidden-circle-structure.json（0e16f29b…・9,730 bytes・実byte再計算で size 一致）・
  K1156 fixture residual23-provider-input.json（51e7a465…・3,105 bytes）・K1156第四幾何監査
  k1156-direct-fourth-audit.json（c4e55dbe…・7,627 bytes）をGitHubから再取得し pin 4/4 一致。
  （2）pristine再実行 4 回: runA/runB（同一cwd・staging tree で 2 回）・runC（複写隔離 tree・隔離cwd・
  隔離HOME・入力複写・env -i 相当）・runD（runC と同じ隔離に加え PYTHONHASHSEED=random）の全 4 回が
  returncode 0・出力 SHA-256 0e16f29b… 9,730 bytes で出版監査正本と byte-identical。判定は
  bash sha256sum+cmp を権威とする。1 実行あたり 1 秒未満（14 出現の D4 埋込み再導出・有理数
  Fraction ガウス消去による円当てはめのみで、DFPN 探索・6,555 根の再列挙を含まない）。
  （3）tamper gate: 出版社 README が検査済みの fixture offset 100 とは異なる offset で
  1 byte XOR 0x01 改変（fixture offset 200 → 改変後 SHA-256 f5c6a73d…・K1156 監査 offset 150 →
  改変後 SHA-256 954843ee…）の 2 件が、ともに returncode 1・出力ファイル未生成
  （FAIL-CLOSED: … SHA-256 mismatch）で捕捉。
  （4）harness決定性: 第三検証harness verify_reexec_third.py（session pinned は監査JSONの
  harness_sha256 フィールドとして同梱）の監査JSON は同一cwd 2 回＋隔離tree/cwd/HOME+
  PYTHONHASHSEED=random 1 回の 3 実行で byte-identical（SHA-256 f12abd19…・3,321 bytes・
  sorted keys・時刻・実行時間・実行パスを含まない）。
  （5）出版とfetch-back: part1（実験dir 7 ファイル: README・harness・stage 4 出版byte複写・
  監査正本）を commit b10b57216509f87617d726f7c35a8b38fc764160 で出版し、同 commit の raw
  CDN から再取得して 7 ファイルとも cmp 全一致。
  （6）採番: 単一オーナー宣言（b7d2880cdf66b2a30ad3e5cc8ebe36481ea8eba3・2026-11-20T16:56:15Z
  着地）が先着。K1161 は push 直前 3 点確認（knowledge README grep items/K1161- 0 件・item path
  404・コミットメッセージに K1161 を含む commit 0 件）で空き。
---

## 検証対象

commit `3ccde3e385137b1a51cd2821a078ede38a2b3dfb`（2026-11-20T16:41:05Z）で出版された
残余23行 零triple-provider候補の禁止円 D4軌道構造解析。K1156 第四幾何の後解析として、
unsafe 10 出現を 3 正準四点型（2 つの D4 円軌道・半径二乗 13/2 と 25/2・いずれも盤面中央
(5,5) を通る）へ分類し、零行 3 行がすべて (5,5) を含む軸上連続 3 点を持つことを機械確定した
出版物。本体第四幾何は K1157 で第三検証済みだったが、本追加解析の検証器（16,831 bytes）と
監査正本（9,730 bytes）は新規 byte で未検証のままだった。

## 第三検証の結果

| gate | 内容 | 結果 |
|---|---|---|
| g1 pin | 出版byte 4 点の SHA-256 照合（pinned commit から再取得） | 4/4 一致 |
| g2 fresh-run | pristine 再実行 4 回（同一cwd 2 回・隔離tree/cwd/HOME・隔離+PYTHONHASHSEED=random）の出力が出版監査正本と byte 一致 | 4/4 byte-identical（0e16f29b… 9,730 bytes） |
| g3 tamper | 出版社未検証 offset（fixture 200・K1156 監査 150）の 1 byte XOR 0x01 | 2/2 fail-closed（returncode 1・出力未生成） |
| g4 determinism | 第三検証harness監査JSON の 3 実行 byte 一致 | 3/3 byte-identical（f12abd19… 3,321 bytes） |

これにより、出版byteだけをGitHubから再取得するだけで第三者が第三検証の全gate結果を
新規に再生成できること（輸送・転写・ローカル記憶を介さない独立検証可能性）が確定した。

## 解釈規約

- 本第三検証は有限構造解析の再現性確認であり、行は 1 行も閉じない（残余宇宙は着手時点のまま）。
- safe 4 出現の除外は pin 済み REFUTED-D10 事実に依存し、幾何からは導かれない。REFUTED-D10 は LOSS 証明ではない。
- 候補被覆の簿記でありゲーム理論的証明書ではない。P''' 最大 3 行被覆は K1147 から継承し再証明しない。
- nodes 数・solved 数を勝敗として読まない。DFPN probe・WIN8 証明書・receipt fold・S6 行閉鎖を含まない。

**標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
