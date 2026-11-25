# 三石69配下の五石N・六石Pを独立検査

2026-10-23。規則は共平面または共球面5点禁止、通常プレイ。番号は`(x*7+y)*7+z`。

前回27,264,695候補行のcheckpointからpriorの底4で100万展開した後、さらに
五石根 `{0,2,5,26,69}` へ最大500万の予算を与えた。307,229追加展開でNを閉じた。
勝ち手は54、座標`(1,0,5)`。着手後 `{0,2,5,26,54,69}` はPである。

証明書では48立方体対称性により次の根へ正規化している。

|元の局面|証明書の正規化済み根|結果|
|---|---|---|
|`{0,2,5,26,69}`|`{7,10,28,42,51}`|N|
|`{0,2,5,26,54,69}`|`{7,10,28,42,51,56}`|P|

五石N証明は431,195局面・580,676辺。六石P証明はその根1件・証人辺1本を除いた
431,194局面・580,675辺。最大16石、終端97,269件。五石N全体を325,137,492回の
5×5整数Bareiss行列式評価で独立検査した。六石Pも別に全証明書を検査した。

## 独立検査の実装と信頼範囲

`verify_incremental.cpp`は探索器をincludeせず、従来の独立検査器を基にした別実装。
幾何は探索器の余因子法を使わず、5×5行列のBareiss整数消去で判定する。
全P局面の全合法子、N局面の合法なP証人、全行の正規化、根からの全行の到達性、
根の安全性を検査する。private checkpointを既知葉として使わない。

検査器でも合法候補を差分更新する。根は全四点組から合法集合を求め、以後は新着手を
含む四点組についてだけ、残っている各候補との5×5行列式を評価する。禁止点は
占有点の追加で合法には戻らないため、これは全合法子の正確な列挙になる。
正規化した変換を候補集合にも適用する。有限性と石数増加による帰納法でラベルが従う。

新検査器は既知3立方20軌道、checkpoint再開、幾何cache追い出し、6ワードの
7立方陽性2件、5件の不正証明書の拒否で回帰確認した（`verifier-regression.json`）。
逆向き親追加と差分合法性の回帰は`retro-regression.json`。これは全7立方幾何の
網羅検査ではない。新しいP/Nの採用は上記の全証明書の検査による。

## 再現

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-balanced-20261023/verify_incremental.cpp -o /tmp/q7-incremental-verifier-repro
gzip -dc research/experiments/cube-q5-seven-balanced-20261023/five-n.cert.gz > /tmp/q7-five-n-repro.cert
/tmp/q7-incremental-verifier-repro /tmp/q7-five-n-repro.cert
gzip -dc research/experiments/cube-q5-seven-balanced-20261023/six-p.cert.gz > /tmp/q7-six-p-repro.cert
/tmp/q7-incremental-verifier-repro /tmp/q7-six-p-repro.cert
```

探索を再構築するにはsix-results.mdの100万展開の後、同じ作業用checkpointで:

```sh
/tmp/q7-balanced-repro --batch 7 5000000 1000000 /tmp/q7-five-repro research/experiments/cube-q5-seven-balanced-20261023/target.txt scratch/q7-base4-repro.memo --base 4 --tree 2000000 --direct
```

三石根 `{0,5,69}`、二石根 `{0,5}`、空盤の勝敗はこの部分証明では決まらない。
7立方の弱解決・全局面の強解決・Lean形式検証を主張しない。
