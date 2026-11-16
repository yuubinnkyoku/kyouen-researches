# z=6・y=3二トークン境界切片の証明・監査記録

- 日付: 2026-11-17
- 作業開始時のmain: 0c486e53bb84c4418c9a6c89073cdc067a4172e8
- 統合直前に再確認したmain: dd116e4a37468fe68372ee6fb2f20d5d3c522f01
- 作業前確認: root AGENTS.md、research/knowledge/README.md、K0832、K0873、K0877、K0878、z=6,y=2の証明報告・検証器を確認。README上の未解決範囲はz=6,y≥3とz≥7。K番号の最大はK0878で、z=6,y=3の項目・実験は存在しない。
- 方針: z=6,y=1,2の境界切片とz=5全スライスが既に証明済みなので、隣接するy=3を選ぶ。A子は同じ切片のR帰納、B子はK0878、C子はK0873に接続できる。

## 導出

親 \(H(R;(x,3);6)\) のA/B/C子は、\(x\ge4\) でそれぞれ
\[
H(R-1;(x-1,3);6),\quad
H(R-1;(x,2);6),\quad
1\oplus H(R-1;(x,3);5).
\]
\(x=3\) では二つのトークン減少手が同じ \((3,2)\) 子へ合流する。

AはR強帰納、BはK0878、CはK0873で既知。Theorem Tにより奇数親の選択肢は0/1に限られ、偶数親の値は高々1。\(x=3..11\) の過渡域と \(x\ge12\) の定常域に分けた全R署名表から、mexを取って値2位置 \(T_6^{(3)}\) と値1位置 \(P_6^{(3)}\) を得る。tail \(R\ge x+10\) は \(H=(x+3)\bmod2\) で既に決まるため、表は残りの全域を覆う。

## 監査

標準ライブラリだけの verify_z6_y3.py を作成。生のトークンを直接減らす再帰と、既証明アンカーからA/B/Cを再構成する方式を分離した。

- 新切片の直接再帰: 4,515状態
- z=5,y=3アンカー: 5,858状態
- z=6,y=2アンカー: 5,959状態
- A/B/C署名: 2,040,957点
- mex恒等式: 2,040,957点
- tail: 19,992点
- 固定seed散点: 2,000点
- Theorem T違反: 0
- 合計: 4,120,238検査、不一致0
- 2回の実行でaudit.jsonはbyte-identical
- SHA-256: 60f27b4bba9a4afc4d45e7180f302e25781fcce4d67b2e0065ebaebaa66d08bc

有限監査は証明の代替ではない。全称性はA/B/C署名表、Theorem T、tail定理とR強帰納による。

## 反映・未実施事項

K0879をprovedとして登録し、K0832のartifact一覧と証明済みスライス要約、K0877/K0878の限界記述、knowledge README、Knowledge integrity workflowの検証器一覧を更新する。generated filesは直接編集しない。

この実行環境には全リポジトリの作業コピーがなく、uv sync --locked、knowledge全体check、unittest、buildは未実施。最新mainのK0876 frontmatterには、少なくとも resume_sweep.sh、resume_check.py、gen_profs.py、output/js_cap12_r6.jsonl.gz が参照されているが、現在のtreeに見当たらない。既存のartifact参照エラーを今回の研究範囲外として修復せず、生成ビューも直接編集しない。新規検証器はこの実行環境で二回実行し、byte-identicalを確認した。
