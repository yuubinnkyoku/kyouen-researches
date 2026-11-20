---
id: K1141
title: 2トークン残余ゲーム y=10族の閉形式候補cand10の有限fittingとbox外spot検証（全称証明は次段階）
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases: [two-token y=10 parametric closed-form candidate fitting, cand10 fit]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1138
  note: テンプレート系列y=1..9の直前の全称証明（y=9全称閉形式cand9）。y=10族の次段階の全称監査ではB子（y=9子）の評価にcand9を使用する（x=10合流子(9,10)≡(10,9)・B子にy=9全称閉形式を使う初の族）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/report.md
  role: data
  note: cand10のz偶奇別T/P集合表全文（pin統一式の6族連続・偶z対角行の値1全欠如〔3族連続〕・最終pin行d=yの値1帯I[z+2y+1)〔4族連続〕・掃引帯の偶奇がoffset基準である点〔y=10で顕在化した表記上の差〕・奇z/偶zのpin行d範囲が互いに逆に寄る遷移を含む）と検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/cand10.py
  role: verifier
  note: 閉形式候補cand10（in_T10値2表・in_P10値1表・Y=10）とprobe_rows.txt全点照合（72,261点・mismatch 0・T/P重複 0・SHA-256 7c08e065…）。正本検証器は本ファイルを逐語転写する
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/probe_y10.py
  role: data
  note: 生二重再帰probeエンジン（順序保持・降順正準形メモ化・z=0..30・x=10..z+27・R<=x+z+26・1,023行RLE生成・約2.7秒）
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/spot_y10.py
  role: verifier
  note: box外spot照合27,318点（深R<=130の8行・z=31..40×16 d・x=y=10エッジz=10..40・d∈{30,41,52}×6 z・bad 0）＋K0832単一トークンmerge回帰18,795比較不一致0＋d>=12行のtail raw 90/90（約16.6秒）
- path: research/experiments/vertical-fiber-two-token-y10-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: fitting段階の実行監査（統計・SHA-256・再生コマンド・probe_rows.txtは公開せず決定論的再生可能の注記）。probe値頻度0:35,393/1:26,886/2:9,982（値3なし）
- path: research/log/2026-11-20-two-token-y10-parametric-allz-fit.md
  role: log
  note: 宣言の確認・導出経緯（T初稿255点不一致の原因=掃引帯の偶奇基準）・出版記録・次に開くもの（12チェック監査）
- path: research/log/2026-11-20-y10-two-token-skeleton-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T10:25:00Z・先行出版。B子はK1138のcand9・clip窓2y+2=22のtight判定・K番号はpush直前再取得）
- path: research/log/2026-11-20-y10-two-token-skeleton-raw-survey.md
  role: log
  note: fitのシードとなったy=10骨格のraw掃引観察（6,613点）。本fitがその奇zの予備onset速報値を置き換える
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,10)。宣言noteの手続き第2段階として、
  z偶奇別パラメトリックT/P集合表候補cand10を生probeから導出し、有限範囲
  （probe box 72,261点＋box外spot 27,318点＝合計99,579点）で生エンジンとの
  完全一致を確認した。全z>=0・全x>=10・全R>=0の全称証明は本項に含まない
  （次段階の選択肢分解・mex恒等式・型機械・12チェック監査による。
  x=10合流子は(9,10)≡(10,9)）。
evidence: >-
  生二重再帰（順序保持・降順正準形）によるprobe z=0..30・x=10..z+27・R<=x+z+26
  （1,023行・72,261点）でcand10と全点一致（mismatch 0・T/P重複0・値域{0,1,2}）。
  うちマージ行x<=z-11は3,630点全点が単一トークン閉形式single_token(x+10,z,R)
  に一致（値0/1/2すべて・境界x=z-10の外ではsingle_tokenと不一致を観測済み）、
  tail領域R>=x+z+11は16,368点でx+z+y+1開始式・(x+10) mod 2 tail値とも一致。
  box外spot 27,318点（深R<=130の8行・z=31..40代表16d・x=y=10エッジz=10..40・
  d∈{30,41,52}×6 z値）も全一致。加えてK0832単一トークン形式とのmerge回帰
  （z∈{13,20,27,34,41,48,60,75}・x<=z-11・R<=x+z+29）18,795比較不一致0・
  d>=12行のtail raw 90/90一致。cand10の構造はy=1..9と同じ族式（tail x+z+y+1・
  マージx<=z-y-1・基底点y点{z+1,..,z+2y-1}=10点・定常pin 2y+z/2y+z+1・
  対角cap z+y-[z≡y mod 2]・pin=z+(d+3y)/2・band下端z+2y+2・掃引d=y+1
  O[2y+z, x+z+y]）のy=10値で、y=10は偶数y型（S=x+10の偶奇はxと一致・
  値1無限帯とtailはx奇の行〔y=9の逆〕）。y=10で実測された有限事実:
  (1) pin行d範囲は奇z [-y+4,y]={-6,...,10}（y=9の[-y+2,y]から左端+2シフト）・
  偶z [-y+2,y-2]={-8,...,8}（y=9の[-y+4,y+2]からy=8と同じ形へ復帰）で
  pin行数は奇z・偶zとも5行（2族連続5/5）。(2) 偶z対角行d=-10は値1を一切
  持たない（y=8/y=9に続き3族連続）。(3) 最終pin行d=y=10（奇z）の値1帯
  b10∪I[z+2y+1)（y=6 d=7・y=8 d=8・y=9 d=9に続く4族連続パターン）。
  (4) 掃引帯の偶奇はoffset基準（R≡z mod 2）であり、y=9までのR基準表記との
  差がy=10で初めて顕在化（初稿255点不一致の原因）。本項は有限fittingと
  spot検査であり全称主張ではない（trust境界はK0003のobserved段階）。
---

## 命題候補（observed・全称は未証明）

すべての z>=0・x>=10・R>=0 に対して H(R;(x,10);z)=cand10(z,x,R) が成り立つと予想する。
cand10 は report.md 全文掲載の z 偶奇別 T/P 集合表（`cand10.py` が正本）であり、
合計 99,579 点（probe box 72,261 点＋box 外 spot 27,318 点）で生エンジンと
完全一致を確認した。マージ行・tail 領域の回帰（各 3,630・16,368 点）および
box 外 merge 回帰 18,795 比較・tail raw 90 点も不一致 0。

## y=1..9 全称表からの横断予想の y=10 での判定（有限範囲）

- tail 開始式 x+z+y+1（y=2..9 全称確定）: y=10 で一致（10 族連続を支持）
- tail 値 (x+y) mod 2 と x 偶奇型: y=10 は偶数 y 型（x 奇の行）。y 偶奇が型を決める
  （y=2,4,6,8,10 偶数 y 型・y=1,3,5,7,9 奇数 y 型・10 族連続の観察）
- マージ命題 x<=z-(y+1)（y=1..9 全称確定）: y=10 の x<=z-11 で回帰（3,630 点＋18,795 比較）
- 基底点 y 点仮説 {z+1,..,z+2y-1}（y=1..9 全称確定）: y=10 の 10 点で一致（y=1..10 連続を支持）
- 対角行上端格子規則・定常 pin 2y+z/2y+z+1・掃引帯 O[2y+z, x+z+y]・band 下端 z+2y+2
  = clip 窓族式 2y+2 の y=10 値 22: すべて y=10 値で一致（型機械 ±22/番兵±23 は次段階）
- pin 格子（y=5..9 統一）: y=10 でも pin 統一式 z+(d+3y)/2 は成立（6 族連続）。
  ただし pin 行 d 範囲は y=9 と互いに逆に寄る（奇z [-y+4,y]・偶z [-y+2,y-2]）。
  y=7 偶z 3行 [-y+4,y-2]・y=8 偶z 4行 [-y+2,y-2]・y=9 偶z 5行 [-y+4,y+2]・
  y=10 偶z 5行 [-y+2,y-2] の遷移に単純な族式はなく、一般証明は今後の課題。
- 偶 z 対角行の値1全欠如（y=8/y=9 に続き 3 族連続）・最終pin行 d=y の値1追加点帯
  2y+z+1（y=6/y=8/y=9 に続き 4 族連続）も y=10 で実測。

## 限界

本項の根拠は有限 probe・spot 照合のみで、選択肢分解の健全性・mex 恒等式の
機械照合・型 confluence・独立 census は次段階（y=1..9 出版系列と同一手続き）。
有限事実の全称への昇格を含意しない。3トークン以上・y>=11 族・固定幅・
q点版安定化長・標準 11×11 の空盤勝敗は範囲外。

## 採番記録

作業中仮番号 K1140 で出版を試みたが、push 直前の README 実ファイル再取得で並走の
n11 fold24 レーンが commit fc4c18fdd（後に 456b48449 で schema 整備）で
items/K1140-n11-residual29-win8-receipt-fold-root438000000818.md
（WIN8-D10 receipt fold・fold24）を先行出版済みであることを検出し、AGENTS.md
再採番規約（first-published-priority・K1135〔仮番号K1133〕・K1138〔仮番号K1137〕と
同じ手続き）により次の空き番号 K1141 へ再採番した。push 直前の items 系コミット
再取得で K1140 が n11 の item に使用済み・K1141 未使用を確認済み。
