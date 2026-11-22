---
id: K1237
title: "2トークン残余ゲーム y=16族のパラメトリック閉形式候補 cand16（fitting + box 外 spot 検証・有限範囲で全点一致・全称は未証明）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=16 parametric closed-form candidate cand16, P16-fit"
  - "cand16 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 74,741 probe points; even-y template mechanical translation from the published FINAL cand14, the promoted-universal y=14 table with Y=14->16)"
  - "seed law 4th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16); first 17-row th-consecutive-integer sweep (17..33); first both-parity 8-row pin lattice (y/2 count law 4th data point y=10:5/12:6/14:7/16:8); first even-y family with merge rows entirely out-of-box (zero in-box merge rows)"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box 外マージ回帰14,910比較・境界行spot照合に使用・y=16ではbox内マージ行0行のため回帰は全面box外）
- type: extends
  target: K1233
  note: y=14族全称閉形式（K1233・昇格済み）の次の偶数y族。cand16初稿はy=14出版最終構造cand14（全称証明済み）のY+2機械翻訳で生成し、probe 74,741点に一発一致（cand12→cand14に続き偶数y seed法則2連続目・全体で4連続一発一致）。コード本体はY定数・関数名・y固有コメント以外は正本cand14と同一構造（Y正規化差分比較で確認）
- type: extends
  target: K1235
  note: y=15族全称閉形式（K1235・昇格済み）の次族。出版系列上の直前族であり、全称段階のB子は出版cand15の逐語転写（x=16合流子{15,16}≡{16,15}）。y=15のband_base/band_int分離（奇y族）とy=16の単一band則（偶y族）の対照がy=16 fitで再確認
- type: extends
  target: K1152
  note: y=12族全称閉形式（偶数y族式系列の基点）。z-odd I帯k=floor((d+3y+2)/4)・th連続整数掃引・偶z I帯k=floor((d+3y-1)/4)の偶数y族式がy=12→14→16で3族連続成立
- type: extends
  target: K1141
  note: y=10族（偶数y行型の基点・x奇行のtail・値1無限帯）。y=16も同じ行型反転（y偶=tail x奇行）で一致
- type: depends_on
  target: K1236
  note: y=15全称part2（系列上の直前工程）で確定した「横断法則y>=15一般補題化レーン」に本fitは偶数y系列第4データ点（y=10/12/14/16）を供給（pin行数y/2・pin mod-4回転・17行掃引・単一band則）
artifacts:
  - research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/
  - research/log/2026-11-22-y16-two-token-skeleton-single-owner-note.md
  - research/log/2026-11-22-two-token-y16-parametric-fit.md
---

# 命題候補（observed・有限範囲で確定・全称は未証明）

**候補**: すべての z>=0・x>=16・R>=0 に対して H(R;(x,16);z) = cand16(z,x,R)。
cand16 は z 偶奇別のパラメトリック T（値2集合）/ P（値1集合）の集合表
（正本: `research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/cand16.py`・
Y=16・b_k = 奇 offset {1,3,...,2k-1}・offset o = R-z・d = x-z）。

## 対象範囲（scope）

2トークン残余ゲーム H(R;(x,16);z) の全パラメータ領域（z>=0・x>=16・R>=0）を**候補**として宣言するが、
本項の根拠は有限範囲（probe box + box 外 spot・合計 125,560 点比較）であり、全称証明は含まない。

## 現在の根拠（evidence・2026-11-22 時点）

- 単一オーナー宣言 `research/log/2026-11-22-y16-two-token-skeleton-single-owner-note.md`
  （commit e0fbd99d・2026-11-22T21:21:34Z・宣言時点観測 HEAD 607c876a・probe 実行前に事前登録した
  横断予想16項目すべて fit level で一致・外挿点数 74,741〔行 899〕も宣言どおり）
- probe box（z=0..30・x=16..z+29・R<=x+z+34・生二重再帰正準形エンジン）74,741 点:
  cand16 全点一致（mismatch 0・T/P 重複 0・値頻度 0:36,738/1:29,032/2:8,971・値3なし）
- 初稿（cand14 の Y+2 機械翻訳）が**一発完全一致・修正 0**。出版最終構造 seed 法則が
  cand11→13・cand12→14・cand13→15・cand14→16 の**4 連続**（偶数 y 3 連）で成立
- box 内 tail assertion（R>=x+z+17 → (x+16) mod 2）16,182 点 bad 0・box 内マージ行 0 行（宣言どおり）
- box 外 spot 35,825 点 bad 0（deep 24 行 R<=130〔対角両偶奇・pin 8+8・skew・base・飽和 d=16・掃引/steady・
  マージ境界 x=z-17 両偶奇〕・bigz z=33..42×24d・x=y=16 エッジ・far d∈{33,44,55}〕。
  全選択行に x>=16 の機械 assert（y=14 fit の (19,13) 事故の構造的再発防止・初適用）
- tail raw 回帰 84 点 bad 0・merge 回帰 cand16 vs K0832 14,910 比較 bad 0（全面 box 外）
- 決定性: probe_rows.txt 3 回再生 byte-identical（SHA-256 5af7582d…）・fail-closed 監査
  `output/audit.json`（pin 兩偶奇 census 16 行・偶z対角値1計数 0・box内マージ行数 0 の gate）
- fail-closed 改ざん試験: 有効 7 変種すべて検出（詳細は audit.json）

## 構造則の y=16 値（詳細な族表は実験dirの report.md）

- pin 格子: o_pin=(d+48)/2∈[17,32]・奇z 8 行 d≡0 (mod 4) {-12,...,16}・偶z 8 行 d≡2 (mod 4) {-14,...,14}
  （y/2 行数則第4点・両偶奇 8 行の初例・最終 pin 行 d=16=y が偶y族で初めて上端に到達し I[33) 型）
- 奇z I 帯（d 偶 17 行）: k=floor((d+50)/4)・th=2k+[d≡y mod 4] が 17..33 の**連続整数 17 行掃引の初例**
  （「pin スロット = th-1」6 族連続・8 行すべて 2k=o_pin）
- base 行 k=floor((d+49)/4)（7 族目）・偶z I 行 k=floor((d+47)/4)（6 族目）・偶z base d=16 で飽和 k=16
- 偶z 対角行 d=-16 の値1全欠如（9 族目候補）・対角 cap z+16/z+15・掃引/定常 pin z+32/z+33・band 下端 34・
  偶y族単一 band 則・tail x+z+17・値 (x+16) mod 2（15 族目候補）・基底点 16 点

## 限界（全称ではない）

- 本項は観測（observed）である: probe box + spot の有限点集合での一致のみを主張する。
  clip 窓 2y+2=34 の tight 判定（12 族目候補）・pin 格子統一式の y=16 全称（12 族目）を含む
  全称証明（verify_y16_universal.py・A子/B子/C子・型機械・census）は本項の範囲外・別工程。
- 3トークン以上・y>=17 族・標準 11×11 空盤・二石 root には一切言及しない。
