# 2026-11-10 p2207単一CNFの独立schema・幾何・RUP/LRAT監査

開始mainはa3b46aca。AGENTS・knowledge README・K0693/K0702/K0706/K0722、最新log・experimentを確認し、fetchしたorigin/main cf837b1fは取り込み済みだった。対象計算プロセスがないことを確認した。素数3601以降のprobeとwitnesses_3501_3700.jsonの他者変更は保持して取り込まない。

前回中にea4ab649で入ったp2207単一CNF証明は、K0722の正確値1104を主張していたが、入力の独立照合・幾何節の健全性・検査器bindingが保存されておらず、本文末尾には旧範囲に基づく制限も残っていた。今回はその証拠経路を評価し、SAT探索は再起動しない。

## 再現

```sh
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/audit.py --output research/experiments/parabola-p2207-single-cnf-audit-20261110/output --timeout 180
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/regression.py --output research/experiments/parabola-p2207-single-cnf-audit-20261110/output/regression.json
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/replay.py --saved research/experiments/parabola-p2207-single-cnf-audit-20261110/output --output research/experiments/parabola-p2207-single-cnf-audit-20261110/output/replay.json
```

## 結果

保存7720変数・50616節のCNFを、CardEncと探索builderを使わない18748明示構造節と31868幾何節へ全分離した。選択子・counter・点変数の予約範囲に衝突はない。全提供幾何節をgeneric整数4x4行列式で禁止四点と確認した。

任意の安全1105点集合から対状態・点選択・BOTH prefix ORを割り当ててCNFモデルを作れることを明記した。提供辺の完全性はこの方向に不要である。元DRATのhashと497179行を照合し、固定DRAT-trim -UがRUP限定で受理した。抽出187955行・100042045 bytesのLRATを空節処理修正版で受理した。RUPは32.22秒、LRATは16.73秒の経過時間だった。

採用CNF・LRAT gzipを別処理で展開して実再生し、source・schema・幾何・証拠hash、元DRAT、既存1104点下界の入力・receiptとのbindingを全て確認した。原証拠・既存sourceは変更せず、raw coreをローカル保持してGit除外した。

回帰ではp=5,7,11の全1104状態を全counter補助割当の存在射影で検査し、6 schema改変拒否と2幾何制御も成功した。単なるソルバ主張や元の875秒検査logの自己申告に依存せず、独立経路で再検査した。

## 正本と次回

K0693をcomputedへ更新する。旧d別の修正版被覆21/1103は歴史的範囲として維持し、単一CNF経路の完了と混ぜない。K0722は独立下界1104と今回の独立上界1104を結び付けてA(2207)=1104という有限計算の結論へ整合させる。検査器・コンパイラ依存は残り、Lean形式証明や他素数への一般化ではない。

p2531の539/1265とp2647の1303〜1322は今回変更しない。途中で他者のcert-2531-1267、cert-2647-1325、cert-3251-1627が未追跡で現れた。次回はプロセスと最新の正本・保存証拠を確認し、同じ単一CNFの独立schema・幾何・証明再生を適用できるか検討する。これらを今回のcommitへ取り込まない。

## 共通検査と統合

uv sync --locked成功。最初のcheckは並行編集中のK0702/K0708のYAMLエラーで停止した。構文修正後の再実行では704項目・error 0・warning 0、共通unittest33件は211.941秒で成功した。最初のbuildは共有worktree走査中にn11の追跡ファイルを一時的に開けず停止したが、ファイルの存在・未変更を確認後の再実行で生成6viewとREADMEの再生成に成功した。

途中の9cb4ffa3で、別作業の単一CNF証明とK0702/K0708更新がコミットされた。こちらの独立監査はp2207に限定し、その変更を自分の未コミット変更として取り込まない。K693/K722・新experiment・本log・正本から再生成した派生物だけを指定してcommitする。

新experiment17ファイルのraw bytesとindexの一致を確認し、100042045 bytesのraw core.lratは配布用gzipと一致してローカル保持・Git除外されていた。元CNF・DRATと既存検査器sourceは変更していない。生成物stage後の指定diff検査と空白検査も実行する。

commit直前に別プロセスのindex.lockと競合し、stageの失敗後に所有範囲assertで停止した。lockは削除せず再確認した。並行するresetとbbd9d367等でK0693/K0722と派生物がコミットされたが、新experiment17ファイルと本logは未追跡のままだった。コードと採用証明のhash、独立再生の成功、生成物diff 0を再確認したうえで、今回はこちらの未追跡artifactと本logだけを補完してcommitする。
