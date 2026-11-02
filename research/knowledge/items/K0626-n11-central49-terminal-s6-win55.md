---
id: K0626
title: 11×11中央二石系の六石一類は元先手WIN、旧2,089七石条件付き証人は反証
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイの合法手と終局規則
- type: depends_on
  target: K0003
  note: 六石局面の局所的勝敗と空盤弱解決の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_55_strategy.b64
  role: certificate
  note: 深さ優先で初めて訪れた元先手手番局面の着手列12,068バイトをzlib/base64圧縮、復号SHA-256 83bdd3c89555bd80eadae802d47a8dc8289f0aee1a935440fb325f7f9ce25b2b
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_55_compact.py
  role: verifier
  note: 独立4×4整数行列式と相手全合法応手の再生、改変拒否4件
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_55_strategy_generator.cpp
  role: solver
  note: 3×3差分整数行列式で決定的戦略を生成、独立検査器とは別実装
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_after_terminal_s6_55_repair_2097.json
  role: manifest
  note: 新たに確定した七類のWIN6を除いた条件付き46証人・2,097七石類、66組の非衝突二対二修復、選択六石のLOSSは未証明
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_55_repair_2097.py
  role: verifier
  note: 固定44証人の二対二置換68組と七石子を4×4整数行列式で独立監査
- path: research/log/2026-11-02-n11-central49-terminal-win6-55-and-repair-2097.md
  role: log
  note: 新規WIN6・旧条件付き計画の反証・修復の経緯と検証境界
scope: 標準11×11完全指摘・通常プレイの六石正準局面00000000000200801002000081000000の元先手視点。中央二石{49,60}・四石・空盤の勝敗は対象外。
evidence: 12,068手選択の固定戦略を独立4×4整数行列式で全到達18,649局面・終局2,554局面まで再生し元先手敗北終局0。生成・独立検証・証明書保存CI 41376071344成功。初版の固定44二対二修復監査はGitHub Actions 41376210618成功。後続K0627による追加六石WINの除外後は66組となり、専用CIの完了を別途確認する。
---

# 六石局面一類の終局までの元先手WIN証明

六石正準鍵 `00000000000200801002000081000000` は、次の着手点43から始まる元先手の必勝戦略を持つ。55個の合法七石子のうち、この一点への着手で元先手WINを維持する。

証明書は相手の全合法応手を展開し、元先手の手番では指定された一手だけを選ぶ。探索器の3×3差分行列式と異なる**4×4整数行列式の余因子展開**で合法手を再計算する。到達18,649局面、戦略指定12,068局面、相手非終局4,027局面、終局2,554局面、検査辺27,947本で、元先手が敗北する終局は**0件**。過去の勝敗cacheやpn/dnは利用していない。改変拒否4件も成功。

これにより、以前の条件付き46六石LOSS証人の一つが元先手WINと判明し、**2,089七石類の旧計画は反証された**。当該六石と別の一類を除いて残る44類を固定する二対二置換68組から、既知WIN6と矛盾しない2,097七石類の条件付き被覆を構成した。これは固定44類・二対二置換に限った最小値であり、選択六石のLOSS証明ではない。初版68組の4×4独立監査は成功。後続の[K0627](K0627-n11-terminal-s7-seven-win6.md)で共有七石の六石親をさらに六類証明したため、68組のうち2組が反証され、66組が非衝突候補として残った。

**六石WIN一類が今回の確定結果。六石LOSS・四石LOSS・二石root閉鎖は新規0件。11×11空盤勝敗はUNKNOWN。**
