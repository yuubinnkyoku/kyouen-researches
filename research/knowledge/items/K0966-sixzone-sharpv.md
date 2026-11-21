---
id: K0966
title: γ枝kodd=4ヒットのSIX-ZONE・P2-LOWER・SHARP-V（K0961 γ sharpの厳密改良）
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [SIX-ZONE, P2-LOWER, SHARP-V, SIX-ZONE-BAND, INT-TIGHTEN]
relations:
  - type: depends_on
    target: K0961
    note: "TWO-ZONE（t≥2）とK4-CAP 3分岐（α/β/γ）・γ sharp（κ≥1: t·2^{2a}p₁²≤M−2・κ=0: t·2^{2a}p₁≤M−2）を前提に使用"
  - type: depends_on
    target: K0965
    note: 出版行modeb_rows_k4_deep/kap0（ユニーク1,741行・γ 1,735 = 違反932行を含む）を行入力に使用・違反行の構造解析（全行a=1・p₁=3・γ枝）が発見の起点
  - type: generalizes
    target: K0961
    note: "γ sharp（κ≥1: t·2^{2a}p₁²≤M−2・κ=0: t·2^{2a}p₁≤M−2）をSHARP-V（t·c²M(M+1)<(M−1)³+c²・c=2^a p₁）へ拡張・厳密改良（両方とも成り立つ域では新<旧⟺c²<2M²−5M+1・c=6では全M≥6・改良量≈1/18）し κパリティ前提を除去（κ=0のγ行にも無条件・旧κ=0 capを3倍厳密化）"
  - type: supports
    target: K0965
    note: 予想(i)反証932行の「six zone」構造（6t<p₂≤p₃≤p₄≤(M−1)/6・p₂p₃>k₀・p₂>6t）の全称定理化・M≡2,3 (mod 36)でγκ≥1整数cap−1・κ=0掃引帯上端を3倍縮小（将来掃引用）
artifacts:
  - path: research/experiments/sixzone-k4-sharpv-20261118/report.md
    role: proof
    note: SIX-ZONE/P2-LOWER/SHARP-V・鋭さ比較・six zone系・整数cap増強系の紙上全称証明と機械検証の正本
  - path: research/experiments/sixzone-k4-sharpv-20261118/sixzone_verify.py
    role: verifier
    note: 出版γ1,735行に8述語（恒等式・t≥2・SIX-ZONE(max判定)・補題EX・GZ・P2-LOWER・SHARP-V・旧γsharp再確認）・非γ行の構造的不成立確認（決定的・冷再実行byte同一・sha256 86ca3909…）
  - path: research/experiments/sixzone-k4-sharpv-20261118/output/sixzone_audit.json
    role: data
    note: 全検査0違反・margin・改良量（sha256 fd2966e9…・2回冷実行byte同一）
  - path: research/log/2026-11-18-sixzone-k4-sharpv.md
    role: log
    note: 発見順・検証器の方向バグ（min↔max）発見と修正の記録・次課題
date: 2026-11-18
scope: >-
  素数M≥5・main regime・t≥2・kodd=4・a=v₂(N)≥1・γ枝（p₂p₃≥M）のsmoothヒット。
  SIX-ZONE・P2-LOWER・SHARP-V・six zone系・整数cap増強系はこのスコープの全称定理
  （紙上証明）。α枝には主張しない（i=4で構造的に不成立・γ固有）。a=0（N奇数）の非存在は
  K0968 A-POS（K0949 PARITYの系）で解決済み（仮定a≥1は全ヒットで自動）。
  機械検証は出版行1,741行（γ 1,735・違反932行を含む）と補助の
  K0965完全センサス34,502行（γ 29,157・a∈{1,2,3,4}・p₁∈{3,…,23}・ローカル実行）。
evidence: >-
  紙上全称証明（補題GZ: TWO-ZONE二分法でγ枝のp₂p₃はzone-2。補題EX: 相補積
  R_i≥p₂p₃≥MとY−k₀=t+2からp₁pᵢ>k₀を仮定するとR_i<(M/2^a)(1+(t+2)/k₀)<M
  （a=1は(M−1)t+κ>3・a≥2は3k₀>t+2）で矛盾。SIX-ZONE: TWO-ZONEをq=p₁pᵢに
  適用しzone-2排除。P2-LOWER: GZ+SIX-ZONE。SHARP-V: p₂,p₃,p₄≤(M−1)/cと
  Y>(M+1)t。鋭さ: 新<旧⟺c²<2M²−5M+1）。機械検証: 出版行8述語0違反
  （SIX-ZONE max超過最小−4,020・p₂p₃−k₀最小+93・p₂/(6t)最小1.0057・
  SHARP-V gap最小1,347,287,508・旧γsharp再確認0違反・改良量が全行で正かつ
  厳密式(2M²−5M−35)/(c²M(M+1))と1e-9一致）・α6行はi=4で構造的不成立を機械確認
  ・冷再実行byte同一。補助（非出版入力・ローカル）: 完全センサスγ29,157行で
  同一8述語0違反（SIX-ZONE max超過最小−7,710・p₂p₃−k₀最小+9）。限界:
  SHARP-V超えの絞り込み（合同式・素数間隔・κ偶奇）と5行の壁密着（c·pᵢ=M−1）
  判定はOPEN（a=0はK0968 A-POS・kodd≥5類推はK0968 γ_rで解決済み）。
---

## 命題・範囲

記法はK0956/K0961/K0965と同一（素数M≥5・main regime・Y=K+1・k₀=Mt+κ−1・
N=MY−1・窓=[M,k₀]・a=v₂(N)・kodd=4: N=2^a·p₁p₂p₃p₄・c=2^a·p₁）。
対象: **γ枝（p₂p₃≥M）・t≥2・a≥1のsmoothヒット**。

- **SIX-ZONE（証明済み・全称）**: **c·pᵢ ≤ M−1 (∀i∈{1,2,3,4})**。
  i=1で2^a·p₁²≤M−1。a=1・p₁=3では「N/2の全奇素因数 ≤ (M−1)/6」。
- **P2-LOWER（証明済み・全称）**: **p₂·(M−1) > c·k₀**、従って **p₂ > c·t**
  （a=1・p₁=3でp₂>6t・実測最小比1.0057でほぼ鋭い）。
- **SHARP-V（証明済み・全称）**: **t·c²·M·(M+1) < (M−1)³+c²**。
  K0961 γ sharp（κ≥1: t·c²≤M−2）を c²<2M²−5M+1 のとき厳密に改良
  （c=6では全M≥6・census全行で鋭い・改良量≈1/18）し、**κ=0のγ行にも
  無条件で成立**（旧κ=0 cap (M−2)/(2^a c) を3倍厳密化）。
- **系six zone**: a=1・p₁=3では 6t < p₂ ≤ p₃ ≤ p₄ ≤ (M−1)/6・
  p₂p₃ > k₀・6p₂p₃p₄ ≡ −1 (mod M)。予想(i)反証932行の全体がこの帯に
  閉じ込められる（極値 t=235@M=9857: 帯[1410, 1642.67]に1523,1567,1597）。
  帯の非空性からt < ((M−1)²+36)/(36M) が直ちに従い、SHARP-Vは因子
  (M−1)/(M+1) 分さらに厳密。
- **系INT-TIGHTEN（将来掃引用）**: M≥11・M≡2,3 (mod 36) でγκ≥1整数capが
  ⌊(M−2)/36⌋から1減る。κ=0掃引帯上端は⌊(M−2)/12⌋から
  ⌊((M−1)³+36)/(36M(M+1))⌋≈M/36へ3倍縮小（γ行の閉じ込めのみ主張・
  band完全性の組み立ては掃引設計時に別途）。

## 現在の根拠と限界

- 根拠は紙上全称証明（report.md §2: 補題GZ→補題EX→SIX-ZONE→P2-LOWER→
  SHARP-V→鋭さ比較）。中核は補題EX: p₁pᵢ > k₀ と仮定すると相補積
  R_i = (MY−1)/(2^a p₁pᵢ) < (M/2^a)(1+(t+2)/k₀) < M が
  γの R_i ≥ p₂p₃ ≥ M と矛盾する（Y−k₀=t+2が鍵の恒等式）。
- 機械検証: 出版行（K0965 deep+kap0・ユニーク1,741・γ1,735 = 違反932行を
  含む全出版γ行）に8述語0違反・2回冷実行byte同一。補助（ローカル・
  非出版入力）でK0965完全センサス全γ29,157行（a∈{1,2,3,4}・
  p₁∈{3,5,7,11,13,17,19,23}）でも0違反。定理の証明はa・p₁一般のまま
  与えられており、有限観察はこれを支持する。
- α枝には主張しない（p₁p₄≥Mによりi=4で構造的に不成立・γ固有の定理）。
  β枝は空（K0961）。a=0（N奇数）の非存在はK0968 A-POS（K0949 PARITY:
  ヒットK偶数⟹κ偶数⟹Y奇数⟹N偶数）で証明済み（補題EXの仮定a≥1は全ヒットで自動）。
- kodd≥5への類推（K0963 18設定への「相補積≥M」型事実）はK0968（γ_r枝
  r≥4一般化・SIX-ZONE_r/P2-LOWER_r/Y-CAP_r・r≥5の⟹方向はK0968 OPEN）で解決。
  SHARP-Vを超える絞り込み（6p₂p₃p₄≡−1 (mod M)・素数間隔・κ偶奇の
  組み込み）はOPEN。
- 有限実験と全称定理の区別: SIX-ZONE/P2-LOWER/SHARP-V・系は全称証明。
  完全センサス・出版行の検証は有限機械確認。11×11空盤には直接影響なし
  （σ_Z highwayのcap定数精密化・K0965掃引設計の増強）。
