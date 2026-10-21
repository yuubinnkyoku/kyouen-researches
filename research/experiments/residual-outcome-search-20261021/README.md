# 勝敗のみの残余探索 (2026-10-21)

## 事前プロトコル

完全Grundy数を求める代わりに、局面全体をP/N再帰で判定し、Pの子を見つけたらNとして
打ち切る。成分のP/Nをboolean xorしない。既存の閉形式とSG保存圧縮のみを再利用する。
P/N memoはSG memoと分離し、未完了結果は格納しない。

予算はkernel呼出し数で数え、memo/閉形式hitを含む各呼出しを1とする。0ならUNKNOWN。
盤面からの呼出しでは1 replay root全体で有限のkernel予算を共有し、枯渇後は従来の盤面探索へ
戻る。外側の盤面node予算は別枠で、両者を混同しない。既定handoffはOFFのまま。

検査は既存の独立subset-mex oracle 107427安全状態、2068小clutter、低予算0/1/2、
部分memoを再利用する予算切れ、64ビット境界、通常buildとUBSanで行う。

kernel比較はK0495と同じ保存826局面を使い、各局面でSG法とP/N法を交互に7回、fresh memo。
入力SHA-256と、SG値・P/N値・呼出し数・memo数・局面ごとの時間中央値を保存する。
P/N予算は各根100000呼出し、SGの値が独立の期待値を持つ52局面とも一致することを検査する。

盤面統合の比較は同じ既知52局面と深い3局面を固定し、外側予算5000 nodes、fresh solver/memo、
共有cacheなし、閾値6/12を用いる。設定はOFF、SG6、SG12、PN6、PN12、各3反復。
各反復で設定順を回転し、探索時間と初期化を分離する。P/Nのkernel予算は各根100000。
既知52局面は独立期待値との一致（UNKNOWNなら記録）、深い3局面はUNKNOWNの維持を要求する。
新しい確定値が出たら測定を停止し独立検証する。固定コーパスの有限比較であり、
新しい未知盤の長時間探索を自動workflowへ追加しない。

## 正しさと予算の境界

正常な残余clutterを入力とする。再帰ではplay後の頂点数が必ず減る。
閉形式は既存の完全SG値を0か非0へ変換し、圧縮は既存のSG保存規則を使う。
それ以外では、Pの子が一つ見つかればN、全ての子がNならP、子を判定できなければUNKNOWN。
この帰納法で判定できた値だけを専用memoに置く。成分分解してP/Nだけをxorする操作はしない。
元の先手に関する勝敗への変換には圧縮前のstone数を使う。

盤面のTTへ書き戻すのは確定値のみ。P/N予算が尽きたrootは通常探索へ戻り、そのroot内では
P/Nを再度試さない。次のreplay rootではquotaとP/N計数をリセットする。UNKNOWNを出した同じ
solverで同じrootを再実行し、通常探索と同じ154 board nodesを必要とすることも確認する。
一度本当に解けたrootのTT再利用も別に確認し、予算切れを誤って確定と扱っていないことを検査する。

`--residual-evaluator=outcome --residual-outcome-budget=100000` をexplicitに指定して使う。
既定evaluatorは従来のGrundy、既定handoffはOFF。SG成分共有cacheとの併用は拒否する。
shadow勝敗照合は従来SGを使うのでP/Nと独立だが、この追加SG処理はP/N quotaには含まない。
証明書captureと残余shortcutの併用禁止は維持する。shortcutを無効にした証明書経路は
別実装のtrace変換・DAG検査器で確認する。

予算はwall時間の上限ではない。盤面node上限とkernel呼出しquotaの両方を明記し、
memo/閉形式hitを含むkernel計数を別に保存する。構築・圧縮等の1呼出しあたりの費用も残る。

## 再現

```sh
c++ -std=c++20 -O2 -Icpp/solvers cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/outcome-solver
python research/experiments/residual-outcome-search-20261021/kernel.py
python research/experiments/residual-outcome-search-20261021/oracle.py
python research/experiments/residual-outcome-search-20261021/integration.py --solver /tmp/outcome-solver --output /tmp/outcome-integration
python research/experiments/residual-outcome-search-20261021/run.py --solver /tmp/outcome-solver
python -m unittest discover -s research/experiments/residual-outcome-search-20261021 -p test_protocol.py
python research/experiments/residual-outcome-search-20261021/verify_outputs.py
```

CIでは通常buildの全小clutter/oracle検査、quota/fallback/proof回帰、保存測定の再検査だけを実行する。
時間比較・深い3局面の再探索は自動起動しない。
