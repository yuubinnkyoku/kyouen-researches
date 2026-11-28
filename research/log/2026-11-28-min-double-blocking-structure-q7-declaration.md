# 2026-11-28 最小2重ブロッキングの構造分類 + q=7 SAT 決定 — 単一オーナー宣言 (publish-then-execute)

- Task: K1370 (t2-blocking-duality-20261128) で得た最小 t=l−s 重ブロッキング集合の
  構造理解を深める 2 部構成の高速レーン作業。
  1. **構造分類**: 出版済みリスト `output/lists/ag2q4s2.minimal.txt` (48個 size-10,
     120個 size-12) と `ag2q5s3.minimal.txt` (9,000個 size-14, 28,000個 size-15,
     12,500個 size-16) を用い、最小 2 重ブロッキング集合の AGL(2,q) 軌道 census・
     line-profile (各直線との交点数の多重集合) 不変量・正準形を決定。
     size-10 (q=4) と size-14 (q=5) の最小サイズ族の構造比較から q 方向の一般則の
     候補を抽出する（予想としてのみ記録し、全称主張はしない）。
  2. **SAT による q=7 決定**: AG(2,7) (49点) と PG(2,7) (57点) の 2 重ブロッキング
     (全直線が C の点を 2 個以上含む) の最小サイズを、k を下から順に
     「|C| ≤ k で 2 重ブロッキングが存在するか」の SAT 判定 (UNSAT/SAT 境界) で
     正確に決定。必要なら AG(2,8)/PG(2,8)/AG(2,9)/PG(2,9) にも拡張。
     PG(2,q) min=3q 有限観察 (q=3,4,5, K1370) の q=7 検証が本丸。
     SAT は決定問題であり、全数列挙ではない。SAT 側の witness は構造分類
     (line-profile・軌道) で補完し、UNSAT 側は列挙なき下界として記録する。
- Method: 
  - 構造分類は純 Python (board file を GF(q) から独立再構成して照合の上、
    AGL(2,q) (q²·|GL(2,q)| = 12,000 @ q=5) の全変換で軌道正準形を計算)。
    入力 mask は C 列挙器の hex 出版値をそのまま使用し、
    safety/blocking/minimality の再判定 (定義直接) で検証。
  - SAT は kissat 4.0.4 (pin sha256 21da5d98... 公開済み pin と同一バイナリ)。
    DIMACS は専用 encoder (Python) で生成: 各直線の at-least-2 制約
    (clause 数 q+1/直線) + 総数 at-most-k (sequential counter)。
    **較正**: 同一 encoder/solver で q=3,4,5 (AG・PG) の既知最小値
    (PG: 9/12/15, AG: AG(2,4) 10, AG(2,5) 14) の UNSAT/SAT 境界を完全再現
    することを宣言後に最初に確認する (K1370 出版値との較正)。
    PG(2,7)/AG(2,7) は GF(7) から盤を独立構成し 2-(v,q+1,1) design を検査。
- Pre-declaration 事実確認: 最新 main HEAD 261432360e (2026-11-28T07:32Z 再取得)。
  eighteenth ladder-top pillars (n11 系) は別レーンが宣言済みで非衝突。
  AG(2,5)/AG(2,4) 最小ブロッキングの構造分類と AG(2,7)/PG(2,7) の SAT 最小決定は
  現時点で未着手 (K1370 は計数のみで構造分類なし・q=7 は未測定)。
- Execution plan (この宣言の出版後): 較正 → 分類 (q=4, q=5) → q=7 SAT 決定 →
  (時間が許せば q=8, q=9) → kit・完了 log・K 項目 (要件を満たせば) の出版。
- Non-claims: 有限盤の完全な構造記述 (分類) と SAT による決定結果の出版である。
  min |C| = 3q (PG) 等の全称命題は予想のまま主張しない。
  SAT witness の「全数」は測定しない (最小サイズの決定のみ)。
  標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
- Declaration-time HEAD: 261432360e30462e9ed67977229fd421bb7af20e
- この宣言は本 session の本セルの単一オーナー宣言。同一セルの並走実行は defer すること。
