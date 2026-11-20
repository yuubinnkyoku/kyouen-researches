---
id: K1101
title: 2トークン残余ゲームの対角線下マージ定理（y=1,2 の全称証明）と一般マージ観察の有限センサス
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token merge below diagonal, height-sum merge]
relations:
- type: depends_on
  target: K0832
  note: H の定義・Theorem T・単一トークン閉形式 single_token(S,z,R) の z>=S+1 場合を比較対象として使用する
- type: depends_on
  target: K1023
  note: y=1 全zパラメトリック閉形式（cand/cand0）の領域制限（x<=z-2）を証明に使用する
- type: depends_on
  target: K1099
  note: y=2 全zパラメトリック閉形式 cand2 の領域制限（ラダー領域 x<=z-3）を証明に使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-merge-below-diagonal-20261120/report.md
  role: proof
  note: 定理と記号的証明（出版閉形式の領域制限どうしの一致）・9チェック監査表・センサス witnesses・鋭さ（S=z 反例）・信頼境界
- path: research/experiments/vertical-fiber-two-token-merge-below-diagonal-20261120/verify_merge.py
  role: verifier
  note: 双直接再帰・出版閉形式錨・y=1/y=2 恒等式全グリッド・固定seed深部probe・一般マージ生センサス・S=z 反例固定・9チェック総13,081,238照合点・不一致0・audit byte-identical
- path: research/experiments/vertical-fiber-two-token-merge-below-diagonal-20261120/output/audit.json
  role: data
  note: 検証器の決定論的監査出力（fixed seed・sorted keys・SHA-256 38299a53b2584c99780d67bc47f3d013dc88fb4e37fd6aaf94691c4cf21da758）
- path: research/log/2026-11-20-two-token-merge-below-diagonal.md
  role: log
  note: 選定・導出・K1100 競合による再採番・出版記録
- path: research/log/2026-11-20-two-token-merge-below-diagonal-single-owner-note.md
  role: note
  note: 単一オーナー宣言（commit dcf5d1be・先行出版）
scope: >-
  κ=1 残余ゲーム H(R;X;z)。主張は2トークン族 X=(x,y) の y∈{1,2} に限る:
  全 z>=1・全 x>=y・全 R>=0 で x+y<z なら H(R;(x,y);z)=H(R;{x+y};z)
  （右辺は出版単一トークン閉形式）。y>=3・3トークン以上のマージ観察は
  有限センサス witness のみであり本項の全称主張には含まれない。
evidence: >-
  証明は出版閉形式どうしの記号的比較である。K1023 の y=1 表を x+1<z に、
  K1099 の cand2 を x+2<z（ラダー領域）に制限すると、どちらも z 非依存の
  行関数になり、 K0832 の single_token(S,z,R) の z>=S+1 場合
  （値2: O[1,q_odd(S)]、q_odd(S)=2⌈x/2⌉+1、超過分: S mod 2）と
  x/y の偶奇4場合で完全に一致する。監査機械 verify_merge.py は
  C1 生二重再帰（順序保持/正準化）×出版閉形式×single_token×生単一トークンの
  五者一致 48,777 点＋出版スライス錨（z=12,y=1・z=16,y=2）、
  C2/C3 y=1/y=2 恒等式全グリッド 11,766,373 点、C4 固定seed深部probe
  （z<=20000・R<=100000）198,567 点、C5 一般2トークン生センサス
  （y=1..40・z<=40）348,270 点、C6 3トークン生センサス（z<=26）156,754 点、
  C7 4・5トークン生センサス 8,740 点、C8 鋭さ（S=z マージ不成立の正準反例
  (3,(2,1),5): 1 vs 2 を固定・帯内発散 828 件計上）、C9 対角線下 z 非依存
  546,000 点、の計 13,081,238 照合点で全チェック不一致 0・同一cwd 2回＋
  別cwd別プロセス 1 回で audit.json byte-identical。系として
  K1023/K1099 のラダー領域の z 非依存（値2位置のみならず全R）と
  K1054 の「低R高さのみ縮約の y=2 全z版」（R<=z+2y でなく全R）が従う。
  有限監査は転写・実装照合であり、全称性は閉形式比較の記号証明が担う
  （K1023/K1099/K0832 と同一の trust 境界・Lean 形式化ではない）。
---

## 命題・範囲

y∈{1,2} に対し、すべての z>=1、x>=y、S=x+y<z、R>=0 で

H(R;(x,y);z) = H(R;{S};z) = single_token(S,z,R)

が成り立つ。対角線（S=z）ではマージは失敗する（正準反例
(z,X,R)=(3,(2,1),5): H=1 vs H(R;{3};3)=2 が、境界 S<z は鋭いことを示す）。

## 証明の構成

1. K1023（y=1 全z）と K1099（y=2 全z）の閉形式を対角線下の行に制限すると
   z 非依存の行関数になる（y=1: x 偶→2 は O[1,x+1]・1 は [x+2,∞)、
   x 奇→2 は O[1,x]・1 なし。y=2: x 偶→2 は O[1,x+1]・1 なし、
   x 奇→2 は O[1,x+2]・1 は [x+3,∞)）。
2. K0832 の単一トークン閉形式の z>=S+1 場合（2 は O[1,q_odd(S)]、
   超過分は S mod 2）と、q_odd(S)=2⌈x/2⌉+1・(x+y) mod 2 の偶奇 4 場合比較で
   完全一致する。
3. 値1・値2の重なりなし（ラダー上端 < 値1帯開始）と R=0 を確認して全 R 成立。

## センサス witnesses（全称主張ではない）

- 2トークン y=1..40（z<=40）: 348,270 点不一致 0。
- 3トークン（z<=26）: 156,754 点不一致 0。
- 4トークン（z<=14）・5トークン（z<=11）: 8,740 点不一致 0。
- 観察「S=ΣX<z なら H(R;X;z)=H(R;{S};z)」は K1078（z=18,y=3 の行一致）・
  K1098（z=19,y=3）・K1100（z=19,y=4）が個別の行レベル一致として記録してきたが、
  本項は y∈{1,2} を全称証明した。y>=3 は観察のまま残る。

## 限界・残務

- 主張の全称性は記号証明による。C1〜C9 の機械照合は二重検査であり証明の
  代わりではない。y>=3・マルチトークンの一般化は、対角線帯の C 子補償構造
  （S=z-1 行の選択肢 1^H(R-1;X;z-1) と 1^H(R-1;{S};z-1) の不一致が
  mex レベルで相殺する機構）の一般化を要し、未解決。
- K1054「低R高さのみ縮約の y=2 全z版」は系として解決済み（全R版）。
