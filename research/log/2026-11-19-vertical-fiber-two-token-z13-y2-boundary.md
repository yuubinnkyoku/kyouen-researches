# 2026-11-19 — z=13・y=2の2トークン切片を全称化

## 作業前確認

- 最新 `main`: `966e3f16024cc4f4a17dfaca00c5b38c0ff8e35e`（直近は11×11 S5 cache laneのlogのみのコミット）。直前の研究成果コミットでK1024（z=12・y=4）が追加されていた。
- `AGENTS.md`を確認。mainへ直接反映し、知識の正本は`research/knowledge/items/`、実験は`research/experiments/`、履歴は`research/log/`、generatedは直接編集しない。
- `research/knowledge/README.md`の2トークン節とK1016〜K1024を確認。y=1族はK1022+K1023で全z全称証明済み。z=13・y=1はK1017、z=12・y=2はK1019として出版済みで、K1024のREADME弾丸は「z≥13のy≥2」を次の未解決として明示していた。B子=K1017・C子=1⊕K1019の子分解が両サイド出版済みのz=13・y=2をK1025として選んだ。
- experimentディレクトリ`vertical-fiber-two-token-z13-y2-boundary-20261119/`はmainに存在せず、採番K1025はitems・README・workflowのいずれにも未使用であった。

## 発見

\[
H(R;(x,2);13),\quad x\ge2,\ R\ge0
\]
のGrundy値0/1/2を完全分類した。

子分解は
\[
A=H(R-1;(x-1,2);13),\quad
B=H(R-1;(x,1);13),\quad
C=1\oplus H(R-1;(x,2);12).
\]
BはK1017、CはK1019。x=2では二つのトークン減少手が同じ多重集合(2,1)に合流し、x>=3ではAをx外帰納で閉じる。

値2位置はx=2で\(\{1,3\}\)、x=3,4でO[1,5]、x=5,6でO[1,7]、x=7,8でO[1,9]、x=9,10でO[1,11]、x=11でO[1,15]、x=12..14でO[1,13]、x=15でO[1,13]∪\(\{17\}\)、x=16の掃引行でO[1,13]∪O[17,31]、x>=17で\(\{1,3,5,7,9,11,13,17\}\)に定着する（pin=17=2y+z・奇数zラダーO[1,z]）。値1の基底点は\(\{14,16\}\)、中間帯は19=z+2y+2から偶奇z追従の奇数帯で現れ、無限I帯は奇数x行にだけ出て tail R>=x+16 の値 \((x+2)\bmod2\) と一致する。tailはR>=x+16で(x+2) mod 2、低RはR<=14でheight-only縮約 single_token(x+2,13,R)。前倒し点はx=11の15とx=15の17で、いずれもd格子点 \(2y+(d+z)/2\)（\(d+z\equiv2\pmod4\)・d=9,14）としてcross-z監査logのd格子法則どおり（奇数zでは掃引行の前の2行に分けて孤立点として出現する型）。

## 全称性と監査

全称性はx外帰納と、全Rを覆う明示的なA/B/C署名帯表・mex対応表による。低R \(R<=14\) はK0832の高さのみ縮約、高R \(R>=x+16\) はK0832の一般tailで閉じる。

独立監査器は順序保持再帰と降順正準化再帰を別実装し、B/Cアンカー、署名帯、mex、Theorem T、低R縮約、tail、固定seed散点を検査した。合計13,806,285照合・不一致0・二回実行byte-identical（検証器自身のSHA-256 `f2ea7cfe34d64dfd9b04c071dd1b85ec3065eb46a759db6ca7dc69831c72c274` を監査JSONに記録）。有限監査は転写・実装照合であり、無界性は帰納証明が担う。別ファイルの`census_z13_y2.py`はx=2..45・R=0..x+45の生二再帰センサスで行表・tailを第三導出から照合した（二回実行byte-identical）。

## 反映

- 新規正本: `K1025-two-token-z13-y2-boundary.md`
- 実験: `vertical-fiber-two-token-z13-y2-boundary-20261119/`
- 本ログとknowledge READMEを更新
- Knowledge integrity workflowに検証器・audit差分検査を追加
- branch/PRは作らずmainへ直接反映

## 残る課題

z=13のy>=3（B=本項・C=1⊕K1021）、z=14以降のy>=2、y>=2族のパラメトリック機械化は未解決。本次だけからz方向・y方向の一般式を主張しない。標準二次元盤の固定幅・q点安定化長も別途未解決。
