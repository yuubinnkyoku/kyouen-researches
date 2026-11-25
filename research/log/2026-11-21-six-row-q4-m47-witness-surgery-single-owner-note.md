# 六行 q=4 (6,4) m=47 witness 構成的 surgery — 単一オーナー宣言

- **宣言時刻**: 2026-11-21T20:24Z 頃（Vibe 高速レーン instance）
- **宣言時 HEAD**: `b19d79a698faf114dacaf25d209c4287b0a36a8d`
- **owner**: この宣言を出した instance（失効時は最新 main の IN FLIGHT 確認の上、他レーンが takeover 可）

## 対象・目的

- (6,4) witness band は m=6..46（six-row 17 石配置、four-row-q4-q5-frontier-20261115
  batch 13 の rowY=0 witness 系・m=46 は構成的 free-column append witness〔4 システム検証済み〕、
  witness band m=6..46・M_{6,4} ∈ [47,1113]）。6x47 rowY=0 SAT instance は CNF 生成 RAM 壁
  （six-row-q4-m47-rowY0-oom-20261115・SIGKILL rc=137）で前線停滞中。
- 本レーンは 6x47 を **構成的** に進める: 公刊 6x46 witness の 6x47 移植
  （公刊記録では唯一の未遮断セル (46,0)）を seed とした bounded-edit surgery
  （編集予算 remove≤2/add・occupied ≤4 点、陰性なら remove≤3/add≤3 に拡張）による
  6x47 row-deficient maximal safe witness 探索。正の結果は下界更新のみ
  （M_{6,4} ∈ [48,1113]）。上界 T_6=1113 は不変。
- witness が見つかれば free-column append criterion（固定石集合の列被覆は幅単調）
  で追加幅を機械掃引し、時間が許す限り追加 surgery round を連鎖する
  （seven-row-q4 band-60plus の chained 2-for-2 方式と同型）。

## 受入条件

- engine は新規 clean-room 実装（repo コード不使用・純整数/Fraction・決定的・自己テスト内蔵）。
- **陽性対照**: 同一 engine が K1209 (5,4) m=39→40 surgery main run
  （64 hits / 16 D4-distinct 石集合・five-row-q4-witness-band-40plus-20261121）を
  石集合レベルで完全再現することを本番前に確認する。
- witness 主張は ≥2 の独立整数実装系で全 PASS（safe・row-deficient・maximal・全空点遮断・
  負対照で改変検出）。主出力は決定性 2 回実行で byte 一致。
- 陰性の場合: 有限 bounded-edit 近傍の機械検証負記録としてのみ主張する。
  6x47 全体の不在は主張しない（INDET/不在/近傍外を明確に区別）。
- 有限実験を全称として主張しない。mwq_stabilization.csv は更新しない（K1201 前例）。

## 非目標（衝突回避）

- (5,4) m=41・(6,5) m=29・(6,6) m=25・(6,7) m=22（宣言済み frontier-bounded-surgery lane の領分・非接触）。
- (6,4) 6x47 の SAT/INDET/class-split 掃引自体（構成が正でも SAT 前線の掃引とは
  独立・先取りではない）。
- 4行/7行/n11/s12-13/fold 系・knowledge corpus — 非接触。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。

## collision protocol

- push 直前に毎回最新 main を再取得する。
- 同一対象 (6,4) m47 構成探索への他レーンの IN FLIGHT 宣言や結果 push を検出した場合、
  本レーンは強行せず状況を簡潔に記録して次回実行に回す。
