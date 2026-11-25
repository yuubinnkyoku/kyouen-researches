# 研究ログ: 2トークン残余ゲーム y=10族パラメトリック閉形式候補の fitting（2026-11-20・高速レーン）

## 宣言の確認

- 単一オーナー宣言 [2026-11-20-y10-two-token-skeleton-single-owner-note.md]
  （宣言時刻 2026-11-20T10:25:00Z）の通り着手。着手時点で y=10 族への別オーナー宣言は
  main に存在しなかった（宣言が最初）。
- 宣言noteの事前予想は以下の通り有限範囲で裏付けられた: tail 開始 x+z+11
  （族式 x+z+y+1 の y=10 版・値 (x+10) mod 2 で値1無限帯と tail は奇数 x 行）・
  基底点 10 点 {z+1,...,z+19}・マージ行 x<=z-11 → single_token(x+10,z,R)・
  pin 格子 pin=z+(d+3y)/2（奇z d∈{-6,-2,2,6,10}・偶z d∈{-8,-4,0,4,8}）・
  最終pin行 d=y=10 の値1帯 I[z+2y+1)・対角 cap z+10/z+9。予想に反した点: なし。
- シードは [y=10 raw skeleton survey](2026-11-20-y10-two-token-skeleton-raw-survey.md) の骨格観察。
  survey の予備 onset 観察のうち奇z の速報値（d=-5→14・d=1→17・d=3→17・d=9→20）は
  本 fit では成立せず（該当行は b6/b8/b8/b10 で値1終端・I 帯なし）、生エンジン全点照合
  （probe 72,261 点＋spot 27,318 点・不一致 0）に基づく本 fit が置き換える
  （survey 自身が明示した窓 30 による読み取り限界の範囲内の訂正）。

## 導出の経緯

1. `probe_y10.py`: 生二重再帰（順序保持・降順正準形・lru_cache・y=9 出版 probe と同型）で
   z=0..30・x=10..z+27・R<=x+z+26 の 1,023 行 RLE 生成（72,261 点・約 2.7 秒）。
2. T 側: survey シード（対角 cap・pin 格子・steady/掃引の族式）で組んだ初稿は 255 点不一致。
   全不一致が奇z d=11 掃引行に集中し、掃引帯の偶奇を R 基準（R%2==0）で書いた誤りと判明。
   y=10 の掃引帯は偶offset [2y, x+y]（= R≡z (mod 2)）であり offset 基準で書く必要があった
   （y=9 では z 偶奇と R 偶奇の関係が逆で R 基準表記が偶然成立していた。y=10 で表記基準の差が
   初めて顕在化した点が今回の新しい落とし穴）。修正で 72,261 点 mismatch 0・T/P 重複 0。
3. P 側: 行別 base・I 帶 th(d) の zigzag（I 帶行は奇z d 偶行・偶z d 奇行・th=z+2k・d が 4 進む
   ごとに +2・最終pin行 d=y のみ th=z+2y+1）を probe 行から抽出して全行 table 化。
   値1無限帯は偶数 y 型（x 奇の行）y=9 の逆に寄る。
4. `spot_y10.py` で box 外 27,318 点（深 R<=130・z=31..40×16 d・x=y=10 エッジ z=10..40・
   遠方 d∈{30,41,52}×6 z）照合・bad 0。加えて K0832 単一トークン形式とのマージ回帰
   18,795 比較（不一致 0）と d>=12 行の tail raw 90 点（(x+10) mod 2 全一致）を確認。

## 採番（K1140 競合検出と K1141 再採番）

- まず items subtree（git trees API・entries 1,121・truncated=false）を再取得して
  最大 K1139 を確認し、次の空き番号 K1140 を採番した。しかしなお README 体裁を整えて
  いる間に並走が進み、push 直前の README 実ファイル再取得で n11 fold24 レーンが
  commit fc4c18fdd で items/K1140-n11-residual29-win8-receipt-fold-root438000000818.md
  （WIN8-D10 receipt fold・fold24・README bullet 末尾追記込み）を先行出版済みである
  ことを検出した。AGENTS.md 再採番規約（first-published-priority・K1135〔仮番号K1133〕・
  K1138〔仮番号K1137〕と同じ手続き）により、items 系コミット再取得で K1141 未使用を
  確認のうえ K1141 へ再採番した（実験 dir・log・item・README bullet の参照を全て差し替え。
  執筆中の併走 AG(2,16) レーン〔commit 91e05d35da・c8e148afc・K1058 更新〕とは番号・パスの
  衝突なし）。
- push ごとに最新 main HEAD の再取得・出版直前の番号再確認を怠らないことが今回も有効だった
  （push 前検出のため main への矛盾した出版は発生していない）。

## 出版内容

- 実験 `research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/`
  （report.md・cand10.py・probe_y10.py・spot_y10.py・output/audit.json。
  probe_rows.txt は probe_y10.py で決定論的に再生可能なため本コミットには含めない。
  CI step は正本監査段階で追加する）
- knowledge item K1141（status: observed・observed 段階であることを明記）
- README bullet（K1141・末尾追記）

## 次に開くもの（宣言note手続き第3段階以降）

1. verify_y10_universal.py: 12チェック監査（生両エンジン直接照合・単一トークン/y=9 子
   〔cand9 は K1138 出版検証器 verify_y9_universal.py SHA-256 299acb6a… からの逐語転写〕・
   x=10 合流子〔(9,10)≡(10,9)〕・出版切片転写アンカー・恒等式グリッド・選択肢分解・
   型機械（clip 窓 ±22/番兵 ±23・族式候補 2y+2=22 の tight 判定
   〔y=5:12,..,y=9:20 の 5 族連続 tight に続く 6 例目〕・B子に cand9 を使う初の族）・
   seed 固定遠方 probe・境界多様体・v 空間シェル・深 z 生 census アンカー・深閉形式グリッド）
   の総照合点不一致 0 と 3 回実行 audit byte-identical。
2. census_rows.py（y=10 版）: z=0..79・x=10..70・R<=x+z+12 の生行表・
   cand10 からのバイト同一再生 SHA-256 照合。
3. 全称証明の成立をもって K1141 を proved に更新（有限 fitting からの昇格。
   AGENTS.md「同じ命題は同じ K 項目」）。失敗した場合は有限反例の記録として本項を維持する。

## 範囲外

標準 11×11 の空盤勝敗・二石 root・S2 {59,60} には言及しない。
3トークン以上・y>=11 族・固定幅・q点版安定化長は本ログの対象外。
