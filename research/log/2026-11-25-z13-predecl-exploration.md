# 実行 log: z=13 min>=8 (floor-8) 事前探査 — 高速レーン 2026-11-25

K1316 (z=12 strip・宣言ノート §7) が「次レーンへの接続」として指名した
z=13 スライスのうち、底の床候補 min>=8 (floor-8) を探査した記録。
本 log は単一オーナー宣言ノート
`research/log/2026-11-25-strip-z13-min8-single-owner-note.md` (仮採番 K1317)
に先行する一次資料の出版である (publish-then-execute: 宣言前探査の全開示)。

## 経緯 (UTC 2026-11-25)

1. **着手時 main**: HEAD `f1542e2a` (09:18Z)。対抗する z=13 / K1317 宣言は
   なし (API・raw 検索)。K1316・rooted-core・Part EF/EG/EH レーンと非交差。
2. **一次資料取得**: K1316 宣言ノート全文 (z=12 セル表 F12..A12 + T-Z12)・
   belowband-row3 kit の `engine_block.py` (sha256 `582c93c1…` を照合 PASS)・
   `verify_k1315.py` 埋込 ENGINE_BLOCK (pin sha256 `bd5f22e4…` 照合 PASS)。
   H(R;X;z) の K1138 再帰・K0832 単一トークン閉形式 v・K1264 階段定理・
   K1312 空位置 L-2 を前提として使用。
3. **紙面誘導 (探査の前提となった構造予測)**: floor-8 セル
   Cell_j(s) := H(j+14; {j}∪Y; 13) (全 Y トークン >= 8) の選択肢が
   (i) Y 内 A 手 → 階段 v(s+j−1,13,j+13)・(ii) 小トークン A 手 → 一つ下の
   段のセル (s 不変)・(iii) C 手 → z=12 の min=j 定理線 (T-Z12(7) または
   出版 z=12 セル表・床 3..7 ⊆ 8 適合) の 3 種のみで、いずれも s のみの
   関数になることを段ごとの帰納で予測した。j=1 の B 手子は
   (14;Y;14) = v(s,14,14) (階段・白紙で 0)。この予測の下で各段の
   mex 手計算を行い、F13f8 の s=12 下向き・s>=14 の恒常 2 尾を先に紙面で
   導出した。
4. **予備 census**: ローカル簡易スクリプト (非出版) で第一走: engine cache
   (maxsize 6,000,000) を共有したまま全 7 セルを掃引した結果 **OOM kill
   (rc 137・F13f8 完了後に死亡)**。メモリ境界のためセル毎 cache_clear を
   挟む再構成で完走 (engine bytes は不変・値はキャッシュと無関係)。
5. **census 結果 (宣言表の元データ)**:
   - 全 7 セル (s ∈ {0}∪{8..40}・アリティ 0..4・床付き全分解 各 460 形状):
     **multivalue (分解依存) 行 0 — 全セルが s のみで決まる**。
   - deviant (Σ崩壊 v(s+j,13,j+14) に対する):
     F13f8: {12 下向き 1<2} ∪ {s>=14 上向き恒常 2>0}・
     G13f8: {12 下向き 0<1}・E13f8: {10 下向き 1<2, 12 上向き 2>0}・
     D13f8: {10 下向き 0<1}・C13f8: {8 下向き 1<2, 10 上向き 2>0}・
     B13f8: {8 下向き 0<1}・A13f8: {8 上向き 2>0}
     (**K1316 §1(c) の z=13 census 観測 A13 [[8],8,2,0] と一致**)。
   - tail spots s ∈ {41..48}: F13f8 は全 8 行で 2 (vs 崩壊 0)、他 6 セルは
     全行崩壊。
   - strip z=13 (m ∈ {8..12}・S ∈ {m..m+39}・部品 >= m・アリティ <= 3):
     **1,069 形状・違反 0**。strip spots m ∈ {13..16} 12 形状・一致。
     m=8 S=16 (X=(8,8)) は v(16,13,22)=1 と一致 (TOLERANT-ABSORPTION 底
     witness)。
6. **手計算との一致**: 上記 3. の机上演算 (各 deviant 位置の 3 選択肢値と
   mex・崩壊領域の一般論証) が census の全数値と一致することを確認した上で
   宣言ノート §2 を執筆した。
7. **正式機体の出版**: `explore_k1317.py` (engine pin ゲート内蔵・決定性
   2 走バイト同一) と凍結 stdout `explore_k1317.out`・`engine_block.py`
   (byte-clone) を本宣言に先行して出版する (下記 kit)。

## 出版 kit (本 log と同一 commit)

- `research/experiments/strip-z13-min8-20261125/engine_block.py`
  sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
- `research/experiments/strip-z13-min8-20261125/explore_k1317.py`
  sha256 `182ec937122d3a1f0a6fd379cce38279d80f6386ab7c9fdd2443ceb2303bfaf8`
- `research/experiments/strip-z13-min8-20261125/explore_k1317.out`
  sha256 `3fbdd1e8e1340c9cb097b5d5acdedc1854901c216845d22d4688e64a2f39c712`

再現: `PYTHONHASHSEED=1 python3 explore_k1317.py` で stdout が
`explore_k1317.out` とバイト一致する (census 実行時間 ~16 秒・メモリ
使用はセル毎 cache_clear により数百 MB 以内)。
