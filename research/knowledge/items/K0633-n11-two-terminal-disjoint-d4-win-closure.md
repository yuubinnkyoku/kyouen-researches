---
id: K0633
title: 11×11の二つの独立終局戦略から444,570正準WIN類を証明、閉包間の交差と相乗増分は0
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイの合法手
- type: depends_on
  target: K0003
  note: 局所WIN証明と空盤勝敗の区別
- type: depends_on
  target: K0626
  note: 第一の六石終局戦略
- type: depends_on
  target: K0628
  note: 第二の六石終局戦略
- type: depends_on
  target: K0630
  note: 第二終局戦略のD4帰納閉包
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_55_strategy.b64
  role: certificate
  note: 第一の固定終局戦略（復号12,068バイト）
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_60_strategy.b64
  role: certificate
  note: 第二の固定終局戦略（復号14,440バイト）
- path: research/experiments/n11-central-19-cover-20261031/verify_two_terminal_joint_d4_closure.cpp
  role: verifier
  note: 両証明書の独立整数幾何再生と三種類のD4帰納閉包の集合比較
- path: research/experiments/n11-central-19-cover-20261031/verify_two_terminal_joint_d4_closure.py
  role: verifier
  note: 固定SHA・件数・改変拒否試験とC++検証器の実行
- path: research/log/2026-11-02-n11-two-terminal-joint-d4-closure-444570-disjoint.md
  role: log
  note: 有限計算の結果、相乗増分が0であること、証明境界
scope: 標準11×11完全指摘・通常プレイ。二つの固定六石元先手WIN終局戦略が訪れる局面を種とする、D4正準化済みの石数降順AND/OR帰納閉包。
evidence: 二つの固定終局戦略を独立4×4整数行列式で全終局まで再生し、各単独閉包と同時閉包を再計算。第一187826類、第二256744類、両閉包の交差0、同時閉包444570類、相乗増分0。専用CI初版41392709384で成功。
---

# 二つの終局戦略を合わせて444,570正準WIN類

第一の固定終局戦略から**187,826類**、第二の固定終局戦略から**256,744類**の元先手WINをD4正準化済みの帰納規則で証明した。二つの証明済み集合は**交差0類**であり、和集合は**444,570類**。両集合を同時に種として再帰納しても**444,570類のまま**で、追加の相乗証明は0類だった。

検証器は各戦略を独立した4×4整数行列式の合法手生成で終局まで再生し、偶数石では少なくとも一つのWIN子、奇数石ではすべての合法子がWINという帰納規則を石数降順で適用する。第一のみ・第二のみ・両方を種とした三つの集合を実際に構成し、単独集合が合成集合に含まれることと差分0を照合する。固定SHA-256・長さ・各層の件数・改変拒否も検査する。初版の独立GitHub Actions [41392709384](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41392709384) は成功。固定件数回帰を加えた最新版の監査結果は別途確認する。

石数6〜19の証明済み類数は `14, 2, 603, 74, 19988, 2178, 221549, 22068, 157135, 14856, 5643, 440, 19, 1`。新規六石・七石正準類はなく、六石14類・七石2類は既存の二つの戦略から得られる局所証明の合計である。

これは**固定された二つの終局戦略の有限帰納閉包**であり、11×11の全WIN類数ではない。勝敗cache、未完探索のpn/dn、条件付きLOSS証人を勝敗証拠に使っていない。六石LOSS・四石LOSS・二石root閉鎖は新規0件。**標準11×11空盤の勝敗はUNKNOWN。**
