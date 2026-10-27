# 2026-10-27：11×11の初期9石WIN証明4群を第三独立C++終局検査へ

開始時の最新main `2a716a7f2a7b89819c4d2f1d25a9e8ceaeedcb41`、AGENTS.md、knowledge README、K0023、14根250辺再最適化、前回の単独監査修正、degree2・degree2-short・short46・short18・n19の証明実験とCIを確認。**空盤UNKNOWN**。

既存n19用C++17整数4×4行列式・終局再帰の独立検査器を、初期4群を証明書単位で再計算できる検査器へ一般化した。各群の根数・合法9→10石辺・相異なる10石子・合法8石親・終局状態数を個別に固定し、証明書の9石根をD4正準・安全性・全子・逆伝播まで再計算する。4群合計85根・1,386辺・群別集計84,937終局状態（群をまたぐ重複は未除去）。保存勝敗表やdf-pnは使用しない。

`research/experiments/n11-s9-batch-cpp-audit-20261027/independent_terminal.cpp` とREADME、専用CI `.github/workflows/n11-s9-batch-cpp-audit.yml` をmainへ直接反映した。専用CIは4群の再計算と各群4件（合計16件）の改変拒否を行う。総状態数を保存する行間+1/-1改変を含む。

初回CI: https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40471415611 。README反映後CI: https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40471528001 。**CI完了結果はこの記録作成時点で未確認**。成功確認前に第三独立検証の成立を主張しない。成功時にも新規勝敗証明ではなく既存証明の独立性向上である。

証明限定8石WIN4,089類、条件付き14根の未証明辺250本は既知値のまま。新規7石・5石・二石root閉鎖なし。**標準11×11空盤UNKNOWN**。
