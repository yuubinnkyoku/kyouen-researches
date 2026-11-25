# six-row q5 (6,5) 6×31 band extension（2026-11-22）

単一オーナー宣言 `bc11e28b`（[2026-11-22-six-row-q5-m31-band-extension-single-owner-note](../../../log/2026-11-22-six-row-q5-m31-band-extension-single-owner-note.md)・宣言時HEAD `bcc39add`）の実験一式。
高速レーン・下方界更新のみを主張する。

## 主張

- **6×31 q=5 に23石の行欠損極大安全witnessが存在する**（rows `[4,4,4,4,4,3]`・maxx 25・23石）。
  石座標は `w6x31q5_L2shift1.json`（sha256 `245adc6d…`）。K0815 第6弾の L2 6×30 witness
  （`L2_c630_def.json`・conflicts 4,001,401・本実験 `verify/L2_pub.json` に正本複製）の
  **x+1 純並進**（maxx 24→25）で与えられる。
- よって **M_{6,5} ∈ [32,658]**（下界のみ更新）。6×32 以降の不在は一切主張しない。
- 同一石集合は `free_append_reach=31`・`witness_widths [26,31]`、すなわち単一石集合で
  **幅26..31の6連続staircase**（c008 の [26,30] を更新し、(6,5) の単一集合最幅広記録）。

## 検証プロトコル（宣言受入条件・全PASS）

3系統の独立検証器で witness を検証し、陰性対照（tamper×2・5同行）と
陽性対照（出版済み L2 6×30 witness の同経路再現）を添えた（`scripts/run_verify_suite.sh`・
生の出力 `output/verify-suite/`）。2回実行（run A/B）は `diff -r` で byte 一致（決定性）。

| 系統 | 実装 | witness @6×31 | L2 陽性対照 @6×30 |
|---|---|---|---|
| (a) surgery_gen.js | 整数正準曲線鍵・全盤 blocked 走査 | WITNESS_OK（safe/maximal/deficient・maxline=4・maxcirc=4・unblockedEmpty=0） | WITNESS_OK |
| (b) det_q_verify.py | 純3×3/4×4行列式ゼロ判定（det3/det4） | safe + maximal_at_m=31（163空点全blocked）・rows OK | safe + maximal_at_m |
| (c) append_criterion.py | 純Python Fraction・出版pin byte一致（sha256 `d08d8fb1…`） | safe・old_uncovered 0・free_append_reach 31・first_unblocked [31,5] | reach 30 |

陰性対照（全て FAIL・`output/verify-suite/tamper*_sys*.txt`・`nc_line_sys*.txt`）:

- tamper1（石 `[14,5]`→`[15,5]` 移動）: (a)(b) rc=1、(c) `safe:false`（maxcirc 5・5-on-curve出現）・old_uncovered 2
- tamper2（`[13,0]` 除去 + `[26,0]` 追加）: (a)(b) rc=1
- 5同行制御 `[[0,0]..[4,0]]`: (a)(b) rc=1（unsafe）

## 純並進census（配置 band top）

公開済み (6,5) m≤30 witness プール（K0808・six-row-q5-q6-frontier-20261120・K0815 第1/5/6弾）の
15 iso-config（D4像込み、`config/pool.json`・`scripts/pool_builder.py`・`scripts/census_shift.py`）について
x-offset 全走査（maxw=50・`append_criterion.py` Fraction 判定）を行った
（`output/translation-census-summary.json`・15 config の covered_ranges/band_top 全数掲載）。

- band top 31 に達する配置は **c009（L2）の offset+1 のみ**（[26,31]・本witness）。
- c008 は [26,30]、c006/c010 は 29止まり。
- **maxw=50 の走査窓内に reach ≥ 32 の配置は皆無**（限定観察・母集団censusではなく不在主張ではない）。

## 6×32 frontier surgery（限定的陰性・オープンのまま）

6×32 盤（w=6・169空点）で witness 構成を試みた編集近傍探索。**全て陰性であり、
6×32 witness は UNDETERMINED のまま**（不在主張ではない）。

base pool: 15 iso-configs × 全 offset の 6×32 配置 165個の unblocked（4石マスク不在空点）数を
census（`output/unblocked_w32.json`・ヒストグラム {1:2, 2:8, 3:14, 4:9, …, 13:15}）。
unblocked ≤ 3 の **24 base** を編集起点に選んだ。

engine `surgery_deep.js`（sha256 `851e5b7b…`・core は surgery_gen.js と byte-verbatim）で
以下のクラスを走査（`output/w32-bounded-edit-negatives.json` に全数記録・per-base candidate 数）:

- `r0s`（rem k add 0・k=1..4・完全）: 24/24 base 陰性
- `r1a1`（rem1 add1・3,887候補/base・完全）: 24/24 陰性
- `r2a1`（rem2 add1・42,757/base・完全）: 24/24 陰性
- `r3a1`（rem3 add1・299,299/base・完全）: 24/24 陰性
- `r4a1`（rem4 add1・1,496,495/base・完全）: 24/24 陰性
- `t2`（rem3 add2・targeted-complete）: **c009@off3 のみ完走** — target (31,5) の D-set 74点 →
  9,731 pair × 1,771 removals = **17,233,201 候補・0 witness**
  （生記録 `output/base-000-t2-c009off3.json`）。残り23 base は checkpoint で resume 可能。

t2 の targeted-completeness: rem3add2 witness W = base − R + A は base の各 unblocked target u を
≥4 W石の曲線でブロックする必要がある。u は base で unblocked（u を通る曲線の base 石数 ≤3）で
kept ⊆ base なので covering curve は必ず add を1個含み、その曲線は ≥2 の base 石を持つ
（covering curve の kept ≥ 4−|A∩C| ≥ 2）。よって各 target の covering add は
D(u) = {u} ∪ {u を通る ≥2 base 石曲線上の空点} に属し、この必要条件を満たす pair のみ
全 C(23,3) removal と交差列挙する（見逃しなし・engine `targetDSet` + header 註記）。
add は base の空点に限定し、「除去石位置への再加算」は純除去クラス r0s に帰着させて閉じている。

## 再現

```sh
# witness 3系統検証 + 対照 + 陽性対照（dir root から・2回実行して diff -r で一致確認）
bash scripts/run_verify_suite.sh A
# 純並進census
python3 scripts/census_shift.py   # pool.json → census/*.json（要 kit 側出力）
# 6×32 surgery（例: 最良base c009@off3 の全クラス + t2 resume）
node scripts/surgery_deep.js config/config_w32_u3.json 0 24 r0s,r1a1,r2a1,r3a1
node scripts/surgery_deep.js config/config_w32_u3.json 0 24 r4a1
node scripts/surgery_deep.js config/config_w32_deep_v1.json 0 1 t2   # 200s/budget 切替で数呼び出し
```

## 境界・非主張

- `mwq_stabilization.csv` は不変（K1201 前例）。上界 T=658（K0806 代入・K0815 記録）不変。
- witness_widths [26,31] overt claim は free-append 判定（K0853/K0854）に基づく構成的事実。
- candidate 数・checked 数は勝敗ではない。6×32 編集近傍陰性は「公開プール配置の
  k≤4R≤1A・3R2A 近傍」という限定スコープの負記録である。
- 標準 11×11 空盤・二石root・S2・class 1/2/4・n11 系レーン: 非接触・UNKNOWN のまま。
