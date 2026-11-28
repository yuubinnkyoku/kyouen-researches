# 完了log: PG(2,5) s=4 軌道分類 (全数・計13軌道) — 2026-11-28

- 宣言: research/log/2026-11-28-pg25-s4-orbit-census-declaration.md (commit `26d82430`)
- 実験dir: research/experiments/pg25-s4-orbit-census-20261128/ (単一commit)
- 知識項目: research/knowledge/items/K1375-pg25-s4-orbit-census.md (仮番号)
- 実行環境: Vibe 高速レーン (GitHub API 出版のみ・ユーザーPC到達不可)

## 結果

**PG(2,5) s=4 極大 safe 1,587,975 個は PGL(3,5) (372,000) 作用下でちょうど 13 軌道。**
size 13: 1軌道 (15,500・stab 24) / size 14: 1軌道 (372,000・stab 1=regular) /
size 15: 5軌道 (186,000/124,000/93,000/186,000/15,500・stab 2/3/4/2/24) /
size 16: 6軌道 (186,000/124,000/3,100/186,000/93,000/3,875・stab 2/3/120/2/4/96・120=S5型)。
補集合双対 (K1365) で最小 DB 15..18 族に転写。K1370 レジューム (c) 完結。

## 実行記録

1. **enum.c** (zig cc 0.13.0, tarball sha `d45312e6`): PG(2,q) 汎用 DFS。較正として
   PG(2,3) s=2 {4:234}・PG(2,4) s=3 {7:360, 9:11,480} が K1300/K1355 出版値と完全一致。
   PG(2,5) s=4 fresh 再実行 (nodes 668,359,659・dumped 1,587,975・~12s) は宣言前スクラッチ
   ダンプと byte-identical: sha256 `9af9a06a3565520c278aa1b7d91e201d10fc9d67fa366b80508dfa7f8a6dbfc8`
   (6,351,900 bytes)。補集合の 2重ブロッキング性・最小性は記録時全件 fail-closed 検査済み
   (fresh_counts.txt: 極大/最小のサイズ別個数が K1370 と双対ミラーで完全一致)。
2. **orbits.js** (Node.js): 生成元 4個で PGL(3,5) 全要素 BFS (位数 372,000 検証)。
   1,587,975 mask をサイズ別軌道分割、各軌道の安定化群位数は 372,000 全要素での
   固定元全数で直接計数 (orbit×stab=372,000 fail-closed)。生成元集合変更で
   分割が不変であることも検証 (独立宣言済み)。out/orbits25s4.json に全 13 軌道の
   rep (最小mask)・line_hist・sample members 付き。
3. **verify.py** (Python・アフィンモデル): C ラベリング→アフィンラベリング写像は
   C 直線 31 本の像が全て直線であることで fail-closed 検査。
   - verify mode: size 13/14/15/16 全 1,587,975 mask の安全性・極大性・補集合最小DB性
     を定義直接再検査、全件 PASS (bad 0)。
   - orbit mode: Python 独自生成元で PGL(3,5) 再構成 (位数 372,000 一致) →
     サイズ別独立再分割が JS 分類と完全一致:
     13 [15500] / 14 [372000] / 15 [15500,93000,124000,186000,186000] /
     16 [3100,3875,93000,124000,186000,186000]・全 JS rep の所属・軌道サイズ照合 PASS。
   - **開示**: 初版は無限遠点正規化の誤り ((v0/v1,1,0) と (1,v1/v0,0) の取り違え) で
     生成群が PGL(3,5) を超えて膨張し BFS が異常終了 (exit 137・出力は counts で停止)。
     修正後に位数がちょうど 372,000 となり全照合 PASS。verify mode (群不使用) は無影響で、
     修正前後で同一結果。

## 出版・検証鎖

- 宣言 `26d82430` (宣言時HEAD `709c8515`) → 本完了 commit (HEAD `a0cede2f` の上に単一commit)。
- 6.35MB mask dump は非出版 (sha pin のみ・enum.c 再実行で byte-identical 再生成可能)。
- fetch-back: kit 全 file を API で読み戻し byte 一致を確認 (下記追記予定)。

## 状態

- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・verdict 不消費。
- 次の候補 (高速レーン): PG(2,5) s=4 の Grundy 計算は重い (局所探索でなく全状態必要) ので
  長期レーン扱い。size-16 高対称軌道 (stab 120/96) の幾何学的特徴付け (S5 型安定化群の
  幾何学的記述) は軽く有望。

## 追記 (同日・構造addendum)

本体出版後も同じ実行内で構造解析を実施し、orbit16-2 = conic∪内部点
(3,100 = conic総数)、orbit16-5 = 三角形の辺上にない点 (3,875 = 三角形総数)
の完全特徴付け、size-13 軌道と 4-arc の stab 同一性・個数一致を得た。
out/structure-addendum.md に詳細。K1375 に追記セクションを反映。
