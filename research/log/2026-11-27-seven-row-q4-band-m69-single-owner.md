# 単一オーナー宣言: 7行・q=4 幅69 witness band 延伸 (2026-11-27)

- 宣言日時: 2026-11-27T05:45Z
- 宣言時 HEAD: `b782b8468b5e0a0336b6bc74a9c617c905ca108c` (main)
- 単一オーナー: 高速レーン (本実行)。他の hourly 実行は本宣言の作業領域に着手しないこと。

## 目的

`research/experiments/seven-row-q4-witness-band-60plus-20261121/` の前線 7×69
(M_{7,4} ∈ [69, 1929], witness 帯 m=4..68) を進める。

## 作業内容 (受入条件)

1. **幅69全基底 fresh 2-for-2 完全掃引**: 出版済み全199基底
   (`output/w68/bases.json`, sha256 `d8e977ec…`) の幅69 fresh 2-for-2 近傍を
   `enum_two.js` (sha256 `ab58c34a…`, 出版mainの byte-clone) で完全列挙する
   (`sweep69.js` 手順・較正として width69 の w68 witness 基底は
   rcc 2,141,205 / safe 199,290 / maximal 0 を再現済み)。
2. **D4鏡像×並進 census** (K1211 手順): 全基底の4鏡像×並進で幅69被覆の
   純並進 witness の有無を機械判定する。
3. witness が発見された場合は 3系統独立整数検証 (出版 `verify_witnesses.py`
   正規化整数方程式系 + `verify_third.py` 素朴4×4行列式系 + 遮断曲線census)
   を全件に実行し、さらに greedy chain で幅70以降の延伸を試みる。
4. 0件の場合は局所負の記録として出版 (不在主張はしない)。

## 主張の範囲

- 本作業は M_{7,4} の下界 (witness 構成的下界) のみを更新しうる。
  上界 1929 (K0068) は不変。`results/fixed-width/mwq_stabilization.csv` は
  K1201/K1209/K1211 前例どおり更新しない。
- 計算結果は有限機械検証であって数論的証明ではない。
  checked/safe/maximal 計数を勝敗として読まない。
- **標準11×11空盤・二石root {60,27}・第三手 {100,108}・S2・closure class は
  本作業と無関係で全時点 UNKNOWN・verdict 不消費。**
