---
id: K1081
title: K1069 depth-10判定根に対するdepth-11/12のprobe nodeコスト倍率測定
kind: computation
status: observed
topics: [search-methods, statistics]
aliases: [depth extension cost scaling, depth-11 cost multiplier, depth-12 second difference]
relations:
- type: verifies
  target: K1069
  note: 再測定したdepth-10 probe 20件（倍率系列4実験横断）のnodes・loss・cappedがK1069の出版値・分類ラベルと一致。ただし本項の主眼はコスト測定であり、判定変更・行の閉鎖は行わない
- type: uses
  target: K1082
  note: 大型root標本（第4実験）の対象選択にK1082台帳by_root sum_nodes上位4根を使用。D10再測定8/8が台帳per-probe値と厳密一致
artifacts:
- path: research/experiments/n11-depth11-cost-scaling-pilot-20261120/output/depth11-cost-scaling-pilot-20261120.json
  role: data
  note: 正本SHA-256 44f1b875… （出版値3件厳密再現・倍率1.0004-1.0220・5/5 gate）
- path: research/experiments/n11-depth11-cost-scaling-pilot-20261120/scripts/depth11_cost_scaling_pilot_20261120.py
  role: verifier
  note: depth10出版値一致fail-closed・pilot_d6制御・生child規約の監査機械
- path: research/experiments/n11-depth11-cost-scaling-pilot-ext-20261120/output/depth11-cost-scaling-pilot-ext-20261120.json
  role: data
  note: 正本SHA-256 8a584be6… （K1069 REFUTED-D10決定論選択4根・倍率1.0052-1.0587・6/6 gate）
- path: research/experiments/n11-depth12-cost-trend-2root-20261120/output/depth12-cost-trend-2root-20261120.json
  role: data
  note: 正本SHA-256 10082aef… （D11→D12倍率1.0000-1.0802・idx12根のフロンティア飽和・7/7 gate）
- path: research/experiments/n11-depth11-large-root-scaling-20261120/output/depth11-large-root-scaling-20261120.json
  role: data
  note: 正本SHA-256 c9927a23… （K1082台帳上位4大型根・倍率1.0024-1.0666・D10再測定8/8台帳一致・7/7 gate）
- path: research/experiments/n11-depth11-large-root-scaling-20261120/scripts/depth11_large_root_scaling_20261120.py
  role: verifier
  note: 台帳選択再導出pin・ledger-determinism-crosscheck fail-closed監査機械
- path: research/log/2026-11-20-n11-depth11-cost-scaling-pilot.md
  role: log
  note: パイロットの宣言・手法・結果・解釈規約
- path: research/log/2026-11-20-n11-depth11-cost-scaling-pilot-ext.md
  role: log
  note: 標本拡張の宣言・選択規則・結果
- path: research/log/2026-11-20-n11-depth12-cost-trend.md
  role: log
  note: depth-12第2差分の宣言・結果
- path: research/log/2026-11-20-n11-depth11-large-root-scaling.md
  role: log
  note: 大型root標本の宣言・結果・供給判断への含意（169.6M×1.0666≈181M nodes上限バンド）
scope: >-
  K1069 39-live witness depth-10掃引の分類に含む根のうち10根（出版済み最大probe根14,249,420
  nodes・第17証明書WIN7-D10根・K1069 REFUTED-D10分類38根からhex昇順index {0,12,24,36}の
  決定論選択4根、うちindex {0,12}はdepth 12まで、およびK1082台帳by_root sum_nodes上位の大型
  4根=両順序D10合計8.7M-13.0M nodes）×両AND順序（andclose 1/0）×depth 10/11/12の、
  cap 30M・timeout 280s・runner v17固定コピーによるnodeコスト測定。
evidence: >-
  4実験とも全probeがuncapped・error 0・pilot_d6制御全合格・正本は生probe記録からassembleのみで
  生成され別cwd別プロセスでbyte-identical（各2回）。D10→D11のnode倍率は20 probe全体で
  1.0004〜1.0666（機種非依存のnode単位・D10 node 0.12M-14.2M）。depth側の再測定は出版
  per-probe値3件（14,249,420・1,576,372・2,544,178）と厳密一致し、REFUTED-D10/WINラベルと
  0不一致。大型root標本ではD10再測定8/8がK1082台帳per-probe値と厳密一致（決定論の三重合意）。
  D11→D12倍率は1.0000〜1.0802、D12/D10は最大1.1105で複利にならない。index12根では
  depth-11からdepth-12でnode数が完全同一（フロンティア飽和・追加depthが追加nodeを生まない
  rootの実例）。倍率はD10 node数の大きいrootでやや高めだが非単調（12.8M根のrank1 ac1は
  1.0024、最大1.0666は6.0M根）。大型root帯でも上限+6.7%で「+1手おおむね+7%以内」の
  経験則は維持される。
---

## 命題と範囲

本項は測定（observation）であり、いかなるrootのゲーム理論的値も主張しない。K1069出版済み
depth-10判定根をdepth-11（一部はdepth-12）へ1手ずつ延長したときのnodeコスト倍率を、
K1075掃引と同一のrunner v17固定コピー（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59）・
cap 30M・timeout 280s・両AND順序・pilot_d6制御・逐次実行で測ったものである。

## 根拠

- パイロット（2026-11-20）: 出版最大probe根（REFUTED-D10）と第17証明書WIN7-D10根。5/5 gate。
  depth-10出版値3件厳密再現。
- 標本拡張（2026-11-20）: K1069 REFUTED-D10分類38根のhex昇順index {0,12,24,36}。6/6 gate。
  8 probe全て分類ラベルと整合。
- depth-12第2差分（2026-11-20）: index {0,12}をdepth 10/11/12で自己完結再測定。7/7 gate。
  D10/D11が標本拡張正本と全数一致（決定論の二重測定証拠）。
- 大型root標本（2026-11-20）: K1082台帳by_root sum_nodes上位4根（最大probe根を除く・
  両順序D10合計8.7M〜13.0M nodes）。7/7 gate。D10再測定8/8が台帳per-probe値と厳密一致。
  倍率1.0024〜1.0666。

## 限界と解釈規約

標本は計10根（K1069分類族に限定・決定論選択と台帳上位選択）であり、36 fresh witnessなど
未掃引root族への外挿は保証しない。倍率バンドは供給判断の事前見積の参考値である。探査深さの
上限（depth-13以降）での維持は未検証。capped/timeout probeはコスト下界であって証拠に
ならない（本系列でcappedは0）。depth-11/12で観測されたloss=falseはREFUTED-D11/D12分類
でも行の閉鎖でもない。REFUTED-D10はLOSS証明ではない。標準11×11空盤・二石root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
