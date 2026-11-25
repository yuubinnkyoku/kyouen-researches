# 2026-11-15 five-row q=7 m=22 class-split completion（高速レーン引き継ぎ）

## 概要

2026-11-14T15:25:57Z の batch-1（commit 1029a0db）が 19 生ログを push したきり
8.5 時間無音（report・records・claim なし・環境リセットと推定）のため、
takeover claim（b637ba8e）を push して完了させた。(5,7) の前線は 5×23 へ。
K0834。

## 実施

- 17 直接クラス: batch-1 ログとの conflicts bit-exact 再現 **17/17**
  （{0,1} 875,682・{1,3} 553,321・{0,2,3} 199,205 等）。{0,2,3} はローカル取得
  コピー破損（243B）だけで repo 上は完全 UNSAT ログ（24,783B）だった。
- {0},{1}: k×minpos 完全分解 32 点すべて UNSAT（最難 {0} k=5 mp=0
  3,380,578 conflicts/153.8s・{1} k=5 mp=0 3,111,756/144.1s）。plain {0}/{1} は
  batch-1 INDET（2,849,545/3,330,616・~142s SIGTERM）。m21→m22 で難度は
  ほぼ横這い（m21 {0}k5p0 3,295,997 vs m22 3,380,578）。
- lex=H 交差確認 {0,1}/{2} UNSAT（627,149/310,356 conflicts）。
- 陽性対照 5×18 {0} SAT 343,134 conflicts — **K0821 レーン対照と bit-exact**・
  decode→census-free verifyConfig PASS（29石 rows 5,6,6,6,6・K0332 witness 再発見）。
- minpos の正確な意味を sat3.js 実装読みで確認: 「第1欠損行の最左石の列を P に
  固定」であり min(x1,m−1−x5)=p の等式制約ではない。列鏡像で左半分を被覆
  （min(x1,21−x5)≤10、x1≥11 なら x5≤10 で矛盾）。初期に書いた「p=9,10 は
  位置数え上げで vacuous」は誤りで修正（p=9,10 も非自明: 60,133/47,157 conflicts）。

## 境界の更新

- (5,7): {19,20,21},23..158 → **{19,20,21,22},23..158**（witness-free 幅集合拡大・
  K0834）。deciding 49 例合計 24,581,763 conflicts（17 直接 5,256,816 + 分解
  19,324,947）・lex 2 例 +937,505・INDET 0・SAT 0。

## 教訓

- `cd X && (A) & (B) & wait` の `&&` は第1サブシェルに取り込まれ、第2ワーカーが
  別 cwd で走る（今回も踏んだ）。`cd X; (A) & (B) & wait` か絶対パスで。
- 引き継ぎ判断: batch-1 の claim 欠如・8.5h 無音・report なし → takeover README
  を push して協調。repo 上の生ログの完全性は「ローカル取得の破損」と区別して
  本体側で確認する（今回は {0,2,3} が該当）。
