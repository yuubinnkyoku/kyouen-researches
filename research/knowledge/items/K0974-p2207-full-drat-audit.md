---
id: K0974
title: p=2207の全1,103 dのDRAT証明が独立checker drat-trimで監査済み（全件VERIFIED）
kind: proposition
status: computed
topics: [verification, search-methods]
aliases: []
relations:
- type: verifies
  target: K0693
  note: p=2207の全d UNSAT主張に対する独立DRAT監査。昇格条件を満たす
- type: depends_on
  target: K0707
  note: 旧増分DRATチェッカーの偽受理(SAT偽UNSAT)発見に起因する再監査・checker分離の方針
- type: depends_on
  target: K0724
  note: assumptionベースDRATとUNSATのgap方針（本監査はassumptionを使わない単一CNF証明を検査）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_2207_92f0aa9575ed519d.json
  role: data
  note: 集約領収書。records 1,082件、全件 verdict=VERIFIED。d=2..1102（標本21件との和集合で全1,103 d）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py
  role: verifier
  note: 再起動耐性のある全量監査ドライバ（W31構築、pilot d=2..6 全件VERIFIED）。領収書方式で再実行を冪等にする
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207-drat-full/progress.log
  role: source
  note: 全量監査ドライバの進捗記録（verdict行1,082、VERIFIED以外0）。per-dのinput.cnf.gz・proof.drat.gz・receipt.json・drat-trim.logはローカル保持
- path: research/log/2026-11-18-p2207-audit-completion-knowledge-omp.md
  role: source
  note: 本監査の完了記録とK0693昇格ドラフト
scope: p=2207（h=1103）・標準q=4構成のd=1..1103各CNFについてのDRAT証明の受理。checkerの一般健全性や他素数への一般化は主張しない。
evidence: drat-trim（binary sha256 92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a、source commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985）で1,082 dを検査し全件VERIFIED（SAT 0・UNKNOWN 0）。標本21件（d={1,50,100,150,200,250,289,297,300,312,324,400,500,550,600,700,800,900,1000,1100,1103}）は修正版増分チェッカー（source sha256 34249932790a9e9d…）で全点VERIFIED（2026-11-09）。和集合で全1,103 d、両checkerのd集合は重複0。progress.log最終行 2026-11-17T19:15:29+0000（JST 2026-11-18 04:15）driver done。
---

## 命題

p=2207（h=1103）の等号否定CNF（各dについて `clauses_for_pair(2207, edges, d)` で生成、節数31,868、edges sha256 d1eb1385…）に対し、dごとのDRAT UNSAT証明が独立checker drat-trimで1,082件すべて受理され（`s VERIFIED` かつ exit 0）、先行の標本21件（修正版増分チェッカー）と合わせて全1,103 dが監査済みである。

## 意味と限界

- 各VERIFIEDは「そのCNFについて、そのDRAT証明がdrat-trimにUNSAT証明として受理された」ことのみを意味する。UNKNOWNはUNSATではない（今回はUNKNOWN 0件）。SAT・checker異常も0件。
- solver（cadical）は証明生成にのみ使われ、検査はdrat-trimが行う（checker/solver分離）。
- 有限事例の監査であり、checkerの一般健全性、他素数・他構成への一般化は主張しない。
- この結果は K0693 の幾何命題（`A(2207) <= 1104`）の昇格条件を満たすが、`A(2207)` の正確な値（1104かそれ未満か）は確定させない。
