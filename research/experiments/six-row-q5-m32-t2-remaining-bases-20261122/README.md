# six-row q5 (6,5) 6x32 t2 remaining-bases scan (2026-11-22 continuation)

K1216 レーンの続編。単一オーナー宣言:
research/log/2026-11-22-six-row-q5-m32-t2-resume-single-owner-note.md
(push b1afb181aaf87b8f5515adaca5acc0065313ee80・宣言時HEAD 05785cdfa5)

config_w32_u3.json (sha256 add8c82f…・K1216出版configとbyte同一) の base 1..23 に対して
scripts/surgery_deep.js (sha256 851e5b7b…・coreはK1216出版pin dfc97506… とverbatim) の
t2 = rem3add2T (targeted-complete・枝刈り完全性の議論はsurgery_deep.js docstringと
K1216記録どおり) を実行した。

## スコープ (限定陰性)

- 各baseについて「base配置 + 全 C(23,3) 除去 × 必要条件を満たすadd対」の完全列挙で
  witnesses=0 = そのbaseの6x32 rem3add2 witnessは存在しない (targeted-complete陰性)。
- 他family由来のbase・rem3add3以上・unblocked>=4対応は含まない。よって本結果は
  6x32全配置の不在主張ではない。M_{6,5}∈[32,658] (K1216) 不変・6x32はUNDETERMINED。
- r0s/r1a1/r2a1/r3a1/r4a1 の24/24完全陰性 (前セッション済み) と合わせ、
  「24 unblocked<=3 base の編集近傍内」の6x32 witnessはrem3add2T級まで(baseごとに)
  存在しないことが確定した。

## 本セッション完走分 (t2 DONE・全0 witnesses・stdout記録値)

| base | label | dsizes | pairs | witnesses |
|---|---|---|---|---|
| 001 | c009@off4 | [67] | 9045 | 0 |
| 002 | c008@off0 | [77,75] | 7850 | 0 |
| 003 | c008@off1 | [62,76] | 6392 | 0 |
| 004 | c008@off2 | [73,63] | 7311 | 0 |
| 005 | c009@off2 | [76,75] | 8175 | 0 |
| 006 | c009@off5 | [69,70] | 7635 | 0 |
| 007 | c011@off4 | [69,58] | 6627 | 0 |
| 008 | c011@off5 | (kitのdone json確認) | (kitのdone json確認) | 0 |
| 009 | c011@off6 | [87,75] | 8457 | 0 |
| 010 | c004@off7 | [69,72,71] | 5572 | 0 |
| 017 | c009@off1 | [79,78,77] | 7298 | 0 |

- base-000 (c009@off3) は前セッションで完了済み (出版 880e288663・pairs=9731・0 witnesses)。

## 未完 (checkpoint resume可・last stdout時も witnesses=0)

| base | label | dsizes | pairs | last doneIdx/1771 |
|---|---|---|---|---|
| 011 | c004@off8 | [61,72,77] | 6843 | 1200 |
| 012 | c006@off4 | [77,58,63] | 5483 | 384 |
| 013 | c006@off5 | [86,72,57] | 5792 | 368 |
| 014 | c006@off6 | [76,87,71] | 6042 | 352 |
| 015 | c006@off7 | [82,76,89] | 7051 | 336 |
| 016 | c008@off3 | [57,77,65] | 5995 | 832 |
| 018 | c009@off6 | [70,73,73] | 7040 | 400 |
| 019 | c010@off3 | [87,65,68] | 6346 | 320 |
| 020 | c010@off4 | [75,83,62] | 5734 | 336 |
| 021 | c010@off5 | [73,78,81] | 5976 | 320 |
| 022 | c010@off6 | [71,76,79] | 6589 | 320 |
| 023 | c011@off3 | [73,59,63] | 5463 | 384 |

## 正本と機械出力の所在

- 本セッション実行のraw (base-XXX.t2.json 完走分・base-XXX.t2.part.json checkpoint分・
  base-XXX.stats.json 更新分) は knowledge kit:
  /home/user/knowledge/kyouen-research/_q65-band-m31plus-kit/output/w32-u3-scan/
  に保存済み (infra failureのfile読出し不能時点で退避を確認済み)。
  次レーン実行時に本ディレクトリ配下へrawを再掲する (受入条件: kit側とのsha256一致)。
- 数値表は本READMEとsession log (research/log/2026-11-22-six-row-q5-m32-t2-resume-session-log.md)
  のstdout記録値のみ。候補数/pairsを勝敗として読まない。

## 実行環境記録 (正直な障害ログ)

- 1実行 = 1 base の 180s time-budget + 16-removal checkpoint resume 設計どおり
  (base-001 で budget stop → resume の doneIdx 継続を確認)。
- 2プロセス並列 (異base同時) で実行。1回の環境reset (timeoutパラメータ未指定事故)。
- 2026-11-22T04:00Z以降: 実行環境 infra failure (bash/filesystem系toolが unavailable、
  GitHub API系toolのみ稼働)。~15分の復旧pollingの後、stdout記録値のみで進捗を出版。
  checkpointはknowledge mountへのsymlink直書きで保護され、上記11完了+12部分の
  進捗は失われていない。