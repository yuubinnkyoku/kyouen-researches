# 共円ゲーム高速レーン・2026-10-18

新結果：6×6整数格子内の11点部分盤に、禁止四点組がちょうど4個で空盤Grundy値5となる例を構成した。11点は抽象的な4禁則ゲームでも最小。5×5の任意11点集合は少なくとも5禁則を持つため、11点・4禁則以下の整数格子証人が収まる最小正方形は6×6。

実行済み：`verify_geometry.py`、`verify_independent.cpp`、`verify_abstract.py`、`verify_abstract_independent.cpp`。証明は `proof.md`、検証出力は各結果ファイル。二つの幾何判定（円係数／行列式）と二つの抽象Grundy再帰（bit集合／所属型残点数）を使っている。

リポジトリのmain（確認時点 `f0087e81`）への書き込みはGitHub連携の安全検査で拒否された。Gitオブジェクトとして未参照のコミットが作られたが、mainの参照は更新されていない。**main未反映**。`research/knowledge/items/K0440-...` は仮番号の登録案であり、登録時に番号衝突の再確認とknowledge生成物の再生成・回帰検査が必要。branch/PRは作っていない。
