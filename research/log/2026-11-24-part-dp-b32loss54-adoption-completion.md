# Part DP 完了: batch-32 (closure class 8730) b32loss54 54-LOSS canonical adoption (2026-11-24)

単一オーナー Part DP・publish-then-execute・宣言
`research/log/2026-11-24-part-dp-b32loss54-adoption-declaration.md` (commit
`4711600e`) に引き続き、全 wave を出版し完結した。
**11×11 空盤・19 central-reply roots・二石root・S2・class 8730 の「rootとしての
勝敗」はすべて UNKNOWN のまま** (class 8730 の free_now は Board-derived な
scheduling bookkeeping・勝敗・被覆主張ではない)。nodes 数は勝敗ではない。

## 出版 wave (全て main 直接・fetch-back byte検証済み)

| wave | 内容 | commit |
|---|---|---|
| A | 宣言 (単一オーナー・HEAD観測・期待値全記載) | `4711600e` |
| B | scripts 4 = maker `44331adc…`・merger byte-clone `90711961…`・extractor `4c16da6e…`・refresh fork (DN `d45832a6…` の) `41bf706f…` | `9b85d4da` |
| C | increment `ca4af3e7…` (54行)・increments-manifest `3f906dc8…`・merge-audit ×3 `5ebfdbfb…`・merged canonical cache `1ded9a08…` (6,502行・WIN 158 / LOSS 6,344) | `4377c987` |
| D | reaudit 3出力 (`74f5dd9b…` / `284bb069…` / `096a9c37…`) + decomp deltas `7def9902…` + 実験dir README/MANIFEST | `8c3b77ae` |
| E | 本完了log | (本commit) |

各 wave 直後に raw fetch-back し sha256/bytes 照合で byte-identical を確認
(全部で宣言1 + scripts 4 + outputs 6 + reaudit 6 = 17 file)。
racing guard: 実行中に他レーン (K-item renumber `74753b66`・
projective-blocking verifier `c3d775da`) が main に先行したが、いずれも
b32loss54/class 8730 非接触・競合なし (各 wave 前に機械走査)。

## 確定機械観測 (宣言どおり・全て reaudit/extractor が出力)

- class 8730 (58子): 54採用 + BASE既知LOSS 4子 (s5 {144458, 212464,
  310606, 311726}) = 58子全て exact LOSS → **unknown から free_now へ**
  (Board 子検証 39/39・rejected 0・free_now 38→39・unknown 34,498→34,497)。
- closure 表 808→807行・left=[8730]・entered=空・完全 stable 27・rank churn
  779・gs_churn 0。unknown 変化は class 8811 のみ (54→52・own採用 2)。
- per-root coverage: root 38 free 13→15 / uncovered 106→104・root 5 free
  8→10 / uncovered 111→109・root 27 119/119 不変・unique_groups 2,119→2,115。
- update8: resolved 185→187 (+2 = s5 {285539, 311727}・ともに採用54内)・
  remaining 31,674→31,672・joint greedy 36,902→36,968 (再選択 churn で
  coverage 後退ではない)・worklist 64,665→64,609。
- verdict 取引: 採用は54 LOSS行のみ。loss-only packet (WIN 0・EXHAUSTED 0)
  のため未消費 WIN は存在せず、scrutiny gate 対象は本 Part に存在しない。

## 公式隔離 rerun (published bytes から全工程再現)

scratch tree に wave B/C の published bytes を raw fetch し、 kit/BASE/
graph/update8/quarantine は pin 検証入力として再構成した上で:

1. maker: rc=0・increment `ca4af3e7…` byte 再現。
2. merger ×3: 全 run merged `1ded9a08…` byte一致 (audit JSON は
   merge-audit-run*.json と入力 file path 表記のみ相違・意味論同一)。
3. refresh: rc=0・4出力 (summary/closure/per-root/worklist) 全て byte一致。
4. extractor: `DECOMP OK changed=1 rank_churn=779 gs_churn=0 stable=27`・
   deltas byte一致。

## tamper battery (sandbox・scratch tree・DNの9項目から本Part構成の8項目)

| # | 改変 | 結果 |
|---|---|---|
| T1 | kit raw ae001.p1.out nodes 1桁改変 | rc=1 `ABORT kit … file sha drift: …ae001.p1.out` |
| T2 | status.log 1行 nodes 桁改変 | rc=1 `ABORT kit … file sha drift: …status.log` (初回の sed が no-op だったのを検出し、改変が入ったことを確認してから再施行した) |
| T3 | status.log に偽装 PASS 行追加 | rc=1 同上 (kit file sha drift) |
| T4 | val-gate host out 削除 | rc=1 `ABORT kit … file missing: …b32-host.out (resolved candidates tried)` |
| T5 | BASE cache 1行 LOSS→WIN 改変 | rc=1 `ABORT base cache sha drift` |
| T6 | increment の複製で採用1キー WIN 改変を merge 注入 | rc=1 `GATE FAILED: WIN/LOSS conflict at 1188950576503717888:262146`・**出力 file なし** |
| T7 | merged (SCEN) cache 改変で refresh 実行 | rc=1 `ValueError: merged cache sha256 drift` |
| T8 | quarantine に採用キー (1188950576503717888, 262146) を active 注入 (両 script の pin を注入後 sha に差し替え) | maker rc=1 `ABORT ae054: quarantined key (1188950576503717888, 262146)` / refresh rc=1 `quarantined key inside merged cache` (出力前に fail) |

全項目 fail-closed・復旧後 maker/refresh とも rc=0 sanity 再通過。
battery 終了後に実験dir全 file (17 published file + 依存 pin 対象) を
元木と照合し **byte-identical** (改変残存なし) を確認。

## honest な限界

- 再構築・隔離 rerun とも単一 host・逐次実行 (並列度 1-2)。大規模中間
  file なし (probe-worklist regen ~3.7MB は repo 外・出版せず regen pin
  `87c2ebd6…` で再現検証済み)。
- batch-32 raw probe の実行本体は Part DM drive-1 (commit `38e6efe8`) の
  出版物であり、本 Part はその読み込み専用採用。
- class 8730 の free_now は「canonical cache 上で58子全て exact LOSS」
  を意味するのみ。11×11 の勝敗・被覆・secured・root verdict の主張は
  一切していない。

次のレーン候補 (本 Part で不変): closure 表上位の小 class
23101 (unknown 1) / 1849 (unknown 1) / 2251 (残1) / 5804 (残4・未消費 WIN 1)。
11×11 空盤は UNKNOWN。
