---
id: K1084
title: 残余72行36-root三手先D4 frontier censusの独立第二検証
kind: verification
status: verified
topics: [search-methods, verification, statistics]
aliases: [36-root three-ply frontier second verification, residual72 D4 overlap census]
relations:
- type: verifies
  target: K1075
  note: K1075 witness_fullの36 rootについて、安全性・残余行incidence・三手先D4重複censusを別実装で再導出。phase-2 verdict join自体は再構築しない
artifacts:
- path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-20261120/output/independent-second-verification-20261120.json
  role: data
  note: 正本SHA-256 a6272056…・19/19 gate PASS・全per-root表と221共有組が先行censusと一致
- path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-20261120/scripts/verify_frontier.py
  role: verifier
  note: Python標準ライブラリのみ・整数外積/内積による独立判定・元JavaScriptをimportしない
- path: research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-20261120/README.md
  role: source
  note: 方法・全数値・限界・再現コマンド
- path: research/log/2026-11-20-n11-residual72-36root-three-ply-frontier-second-verification.md
  role: log
  note: 独立第二検証の着手判断・結果・解釈上の限界
scope: >-
  K1075の残余72行を1回被覆する36本のfresh-safe 7石rootについて、root安全性・D4正準形・D4像から
  1石除去した残余行incidence、およびrootからの合法な1・2・3手局面を整数演算で全列挙し、
  9石/10石の個数、root別D4類、root間の全pairwise overlap、roots[W::4]のworker別集計を
  先行三手先censusと独立照合する。
evidence: >-
  19/19 gate PASS。132,291個の三点組と16,007,211回の点判定を整数外積/内積で再計算。
  36 root・1,260安全性四点組・72 residual-row incidenceを再導出し、9石56,597、
  raw 10石733,855、root別D4 membership 733,800、root内併合55、全体D4類728,370、
  重複membership 5,430（0.739984%）、pairwise overlap 5,435/221組、worker境界重複
  4,193/5,435（77.148114%）を完全一致で再現。全per-root表・全221共有組・4 worker集計も
  一致。別cwd・別プロセス2回で正本byte-identical（SHA-256 a6272056…）。
---
## 命題と範囲

本項は有限の幾何censusに対する独立第二検証であり、ゲーム理論的勝敗の証明ではない。K1075の
candidate universeやphase-2 verdict joinを再構築したものではなく、公開済みwitness_fullの36 rootを
入力として、その幾何・三手先状態重複だけを検査した。

## 限界と解釈規約

同一D4類の共有は実DFPNの同一深さ・同一証明境界・再利用可能な表状態を意味しない。表命中率や
探索節点削減率は未測定。REFUTED-D10はLOSS証明ではない。36-root sweepは別レーンの管轄であり、
本項は判定・証明書・receipt・行の閉鎖を一切追加しない。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。
