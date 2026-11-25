# 3×m・q=4 ブロッキング計数（全プロファイルクラス上界）— 単一オーナー宣言ノート（2026-11-21 高速レーン）

## 宣言

3×m・q=4（勝利 = 共円または共線上の 4 点）の行欠損極大安全配置に対する
K1196 型ブロッキング計数の需要式による**全 19 プロファイルクラスの明示的上界表**を、
本レーンが単一オーナーとして着手・出版する。
ext28plus レーンの再開課題 (b)「family 消滅の一般計数証明（K1196 型の 3 行 q=4 版）」は
どのレーンにも宣言されていないことを、宣言時点の main で確認した。
宣言時 main HEAD: `f02d06c8041a2ab2c3af2309b4ac057fb2587dde`（2026-11-21T11:11:44Z・宣言作成 2026-11-21T11:12Z。
並走宣言の確認は 10:57Z HEAD `95dbf1bc…` で実施し、その後の main 増分
`f02d06c8`（n11 quarantine parser fix・本レーン非接触）を反映済み）。

## 対象と方針

- 主定理（数学的証明）: 3 行スラブ（行 y∈{0,1,2}・列 x∈{0..m−1}）・q=4 において、
  行欠損（プロファイル (r0,r1,r2) ≠ (3,3,3)）極大安全配置の存在幅 m は
  ソート済みプロファイルクラス c = sorted(r) のみで決まる上界 B(c) を超えない。
  証明骨子: 欠損行の空点は水平線（石数 ≤ 2 で 4 点に届かない）も非水平直線
  （3 行と高々 3 格子点で交わる）も block できず、すべてブロッカー円が担う。
  円と水平線の交点は ≤ 2 なので、石 3 つ組 T（円を一意に決定）ごとの覆点数は
  構成 u(T) に対して高々 Σ_def (2−u_i)、3 つ組数は mult(u) = Π C(r_i, u_i)、
  需要式 `d·m − Σ_def r_i ≤ CAPS(r) := Σ_u mult(u)·Σ_def max(0,2−u_i)` を解いて
  `m ≤ B = floor((CAPS + Σ_def r_i)/d)`。
- 上界表（主要）: {0,3,3}→36・{1,3,3}→52・{2,3,3}→68・{2,2,3}→40・{1,2,3}→24・
  {2,2,2}→22・{1,1,3}/{0,2,3}→13・{1,2,2}→11・{0,1,3}/{0,2,2}/{1,1,2}→5・
  {0,1,2}/{1,1,1}→2・{0,0,*} と {0,1,1} は全 m で不可能。
  系1: def-mode 存在は m ≤ 68（K0024 の U_{3,4}=69 境界の、K0318 非依存の
  自己完結な第二certificate）。系2: 69 境界の実体はクラス {2,3,3} の CAPS=66。
  系3: M_{3,4}=24 閉包のための掃引窓は 32..68 から上表で大幅縮減
  （53..68 は {2,3,3} の 3 行位置のみ・41..52 は {1,3,3} と {2,3,3} のみ）。
- 機械検証（実験 `three-row-q4-blocking-counting-selfcontained-20261121`）:
  stdlib のみ・決定的・fail-closed 検証機（6 gate: g_pin/g_table/g_curves/g_enum/
  g_account/g_witness23・約 6 秒/実行）。g_table は CAPS を閉形式積と石プール直接
  列挙の 2 実装で交叉検証、g_curves は独自整数幾何で m=4..8 の勝利曲線数
  29/50/86/141/221 を既刊値と照合、g_enum は m=4..8 の全安全集合を安全枝刈り
  DFS で走査し既刊 brute JSON と全数一致、g_account は全 18,729 個の行欠損
  極大配置を per-witness で直接検証（安全・極大・2−u_i cap・CAPS 不等式）、
  g_witness23 は既刊 m=23 SAT witness 5 件を plain board 上で検証
  （全てクラス {2,3,3}・demand 21・CAPS 66）。

## 出版物（すべて本レーン所有）

1. 実験 dir `research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/`
   （README・検証機・入力 pin 7 件・captable 生成器・output/audit.json・
   output/reproduction.log・output/comptable.md）
2. K 項目（番号は push 直前に 3 点確認で取得・現在 K1198..K1201 が使用済みで
   K1202 を想定）+ 研究log 2 本（単一オーナー宣言ノート・セッションlog）
3. knowledge README bullet 追記（append only・並走 bullet 温存）

## 受入条件

1. 検証機の全 6 gate が PASS（fail-closed: 監査は全 gate 通過時のみ書込）。
2. battery 4 実行（同一 cwd 3 回 + 隔離 copytree・`env -i`・
   `PYTHONHASHSEED=random` 1 回）で audit.json が byte-identical。
3. 入力 pin 7 件（brute_3x{4..8}_4.json・frontier records m=23 copy・
   列挙レーン family witnesses copy）の sha256 を検証機埋め込み値と照合
   （g_pin・不一致は fail-closed）。負の制御 `--tamper` で g_table が FAIL・
   rc=1・監査未書込であること。
4. 主定理が K1183・K0024・K0318・K1196 の既存主張を一切変更しない
   （M_{3,4} の値は不変・witness-free 帯 {24..31} も不変・K1196 の本文 byte 不変）。
5. 知見の誠実な記載: CAPS は上界であり経験的消滅 onset より緩いこと
   （{2,3,3} の 68 は CAPS=66 が全トリプレス円の最大効率動員を要求する
   「ぎりぎり」の値で、洗練で下がる可能性は未解決課題として残す）、
   構築中の 2 件の実装事故（需要式定数の誤りで一時 B=67・円×水平線の接線重根
   の二重計上で m=4 曲線数 39）と修正を記録すること。

## 非目標

- m=23 SAT レーン・m≥32 治具拡張レーン（宣言 `3aa6fb7f`・wsearch35/wsearch35b）・
  four-row q5 m23 class-split レーンのファイルには 1 byte も触れない。
  系3 の縮減は彼らの掃引対象を狭める知見として読まれるもので、
  彼らの既刊主張の変更ではない。
- 新たな SAT 掃引・列挙閉包の拡幅は行わない（M_{3,4} の確定はしない）。
- P の幅単調性は主張しない。nodes 数・conflicts 数・solved 数・checked 数を
  勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  本レーンと無関係で UNKNOWN のまま。**
