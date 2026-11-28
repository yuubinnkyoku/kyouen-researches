# 完了log: PG(2,3)/PG(2,4) 最小2重ブロッキング・極大safe族の PGL(3,q) 軌道分類

- 日時: 2026-11-28
- 宣言: `2d910e1b` (research/log/2026-11-28-pg23-pg24-orbit-census-declaration.md,
  宣言時 HEAD pin `fdf1ed8b`・publish-then-execute・単一オーナー)。
  宣言後に追加の並走commitは無し（宣言が実行直前のHEAD）。
- 実験dir: research/experiments/pg23-pg24-min-double-blocking-orbits-20261128/
- K項目: K1372（仮番号・統合時に再採番可能性あり・AGENTS.md規約どおり）

## 実行内容（宣言どおり・クリーン作業dirで最初から再実行）

1. boards.py: GF(3)/GF(4) 独立盤構成。design 検査 PASS
   （PG(2,3) 13点13直線・PG(2,4) 21点21直線、各点対=1直線・各点=q+1直線）。
2. enumerate_families.py: 反射Gray + O(1)違反計数器で全数列挙。
   **較正完全一致**: PG(2,3) 極大safe {4:234} / 最小DB {9:234}、
   PG(2,4) 極大safe {7:360, 9:11480} / 最小DB {12:11480, 14:360}
   （K1370/K1300 出版値どおり）。
3. orbits.py: PGL(3,3) = 5,616 / PGL(3,4) = 60,480 全生成（理論位数と一致）。
   - **PG(2,3)**: 両族とも**単一軌道**（234 each・安定化群 24・oval型。
     PG(2,3) の oval 数 234 は古典値と整合）。
   - **PG(2,4)**: 極大safe = **4軌道**（size7: 360・安定化群168、
     size9: 10,080 + 1,120 + 280・安定化群 6/54/216）。
     最小DB = **4軌道**（size12: 3軌道、size14: 360）。鏡像。
   - 補集合双対 (K1365): 両盤・全件・両方向一致。
4. pgl_vs_pglplus.py: PΓL(3,4)（σ: α→α+1・位数 120,960）でも
   **軌道併合なし**（4軌道とも σ 不変）。
5. verify.py: **ALL_OK**
   - 全 mask 定義直接再検査 fail 0（234+234+11,840+11,840）
   - Gray法と独立な 2^n 直接popcount全走査: 両族の全集合一致
   - 軌道クラス群閉包ランダムサンプリング 50×族×盤 + |orbit| divisibility PASS
   - **Baer同定: PG(2,4) size-7 極大safe 360/360 が Fano (Baer) 部分平面**
     （7本の3点交差直線が 2-(7,3,1)・線プロファイル {1:14, 3:7}。
     PG(2,4) の Fano 部分平面の古典的個数 360 と一致）
6. 再現性: 宣言前スクラッチ実行（宣言に開示済み）と宣言後クリーン再実行で
   mask list 4本 byte-identical・JSON は wall_s のみ差。
   出版キット構成（相対パス版 scripts）からの再実行でも同一（out/*.txt は
   pgorbit2 実行と byte-identical・MANIFEST はキット版 sha を記録）。

## 教訓（fail-closed が機能した例）

- GF(4) の加法を (a+b)%4 とした初版バグ → PG(2,4) design 検査の
  line-size assertion が即捕捉。
- 行列式の中間項の符号（加法のまま）誤り → 特異行列が混入し canon(None) の
  KeyError が即捕捉。両バグとも較正盤の値が壊れる前に検出・修正。

## Non-claims

- 有限盤 PG(2,3)/PG(2,4) のみの結果。「PG(2,q) min = 3q」等の全称主張はしない。
- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts/nodes は
  bookkeeping。

## レジューム（着手前に必ず最新main再取得・hourly並走注意）

- PG(2,5) s=4 の軌道分類は未実施（2^31 全走査はこの手法のスケール外。
  K1370 の非出版 mask list（MANIFEST sha pin `89681f9c` / `d381fe68`）を
  用いるか対称性割り込みが必要）。
- PG(2,9) Baer 部分平面対による 3q 未満候補の厳密判定（K1371 レジューム (d)）
  は未着手: Baer 対の交差census → min |B1∪B2| = 26 − max|∩| で上界が決まる。
- 他レーン所有中の 8x29 / n11 / six-row 系には不参入。
