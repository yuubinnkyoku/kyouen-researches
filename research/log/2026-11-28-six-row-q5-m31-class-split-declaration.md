# 宣言: six-row q=5 6x31 class {2} krow/minpos 分割 (single-owner, publish-then-execute)

- 日時: 2026-11-28T02:05Z (本宣言出版時点)
- 宣言時 HEAD: `d5eaaba675c22f4bdd4f6f7e1dbd77962d36326b`
- オーナー: 高速レーン (本 session)。他レーンは本セル (6x31 (6,5)) に宣言なしを commit 列と KNOWLEDGE resume で確認済み。

## 対象

(6,5) フロンティア幅 6x31 (w=6, m=31, q=5)。現況 M_{6,5} ∈ [31,658]
(mwq_stabilization.csv bounds,6,5,5 行)。6x31 は K0815 の weak な pool-relative 負記録
(~99.8% uOverflow incomplete-skip, not absence) のみで、class-split 掃引は一度も実施されていない。

## 計画 (publish-then-execute)

1. ** SAT側優先**: 単一欠損 class {2} (V-mirror で class {3} を被覆: w=6 では V: y→5-y が row2↔row3 を交換するため class {2} の掃引は class {3} を代表する) の krow=2:3 (欠損行は3石) を
   minpos (欠損行の最左石の列位置) で分解し P=0 から昇順に掃引。
   sound minpos 上限は floor((m-1)/2)=15。
2. **各片は cold pair (run1/run2) で実行**、cap は各走 270s (SIGTERM cut は honest negative として記録)。
3. **WIN-stop 則**: どれかの片で SAT が出たら以降の片・残り class ({0},{1})・多欠損 class は掃引しない。
4. SAT の場合は witness を decode し、sat.js verifyConfig (census-free integer) と
   fresh Python exact-Fraction verifier (verify_frac.py, 出版正本 sha256 `837fe24b…`) の
   2独立系で検証。tamper 陰性対照 (remove/add) を実施。
5. SAT なら M_{6,5} 下界 31→32 を csv 行へ反映 (bounds,6,5,5 の M 列 "31..658"→"32..658")。
   UNSAT/INDET のみの場合は csv 不変・honest negative のみ記録。

## 事前較正・対照 (宣言時点で実施済み、開示)

- **Toolchain calibration (bit-exact)**: 6x20 q7 class {2} plain —
  kissat 4.0.4 (sha256 `21da5d98…`, 公式 linux-amd64) SAT **641,859 conflicts**、
  出版対照 (seven-row-q7-m27-class-split-20261128/output/r6x20q7_c2.txt) と完全一致。
  sat3.js/sat2.js/sat.js は同 kit 出版正本と sha256 完全一致
  (`e04581eb`/`14ceb854`/`fcc0cfd8`)。
- **(6,5) family positive control**: 6x20 q5 class {2} krow=2:3 (同一 encoder/family/q) が
  SAT で witness を返すことを掃引前に確認する計画 (bit-exact 対照は存在しないため、
  encode-decode-verify の健全性確認として位置づける)。
- 6x31 q5 class {2} krow=2:3 minpos=0 CNF は事前生成済み:
  vars 110,036 / clauses 383,665 / 6,737,908 bytes / md5 `9233874fd01277fccdf6aadff102a271`。

## 明示しないこと

- 全片 UNSAT/INDET でも 6x31 の witness 不在は主張しない (INDET は time-cut)。
- class {0}/{1}、多欠損 class、minpos>P の片は WIN-stop もしくは cap 到達で未掃引のまま。
- 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は
  本レーンと無関係で全時点 UNKNOWN。verdict は不消費。conflicts/nodes は bookkeeping。

(実行はこの宣言の push 完了後に開始する)
