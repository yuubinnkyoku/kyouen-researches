---
id: K0658
title: 11×11中央49の2,090七石条件付き計画は既知の終局WIN6を再選択しており失効
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0105
  note: 1984計画の六石WIN終局戦略とその独立検証
- type: depends_on
  target: K0644
  note: 現行幾何計画で再利用した六類の終局LOSS7証明
- type: refutes
  target: K0654
  note: 2,090類の幾何計数は正しいが46六石すべてをLOSSとして閉じる計画は不可能
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/audit_2090_known_win6_refutation.py
  role: verifier
  note: 2090の46証人を再生し、SHA固定1984 WIN6終局戦略を4×4整数行列式で独立再検証
- path: research/experiments/n11-central-19-cover-20261031/verify_focus_s6_win_strategy.py
  role: verifier
  note: 六石元先手WINの全合法応手・全終局を独立検査
- path: research/experiments/n11-central-19-cover-20261031/focus_s7_worker_2090.py
  role: source
  note: 失効済み2090計画の新規配布・直接監査・直接統合を拒否
- path: .github/workflows/n11-central49-2090-win6-refutation.yml
  role: source
  note: 独立再検証CI 41543737197成功
- path: .github/workflows/n11-central49-2090-focus.yml
  role: source
  note: 失効済み計画の配布拒否回帰
- path: research/log/2026-11-03-n11-central49-2090-missed-1984-win6-refutation.md
  role: log
  note: 既知WIN6の除外漏れ、反証、検証境界と修復方針
scope: 標準11×11・完全指摘・通常プレイ。中央49の94五石類を46六石LOSS候補で被覆する旧K0654の2,090七石条件付き計画の有効性。二石rootと空盤勝敗は対象外。
evidence: 2090の独立幾何再生で46六石・2,983合法七石辺・2,090正準七石類・既存終局LOSS7六類を確認。46証人中にK0105で既に終局WINと証明された六石00000000000000603800000000008000が含まれる。固定SHA-256 390554902426c5876b9742edb4219cae13648e103d6310d4f94b9d690ea4e63eの戦略を別実装4×4整数Bareissで再生し、元先手の5923手番選択・到達8949局面・奇数石終局951件・初手20を検証。CI 41543737197成功。元先手WIN6は元先手LOSS6の証人になれないため、2090計画は失効。2,090という幾何学的計数や局所交換監査そのものを反証したわけではない。
---

# 2,090類の条件付き計画に、既に反証済みの六石が再混入

K0654の46六石証人を再生すると、次の正準六石が含まれていた。

`00000000000000603800000000008000`

これはK0105に記録された、**元先手WIN6が終局まで独立検証済みの局面**である。元先手は点20に置き、その後の全合法応手に勝つ。戦略の固定SHA-256を照合したうえで4×4整数Bareissによる全分岐再生を行い、5,923手番選択、8,949到達局面、951終局（すべて元先手勝ち）を再確認した。専用CI [41543737197](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41543737197) は成功。

根本原因は、旧1,984類計画を失効させたこのWIN6を、後の `comparison_inventories()` が作る145類の既知WIN6除外集合へ継承していなかったこと。修復済み2,301類から2,090類への交換系列では、集合に含まれないこのWIN6を再選択できてしまった。**「既知WIN6との衝突0」という旧主張は、その145類の不完全な集合に関するものに限られる。**

旧2,090類の七石義務数・最大三証人交換の局所最適性は、**固定された幾何集合に関する計算結果としてのみ**残る。全46六石をLOSSとして証明する計画としては無効である。旧集中配布器は新規配布・直接統合を拒否するよう変更した。

有効な後継計画は、少なくともこのWIN6を除外し、終局証明由来のWIN6を**146類以上**として再監査する必要がある。修復計画の完成・六石LOSSの新規証明は別問題である。

**四石LOSS・二石局面{49,60}・標準11×11空盤の勝敗はUNKNOWN。**
