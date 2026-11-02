---
id: K0642
title: 11×11中央49の現行2,301七石義務には終局証明済みLOSS7が4類含まれる
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 合法手と安全な局面の定義
- type: depends_on
  target: K0003
  note: 条件付き幾何被覆と勝敗証明の区別
- type: depends_on
  target: K0637
  note: 元先手LOSS7五類の固定終局戦略と独立監査
- type: depends_on
  target: K0641
  note: 現行46六石証人と2,301七石正準類の条件付き被覆
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_post_seven_win6_repair_2301.py
  role: verifier
  note: 旧18交換を再生して現行46証人の七石子を独立4×4整数Bareissで構成しK0637の五根と照合
- path: .github/workflows/n11-central49-post-seven-win6-repair-2301.yml
  role: source
  note: 現行被覆と終局LOSS7四類・四辺の監査用CI
- path: research/log/2026-11-02-n11-central49-k0637-terminal-loss7-overlap-current-2301.md
  role: log
  note: 五つのK0637根からの六石親照合、四類の再利用と信頼境界
scope: 標準11×11中央49の現行K0641条件付き46六石証人・七石2,301正準類と、K0637の元先手LOSS7終局証明五類の交差。六石LOSS・二石root・空盤勝敗は対象外。
evidence: 旧18交換と七WIN6除外・七証人追加を再生した現行46六石から、4×4整数幾何で七石子を再計算し、K0637の五つの終局証明済みLOSS7正準鍵と照合。交差4類・合法辺4本・親六石2類、計画外の確定LOSS7は1類。K0637の勝敗証明を再実行したものではなく、その既存証明の現行被覆への再利用。
---

# 旧計画で証明された七石LOSSは現行2,301類のうち4類に残る

K0637は旧1,985類の七石条件付き計画内の五つの七石局面について、元先手LOSSを固定終局戦略で独立検証した。その後、旧計画の六石証人がWINと判明して失効し、K0641で新しい46六石証人・2,301七石義務へ修復された。

現行46証人の七石子集合とK0637の五つの確定LOSS7との交差は、**4正準類・4合法辺**。五つのうち一つは現行計画に含まれない。四つの七石子は二つの選択六石証人に各二つずつ対応する。

| 指標 | 確定した値 |
| --- | ---: |
| 現行七石義務 | 2,301正準類 |
| K0637の終局証明済みLOSS7との一致 | **4正準類** |
| 一致する六石→七石辺 | **4本** |
| 一致する現行六石証人 | **2類** |
| K0637五類のうち現行被覆外 | 1類 |
| K0637だけでは証明されていない現行七石義務 | **2,297正準類** |

旧計画の「5類・8辺」を現行計画にそのまま引き継ぐことは誤り。今回の4類・4辺は現行証人を復元して再計算した値であり、`verify_central49_post_seven_win6_repair_2301.py` と専用CIに固定した。七石の勝敗根拠はK0637の独立終局検証に依存する。今回の照合だけで新しい七石勝敗を証明したわけではない。

残り2,297類は「K0637の五つの終局証明によっては被覆されない」という意味に限る。他の証明・cacheを統合した厳密な未確定数ではない。選択六石LOSS・四石LOSS・二石rootは未閉鎖。**標準11×11空盤はUNKNOWN。**
