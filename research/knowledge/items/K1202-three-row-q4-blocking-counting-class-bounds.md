---
id: K1202
title: 3×m・q=4の行欠損極大安全配置は全プロファイルクラスで明示的上界を持ち、def-modeの存在はm≤68（K0024の69境界の自己完結第二certificate・ブロッキング計数需要式）
kind: proposition
status: proved
topics: [rectangles, variants, geometry, maximal-safe]
aliases: ["three-row q4 blocking-counting class bounds", "U_{3,4} second certificate"]
relations:
- type: supports
  target: K1183
  note: M_{3,4}閉包プログラムの掃引窓を系3で大幅縮減（幅53..68はクラス{2,3,3}の3行位置のみ・41..52は{1,3,3}と{2,3,3}のみ・37..40はさらに{2,2,3}を追加）。K1183のwitness-free帯{24..31}・P(28..31)・statusは一切変更しない
- type: related
  target: K1196
  note: K1196型ブロッキング計数の3行q=4版。4行q=7では割当円の幾何制約（e+u≤2・3つ組非交差・ΣC(t,3)≤816）だったのに対し、3行ではトリプレス構成の全列挙（mult(u)×Σ_def(2−u_i)）でCAPSが閉じた点が構造的に新しい。K1196の本文・status不変
- type: related
  target: K0024
  note: 条件付き一般定理のU_{3,4}=69境界（m≥69でdef-mode不可能）の自己完結な第二certificate（系1）。K0024本文不変・境界値69は不変
- type: related
  target: K0318
  note: K0024の境界導出で用いられた曲線パックキング機構（K0318）に依存しない独立導出。K0318本文不変
artifacts:
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/README.md
  role: proof
  note: 証明本文（補題L1〜L3・需要式計数・系1〜3・掃引窓縮減表・機械検証・制限・sha256 757c7ea7…）
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/verify_blocking_counting_3x4_20261121.py
  role: verifier
  note: stdlibのみ・決定的・fail-closed検証機6 gate（sha256 e0ac09b5…・約6秒/実行）
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/captable.py
  role: verifier
  note: 構成別貢献表（comptable.md）生成器（CAPS閉形式・検証機g_tableと同一コード）
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/output/audit.json
  role: verifier
  note: 機械可読監査正本（sha256 d56c192b…・3,928 bytes・battery 4実行byte-identical）
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/output/reproduction.log
  role: log
  note: battery 4実行（隔離copytree・env -i・PYTHONHASHSEED=random込み）と負の制御の実行記録
- path: research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/output/comptable.md
  role: data
  note: 全19クラスの構成u別トリプレス数×覆点数の明示表（88行）
- path: research/log/2026-11-21-three-row-q4-blocking-counting-single-owner.md
  role: log
  note: 単一オーナー宣言ノート（宣言時HEAD・対象・受入条件）
- path: research/log/2026-11-21-three-row-q4-blocking-counting-session.md
  role: log
  note: セッションlog（証明・実験事実2件の事故記録・並走レーンとの接続）
scope: "全称数学的証明（定義は3行整数スラブ・q=4・勝利=共円or共線4点・極大安全配置）。盤・レーン依存の要素は使わない。M_{3,4}の値は不変。"
evidence: "需要式計数の数学的証明＋fail-closed機械検証（6 gate・CAPS 2実装交叉・m=4..8全数一致18,729 witnessのper-witness安全/極大/cap較正・m=23 witness 5件・battery 4実行byte-identical・負の制御）。全て整数演算のみで浮動小数点・乱数・時刻不使用。実験README.md参照。"
---

# 3×m・q=4の行欠損極大安全配置は全プロファイルクラスで明示的上界を持ち、def-modeの存在はm≤68（K0024の69境界の自己完結第二certificate・ブロッキング計数需要式）

ext28plus レーンの再開課題「family消滅の一般計数証明（K1196 型の 3 行 q=4 版）」で、
どのレーンにも宣言されていないことを確認して着手した
（単一オーナー宣言: `research/log/2026-11-21-three-row-q4-blocking-counting-single-owner.md`
・宣言時 main HEAD `f02d06c8…`・2026-11-21T11:12Z）。
主定理は SAT 掃引・列挙閉包・K0318 のいずれにも依存しない独立の数学的証明で、
K1196（4 行 q=7）では割当円 1 個ずつの幾何制約から見積もったのに対し、
3 行では**石 3 つ組の構成別全列挙**で各クラスの覆点容量 CAPS が閉形式で閉じる。

## 主定理（全プロファイルクラス上界）

**定理.** 3×m・q=4（行 y∈{0,1,2}・列 x∈{0..m−1}・勝利 = 共円または共線上の 4 点）
において、行欠損（r_y ≤ 2、プロファイル ≠ (3,3,3)）を伴う極大安全配置が
存在するなら、ソート済みプロファイルクラス c = sorted(r) に対し m ≤ B(c) であって、
B は次の明示表で与えられる（19 クラス・d = 欠損行数）。

| クラス c | CAPS | d | B(c) | | クラス c | CAPS | d | B(c) |
|---|---:|---:|---:|---|---|---:|---:|---:|
| {0,3,3} | 36 | 1 | 36 | | {1,2,2} | 30 | 3 | 11 |
| {1,3,3} | 51 | 1 | 52 | | {0,1,3} | 9 | 2 | 5 |
| {2,3,3} | 66 | 1 | 68 | | {0,2,2} | 12 | 3 | 5 |
| {2,2,3} | 76 | 2 | 40 | | {1,1,2} | 12 | 3 | 5 |
| {1,2,3} | 46 | 2 | 24 | | {0,1,2} | 3 | 3 | 2 |
| {2,2,2} | 60 | 3 | 22 | | {1,1,1} | 3 | 3 | 2 |
| {1,1,3} | 24 | 2 | 13 | | {0,0,x}(x=0..3)・{0,1,1} | 0 | — | 不存在 |
| {0,2,3} | 24 | 2 | 13 | | | | | |

**証明骨子**（全文は実験 README 参照）: 欠損行の空点は block に勝利集合を要する。
L1: 水平線は石数 r≤2 で 4 点に届かず、非水平直線は 3 行の各々と高々 1 格子点で
交わるため 4 点に届かない。よって空点はすべて 3 石を含む**ブロッカー円**で
block される。L2: 円と水平線の交点は高々 2（接線なら 1）。L3: ブロッカー円は
その上の石 3 つ組 T を 1 つ選ぶと一意に決まるので、3 つ組ごとに数え上げてよく、
構成 u(T)（各行からの石数・u_i ≤ min(r_i,2)、同一行 3 石は行直線で L1 不成立）
に対する覆点上界は Σ_def max(0, 2−u_i)。3 つ組数 mult(u) = Π_i C(r_i, u_i) なので

`demand = d·m − Σ_def r_i ≤ CAPS(r) = Σ_u mult(u) · Σ_def max(0, 2−u_i)`

であり、`m ≤ B = floor((CAPS + Σ_def r_i)/d)`。B は行位置（中央/外側）に
依らないのでクラスでよい。CAPS=0（トリプレス構成が存在しない）なら全 m で不可能。∎

**系1.** 行欠損極大安全配置は m ≤ 68 でのみ存在する。これは K0024 の
条件付き一般定理による U_{3,4}=69 境界を、K0318 の曲線パッキング機構に依らず
需要式計数だけで再導出する自己完結な**第二certificate**である
（境界値 69 は不変・K0024/K0318 の本文は不変）。M_{3,4} ∈ [24,69] も不変
（下界 24 は既刊 witness band 4..23・有限掃引 {24..31} による）。

**系2.** K0024 の 69 境界を決めている実体はクラス {2,3,3}（triangular family
(3,a,3) の a=2）の CAPS=66 である。クラス単位に分解すると family は
a=0→36・a=1→52・a=2→68 と小さい窓の列に割れる
（{2,3,3} の 66 は (0,1,2)/(0,2,1) 型 18+18、(1,1,1) 型 18、(1,0,2)/(1,2,0) 型 6+6、
(2,0,1)/(2,1,0) 型は欠損行の 2 石を両方含み 0）。

**系3（掃引窓の縮減）.** M_{3,4}=24 を閉じるための残り幅 32..68 の
各行欠損 witness 不存在の確認は、幅の範囲ごとに次のクラスインスタンスだけでよい
（プロファイル全数の走査は不要）。

| 幅の範囲 | 残るクラス×行位置 | インスタンス数 |
|---|---|---:|
| 32..36 | {0,3,3},{1,3,3},{2,3,3},{2,2,3}（各3） | 12 |
| 37..40 | {1,3,3},{2,3,3},{2,2,3} | 9 |
| 41..52 | {1,3,3},{2,3,3} | 6 |
| 53..68 | {2,3,3} のみ | 3 |

また {1,2,3}(24)・{2,2,2}(22)・それ以下の全クラスは既刊 witness-free 帯 {24..31}
（K1183）と合わせて **m ≥ 24 での消滅が確定**する。

## 機械検証（fail-closed・stdlib のみ・約 6 秒/実行）

`verify_blocking_counting_3x4_20261121.py`（sha256 `e0ac09b5…`・6 gate）:
- **g_pin**: 同梱 7 入力の sha256 照合（brute_3x{4..8}_4.json 5 件・
  frontier records.jsonl の m=23 copy commit 13098121 時点・列挙レーン family witnesses copy）。
- **g_table**: CAPS を閉形式積（組み合わせ数）と石プール 3 つ組直接列挙の
  2 実装で独立計算し一致・期待表照合・floor 算術・クラス最大 68 を検証。
- **g_curves**: 独自の整数有理幾何（Cramer 整数解・isqrt 判別式）で m=4..8 の
  勝利曲線数 29/50/86/141/221 を全列挙照合（brute34 系とは第三系統の実装）。
- **g_enum**: 安全枝刈り DFS で m=4..8 の全安全集合を走査し、極大・行欠損の
  size 別・プロファイル別集計を既刊 brute JSON と全数照合
  （欠損極大 182/674/1724/4607/11542 = 18,729・P(m) 真偽込み）。
- **g_account**: 全 18,729 個の行欠損極大配置それぞれについて
  3 つ組ごとの整数幾何オブジェクトを再計算し、(a) どのオブジェクトも 4 石を
  含まない（安全性の独立再検証）、(b) 欠損行の全空点がブロッカーで覆われる
  （極大性の独立再検証）、(c) 覆点数 ≤ 2−u_i（L2 の実測較正）、
  (d) demand ≤ 観測関連ヒット総数 ≤ CAPS、(e) m ≤ B(class)、を検証
  （クラス別 checked: {2,3,3} 9,208・{2,2,3} 4,498・{1,3,3} 3,296・{1,2,3} 1,364 他）。
- **g_witness23**: 既刊 m=23 SAT witness 5 件（中央行欠損 2・外側行欠損 2・
  列挙レーン family 外側 1）を plain board 上で同検査
  （全てクラス {2,3,3}・demand 21・CAPS 66・m=23 ≤ 68 と整合）。

battery 4 実行（同一 cwd 3 回 + 隔離 copytree・`env -i`・`PYTHONHASHSEED=random`）
で監査が byte-identical（audit.json sha256 `d56c192b…`・3,928 bytes）。
負の制御 `--tamper`（期待表 {2,3,3} を 67 に改竄）は g_table FAIL・rc=1・監査未書込。

## 事故の誠実な記録（reproduction.log に同じ）

1. 初版で需要式の定数項を Σ(3−r_i) と誤り B({2,3,3})=67 を算出した。
  交叉検証前に気づき修正（正は Σ_def r_i、B=68）。tamper はこの過度に強い
  境界主張を機械的に捕捉する。
2. 円と水平線の交点列挙で判別式 0（接線）の重根を二重計上し、m=4 の曲線数
  39（正 29）を生んだ。全格子点の方程式再照合で検出し修正。fail-closed の
  g_curves がこの種の誤りを落とす実例。

## 制限・未解決

- 本定理は M_{3,4} を確定しない。37 幅（32..68）の有限掃引は依然必要で、
  系3 の窓は m≥32 治具拡張レーン（宣言 `3aa6fb7f`・wsearch35 系）の対象。
  fast 系の行欠損クラスは {2,2,3} の m≤40 が最大。
- CAPS は上界であり、経験的消滅 onset（非 family は m≈12 で全滅・family は
  m=23 で終端）よりはるかに緩い。{2,3,3} の 68 は CAPS=66 が全トリプレス円の
  最大効率動員を要求する「ぎりぎり」の値で、全ヒット相異の強制・接線・
  格子外根の稀少性で 68 を下げられるかは未解決課題。
- P の幅単調性は未証明。checked 数・nodes 数を勝敗として読まない。
  **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  本項目と無関係で UNKNOWN のまま。**

## 他レーンとの接続（非接触）

m≥32 治具拡張レーンの掃引対象は系3 で縮減されるが、本項は彼らのファイルに
1 byte も触れず、K1183・K0024・K0318・K1196 の主張を一切変更しない。
part1（実験 dir 13 ファイル）・part2（本 item・セッション log・宣言 log）・
part3（knowledge README bullet 1 行 append）で出版。
