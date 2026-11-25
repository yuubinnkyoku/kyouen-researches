# 前線 witness bounded-edit surgery（(5,4) m=41・6行3前線 m=29/25/22）— 単一オーナー宣言

- **宣言時刻**: 2026-11-21T18:47Z 頃（Vibe 高速レーン instance）
- **宣言時 HEAD**: `ddb1564ceeba865fddcf3e17f2356a0d12fd5e56`
- **owner**: この宣言を出した instance（失効時は最新 main の IN FLIGHT 確認の上、
  他レーンが takeover 可）

## 対象・目的

five-row-q4-witness-band-40plus-20261121 レーン（K1209・commit 列 `6604dbe2`..`16478850`）
が自レーンのレジューム (a)(b) として残した未掃引前線を、この instance が単独で進める:

1. **(5,4) m=41 witness 構成探索**: m=40 witness 16個（K1209・D4 modulo distinct・
   14石・全て R(S)=40・stop cell (40,1)）と公刊 m=37/38/39 witness（計19基底）の
   D4 像を基底とする bounded-edit surgery（編集予算 single-move・remove-2/add-1・
   remove-2/add-2・時間が許すなら remove-3/add-3）で 5×41 盤の witness 検索。
   正の結果は下界更新（M_{5,4} ∈ [42, 567]）。上界 T_5=567（K0068/K1207）は不変。
2. **6行3前線の witness 構成探索**: K1209 free-append census が真の前線と確認した
   (6,5) m=29・(6,6) m=25・(6,7) m=22 の各幅で、公刊前線 witness
   （(6,5) m=28 rowY0・23石・(6,6) m=24・29石・(6,7) m=21・35石）を基底とする
   bounded-edit surgery（同一編集予算）。正の結果は各下界更新のみ
   （上界は K0318 系のまま）。構成的 witness 検索であり、K1201 の SAT INDET
   （(6,5) m=29 等）の先取り・置換ではない（構成が成功すれば INDET 幅に constructive
   決着、失敗しても不在主張にならない）。

## 手法・検証要件（受入条件）

- 探索機は pinned `surgery.js`（five-row-q4-witness-band-40plus-20261121 配下・
  sha256 同 experiment の sha256s.txt）の検証済み engine 部分を (w,m,q) 一般化した
  **新規ファイル**（surgery_g.js 等の別名）とし、pinned 原版は 1 byte 変更しない。
- **較正**: 一般化機が (a) 公刊 m=40 main run（surgery-main-m40.json・64 hits /
  16 distinct 石集合）を石集合レベルで完全再現、(b) m=39 control（single-move で
  m38 基底から2 witness 再発見）を再現することを本番前に確認する。
- witness 主張は **≥2 の独立整数実装系**で全 PASS: (i) surgery engine 発見時検証
  （safe-integer canonical curve census）・(ii) `append_criterion.py`（Fraction・
  w,q は CLI 引数で一般）による安全・旧列被覆・R(S)・(iii) 可能なら行列式/rank 系
  第三検証器（q≥5 は一般化新規実装）。
- 各 witness の rows・石数・maxx・R(S)（>m なら追加幅の階段も）を記録。
- **陰性の場合**: 有限の bounded-edit 近傍機械検証サブセットとして誠実記録し、
  大域的な不在は主張しない（frontier 近傍の感度下界としてのみ）。
- 有限実験を全称として主張しない（INDET/不在/近傍外を区別）。
- 出版は下界更新のみ・上界不変。mwq_stabilization.csv は更新しない（K1201 前例）。

## 非目標（衝突回避）

- 3行 q=4 m≥32 治具拡張（`2026-11-21-three-row-q4-jig-extension-m32-single-owner` 宣言済み）。
- 4行 q=4 m=35/36（four-row-q4-m35 class-split 停滞レーン + part2 crosscheck K1208済）。
- (7,4) m≥60 band（`2026-11-21-seven-row-q4-band-m60-single-owner` 宣言済み）。
- 4行 q=6 の m≥35 延伸・(4,5) m=21/23 class-split（各レーン）。
- 6行 q8 帯閉包（six-row-q8-band-closure resume 宣言済み）。
- six-row SAT 前線の SAT/INDET 掃引自体（K1201 lane の領分）。本宣言は構成的
  surgery のみ。
- n11 系・fold 検証系・s_n/K_n 系・knowledge corpus 修復 — 非接触。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。

## collision protocol

- push 直前に毎回最新 main を再取得する（前レーン `6604dbe2` の手順ミス〔push直前の
  HEAD 再取得忘れ〕を繰り返さない）。
- 同一対象への他レーンの IN FLIGHT 宣言や結果 push を検出した場合、本レーンは
  対象を外すか convergence を優先する。
- 失敗時は無理に進めず状況を簡潔に記録して次回実行に回す。

## 進行の公表

- 実験は新規 dir `research/experiments/frontier-bounded-surgery-20261121/` に置く。
- 既存実験 dir への追記はしない。
