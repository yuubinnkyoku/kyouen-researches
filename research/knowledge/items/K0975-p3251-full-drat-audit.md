---
id: K0975
title: p=3251の全量DRAT監査が完了（drat-trim残り1541 d + 修正版サンプル84 d = 全1625 d）
kind: proposition
status: needs-review
topics: [maximum-safe, verification, search-methods]
aliases: []
relations:
- type: supports
  target: K0708
  note: 全数量化の残余1,541 dの監査証拠。K0708のdrat-trim全量監査を補完し昇格を可能にする
- type: depends_on
  target: K0334
  note: 等号 ⟺ あるdについてCNFが充足可能。したがって全1625 dのUNSAT証明で等号を否定
- type: depends_on
  target: K0707
  note: 修正版DRAT検証器の削除時代入失効の修正（本観測は修正版で実施）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_3251_92f0aa9575ed519d.json
  role: data
  note: drat-trimによる残り1,541 d全量の受理記録（全VERIFIED・d重複なし）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p3251-drat-full/progress.log
  role: source
  note: 全量監査の進捗記録とd=781 recheck修復の一次記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_3251_34249932790a9e9d.json
  role: data
  note: 先行監査済みサンプル84件（修正版増分チェッカー、別実装）
- path: research/log/2026-11-18-p3251-audit-completion-knowledge-omp.md
  role: source
  note: 監査完了記録とK0708昇格ドラフト
scope: 奇素数p=3251のDRAT監査の被覆。drat-trimの健全性の一般証明を含まない。
evidence: progress.log 1,541行VERIFIED（SAT 0・UNKNOWN 0）と集約JSON 1,541レコード全VERIFIEDが一致。先行サンプル84件と合わせ1,625全d被覆。unknown.json不存在。d=781の0バイト領収書はrecheckで同一proof_gz_sha256 (9b00b701…)を再現し修復。
---

## 観測内容

p=3251（h=1625）の全量DRAT監査が2026-11-18 12:07 JST (03:07 UTC)にALL DONEした。

1. 先行監査済みサンプル84 d（修正版増分チェッカー、checkerソースSHA-256 `34249932790a9e9d…`、別実装）。
2. 残り1,541 dをdrat-trim（checkerバイナリSHA-256 `92f0aa9575ed519d…`）で監査し、**VERIFIED 1,541・SAT 0・UNKNOWN 0**（`drat_trim_audit_full_3251_92f0aa9575ed519d.json`、dは1,541件ともユニーク）。合わせて**1,625 全 d 被覆**。

## 品質記録と注意

- チェーンALL DONE時点でd=781のper-d領収書のみ0バイトだった（VM再起動で書き込み途中に中断）。2026-11-18に`--ds 781 --recheck`で再solveを実施し、同一の`proof_gz_sha256`（9b00b701…）を再現、領収書とdrat-trim.logが正常再生成、progress.logも1,541行VERIFIEDとなった。
- 集約JSONのd=781レコードが「チェーン完了時点で既に存在した」ことは進捗記録からは直接確認できない。修復後の集約レコードはrecheck実行のものと一致する。
- 本観測はdrat-trimの一般健全性の証明ではない。また`A(3251)`の正確な値は未確定のまま。
