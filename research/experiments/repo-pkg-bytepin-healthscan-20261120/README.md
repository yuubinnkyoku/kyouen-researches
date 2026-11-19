# repo-pkg-bytepin-healthscan-20261120

knowledge.yml に登録された全「監査再実行 + audit.jsonへの `git diff --exit-code`」ステップについて、**検証器のbyte-pin健全性**（コミット済み検証器の実SHA-256と、audit.jsonが刻む自己参照pin `verifier_sha256` の一致）を一括スキャンした。単一オーナー宣言ノートは `research/log/2026-11-20-repo-pkg-bytepin-healthscan-single-owner-note.md`（commit 353aba77）。

動機: K1079がK1076パッケージ（z17-y4）でこの不整合を検出（pin主張388e1a47 vs 実a7878b8e）したのと同種の失敗モードを、本レーンが着手前検査でK1078（z18-y3）でも検出したため、同モードをrepo全体で系統掃引した。

## 結果（commit pin `353aba77fa6e7b99d462a0605af6c9422379bcd1` の時点）

機械可読正本: `output/pkg-bytepin-healthscan-20261120.json`（SHA-256 `0993292a03c4313411b543a92e3665fc5b72d99a7d8f74849953e9be978ebf23`・同じcommit pinに2回実行＋別cwd別プロセスでbyte-identical・fetchのみで探索・再実行なし）

- **監査ステップ総数: 124**（fetch失敗0・パース失敗0・未解析0）
- **verifier pin方式別**:
  - `verifier_sha256` 自己参照pinなし（`sha256_without_hash_field` 型・内容ハッシュで自己参照を回避）: **82** — この失敗モードには構造的に影響しない
  - `verifier_sha256` 自己参照pinあり・実検証器と一致: **37**
  - `verifier_sha256` 自己参照pinあり・**不一致: 5**

### 不一致5パッケージ（actual = 実在検証器のSHA-256 / claimed = audit.jsonのpin）

| package | actual | claimed | 備考 |
|---|---|---|---|
| vertical-fiber-t2-q12-grundy-20261118 | 516d85fe… | 51f133ae… | 本レーン再生検証 |
| vertical-fiber-two-token-z11-y3-boundary-20261119 | 2eab05bb… | a68bc68d… | 本レーン再生検証 |
| vertical-fiber-two-token-z11-y4-boundary-20261119 | 96c42327… | 395ac8da… | 本レーン再生検証 |
| vertical-fiber-two-token-z17-y4-boundary-20261120 | a7878b8e… | 388e1a47… | K1079が検出済み・再生検証済み |
| vertical-fiber-two-token-z18-y3-boundary-20261120 | 4fecbd21… | b7d14660… | **本レーンが新規検出** |

### 重要: 全5件とも「benign pin rot」であることを確認

本レーンは上記5件のうち4件（新規検出のz18-y3・z11-y3・z11-y4・t2_q12）について**コミット済み検証器をそのまま実行**し（rc=0・それぞれ13秒〜数十秒）、再生されたaudit.jsonが**コミット済みaudit.jsonと `verifier_sha256` の1行だけ違い他の全行がbyte一致**することを確認した。z17-y4の再生（12,693,293照合・bad空）はK1079が実施済み。すなわち:

- 監査の**数学的内容はコミット済み検証器で完全に再現する**（控除されるのは自己参照pin行のみ）
- 不一致の実体は「audit生成後に検証器へ最終微編集（転写修正・コメント等の非出力系変更）が入ったが、auditの自己hashは編集前版のまま」型のpin rotである
- 影響: 各パッケージのCI監査ステップ（検証器再実行→`git diff --exit-code`）は**現mainでは原理的に落ちる**。計算内容・定理への影響はない
- 修正は各パッケージのオーナーレーン管轄: (a) 検証器をpin主張版のbytesへ戻す（K1076/K1077の「Pin … to exact audited bytes」方式）、または (b) 現行検証器でauditを再生成してpin行を更新し、report/item内の該当pin指摘も更新する。数学的内容は不変

本スキャナは任意のcommit pinに対して決定的に実行できるため、「監査生成後に検証器が微編集されてコミットされた」パターン（K1076/K1077/K1078で実際に起きた）を将来の任意時点で一括再検出できる。

## 再現手順

```sh
python3 scripts/pkg_bytepin_healthscan_20261120.py <commit_sha> [out.json]
```

出力はcommit pinのみの純関数（ネットワークfetch・探索・監査再実行なし・タイムスタンプなし）。同じpinで2回実行＋別cwd別プロセスでbyte-identicalであることを要求。

## 解釈境界

- 本スキャンはCI再現性・pin健全性の検出であり、**数学的健全性の主張ではない**（中身の再現は本README記載の個別検証器実行による）。
- 修正は各パッケージのオーナーレーンの管轄であり、本レーンは実施しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
