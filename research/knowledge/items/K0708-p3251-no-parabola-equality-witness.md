---
id: K0708
title: p=3251でも剰余放物線の等号A(p)=(p+3)/2を達成できない（単一CNF独立schema・RUP/LRAT監査済み）
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 上界A(p)<=(p+3)/2と等号集合の完全対構造
- type: depends_on
  target: K0334
  note: 等号 ⟺ あるdについてsigned NAE3/4と原点節のCNFが充足可能（全奇素数で証明済み）
- type: supports
  target: K0706
  note: 2647に続く4例目
- type: supports
  target: K0101
  note: 単一CNFの独立監査により全奇素数での等号を否定する4番目の反例
- type: depends_on
  target: K0707
  note: 旧d別監査では削除時代入失効の修正版を使用。別経路の単一CNFはRUP限定検査と空節処理修正版LRATで再検査
artifacts:
- path: research/experiments/parabola-single-cnf-audits-20261110/check_case.py
  role: verifier
  note: 凍結したCardEnc非依存schemaを用いて単一CNFの構造・幾何・元DRATを検査
- path: research/experiments/parabola-single-cnf-audits-20261110/replay.py
  role: verifier
  note: 採用CNF・LRAT gzipの別処理実再生と全source・schema・幾何・証拠hash binding
- path: research/experiments/parabola-single-cnf-audits-20261110/output/p3251/schema.json
  role: manifest
  note: 11374変数・87888節を27622構造節と60266幾何節へ全分離した独立schema
- path: research/experiments/parabola-single-cnf-audits-20261110/output/p3251/geometry.json
  role: data
  note: 全60266提供辺をgeneric整数4x4行列式で禁止四点と確認
- path: research/experiments/parabola-single-cnf-audits-20261110/output/p3251/rup.json
  role: data
  note: 元229866行DRATを固定DRAT-trim -UでRUP限定受理
- path: research/experiments/parabola-single-cnf-audits-20261110/output/p3251/lrat.json
  role: data
  note: 抽出44623行LRATを空節処理修正版の別C実装で受理
- path: research/experiments/parabola-single-cnf-audits-20261110/output/p3251/manifest.json
  role: manifest
  note: 上界1626の採用CNF・LRAT gzipと元DRATの所在、raw・gzip hashと検査器source hash
- path: research/experiments/parabola-single-cnf-audits-20261110/output/replay-p3251.json
  role: data
  note: 圧縮CNF・LRATの実再生と全bindingの照合に成功
- path: research/experiments/parabola-single-cnf-audits-20261110/regression.py
  role: verifier
  note: 両実入力と10件のschema改変・素数取り違えを制御
- path: research/experiments/parabola-single-cnf-audits-20261110/output/regression.json
  role: data
  note: 凍結schemaの既存意味検査bindingと、新しい10負例の拒否
- path: research/experiments/parabola-single-cnf-audits-20261110/README.md
  role: source
  note: 単一CNFで全h+2点集合を排除する論理、保存証拠再生と旧d別監査との区別
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3251-1627/receipt.json
  role: certificate
  note: サイズ1627（クラス(1,1,0)）の単一CNFがUNSAT、DRAT証明229,866行を修正版検証器でVERIFIED（185.6秒）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-3251-1627/a3251_1627.drat.gz
  role: certificate
  note: 上記のDRAT証明（gzip、SHA-256はreceipt.json）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_3251.json
  role: data
  note: d=1625..1の全数走査（UNSAT 1625・unknown 0・SAT 0、4,694秒）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/scan_mp.py
  role: verifier
  note: マルチプロセス衝突予算スキャナ（4並列、dごとに独立なCNF）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_3251_34249932790a9e9d.json
  role: data
  commit: 87e28af3c927d640bde3fbc8a20238efc30bccb8
  note: 修正版の受理記録70 d。計画標本は51/65、全1625 dの監査ではない
- path: research/experiments/parabola-audit-coverage-20261109/inventory.json
  role: data
  note: 固定commitで修正版70/1625 d、計画標本の未被覆14 dを特定
- path: research/experiments/parabola-audit-coverage-20261109/inventory.py
  role: verifier
  note: 総件数70と計画標本51/65の被覆を区別する再現コード
- path: research/log/2026-11-09-drat-reaudit-status-omp.md
  role: source
  note: HEAD時点の修正版再監査の確定状態（3251は84/1625、計画標本65/65完了）
scope: 奇素数p=3251のQ_p、標準q=4、等号A(p)=(p+3)/2の不達成。他素数への一般化は主張しない。
evidence: 別経路のサイズ1627単一CNFを27622構造節と60266真の禁止四点へ独立照合し、元DRATをRUP限定検査・空節処理修正版LRATで受理した。採用CNF・LRAT gzipの別処理実再生と全bindingも成功し、A(3251)<=1626を有限計算として独立監査済み。旧d別の修正版被覆84/1625は履歴として維持する。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 3251 では
`A(3251) < (3251+3)/2 = 1627`**（すなわち `A(3251) <= 1626`）。
K0693（2207）、K0702（2531）、K0706（2647）に次ぐ**4例目の等号不達成**であり、
K0101 の「全奇素数で等号」に対する四つ目の反例である。`A(3251)` の正確な値は未確定。

## 単一CNFによる独立監査（2026-11-10）

全1627点安全集合は原点あり・完全対一つ・空対なしの形に限られる。
保存11374変数・87888節のCNFを、探索builderやCardEncを使わない凍結schemaへ全照合した。
構造27622節と幾何60266節に全分離し、全提供幾何節をgeneric整数4x4行列式で禁止四点と確認した。
任意の安全1627点集合から対状態・点選択・BOTH prefix ORでCNFモデルを作れるため、辺集合の完全性は排除に不要である。

元229866行DRATを固定DRAT-trim -Uで受理し、抽出44623行LRATを空節処理修正版の別C実装で受理した。
Git管理する採用CNF・LRAT gzipの別処理での実再生と全bindingも成功した。
したがって安全1627点集合は存在せず、A(3251)<=1626である。旧d別全数監査の完了とは扱わない。

## 根拠

1. サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` と一つの完全対 `{d,p-d}` と他の各対の一側に限られ
   （K0097 の上界証明から初等的に従う）、K0334 が等号を「ある `d` について signed NAE3/4 と
   原点節の CNF が充足可能」と全奇素数で同値に還元している。
2. `scan_mp.py`（マルチプロセス、衝突予算 20 万、4 並列）で **d = 1625..1 の全 1625 個**を走査し、
   **UNSAT 1625・SAT 0・不明 0**（`output/deep_scan_3251.json`、4,694 秒）。
3. この素数は「浅い走査で 6 個の d がすべて UNSAT 証明済み（タイムアウト 0）で証人なし」という
   2026-11-08 の交絡訂正で導入した基準で選ばれた候補であり、2647 に続いて同基準から確定した。

## 限界

- commit `87e28af3c927d640bde3fbc8a20238efc30bccb8` の修正版検査器
  （ソースSHA-256 `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`）の
  受理記録は重複のない70 d。全件UNSAT・終了コード0・出力VERIFIEDだが、全1625 dのうち1555 dは未被覆。
  計画標本 `d=1,26,...,1601` も51/65であり、総件数が65を超えていても標本完了ではない。
  このsnapshotの未被覆標本は `d=1276,1301,...,1601` の14件。
  追記（2026-11-09）: その後レシートはHEAD `a0fcb1f` 時点で84 dまで追記され、
  計画標本 `d=1,26,...,1601` は65/65完了した（残りは標本外の1541 d）。
  現況の確定は [再監査ステータスログ](../../log/2026-11-09-drat-reaudit-status-omp.md) を参照。
- inventoryは保存レシートの整合性・被覆を検査したもので、今回DRATを再生していない。
  旧d別全数監査は未完了だが、現在の本項は別経路の単一CNF監査により `computed` とする。
  検査器・コンパイラ依存は残り、一般健全性やLean形式証明ではない。
- K0693/K0702でも旧版と修正版の受理記録を区別する。K0101は全数監査済みのK0706により反証済み。
- `A(3251)` の正確な値は未確定。
