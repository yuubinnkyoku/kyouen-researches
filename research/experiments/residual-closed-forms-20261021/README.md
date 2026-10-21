# 残余ゲームの構造別厳密評価（2026-10-21）

監査済みK0483（二禁止集合）、K0465（ヒマワリ型）、K0460（最大次数2のグラフ）を共有評価器に組み込んだ。現在の観測結果の正本はK0493。本ディレクトリは入力由来・実行方法・当日の出力を保存する。

## 実装と信頼境界

`cpp/solvers/kyouen_residual_micro.hpp` の `closed_grundy` は、正規化済み・包含極小の残余禁止集合を入力に取る。自由点、辺2本以下、花弁が互いに素なヒマワリ型、全辺が2点かつ最大次数2のグラフを順に認識し、厳密なGrundy値を返す。どれにも該当しない場合は既存の対称点圧縮・成分分割・完全mex再帰へ戻す。自由点は個数の偶奇とのxorで合成する。

Stateは64ビットなので、道の値は0..64の有限mex再帰で初回に計算する。無限周期から範囲外の値を推測する処理はない。閉路の値は残る道の値から0/1へ変換し、非干渉成分をxorする。

通常版と共有キャッシュ版の両方で、圧縮・正準化の前に同じ認識器を使う。検査・比較用に `grundy` / `grundy_shared` の最終引数 `use_closed_forms=false` を指定できる。これは構造別評価だけを止め、既存の圧縮と分割は維持する。df-pn本体の残余評価ゲートは従来どおり明示的に選択する。証明DAG収集と残余ショートカットを併用できないガードも維持した。

`Stats` とreplayの `residual_shadow` 行に `closed_free`, `closed_two_edges`, `closed_sunflower`, `closed_paths` を追加した。これらは評価器内の適用回数であり、盤面全体の出現頻度とは異なる。

## 再帰との照合

既存の全2068小超グラフ検査に加え、独立の占有部分集合DPを使用した。独立DPはkernelの `play`, `normalize`, 圧縮、閉公式を使わず、元の禁止集合が完成する手を直接除外してmexを計算する。

- 6頂点上の非空二辺の全組合せ。同一辺・包含辺・単点辺も含む。全安全局面から残余集合を構成して照合。
- 花芯0..3点、花弁3..5本、非一様花弁、自由点を含むヒマワリ族。
- 3..11頂点の道・閉路の全安全局面、および固定乱数の一般超グラフ120例。
- 64番目のビット、64頂点の道、適用外の三点辺・次数3グラフのフォールバック。

合計107427安全局面について、直接DP、閉公式適用時の値、通常kernel、構造別評価を止めたkernel、共有版が一致した。`kernel-tests.txt` に出力を保存。未定義動作サニタイザでも同じ回帰を実行し `ubsan-tests.txt` に保存した。既存CIが同じC++テストを実行するため、新しい網羅検査も通常pushで走る。

## 保存済み826局面での測定

入力は `research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json` の826局面をすべて使用。新しい未知盤探索は行わない。各残余状態の合法点を0..n−1へ付け替え、各rootのmemoを空にして、構造別評価OFF/ONを交互の順序で各7回測る。両方式のGrundy値が毎回一致しなければ実行を失敗させる。

`benchmark.csv` は各局面の値、再帰呼出数、memo数、各適用回数とroot別時間中央値。`summary.json` はその合計、入力SHA-256と測定条件。時間は各rootの中央値の合計であり、df-pn全体の時間や11×11空盤探索の速度改善を意味しない。比率は同ファイルを正本とし、マシン負荷で変動する。

```sh
python3 research/experiments/residual-closed-forms-20261021/run.py
```

## df-pn本体との統合検査

`integration.py` は同じ保存局面から合法点3..10の各個数と手番偶奇を網羅する16局面を選ぶ。Pythonの独立した全占有部分集合mexで値と元先手固定視点の勝敗を求める。旧版、新版、共有キャッシュ版、影響を与えず照合だけ行う版で全16件の確定結果が期待値と一致することを要求する。予算20000内でUNKNOWNのままなら成功としない。出力は `late-*` と `integration-summary.json`。

旧版の比較基準はコミット `9295ee55` のsolverと残余header。独立した/tmpディレクトリへ両ソースを置き、その他のincludeは現行 `cpp/solvers` を指定してコンパイルした。今回の上流更新は別領域の研究資料だけで、solver基準には影響しない。

```sh
g++ -std=c++20 -O2 -Icpp/solvers cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/residual-fast
mkdir -p /tmp/residual-base
git show 9295ee55:cpp/solvers/kyouen_dfpn_root.cpp > /tmp/residual-base/kyouen_dfpn_root.cpp
git show 9295ee55:cpp/solvers/kyouen_residual_micro.hpp > /tmp/residual-base/kyouen_residual_micro.hpp
g++ -std=c++20 -O2 -Icpp/solvers /tmp/residual-base/kyouen_dfpn_root.cpp -o /tmp/residual-base/solver
python3 research/experiments/residual-closed-forms-20261021/integration.py \
  --solver /tmp/residual-fast --baseline /tmp/residual-base/solver
```

既存CIと同じ3個のS5入力についても、各200000ノード予算で旧版・新版・共有・照合モードを実行した。`replay-input.csv` と `replay-*.csv` がその記録。これらの深いrootのUNKNOWNを解決済みとして扱わない。4モードを並行実行したため、こちらのwall_sを性能比較には使用しない。

標準11×11の空盤勝敗は引き続きUNKNOWN。本変更は残余評価の厳密化・高速化と、明示された保存局面での検証に限る。

## 当日の測定結果

- 826局面すべてのGrundy値が一致。再帰呼出数122720→96570（21.3%減）、memo登録数23646→14410（39.1%減）、730局面で呼出数が減少。
- 最後の7回交互測定ではroot別中央値の合計が約175857µs→149844µs（14.8%減）。単体kernel・この保存コーパス・この環境での時間観測である。
- 16終盤の4モードはすべて独立Pythonの確定勝敗と一致。照合モードは90個の盤面遷移を監査した。証明収集ガードは残余ショートカットとの併用を拒否した。
- 深いS5の3入力は4モードとも各200000ノードでUNKNOWN。照合モードの遷移監査・勝敗照合は合計479097回で不一致なし。`deep-summary.json` はその集計。これらを新しい勝敗証明として採用しない。
- C++回帰・UBSan・knowledge検査（484項目、0 errors / 0 warnings）・knowledge単体テスト33件が成功。生成索引は正本から再生成した。
