# 2026-11-18 2トークン残余ゲーム z=6,y=26切片の全Grundy分類（K0938）

## 開始時点の確認

- 最新main: 99aa7db4bb7b98d4995b49af5208e4d621f4cc69（branch APIで確認）。
- AGENTS.mdを確認。main直接反映、knowledge/itemsを正本、experiment/logを分離、generatedとroot READMEは直接編集しない。
- research/knowledge/README.mdとK0832、K0873、K0918、K0936を確認。
- 現在の残件はz=6,y≥26、z≥7の全Grundy分類、3族値2位置一般式、標準二次元共円ゲームの固定幅・q点安定化長など。y=25までは全称証明済み。
- K0938はmain上で未使用。K0937は別のREMO/SIEVE研究であり、本件と重複しない。

## 選定と発見

直前のy=25切片K0936をA/B/C再帰のB子に使い、y=26を次の境界として選定した。x=26ではA子とB子が正準化後に同じ(26,25)へ合流する。x≥27ではA子をRに関する帰納仮説にできる。

全x≥26・全R≥0について、H(R;(x,26);6)のGrundy値を0/1/2に完全分類した。値2位置は低いラダー{1,3,5}に加えて、x=26の55、x=30の57、x=33の{59,61,63,65}、x≥34の59だけである。値1位置はK0938の正本と証明報告に閉形式で記録した。

証明はA/B/Cの選択肢署名表、K0832のTheorem T、一般tail定理、R強帰納による。x=26..34を個別処理し、x≥35では奇数x・偶数xの二系列へ閉じる。有限監査を全称証明とは扱わない。

## 独立監査

順序付き直接再帰と降順正準化直接再帰で、y=26本体・y=25アンカー・z=5アンカーを照合。x=26..2000の署名2,065,850点、mex2,065,850点、tail128,375点、遠方tail5,000点など、合計6,339,920検査で不一致0。初期状態から2回実行し、監査内容はbyte-identical。検証器と監査JSONはexperiment内に保存する。

## 統合

- K0938をknowledge/itemsに追加。
- research/knowledge/README.mdの証明済み境界をy=26まで更新し、未解決をy≥27へ進める。
- experiment、verifier、audit、logを追加。
- branch / PRは作成しない。generatedとroot READMEは直接編集しない。
- この実行環境にローカルcheckoutがないため、uv sync --locked、knowledge check、unittest、build、git diffは未実施。GitHub Actionsの結果と区別して記録する。

## 次の課題

次はz=6,y=27。今回と同じくAは同一切片の帰納仮説、Bはy=26、Cはz=5で閉じられる見込み。ただし過渡署名がどう変わるかは未確認であり、今回の式の単純な平行移動とは仮定しない。z≥7と標準二次元盤の安定化長は別の未解決問題として維持する。
