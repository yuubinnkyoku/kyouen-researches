# 2026-11-20 — z=15・y=4の2トークン切片を全称化（K1048）

## 作業前確認

- default branchはmain。作業開始時のmainは 05096f4ae032fc3da673c0d98b0696f26bd894d5（K1047）。
- AGENTS.md、research/knowledge/README.md、生成summaryの未解決一覧を確認した。K番号は正本のresearch/knowledge/items/を優先し、generated領域とroot READMEは直接編集しない。
- z=15・y=4の項目・実験dir・K1048は未登録。B子はK1034（z=15,y=3）、C子はK1031（z=14,y=4）で、A/B/Cが閉じる。
- z=14・y=5はK1047で既に証明済みだが、K1031の未解決欄には古い記述が残っていた。今回の反映で除去する。K1047の次の未解決境界もz=15,y=4の解決に合わせて更新する。
- branch / PRは作らずmainへ直接反映する。knowledge integrityとgenerated refreshの両workflowへ検証器を登録し、生成物は専用workflowに再生成させる。

## 実験と発見

H(R;(x,4);15)、x≥4の全Grundy値を調べた。Tの定常形はO[1,15]∪{23}、Pの基底点は
{16,18,20,22}={z+1,z+3,z+5,z+7}
となる。値1の基底点がy個並ぶという既知の予想に、y=4・奇数zの新しい全称実例が加わった。

値2の掃引行はx=z+y+1=20で、pin 23=2y+zがO[23,39]に広がる。x=19ではpinだけが先行し、x=21は掃引行の子署名を受ける過渡行として残る。x=15の前倒し点21はd=x-y=11、d+z=26≡2 (mod 4)の格子値2y+(d+z)/2と一致する。h=z行x=11の値2上端は19。

## 全称性

子局面は
A = H(R-1;(x-1,4);15)
B = H(R-1;(x,3);15)
C = 1 xor H(R-1;(x,4);14)
である。x=4ではA/Bが同じ(4,3);15多重集合子に合流し、K1034のx=4行を基底とする。x>=5ではAをx外帰納、BをK1034、Cを1 xor K1031で評価する。

署名帯表は過渡行x=4..21と定常行x>=23奇数/x>=22偶数で全1<=R<=x+19を互いに素に被覆する。K0832の高さのみ縮約でR<=16、一般tailでR>=x+20も閉じる。よって有限走査の外挿ではなく、全x・全Rの帰納証明である。

## 独立監査

検証器は順序保持・降順正準化の二直接再帰、K1034/K1031子アンカー、親直接再帰、署名帯の被覆・子署名・mex・Theorem T、高さ縮約、tail、固定seed散点を検査した。

- 合計2,128,617照合、不一致0。
- 同一プロセス内2回実行でaudit.jsonはbyte-identical。
- verifier SHA-256: 21f76dac2f3d0a2a68967b0ae298085f8c36016b1c38b206f4722ae9bf8edd21
- audit.json SHA-256: 34891067e91d54f7fb46c53564afe0694c009cbcb1ef3f1dfec70904cd89252a

有限監査は証明表の転写・実装照合であり、全称性はx外帰納と全R署名帯表が担う。

## 反映

- 正本: research/knowledge/items/K1048-two-token-z15-y4-boundary.md
- 実験: research/experiments/vertical-fiber-two-token-z15-y4-boundary-20261120/
- 研究ログを追加。K1031/K1047の現在の未解決範囲を更新する。
- knowledge integrityとgenerated refreshの両workflowにK1047/K1048検証を登録する。generated領域・root READMEは直接編集しない。

## 次の課題

z=15・y=5はB子K1048、C子K1045が揃い、次の切片候補になる。z=14・y=6、z>=16・y>=2、値1基底点y点仮説、d+z剰余格子の一般証明、標準盤の固定幅・q点版安定化長は引き続き未解決.