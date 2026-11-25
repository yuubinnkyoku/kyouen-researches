# s-パラメータ共演ゲーム: キャップ・ゲームとブロッキング・ゲーム（宣言・2026-11-25）

## 目的

共演ゲームの「各ブロックと高々 3 点」という条件の **3 をパラメータ s に一般化**し、
盤ごとの s-スペクトルを調べる。とくに:

- **s = 2（キャップ・ゲーム）**: どの直線とも高々 2 点 = アーク／キャップ。
  `PG(2,q)` では ovals/hyperovals、`AG(2,q)` では complete caps が極大集合。
- **s = q−2（ブロッキング・ゲーム）**: 補集合が 1 重ブロッキング集合。
- **s = 3**: 既存の共演ゲーム（K1058/K1253、K1293、K1295）。

K1298 の parity-graded 補題（全極大安全集合のサイズの偶奇が一様 ⇒ Grundy ∈ {0,1}）を
3 つの盤族で検証する。

## 盤

- `PG(2,q)`: 出版済み `projective-blocking-kyouen-20261125/output/board_pg2q*.txt`。
- `AG(2,q)`: `PG(2,q)` から 1 本の直線を無限遠線として除いて構成
  （`scripts/build_ag2.py`、点対の一意性を全数検査）。q=2,3,4,5。

## 手法

- 安全集合の完全列挙（DFS、増分カウント）→ サイズ降順の DP で Grundy・misère を計算。
- n ≤ 25 では `bytearray(2^n)` に Grundy を格納（`scripts/grundy_general.py`）。
- 極大集合のサイズ・個数、パリティ、Grundy 分布を記録。

## 期待する結果

- `PG(2,q)` の s=2: 全極大 = 最大サイズ（graded）→ Grundy {0,1}。
- `AG(2,q)` の s=2: complete caps により極大サイズが混在。q ≤ 4 は偶数のみ
  （parity-uniform）→ Grundy {0,1}、q=5 で奇数・偶数混在 → Grundy 2 が出現、と予想。
- `AG(2,4)` の s=3（ブロッキング）: 極大サイズ 8/9 混在 → Grundy 2。

## 成果物

- `scripts/build_ag2.py`, `scripts/grundy_general.py`
- `output/board_ag2q*.txt`, `output/grundy_general.json`, `output/*.log`
- `report.md`, K項目、独立検証
