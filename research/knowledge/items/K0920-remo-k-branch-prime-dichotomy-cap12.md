---
id: K0920
title: 3枝REMO決定性の素数二分法のcap≤12固定点（定理PD12） — 全r ≥ max(M,2)で一様決定 ⟺ Δ=0または全枝サイズ{2,3,5,7,11}（172=98+74キー・両方向違反0・γ独立）を定理J組立で全称確定・exotic11欺瞞のp=11延伸とexotic12のr=M-1サブ窓反転は低r観察として分離
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [prime dichotomy cap12, REMO prime-size classification cap12, PD12 fixed point]
relations:
- type: depends_on
  target: K0916
  note: cap≤10分（98決定キー）の二分法定理PD。本項はその650新キー拡張で、K0916が予告した22-exoticキーのcap≤11/12固定点問題を解消（exoticは固定点では非決定側）
- type: depends_on
  target: K0906
  note: 定理J(i)（全称・プロファイルごとのdet/svはr ≥ max(M,2)で一定）が本定理の全称化エンジン。各キーのr=M列1本で固定点が確定し、r=13アンカーは窓外冗長確認
- type: depends_on
  target: K0859
  note: Δ=0族（(11,11,11)×γ=0..10・(12,12,12)×γ=0..11の決定性と生存者は定理Dが全rで単独保証（本項ではr=2..9 committed列・r=10/11 focus・r=11/r=12 cheapestアンカーの冗長機械アンカー）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりキーのverdictは実現盤面すべてに転写
- type: depends_on
  target: K0875
  note: cap≤12 Burnside計数(261749,7805,203)・47,595正準プロファイル・1,365キー・650新キー列挙の根拠
- type: depends_on
  target: K0881
  note: cap≤12 r=2,7,8 committed列（低r窓・witness選択規則のstates@r9の相手側）
- type: depends_on
  target: K0876
  note: cap≤12 r=3..6 committed列（同上）
- type: depends_on
  target: K0912
  note: cap≤12 r=9 committed列（witness選択のstates@r9ソース）・検証機構のverbatimブロックと650新キー(45 det/65休眠/540残り)のr=2..9構造ピン
artifacts:
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/report.md
  role: proof
  note: 定理PD12の主張と組立（定理J+K0916+r=M列）・650分類（74決定+576 witness）・低r新観察（prime-11傾斜状休眠とr=M覚醒・exotic11欺瞞p=11延伸・exotic12のr=M-1サブ窓反転）・18機械チェック・限界・再現
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/verify_prime_dichotomy_cap12_20261117.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・入力はsha256ピン留め8 committed列+11新列（packed単一ソース）・機構はK0912 verbatimブロック。18機械チェック全合格・二回cold実行で監査byte同一・LIVEは独立twin再計算1,710レコードverdict一致+状態数一致・所要約2.5分
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/prime_dichotomy_cap12_audit.json
  role: data
  note: 監査JSON（sha256 40b11680…・det 74キー全表・witness 576キー全表・dormancy系列・J13アンカー源泉表込み）
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r11_focus.jsonl
  role: data
  note: r=11 focus列・64候補キー全1,619プロファイル・[canon, sv, fl, states] packed・二重実行byte同一
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r10_focus.jsonl
  role: data
  note: r=10 focus列・同一1,619プロファイル・二重実行byte同一
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r12_witness.jsonl
  role: data
  note: r=12 witness走査・exotic12 20+others12 332のcheapest profile・全非決定・選択規則は検証器がcommitted r=9列から再導出
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r11_witness.jsonl
  role: data
  note: r=11 witness走査・others11 222のcheapest profile・全非決定
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_r12_d0anchor.jsonl
  role: data
  note: (12,12,12)×γ=0..11のr=12 cheapestアンカー12件・定理D生存者P_11
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_d0_r11.jsonl
  role: data
  note: (12,12,12)×γのr=11 cheapestアンカー12件・定理D(12,11)生存者P_10
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_ex12_r10.jsonl
  role: data
  note: exotic12 20キーのr=10 cheapestプローブ・全決定（欺瞞窓のr=10端）
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_ex12_r11.jsonl
  role: data
  note: 同r=11プローブ・全非決定（r=M-1サブ窓反転の直接データ）
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_others12_r11.jsonl
  role: data
  note: others12 332キーのr=11 cheapestプローブ・全非決定（sub-M）
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_others11_r10.jsonl
  role: data
  note: others11 222キーのr=10 cheapestプローブ・全非決定（sub-M）
- path: research/experiments/remo-k-branch-prime-dichotomy-cap12-20261117/output/packed_j13_anchor.jsonl
  role: data
  note: 定理J r=13 constancyアンカー15件（witness 10+prime-11 light 5・sv mask 0不一致）
scope: '極大安全集合がちょうど3個の点族（3枝合成族・正準領域・cap≤12の47,595正準プロファイル・1,365キー）のREMOについて、キー（サイズ多重集合+γ）がrで一様決定的であることがすべてのr ≥ max(M,2)で成立するのは Δ=0（一様サイズ(C,C,C)|γ・定理D族）または全枝サイズが{2,3,5,7,11}のとき、かつそのときに限ること（cap≤12全体で172=98+74決定キー・両方向違反0・γ独立・576キーはr=M列の非決定witness）。r全称は定理J(i)（K0906全称証明）とK0916（cap≤10分）とr=M列1本組立で確定し、定理E′経由で実現盤面に及ぶ。Δ=0族の決定性と生存者は定理Dが全r（r < Mを含む）で全称保証。付随する有限観察（prime-11の傾斜状休眠とr=M覚醒・exotic11欺瞞窓r=2..M-1のp=11延伸・exotic12のr=M-1サブ窓反転・G′のr=11チェーン一致）は全称昇格しない。枝サイズ≥13・{2,3,5,7,11}が素数性として機構であることの特徴づけ・G′のr ≥ 7全称拡張・順位決定性・others11/others12の全プロファイル分類は含まない'
evidence: 'verify_prime_dichotomy_cap12_20261117.py全チェック合格（18/18・二回cold実行で監査JSON byte同一・sha256 40b11680…）。PIN: 8 committed列+11新列がピン一致。B: Burnside(261749,7805,203)→47,595・1,365キー・650新キー・31,732新プロファイル。TAX: 650=23Δ0+51prime-nD0+2exotic11+20exotic12+222others11+332others12。FOC: focus列が64候補キーの全プロファイルを被覆（1,619=1,607+12）。S1: 62 prime-11キーがr=11で一様決定・生存者==チェーン生存者P_1（0不一致）。S2: exotic11一様非決定（sv 0b11）。O1: r=10 focus=13一様決定/51一様非決定/0混合。EX11: exotic11がr=2..10の9列全部で決定的（12×9）・r=M=11で反転・欺瞞族p=11延伸。P11: prime-11休眠系列ピン（r=2..6混合90/273/273/704/704・r=7..10一様非決定・r=11覚醒）。D0C: Δ0プロファイルが定理D生存者で決定的（r=2..9の336+448両方・r=10/11 focus・計6,224 profile-columns違反0）。D0: (12,12,12)cheapestアンカーが定理D生存者P_11(r=12)/P_10(r=11)。EX12: exotic12全1,425プロファイルr=2..9決定的・cheapest r=10決定→r=11(M-1)非決定→r=12(M)非決定。N1/N2: witness全非決定かつ選択規則（states@r9昇順・canon tiebreak）をcommitted r=9列から再導出して0違反。C1: 64+222+352+12=650被覆・144多重集合でγ混合0。PD12: 650新キーの決定集合==Δ0∪全素数（74/576・双方向違反0）。FL1: 全4,445新レコードでfl==OR{1<<(C_i mod r)}・違反0。J13: r=13アンカー15件のsv maskがr=11/r=12源と同一。LIVE: 独立Python mask twinがwitness/probe/anchor全1,007+focus抽出を再計算し1,710レコードverdict一致・かつtwin状態数==engine statesが1,710/1,710。機械列11本は独立二重実行でbyte同一。r全称は定理J（K0906）への依存で、PD12/N1N2以下の再導出は機械アンカー。低r観察は有限データで全称昇格しない'
---

# 3枝REMO決定性の素数二分法・cap≤12固定点（全r）

## 命題（定理PD12・全称）

正準領域 cap≤12（47,595プロファイル・1,365キー）の3枝REMOに
ついて。M = max C_i とすると、キー K = (sizes, γ) が **すべての
r ≥ max(M,2)** で一様決定的であるのは

> Δ=0（一様サイズ (C,C,C)|γ・定理D族）または全枝サイズ ∈ {2,3,5,7,11}

と同値。確定値:

- 固定点一様決定キー **172個ちょうど** = K0916 cap≤10分 98
  ∪ 新規 74（Δ0 23 + 非一様素数 51）。両方向違反 0。
- **系（γ独立）**: 固定点の一様決定性はサイズ多重集合のみで
  決まる（144多重集合・0混合）。
- 新規650キーの内訳: 決定側 74、非決定側 576（exotic11 2・
  others11 222・exotic12 20・others12 332・各キー r=M 列に
  非決定witness 1件以上）。

## 証明の組立

新規スイープは機械列計算（focus全列・witness走査・アンカー）
のみ。(1) 定理J(i)（K0906・全称証明済み）: プロファイルごとの
det/svは r ≥ max(M,2) で一定 → キーの一様決定性も窓上一定 →
各キー r=M 列1本で固定点確定。(2) cap≤10分98キーは定理PD
（K0916）。(3) 650新キーの r=M 列: 64候補キー（62 prime-11
+ 2 exotic11）はr=11 focus全プロファイル列、(12,12,12)×γは
定理D+cheapest機械アンカー、残り576キーはcheapest witness
走査（選択規則はcommitted r=9列から検証器が再導出）。(4)
定理E′（K0861）で実現盤面に転写。

## 低r構造の新観察（有限データ・全称昇格しない）

- **prime-11の覚醒はちょうど r=M**: 51非一様素数-11キーの
  休眠は傾斜状（r=2..6 混合: 90/273/273/704/704 of 1,271
  プロファイル非決定、r=7..10 一様非決定）、r=11=M で一様
  決定に反転。生存者は全62 prime-11キーでチェーン生存者
  P_1（G′ r=11 有限アンカー・全称保証はK0864の r=2..6 まで）。
- **exotic11欺瞞のp=11延伸**: (1,1,11)|0, (1,11,11)|0 は
  低r窓 r=2..10 全体で決定的（12プロファイル×9列）のまま
  r=11=M で一様非決定に反転。K0916の6欺瞞キー族
  (1,1,p),(1,p,p) p∈{3,5,7} は8キー族へ。K0916が予告した
  「22 exoticキー問題」は解消: exoticは固定点では正しく
  非決定側（低r現象であった）。
- **exotic12のサブ窓反転**: (10,10,12),(10,12,12)×γ=0..9 の
  全1,425プロファイルは r=2..9 で決定的、cheapest profile は
  r=10 でも決定的だが **r=11 = M−1（定理J窓の下）で非決定**、
  r=12=M でも非決定。定理J窓外の低r反転の第1例。
- Δ0のsize-11/12キーは定理Dが全rで全称保証。((11,11,11)×γ
  の全336プロファイルは r=2..11 全10列で定理D生存者と一致。)

## 限界

- rについて全称は定理J（K0906）経由。サイズは≤12で有限。
- {2,3,5,7,11}は有限集合の記述で、素数性が機構であるとは
  主張しない（K0916と同一の注意）。
- G′の全称保証は r=2..6。傾斜状休眠・サブ窓反転は有限観察。
- witness走査は各キーの「一様決定でないこと」の確立に十分
  だが、others11/others12のプロファイル全体の分類ではない。
- 順位決定性は扱わない。11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。

## 再現

`verify_prime_dichotomy_cap12_20261117.py`（自己完結・決定的・
stdlibのみ・入力はsha256ピン留め19列・機構はK0912 verbatim
ブロック）。18機械チェック全合格・二回cold実行で監査JSON byte
同一（sha256 40b11680…）。所要約2.5分。
