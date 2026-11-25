# 2026-11-21 (4,22,5) class-split 掃引完結・4×22 witness-free（高速レーン batchD/batchE）

## 到達点

- **M_{4,5} = 21 または ≥ 24**（witness-free 幅集合 {21,22}・K0821 監査規約・上界 U=140 は不変）。
  (4,22,5) の 9 正準欠損クラス被覆が完結し、**4×22 に行欠損極大安全配置は存在しない**
  （全極大安全配置 16 石・行占有率 (4,4,4,4)）。K 昇格は K1197。
- 内訳: multi 7 直接 + k0/k1/k2 46 直接 + c1k3 11 直接 + c0k3p3..p10 8 直接
  （batchD）+ c0k3p0/p1/p2 の x2 第2石完全分割 57 枚（batchE）= 計 129 UNSAT。
  陽性対照 SAT 1（4×20 witness V 像再発見・375,415 conflicts bit-exact）。
  直接 600s INDET 3 幅は完全分割で決着（INDET 行は誠実な負記録として残存）。

## セッション経過

- **宣言** [f0b1fbad](2026-11-21-four-row-q5-m22-batchDE-resumption.md) 07:10Z。
  前セッション（2026-11-20 12:13Z〜13:04Z takeover）が RESETUP-20261120.md で
  「次回実行」へ明示的に引き継いだ batchD/batchE の継続着手。push競合 1 件
  （無関係 z17-y4 レーン d6858a93 の宣言ノート・同一対象なし確認の上で内容変えず再push）。
- **較正**: ctrl_4x20_c0k3p1 CNF byte-exact（362034b2…）・SAT 375,415 bit-exact。
  c1k3p3 CNF 再生 byte-exact（25bccf63…）。c1k3p10 再実行 1,146,769 bit-exact。
  新旧 sat4 x2 符号器は (4,21,5) c0k3p0 x2=1 で byte-identical（13749780…）。
- **batchD**（c0k3p3..p10 直接・cap 900s）: 8 枚全 UNSAT・最難 c0k3p3
  5,162,737 conflicts / 415s。m21 の同バケット比約 2x の一貫難化。
  records 68→76 を 497f4e17 で push。
- **環境ハードリセット事故 07:53Z**: work area 全消滅（本レーン 4 回目）。
  未push の x2 決着 30 枚（c0k3p0 b1..20・c0k3p1 b2..b11 の内未push 分）を喪失。
  repo 正本 76 行は m22lane records push 済みで無事。kissat・scripts・records を
  repo pin から再構築（kissat md5 3a5eba83… 一致・records fetch-back md5 一致）し
  再実行。喪失前観測済み 15 枚の conflicts はすべて bit-exact 再現
  （b1 2,196,989・b4 870,895・b5 826,926・b6 998,167・b7 1,037,562・b8 839,299・
  b18 288,320・b19 178,341・b20 134,020・p1b2 1,310,589・p1b8 690,728・
  p1b9 629,565・p1b10 701,470・p1b11 538,122 + c1k3p10 1,146,769）。環境またぎ
  決定性の較正を兼ねる。
- **batchE**（x2 分割 57 枚・cap 900s・resumable driver で逐次）: 全 UNSAT・INDET 0。
  p0 b1..20 計 14,914,910・p1 b2..20 計 11,831,256・p2 b3..20 計 9,750,138 conflicts
  （総計 36,496,304）。最難 c0k3p0x2b1 2,196,989 / 115s。m21 最難 x2
  （1,969,663）比 1.1x。増分push 3 回（433215df 76→88・dddf26bd 88→112・
  02517132 112→133）。
- **第二検証**: x2-split-verification-20261121.json を experiments dir に出版。
  CNF 再生 md5 4 件（p0b7/p0b12/p1b13/p2b10）記録一致・サンプル再実行 3 件
  （p0b1/p1b2/p2b3）conflicts bit-exact・全 57 枚 tally・p 別合計・
  増分 commit 内訳。

## 判断と規約の確認

- x2 分割の完全性は K0857 の規約（exhaustive disjoint case analysis・B ≤ m−2=20 for
  k=3・k-aware 拡張は k=2 限定で今回不関与）。minpos 分解の健全性
  （min(x1, 21−x_k) ≤ 10・H は行を保存）も 4×21 と同型で不変。
- cap 到達の INDET は不在主張でない。今回の 129 UNSAT はすべて cap 内決着
  （打ち切りによる INDET は新規に発生せず）。
- 計算結果は有限機械検証として出版。m ≥ 23 の持続性は未解決のまま
  （M_{4,5} の確定には 4×23 以降全幅の witness-free 検証か普遍的 tail 論証が必要）。

## 次の前線

- **4×23**: SAT なら M ∈ [24, 140]・UNSAT なら witness-free 幅集合 {21,22,23} で
  M = 21 or ≥ 25。難化予測は m22 比 1.5〜2x（batchD/k3 直接の外挿）だが
  x2 分割の実績（m21 185s→m22 115s 最難・寧ろ横ばい）から分割は m23 でも
  機能する見込み。着手時には単一オーナー宣言と最新 main 再取得を必須とする。
- K1197 は K 番号 3 点確認（K1196 が上限・K1197 未使用を search_code で確認）の上で採番。

標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 は本レーンと無関係・UNKNOWN のまま。
行は1行も閉じない。nodes/solved 数を勝敗として読まない。REFUTED-D10 は LOSS 証明ではない。
