---
id: K0869
title: p=2647 サイズ1322 の3形状クラス (0,0,1),(1,0,2),(0,1,2) は DRAT 監査済み
kind: verification
status: verified
topics: [maximum-safe, geometry, verification, certificates]
aliases: []
relations:
- type: verifies
  target: K0711
  note: 上界 A(2647)<=1322 のうち (1,1,3) を除く3クラスのソルバUNSAT主張
- type: depends_on
  target: K0771
  note: 禁止四点生成器の完全性（CNF構築の前提）
- type: depends_on
  target: K0706
  note: 同じ増分DRATチェッカーによる全1323 d監査の流儀
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/w20_drat_1322.py
  role: solver
  note: クラスごとに再開可能な solve+DRAT+監査ドライバ（Cadical195 with_proof）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-001/audit.json
  role: data
  note: (0,0,1) 増分チェッカー VERIFIED, returncode 0, 8.11秒。checker source/binary hash 付き
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-001/drat-trim-audit.json
  role: data
  note: (0,0,1) drat-trim クロスチェック VERIFIED, exit 0, 0.425秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-102/audit.json
  role: data
  note: (1,0,2) 増分チェッカー VERIFIED, 982.81秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-102/drat-trim-audit.json
  role: data
  note: (1,0,2) drat-trim クロスチェック VERIFIED, 4.998秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-012/drat-trim-audit.json
  role: data
  note: (0,1,2) drat-trim 単独監査 VERIFIED, 249.726秒（増分チェッカーは3600秒タイムアウト）
- path: research/log/2026-11-12-a2647-1322-drat-audit-omp.md
  role: log
  note: 方法・経緯・(drat-trim切替理由)・留保
scope: p=2647、size=1322 の形状クラス (x,c,e)=(0,0,1),(1,0,2),(0,1,2) の単体CNF。各CNFの UNSAT 判定の独立DRAT監査に限る。クラス (1,1,3) と A(2647) の正確値を含まない。
evidence: 各クラスの CNF/proof の SHA-256 を JSON と照合し、増分チェッカー2クラス・drat-trim3クラスが exit 0 と VERIFIED を返した。CNF/proof のバイト列は再生成可能（gz は mtime=0）。
---

## 検証内容

A(2647) <= 1322 を支える size-1322 の全4形状クラスのうち、(1,1,3) を除く3クラスについて、
Cadical195（with_proof）で UNSAT 判定と DRAT 証明を生成し、独立チェッカーで検査した。
証明は `output/w20-drat-1322/class-*/` に proof.drat.gz、CNF は input.cnf.gz として保持する
（バイナリのため push 対象外。SHA-256 は JSON に記録）。

- (0,0,1): 増分チェッカー `drat_check_incremental` VERIFIED（8.11秒）、
  drat-trim VERIFIED（0.425秒）。
- (1,0,2): 増分チェッカー VERIFIED（982.81秒）、drat-trim VERIFIED（4.998秒）。
- (0,1,2): 増分チェッカーは 3600 秒でタイムアウト（`timed_out: true`, `verified: false`）。
  drat-trim 単独で VERIFIED（249.726秒、exit 0）。このクラスは両チェッカーで検証したのではなく、
  drat-trim のみが領収書である。

drat-trim の backward checking はいずれも RAT lemmas in core 0（全 lemma が RUP で core に入る）。
CNF・証明の SHA-256 は audit.json / drat-trim-audit.json の記録と一致することを確認済み。

## 限界

- (0,1,2) は増分チェッカーでは未検証（タイムアウト＋VM再起動中断のみ）。領収書は drat-trim 単独。
- クラス (1,1,3) は対象外で未解決。UNSAT なら A <= 1321、SAT なら A = 1322。
- 証明バイナリは push 対象外。JSON の hash からバイト単位で再生成可能であることが前提。
- チェッカー実装（増分チェッカー、drat-trim）とコンパイラへの依存が残る。Lean 形式証明ではない。
