# 7立方: ディスク基礎表・追加確定候補・未確定df-pnの再開

2026-10-23。K0505の4石根 `{0,2,5,69}` を継続するための実装。
基礎表は前回の`balanced-final.memo`（35,412,458候補行）。この全体は独立未検査。
今回の実装だけから根の勝敗は主張しない。確定結果は通常の全証明書へ抽出してから、
K0517と同じ独立Bareiss検査器へ渡す。

## 三つの保存領域

1. 基礎表Q5MEMO2を読み取り専用mmapで参照する。64bit索引セルは32bitの行位置と
   32bitのhash tag。tag一致だけで同一視せず、元の全6ワードを比較するのでhash衝突は
   正誤を変えない。既存の確定候補35,412,458行を巨大なunordered_mapへ再展開しない。
2. 新たなP/N候補だけをメモリ上の追加表へ置く。証明の条件を閉じたときだけ追加する。
3. 未確定局面の合法集合、子と対称変換、128bit PN/DNの有限作業量推定を別に保存する。
   推定値をP/Nとは扱わない。0またはINFを持つ未確定行は復元時に拒否する。

Q5HYB1は基礎表のfingerprint・headerとprior・逆向き親の設定を束縛し、追加表と
未確定treeを単一ファイルへ書く。`.new`を書き終えてからrenameする。
終了マーカーと全レコード長を検査する。基礎表は変更せず保持する必要がある。
fingerprintは誤った基礎表の取り違えを防ぐ非暗号学的識別子で、配布manifestには別途
SHA-256を記録する。checkpointも索引も、独立検査済みの既知葉には使わない。

SIGTERM/SIGINTでは次の探索安全点で中断し、追加表と未確定treeを保存して終了する。
tree上限では深い未確定局面を最大1万展開の完全DFSで処理してから、浅いtreeを
半分まで保持し直す。残したPN/DNは子から再計算する。浅い局面だけを無条件に残す
初期案は小盤面で同じ層を作り直し続けたため、この方式へ修正した。
破棄した未確定の作業量推定から勝敗を推定しない。確定候補は破棄しない。

## 回帰

`regression.json`は以下を確認した。

- 既知3立方20根をディスク基礎表から追加展開0で再利用し、全証明書を独立検査。
- 10展開で中断して復元した探索と、連続探索の展開数・証明書が同一。
- tree上限40の置換を繰り返しても既知P根を閉じ、全証明書を独立検査。
- 切れたファイル、prior不一致、基礎表不一致、不正な未確定合法集合を拒否。

探索の幾何と勝敗閉包は前回の差分更新・底4のdf-pn・逆向き親追加を継承している。
索引とcheckpointは探索の保存・参照方法を変えるもので、ゲーム規則は変えない。

## 再現

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-hybrid-20261023/engine.cpp -o /tmp/q7-hybrid-repro
python research/experiments/cube-q5-seven-hybrid-20261023/regression.py /tmp/q7-hybrid-repro /tmp/q7-legacy /tmp/q7-verify-incremental
/tmp/q7-hybrid-repro 7 scratch/cube-q5-seven-balanced-20261023/balanced-final.memo scratch/q7-base.idx scratch/q7-work.hyb research/experiments/cube-q5-seven-hybrid-20261023/roots.txt 1000000 20 4 2500000 9 scratch/q7-proof
```

CLI末尾は1epochの展開上限、epoch数、priorの底、tree上限、逆向き親の石数上限、
証明書prefix。必要なら最後に`--validate`を付け、復元した合法集合と子の変換を再計算
する。3立方回帰用のlegacy/verifierのコンパイル方法は前回のsix-results.mdと
five-results.mdを参照。基礎表がない場合、前回の再構築手順が必要。

索引はQ5IDX2。初期Q5IDX1索引との互換性はないため別pathで再構築する。
Q5HYB1の追加表・未確定treeは索引のv1/v2間で共通。同じ基礎表・設定で再開できる。
