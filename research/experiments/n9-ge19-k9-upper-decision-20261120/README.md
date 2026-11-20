# n9 ge19 (K_9 上界) 決着レーン — part1: 検証基盤・正負制御・較正 (2026-11-20)

単一オーナー宣言: `research/log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md`
(commit 21f8610464d2711f768b5764d23b21a40295dee5)。本 dir はその受け入れ条件に従う。

## 目的

9×9 盤の安全 19 石配置 (4 点が同一円上・同一直線上にない配置、安全条件は
`det[x^2+y^2,x,y,1]≠0`) の存在判定 = `n9_ge19` の SAT/UNSAT。
UNSAT ⟹ W9 (18石証人, n9-k9-upper-sat-20261115) と合わせ K_9=18 が repo 内で確定。
SAT ⟹ 19 石 witness の独立検証を経て K_9>=19 (先行的外部上界 18 の反証)。
**判定は main には反映済みの既知値 (K0029 表) と矛盾しない有限盤面の完全判定としてのみ扱う。**

## 現在の状態: INDET (判定に必要な 2 系一致の高速側が未決着。不在・上界の主張は一切しない)

- 判定対象 `n9_ge19_strong.cnf` (後述の強化符号化) の fastsat 直接実行は未着手。
  理由: 較正条件「n7/n8 既知 UNSAT を fastsat で閉じる」が未達のため
  (ラダーゲート方針: 小さい既知 UNSAT で 2 系一致が取れないものを対象に投げても
  確証にならない)。
- 2 系のうち探索系 (ksearch.js) は n7-15 UNSAT を fresh に再現 (下記)。
  SAT 系交差 (fastsat) は n5-10 UNSAT で一致を確認済み、n7/n8 は予算内 TIMEOUT。

## 今回確定した事実 (すべて再現手順つき、FNV で固定)

### 1. 強化 CNF 符号化 (gen_strong_cnf.js)

`--n=N --k=K --out=DIR` で `n${N}_ge${K}_strong.cnf` と変数マップ `.map.json` を生成。

- cell 変数 p+1 (p=row-major index)。
- forbidden quads: 全曲線 (直線 92 + 円 6722 for n=9) の各 4 点組に
  `-(a+1) -(b+1) -(c+1) -(d+1)`。計 F_9=29,152 節 (Σ C(t,4) = F と一致、
  相異なる曲線は 3 点以上共有しないため重複なし)。
- at-least-K 逐次カウンタ (forward 全セル順) + **冗長強化**:
  (S1) 曲線ごとの at-most-3 逐次カウンタ、(S2) 逆順 at-least-K カウンタ。
  (S1)/(S2) は共に forbidden quads から論理的に従う冗長付加であり、
  cell 変数上の SAT/UNSAT 判定を変えない (sound な付加節のみ、と宣言条件どおり)。
- 出力メタ: n9_ge18_strong 89,607 vars / 278,036 clauses / FNV-1a-64 `d7ffb2bca4a7664f`
  n9_ge19_strong 89,733 vars / 278,538 clauses / FNV-1a-64 `83f9407a12eff3ea`

生成記録 (本レーン、--n=5..9 すべて 8 種):
n5_ge9 `c3285b8f0fd92df8` (3,391v/10,496c), n5_ge10 `38c7b8812150babc` (3,423v/10,622c),
n7_ge14 `bd74017aef24e6a5` (22,047v/68,232c), n7_ge15 `0f3ee7fe14af06d4` (22,117v/68,510c),
n8_ge15 `3b2f3650de9d0fd1` (47,014v/145,328c), n8_ge16 `f674302dae5c3fb7` (47,112v/145,718c),
n9_ge18 `d7ffb2bca4a7664f`, n9_ge19 `83f9407a12eff3ea`。

### 2. 正負制御 (eval_strong.js, すべて PASS)

eval_strong.js は CNF と .map.json と witness cell 列を読み、
すべての補助変数を**定義の意味論** (prefix/suffix 個数の大小比較、曲線ごとの個数) から
独立に値決定し、全節を評価する第三系。あわせて witness の安全性を 4x4 整数行列式で
全 4 点組について直接再検査する。

| witness | K ( Stones ) | 対象 CNF | 結果 |
|---|---|---|---|
| W5 (naive fresh) | 5 (9) | n5_ge9_strong | WITNESS-SAT (10,496/10,496 節、forbidden quads 0) |
| W5 | 5 (9) | n5_ge10_strong | VIOLATION (違反は fwd/rev の at-least ユニット 2 節のみ) |
| W7 (naive fresh) | 7 (14) | n7_ge14_strong | WITNESS-SAT (68,232/68,232) |
| W7 | 7 (14) | n7_ge15_strong | VIOLATION (ユニット 2 節のみ) |
| W8 (naive fresh) | 8 (15) | n8_ge15_strong | WITNESS-SAT (145,328/145,328) |
| W9 (既刊 18石) | 9 (18) | n9_ge18_strong | WITNESS-SAT (278,036/278,036、det4 再検査 forbidden 0) |
| W9 | 9 (18) | n9_ge19_strong | VIOLATION (ユニット 2 節のみ: var 1449 (fwd a[81][19]) と var 89733 (rev r[81][19])) |

W9 = [5,6,8,9,11,18,24,31,44,47,50,52,54,55,70,73,75,79] (既刊、変更なし)。
fastsat 由来の新 witness: n5_ge9 (9石) cells [2,4,5,7,11,12,21,23,24] —
eval_strong + det4 で完全検証 (第三系一致)。W5 と異なる解であり、
SAT 側のモデル復号パイプラインが機能していることを示す。

### 3. センサス較正

- naive.js (4 点組全列挙 det4): F_5=826, F_7=6,364, F_8=14,564 — 既刊値と一致。
- gen_strong_cnf.js 内カタログ (n=9): F_9=29,152、直線 92 本、円 6,722 本 —
  既刊 catalog (lineCatalog total 92 / circleCatalog total 6,722) および
  n9-k9-upper-sat-20261115 の n9_census_cnf JSON と一致。
  quadClauses=29,152=ΣC(t,4) で、曲線 4 点組に重複なし (相異なる 2 曲線は
  最大 3 点を共有できないため、各 forbidden quad はちょうど 1 曲線に属する)。

### 4. 探索系 (ksearch.js v3c) 較正

- n7 target=15 (既知 UNSAT): **UNSAT**, 11,880,598 nodes / 17.4s /
  boundChecks 9,096,190 / boundPrunes 1,563,258 (fresh, 本レーン)。
- lane 内既応算: K_5=9/10, K_6=11/12, K_7=14/15 の SAT/UNSAT 全再現、
  n8-16 は 220s/518M nodes で INDET (ksearch 単独では n9-19 には遠い)。

### 5. fastsat 交差較正 (既刊 fastsat, pinned @2e9ec4c5…)

| インスタンス | 既知判定 | fastsat 結果 |
|---|---|---|
| n5_ge10_strong | UNSAT (K_5=9) | **UNSAT** 12,583 conflicts / 2.6s — 2 系一致 ✓ |
| n5_ge9_strong | SAT (K_5=9) | **SAT** 178 conflicts / 0.1s、モデル検証済み |
| n7_ge15_strong | UNSAT (K_7=14) | TIMEOUT 280s / 197,359 conflicts (既定 opts) |
| n7_ge15_strong (portfolio) | UNSAT | TIMEOUT 90s ×3: cellphase=0 / seed=7 / base=64 (65k-73k conflicts) |
| n8_ge16_strong | UNSAT (K_8=15) | TIMEOUT 280s / 82,904 conflicts |
| n9_ge19_strong | 判定対象 | 未実行 (ラダーゲート未達のため) |

実行環境: 1.0 CPU / 約1GiB / Node 20 (sandbox)。fastsat の衝突率 約700-750 conf/s であり、この符号化では n7-15 すら閉じられない。UNSAT 側の決着には
(1) より長い連続予算、(2) fastsat 改造 (minimization 既定 ON・イベント間隔調整)、
(3) 探索系の chunk 分割 resume (宣言方法 (a)) のいずれかが必要。

## バグ追跡 (notes/strong-encoding-bugfix-tracking-20261120.md に詳細)

gen_strong_cnf.js は本レーンで 2 件の符号化バグを発見・修正した。
1 件目 (鏡像節内のリテラル 0 出力 = 不正 DIMACS) は構造検証+正制御で、
2 件目 (j==i 対角・境界の上界鏡像欠落 = カウンタ意味論の不健全化) は
**既知 UNSAT ネガティブ制御** (fastsat が n5_ge10 に 0 conflicts で SAT を返した) で
捕捉された。2 件目は制御実験なしには偽 SAT/UNSAT として沈黙しうるクラスであり、
同型パターン (逐次カウンタの定数置換) の既刊 gen_n9_cnf.mjs を監査した結果、
こちらは定数置換が正しく健全であることを確認した (参照のみ、変更なし)。

## ファイル構成

```
scripts/ksearch.js        専門探索 (包含/除外 DFS, 曲線at-most-3伝播, aliveFuture bound)
scripts/naive.js          最小仮定参照探索 (SAT witness 採取・F 再計算)
scripts/gen_strong_cnf.js 強化 CNF + 変数マップ生成 (使用法: --n=9 --k=19 --out=DIR)
scripts/eval_strong.js    CNF+witness の意味論的全節評価・det4 安全性再検査
scripts/fastsat.js        既刊 CDCL の pinned copy (@2e9ec4c547d1bed5d277bda1eea37c39767f79ef)
                          ※ HEAD は research/experiments/sat-fastcdcl-20261114/scripts/fastsat.js
results/controls-and-ladder-20261120.json  上記をまとめた生の数値
notes/strong-encoding-bugfix-tracking-20261120.md  符号化バグの特定→修正→再検証の追跡
```

## 再開手順 (次回の実行)

1. 最新 main を確認 (他レーンとの競合回避)。
2. `node scripts/gen_strong_cnf.js --n=9 --k=19 --out=OUT` で FNV `83f9407a12eff3ea` を照合。
3. 較正ゲート: fastsat で n7_ge15_strong / n8_ge16_strong の UNSAT を閉じる
  (長時間連続実行または高速化後)。閉じたら n9_ge19_strong に着手。
4. ksearch 系: 宣言方法 (a) の min(S) 場合分割チャンク (n8-16 → n9-19) を resume 対応で。
5. 両系一致でのみ判定出版 (K item + K0029 注記 + README 未尾 bullet、3 段階)。
   予算内 undecided なら本 README と results への INDET 追記のみ。
