---
id: K0965
title: kodd=4完全センサス（M≤10000・t≥2）と予想(i)（kodd=4⟹t<√M）の反証
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [K4-CENSUS-M10K, CONJ-I-REFUTED, KAPPA0-GAMMA-ROWS]
relations:
  - type: refutes
    target: K0961
    note: 予想(i)「kodd=4 ⟹ t < √M」を反例で否定（最初の反例 M=2221・t=54・M≤10⁴で932反例・全てγ枝κ≥1）
  - type: depends_on
    target: K0961
    note: K4-CAP（α/β/γ 3分岐とγ sharp上界 t·2^{2a}p₁²≤M−2/κ=0版）・EW/TZ・K4-A/T7をband完全性の前提に使用
  - type: depends_on
    target: K0963
    note: 出版kodd5_core（band_tmax・k5_config/cap_check・k6plus_case）をバンド計画と監査に再利用・掃引会計の意味論を継承
  - type: verifies
    target: K0963
    note: 出版掃引バンド[4,T₅]を同一エンジンで完全再現（候補26,574,669・smooth 5,038,337・ヒット133,726・kodd hist・tmax行3件・kodd=5 406行の全フィールド一致）
  - type: supports
    target: K0961
    note: 予想(ii)のkodd≥6部分（kodd≥6⟹t≤3）は掃引帯内で支持（25行全てt≤3・M≤10⁴・LG-OPENのため証明なし）
artifacts:
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/report.md
    role: proof
    note: バンド完全性論・検証（バンドA再現・独立監査・決定性）・反証の構造・census詳細の正本
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/sweep.js
    role: verifier
    note: 掃引エンジン（Node.js・全整数<2^53・出版と同一のsieve-walk法・mode A検証/mode B本掃引・sha256 0bf08a5b…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/audit.py
    role: verifier
    note: 全行独立監査（新規素数リスト試除再因数分解・identity/window/TZ/EW/K4-A/T7/branch cap・sha256 0953a218…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/bounds.py
    role: verifier
    note: バンド計画（出版kodd5_core import・T₅≤(M−2)/36等全件assert・sha256 3d2d3a0f…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/summarize.py
    role: verifier
    note: 出版サマリー組立（決定的・sha256 8a1b3b51…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/audit_progress.json
    role: data
    note: 監査進捗（78,893行検査・bad=0・sha256 6b4f2abc…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_summary.json
    role: data
    note: 集計・census構造・違反ブロック・検証ブロック（sha256 4147bd28…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modea_acct.jsonl
    role: data
    note: バンドA完全再現のper-M会計926行（検査の一次記録・sha256 a2133118…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_acct.jsonl
    role: data
    note: 本掃引per-M会計926行（sha256 4b3d0296…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_rows_k4_deep.jsonl
    role: data
    note: kodd=4のt>T₅(M)行1,728行（violフラグ付き・違反932行を含む・sha256 38e57832…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_rows_k4_kap0.jsonl
    role: data
    note: κ=0のkodd=4行15行（γ 9/α 6・sha256 be6bff78…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_rows_k5p.jsonl
    role: data
    note: kodd≥5行1,217行（t∈{2,3}ギャップ786行込み・sha256 25a0a334…）
  - path: research/experiments/remo-kodd4-sqrt-band-20261118/output/modeb_rows_k3_t300plus.jsonl
    role: data
    note: kodd=3深部t≥300行19行（sha256 e45f0293…）
  - path: research/log/2026-11-18-remo-kodd4-sqrt-band.md
    role: log
    note: 発見順・K番号並走衝突・scratch失敗の記録
date: 2026-11-18
scope: >-
  素数M∈(2000,10000]（926素数）のkodd=4 smoothヒット（main regime・t≥2・[Y ok]クラス）の
  完全センサス帯（part 1: t∈[2,⌊(M−2)/36⌋]全κ・part 2: t∈(⌊(M−2)/36⌋,⌊(M−2)/12⌋]κ=0）の
  決定的完全列挙と、それに基づくK0961予想(i)（kodd=4⟹t<√M）の反証。同帯のkodd=5・kodd≥6・
  κ=0行・kodd=3深部帯の観測を含む。
evidence: >-
  反証は検証済み反例の提示（M=2221・t=54・κ=78・N=266,668,806=2·3·347·349·367・
  独立監査でidentity/窓空/smooth/Y素数/γ sharp上界を確認）による論証で、全932反例の各行を
  同様に独立検証（0失敗）。センサス帯の完全性はK0961 K4-CAPの既証明（α枝t<√M・γ枝
  κ≥1は(M−2)/36・κ=0は(M−2)/12）から導かれる。エンジン検証として出版K0963掃引バンド
  [4,T₅]を完全再現（全集計・kodd=5 406行の全フィールド一致・kodd=4 23,260行の重複帯一致）。
  78,893行の独立監査（試除再因数分解・全述語）0違反・冷再実行で全出力byte同一。
  ただしkodd≥6に対する帯の完全性はなく（LG-OPEN・capなし）、kodd=3の帯も完全ではない
  （SEAM t<M−3）。M>10000は未掃引。
---

## 命題・範囲

記法はK0956/K0958/K0960/K0961/K0963と同一（M素数・K=(M+1)t+κ・0≤κ≤M−2・
Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・a=v₂(N)・kodd=Ω(N/2^a)・smoothヒット=
(M−1)-smooth∧窓空・[Y ok]=Y素数∨Y=M²）。

- **反証（主張・証明済み）**: K0961予想(i)「kodd=4 ⟹ t < √M」は偽。
  反例: **M=2221・t=54・κ=78・Y=120,067・N=266,668,806=2·3·347·349·367**
  （√M≈47.13・γ枝・κ≥1・a=1・p₁=3・窓[2221,120011]空・γ sharp上界
  t·4·9=1,944≤M−2=2,219成立・2·3·p₂=2,202はMの0.9%下）。
  M≤2000の出版552行（K0961）は0違反のまま、違反は2000<M≤10⁴で932件
  （t/√M median 1.241・max 2.367@t=235, M=9857・N=2·3·1523·1567·1597・
  γ cap飽和86%）。全違反はγ枝・κ≥1・a=1・p₁=3（α枝は構造的に違反不能:
  t<√M/2^a+1/M・実測5,345行でmax t=29）。
- **完全センサス（有限計算・決定的）**: kodd=4・t≥2のsmoothヒットは
  M∈(2000,10000]で34,502行（γ 29,157/α 5,345・β 0行）。
  帯の完全性: K4-CAPによりκ≥1はt≤⌊(M−2)/36⌋・κ=0はt≤⌊(M−2)/12⌋・
  α枝はt<√M<band外・β枝は空。出版バンドA（t∈[4,T₅]）と重複する
  23,260行は完全一致。全行でK4-CAPの全capが成立（0違反）。
- **κ=0のkodd=4行**（K0963 OPEN(iv)）: 15行がM>2000で初出現
  （γ 9/α 6・max t=48@M=7639<√M・κ=0違反0件）。
- **K0963掃引のt∈{2,3}ギャップ**: kodd=5 786行（t=2: 553・t=3: 233・
  最初はM=2069 t=2 N=8,861,526=2·3²·43·107·107）は出版掃引の開始点t=4より
  下で未列挙だった。含めて1,192行全てt≤T₅(M)（**K5-CAPの全行機械確認**）。
  kodd≥6は25行（kodd=6: 24・kodd=7: 1@M=5851 t=3）で全行t≤3
  （PS 11/LG-OPEN 14・予想(ii)のkodd≥6部分は帯内支持・未証明）。
- kodd=3深部帯（t≥⌈√M⌉・帯内）: 43,174行・max t=611@M=9421
  （κ=0・N=2·2477·2897·3779）・帯はkodd=3に対し完全ではない（参考観測）。

## 現在の根拠と限界

- 反証の根拠は「反例が存在する」ことの証明（決定的・検証済み）。
  違反密度・t分布の漸近論は含まない。M>10⁴は未掃引。
- センサスは有限範囲（M∈(2000,10⁴]・t≥2）の完全列挙であり、
  kodd=4の全称命題ではない。t=1行は範囲外（出版規約と同一）。
- kodd≥6の観測は掃引帯内のみ（LG-OPEN・帯外のcapなし）。
- 機械検証: バンドA完全再現（出版K0963集計と全部一致・k5 406行
  全フィールド一致）・78,893行独立監査0違反・冷再実行byte同一・
  会計恒等式（n_smooth=n_blocked+n_hits+n_dead）926素数全件。
- branch型ヒット・F(M)には不適用。11×11空盤に言及しない。
  uv check/buildは本環境にcloneとuvがなく未実施（歴代remo項目と同じ扱い）。
  generated/とroot READMEは未編集。
