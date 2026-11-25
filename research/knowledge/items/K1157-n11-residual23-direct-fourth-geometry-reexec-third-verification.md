---
id: K1157
title: 残余23行 零triple-provider第四幾何（K1156）のpristine再実行第三検証（出版pin（検証機+監査+入力3点）一致・同一cwd 2回+隔離tree/cwd/HOME+PYTHONHASHSEED=random計4実行byte-identical・1 byte tamper（出版社検査offset 100と異なるoffset 200）をfail-closed捕捉）
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - third verification (post-publication independent re-execution) of K1156 residual-23 zero triple-provider direct fourth geometry（published machine verify_direct_fourth.py 850df34b and published audit c4e55dbe (7,627 bytes) fetched at pinned commits (inputs 6f2c70e8/261f4847/ce13afe4, machine 3969a050, audit 7c21ad16, full-dir fetch 49e420fe), machine pristine-re-executed 4 times (2 same-cwd, isolated tree/cwd/HOME, isolated + PYTHONHASHSEED=random), all outputs byte-identical to the published audit across all 12 gates （19,665 generation events and 550,620 child positions recomputed each run）
  - tamper test（1-byte input mutation (residual23-provider-input.json offset 200, XOR 0x01, mutated sha f5c6a73d, the publishing lane already covered offset 100）fails closed with returncode 1 and no output written; third-verification harness audited deterministically（audit byte-identical across 2 same-cwd + 1 isolated-cwd/isolated-HOME run, sha 5810ceac）
  - no new geometry variant, no residual row closed; every gate parses or regenerates the published bytes only; cover counts are planning bookkeeping, not game-theoretic certificates
relations:
  - type: verifies
    target: K1156
    note: 残余23行 零triple-provider第四幾何（出版 machine 3969a050・監査 7c21ad16・item 1d1b185a）の実験一式（検証機・3入力fixture・監査正本）の、出版後の別実行者によるpristine再実行第三検証。出版レーンの環境に加え、第4〜7環境相当（同一cwd 2回・隔離tree/cwd/HOME・隔離+PYTHONHASHSEED=random）で出版監査 c4e55dbe とbyte一致した
artifacts:
- path: research/experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/README.md
  role: document
  note: 実験README（pin表・harness仕様・4実行手順・tamper・再現コマンド・解釈規約）
- path: research/experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/scripts/verify_k1156_reexec_third_20261120.py
  role: verifier
  note: 第三検証harness（stdlibのみ・fail-closed・乱数・時刻・環境依存出力なし・検証機+出版監査+3入力の独立pin内蔵・4回pristine再実行+1 byte tamper・監査JSONはsorted keysで実行時間を含まない・SHA-256 315332ba00d78c4c65a142dc09ee790f9ffba8d64e1eaae0e232fde36eff5d83・12,862 bytes）
- path: research/experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json
  role: data
  note: 監査正本（SHA-256 5810ceacb1b3a4d28df594834cff227272c7020ff6eb69dd0b3b5bcdcd3f2d68・4,930 bytes・pin gate 5/5・run gate 4/4・tamper gate PASS・interpretation_guard 5文言同梱・同一cwd2回+隔離cwd/HOME1回の3実行byte一致・status k1156-reexec-third-verification-passed）
- path: research/log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification.md
  role: log
  note: 実行記録（最新main確認→単一オーナー宣言→staging→全gate→part1出版・fetch-back→引継ぎ）
- path: research/log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 251523913cdc962c7f6d1eee581de9b641f0a866・2026-11-20T15:49:00Z宣言・先行出版）
scope: >-
  K1156（残余23行 零triple-provider第四幾何、出版 machine commit 3969a0505d03bebaf12f88875f3fba6b9a5635ff・
  監査 commit 7c21ad16311c9af36e928f993e94da205b577cf7・item commit 1d1b185a7de36748d1653a48f1f0ca397a3b75da）
  の実験一式の pristine 再実行第三検証。出版byte（検証機 verify_direct_fourth.py 850df34b…・
  出版監査 direct-fourth-geometry-audit.json c4e55dbe… 7,627 bytes・入力3 fixture 51e7a465…/526eada2…/17dbd6ab…）
  の SHA-256 pin 確認（harness側独立pin+検証機内部pinの二重）、出版機の pristine 再実行 4 回
  （同一cwd 2回・隔離tree/cwd/HOME 1回・隔離+PYTHONHASHSEED=random 1回）の出力 byte 一致、
  1 byte tamper（offset 200）の fail-closed 捕捉、第三検証harness自身の決定性 3 実行 byte 一致、
  part1出版のfetch-back検証までを含む。幾何の新規変種・残余23行の閉鎖・K1147 8根被覆判定の第三検証
  （別レーン宣言 887e594d 管轄）・他レーン成果の検証・既存文書の改変は含まない。
evidence: >-
  （1）出版byte完全性: 出版各commitの raw CDN から検証機 verify_direct_fourth.py（SHA-256 850df34b…・
  14,771 bytes・commit 3969a050）・出版監査 direct-fourth-geometry-audit.json（c4e55dbe…・7,627 bytes・
  commit 7c21ad16）・入力3 fixture（residual23-provider-input.json 51e7a465… 3,105 bytes・
  k1148-third-geometry-audit.json 526eada2… 4,418 bytes・k1147-external-audit.json 17dbd6ab… 11,150 bytes）を
  取得し pin 一致。harness側で検証機・監査・3入力の独立 SHA-256 pin を、出版機内部の fail-closed pin 3点と
  二重に照合した。（2）pristine再実行 4 回: 1 byte も改変していない出版機と3入力を、各実行前に監査を同stageから
  除いた新規生成として、同一cwd 2 回（ambient・PYTHONHASHSEED unset）・隔離tree複写+隔離cwd+隔離HOME 1回・
  隔離+PYTHONHASHSEED=random 1回で実行し、全4回とも returncode 0・12 gate all ok・出力 SHA-256 c4e55dbe…
  7,627 bytes で出版監査と byte-identical。1実行あたり約5秒（19,665生成事象・550,620個の6石子局面の
  D4正準化・28子被覆・4×4行列式24置換展開の再計算込み）。
  （3）tamper gate: 入力 residual23-provider-input.json の offset 200 の 1 byte を XOR 0x01 で改変した偽入力
  （改変後 SHA-256 f5c6a73d…・出版社が検査済みの offset 100 とは異なる offset）に対して出版機は returncode 1・
  出力を書き込まず fail-closed 終了した。（4）harness決定性: 第三検証harness
  （verify_k1156_reexec_third_20261120・315332ba…・12,862 bytes）の監査JSONは同一cwd 2回＋隔離cwd/隔離HOME 1回の
  3 実行で byte-identical（SHA-256 5810ceac…・4,930 bytes・sorted keys・時刻・実行時間を含まない）。
  （5）出版とfetch-back: part1（実験dir 3ファイル）を commit 792e9e37d2dd1bacb30413a339200f08c6b572e7
  （2026-11-20T15:52:03Z）で出版し、同 commit の raw CDN から再取得して 3 ファイルとも cmp 全一致。
  （6）採番: 単一オーナー宣言（251523913cdc962c7f6d1eee581de9b641f0a866・15:49:05Z）が先着。
  K1157 はpush直前3点確認（knowledge README grep items/K1157- 0件・item path 404・recent commits 0件）で空き。
  本検証は残余23行のどの行も閉じない。第四幾何は8根被覆判定の被覆計画の簿記でありゲーム理論的証明書ではない。
  REFUTED-D10 は LOSS 証明ではない。nodes/solved数を勝敗として読まない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
---

## 詳細

単一オーナー宣言ノート（commit `251523913cdc962c7f6d1eee581de9b641f0a866`・2026-11-20T15:49:00Z・先行出版）の下で、
[K1156 第四幾何実験](../../experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/README.md)（出版 machine commit `3969a050`・監査 commit `7c21ad16`・2026-11-20T15:26Z）に
対して第三検証層を追加した: 出版byte 2 pin+入力3点の独立照合・出版機の pristine 再実行 4 回（PYTHONHASHSEED=random 隔離環境含む）の
全 byte 一致・1 byte tamper（出版社検査 offset 100 と異なる offset 200）の fail-closed 捕捉・第三検証 harness 自身の 3 実行監査 byte 一致、である。

本検証の個性は、K1156 の第四幾何が**行+2空き点という生成方法と4×4整数行列式24置換展開という安全性判定を、K1148 の第三幾何（3行組×8³向き和集合と3×3判定）と共有しない**点にある。
出版機の再実行は19,665生成事象と550,620個の6石子局面の計算を毎回新規に行い、8根の和集合・分類・共円四点座標が出版監査と bug-free に一致することを第4〜7環境相当で確定した。
K1147 8根被覆判定の第三検証は宣言 `887e594d`（15:21:00Z）の別レーン管轄で範囲外。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/README.md)・
[検証機](../../experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/scripts/verify_k1156_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/output/reexec-third-verification-audit-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification.md)・
[単一オーナー宣言](../../log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification-single-owner-note.md)。
