# 研究ログ: 2トークン残余ゲーム y=9族パラメトリック閉形式候補の fitting（2026-11-20・高速レーン）

## 宣言の確認

- 単一オーナー宣言 [2026-11-20-two-token-y9-parametric-allz-single-owner-note.md]
  （宣言時刻 2026-11-20T08:41:00Z・先行出版 a096f2bc）の通り着手。着手時点で
  y=9 族への別オーナー宣言は main に存在しなかった。
- 宣言noteの予想は以下の通り裏付けられた（有限範囲）: tail 開始 x+z+10
  （族式 x+z+y+1 の y=9 版）・マージ行 x<=z-10 → single_token(x+9,z,R)
  ・基底点 9 点 {z+1,..,z+17}・clip 窓 2y+2=20（型機械は次段階）。
  予想に反した点: 特になし（y=8 系列からの構造外挿がすべて有限範囲で一致）。
  ただし偶 z pin 行の d 範囲が y=8 の [-y+2,y-2]（4行）から y=9 は
  [-y+4,y+2]（5行）に +2 シフトしており、偶 z の pin 行数の増加は y=9 で
  初めて実測された（y=7 は偶 z 3行 [-y+4,y-2]）。

## 導出の経緯

1. `probe_y9.py`: 生二重再帰（順序保持・降順正準形・lru_cache）で
   z=0..30・x=9..z+27・R<=x+z+26 の 1,054 行 RLE 生成（73,811 点）。
2. 初回 T ドラフト（y=8 型の y シフト＋自己流 pin 範囲）は 376 点不一致
   （d≡y mod 4 の d>y 行に格子 pin を誤適用）。pin_extract で全 pin 行の
   値2オフセットを抽出した結果、d>y の同 residue 行は steady pin と一致
   （格子 pin は d∈[-y+2,y] 奇 z・d∈[-y+4,y+2] 偶 z に限る）と判明。
   修正 T 表で 73,811 点 mismatch 0。
3. P 側は y=8 の in_P8 構造（base b4..base_y・I 帯 th(d)・band・tail）の
   偶奇反転（y 奇 → 値1無限帯は x 偶行）で初稿 582 点不一致 → 不一致
   クラスタ分類（d=-9 偶 z 値1全欠如・d=-8 偶 z I 帯 z+9・d=-7 奇 z I 帯
   開始 z+11・d=10 偶 z band 追加）の 4 修正で 73,811 点 mismatch 0・T/P 重複 0。
4. `spot9.py` で box 外 25,376 点（深 R・z=31..40・x=y エッジ・d<=52）照合・bad 0。

## 採番（K1137 競合検出と K1138 再採番）

- 作業中仮番号 K1137 で出版を試みたところ、push 直前の README 実ファイル
  再取得で並走の n11 residual29 レーンが
  items/K1137-n11-residual29-win8-cert-extract-root00000000000200003800200008180000.md
  （WIN8-D10証明書抽出・commit acc949b6）を先行出版済みであることを検出。
  AGENTS.md 再採番規約（first-published-priority・K1135 の仮番号 K1133 と
  同一手続き）により、README item 参照で空きである次番号 K1138 へ再採番した。
- push 前に items/K1138・実験 dir・本 log の不存在を再確認済み。

## 出版内容

- 実験 `research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/`
  （report.md・cand9.py・probe_y9.py・spot9.py・output/audit.json。
  probe_rows.txt は probe_y9.py で決定論的に再生可能なため本コミットには含めない）
- knowledge item K1138（status: observed・observed段階であることを明記）
- README bullet（K1138・末尾追記）

## 次に開くもの（宣言note手続き第2段階以降）

1. verify_y9_universal.py: 12チェック監査（生両エンジン直接照合・
   単一トークン/y=8 子〔cand8 は K1135 出版検証器からの逐語転写〕・
   x=9 合流子〔(9,8)≡(8,9)〕・出版切片転写アンカー・恒等式グリッド・
   選択肢分解・型機械（clip 窓 ±20/番兵 ±21・族式候補 2y+2=20 の tight 判定
   〔y=5:12,..,y=8:18 の 4 族連続 tight に続く5例目〕）・seed 固定遠方 probe・
   境界多様体・v 空間シェル・深 z 生 census アンカー・深閉形式グリッド）
   の総照合点不一致 0 と 3 回実行 audit byte-identical。
2. census_rows.py（y=9 版）: z=0..79・x=9..70・R<=x+z+12 の生行表
   ・cand9 からのバイト同一再生 SHA-256 照合。
3. 全称証明の成立をもって K1138 を proved に更新（有限 fitting からの昇格）。
   失敗した場合は有限反例の記録として本項を維持する。

## 範囲外

標準 11×11 の空盤勝敗・二石 root・S2 {59,60} には言及しない。
3トークン以上・y>=10 族・固定幅・q点版安定化長は本ログの対象外。
