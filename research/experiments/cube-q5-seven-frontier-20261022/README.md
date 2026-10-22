# 7立方q=5：19軌道の境界、再開可能な探索、独立部分証明書

2026-10-22。開始main `b327bbfa8e5276d93f7abb2eb95a9f27cb674854`。
共平面または共球面5点禁止、通常プレイ。点番号は `(x*7+y)*7+z`。
現在の問いはK0505、独立検査した有限構成はK0506。

## 第三手境界

前回の `{0,5}` の35個の未処理第三手を、立方体48等長変換で19軌道にまとめた。
`third-orbits.json` は実盤上の所属第三手、`roots.txt` は各軌道の代表三石局面。
これは同じゲームの対称性による圧縮であり、35手の勝敗を新たに決めたものではない。
残り306第三手の4石終局応手は前回の `coverage-7.json` を使う。

## 探索と再開

`solver.cpp` は前回のDFSから派生した。四点→6ワード禁止点集合を直接保存する
代わりに、四点→32bitブロック番号と、重複を除いた禁止点集合を保存する。
四点しか含まない球面は追加禁止点を持たないため、共通の空ブロック0で表す。
geometry cache上限では表を捨てて再計算し、確定勝敗memoを維持する。

`Q5MEMO2` checkpointは8byte magic `Q5MEMO2\n` に続き、side・累積展開数・
行数のlittle endian uint64を置く。各行はmask6語・label1語・witness6語の計104byte。
labelはP=0/N=1。確定したP/Nだけを書き、UNKNOWNは書かない。
一時ファイルへ全量を書いてrenameし、終了時や中断後も最後の完了rootまで再開できる。
checkpoint自体は独立検査済み証明書ではなく、根の採用には別の証明書検査を要する。

| 試行 | 予算 | 完了root | 結果 |
|---|---|---:|---|
| DFSで19三石軌道 | 各100,000展開 | 19 | 全てUNKNOWN |
| 第三手34に対するx=0面の第四手46個 | 各20,000展開 | 46 | 全てUNKNOWN |
| 単位prior df-pn | 各100,000展開 | 4 | 全てUNKNOWN、その後8GiB上限でOOM |
| 件数制限・平坦prior df-pn | 各200,000、保持50,000 | 8 | 木上限でUNKNOWN、その後手動終了 |
| 深さ重み付きdf-pn | 各250,000展開 | 19 | 全てUNKNOWN |

最初の二つのDFSを継続して、累積2,820,000展開・3,818,433確定memoを保存した。
深さ重み付きdf-pnはその同じsnapshotから継続し、追加4,750,000展開で
8,568,236確定memoになった。DFSは即時終端子の登録を展開数に数えず、df-pnは
展開した終端も数えるため、両者の累積展開数を速度比較には使わない。

`dfpn_unit.cpp` と `dfpn_flat.cpp` は失敗した優先度の再現用。
単位prior版はroot間に未確定木を維持し、深さ5〜6の幅優先展開でメモリを消費した。
平坦prior版は保持件数を制限したが、同じ浅い層に集中し確定memoが増えなかった。
`dfpn.cpp` は深さに応じて正のpriorを重み付けし、未確定木はrootごとに捨てる。
priorで使う17は探索順のパラメータであって、安全石数や手数の上限仮定ではない。
priorだけからP/Nを採用せず、全AND/OR条件を閉じたときだけ確定memoに入れる。

大きなprivate checkpointはGitに入れず、`scratch/cube-q5-seven-frontier-20261022/`
に保存する。`manifest.json` にファイル名・byte数・SHA-256・行数を記録する。
このignoredファイルが別checkoutにも存在すると仮定しない。再生成は以下の手順を使う。

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-frontier-20261022/solver.cpp -o /tmp/q7-dfs
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-frontier-20261022/dfpn.cpp -o /tmp/q7-dfpn
/tmp/q7-dfs --batch 7 100000 30000000 /tmp/q7-a research/experiments/cube-q5-seven-frontier-20261022/roots.txt /tmp/q7.memo
/tmp/q7-dfs --batch 7 20000 12000000 /tmp/q7-b research/experiments/cube-q5-seven-frontier-20261022/fourth-roots-34.txt /tmp/q7.memo
/tmp/q7-dfpn --batch 7 250000 6000000 /tmp/q7-c research/experiments/cube-q5-seven-frontier-20261022/roots.txt /tmp/q7.memo
/tmp/q7-dfpn --batch 7 1000000 6000000 /tmp/q7-d research/experiments/cube-q5-seven-frontier-20261022/descent-roots.txt /tmp/q7.memo
```

この時点で19三石軌道はすべて未解決であり、二石根も空盤もUNKNOWN。
private memoの全8,568,236ラベルを独立検査したという意味ではない。

そのsnapshotから、第三手69の下の五石根 `{0,2,5,26,69}`、`{0,2,5,49,69}`、
`{0,5,26,49,69}` を各1,000,000追加展開した。3件ともUNKNOWNで、最終確定候補は
11,568,207局面、累積展開カウンタは10,570,000になった（`descent-1m.jsonl`）。
五石根への予算であって、三石根69や二石根全体を同じ予算で証明した意味ではない。
`descent-roots.txt` と最新private checkpointで次回はこの続きから再開できる。

## 独立検査した部分証明

DFS checkpointから、根に近い確定局面を `extract.cpp` で検索せず抽出した。

| 占有点番号 | 手番側の勝敗 | 証明書局面数 | 関係数 |
|---|---|---:|---:|
| {1,4,6,22,55,63} | N | 8,314 | 10,705 |
| {1,4,6,22,55,57,63} | P | 8,313 | 10,704 |

両証明は最大15石まで。Nの実際の必勝応手は57で、次の7石P局面に移る。
この6石局面は7立方のisometryで `{0,2,5,26,49,69}` に移せるため、
未処理第三手69の下にある部分木の一部を厳密に確定したことになる。
第三手69そのものや二石根を閉じたわけではない。

`verify.cpp` は探索器を呼ばない独立検査器。Q5CUBE1と6ワードのQ5CUBE2を読み、
Bareiss法の5×5整数行列式から合法手を再生成し、全P境界・N証人・根の安全性・
正規化・全記録の根からの到達性を確認する。幾何cacheは上限で捨てる。
各部分証明の検査で161,740,290回の行列式評価を行った。
外部の既知葉や未検査checkpointのラベルを検査器に入力することはない。

## 17石の極大安全局面

次の17点は安全かつ合法追加点0であることも独立検査した。

`{5,7,9,42,56,68,78,169,178,187,196,220,239,243,247,258,275}`。

`terminal17.cert.gz` はこのP終端1局面の証明書。806,820回の独立行列式評価で
安全性と全343点への追加不可を検査した。したがって7立方の最大安全石数は
少なくとも17である。17が最大だとは主張しない。奇数石の終端があるため、
既知の4石終局と偶奇が異なるので、全終局が偶数石という仮定は使えない。

## 証明書の再検査と回帰

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-frontier-20261022/verify.cpp -o /tmp/q7-verify
python3 research/experiments/cube-q5-seven-frontier-20261022/check_artifacts.py
gzip -dc research/experiments/cube-q5-seven-frontier-20261022/six-n.cert.gz > /tmp/q7-six.cert
/tmp/q7-verify /tmp/q7-six.cert
python3 research/experiments/cube-q5-seven-frontier-20261022/regression.py /tmp/q7-dfs /tmp/q7-dfpn /tmp/q7-verify research/experiments/cube-q5-seven-frontier-20261022/known-roots3.txt
```

回帰は既知3立方の全20二石軌道、checkpoint再開時の追加展開0、幾何cache強制破棄、
7立方のP終端/N局面、偽証明書5種類の拒否、予算0のUNKNOWNを検査した。
`arithmetic.cpp` は独立したstd::bitsetと6ワード演算を12,352例で比較する。
元の7立方104四点配置・35,672合法候補の独立Python比較も新DFSで再実行した。
ソースと結果・圧縮前後の証明書hashはmanifestと `proofs.json` に記録する。
