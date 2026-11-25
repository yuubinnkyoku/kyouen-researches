# 2026-11-14 five-row q=7 m=22 class-split sweep — 途中経過（実行環境障害による中断記録）

高速レーン第8回・第4成果の仕掛かり。K0821（5x21 witness-free）が開いた新前線 5x22 を
K0821 と同一機構（sat3.js class-split + kissat 4.0.4・k×minpos分解）で走査中。
実行環境（bash・filesystem）が継続的な一時障害に入ったため、決着済み31インスタンスの
記録をここに残し、残り18インスタンスを次回実行に回す。

## 進捗（49決着インスタンス中31点・全て UNSAT・INDET 0）

- 17直接クラス全て UNSAT: {2} 415,785・{0,1} 875,682・{0,2} 459,366・{0,3} 527,330・
  {0,4} 532,938・{1,2} 147,267・{1,3} 553,321・{0,1,2} 176,655・{0,1,3} 205,904・
  {0,1,4} 101,688・{0,2,3} 199,205・{0,2,4} 413,185・{1,2,3} 92,611・{0,1,2,3} 105,192・
  {0,1,2,4} 155,772・{0,1,3,4} 141,060・{0,1,2,3,4} 153,855 conflicts。
  （m=21より全体的に容易。最難関 {0,1} 875,682 は m=21 の 1,050,634 を下回る）
- {0}k=0..4 全て UNSAT: 161・1,947・42,948・252,166・1,465,046 conflicts
  （{0}k4 は m=21 の 1,465,515 と実質同値 — 分解難度は幅に対して平坦）。
- {1}k=0..4 全て UNSAT: 108・3,758・49,541・316,501・1,402,958 conflicts。
- {0}k5mp0 UNSAT 3,380,578（162.5s 単独走行）・{1}k5mp0 UNSAT 3,111,756（154.4s）。
- {0}k5mp1 UNSAT 1,370,195・{1}k5mp1 UNSAT 1,256,417。
- 素の {0},{1} 単発（witness探索・280sペア）は 2,849,545 / 3,330,616 conflicts で未決着
  （分解で被覆されるため決着には不要・負記録として保有）。
- 生ログ19件（直接17+素{0},{1}）は実験dir
  research/experiments/five-row-q7-m22-class-split-20261114/output/ にpush済み
  （commit 1029a0db）。分解14件分の生ログはローカル
  /home/user/krwork/m22/out/ にあり環境復旧後にpushすること。

## 残作業（次回実行）

1. {0}k5mp2..mp10・{1}k5mp2..mp10 の18インスタンス
   （m=21実績では mp2..mp10 は全て ≤1.2M conflicts・軽量。CNFは既に生成済み
   /home/user/krwork/m22/out/c5x22q7_[01]k5p[2-10].cnf・meta json付き）。
2. 全49点UNSATなら: 5x22 witness-free → witness-free width set {19,20,21,22}・
   M_{5,7} ∈ {19,20,21,22} or ≥24・前線 5x23。K0824 item・records/summary/report・
   CSV (5,7)行・fixed-width README・log を K0821 と同じ形式で反映。
3. どれか1点でも SAT なら: 5x22 に29石欠損極大witness → M_{5,7} ≥ 23・K0824 item は
   witness報告形式（decode・verifyConfig・行構成を必ず記録）。

## 補足（census独立再計算・sandbox計算）

5xm q=7 の円census（7点以上・外心三元組形式・sat3.js circleABC と独立の実装）を
sandbox で再計算し、公表値 5x18=84・5x19=95・5x20=104 を完全再現。
5x21=113・5x22=122（サイズ7は m≥19 で常に8個・サイズ8は 87,96,105,114 と
幅+1ごとに+9）。5x22 はサイズ7・8のみで L≥9 は不在 — class-split符号化の
census完全性前提は m=22 でも成立。なお sandbox 計算は bash 障害中の代替手段として
実行したもの（K0822 lane と同手法）。

環境: bash/filesystem の一時障害（"execution environment is temporarily unavailable"）。
sandbox純JS計算とGitHubコネクタは健在。1コマンドのCPU上限は約285 CPU秒
（単独285秒 or 2ワーカー×142秒）を今回確認 — m=22走査は全てこの制約内で完走可能。
