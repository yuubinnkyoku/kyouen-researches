---
id: K1225
title: 3×3〜6×6 極大安全配置の全行分布・最大サイズ・D4軌道・三点共線統計の機械確定
kind: computation
status: computed
topics: [maximal-safe, geometry]
aliases: ["small board maximal safe rows", "M_4=7 M_5=9 M_6=11", "n6 maximal rows orbits"]
relations:
- type: depends_on
  target: K0030
  note: 出版分布表（3×3..6×6・5..11石）の全セルを機械再現・6×6総数349,596一致
- type: depends_on
  target: K0057
  note: 禁止四点組アンカー（F_5=826, F_6=2491 は出版sha一致・F_4=194は新規記録）
- type: depends_on
  target: K1224
  note: 列挙・分類機材（enum_catalog.mjs/classify.mjs/census.mjs）のbyte同一再利用
- type: contrasts
  target: K1224
  note: 最小行軌道系列の拡張（n5:1, n6:1, n7:2, n8:51 に n4:22/n3:8 を追加）
- type: contrasts
  target: K0032
  note: n=8の三点共線24配置（B372）に対する n=3..6 全行の対照系列
artifacts:
- path: research/experiments/small-board-maximal-rows-20261122/README.md
  role: source
  note: 主張・方法・多系統検証・trust boundary・規模方針
- path: research/experiments/small-board-maximal-rows-20261122/output/rows-summary.json
  role: data
  note: 全77行の機械レコード（K0030一致表・2系統一致・決定性の統合ゲート rc=0）
- path: research/experiments/small-board-maximal-rows-20261122/output/determinism.json
  role: verification
  note: 77行×2走行のcanonical byte一致・nodes bit一致・classify/verify 2回一致
- path: research/experiments/small-board-maximal-rows-20261122/output/verify_n6_rows.json
  role: verification
  note: 独立Leibniz幾何（系統B）・別言語別実装による全配置SAFE+MAXIMAL・軌道再構成・対照群
---

# 3×3〜6×6 極大安全配置の全行分布・最大サイズ・D4軌道・三点共線統計の機械確定

標準共円盤（q=4）の 3×3〜6×6 について、石数ごとの包含極大安全配置（極大安全集合）の
行分布を**全石数域 k=1..N² で完全列挙**し、K0030 の出版分布を全セルで機械再現した上で、
K0030 が表に掲載していなかった領域を機械確定した（有限計算・trust boundary は実験
README による）。

## 主な確定事実

1. **K0030 完全再現**: 出版表の全セル（5..11石列）と一致し、6×6 の極大安全集合総数
   349,596 も一致。今回が初の機械較正となった行は 5×5 k=9（100）と
   6×6 k=9/10/11（199,184/30,492/464）。残りの既刊行も n7 カタログ機材で再現。
2. **全行の明示的確定 → 最大サイズ**: 各盤面の全行 k=1..N²（4×4:16行・5×5:25行・
   6×6:36行）を列挙し、非零行は
   3×3 {5:56}・4×4 {5:176, 6:688, 7:64}・5×5 {5:4, 6:1136, 7:11280, 8:4340, 9:100}・
   6×6 {6:8, 7:3952, 8:115496, 9:199184, 10:30492, 11:464}
   のみ。よって**極大安全集合の最大サイズは M_3=5, M_4=7, M_5=9, M_6=11**（機械値）。
   6×6 の k≥12 の消滅は K0030 の表では陽に掲載されておらず、本実験が初の明示的
   確定。最小行は s_3..s_6 の既刊値と整合（値更新ではない）。
3. **D4 軌道数・安定化群**（全14非零行、Node/Python 2実装完全一致）:
   n3 k5: 8軌道{1:6,2:2}・n4: 22/87/8・n5: 1/143/1413/543/13・n6: 1/494/14441/24898/3814/58。
   5×5/6×6 の最小行が単一軌道（安定化群位数2/1）であることも出版文言の再現。
4. **三点共線統計**（B372 対照系列の拡張）: 各行の1トリプル配置数・0トリプル配置数・
   「全配置が3点共線を持つ」bool を確定（実験 README §1.4 の全行表）。
   観察: n≥5 では最小行と最大行で「全配置が3点共線を持つ」が成立し中間行では崩れる
   （n=4 の最小行では不成立・最大行では成立）。最小行の1トリプル個数系列は
   n=4:88, n=5:0, n=6:0,（既刊 n=7:0, n=8:24）。

## 検証の backbone（詳細は実験 README）

- 禁止四点組カタログ2系統 byte 一致（F_4=194 を新規記録、F_5/F_6 は出版 sha 一致）。
- DFS 全列挙 77行×2走行: canonical projection（cfg行 + elapsedMs除去summary行）で
  byte 一意・nodes bit 一致。
- 独立検証（系統B幾何・Python・triple→completion map の別実装）: 全 367,384 配置が
  SAFE+MAXIMAL、軌道・安定化群・trips/dirs が classify と 14/14 行完全一致、
  tamper 陰性対照全行拒否、陽性対照（最小行単一軌道）受理。
- 第三方式 2^N 部分集合全走査（n=3/n=4）: n=4 の非零3行は配置集合そのものが DFS と
  完全一致、n=3 は K0030 明示値 56 に一致。
- 「極大安全集合族は反鎖（包含極大の定義から従う補題）」を 367,196 配置で
  remov=0（行間エッジ0）として機械確認したが、これは主張ではなく整合ゲート。

## 非主張

- 有限計算であり形式証明ではない。実装と言う trust を含む（K1224 と同水準）。
- s_n の値更新なし。7×7/8×8 の既刊カタログ（K1224/K0032）との行レベル比較は
  本項ではしない（最小行の軌道数系列は既刊の n7/n8 値をそのまま引用）。
- n≥7 の k≥12 行・n≥9 盤面は未着手。ecc ヒストグラムは classify.mjs 単独計測。
- 標準 11×11 空盤・二石 root・S2・closure class は非接触（UNKNOWN のまま）。
