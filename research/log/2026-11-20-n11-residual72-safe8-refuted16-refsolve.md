# n11 残余72行 safe8 pool の REFUTED-D10 16根除外後再解決（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-safe8-refuted16-refsolve-single-owner-note.md](2026-11-20-n11-residual72-safe8-refuted16-refsolve-single-owner-note.md)
（commit 9cf2f8d5）の下で、K1086（add-two greedy 23根 depth-10掃引）
README「次の一手」第2項を実施した。**行の閉鎖claim・証明書抽出・receipt fold
・probe実行は行っていない**。記録したのは幾何・組合せの計画簿記のみである。

- 機械: `research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/scripts/safe8_refuted16_refsolve_20261120.py`
  （stdlibのみ・universe82/coverage/demand/greedy計画の独立再導入込み・全16 gate fail-closed）
- 正本: `research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json`
  （SHA-256 `16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724`）
- 実験README: 上記実験dir `README.md`（16代替根の全表・解釈規約・次の一手込み）

## プロトコルと入力の信頼境界

K1085 census正本（SHA-256 `5fdd342d…`）とK1086掃引正本（SHA-256 `3045e152…`）
のみをfail-closed pinで読む。本実験はrunnerを呼ばず、K1086のverdictを
（両AND順序 uncapped・cap 0・error 0のpinごと）そのまま使う。trust境界は
「engine depth-10 verdict健全性 + D4不変性」で全出版verdictと同一。

## 結果（16/16 gate PASS・3実行byte-identical）

- **K1085 universe82・safe8・demand・coverage crosscheck（39,255根）・
  greedy 23根計画（根順序と主張被覆行の両方）を独立再導入で完全再現**
  （publishされた実験機械を用いず、正本2点からの再計算のみで一致）。
- K1086 verdict join: 7 WIN8 + 16 REFUTED = greedy 23根と集合一致、
  72行はgreedy計画上 23行（WIN側）+ 49行（REFUTED側）にちょうど分割。
- 除外後 pool P（120,458根）での残余49行:
  - **stranded行0**（demand min 1,713・max 2,943・合計109,719。
    safe8全域からの低下は各行高々1）。
  - **greedy 16根が残余49行をleftover 0完全被覆**（gains {4:3, 3:11, 2:2}）。
    下界ceil(49/4)=13に対し+3根。
  - **二部最大マッチング49**: 全49行に互いに異なる被覆根が存在。
  - **WIN8 7根の内在被覆（全C(8,6)=28削除）は主張23行と完全一致**:
    residual49への幾何学的余剰なし。将来のWIN8 receipt foldは残余49行の
    需要構造を変えない（scope1=scope2同一16根で機械保証）。
  - 全体計画: **7 WIN8根（23行）+ 16代替根（49行）= 23根で72行**
    （最元のgreedy計画と同数の23根）。代替16根は未掃引で、depth-10掃引には
    両AND順序32 probesを要する（候補であり証明書ではない）。

## 決定性の確認

同一cwd2回+別cwd別プロセス1回の計3実行で正本JSON byte-identical
（SHA-256 `16b38d04…`）。stdlibのみ・逐次・乱数・時刻・wallを正本に含まない。
coverage crosscheckの39,255根はK1085出版のchecked_rootsと同一の抽出規則
（被覆≥2のsafe8根すべて+sorted順60番目ごと）で同一数。

## 解釈規約（再掲）

greedy/witnessは**条件付き計画（候補根の簿記）であり証明書ではない**。
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## 次の一手（着手時は単一オーナー宣言を要する）

1. 16代替根のdepth-10掃引（両AND順序・cap 30M・pilot_d6制御・32 probes・
   K1086 protocolと同一条件）。
2. WIN8-D10 candidate 7根の証明書抽出（windfall型extractorの8石拡張）・
   独立二重検証（別の単一オーナー宣言を要する）。
3. 掃引でさらにREFUTEDが出た場合の段階的除外と再解決の反復
   （stranded構造が出るまで需要は尽きない見込み: demand min 1,713）。
