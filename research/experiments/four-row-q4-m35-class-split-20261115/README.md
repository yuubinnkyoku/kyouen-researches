# (4,4) 4×35 class-split k×minpos 掃引 — IN FLIGHT (2026-11-15 高速レーン)

## 位置づけ

`M_{4,4} ∈ [35, 237]` (witness 帯 m=4..34、上界 K0068 T_4=237、K0833)。
前線 m=35 を** absence-capable に決着する**ための完全分解掃引。
先行する honest negatives — def-mode 260s INDET 317,151 conflicts
(four-six-row-q4-q5-band-extension-20261115)、lex=H rowY=0/1 2クラス被覆
600s INDET 324,870/230,642 (four-row-q4-q5-frontier-20261115) — の
完全分解版が本掃引である。

## status

**IN FLIGHT** — resumable driver `sweep35.sh`。1インスタンス1行を
`output/records.jsonl` に追記し、既に記録済みの key は再実行しない
(環境リセット越えの再開可能。CNF は決定的再生成)。
この dir は掃引の進行に合わせて増分 push される。
1件 700s cap (env `CAP`)・実効 CPU ~1コアのため全82件の完了には
複数セッションを要する見込み。

## 被覆の完全性論証 (absence-capable cover)

4×35 の行欠損極大安全配置 (deficient maximal witness) の非存在は、
次の分解で**完全に被覆**される (いずれも sat3.js class-split 符号化):

1. **9 正準クラス (mod V)**: V (垂直鏡映) は行 0↔3・1↔2 を送り、
   欠損行集合 D (石数 ≤ q−2 = 2 に強制される行) を保存して
   {0}≡{3}, {1}≡{2} と同一視する。D の正準代表は9個:
   {0}, {1}, {0,1}, {0,2}, {0,3}, {1,2}, {0,1,2}, {0,1,3}, {0,1,2,3}。
   クラス外の行は exactly q−1 = 3 石 (full) に固定、クラス内の行は ≤2 石。
2. **単一クラス {0},{1} の k×minpos 分解**: 欠損行の正確な石数
   k ∈ {0,1,2} (`--krow=y:k`・chain 単位ピン) で分解し、k≥1 は
   さらに minpos で分解。欠損行の石を列 x₁<…<x_k とすると
   `min(x₁, (m−1)−x_k) ≤ floor((m−1)/2) = 17` が常に成り立つため、
   minpos p ∈ 0..17 の18点で各 H-pair を被覆できる
   (H は行を保存するため class・krow と両立する。**sound H-split**)。
   k=0 は minpos 不要の1点。
3. **multi クラス (7個) は直接**: 各欠損行 ≤2 石・石数は未固定。
   `--class=D` のみで sound。
4. **符号化は全インスタンス lex なし**: minpos ピンと lex=H の併用は
   H-pair の両要素を同時に落としうる (unsound) ため使用しない。
   lex なしは常に sound (探索空間は広い分、UNSAT は強い)。
   最難 multi クラスへの lex=H 交叉符号化確認は完了時に追加予定。

合計 82 インスタンス = 陽性対照 1 + {1}k2 p0..17 (18) + {0}k2 p0..17 (18) +
multi 7 + {1}k1 p0..17 (18) + {1}k0 (1) + {0}k1 p0..17 (18) + {0}k0 (1)。

**全 UNSAT ⟹ 4×35 欠損極大不在が確定し
M_{4,4} = 35 or ≥ 37** (K0821-audit 規約: 35 が witness-free でも
36..236 に witness があれば M ≥ 37)。
**いずれか SAT ⟹ witness 帯は m=4..35 に拡大し M_{4,4} ∈ [36, 237]**。
SAT 発見時は model → decode → `verify_witness.py` (Python Fraction)
の2系統検証を driver が自動実行して記録する。

## 優先順・対照

- **陽性対照 (4,34,4) class {1} k=2 minpos=7**: m=34 witness の
  V∘H 像 (rows [3,2,3,3]・欠損行1の石 (20,1),(26,1) → H 鏡像で左端 7)
  を含むので SAT が正解。driver は SAT なら witness を記録して全掃引を停止。
  ただし m=34 は (4,4) 帯の難化前線 (事前 probe 240s で 1,052,475
  conflicts 未決着・`output/r_ctrl_4x34_c1k2p7.txt`) であり、
  cap 700s でも INDET になりうる。その場合は pipeline 較正 (CNF 生成・
  kissat 実行・記録) のみを検証したと解釈する (判定には影響しない)。
- その後の歴史的 witness 軌道優先: {1}k2 → {0}k2 → multi direct → k1 → k0。

## 較正・決定性

- sat3.js = sat2.js (K0810 コア) 上の class-split/krow/minpos 拡張。
  census は sat.js 全三つ組 (4,35,4) 41,607 曲線 —
  surgery4.js buildCensus4 とも完全一致
  ([four-row-q4-m35-surgery-20261115](../four-row-q4-m35-surgery-20261115/)
  の census 完全性検査 8/8 PASS)。
- kissat 4.0.4 公式静的バイナリ (md5 3a5eba830aa6008a604fcc9bbe99a325)。
  CNF 生成・ソルバとも決定的 (record に cnf_md5 を記録)。
- records.jsonl の time-cut 値 (cap 到達 INDET) の conflicts は
  同一軌跡の壁時計打ち切りであり bit-exact ではない旨をここに明記する
  (UNSAT/SAT 判定は決定的)。

## 副次記録: (6,4) m=47 rowY=0 の kissat RAM 壁

(6,4) 前線 m=47 の rowY=0 固定分割 (sat3 streaming 7r 版) は
CNF 生成成功 (vars 2,701,853 / clauses 8,965,702 / curves 259,412・
CNF md5 e2c7ab7255893ea4e974a479bd04c8f3) 後、kissat 4.0.4 が
rc=137 (SIGKILL/OOM) で 14.3s で死亡。sandbox RAM ~2.1GB が壁で、
cap 900s に到達する前に殺される。m=45 まで動作していた frontier レーン
(最大 581s) との対比で (6,4) rowY 固定分割の環境 RAM 境界は m=47。
INDET/OOM であり不在主張ではない。生記録は
[six-row-q4-m47-rowY0-oom-20261115](../six-row-q4-m47-rowY0-oom-20261115/)。

## files

- `scripts/sat3.js` — class-split / krow / minpos 符号化 (sat2.js 上)
- `scripts/sat2.js` — K0810 def-mode コア (lexLeader・S 再エクスポート)
- `scripts/sat.js` — K0810 census・検証器
- `scripts/verify_witness.py` — Python Fraction 検証 (第2系統)
- `sweep35.sh` — resumable driver (root に置いて実行)
- `output/records.jsonl` — 1インスタンス1行の進行記録 (増分 push)
- `output/r_ctrl_4x34_c1k2p7.txt` — 事前 probe 240s の対照生ログ


## 追記 (2026-11-15 bugfix)

- `sweep35.sh` に2つの欠陥を修正した (commit 同日):
  (1) 陽性対照が SAT だと SATFOUND=1 のまま後続ループに入り、
  掃引全体が誤終了する bug — 対照直後に `SATFOUND=0` をリセット。
  今回は対照が cap 700s INDET (rc=124) だったため顕在化しなかった。
  (2) conflicts 抽出の `grep -E "^c conflicts"` が kissat ログの CR を
  含む行で binary 判定になり、対照 record の conflicts が null に化けていた —
  `grep -a -E` に修正。対照の真値はログから復元可能
  (output/ctrl_4x34_c1k2p7.txt の最終 "c conflicts" 行)。
- 2026-11-15T08:49Z に lane の一時停止で c1k2p0 を 161.3s で打ち切った
  (rc=143・conflicts 367,338)。この truncation record は records.jsonl から
  除去済みで、resume 時に cap 700s で再実行される。
- 同レーンの (4,21,5) 姉妹掃引 (four-row-q5-m21-class-split-20261115) は
  この修正版 driver 構造で運用中。


## 追記 (2026-11-15 bugfix v2: skip 経路の per-key SAT 判定)

前記 (1) の修正 (対照直後の SATFOUND=0 リセット) は**不十分**だった。
真の root cause は run() の skip 経路
`done_key "$key" && { grep -q "\"result\":\"SAT\"" records.jsonl && SATFOUND=1; … }`
が records 全体から SAT を探す点にあり、**対照の SAT record が存在する限り
resume 後の最初の skip で SATFOUND=1 が立って掃引が即終了する**
(姉妹掃引 four-row-q5-m21-class-split-20261115 の再開時に実際に発生・
1回の誤終了 SWEEP_BATCH_DONE satfound=1 を観測して発見)。
v2 では skip 時の SAT 判定を同一 key の record に限定した。幸い
本掃引 (sweep35) では対照が INDET だったため一度も誤終了していない。


## 追記 (2026-11-15 hardening: resume skip の key 前衝突防止)

skip 経路の key 照合 `grep "\"key\":\"$1\""` (done_key) は部分一致のため
`c1k2p1` が `c1k2p10`..`c1k2p17` の record 行にも一致しうる
(prefix-collision)。records 破損で p1 の record のみ失われた場合、
p1 が p1x 行で**誤 skip され被覆の完全性が黙って損なわれる**。
照合 pattern を `"key":"$1",` / `"key":"$key",` (閉じ quote + comma
anchor) に強化した。全 record 行は `{"key":"...","w":...` 形式で
key 値の直後に comma が必ず続くため既存 record と完全互換
(判定結果は不変)。姉妹掃引 four-row-q5-m21-class-split-20261115 の
sweepp0x2.sh (`b1` vs `b10..b19`)・sweepp0gpin.sh (`g1` vs `g10..`)
にも同種の衝突があり、同日修正済み。
