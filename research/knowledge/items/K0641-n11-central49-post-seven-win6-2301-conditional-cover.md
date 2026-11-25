---
id: K0641
title: 11×11中央49の七つの確定WIN6を除外した条件付き六石被覆は七石2,301類
kind: computation
status: superseded
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘ルールと安全な追加
- type: depends_on
  target: K0003
  note: 条件付き幾何被覆と実際の勝敗証明を区別
- type: depends_on
  target: K0624
  note: 共有七石から導いた元先手WIN6
- type: depends_on
  target: K0627
  note: 第一終局戦略の七親WIN6
- type: depends_on
  target: K0628
  note: 第二終局戦略の七親WIN6
- type: depends_on
  target: K0640
  note: K0638の七石WINから導いた七親WIN6
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_repair_2301.json
  role: certificate
  note: 旧46証人からの除外七類・追加七類、被覆と七石義務の計数
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_post_seven_win6_repair_2301.py
  role: verifier
  note: 旧18置換の再生と4×4整数Bareissによる新証人の合法七石子・既知WIN非衝突監査
- path: .github/workflows/n11-central49-post-seven-win6-repair-2301.yml
  role: source
  note: 独立監査CI、実行41443189538成功
- path: research/log/2026-11-02-n11-central49-seven-win6-exclusion-and-2301-repair.md
  role: log
  note: 旧1,980計画の失効と修復の探索過程・検証境界
scope: 標準11×11・二石{49,60}・中央49の優先四石00000000000000003800800000000000から生じる94五石類を、46六石LOSS候補で被覆する条件付き計画。六石LOSSや二石rootの証明は含まない。
evidence: 旧1,980七石計画の46六石証人から、終局戦略に基づくWIN6七類を除外し、残る39類に七類を追加。4×4整数Bareissによる全合法七石子再計算で五石94/94被覆、六石46類、合法七石辺2,992本、相異なる七石2,301正準類、既知WIN6 145類・WIN7 23類との衝突0。専用CI 41443189538成功。
---

# 旧1,980類計画の七つの反証を除いた条件付き修復

> **2026-11-03更新：** この2,301類計画は、K0646の2,154類・46証人計画に置き換えられた。以下は当時の有効な幾何証明として保存する。勝敗証明ではない。

歴史的な46六石証人・1,980七石類の被覆は、元先手WINと終局証明された六石を**七類**含む。従って幾何学的な94/94被覆が正しくても、46類すべてを元先手LOSSとして証明することは不可能だった。

K0624・K0627・K0628・K0640の終局戦略由来の六石WINと、旧19類WIN7からの117六石親を合わせた145類を除外して、旧証人から七類を交換した。

| 指標 | 旧計画（失効） | 新しい条件付き計画 |
| --- | ---: | ---: |
| 六石証人 | 46 | 46 |
| 五石被覆 | 94/94 | **94/94** |
| 終局証明由来の既知WIN6との衝突 | 7 | **0** |
| 合法七石辺 | 2,972 | **2,992** |
| 相異なる七石正準類 | 1,980 | **2,301** |
| 既知WIN7との衝突 | 未更新 | **0** |

新しい証人集合は `conditional_s6_cover_46_post_seven_win6_repair_2301.json` に固定した。独立監査器は旧18置換の出典と歴史的な七類の衝突を確認し、新証人七類を含む全46類の七石子を4×4整数Bareissで再計算する。**専用CI 41443189538成功**。

2,301類は七石の**条件付き証明義務**であり、LOSS7確定数ではない。七類交換は構成的な改善であって、最小性は証明していない。選択六石のLOSS、四石LOSS、二石root、空盤の勝敗はいずれも未証明。**標準11×11空盤はUNKNOWN。**
