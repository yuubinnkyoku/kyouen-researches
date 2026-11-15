# (8,9) 8x29 witness decision — rowfixed 4-split SAT — IN FLIGHT

2026-11-15 高速レーン（SATレーン）。`eight-row-q9-m29-surgery-20261115`
の次課題 4「m=29 の def-mode SAT 直接評価（kissat 環境があるレーンでの実施が望ましい）」
を実行する。CSV (8,9) 行の前線は 8x29（bounds 29..984）。

## status: IN FLIGHT（実行中・結果未確定）

## 主張の対象

witness = 極大安全配置で 63 = 8(9−1)−1 石以下。8x29 盤での witness 存在を
rowfixed 分割 SAT で判定する。結果はどちらでも新規:

- **SAT** → 8x29 witness → M_{8,9} ≥ 30（CSV lower 境界 30..984 に前進）。
- **4分割全 UNSAT** → 8x29 witness-free → M_{8,9} = 29 or ≥ 31
  （K0821-audit convention: M=30 には 8x29 witness が必要）。

## 分割被覆補題（健全性）

|F| ≤ 63 < 64 = 8·8 により鳩の巣で欠損行（≤7石）が存在する。行鏡像
y → 7−y は 8x29 盤の自己同型で rowY=k を rowY=7−k に写す。ゆえに
rowY ∈ {0,1,2,3} の 4 分割が全 witness を被覆する（各 witness は鏡像変換で
{0,1,2,3} のいずれかの欠損行を持つ）。m=26/27/28 の既知 witness はすべて
rows [8,8,8,7,8,8,8,8] 系（rowY=3）なので、rowY=3 から開始する。

## センサスの健全性

genfast.js chord-pair census は (8,9) では q9-census（eight-row-q10-band-closure-20261115、
CSV (8,9) 行の census 記録）により「1-double-row 9点円は m ≤ 40 に存在しない」
ことが機械検証済み → m=29 では chord-pair census は完全。

## 較正（claim 時点で実施済み）

- C1: `genfast.js 8 27 9 --rowY=3` → CNF vars=9612 / clauses=35005 / curves=146
  （公開記録と一致）。kissat 4.0.4 SAT、154,022 conflicts — 公開記録
  154,022 と bit-exact（6.5s）。
- kissat バイナリは公式 rel-4.0.4 asset（md5 3a5eba830aa6008a604fcc9bbe99a325）。
- scripts は main から md5 照合のうえ復元（genfast.js c5e6b5fe…、
  decode_verify.js e355e4b5…、sat.js 0cc6021a…、verify_witness.py 0530d166…、
  verify_witness_int.py 9b135808…）。

## 計画

1. rowY=3 CNF 生成 + kissat 4.0.4（バックグラウンド長cap）。
2. SAT の場合: decode_verify.js で石座標へ復号し、sat.js verifyConfig・
   verify_witness.py（exact Fraction）・verify_witness_int.py（純整数・
   census不使用）の3系統独立検証。
3. rowY=3 UNSAT の場合: rowY=0,1,2 を順次実行して 4分割完結。
4. 結果は records + 本README 更新 + CSV (8,9) 行 + fixed-width README に統合。

## 既知の条件付き結果との接続（重複なし確認）

- anchored-window-SAT（095c4d04）: 8x29 witness は s8x28（±1 shift）と
  列 0..20 での一致なし — 条件付き。
- surgery（eight-row-q9-m29-surgery-20261115）: s8x28 系 5配置の sd≤5 球・
  s8x27/s8x26 系の sd≤4 球に 8x29 witness なし — 局所閉包。
- 本実験はこれらの条件を課さない無条件判定であり、上記と独立。

## 部分記録（2026-11-15・高速レーン・環境制約で中断）

- rowY=3: kissat 4.0.4 を長 cap で起動したが、実行環境の bash 制限と実行中の
  環境リセット（2回）により kill。到達した最終 progress は
  **INDET 25,375,195 conflicts / 1665s**（time-cut。same-trajectory not bit-exact）。
  判定は未確定のまま。
- rowY=0/1/2: CNF 未生成。4分割完結には rowY=3 の長 cap 再実行とその続きが必要で、
  bash 280s 制限の下では完走不能 → 長期レーンへの引き継ぎ。
- したがって status は IN FLIGHT を継続（判定結果なし。anchored-window・surgery の
  条件付き結果との重複なし）。
- 次の実行可能課題（長期レーン）: rowY=3 を cap 5400s で再実行（kissat 4.0.4
  linux-amd64・md5 3a5eba830aa6008a604fcc9bbe99a325・zip md5
  eba46606374d283507ce1c37bdf910ac）し、UNSAT なら rowY=0/1/2 へ。
