# 2026-11-19 — z=11・y=5の2トークン切片を全称化

## 作業前確認

- 最新 `main`: `cc8be6d6dc1df9ef87dd10aae4b9103035e82754`。直近コミットでK1035（n11残余28-root witnessの第4WIN7-D10証明書）まで着地していた。
- `AGENTS.md`を確認。mainへ直接反映し、知識の正本は`research/knowledge/items/`、実験は`research/experiments/`、履歴は`research/log/`、generatedは直接編集しない。
- `research/knowledge/README.md`の2トークン節を確認。z=11はy=1..4（K1012..K1015）、z=13・z=14・z=15のy=2..4とz=12のy=1..4が全称証明済み。z=11・y=5は未登録で、B子K1015（z=11,y=4）・C子1⊕K1007（z=10,y=5）がともに出版済みのため着手可能だった。並走第一候補のz=15・y=4とは切片が異なるため非衝突、採番はpush直前に再確認した（K1036が空き）。
- なお`research/knowledge/generated/`はitemsに対して旧いまま（summary.mdが872項、K0894まで）で、`tmp-knowledge-build.yml`の「broken Markdown links修理後の再生成待ち」状態。本pushでは兄弟切片と同様にgeneratedを直接編集せず、再生成レーンに任せた。

## 発見

\[
H(R;(x,5);11),\quad x\ge5,\ R\ge0
\]
のGrundy値0/1/2を完全分類した。

子分解は
\[
A=H(R-1;(x-1,5);11),\quad
B=H(R-1;(x,4);11),\quad
C=1\oplus H(R-1;(x,5);10).
\]
BはK1015、CはK1007。x=5では二つの減少手が同じ多重集合(5,4)に合流し、x>=6ではAをx外帰納で閉じる。

値2位置はx>=18で\(O[1,11]\cup\{21\}\)に定着し、pin=21をx=16（x=z+y）で前倒し、x=17（x=z+y+1）で掃引帯\(O[21,33]=O[\mathrm{pin},x+y+z]\)が出る。x=6は高さx+y=zの行で孤立上端15=2y+(d+z)/2−1（d=1・d+z=12≡0 (mod 4)）を持ち、K1034の「h=z孤立上端はd+z mod 4だけで2値」という規則の第6実例でy奇数初例。前倒し点x=8の17・x=12の19はd+z≡2 (mod 4)の格子値2y+(d+z)/2、x=16の21はその格子値がpin=2y+zに一致する型。
値1の基底点は{12,14,16,18,20}（y点仮説のy=5例・5例目）で行ごとに段階出現し、中間帯開始は23=z+2y+2、無限I帯は偶数x行のみでtail値(x+5) mod 2が1の行と一致する（y奇数による反転）。先駆I帯はx∈{6,8,10,12,14,16}から17,18,18,21,20,22で立つ。tailはR>=x+17で(x+5) mod 2、R<=12はheight-only縮約single_token(x+5,11,R)。

## 全称性と監査

全称性はx外帰納と、全Rを覆う明示的なA/B/C署名帯表・mex対応表による。低R（R<=12）はK0832の高さのみ縮約、高R（R>=x+17）はK0832の一般tailで閉じる。

独立監査器は順序保持再帰と降順正準化再帰を別実装し、B/Cアンカー（K1015/K1007レポート閉形式の転写）、署名帯、mex、Theorem T、低R縮約、tail、固定seed散点を検査した。深行（x<=700）は閉形式子アンカー署名で被覆した。合計5,406,960照合・不一致0・別プロセス2回実行で監査JSONはbyte-identical。第三導出として生二再帰センサス（x=5..45・R=0..x+45、行表・閉形式・tail照合、2,911点×2）も二回実行byte-identical。有限監査は転写・実装照合であり、無界性は帰納証明が担う。

## 反映

- 新規正本: `K1036-two-token-z11-y5-boundary.md`
- 実験: `vertical-fiber-two-token-z11-y5-boundary-20261119/`（report・verify・census・audit・census.txt）
- 本ログとknowledge READMEを更新、Knowledge integrity workflowに検証器・audit差分検査stepを追加
- branch/PRは作らずmainへ直接反映

## 残る課題

z=12のy=5（B=K1024・C=1⊕本項）、z=11のy=6（B=本項・C=1⊕K1008）が着手可能になった。y>=2族の全高さパラメトリック一般化、値1基底点のy点仮説、d+z mod 4二値規則の一般証明は未解決。標準二次元盤の固定幅・q点安定化長も別途未解決。
