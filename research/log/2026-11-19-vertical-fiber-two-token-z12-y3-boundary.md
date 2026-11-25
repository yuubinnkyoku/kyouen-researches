# 2026-11-19: z=12・y=3 2トークン境界切片（K1021）

## 作業前の確認

- 作業開始時点のmain: 5c823954ea03e17a4c10cc01b90c409fc64830a2。
- AGENTS.md、research/knowledge/README.md、既存K1014/K1019、knowledge.yml、refresh-knowledge-generated.ymlを確認した。
- K番号はK1020まで使用済み。K1021は未使用。
- z=12,y=3の候補行は、既存のcross-z有限監査logで既に観察されていたが、全称証明・署名帯表・保存検証器は未登録。候補の再掲ではなく、出版済みB/C子に基づく全称証明を新規に構成する。

## 選定理由

z=12,y=3の三子は全て閉じている。
- A: 同じz=12,y=3切片のx-1行（外帰納）。
- B: K1019のz=12,y=2全称公式。
- C: 1 xor K1014のz=11,y=3全称公式。

したがって、有限探索を広げず、署名帯の全R被覆を作れば全称証明にできる。z=12,y=4の次段でもB=K1021、C=1 xor K1015となり、今回の成果が直接使える。

## 新結果

K1021として、全x>=3・全R>=0のGrundy値0/1/2を証明した。値2の定常集合はO[1,11]∪{19}、値1の定常部分は基底{13,15,17}と偶数帯20から始まる。x=16は掃引行でO[19,31]が現れ、x=17以降はピン19へ収束する。対角線x+y=zに当たるx=9ではO[1,15]への拡張ラダーが残る。

証明の詳細は同ディレクトリのreport.md。署名表はx=3..17の個別行とx>=18の偶奇2行で全R>=1を被覆し、各帯のA/B/C mexがT/P閉形式を与える。

## 検証

- 順序保持・正準化の二直接再帰と候補公式: 52,597点、不一致0。
- K1019 B子アンカー: 24,849点、不一致0。
- K1014 C子アンカー: 24,849点、不一致0。
- A/B/C署名帯の被覆・実値・mex: 各52,299点、不一致0。
- Theorem T: 52,597点、不一致0。
- 高さのみ縮約R<=13: 4,172点、不一致0。
- 一般tailR>=x+16: 2,682点、不一致0。
- 固定seed散点: 5,000点、不一致0。
- 合計323,643照合。検証器2回実行でaudit.jsonがbyte-identical。verifier SHA-256は7fefb5d96ec57ed7c849f44094f0d7cda92f39e4ded4d9015d6428ae8fa199ea。

有限監査は全称性の根拠ではない。全称性は報告した外帰納と署名帯表である。

## main反映と残件

K1021、report、verifier、audit、logをmainへ直接反映し、knowledge READMEとKnowledge integrity workflowを更新する。生成ビューは直接編集せず、refresh-knowledge-generated workflowを起動するコメントを追加する。K1014/K1019の現在の未解決範囲も、それぞれz=11のy>=5、z=12のy>=4へ更新する。

この環境ではrepo全体のuv sync --locked、tools/knowledge/check.py、unit test、build.pyは未実施。push後のGitHub Actionsで確認し、成功が返るまではCI完了と扱わない。branch/PRなし。
