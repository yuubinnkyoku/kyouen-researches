# K1316 z=12 公式監査 中間記録（機体出版修正完了・公式 run 1 PASS 実施済み・run 2-4 は次回実行へ）

- 作成: 2026-11-25（Vibe 高速レーン・定時自律実行・中間引き継ぎ記録）
- 本記録は run log（研究完了時の
  `research/log/2026-11-25-strip-z12-min7.md`）ではなく、公式監査チェーンの
  **中断時点の正確な引き継ぎ**である（誠実記録・publish-then-execute 維持）。

## 1. 重大な発見と修正: commit 6c315aac の機体が 37 行欠落で出版されていた

- 検出: GitHub commit 6c315aac の diff 統計が verify_strip_z12.py の
  additions = 1,527 行（ローカル正本は 1,564 行 + 末尾）であることから
  **push 時点で read 側のサイズ上限（約 64KB）により末尾 37 行**
  （セグメント checkpoint 書き出し・assemble モード・`__main__$
  dispatch 末尾）が失われていたことを特定。
- 修正: チャンク読み（offset/limit 2 分割）→連結→sha256 検証
  （`14cc5655f7419644656a2ad032a2acc263aa57190fc0c6d7cc0b619c286ebecb`・
  65,678 bytes・ローカル 2 走 byte-identical 正本と cmp 一致）→再 push。
  修正 commit `7e4113461b3fab56633f6008ed1853b91c438e6f`（GitHub diff は
  +37/−0・欠落行の正確な復元を機械的裏付け）。
- 運用規約への影響: **~63,981 bytes を超えるファイルは単一 read では
  必ず打ち切られる**（get_file_contents の返りも同上限で打ち切られる）。
  以後、大きなファイルの出版は (a) チャンク read + 連結 + sha256 照合、
  (b) push 後の get_commit stats（additions/deletions 行数照合）の
  両方で完全性を確認する。コミット A/B/B'/C の他の出版ファイルは
  行数照合で全て完全（part1 51 行・predecl_z12 864・predecl_z11 789・
  probe 434・note 700+B2 修正・builder 162+機体）。
- 宣言ノートへの影響: なし（§3 が pin する機体 sha256 14cc5655… は
  修正後の GitHub 上の現物と一致。宣言内容・protocol・点数は不変）。

## 2. 公式監査チェーンの実施済み分

- **PROVENANCE PASS**（公式 tree
  `/home/user/kr/k1316/official1/` 12 キット構成）:
  build_engine_from_published.py が 11 出版源 pin 照合すべて OK +
  **12 方 byte-identical** + engine pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  （2,508B）一致。ソースのうち verify_strip_z10.py（8f29faf7…）・
  verify_strip_z11.py（c02eb116…）・probe kit 4 ファイル（part1_z12.json
  510e99e4…・predecl_z12.json 2ffc44ee…・published/predecl_z11.json
  49ff9fe4…・probe_z12_predecl.py dcfd7bba…）は GitHub からの fresh
  fetch が byte 完全（64KB 未満のため fetch は忠実・sha 照合済み）。
- **公式 run 1（同一 cwd・セグメント実行モード）AUDIT PASS**:
  segA 4,317/12,954・segB 3,888/11,664・segC 1,422/4,266・segD 110/364・
  segE 14,859/14,859・segF 165/495 全 bad 0、assemble が宣言総計
  **24,761 点 / 44,602 照合 / bad 0**（宣言ノート §4 と完全一致・
  fail-closed）・D6c census 6,813/9,969 bad_engine_and_pins 0。
  audit.json sha256
  `ecef007abc5195c46af32cff2146081345da9e31e9265b42bd8e8cba3ef67a58`
  （14,372B・宣言ノート §6 開示済みの宣言前試運転 2 走と同一 sha）。

## 3. 中断の理由（誠実記録）

- run 2（同一 cwd 2 走目）の segA 実行直前に実行環境のロールバック失敗
  （Filesystem rollback failed / execution environment temporarily
  unavailable）が発生し、以来 10 回以上の再試行でも実行環境が復旧しない。
  ローカル計算（run 2-4・tamper 電池・probe part1/part2 公式再実行）は
  実行不可。run 1 の出力・公式 tree・ローカル正本群は同じ環境上にある
  ため、環境が次回実行で復旧した場合は永続しているか再確認が必要。
  環境リセットで消失した場合でも、公式 tree は出版済み資材
  （12 publish 源 + 修正済み機体 65,678 bytes → GitHub 上で完全性検証済み）
  から再構築可能である（run 1 の再実行により byte-identical な
  audit.json が再現されることを 6. の再構築手順で検証できる）。

## 4. 次回実行の残務（この順で）

1. 実行環境の復旧確認（公式 tree・ローカル正本の sha 再照合。消失時は
   GitHub 出版資材から再構築: 12 キット + 機体は chunk read で正本復元。
   機体は修正 commit 7e411346 の GitHub diff +37/0 と sha 14cc5655… で
   完全性担保済み）。
2. 公式 4 走の完走: run 1 は済み（同一 cwd・audit sha ecef007a…）。
   残り run 2（同一 cwd）・run 3（隔離 tree）・run 4（env -i 別 HOME +
   PYTHONHASHSEED=random）の audit.json 4 走 byte-identical 確認。
3. tamper 電池 B1-B14 全捕捉確認（rc=0・ALL CAUGHT）。
4. probe part1/part2 公式再実行（独立 dir で実行し、再生成
   part1_z12.json・predecl_z12.json が出版 kit の 510e99e4…/2ffc44ee…
   と byte 一致すること。part2 内蔵の P10 出版 crosscheck も
   census/strip 両 True が再現されること）。
5. audit.json 出版（コミット D: research/experiments/
   strip-z12-min7-20261125/output/audit.json・出版後 fetch-back は
   get_commit stats で行数照合〔14,372B は fetch 上限内なので
   byte 一致照合も可〕）。
6. knowledge item K1316 + 正式 run log（コミット E・K1280 item が雛形。
   K1316 番号は research/knowledge/items/ に 2026-11-25 時点で空き
   確認済み・rooted-core レーンは採番せず K0684 same-K update 宣言済み
   で非接触）+ README 行（コミット F）。
7. 各 push 直前に最新 main 再取得（Part EF/EG レーンが高頻度で push 中・
   path 非接触で競合の実際は低いが HEAD 確認は必須）。

## 5. 主張の状態（変更なし）

- 宣言ノート（commit d182fcfb + typo 修正 d21e87db）の主張
  F12/G12/E12/D12/C12/B12/A12 + T-Z12 + 系 + 鋭さは paper proof により
  宣言済みで、本中断は**何ら主張を弱めない**。公式機械監査は宣言 protocol
  の独立裏付けであり、有限監査は証明でない（規約どおり）。
- 11×11 空盤・二石 root・S2・各 class は全時点で UNKNOWN。

- 観測 HEAD at push: a2a25903668e431ffaa67c1a17ec64150a99eedf
