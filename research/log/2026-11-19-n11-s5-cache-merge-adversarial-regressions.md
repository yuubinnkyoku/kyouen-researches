# 2026-11-19 N11 S5 worker-cache merge adversarial regression

## Starting point

作業開始時の main は `aff83906d07c506de2275f3f7ee845df2e4fb893`。最新の `AGENTS.md`、`research/knowledge/README.md`、K0863・K0865・K0868、および `docs/NORMAL_DFPN.md`、S5 cache merge 実装・回収記録を確認した。

K0865の49候補rootは、既存133 child universeでは全49本が未判定であり、WIN7-D10証明書ではない。Proxmox runner `pve:199` は1 vCPU・4 GiB RAMだがroot filesystemが3.9 GiB中3.7 GiB使用、空き37 MiBで100%だった。C++ compilerも存在しないため、この環境でDFPNを起動しない判断をした。今回の実作業は、優先事項(3)のworker verdict cache安全統合を強化する。

## 変更

既存の `dfpn_s5_merge_test.sh` は、clean merge、異verdict conflict、UNKNOWN除外、既存出力保全、非競合writer union、不正幾何の6系統を検査していた。これを13系統へ拡張した。

1. clean canonical mergeと同一verdictの最小node数採用
2. WIN/LOSS conflict時に出力・一時ファイルを作らない
3. UNKNOWNをcacheへ残さない
4. 既存出力を入力として扱い、conflict時に変更しない
5. 非競合する2 writerの和集合を保持
6. 不正幾何の5石鍵を拒否
7. 安全だが非正準なD4 aliasを拒否
8. quarantine registryのactive keyをunionから除外
9. 同一keyへ異verdictを同時投入する競合writer raceを5回実行し、各回で一方だけcommit・他方はconflict拒否
10. symlink lock sidecarを拒否し、リンク先を変更しない
11. hard-linkされた出力を拒否し、別名を分離・変更しない
12. atomic replacement後も通常のgroup-readable permission bitsを保持
13. quarantine registryの欠落・schema破損をfail-closedで拒否

既存のmerge実装・cache・verdict・certificate・manifestは変更していない。新しいWIN/LOSS判定も生成していない。

## 実行結果

- 実行環境: Linux x86_64、3 CPU、Python 3、ローカル一時領域
- merge実装のGit blob SHA-1: `5658cab3492c3df7f453ed7dbc39532374ed5e56`
- policyのGit blob SHA-1: `0f38efc3720d321b7f43e2d0514eea0f8114e99c`
- quarantine registryのGit blob SHA-1: `6a320237545874ddd841c90be095cccccc46249d`
- 結果: **13/13系統 PASS**、5回の競合writer raceすべてで一方のみcommit、もう一方はconflict拒否
- 最終表示: `MERGE_GUARD_OK`

テストはmain上のmerge script・policy・registryのGit blobをローカルfixtureへ再構成し、各blob SHA-1が上記pinと一致することを確認してから実行した。更新したテストscript自体は今回の変更対象であり、実行対象の既存merge実装はbyte-exactだった。

## 境界・次の作業

これはcache統合器の回帰検査であり、cacheの実件数・verdict・証明書被覆を増やすものではない。DFPN探索、証明書抽出、manifest foldは行っていない。49候補rootの実探索は、再現可能なビルド環境と十分な空き領域が確保できてから行う。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN** のまま。REFUTED-D10や未完探索をLOSS証明として扱わない。
