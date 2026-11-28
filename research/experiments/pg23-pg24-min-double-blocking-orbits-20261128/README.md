# pg23-pg24-min-double-blocking-orbits-20261128 — PG(2,3)/PG(2,4) 最小2重ブロッキング・極大safe族の PGL(3,q) 軌道分類

宣言: research/log/2026-11-28-pg23-pg24-orbit-census-declaration.md
(commit `2d910e1b`, 宣言時 HEAD pin `fdf1ed8b`)。K1370
(t2-blocking-duality-20261128) のレジューム候補 (b)「PG(2,3)/(2,4) 出版リストの
PGL(3,q) 軌道分類」の実行。K1371 が AG(2,4)/AG(2,5) 側を完了済みのため、
本実験は PG 側のみを扱う。

## 結果（すべて有限盤・全数。検証は定義直接 + 独立全走査 + 群閉包サンプル）

### PG(2,3) s=2（直線4点・t=2）
- 極大safe: 234 個（size 4 のみ）。**PGL(3,3)（位数 5616）で単一軌道**
  （安定化群位数 24・oval と整合。PG(2,3) の oval 数 234 は古典値と一致）。
- 最小2重ブロッキング: 234 個（size 9 のみ = 3q）。**単一軌道**
  （size-9 は size-4 極大safe の補集合そのもの）。
- 補集合双対（K1365）: 全234対で両方向一致。

### PG(2,4) s=3（直線5点・t=2）
- 極大safe 11,840 個 = **4 PGL(3,4) 軌道**:
  - size 7: 1 軌道（360 個・安定化群 168）。
    **全 360 個が Baer (Fano) 部分平面**（7本の3点交差直線が 2-(7,3,1) design、
    線プロファイル {1:14, 3:7}、360/360 検証）。PG(2,4) の Fano 部分平面の
    古典的個数 360 と一致。
  - size 9: 3 軌道（10,080 + 1,120 + 280 = 11,480・安定化群 6 / 54 / 216）。
- 最小2重ブロッキング 11,840 個 = **4 軌道**（size 12: 3 軌道 10,080+1,120+280、
  size 14: 1 軌道 360）。鏡像構造。
- 補集合双対: 11,840 対で両方向一致。軌道単位でも対応。
- **PΓL(3,4)（σ: α→α+1 を追加した位数 120,960）でも軌道併合なし**
  （4軌道はいずれも σ 不変）。

## 手法・検証（すべて fail-closed）
- scripts/boards.py — GF(3)/GF(4)（加法=XOR・α²=α+1）独立構成 +
  2-(v, q+1, 1) design 検査（点対=1直線・各点 q+1 直線）
- scripts/enumerate_families.py — 2^n 反射Gray走査 + O(1)違反計数器
  （violating/deficient）による極大safe・最小DB全数列挙
- scripts/orbits.py — GL(3,q) をスカラー正規化して PGL(3,q) 全生成
  （q=3: 5,616 / q=4: 60,480、位数は理論値と一致）・rep からの全群像による
  厳密軌道分割・線プロファイル
- scripts/pgl_vs_pglplus.py — σ を含む PΓL(3,4) での軌道併合確認
- scripts/verify.py — (i) 全 mask の定義直接再検証（fail 0）(ii) Gray 法と
  独立な 2^n 直接 popcount 全走査で全集合一致 (iii) 軌道クラスの群閉包
  ランダムサンプリング 50×2 + |orbit| | |PGL| 割り切り確認 (iv) 補集合双対
  両方向全件一致 (v) size-7 の 2-(7,3,1) 検査（360/360 Fano）
- out/ — boards.json, enumeration.json, orbits.json, pgammal.json, verify.json,
  mask list 4本（234+234+11,840+11,840）
- 較正: K1370/K1300 出版値 PG(2,3) 4:234/9:234・PG(2,4) 7:360, 9:11480 /
  12:11480, 14:360 を完全再現。
- 再現性: 宣言後のクリーン再実行で mask list 4本 byte-identical、
  JSON は wall_s のみ差。キット構成（相対パス版 scripts）からの再実行でも
  同一。

## Non-claims
- 有限盤 PG(2,3), PG(2,4) のみ。「PG(2,q) の min = 3q」等の全称主張はしない。
- Baer 部分平面との同一視（size-7 極大safe = Fano 部分平面）は有限全数の
  機械検証による同定であり、一般 q への外挿はしない。
- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
