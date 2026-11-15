# 2026-11-16 — 2トークン残余ゲームの z=1 全Grundyスライス

## 作業前確認
- 作業開始時のmainは4c69f34。統合前にmainを再取得し、別作業の更新f511ac0も確認した。
- AGENTS.mdはmain直接反映、knowledgeを正本、experiment/logを独立保存、generatedとroot READMEの生成領域を直接編集しない方針。
- research/knowledge/README.md、生成済み未解決一覧、K0832本文を確認。2トークン族の全z位置予想は有限監査のみで未証明、z=0の全Grundy値だけが全称証明済み。z=1全Grundyスライスの項目は存在しない。
- 4×m・q=8、3×m・q=5、3×m・q=4は既存K0077/K0071/K0351等で確定済み。今回の対象外。open issuesは0件。

## 選定と発見
既存ログが次の課題として挙げた「z≥1の2トークン族」から、最小の未解決高さz=1を選んだ。任意x≥y≥1、S=x+y、d=x-yについて、H(R;(x,y);1)の全Grundy値を閉形式で決定した。

- R=0,1,2: 0,2,1。
- 3≤R≤2y: (R+1) mod 2。
- R=2y+1: d>0なら2、d=0なら0。
- 2y+2≤R≤S: R mod 2。
- R=S+1: d=1ならS mod 2、d=2なら2、d≥3ならR mod 2。
- R≥S+2: S mod 2。

従って値2位置は、d=0: {1}、d=1: {1,2y+1}、d=2: {1,2y+1,S+1}、d≥3: {1,2y+1}。

証明はR強帰納。C子は既証明z=0閉形式、y=1のB子は既証明単一トークンz=2閉形式で評価する。対角線、非対角線y≥2、境界y=1（x=2,3,4とx≥5）に分けた選択肢値表でmexを確認した。完全な場合分けはexperiment reportに記録。

## 独立有限監査
verify_z1_slice.pyは、(1) cap補題を使うソート済み多重集合エンジン、(2) capを使わない順序付きラベルエンジンを独立実装した。
- x≤80、全1≤y≤x、0≤R≤x+y+7の288,360状態で両エンジンと閉形式を照合。不一致0。
- 偶数RでH≤1、奇数RでH≤2を301,320点で照合。違反0。
- 既知tail R≥S+2ならH=S mod 2を32,400点で照合。違反0。
- 二回の実行で監査JSONはbyte-identical。py_compile成功。
- 検証器SHA-256: 607055ab81723a73fbbc3e534f943736bc385c7a14d754763522dba73b508993
- 監査JSON SHA-256: 46139537cfab5eb51a7951d0a45c5f1208e9d442ddc0c73c186c1d6ecaa3f810

有限監査は全称性の根拠ではない。全称性はR強帰納による。

## K0832への反映
新しいK番号は発行せず、既存K0832へz=1スライス定理を追記。artifact一覧に証明報告・検証器・監査JSON・本ログを登録。research/knowledge/README.mdでは「z≥1未解決」を「z=0,1の全Grundyスライス証明済み、z≥2未解決」へ精密化した。knowledge workflowに検証器実行stepを追加。生成物とroot READMEは直接編集しない。

## 限界と次課題
z=1の全Grundy値は証明済みだが、z≥2の2トークン族全位置予想は未証明。次の最小課題はz=2スライスである。対象はK0832の抽象残余ゲームであり、標準二次元幾何ゲームの勝敗や固定幅安定化長は主張しない。

## CI
mainへ直接反映後、knowledge workflowの実行結果を確認する。ローカルにリポジトリ全体の作業ツリーがないため、uv sync、knowledge check、unittest、生成物buildはGitHub Actionsに委ね、成功確認前に成功とは記載しない。
