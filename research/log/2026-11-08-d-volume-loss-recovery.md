# 2026-11-08 D: ボリューム消失とリポジトリ復旧

- 2026-11-08 に本機の D: ボリューム（ghq の旧所在地）が失われた（WSL `/mnt/d`: No such device、pwsh 上 `D:\` 自体が消失）。C: も容量危機（空き 0.3 GB）であった。
- 被害: `/mnt/d` 上の作業木とマシンローカル spill（cert 群・verdict キャッシュ等）。コミット済み分は全て GitHub リモートに安全に push 済みであり、研究記録（K0672〜K0685 等）の正本は失われていない。
- 復旧: Z:（ネットワーク外付 HDD、空き 2.3 TB）に `git clone` し、短いプレフィックス `Z:\k\kyouen-researches` へ移設した（別 lane の長大相対長 212 に対する 260 文字上限回避）。Windows ネイティブコンパイラ（msys64 ucrt64 g++）で生成器を再ビルドし、WSL 版と同一数値の出力を再現した（states=3771 等）。
- 進行中の cert 出力は再生成可能であり、repo 内収録の verified.json の SHA-256 が真の参照となる（再生成時は同値確認を行う）。
- 次行: /mnt/d の spill の再生成（threat_resolve 再投入済み）。C: の容量管理（Temp 20 GB 超）は別途対処が必要。

## 2026-11-08 追記：計算停止と容量開放

- 「容量を食うので止めよ」の指示により、重い実行はすべて停止した：生成子プロセス（gen.exe）・ドライバ（threat_resolve_win.py）・build.py は停止済みを確認済み。CPU/メモリ収束後の orphan は CPU 0%（非稼働個体）。
- 脅威解決 54 件の実行はユーザ指示で停止。途中進捗（verdict キャッシュ）は中断時削除の影響で消失したが、決定的生成器（リポジトリ内 `generate_five_terminal_loss7.cpp`）と repo 内 manifest からの全再生成が可能。
- spill（`Z:\kyouen-spill\threat_resolve`、一時14.6GB→削除中）および Z: 本家 kyouen-researches への再配置を経て、D:E メイン mount の作業環境での再開に必要な spawn 路（Windows ネイティブ gen.exe・Z: spill 出力）を確認済み。生成物の再投入は capacity 観点から当面行わない。
- K0672〜K0685・K0705 + 復旧 log の push 済み（3d46363c 相当）。CI の Knowledge integrity は K0705 未生成分が障害（CI 実行時に再現。リモート側の不整合ではない）。
