# 2026-11-19 N11 cost-16 rank-36 preread: Proxmox runnerでのPython再現

## 基準と目的

開始時の `main` は `a956245bfdca40a41b3145d291eedbd202d1259e`。作業前に `AGENTS.md`、`research/knowledge/README.md`、K0865/K0868、および直近のcost-16 rank-35/36記録を確認した。

rank-36 preread logには、公開Python scriptの二重実行・byte-identical確認が未実施として残っていた。公開済みの構造結果を変更せず、固定入力を使ったPython実行を再現し、その未実施項目を埋める。

## 固定入力・実行環境

- script: `cost16_survival_k36_preread_20261118.py`
- script Git blob SHA-1: `cc25c4f3e0c45a21df4006fe4338a8c5c04efdad`
- script size: 36,123 bytes
- pinned aggregate blob: `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`
- pinned k34 preread blob: `8dbb1bcbdaed9bee475f3b95932d35a9500e62cb`
- pinned k35 preread blob: `490fa3a00b8e0b19229c94aa6b1aba4a5604ec13`
- runner: Proxmox LXC `pve:199` (`kyouen-80f-runner`)
- OS/runtime: Debian系Linux、Python 3.13.5、1 vCPU、4 GiB RAM
- 実行時のroot filesystem空き: 約353 MiB

取得したscriptのGit blob SHA-1をローカル計算し、公開pinと一致することを確認してから実行した。script自身も3入力をGit blob SHA-1で検査する。

## 実行結果

最初に二重実行を一つのコマンドへまとめたところ、実行基盤の60秒上限に達した。出力から、1回目は正常終了して33 checks / 0 failuresを出力済みで、2回目の途中でコマンドが打ち切られたことを確認した。これは探索timeoutではなく、検証コマンドを二回連続で実行した際の外側の待機上限である。

その後、保存済みの1回目出力を読み直して `check_count=33`、`all_pass=true`、失敗0件、SHA-256を確認した。2回目は独立したコマンドとして再実行し、同じ33 checks / 0 failuresで完了した。`cmp` によるbyte比較も成功した。

両方の出力は次のとおり完全一致した。

- output size: 16,942 bytes
- SHA-256: `74254b7b0903077001b00c45572e57cee6463b68e55eede9754ca04b46f5248a`
- checks: 33 / 33 PASS
- mismatches: 0
- byte-identical: yes

主要な再現値:

- rank-36 root: `00000000000000801212020000001000`
- covered rows: [19, 22]
- membership: 120,046,727,515,486,665
- A/B split: 92,003,630,985,566,871 / 28,043,096,529,919,794
- new pair census: shared 10 / disjoint 25
- new triple census: b_only 391 / zero 63 / disjoint 141
- new quad census: b_only 2,458 / zero 3,919 / disjoint 168
- new quint census: b_only 2,835 / zero 49,525 / disjoint 0
- full C(36,5): b_only 17,434 / zero 359,558 / disjoint 0
- full C(36,6): all 1,947,792 are zero

## 解釈・境界

これは公開済みrank-36 prereadの同一scriptによる再現性確認であり、第二の独立実装を新たに作ったものではない。preread logに記録済みのTSミラー・第二導出系列の独立性を、この再実行で上書きして主張しない。

また、rank-36の組合せ分類・cover-plan計数であって、DFPN探索、WIN/LOSS verdict、証明書、receipt、manifest閉鎖ではない。行22の初被覆やsextet全zeroからゲームの勝敗を推測しない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN** のまま。

この回は1 vCPUのrunnerで再現確認だけを行い、長時間探索は起動していない。
