---
id: K0708
title: p=3251でも剰余放物線の等号A(p)=(p+3)/2を達成する証人が存在しない（4例目）
kind: proposition
status: needs-review
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
  note: 全奇素数での等号を否定する4番目の反例候補
- type: depends_on
  target: K0707
  note: DRAT検証器の削除時代入失効の修正。本項の修正版監査は一部dのみ
artifacts:
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
evidence: 全1625 dでCNF UNSAT（cadical、衝突予算20万、unknown 0）。修正版の固定commitには70 dのDRAT受理記録があり、計画標本は51/65。その後のHEADでは84 d（計画標本65/65完了）まで追記。全数監査は未完了。
---

## 命題・範囲

`Q_p = {(t, t² mod p)}` の安全集合の最大を `A(p)` とすると、**p = 3251 では
`A(3251) < (3251+3)/2 = 1627`**（すなわち `A(3251) <= 1626`）。
K0693（2207）、K0702（2531）、K0706（2647）に次ぐ**4例目の等号不達成**であり、
K0101 の「全奇素数で等号」に対する四つ目の反例候補である。`A(3251)` の正確な値は未確定。

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
  全数監査未完了のためstatusは `needs-review`。検査器の一般健全性の証明でもない。
- K0693/K0702でも旧版と修正版の受理記録を区別する。K0101は全数監査済みのK0706により反証済み。
- `A(3251)` の正確な値は未確定。
