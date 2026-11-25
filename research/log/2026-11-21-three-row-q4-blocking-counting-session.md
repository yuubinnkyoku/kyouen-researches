# 3×m・q=4 ブロッキング計数（K1202）セッションlog（2026-11-21 高速レーン）

## 目的と着手の適法性

ext28plus レーンの再開課題 (b)「family 消滅の一般計数証明（K1196 型の 3 行 q=4 版）」。
着手時に最新 main（HEAD `95dbf1bc…`・2026-11-21T10:57Z）で全並走宣言を確認し、
本課題が未着手であることを確認（m≥32 治具拡張は `3aa6fb7f` が wsearch35/wsearch35b/m=32
掃引/dx35/P(32)/K1183 更新を占有・four-row q5 m23 class-split は `0adc2d27` 系占有・
MIN_MAXIMAL s(9) は finite-field 実験dir 占有・n11/fold 系は各レーン占有）。
単一オーナー宣言ノート: `research/log/2026-11-21-three-row-q4-blocking-counting-single-owner.md`
（commit `538b25ed`）。区分: 本セッションは数学的証明＋機械検証の出版であり、
SAT 掃引・列挙閉包の拡幅・他レーンファイルへの変更は行っていない。

## 成果

### 主定理: 全 19 プロファイルクラスの明示的上界（proved・K0318 非依存）

3×m・q=4・行欠損極大安全配置の存在幅は sorted プロファイルクラス c で
m ≤ B(c) = floor((CAPS(c) + Σ_def r_i)/d)。主要値: {0,3,3}→36・{1,3,3}→52・
{2,3,3}→68・{2,2,3}→40・{1,2,3}→24・{2,2,2}→22・{1,1,3}/{0,2,3}→13・
{1,2,2}→11・{0,1,3}/{0,2,2}/{1,1,2}→5・{0,1,2}/{1,1,1}→2・
{0,0,x}・{0,1,1} は全 m で不可能。

- 証明骨子: L1 欠損行の空点は水平線・非水平直線のいずれでも block 不能で
  すべてブロッカー円。L2 円×水平線交点 ≤ 2。L3 ブロッカー円は石 3 つ組で
  一意に決まるので、構成 u（mult(u) = Π C(r_i,u_i)）別に数え上げた覆点容量
  CAPS が需要 d·m − Σ_def r_i を上回れない、の需要式。
- 系1: def-mode 存在は m ≤ 68（**K0024 U_{3,4}=69 境界の、K0318 非依存な
  自己完結第二certificate**・69 は不変）。M_{3,4} ∈ [24,69] 不変。
- 系2: 69 境界の実体はクラス {2,3,3} の CAPS=66（family (3,a,3) は
  a=0→36・a=1→52・a=2→68 に割れる）。
- 系3: 掃引窓の大幅縮減（53..68 は {2,3,3} の 3 行位置のみ・41..52 は
  {1,3,3} と {2,3,3} のみ・37..40 は +{2,2,3}・32..36 は +{0,3,3}。
  12/9/6/3 インスタンス）。{{1,2,3}(24)・{2,2,2}(22)・それ以下は
  witness-free 帯 {24..31}（K1183）と合わせ m ≥ 24 で消滅}。

### 機械検証（fail-closed・stdlib のみ・約 6 秒/実行・ALL 6 GATES PASS）

`verify_blocking_counting_3x4_20261121.py`（sha256 `e0ac09b5…`・6 gate:
g_pin（入力 7 件 sha 照合）/g_table（CAPS 2 実装交叉・期待表・floor 算術）/
g_curves（独自整数有理幾何・m=4..8 曲線数 29/50/86/141/221 既刊照合）/
g_enum（安全枝刈り DFS・m=4..8 全数一致・欠損極大 18,729）/
g_account（全 18,729 配置の per-witness 安全・極大・2−u_i cap・CAPS 不等式）/
g_witness23（既刊 m=23 SAT witness 5 件の plain board 検証・全て {2,3,3}・
demand 21・CAPS 66）。

- battery 4 実行（同一 cwd 3 回 + 隔離 copytree・`env -i`・`PYTHONHASHSEED=random`）で
  監査 byte-identical（audit sha256 `d56c192b…`・3,928 bytes）。
- 負の制御 `--tamper`（期待表 {2,3,3} → 67）: g_table FAIL・rc=1・監査未書込・
  既存監査 sha 不変。所要 0.07 s。
- 幾何・列挙とも既刊 brute34 系とは独立の第三系統の実装（Cramer 整数解・isqrt）。

## 事故の誠実な記録（2 件・いずれも修正済み）

1. 需要式の定数項を Σ(3−r_i) と誤り一時 B({2,3,3})=67。クラス表の交叉検証前に
  手計算で気づき修正（正は Σ_def r_i、B=68）。tamper 制御はこの型の誤りを
  機械的に捕捉する（67 に改竄すると g_table が落ちる）。
2. 円×水平線の交点列挙で接線（判別式 0）の重根を二重計上し、m=4 の曲線数
  39（正 29）。全格子点の方程式再照合で検出し修正。fail-closed gate が
  この型の誤りを落とす実例。

実行環境ハードリセット（バッテリ中 1 回）にも対応済み: /tmp 隔離 battery D の
初回は PATH に python3 が無く rc=127 即失敗（監査・入力に非干渉）。
bin 実在確認のうえ `PATH=/usr/local/bin:/usr/bin:/bin` で再実行し確定
（run D の失敗記録は残す。K1193 第三検証と同型の失敗記録運用）。

## 出版（part1→part2→part3・すべて push 後 fetch-back で byte 照合）

- part1 commit `e9fa9314`: 実験 dir
  `research/experiments/three-row-q4-blocking-counting-selfcontained-20261121/`
  13 ファイル（README `757c7ea7…`・検証機 `e0ac09b5…`・captable.py `526d8c40…`・
  入力 pin 7 件・output/audit.json `d56c192b…`・output/reproduction.log `4047ddc3…`・
  output/comptable.md `9dc4e1d0…`）。
- part2: K1202 item
  `research/knowledge/items/K1202-three-row-q4-blocking-counting-class-bounds.md`・
  本 log・宣言 log（`538b25ed`）。
- part3: knowledge README の K1202 bullet 1 行 append。

K 番号は push 直前 3 点確認で取得した（README grep K1202 = 0・items commits
に K1202 無し・`K1198..K1201` は重複 ID 再採番で使用済み）。

## 未解決・次の価値ある課題（resume 欄）

1. {2,3,3} の CAPS=66 洗練: 68 を下げるには「全 54 トリプレスがそれぞれ
   欠損行の 2 空点 を相異なる点で覆い・かつ全ヒットが相異なる」ことが
   m=68 で強制される構造を使う。接線（重複 1 点）・格子外根・同一行 2 石
   トリプレスの覆点退化を完全に動員する不可能性を示せれば m ≤ 68 から
   戴下する。実験: g_account の by_class 実測 {2,3,3} max_relevant
   relevant/demand 比 18/max_demand 6（実在配置の余裕は大きい）から、
   62..68 帯の bridge 構造は管理しやすいと推定できるが証明ではない。
2. 需要式の下界方向（CAPS を下回れない理由の形式化）: g_account で
   全配置が CAPS を strict に下回る（max_relevant 18 < CAPS 66）ことは、
   均衡の失敗が一般則であることを示唆する。「実在する行欠損配置では
   多くのトリプレス円が重複または 4 石を含む」型の一般的補題が取れれば
   系3 の縮減よりさらに強い消滅定理になる（family m=23 末端 witness 5 件の
   検査でも relevant 21 < CAPS 66）。
3. 3×m・q=5 版の同型定理: 行容量が 4 になる（水平線が q−2=3 石で block 可能に
   なる）ため L1 が崩れ、需要式の拡張（同一行 3 石の割当可能性）が必要。
   独立した一般化レーン（宣言制）。

並走レーンは本文・records・verdict 一切不変・ファイル 1 byte も非触。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
本レーンと無関係で UNKNOWN のまま。**（2026-11-21）
