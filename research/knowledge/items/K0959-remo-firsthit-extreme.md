---
id: K0959
title: "初回ヒットの極値構造: F恒等式・指数平坦化のフィッティング産物化・BH極値モデル・EV増幅（F-IDENTITY・FLAT-ARTIFACT・BH-EXTREME・EV-AMP・ENGINE-F）"
kind: proposition
status: observed
topics: [residual-games, statistics, verification]
aliases: [F-IDENTITY, FLAT-ARTIFACT, BH-EXTREME, EV-AMP, ENGINE-F-ANCHOR]
relations:
  - type: depends_on
    target: K0956
    note: F_by_M（303素数）・firsthit_rows.json 1,546行・修正t*・ピン済み5 core（prehit bf8ed817…・composite 3990d67f…・sievegen a69f916c…・branch_density 34b4ff15…・hitpair 0237aa1b…）を使う
  - type: depends_on
    target: K0954
    note: 修正from-start BHモデル（t*・Λ*）の定義を使う
  - type: depends_on
    target: K0950
    note: F-fit出版値（1.767·M^1.509@M≤199）との照合に使う
  - type: supports
    target: K0956
    note: OPEN「F(M)の遠域平坦化の機構」をフィッティング産物として解決する
  - type: connects
    target: K0949
    note: κ*偶数303/303はPARITYの系として再確認する
  - type: connects
    target: K0958
    note: F_type=branch全303行はsmoothヒットのt集中（K0958）と整合する
artifacts:
  - path: research/experiments/remo-firsthit-extreme-20261118/report.md
    role: data
    note: 全表・解釈の正本（本項は有限観察で証明項目ではない）
  - path: research/experiments/remo-firsthit-extreme-20261118/extr_core.py
    role: verifier
    note: 冪/log-spaceフィット・Spearman・bucket median・EV増幅の実装
  - path: research/experiments/remo-firsthit-extreme-20261118/audit_build.py
    role: verifier
    note: 決定的builder（2回cold実行byte同一）
  - path: research/experiments/remo-firsthit-extreme-20261118/prehit_core.py
    role: verifier
    note: K0956ピン（sha256 bf8ed817…一致）
  - path: research/experiments/remo-firsthit-extreme-20261118/composite_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 3990d67f…一致）
  - path: research/experiments/remo-firsthit-extreme-20261118/sievegen_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 a69f916c…一致）
  - path: research/experiments/remo-firsthit-extreme-20261118/branch_density_core.py
    role: verifier
    note: K0954/K0956ピン（sha256 34b4ff15…一致）
  - path: research/experiments/remo-firsthit-extreme-20261118/hitpair_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 0237aa1b…一致）
  - path: research/experiments/remo-firsthit-extreme-20261118/output/audit.json
    role: data
    note: 全数表とK0956 outputピン（sha256 75063f46…）
  - path: research/log/2026-11-18-remo-firsthit-extreme.md
    role: log
    note: 発見順・機械結果の要約・次課題
date: 2026-11-18
---

## 命題・範囲

本項はK0956出版データ上の有限観察のまとめであり、全称定理を含まない。
F(M)=(M+1)t*+κ*はMの最悪初回ヒット（t*=F_t・κ*=F_kappa・liveクラス全体のargmax）。
対象はF_by_M（素数M≤2000の303行）とfirsthit_rows.json（素数M≤199の1,546 live
クラス・修正t*つき・sha256 e7df3eae…ピン）。すべての数値は決定的builderで
2回cold実行byte同一。

- **F-IDENTITY（有限・303/303）**: F=(M+1)F_t+F_kappaが全行で厳密成立。
  F_type=branchが303/303（どのMにもsmooth最悪クラスがない。smoothヒットの
  t集中（K0958）と整合）。F_kappaは全行で偶数（K0949 PARITYの系: 奇素数Mでは
  K偶数⟺κ偶数・M=2はκ*=0）。F_t=2はM∈{2,3,17}のみ。κ*=0は6素数。
  median κ*/M=0.564（max 0.991）。FはMについて単調でない（302隣接素数ペアの
  137ペアで減少、例: M=1511: F=118798 vs M=1523: F=56950）。max F=220,140。
  Fについての漸近的主張は点別でなく統計的でなければならない。
- **FLAT-ARTIFACT（有限・方法論的）**: K0956が読んだ「指数平坦化」
  （冪フィットの指数βがgrid拡大で1.5088→1.3861→1.2798に減少）は
  フィッティング産物。純粋決定論的法則g_d(M)=M ln^d Mを同じ3 gridで
  冪フィットすると同じ指数減衰パターンが出る（d=1.8: 1.6282/1.3900/1.2736で
  大きい2 gridはobserved 1.3861/1.2798と0.006以内一致・d=1.5: 1.5235/1.3250/1.2280で
  小gridはobserved 1.5088と0.016以内一致）。よって指数ドリフトはレジーム変化の
  証拠でない。逆に固定(α,d)は3 gridを同時に当てはめられない（log-space slope-1
  フィットのR²が0.886/0.924/0.745で冪フィットと同程度）。この範囲ではFは
  固定dのαM ln^d Mでもない。安定量はF_t/ln²Mのbucket medianで、
  6 bucket（M∈[2,50)/[50,100)/[100,200)/[200,500)/[500,1000)/[1000,2001]）で
  0.8696/0.9761/0.8949/0.9126/0.9351/0.8560 ∈[0.856,0.976]。
  F~(M+1)F_t+κ*はM ln²M形を遺伝する。
- **BH-EXTREME（有限・heuristic）**: クラス数≥3の素数M≤199（43個）で、
  pooled Spearman(t_first,t*)=0.1619（全体順序はノイズ支配・K0956と再現）に対し
  top-decile Spearman=0.5633・top-3 overlap平均0.9302（観測最悪3クラスの平均
  2.79個がモデルtop-3内）・argmax一致9/43・観測最悪クラスのBH正規化rank
  median 0.273/mean 0.399（ランダム0.5）。修正from-start BHモデルは
  順序モデルでなく極値モデル（どのクラスが遅いかの予測に使え、
  bulkの順位付けには使えない）。
- **EV-AMP（有限・M≤199）**: 各Mのt*/median(t_first)はiid指数baseline
  ln(2n)/ln2（n=liveクラス数）をmedian 1.363倍（mean 1.609・M≥50でmedian 1.385）
  上回る。極値: M=181: t*=81 vs median 2（超過5.66倍）。クラス間レートの
  非一様性が最悪値を一様Poisson予測より典型的~1.4倍増幅する。
- **ENGINE-F（有限・機械）**: 全303 F行をピン済みengineでσ_Z(M,F)=1と
  直接照合（0失敗・3.4秒）。engine錨をK0956のK≤7,440からK≤220,140へ拡大。

## 現在の根拠と限界

- 本項の全主張は有限観察・heuristicであり、全称証明を含まない。
  statusはobserved。
- FLAT-ARTIFACTはFについての定理ではなくフィッティング手法への方法論的注記
  （surrogate回帰実験）。K0956のOPEN記述を解決するが、F/(M ln²M)の真の
  漸近形（limsup/liminf・ bucket medianのM→∞挙動）はOPENのまま。
- F_C=gcd(M+1,κ*+2)は2が68/303・残りは多様（C>100が55件・C=(M+1)/2が20件）で、
  最悪クラスはC単独では特徴づけられない。
- EV-AMPの増幅機構（クラスレートの異質性の定量モデル化）・BH極値モデルの
  極値分布としての正当化は未解決。
- 11×11空盤・二石root・標準有限盤には言及しない。uv check/buildは本環境にcloneとuvが
  なく未実施（歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。