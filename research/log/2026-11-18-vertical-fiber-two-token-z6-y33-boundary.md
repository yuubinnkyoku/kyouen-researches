# 2026-11-18 高速レーン: z=6・y=33の2トークン残余ゲームを全称分類（K0967）

## 作業前の確認

- 最新コミット列を確認。開始時の最新main候補は `d9d48bd630edd1d2c25ccbc0be633713291fa58e`（n11レーンのk=22 survival curve拡張）。その直前にK0966（γ枝kodd=4 SIX-ZONE）がmainへ入っていた。
- `AGENTS.md` を確認。main直接反映、knowledge/itemsを正本、experiment/logを分離、generatedとroot READMEを直接編集しない、K番号衝突を確認する方針。
- `research/knowledge/README.md` と `generated/summary.md` を確認。z=6はy=32（K0955）まで連続証明済みで、y≥33・z≥7・全高さ統一式が未解決。純ファイバーt=2,q=10はK0964で解決済み、標準4×m・q=8とは別問題。
- K0955の完全証明報告・検証器、K0953、K0873、K0832のtail定理とTheorem Tを確認。y=33はA/B/Cのx帰納で閉じられるため、次の未解決切片として選択した。
- K0967はmain上に存在しないことを検索で確認してから採番。branch/PRは作成しない。

## 発見と証明

対象は \(H(R;(x,33);6)\)、全 \(x\ge33,R\ge0\)。

A/B/Cの子は
\[
A=H(R-1;(x-1,33);6),\quad
B=H(R-1;(x,32);6),\quad
C=1\oplus H(R-1;(x,33);5).
\]
x=33のAは(32,33)の正準化でBと一致する。x≥34ではAにx帰納、BにK0955、CにK0873を適用する。K0832のTheorem Tで奇数親の子値を{0,1}、偶数親の親値を≤1に制限し、過渡署名表x=33..41と一般署名表x≥42をmexで読む。tailはK0832から \(R\ge x+40\)、値 \((x+33)\bmod2\)。

得られた値2位置:
- 常に {1,3,5}
- x=33: {69}
- x=37: {71}
- x=40: {73,75,77,79}
- x≥41: {73}
- その他の追加位置なし

値1位置の全式・署名表はexperiment reportを正本とする。

## 横断的な一致

y=26..33の8切片すべてで、値2の追加位置は
\[
\{2y+3\}\ (x=y),\quad
\{2y+5\}\ (x=y+4),\quad
\{2y+7,2y+9,2y+11,2y+13\}\ (x=y+7),\quad
\{2y+7\}\ (x\ge y+8)
\]
という同じ形に一致した。8個の個別切片は全称証明済みだが、y方向の一般定理は未証明。ここを次の一般化候補として残す。

## 検証と修正履歴

最初の候補式ではx=34,36,38のP33にtail \([x+40,\infty)\) を入れ忘れ、直接再帰が反例を返した。K0832のtail値はx偶数で1なので、この無限尾を追加して修正した。また一般署名表はx=41が例外で、x≥42では偶数Rの{74}:02とE[76,...]:0への分割が必要だった。修正後は次を全てPASS:
- 順序付き・正準化直接再帰 4,584呼び出し（x=33..56）
- x帰納再帰 5,160状態（x=33..80）
- A/B/C署名 2,077,224件
- mexと閉形式 2,077,224件
- 奇数親子値上界 1,039,104件、偶数親値上界 1,038,120件
- tail 125,952件、xパラメータ1,968件
- 不一致0、独立プロセス2回のaudit.jsonはbyte-identical

有限監査は全称証明の代わりではない。全称性はx帰納・全署名表・K0955/K0873/K0832に依存する。

## main反映

- K0967: `research/knowledge/items/K0967-two-token-z6-y33-boundary.md`
- proof: `research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/report.md`
- verifier: `research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/verify_z6_y33.py`
- audit: `research/experiments/vertical-fiber-two-token-z6-y33-boundary-20261118/output/audit.json`

knowledge READMEと両knowledge workflowへの登録は続けて反映する。generatedとroot READMEは直接編集しない。repo全体のuv sync / knowledge check / unittest / buildはこの実行環境から未実行であり、GitHub Actionsの完了を確認する。

## 最終固定値と登録

- committed verifierのSHA-256をGitHub上の実ファイルから再計算し、`433c49a6530e182255aac0952ed4d3c3485d3c35ff1a2e091611c99f12c69bf7`を確認。
- audit.jsonの正準JSON自己ハッシュを再計算し、`40a3b79315eb78029bfcdcf62e5f0d5f91ff9a55f8ad7df822f3c7fda80746b1`と一致。audit内のverifier hashとも一致。
- knowledge READMEのz=6切片一覧をy=33まで延長し、未解決範囲をy≥34へ更新。K0873/K0944/K0947/K0953/K0955の現在の未解決記述もy≥34へ揃え、K0947/K0953/K0955の横断観察を8切片へ更新。
- knowledge integrity workflowとgenerated-view refresh workflowの両方にK0967検証器を登録。生成領域は直接編集していない。
- GitHub Actionsはpush連鎖後の最新runを確認する。uv sync、knowledge check、unittest、buildの成功はまだ未確認。
