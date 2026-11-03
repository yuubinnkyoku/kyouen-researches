> **実験一次資料**：本文の判定・数値・計画は記録時点のものです。現在の結論・status・未解決の唯一の正本は[knowledge](../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

# 8×8の層別Grundyプロファイル、J_8、飽和開始層の再計算（2026-11-01）

## 目的

K0006は8×8の全6,700,711,937安全局面のGrundy DPを完走済みだが、保存された集計は
層別状態数・P/N数・最大安全サイズ・p_rand統計のみで、**層別Grundyヒストグラム、
1石層・2石層のg値、J_8グラフは残っていない**。そのため次の未解決項目が
「n=8のデータがない」まま止まっている：

- [K0113](../../knowledge/items/K0113-losing-first-move-odd-nimber-open.md)：負け初手後の1石nimberは奇数
- [K0119](../../knowledge/items/K0119-jn-losing-board-connectivity-open.md)：後手勝ち盤のJ_n連結（n=8未検査）
- [K0182](../../knowledge/items/K0182-all-losing-first-moves-few-nimbers-open.md)：全初手負け盤の1石nimber種類数
- [K0183](../../knowledge/items/K0183-saturation-missing-nimber-contiguity-open.md)：飽和開始層の欠番は連続しない
- [K0184](../../knowledge/items/K0184-saturation-missing-nimbers-powers-of-two-open.md)：欠ける正のnimberは2の冪だけ

本実験は同じ全局面DPを**Grundy値だけ**に絞って再実行し、層別プロファイル・
J_8・飽和開始層σ_8を新規に取得する。p_randは再計算しない（K0006の別実装が既存）。

## 方法

1. **列挙**（既存検証済み列挙器を無変更で使用）：
   `round5_prand_stream.cpp --enum 8` がsort-free v-max partitionで全安全集合を
   石数層ごとに生成し、ソートされたu64マスク列 `level_k.occ` をspill先へ書く。
   メモリ0.3GB、歴史的所要時間約22分。
2. **Grundy専用ストリーミングDP**（新規 `scripts/grundy_only_stream_solve.cpp`）：
   子層マスクをmmap、親層をチャンクで逐次読み、DP値はint8 gのみ（1 B/state）。
   最広層ペア（L9+L10）でも匿名メモリ約4GB。mexは子gのビットマスクから。
   各層の `dp_k.bin`（g値配列、indexはlevel_k.occと一致）を保存し、
   層別ヒストグラム・M_8(k)・天井達成証人・根のgをJSONに出力する。
3. **後処理**（`scripts/postprocess.py`、Python標準ライブラリのみ）：
   - 1石層：値の種類・奇偶（K0113/K0182）
   - 2石層：g({p,q})=0の辺を持つJ_8グラフの連結性・次数分布（K0119）
   - 全層：M_8(k)、天井K_8−k初達成層σ_8、D_8(k)=K_8−k−M_8(k)の単調性（K0041回帰）、
     σ_8層の実現nimberと[0,K_8−σ_8)の欠番（K0183/K0184）

## 記憶域の注意

C:ドライブ（WSL ext4 VHD搭載）の空きが約8.7GBしかなく、n=8 spill（約54GB）を
拡張できないため、列挙spill・dp_k.binはすべて `/mnt/d`（D:、空き約1TB）に置く。
drvfs上のmmap・preadをn=3スモークテストで確認済み。

## 再現

```sh
# WSL内。バイナリは恒久場所 /home/yuubi/kc_build にビルド
g++ -O3 -march=native -std=c++20 -fopenmp -o /home/yuubi/kc_build/stream \
  research/experiments/original-claims/scripts/round5_prand_stream.cpp
g++ -O3 -march=native -std=c++20 -fopenmp -o /home/yuubi/kc_build/grundy_solve \
  research/experiments/n8-grundy-layer-profiles-20261101/scripts/grundy_only_stream_solve.cpp

# 1. 列挙（約22分、spillはD:）
OMP_NUM_THREADS=12 /home/yuubi/kc_build/stream --enum 8 --spill=/mnt/d/kyouen-spill8 \
  > /mnt/d/kyouen-spill8/enum.json 2> /mnt/d/kyouen-spill8/enum.log

# 2. Grundy DP（約30分予、匿名メモリ約4GB）
OMP_NUM_THREADS=12 /home/yuubi/kc_build/grundy_solve 8 --spill=/mnt/d/kyouen-spill8 \
  --out=/mnt/d/kyouen-spill8/solve.json 2> /mnt/d/kyouen-spill8/solve.log

# 3. 後処理
python3 scripts/postprocess.py 8 /mnt/d/kyouen-spill8 /mnt/d/kyouen-spill8/solve.json \
  output/n8_analysis.json output/n8_J8_edges.txt
```

n=7回帰（同一パイプラインの検証）：spill7regで同手順を実行し、
層サイズ・P/N数・M_7(k)・σ_7=4・J_7（49頂点552辺連結）・1石層全g=1・
天井証人mask=9044480(g=10)が既知値と一致した。
成果物は `output/n7_grundy.json`、`output/n7_analysis.json`、`output/n7_J_edges.txt`。

## 独立検算

- 層サイズ・全状態数・P/N数・g(root)をK0006の歴史的p_rand DP（別実装）と照合
- M_8(k) ≤ K_8−k の定理不変式を全層で確認（K0041）
- J_8連結性をunion-findとBFSの二方式で確認
- dpファイルからのmex再計算で1石・2石層のg値を標本照合
- n=7回帰で全パイプラインを歴史値と一致（K0119/K0113/K0042の記録値を再現）

## 範囲と限界

- 通常プレイのGrundyのみ。misère補助値h、p_randは対象外。
- n=8のみ。n=10のP盤1石層は本実験では計算しない（状態数が桁違い）。
- 有限盤の計算であり、K0113/K0119/K0182/K0183/K0184の無界全称は証明しない。
- spill・dpファイル（約61GB）は再生成可能なためrepoには保存せず、
  小さい成果物（JSON・辺リスト・解析結果）のみoutput/に置く。

## 結果

2026-11-03にWSL Ubuntu（16コア、12スレッド）でn=8を完走した。列挙34分（20:15–20:49 JST、rc=0）、Grundy DP 37分（20:49–21:24 JST、rc=0、peak RSS 17.75GB）、postprocess即時。

**列挙の再現**（`n8_enum.json`）：禁止四点14,564（Python/C++両方で一致）、安全局面数 6,700,711,937、最大安全サイズ K_8=15、層サイズ [1,64,2016,41664,620812,6784816,53020968,281902248,956468384,1921019144,2092205428,1112723392,254143028,21240760,535844,3368]。K0006の歴史的集計（安全局面数・層数・K_8・禁止四点数）と完全一致。

**DPの集計**（`n8_grundy.json`）：P=1,457,674,065、N=5,243,037,872、g_root=0、M_8(k)=[0,3,4,6,11,10,9,8,7,6,5,4,3,2,1,0]。層サイズ・層別P/N数・M_8(k)はK0006記録（n8_analysis.jsonの`ceiling_invariant_M_le_K_minus_k: true`、D_8(k)=[15,11,9,6,0,…] 単調非増加）と一致。2,232.6秒。

**独立検算**（`n8_analysis.json`）：
- 禁止四点数はPython/C++で両方 14,564、一致
- mex再計算：1石層 64/64一致、2石層 300/300一致
- σ_8=4 最適証人は mask=148032（idx 2558）、g=11 を独立再計算で確認
- J_8：64頂点・1,380辺・孤立点なし・union-find/BFSの二方式でいずれも1成分（連結）。次数min=11/max=59

**五つの未解決項目への含意**（有限盤の証拠であり、無界全称は証明しない）：
- K0113：全64初手が負け手（後手勝ち盤）。一石局面の非零Grundy値は {1（12点）, 3（52点）} のみで、すべて奇数
- K0119：n=8のJ_8は連結（二方式一致）
- K0182：初手負け盤の一石nimberの種類数は 2
- K0183：σ_8=4層で欠番なし（realized [0..11]、missing=[]）。∴ 連続する欠番の反例は存在しない
- K0184：σ_8=4層の正の欠番は存在しない（真空に「2の冪」を満たす）

**成果物**：`output/n8_enum.json`、`output/n8_grundy.json`（層別集計・Grundyヒストグラム）、`output/n8_analysis.json`（後処理・独立検算）、`output/n8_J8_edges.txt`（1,380辺）。spill（level_k.occ・dp_k.bin、約61GB、`/mnt/d/kyouen-spill8`）とsolve/enumの生logは再生成可能なためrepoには保存しない（enum約22〜34分、DP約37分、D:空き945GBを利用）。
