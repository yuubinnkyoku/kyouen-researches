# 単一オーナー宣言ノート: multi-c web F2 スプレッド法則表・T-RC 子恒等式・mex 不動点証明書（K1287 lane）

- 日付: 2026-11-24
- lane: 高速レーン（短〜中時間・厳密結果）。本ノートは fast-lane の単一オーナー宣言。
- 観測 HEAD（着手時・main）: `5b9c6231`。その後の `9336611a`〜`e56c8cce`
  （対抗 K1286 出版・README 修復）と `a4e00aa3`〜`076e05c1`（Part DH
  takeover・interim・長期レーン bookkeeping・非接触）を本セッションで
  取得済み。**push 直前再取得: `076e05c1`**（Part DH interim note・
  非接触。K1287 採番・multic-web-f2 領域の対抗宣言なしを再確認）。
- K item 番号: **K1287 は空き**（items dir のコミット履歴で最新 K item は
  K1286 = `9336611a`〔items/K1286-border-slices-prediag-collapse.md〕、
  `K1287` を含む log コミットなしを出版直前に確認）。
- 対抗宣言との関係（非重複の明示）: 対抗 fast-lane が `f6db3f33`〜
  `9305b278`（修復 `e56c8cce`）で出版した **K1286 はペア (m,m+g) の
  境界スライス・対角下バンド・床の全称定理パッケージ**（T-PD0/T-B0/
  T-Z1/T-B1/T-Z2/T-B2・K1285 F1 完了）である。その §5 O3 は
  F_d/G_d（d ∈ {1,2,3}・288 点・OBS）を「**未来課題 F2（spread 理論）
  への入力**」として登録した。本ノートはその F2 を引き継ぎ、
  5 族 × 3 面 × d ≤ 8 の法則表・例外構造・frontier・子恒等式を
  有限全数 census + 機械監査として確定する。census の重複行
  （d ≤ 3 の F/G 列・c=1 出版アンカー）は整合行として再検証するのみで、
  全称主張の重複なし。K1286 O1/O2/O4（床負域・pre-diag 分裂）には
  触れない（K1288 以降候補）。
- 規約: publish-then-execute（K1282–K1286 実務と同一。宣言ノート先頭
  出版 → kit 出版 → fetch-back byte 照合 → 公式 4 走 → 変異電池 →
  監査成果物出版 → K item・run log・knowledge README bullet）。

## 用語・記法（repo 標準・K1286 note と同一の規約）

- 局面: H(R; X; z)。X = トークン多重集合、R = 予算、z = plane（pass 残数）。
  手は A（トークン v>1 → v−1・R−1）/ B（トークン 1 除去・z+1・R−1）/
  C（z≥1 で子の値 1 XOR・z−1・R−1）。値 = mex。
- 族点（本ノートが確定する min-gap band の multi-c web・families）:

| 族 | X | 予算 R | 範囲 |
|---|---|---|---|
| W(d,c,m,z) | {m, (m+d)^c} | 2m+d+2+z | m≥1, d≥1, c≥2 |
| D(d,c,m,z) | {m, m+d−1, (m+d)^(c−1)} | 2m+d+1+z | m≥1, d≥2, c≥2 |
| E(d,c,m,z) | {m, m+d−2, (m+d)^(c−1)} | 2m+d+z | m≥1, d≥3, c≥2 |
| A′(d,c,m,z) | {m, (m+d−1)^2, (m+d)^(c−2)} | 2m+d+z | m≥1, d≥2, c≥2 |
| A(m,s,z) | {m^2, (m+1)^s} | 2m+2+z | m≥1, s≥0 |

  frontier（有限観測族・§1 で OBS として区別）:
  Am(m,h,s,z) = {m^2, (m+h)^s}@(2m+2+z)（h≥2）/ SLB2: (x^c)@(x+3) z2 /
  SLB3: (x^c)@(x+4) z3 / L(zp,d,s) = {d, (d+1)^s}@(d+2+zp) plane zp+1。
- [P] = 1 if P else 0。OBS（有限観測）と全称量化を明確に区別する。
  本ノートの**値法則は全て「有限全数 census で bad=0」の観測・予想
  （conjecture）であり、全称定理としての主張はしない**。恒等式
  （§2・I1–I11）のみが代数的全称定理（自明の multiset 等式）である。

## §1 主張一式（値法則 = census-verified conjectures・機体 D1–D6 と
   explore 広域 census で照合・全称は open）

[z ∈ {0,1,2} 共通の記載。z は族点の plane。]

- **C-SPW（W 族法則・予想）**: c ≥ 2 に対し、
  - z=1 面: H = [d even]（例外なし・d=1 は 0。**これが K1284 open
    登録 C-PC1z1-d4 の c≥2 半分の census 上の解**〔全称は open〕）。
  - z ∈ {0,2} 面: d ≥ 2 なら H = [d even]。
    d = 1 なら: (z=2, m=1) → 2（全 c）; (z=0, m=1) → c=2 は 0・c≥3 は 2;
    m ≥ 2 → c=2 は 0・c≥3 は 2（z に依存しない）。
- **C-SPD（D 族法則・予想）**:
  - z=1 面: H = [d odd]（c=1 の pair-slice [g odd]〔K1285 T-PS・公刊〕
    と同一則）。
  - z ∈ {0,2} 面: d = 2 → H = 2（例外: (z=2, m=1, c=2) → 0）;
    d ≥ 3 → H = [d odd]。
- **C-SPE（E 族法則・予想）**: d even → H = 1; d = 3 →
  (z=1 → 0, z ∈ {0,2} → 2); 奇 d ≥ 5 → H = 0。
  （歴史的注記: 「奇 d 全て 2」は旧読みで、広域 census が奇 d≥5 で
  bad=96 の反例を検出し修正した。探索・機体の §3・honest 記録参照。）
- **C-SPA′（A′ 族法則・予想）**: H = [d even]（3 面共通・例外なし）。
- **C-SPA（A 族法則・予想）**: 
  - z=0 面: H = [s = 1]（全 m）。
  - z=2 面: m = 1 → 0; m ≥ 2 → [s = 1]。
  - z=1 面: s=0 → 0; m=1 → 2 (s≥1); m ≥ 2 → (s=1 → 1, s≥2 → 2)。
- **OBS-F1（Am・h ≥ 2・観測）**: z=0 → 全 0; z=1 → (s=0 → 0, s≥1 → 2;
  m・h 非依存); z=2 → (m=1, h=2, s=1 のみ 1・他全 0)。
- **OBS-F2（SLB2 (x^c)@(x+3) z2・観測）**: x=2 → (c=1→0, c=2→2, c≥3→1);
  x ≥ 3 → (c=1: [x odd], c ≥ 2: [x even])。
- **OBS-F3（SLB3 (x^c)@(x+4) z3・観測）**: x=2 → (c≤2→0, c≥3→1);
  x ≥ 3 → (c=1: [x odd], c ≥ 2: [x even])。
- **OBS-F4（L {d,(d+1)^s}@(d+2+zp) plane zp+1・観測）**:
  zp=0: d=1 → 2（全 s）; zp=0 d≥2 → [d even]（全 s）。
  zp=1: d=1 → (s=1→1, s≥2→0); zp=1 d≥2 → [d even]。
- **census 箱の正確な記述（全て bad=0）**: 機体コア箱:
  W: z3 × d 1..8 × c 2..6 × m 1..10〔1200〕/ D: d 2..8 × c 2..6 ×
  m 1..10〔1050〕/ E: d 3..8 × c 2..6 × m 1..9〔810〕/ A′: d 2..8 ×
  c 3..7 × m 1..9〔945〕/ A: s 0..6 × m 1..12〔252〕/ Am: h 2..5 ×
  s 0..5 × m 1..8〔576〕/ SLB2・SLB3: x 2..12 × c 1..8〔88+88〕/ L:
  zp 0..1 × d 1..8 × s 1..5〔80〕。広域 explore 箱（§3・D1–D6 より
  広い部分のみ）: W: c 2..7, m 1..12〔z0/z1/z2 各 576〕/ D: c 2..7,
  m 1..10〔420〕/ E: c 2..7, m 1..9〔324〕/ A′: c 3..7, m 1..9〔315〕/
  A: s 0..6, m 1..12〔84〕。**全称量化はこれらの箱の外では未検証**。

## §2 T-RC 子恒等式（I1–I11・代数定理・機体 D8 で 3,132 点を照合）

族の閉性: W/D/E/A′/A の点の手は全て「同 web の既知族点・または
SLB/L/A frontier 点」に予算 R−1 で落ちる。以下、全て multiset と
予算の等式として一行で証明される（恒等式の機体照合は bad=0・§4 D8）。

- **I1（A-top of W = D）**: W(d,c,m,z) の上トークン m+d を A で
  落とすと X = {m, m+d−1, (m+d)^(c−1)} = D(d,c,m,z)、予算
  2m+d+2+z−1 = 2m+d+1+z。
- **I2（A-min of W = 行 m−1 の W）**: m ≥ 2 のとき A で m → m−1:
  X = {m−1, (m+d)^c} = W(d+1, c, m−1)、予算 2m+d+1+z =
  2(m−1)+(d+1)+2+z。**d が +1 しながら行が下がる**（web の
  m 方向 Episcopal 構造）。
- **I3（C of W = 1 面下の同族）**: z ≥ 1 のとき子は W(d,c,m,z−1)
  （同 X・予算 R−1 = 2m+d+2+(z−1)）。
- **I4（A-mid of D = E）**: d ≥ 3 のとき中央トークン m+d−1 を A で
  落とすと {m, m+d−2, (m+d)^(c−1)} = E(d,c,m,z)、予算
  2m+d+1+z−1 = 2m+d+z。
- **I5（A-top of D = A′）**: 上トークン m+d を A で落とすと
  {m, (m+d−1)^2, (m+d)^(c−2)} = A′(d,c,m,z)、予算 2m+d+z
  （c=2 でも成立: {(m+d−1)^2}）。
- **I6/I7/I8/I9（C of D/E/A′/A = 1 面下の同族）**: いずれも
  子 = 同 X・予算 R−1・plane z−1 の族点。
- **I10（B-min of 行 1 の D = L 点）**: m=1 の D(d,c,1,z) の B は
  {d, (d+1)^(c−1)}@(d+2+z) plane z+1、すなわち frontier L 点
  （zp = z, s = c−1）。
- **I11（B-min of 行 1 の W = 単一層 frontier 点）**: m=1 の
  W(d,c,1,z) の B は ((d+1)^c)@((d+1)+2+z) plane z+1、すなわち
  単一層 frontier 族点（z=0 → (x^c)@(x+2) z1 = 公刊 C-PB2 族、
  z=1 → SLB2 の 1 面上格子、z=2 → SLB3 同）。

含意: 5 族法則（C-SPW/D/E/A′/A）の全称証明は「m=1 の B-exit が
落ちる SLB/L frontier 族 + 床負域（K1286 O1/O2/O4）+ 単一トークン
閉形式」が全称化されれば、K1286 §2 と同じ typed 子 mex 解析の
R 強帰納で閉じる見通し（blocker 診断として §5 に登録）。

## §3 宣言前探索実績（explore_k1287.py・出版 kits に同梱）

- 探索は本セッションの実行環境内で実施。探索スクリプト（stage z0/z1/
  z2/frontier 分離・stdout 決定的）: 各面の広域 census で
  FAMILY_SUMMARY bad=0（z0/z1/z2 とも W 576・D 420・E 324・A′ 315・
  A 84 点）、frontier で Am 576・SLB2 88・SLB3 88・L 80 全 bad=0。
- E 族法則の歴史（honest）: 旧読み「E は奇 d → 2（z0/z2）」は
  旧 lawcheck の広域走で bad=96（全て奇 d≥5 の 96 cell）として反例
  検出され、binham 表（d=3 のみ例外的に 2〔z0/z2〕・奇 d≥5 は 0）に
  修正された。旧出力（lawcheck_z0/z2.out・反例行 96）は探索過程の
  一次資料として run log に記録する。
- 例外行の直接確認: W(z=2, m=1, d=1, 全 c) = 2 /
  W(z=0, m=1, d=1): c=2 → 0・c≥3 → 2 /
  D(z∈{0,2}, m=1, d=2) = 2〔z=2, c=2 のみ 0〕/
  E(d=3, c=2, m 1..9): z=1 全 0・z∈{0,2} 全 2 /
  A(z, s, m=1): z=0 [s=1]・z=1 s≥1 全 2〔s=0 は 0〕・z=2 全 0。
- 決定論の事前確認（宣言前 dryrun・ローカル）: PYTHONHASHSEED
  random/1/99 の 3 走で stdout byte-identical
  （sha256 `9e3a61f524af7bdcf7f32a31ceb465b3a63e69e0d86ae25ccee4243f0f8d7594`）。

## §4 機体宣言（verify_k1287.py・kit に同梱）

- kit パス: `research/experiments/multic-web-f2-20261124/`
- 機体: `verify_k1287.py`・sha256
  `52e7eea70090ef41095d19b33de177793a80d7b3a5619ff7708d12ae851fe434`
 （publish 後の fetch-back で byte 照合する）。
- engine block: K1138–K1286 連鎖の公開 block を verbatim 同梱・起動時
  sha256 ゲート。pin =
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
 （K1285/K1286 機体と同一）。engine_block.py 単体ファイルも同梱
  （sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1286 kit と同一 bytes）。
- 電池（合計 **11,743 比較点**・期待 overall_bad = 0・stdout は
  決定的 byte-identical・揮発情報は stderr のみ）:

| gate | 内容 | 点数 |
|---|---|---|
| D1 | W-law: z∈{0,1,2}, d 1..8, c 2..6, m 1..10 engine vs C-SPW | 1200 |
| D2 | D-law: d 2..8, c 2..6, m 1..10 engine vs C-SPD | 1050 |
| D3 | E-law: d 3..8, c 2..6, m 1..9 engine vs C-SPE | 810 |
| D4 | A′-law: d 2..8, c 3..7, m 1..9 engine vs C-SPA′ | 945 |
| D5 | A-law: s 0..6, m 1..12 engine vs C-SPA | 252 |
| D6 | frontier OBS: Am 576 + SLB2 88 + SLB3 88 + L 80 | 832 |
| D7 | 出版アンカー再照合: pure-c1 ラダー [d odd]（K1285 T-L・288）+ D-c1 pair-slice [g odd] 再添字（210）+ T-ALM 六床（72）+ C-PC/C-PB2（66+66） | 702 |
| D8 | T-RC 子恒等式 I1–I11（engine-free・位置代数） | 3132 |
| D9 | mex 不動点証明書: 法則値 == mex(engine 子値)（A/B/C 子の値集合から直接構成・W/D/E/A′/A 箱） | 1458 |
| D10 | 交差エンジン（canonical vs ordered）web 18 spot | 18 |
| D11 | K0832 単一トークン閉形式 vs 両 engine（x 2..9, z 0..3, R 1..21） | 1344 |

- **公式 4 走の期待値（宣言）**: stdout byte-identical・sha256
  `9e3a61f524af7bdcf7f32a31ceb465b3a63e69e0d86ae25ccee4243f0f8d7594`
  （counts `[1200, 1050, 810, 945, 252, 832, 702, 3132, 1458, 18, 1344]`・
  総計 11,743・bad 全電池 0・engine_gate PASS を JSON に含む）。
  宣言前ローカル dryrun（§3）で同一 sha を確認済み。
- TAMPER（事前宣言・各 rc と bad の出現 gate と個数）:
  `--tamper-engine`（rc 2・pin 不一致出力・mutated sha
  `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882`）、
  `--tamper=wlaw`（rc 1・D1 400 + D9 144 = 544 bad）、
  `--tamper=dlaw`（rc 1・D2 600 + D9 192 = 792）、
  `--tamper=elaw`（rc 1・D3 315 + D9 72 = 387）、
  `--tamper=aplaw`（rc 1・D4 945 + D9 270 = 1215）、
  `--tamper=alaw`（rc 1・D5 84 + D9 60 = 144）、
  `--tamper=amlaw`（rc 1・D6 160・他 0）、
  `--tamper=identity`（rc 1・D8 336・I1 の宣言ターゲットを E 族に
  すり替え・d≥3 行 336 点全 bad・他 0）、
  `--tamper=mex`（rc 1・D9 175・子集合を最初の 1 子に制限した場合の
  bad・他 0）。**各フラグの bad 個数は宣言前ローカル実行で確定した
  期待値であり、公式電池で個数まで一致することを検証する**。

## §5 open 登録と K1288 ロードマップ

- **O1（census → 全称の blocker 診断）**: C-SPW/D/E/A′/A の全称化は
  §2 の typed 子帰納で閉じる見通しだが、m=1 の B-exit が要求する
  (i) 単一層族 (x^c)@(x+2+z) plane z+1 の全称則（z=0 は公刊 C-PB2・
  z=1/z=2 は OBS-F2/F3 の SLB2/SLB3 全称化）と (ii) L 族
  （OBS-F4）・Am 族（OBS-F1）の全称化、(iii) 床負域（K1286
  O1/O2/O4・z1/z2 床の m 分裂）が blocker。**K1288 目標**:
  SLB2/SLB3/L の typed 全称証明（C 子は SLB 自身・A 子は L/Am 族で
  web 閉包するかの判定）。
- **O2（C-PC1z1-d4 の c≥2 半分）**: C-SPW の z=1, d=1 行
  （{m,(m+1)^c}@(2m+4, 1) = 0）が c=2..6, m=1..12 で bad=0。
  K1284 open 登録の census 上の解決として登録（全称は O1 待ち）。
- **O3（multi-c web の遠方 c）**: c ≤ 7 まで検証済み。c 方向の法則
  変化は census 範囲内では観測されず、spread 理論（K1285 F2・
  K1286 O3 の継承）として「c 方向に不変」予想を登録（C-SPW 予想は
  c ≥ 2 で全称を狙うが、証明は O1 の blocker 解消待ち）。
- **O4（Am の z=2 異常）**: (m=1, h=2, s=1) のみ 1 という単点異常は
  構造説明がなく OBS のまま。K1289 候補。
- **11×11 巨大探索との接続**: 本項の法則表は multi-c 低 z 面の
  枝刈り格子の評価表としてそのまま使えるが（族点の値が法則表で
  O(1) 即値評価可能・census 箱内）、verdict は不消費・11×11 は
  UNKNOWN のまま。接続は記録のみ。

## Honest 記録

- 本ノートの公式 4 走は push 後の fetch-back 機体から実行する
  （publish-then-execute）。宣言前のローカル runs は dryrun として
  predry/ に保存・成果物に含める。
- 値法則（§1・C-SP*）は有限箱内の census であって全称定理では
  ない。本ノートの全称定理は §2 の恒等式 I1–I11（自明の代数）のみ。
  機体の D9 mex 不動点も有限箱内の機械証明書である。
- E 族法則の旧読み「奇 d → 2」の反例検出（bad=96）は探索過程の
  失敗記録として run log に残す。
- 計算・検証は今回の高速レーン実行環境内で行った（外部リソース
  不使用）。
- 並走レーンとの非接触: Part DF/DG/DL/DH の b28/b31 solver 系
  bookkeeping とは対象が直交。README は全文取得（1,028,444 bytes・
  切断 incident〔e56c8cce〕の再発防止）の上 bullet 追加のみ。
- push の競合・同時書き込み・取得失敗が起きた場合は無理に押し
  進めず、その状況を run log に簡潔に記録して次回の実行に回す。
