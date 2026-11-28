# t2-blocking-duality-20261128 — t>=2 補集合双対性の6盤確認と新規計数

宣言: research/log/2026-11-28-t2-blocking-duality-declaration.md (commit 9def08790034abc9f87f02203cfd027a7a3733e8, 宣言時HEAD 775e1a6)。所有セル: K1365 補集合双対性の t=l-s>=2 初確認（PG(2,3) s=2, PG(2,4) s=3, AG(2,4) s=2, AG(2,5) s=3, PG(2,5) s=4 の5盤）+ AG(2,3) s=2 の t=1 小盤。並走レーン（n11 系・8x29 系・7x28 系・6x26 系等）とは非衝突。

定義（K1365 と同一）: 集合 S が s-安全 ⟺ 全直線が S の点を高々 s 個含む（≤s、すなわち <s+1）。S が極大安全 ⟺ s-安全でどの点も追加できない。C が t=l-s 重ブロッキング ⟺ 全直線が C の点を t 個以上含む。極小 ⟺ どの点も除去できない。

## 主張（有限全列挙による計算結果）

各盤で 2^n 全部分集合を1回の Gray-code 走査で判定し、極大安全集合と最小 t 重ブロッキング集合を同時列挙、要素レベルで補集合全単射（C = P∖S、両方向 0 fail）を確認した。

| board | n | l | s | t | 極大安全 サイズ:個数 | 最小t重ブロッキング サイズ:個数 |
|---|---|---|---|---|---|---|
| AG(2,3)  | 9  | 3 | 2 | 1 | 4:54 | 5:54 |
| PG(2,3)  | 13 | 4 | 2 | 2 | 4:234 | 9:234 |
| AG(2,4)  | 16 | 4 | 2 | 2 | 4:120, 6:48 | 10:48, 12:120 |
| PG(2,4)  | 21 | 5 | 3 | 2 | 7:360, 9:11,480 | 12:11,480, 14:360 |
| AG(2,5)  | 25 | 5 | 3 | 2 | 9:12,500, 10:28,000, 11:9,000 | 14:9,000, 15:28,000, 16:12,500 |
| PG(2,5)  | 31 | 6 | 4 | 2 | 13:15,500, 14:372,000, 15:604,500, 16:595,975 (計 1,587,975) | 15:595,975, 16:604,500, 17:372,000, 18:15,500 (計 1,587,975) |

### 新規の計数（公開値と照合できるものは照合済み）
- PG(2,3) s=2 極大 4:234 = K1300 の極大アーク数と一致。最小2重ブロッキング 9:234 は新規（最小サイズ 9 = 3q）。
- PG(2,4) s=3 極大 7:360, 9:11,480 = K1355 出版値と一致。最小2重ブロッキング 12:11,480, 14:360 は新規（最小 12 = 3q）。
- AG(2,4) s=2 極大サイズ集合 {4,6} = K1300 と一致、個数 120/48 は新規。最小2重ブロッキング 10:48, 12:120 は新規（最小 10）。
- AG(2,5) s=3 極大サイズ集合 {9,10,11} = K1357 と一致、個数 12,500 / 28,000 / 9,000 は新規。最小2重ブロッキング 14:9,000, 15:28,000, 16:12,500 は新規（最小 14）。
- PG(2,5) s=4 は両側とも新規（2^31 全走査、数秒/回。リスト 14MB×2 は出版せず MANIFEST の sha256 pin のみ）。

### 較正（宣言前に実施・output/calibration/）
t=1 の4盤（AG(2,4) s=3, PG(2,3) s=3, PG(2,4) s=4, AG(2,5) s=4）で本列挙器は出版値を完全再現: 総数 1,240 / 247 / 10,741 / 36,475、サイズ別内訳も完全一致（K1367, K1356+K1366, K1366, K1364）。

### 有限観察（全称主張ではない）
- PG(2,q) の最小2重ブロッキングの最小サイズは q=3,4,5 で 3q。q=7 は n=57 (2^57) で全列挙不可、別手法が必要。
- AG(2,q) t=2 の最小サイズは q=4: 10, q=5: 14（生値のみ記録、式の主張はしない）。
- PG(2,5) s=4 の極大サイズ 13..16 は偶奇混在。K1298 から G>=2 の存在が示唆されるが、本実験では Grundy を計算しておらず主張しない。

## non-claims
- K1365 の命題自体は既に証明済み。本キットは t>=2 での要素レベル確認と新規計数の出版であり、命題の新証明ではない。
- 標準11x11空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
- 全結果は有限盤の完全列挙に基づく。無界一般化（例: min |C| = 3q for all q）は未証明。

## 手順・検証（3系統、scripts/canon.sh で完全再現可能）
1. scripts/blocking_duality.c — 2^n Gray-code 全走査で両側（safe/maximal と blocking/minimal）を各 mask で独立に直接判定し、要素レベル両方向補集合照合。全6盤で2回実行し stdout・リストとも byte-identical（output/runs/）。zig 0.13.0 build（repo pin と同一 tarball）。
2. scripts/verify_duality.py — GF(q)（q=3,4,5; GF(4) は加法 XOR）から盤を独立再構成し 2-(v,k,1) design を検査、board file 自身の design 性も検査、dump された全 mask（PG(2,5) は 1,587,975×2 mask、約3分）の safety/maximality/blocking/minimality を直接定義で再判定、補集合全単射・個数一致を確認（output/verify/、全盤 all_ok=true）。導出盤（ラベル順が異なる独立構成）で C 列挙器を再実行し count 完全一致。
3. scripts/brute_third.py — 純 Python 第三全列挙（Gray code 不使用・直接定義判定）。n≤25 の5盤（PG(2,3), AG(2,3), AG(2,4), PG(2,4), AG(2,5)）で C 列挙器と完全一致（output/brute/brute_third.txt、AG(2,5) は約15分）。PG(2,5) n=31 は対象外（系統2が全 mask 検証を担う）。

盤ファイル: PG(2,3)/PG(2,4) = ../projective-blocking-kyouen-20261125/output/board_pg2q{3,4}.txt、AG(2,3)/AG(2,4)/AG(2,5) = ../s-parameter-kyouen-20261125/output/board_ag2q{3,4,5}.txt、PG(2,5) = boards/board_pg2q5.txt（本キット同梱、verify_duality.py の GF(5) 構成・2-(31,6,1) 検査済み）。

## files
- scripts/ — 列挙器 (blocking_duality.c)・独立検証器 (verify_duality.py)・第三列挙器 (brute_third.py)・counts 抽出 (counts_from_run.py)・再現手順 (canon.sh)
- boards/board_pg2q5.txt — PG(2,5) 導出盤
- output/runs/ — 列挙器生 stdout 2回分 x 6盤
- output/calibration/ — t=1 較正4盤の stdout
- output/counts/ — サイズ別個数 JSON（盤別 + all_counts.json）
- output/verify/ — Python 独立検証器出力（全盤 all_ok=true）
- output/lists/ — mask リスト（AG(2,5) まで、hex 1行1 mask）
- output/brute/brute_third.txt — 第三系統
- output/summary.json — 全盤まとめ
- output/MANIFEST-sha256.txt — 全ファイル + 非同梱 PG(2,5) リスト 2本の sha256 pin
