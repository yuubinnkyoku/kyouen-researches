---
id: K0855
title: "q∈{2,3}完全退化定理: 任意のq点は共線または共円 — safe⟺|S|≤q−1・極大safe⟺|S|=q−1・w≥2では全幅でwitness存在しM_{w,q}=∞・w=1ではM_{1,q}=q−1・g(S)=((q−1)−|S|) mod 2・非退化はq≥4から"
kind: proposition
status: proved
topics: [rectangles, geometry, grundy, variants]
aliases: []
scope: "標準整数格子の固定幅 w×m 盤・禁止族=直線と円・q∈{2,3}・全 w≥1・全 m ≥ 1。任意の2点は一直線上にあり、任意の3点は一直線上または同一円上にある(非共線の3点は一意の外接円を持つ)。よって q∈{2,3} では全ての q 点部分集合が禁止曲線を含み、盤面のセル数が q−1 以上なら (1) safe(S) ⟺ |S|≤q−1、(2) 極大 safe ⟺ |S|=q−1、(3) w≥2 なら全ての (q−1) 石配置が行欠損(ある行の石数 ≤ q−2)かつ極大なので全幅 m≥1 で欠損 witness が存在し witness 帯=[1,∞)・満容量安定化は決して起きず M_{w,q}=∞、(4) w=1 なら M_{1,q}=q−1、(5) 全極大が同一サイズ q−1 なので通常対戦値は g(S)=((q−1)−|S|) mod 2。q≥4 は最初の非退化 q(共線でも共円でもない safe 4 点集合が存在する)。"
evidence: "全称数学的証明: 幾何的事実(2点→直線・3点→直線または外接円)と各定義(safe・blocked・行欠損・安定化長M)の展開のみで、有限実験に依存しない。q≥4 の非退化性は明示反例 (0,0),(1,0),(0,1),(2,2)(どの直線も4点含まず・(0,0),(1,0),(0,1) の外接円 center=(1/2,1/2)・r²=1/2 に (2,2) は乗らない)。独立機械監査 scripts/q23_degeneracy_check.py(全曲線census: ≥2点の直線全列挙・≥3点の円全列挙、円はrepo既存実装と独立な周心構成+ squared distance 等値判定の純Fraction)が7盤面×q∈{2,3}の14構成で (A) census退化(q点部分集合の全てがcensus曲線上=符号化の健全性)・(B) 全部分列挙(safe⟺|S|≤q−1・極大⟺|S|=q−1、例 3×4盤 4096部分集合・極大数66=C(12,2) ちょうど)・(C) 全空点blocked(K0853定義)・(D) 欠損構造(w≥2: 全(q−1)石配置が行欠損=その幅の全極大がwitness、w=1: 欠損極大なし)・(E) Grundy完全逆算(例 3×4・q=3 の79安全局面すべて g=(2−|S|) mod 2)の5検査を実施し14/14 PASS(output/q23-degeneracy-audit-20261115.json)。"
solution:
  board: 幅w固定長m可変の標準整数格子（w×m・全m≥1）・禁止族=直線と円
  level: strong
  outcome: solved
  classification: [all-safe-grundy, degenerate]
  coverage: q∈{2,3}・全w≥1・全m≥1・全安全局面
  conditions: 連続整数行・セル数≥q−1（(2)(3)(5)の盤面条件）
  verification: [mathematical-proof, exhaustive-finite-audit]
  certificate: 2点の直線決定性・3点の共線/外接円二分と定義展開
  independent_check: 全曲線census 5検査・14構成全PASS・部分集合全列挙・Grundy完全逆算（q23_degeneracy_check.py）
  note: "q=3 では def-mode SAT 符号化は全幅で 2石witness を返す(正の制御族)。欠損 witness 探索・M 値確定の全てが q∈{2,3} で閉形式で解決する"
relations:
- type: depends_on
  target: K0332
  note: "安定化長 M・行欠損 witness・満容量の定義的枠組み"
- type: depends_on
  target: K0853
  note: "blocked(c を通る曲線が ≥q−1 石)の定義。機械監査の検査Cで使用"
- type: supports
  target: K0795
  note: "M_{w,q} 横断表の q<4 コーナーを埋める(w≥2: M=∞、w=1: M=q−1 の4行を results CSV に追加)"
- type: generalizes
  target: K0025
  note: "『残り手数偶奇で Grundy 値が決まる』退化帯の q 側極小例(q≤3)。K0025 は q>2w の w 側巨大帯"
artifacts:
- path: research/experiments/q23-degeneracy-20261115/scripts/q23_degeneracy_check.py
  role: verifier
  note: "独立純Fraction実装。全曲線census(直線≥2点全列挙・円≥3点全列挙・周心構成)と5検査(census退化・全部分列挙safe/極大分類・blocked・欠損構造・Grundy完全逆算)。exit 0 iff 全検査PASS"
- path: research/experiments/q23-degeneracy-20261115/output/q23-degeneracy-audit-20261115.json
  role: data
  note: "7盤面×q∈{2,3}=14構成の監査結果(全PASS)。盤面ごとのcensus規模・部分集合数・極大数・witness数・Grundy整合"
- path: research/experiments/q23-degeneracy-20261115/README.md
  role: source
  note: "定理・証明・監査設計・結果・限界"
- path: results/fixed-width/mwq_stabilization.csv
  role: data
  note: "q∈{2,3}の4行追加(w≥2: M=∞ 2行・w=1: M=q−1 2行)"
- path: research/log/2026-11-15-q23-degeneracy.md
  role: log
  note: "既存性確認(repo検索でM_{w,3}未記録)→証明→機械監査→表統合の記録"
---

## 命題（全称・証明済み）

標準整数格子の固定幅 w×m 盤・禁止族 = 直線と円・q ∈ {2, 3} とする。

**幾何的事実**: 任意の2点は一直線上にある。任意の3点は、共線なら
その直線上に、非共線なら一意の外接円上にある。よって q ∈ {2,3}
では**全ての q 点部分集合が禁止曲線を含む**。

セル数 ≥ q−1 の盤面で:

1. **安全類**: safe(S) ⟺ |S| ≤ q−1。
   q 点以上あればその q 点が禁止曲線を含む。q−1 点以下なら
   どの曲線も q 石を含めない。
2. **極大類**: 極大 safe ⟺ |S| = q−1。
   |S| = q−1 のとき任意の空点 c の追加は q 点をなし、必ず違反。
   |S| ≤ q−2 なら空点を1つ追加してもまだ safe。
3. **witness 構造（w≥2）**: 任意の (q−1) 石配置は行欠損である。
   全行の石数が ≥ q−1（非欠損）であるには合計 w(q−1) 石が
   必要だが |S| = q−1 < w(q−1)（w ≥ 2）なので、少なくとも1行の
   石数は ≤ q−2 である。極大でもあるので、**全幅 m ≥ 1 で
   行欠損 witness が存在**し、
   witness 帯 = [1, ∞)。満容量安定化（全極大が行容量 q−1 まで
   埋まる）は決して起きない: **M_{w,q} = ∞**。
4. **w = 1**: 極大は常に単一行の q−1 石 = 行容量ちょうど。
   よって m ≥ q−1 の全幅で満容量安定化しており **M_{1,q} = q−1**
   （合成分離帯 K0767系/K0795 の極小例と一致）。
5. **Grundy**: 全極大が同一サイズ q−1 なので、全安全局面で

   **g(S) = ((q−1) − |S|) mod 2**。

   空盤からは q−1 手で終了し、最後の手の偶奇が勝敗を決める
   （q=2: 先手勝ち・1手、q=3: 後手勝ち・2手 — 通常対戦規則）。
   なお「q石完成で着手者の勝ち」規則なら逆順になり
   q=2: 2手目完成で後手勝ち・q=3: 3手目完成で先手勝ち（退化により
   3手目は必ず曲線を完成させる）。
6. **非退化の境界**: q ≥ 4 が最初の非退化 q。
   (0,0), (1,0), (0,1), (2,2) はどの直線も4点含まず、
   (0,0),(1,0),(0,1) の外接円（中心 (1/2,1/2)・r²=1/2）にも
   (2,2) は乗らない → safe 4点集合が存在し、
   「全 q 点部分集合が違反」が崩れる。以降の全レード
   （witness 探索・M 確定・Grundy の非自明性）は q ≥ 4 で始まる。
7. **次元备注**: 任意の3点は2次元以下のアフィン部分空間に収まり、
   その中で共線または共円。よって退化は d 次元版でも持続する
   （d次元版の禁止族の定義に依る）。

**証明の本質は2行**: 2点は直線を決め、3点は直線か円を決める。
q ∈ {2,3} の全称主張はこの事実の定義展開であり、(1)〜(5) は
いずれも機械監査が有限盤面で全照合した（下記）。

## 機械監査（独立実装・14構成全PASS）

`q23_degeneracy_check.py` は各盤面で全曲線 census を構築し
（≥2点を通る全直線・≥3点を通る全円。円は repo 既存 checker と
独立な周心構成: 垂直二等分線交点を純 Fraction で解き、
squared distance 等値で所属判定）、次の5検査を実施:

| 検査 | 内容 | 結果 |
|---|---|---|
| A | 全ての q 点部分集合が census 曲線上(符号化健全性) | 0 件見逃し |
| B | 全部分集合で safe⟺\|S\|≤q−1・極大⟺\|S\|=q−1 | 4096/盤・誤分類0 |
| C | 全 (q−1) 石配置の全空点が blocked(K0853定義) | 非blocked 0件 |
| D | w≥2: 全 (q−1) 石配置が行欠損(=全極大がwitness)・w=1: 欠損極大0件 | 全PASS |
| E | Grundy 完全逆算 = ((q−1)−\|S\|) mod 2 | 全安全局面で一致 |

代表値（3×4盤・q=3）: census 49直線+90円・4096部分集合・
極大数 66 = C(12,2) ちょうど・witness 数 66（全極大がwitness）・
79安全局面の Grundy 全一致。7盤面 (1,3),(1,6),(2,3),(2,4),
(3,3),(3,4),(4,3) × q∈{2,3} で全PASS
（`output/q23-degeneracy-audit-20261115.json`）。

## 統合

- results/fixed-width/mwq_stabilization.csv に4行追加:
  - `parametric,w>=2,2,2,INF` / `parametric,w>=2,3,3,INF`
    （witness帯 [1,∞)・満容量安定化なし）
  - `exact-threshold,1,2,2,1` / `exact-threshold,1,3,3,2`
    （単行盤は m=q−1 から安定）
- solver 接続: q=3 の def-mode SAT は全幅で即 SAT（2石witness）。
  符号化・デコーダの正の制御族として使える
  （witness は2石なので復号検査も定数時間）。

## 限界・言っていないこと

- 主張は禁止族=直線と円の標準版に限る。禁止族が片方（円のみ等）
  の変種や多項式超曲面版（K0832 ファイバーゲーム等）には
  そのまま適用しない。
- 有限監査は実装整合の確認であり、全称主張の根拠は数学的証明。
- d 次元版は幾何的事実の持続のみを主張し、d次元版の勝敵・
  安定化長の詳細には踏み込まない。
- 「M=∞」は「満容量安定化が任意の幅で起きない」の意味で
  使い、特定の m での個別記録ではない。
