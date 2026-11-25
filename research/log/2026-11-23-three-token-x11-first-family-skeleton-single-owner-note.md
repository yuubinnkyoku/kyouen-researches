# 単一オーナー宣言ノート: 3トークン第1族 X=(x,1,1) のパラメトリック閉形式 fit（skeleton 宣言）

- 日付: 2026-11-23
- レーン: 高速レーン（3トークン第1族 fit）
- 対象: κ=1 残余ゲーム H(R; X; z)（K0832 抽象残余ゲーム・2次元盤面への主張なし）の
  3トークン最小族 X=(x,1,1)（2番目・3番目トークンが 1 の固定族）に対する
  パラメトリック閉形式候補 **cand_x11** の fitting・box・box 外 spot・closure・
  例外行・全世界との機械照合。
- スコープ: z>=0・x>=1・R>=0 の閉形式候補の fit 段階（status: observed）。
  **全称主張は含まない**（全称は別宣言）。正本検証器 verify_x11.py の実行前に
  本宣言ノートを出版する（publish-then-execute）。

## 単一オーナー宣言と対抗確認

本レーンが X=(x,1,1) 族の全領域 fit の単一オーナーであることを宣言する。

対抗宣言チェック（宣言直前・GitHub code search）:
- `three-token repo:yuubinnkyoku/kyouen-researches path:research/log` → **0 件**
- `w11 repo:yuubinnkyoku/kyouen-researches path:research/log` → **0 件**
- 既存 3 トークン成果との非重複: vertical-fiber-three-token-transient-band-20261116
  （予想 U/A/B/C の提唱）・vertical-fiber-transient-band-extension-20261116
  （対角線 OK 表 m=9/10・偶数統一形）・vertical-fiber-diagonal-m11-m16-20261116・
  全 1 族 U(k,z,R) の全称帰納証明（vertical-fiber-all-ones-induction-proof-20261116・
  K0832 配下）はいずれも一般的 3 トークン過渡帯の観察・予想・特定行の証明であり、
  **(y,w)=(1,1) 固定で x 方向に全領域（マージ・過渡帯・定常・tail・例外行）を閉形式化した
  fit は本宣言が初**である。
- K 番号: **K1247 を仮採番**（K1246=y20 fit 使用済み・K1250-K1253=inversive arc
  使用済み。K1247/K1248/K1249/K1254/K1255/K1256 は repo 内 code search で未使用を確認。
  push 直前に items tree・実験 dir・list_commits の 3 点再確認で空番を確定する）。

- 宣言時点観測 HEAD: `1a868d05ea3b83aedd1fe46451f612dbf28d5f4e`（2026-11-23T06:21:32Z・y20 fit commit C の直後・push 直前に再取得確認）

## 事前横断予想（閉形式の全領域宣言・機械照合の対象）

記法: d = x - z・S = x+2・O[a,b] = [a,b] 内の奇数全体・
band_{≡z+1}[a,b] = [a,b] 内の z+1 (mod 2) 合同数全体。
行 = (V2 集合, V1F 集合, tail 開始 t, tail 値 tv)。値は R∈V2→2・R∈V1F→1・
R>=t→tv・その他→0・R=0→0。

1. **マージ領域 x<=z-3**: cand = single_token(x+2, z, R)（K0832 出版単一トークン
   閉形式・逐語転写）。z>=4 で生る。
2. **過渡帯 d∈[-2,+4]**（汎用パラメトリック 14 行型・z 偶奇× d）:
   - d=-2: 偶z (O[1,z+1], ∅, z+2, 0) / 奇z (O[1,z], ∅, z+1, 1)
   - d=-1: 偶z (O[1,z-1], ∅, z+1, 1) / 奇z (O[1,z], {z+1}, z+2, 0)
   - d=0: 偶z (O[1,z-1], {z+1}, z+2, 0) / 奇z (O[1,z+2], {z+1}, z+3, 1)
   - d=+1: 偶z (O[1,z-1]∪{z+3}, {z+1}, z+4, 1) / 奇z (O[1,z+2], {z+1}, z+3, 0)
   - d=+2: 偶z (O[1,z-1]∪{z+3}∪O[z+5,2z+3], {z+1}, 2z+4, 0) /
     奇z (O[1,2z+3], {z+1}∪band_{≡z+1}[z+5,2z+3], 2z+4, 1)
   - d=+3: 偶z (O[1,z-1]∪{z+3}, {z+1}∪band_{≡z+1}[z+5,2z+3], 2z+5, 1) /
     奇z (O[1,z+4], {z+1}∪band_{≡z+1}[z+5,2z+4], 2z+5, 0)
   - d=+4: 偶z (O[1,z-1]∪{z+3}∪{2x-1}, {z+1}∪band_{≡z+1}[z+5,2z+5], x+z+4, (x+2) mod 2) /
     奇z (O[1,z+4]∪{2x-1}, {z+1}∪band_{≡z+1}[z+5,2z+6], x+z+4, (x+2) mod 2)
3. **定常領域 x>=z+5**:
   - 偶z: V2 = O[1,z-1]∪{z+3}（z=0 は {3}）・奇z: V2 = O[1,z+4]
   - V1F = {z+1} ∪ band_{≡z+1}[z+5, x+z+3]
   - t = x+z+4・tv = (x+2) mod 2・tail は全行で鋭い（x+z+3 の値 ≠ tv）
4. **例外 7 行** (z,x): (2,1),(1,1),(1,2),(0,1),(0,2),(0,3),(0,4) は明示表
   （正本 cand_x11.py の _EXC 表・report.md に全値を掲載）。
5. **出版予想との対応**（vertical-fiber-three-token-transient-band の予想
   U/A/B/C・j = x-(y+w+z) = d-2）:
   - 予想A（j=0 掃引）: d=+2 行の偶z 掃引帯 O[z+5,2z+3] の上端 2z+3 = 2x-1。✓ 一致
   - 予想B（j=2 対角ピン）: d=+4 行で V2 に単独ピン {2x-1} が出現・tail x+z+4 は
     定常と exact に接続。✓ 一致
   - 予想C（j=1）: d=+3 行では 2x-1 無出現（z>=1）。z=0 の例外行 (0,3) のみ
     V2={3,5} の 5=2x-1 が陽性。✓ 予想C の「z=0 のみ陽性」と一致
6. **全 1 族定理との整合（Lemma T）**: x=1 行のうち z=0,1,2 の 3 行
   (0,1),(1,1),(2,1) は出版全称定理 U0(3,·)/U(3,1,·)/U(3,2,·)
   （vertical-fiber-all-ones-induction-proof・K0832 配下）と厳密一致（z<=80 で
   機械確認済み・正本検証器 C5 で再照合）。z>=4 の x=1 行はマージ行であり
   U(3,z,·) ≡ single_token(3,z,·)（z>=4）が成り立つことを紙上の 2×2 場合分けで
   確認済み・正本検証器 C9 で 3 方機械照合する（z=4..80・raw エンジン込み）。

## 誠実な事前観察の記録（informal preflight 実施済み）

本宣言ノートの出版前に、宣言レーン上で以下の informal preflight を実施済みであり
**すべて bad 0** である。よって正本検証器の C1〜C7b は同一幾何の正本再実行であり、
C8・C9 が本宣言後の実質的な新規照合である:

- box preflight（z=0..30・x=1..z+40・R<=x+z+30）: 1,705 行・129,890 点・
  H_ordered == H_canonical == cand の 3 方一致 bad 0
- S1 深部 spot（z=31..45・60・99・両 bounded エンジン）: 28,394 点 bad 0
- S2 大 x 低 R 列（x∈{300,500,1000}・z∈{15,31,60}・R<=120）: 1,089 点 bad 0
- S3 マージセンサス（z<=45・4 方: raw==single_token==cand==raw 単一トークン）:
  69,531 点 bad 0
- S4 全 1 族アンカー（z<=80・raw==U(3,z,·)==cand）: 6,096 点 bad 0
- S5 closure 恒等式 fit レベル（B子=K1023 出版 cand_y1・z=1..60）: 163,860 点 bad 0
- S5b closure 恒等式 raw レベル（z=1..30）: 26,460 点 bad 0
- S6 tail 鋭性（z<=75・x=z+5..z+40）: 2,736 行 bad 0
- S7 far-tail 列 3 本（(20,25)/(31,36)/(33,38)・R ブロック+R<=30000 深部散点）:
  安定化点 == x+z+4・値 == (x+2) mod 2 bad 0

C8（LCG seed 20261123・N=60,000 散点・z<=200）は宣言時点で**未実行**であり
真の事前予想である。draw 仕様: x_{n+1} = (6364136223846793005·x_n +
1442695040888963407) mod 2^64・seed=20261123・3 draw で 1 点
（z = d1 mod 201・x = 1 + d2 mod (z+60)・R = d3 mod (min(x+z+12,150)+1)）。
最初 3 点: (75,1,5),(129,7,42),(16,72,15)・最終 3 点: (182,39,108),(149,37,62),(146,121,106)。

## 機械算出点数（出版前に predict_counts.py で算出・宣言指標）

| check | 幾何 | 行 | 点数 |
|---|---|---|---|
| C1 box | z=0..30・x=1..z+40・R<=x+z+30・3方 | 1,705 | 129,890 |
| C2 深部spot | z=31..45,60,99 両BoundedEngine | 255 | 28,394 |
| C3 大x列 | z∈{15,31,60}×x∈{300,500,1000}・R<=120 | 9 | 1,089 |
| C4 マージセンサス | z<=45・x<=z-3・R<=x+z+30・4方 | 903 | 69,531 |
| C5 全1族アンカー | z=0..80・R<=min(z+40,90)・3方 | 81 | 6,096 |
| C6 closure fit/raw | z=1..60 / z=1..30 | — | 163,860 / 26,460 |
| C7 tail鋭性 | z=0..75・x=z+5..z+40 | 2,736 | 2,736 |
| C7b far-tail列 | 3列・[t,t+39]+R∈{29997..30000} | 3 | 132 |
| C8 LCG散点 | seed 20261123・N=60,000・z<=200 | — | 60,000 |
| C9 Lemma T | z=4..80・R<=z+40・3方 | — | 6,391 |
| C9b 行整合性 | z=0..75・x=1..z+40・T/P非交差+例外照合 | 5,890 行 | — |

総比較点: **494,579**（+ T0 逐語転写 byte 照合・C6 closure は候補レベル恒等式）
正本検証器は各点数を埋込み期待値として持ち、一致しなければ CHECK-COUNT-MISMATCH で
fail-closed する。

## 実行プロトコル（宣言後の正本実行）

1. verify_x11.py（self-contained・純 stdlib・決定論的）:
   - T0: @@CAND_TRANSCRIPTION@@ block が兄弟正本 cand_x11.py と byte 一致
     （marker 各 1 対・転写 drift 防止）・cand 内 single_token と engine block 内
     single_token の偶発スポット一致。
   - C1〜C9b: 上表の幾何・期待点数 fail-closed 照合。
   - 各 part は Python プロセスを分けて実行し output/part-*.json を書き出し、
     --audit が全 part を収集して output/audit.json を生成（part 欠落・点数不一致・
     bad>0 はいずれも FAIL-CLOSED・audit を書かない）。
2. 決定性: 各 part を同一 cwd 2 回 + 隔離側（別 tree/cwd/HOME・env -i・
   PYTHONHASHSEED=random）1 回で再実行し、JSON 全 byte-identical。
3. fail-closed 改ざん電池 10 変種（正本 cand に対する値レベル改ざんを wrapper で
  注入し C1/C4/C5/C8 電池で検出を期待・検出不能なら rc=2 fail-open として記録・
   改ざんは正本 non-write で実施）:
   T1 box 内 1 点値反転 (0,1,1)・T2 例外行 (2,1) の V2/V1F 交換・
   T3 定常 band parity 反転・T4 マージ境界 x=z-3 で値 xor 1・
   T5 tail 開始 x+z+4→以降 1 点欠落・T6 tail 値反転・
   T7 d=+2 偶z 掃引上端 2z+3 除去・T8 d=+4 対角ピン {2x-1} 除去・
   T9 例外行 (0,1) の V1F {1}→{2}・T10 例外行 (1,1) の tail 値 1→0。
   なお例外行 (0,4) が汎用 d=+4 偶z 行と集合完全一致する二重記帳であることを
   C9b で機械確認する（不一致なら fail）。
4. **status は observed のまま**: 全称（巻き戻し帰納 H(R;(x,1,1);z) の全 z・全 x・全 R・
   trust 境界の機械分類）は本宣言の範囲外・別宣言が必要。
   標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
   すべて UNKNOWN のまま一切言及しない。3トークン (·,2,1) 族・(y,w) 一般化・q 点版も
   本宣言の範囲外（次候補として (·,2,1) 族の同型 fit を記録する）。

## 出版予定

- 実験 dir: research/experiments/vertical-fiber-three-token-x11-first-family-fit-20261123/
  （report.md・cand_x11.py・verify_x11.py・output/audit.json・predict_counts.py）
- K item: K1247（仮採番・kind proposition・status observed・topics grundy, residual-games）
- log: 本宣言ノート + 実行記録 research/log/2026-11-23-three-token-x11-first-family-fit.md
- README 弾丸: research/knowledge/README.md 該当セクション末尾に 1 弾丸
