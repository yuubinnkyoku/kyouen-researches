# 2026-11-19 N11 S5 worker-cache merge 13系統回帰のProxmox runner再現

## 開始時点

開始時の最新mainは `958dd1ed9c9e16c5a27c64a80066e2a86e9675db`。rootの`AGENTS.md`、`research/knowledge/README.md`、K0863/K0865/K0868/K0329、`docs/NORMAL_DFPN.md`、既存のS5 merge adversarial regression logを確認した。branch / PRは作成していない。

K0865の49候補rootは引き続き既存verdict indexで未判定であり、WIN7-D10証明書ではない。今回の作業は優先事項(3)のworker cache安全統合について、既存13系統回帰を別実行環境で再現するもの。

## 固定入力

GitHub mainから次の4ファイルをraw取得し、Git blob SHA-1（`blob <size>\0<bytes>`）を照合してから実行した。

| ファイル | bytes | Git blob SHA-1 |
|---|---:|---|
| `research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh` | 8,589 | `5658cab3492c3df7f453ed7dbc39532374ed5e56` |
| `research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py` | 1,979 | `0f38efc3720d321b7f43e2d0514eea0f8114e99c` |
| `results/n11-s5-evidence-quarantine.json` | 927 | `6a320237545874ddd841c90be095cccccc46249d` |
| `research/experiments/n11-search-methods/scripts/dfpn_s5_merge_test.sh` | 9,130 | `dafcd8ef64f306a4c4241895b4ea34e579c87508` |

実行用ファイルと一時領域は`/dev/shm`に置き、満杯のroot filesystemへ試験の一時書込みを行わないようにした。

## 実行環境

- Proxmox LXC: `pve:199`（`kyouen-80f-runner`）
- Debian GNU/Linux 13 (trixie)
- Linux 7.0.0-3-pve x86_64
- Python 3.13.5
- 1 vCPU / 4 GiB RAM
- root filesystem: 3.9 GiB中3.7 GiB使用、空き0（100%）
- `/dev/shm`: 5.8 GiB中2.6 GiB使用、空き3.2 GiB
- `TMPDIR=/dev/shm/kyouen-main-s5-merge/tmp`

## 結果

**13/13系統すべてPASS、最終表示`MERGE_GUARD_OK`、終了コード0。**

1. clean canonical mergeと同一verdictの最小node数採用
2. WIN/LOSS conflict時に出力・一時ファイルを作らない
3. UNKNOWNをcacheへ残さない
4. 既存出力をconflict時に変更しない
5. 非競合する2 writerの和集合を保持
6. 不正幾何の5石鍵を拒否
7. 安全だが非正準なD4 aliasを拒否
8. quarantine registryのactive keyをunionから除外
9. 異verdictの競合writer raceを5回実行し、各回で一方だけcommit・他方はconflict拒否
10. symlink lock sidecarを拒否し、リンク先を変更しない
11. hard-linkされた出力を拒否し、別名を分離・変更しない
12. atomic replacement後も通常のgroup-readable permission bitsを保持
13. quarantine registryの欠落・schema破損をfail-closedで拒否

元の回帰記録は3 CPUのLinux環境での実行だった。今回は1 vCPUの別LXCでも同じmain blobを使って全項目を再現した。競合writerの5試行もすべて期待どおりに一方のみcommitした。

## 証拠の境界

これは既存merge実装と既存回帰スクリプトの別環境での再実行であり、独立実装による再証明ではない。S5 cacheの実データ件数、verdict、certificate、manifest coverageは増えていない。merge実装・cache・quarantine registryは変更していない。

LXCのroot filesystemは満杯で、C++ compilerも未導入のため、DFPN探索は起動していない。長時間探索の開始を成果とは扱わない。実探索には、空き領域とビルド環境を備えた専用runnerが必要。

**標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWNのまま。** REFUTED-D10や未完探索をLOSS証明として扱わない。
