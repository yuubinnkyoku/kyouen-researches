# 2026-11-20 two-token z=19 y=4 boundary slice (K1100)

高速レーン自実行。2トークン残余ゲーム H(R;(x,4);19)、全x>=4・全R>=0 の全Grundy分類。

## 経緯

- 前回実行（K1098, commit 8e98481da1）の着地確認で7ファイル byte-exact を検証した後、
  並走の K1099（y=2パラメトリック全z・commits b831bf4d〜9147f52c）出版を確認。
- 「次候補 z=19,y=4」は未着手・未宣言だったため単一オーナー宣言ノートを先行出版
  （commit 056c00bd23）→ `research/log/2026-11-20-two-token-z19-y4-single-owner-note.md`。
- push直前の再取得で並走の「two-token merge below diagonal」宣言（dcf5d1be99）を確認したが
  対象が異なるため本項に影響なし。

## 導出

1. raw エンジン（順序保持・降順正準化の2実装）で x=4..33 の T/P 構造を抽出。
2. アンカーのみからの帯導出: K1098/K1083 をそのまま移植し、
   F(x,R)=mex{A=F(x-1,R-1), B=K1098(x,R-1), C=1⊕K1083(x,R-1)} を x=4 から伝播させ
   偶奇別署名帯表を導出（x=4..25 の静的22行＋x>=26 のアフィン帯）。閉形式と伝播 F が不一致0。
3. 閉形式を raw 親グリッド（x=4..41, R<=x+32）で照合し、検証器 verify_z19_y4.py に統合。

## 主結果

- 値2: 対角行 x=15 の上端 23=2y+q_o(z−y)（8実例目）、前倒し点 x=19/23（25/27、d∈{15,19} は
  y=3 と同値で d 活性値の y 非依存が新観察）、掃引行 x=24 の O[27,47]、pin 27=2y+z（x>=25）。
- 値1基底点 {20,22,24,26}（y点仮説、z=19 で y=2/3/4 の縦3連続）、中間帯 O[29,q_o(x+23)]。
- 「高さのみ」x<=14 全行（S<z 候補の3実例目）、x>=23（=z+y）で R<=26=pin−1 一様・pin 27 で鋭く反例
  （R<=pin−1 の4実例目・開始行 x=z+y は y=3 と同一形式）、tail R>=x+24=S+z+1 で (x+4) mod 2。

## 監査

- 総検査 945,926・不一致0（parent 2,109 / B 2,067 / C 2,033 / 帯+mex 7,275 / 帰納閉包 136,648 /
  set対述語 37,036 / 低R 6,112 / tail 259 / 深域アフィン 749,375 / seed散点 3,000・seed 20261122）。
- 検証器 SHA-256 09cc65208d4696a73354455ac348e2f4054fca34e74ecacbb9eaa5b434d56b3f・
  監査正本 SHA-256 1669d20a2fbe94b44bb5783e2f9a9a1c20c63daf125ad12182d024576fe3e8cc。
- 同一cwd 2回＋別cwd別プロセス 1回で byte-identical。

## 出版

- 実験dir: `research/experiments/vertical-fiber-two-token-z19-y4-boundary-20261120/`
  （report.md・verify_z19_y4.py・output/audit.json）
- item: `research/knowledge/items/K1100-two-token-z19-y4-boundary.md`
- knowledge README 弾丸（末尾純追加）と knowledge.yml の K1099 census ステップ直後に監査ステップ挿入。
- K番号はpush直前に3点確認（slug 404・README grep・list_commits）。

## 限界と次候補

- 本項は z=19,y=4 に限定。全称性は x外帰納＋署名帯表による（有限監査は照合であって証明の代わりではない）。
- 次候補: z=19,y=5（B子=本項・C子=1⊕K1092、両アンカーが揃う。着手前に単一オーナー宣言）、
  z=19,y>=6 一様族（z=18,y>=6 並走宣言の状況を確認してから）。
- 二トークン係の一般化候補（未証明の交叉観察）: (a) S<z ⇒ 高さのみ（3実例）、(b) 対角行上端 2y+q_o(z−y)（8実例）、
  (c) 低R一様 R<=pin−1 と開始行 x=z+y（4実例）、(d) 基底点 y 点 {z+1,…,z+2y−1}（同一z縦3連続）、
  (e) 前倒し点 d の活性値が y 非依存（y=3・y=4 で d∈{z−4,z}・2点。ただし z 依存は未検討）、
  (f) tail R>=S+z+1 で S mod 2（3切片）。
- y=2 パラメトリック全z（K1099）・y=1 全z（K1023）を踏まえると（z=19,y）平面のこの列は
  y>=2 でアフィン帯が q_o/q_e(x+2y+15) 型に統一される可能性があるが、本項では主張しない。
