---
id: K0008
title: 1×1〜9×9証明書の独立C++全件検査
kind: verification
status: verified
topics:
- certificates
- verification
aliases: []
relations:
- type: verifies
  target: K0007
  note: 具体的な1..9の局所条件の実検査
- type: verifies
  target: K0011
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0012
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0013
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0014
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0015
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0016
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0017
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0018
  note: 当該空盤の公開AND/OR証明書の独立検査
- type: verifies
  target: K0019
  note: 当該空盤の公開AND/OR証明書の独立検査
artifacts:
- path: cpp/certificate/kyouen_certcheck.cpp
  role: verifier
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/all-certificates-check.txt
  role: log
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/certificates.csv
  role: manifest
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: release-assets/SHA256SUMS.txt
  role: manifest
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 1×1〜9×9証明書の独立C++全件検査

探索器と別の `kyouen-certcheck` が座標から禁止四点組・合法手を再生成し、WIN証人・LOSS全分岐・安全性・rank減少・D4正規化を全ノード検査する。

| 盤面 | 証明書ノード数 |
|---|---:|
| 1×1 | 2 |
| 2×2 | 5 |
| 3×3 | 28 |
| 4×4 | 135 |
| 5×5 | 1,217 |
| 6×6 | 21,712 |
| 7×7 | 393,550 |
| 8×8 | 8,744,406 |
| 9×9 | 13,457,134 |

全件検査記録とhash/sizeをrepo内に保存。巨大raw証明書・圧縮配布物の存在をGit管理ファイルと混同しない。この移行では既存検査記録の監査を行い、92MiB配布物の再展開・全件再検査は実行していない。
