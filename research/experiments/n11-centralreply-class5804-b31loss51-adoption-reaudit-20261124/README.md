# Part DL — batch-31 (class 5804) 51-LOSS canonical adoption (b31loss51)

2026-11-24。単一オーナー Part DL。**11×11 空盤は引き続き UNKNOWN**
(verdict 不消費)。本実験dirは class 5804 の batch-31 51行 fresh LOSS を
canonical chain に接続した記録であり、勝敗の決着ではない。

## 何が確定したか (機械観測)

- canonical chain head (merged cache):
  `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache`
  sha256 `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`
  (6,405行・264,619 bytes・WIN 158 / LOSS 6,247)。
  BASE `04b0a239…` (Part DB, 6,354行) + `output/increment-b31loss51-20261124.cache`
  `e750a0e6…` (51行 fresh LOSS, node 合計 237,596,711, 2-pass node-exact)
  を fail-closed union merger (CU byte-clone 90711961…) で併合。
- batch-31 は probe-complete: 55/55 キーが honest label を持つ
  (51 LOSS・3 WIN-HALT (ad024/ad028/ad055)・1 15M EXHAUSTED (ad043,
  DI 30M reprobe で supersede: WIN (1, 18,247,029))。
  manifest `ae06f855…` (schema b31loss51-increments-manifest-v1)。
- **WIN 4行 (ad024/ad028/ad043/ad055) はどこにも消費していない**:
  increment にも merged cache にも含まれず、class 5804 は unknown のまま
  (unknown 55 → 4, rank 38 → 4)。WIN 行の scrutiny は C++ 第二実装
  オーナー gate (9193f5b6…) に属する。
- refresh (reaudit): class status 計数は不変 (free_now 38 / excluded_now 23 /
  unknown 34,498 / excluded 390)。update8 は resolved 141 → 142 (ちょうど
  1行、ad009 s5 148458)、remaining 31,718 → 31,717。joint greedy union
  36,903 → 36,854、probe worklist 64,765 → 64,711 (いずれも scheduler
  bookkeeping で coverage 主張ではない)。
- decomp deltas: `output/decomp-deltas-b31loss51-adoption.json`
  `0af301b8…` (54+ gate、独立 2 tree で byte 一致)。

## インシデント (honest)

宣言 (commit `00e17cda…`, 2026-11-24T08:20:29Z) と本 wave 出版の間に
実行環境が reset され、宣言前の作業成果物が消失した。宣言 bytes から
全入力 (249 file, 逐 sha 検証) を再取得・再構築し、独立 tree で
公式隔離 rerun (maker → merger ×3 → refresh → extractor) を実施して
全 pin を再現した。再構築に伴い tool/output sha が変わったものは
amendment `research/log/2026-11-24-part-dl-b31loss51-adoption-incident-amendment.md`
の supersede 表が正本。merged cache `60222707…` をはじめデータ系 pin
は宣言どおり不変。

## 文字衝突の記録 (honest)

本 Part の文字「DL」採用に際し、同日 08:11:41Z に batch-30 ac013 reprobe
レーン (Part DK A scaffold, commit `890e6186…`, 宣言 `e411045b…`) が
先に「DK」を出版済みだった。part 文字の割当は先着順のため本 Partは
「DL」を採用した (declaration 冒頭に明記済み)。DK→DL の間に DH/DJ が
他レーンで使われた形跡は本期間の log にない。

## 検証手順 (第三者用)

1. repo を clone し、`reaudit/output/probe-worklist.csv` だけ再生成
   (体積のため未出版): DL 側は本dir `reaudit/scripts/refresh_adoption_b31loss51.py`
   を本dir上で実行 (`006ccd78…` に byte 一致)。BASE 側は Part DB dir の
   refresh script を DB dir 上で実行 (`4ecb9a0a…`)。
2. `scripts/compare_deltas_b31loss51_adoption.py` を本dir上で実行:
   54+ の pin gate が全て PASS すれば、published bytes だけで全体が検証できる
   (kit manifest 194+40 files・val-gate 6-host node-exact・raw 110 files・
   status.log 59行・ad043 supersede 鎖込み)。

verdict 不消費・11×11 UNKNOWN 担保不変。
