# Part EM waves B-E 第二環境検証 log: b38loss24 loss-only adoption (maker / merger / refresh / extractor の出版 bytes からの完全再現 + tamper battery) (2026-11-25)

単一オーナー Part EM (`b38loss24`・24 fresh exact-LOSS 行の loss-only canonical
adoption + reaudit) の waves B-E 成果物に対する独立第二環境検証。検証対象の
一次資料は出版 bytes のみ (owner ホストの作業状態には不触)。本 log は検証
記録であり、新規の数学的主張・verdict 消費・coverage 主張を一切含まない。

## 0. 環境と取得

- 第二環境: Vibe sandbox (Python 3.12.14, 2 vCPU, g++ なし・C++ 第二実装
  gate `9193f5b6…` は不触・実行不可)。node は本検証では一度も使っていない
  (drive/probe なし・純 bookkeeping 検証)。
- 取得: raw CDN から commit `9cf1f53f` 固定で EM dir 16 file / EL dir 16
  file / EF kit 182 file / 共有固定入力 5 file (quarantine / update8 /
  dependency-graph / board / policy) を取得し、MANIFEST SSOT 照合:
  **EM 14/14 pin OK・EL 14/14 pin OK・EF 181/181 sha+size OK**。
  共有入力の board `954d3a10…` / policy `78655e94…` / quarantine
  `81d23160…` は script 内 pin 定数と一致 (refresh 実行時にも fail-closed
  gate される)。
- 直交確認: 検証期間中に main が `9cf1f53f` → `8507df7f` に進んだが
  (K1328 T-Z18 宣言〜公式実行・K1327 PG(2,8)・6 commits)、追加変更 32 file
  に EM/EL/EF 三 dir の file は 1 つも含まれないことを機械確認し、検証
  bytes の正本性は維持された。

## 1. 実行 battery (すべて出版 bytes から・single-call foreground)

- **maker `c787472a…` 3x byte-identical** (rc=0): increment
  `3c6326618944…` (2,638B) / increments-manifest `ac5649f809ee…`、
  ともに出版 bytes と cmp 一致。adopted digest `a56b1cde…`。
- **merger `90711961…`**: selftest PASS (positive dedupe+sort / cross-file
  WIN-LOSS conflict reject no-output / within-file conflict reject /
  malformed row reject / double-run determinism)。**merge 3x
  byte-identical** (rc=0): merged chain head `b5be64e6b96a…` 6,737 行
  (WIN 158 / LOSS 6,579・281,016B) と merge-audit `4a877e17…` ×3。audit の
  input path 字面 (BASE 絶対 path + increment 相対 path) は本環境の
  mirror symlink で再現し audit bytes まで一致。
- **refresh fork `baf9cbde…` 3x byte-identical** (rc=0, 61s / 58s / 57s):
  refresh-summary `bacf6a68…` / closure-classes `93a68897…` /
  per-root-coverage `bce9f8f1…` すべて出版 bytes と cmp 一致。不出版
  probe-worklist.csv の regen sha
  `b4d16b7f21b0f0bc92e6a1022211327f6d3e153f015630f40e9e1f9315cee488`
  (3,719,664B) = MANIFEST 記載の regen pin に 3 走すべてで一致。
- **extractor `2d6ae570…` 2x byte-identical** (rc=0, 117s / 118s): machine
  decomp `cd8bbf898772…` が出版 bytes と cmp 一致。各 run は BASE (EL
  refresh `c0debd18…`) と SCEN (EM refresh `baf9cbde…`) の両 fork を
  scratch tree で再実行し 8 output 全ての byte 一致を gate しており、
  **EM reaudit outputs に加えて Part EL reaudit outputs も出版 bytes から
  誰でも再生成できることが本環境で 2 回再保証**された。
- 機械 deltas は decomp byte 同一性で再現 (= 手転写 0): class 30345 unknown
  50→26 / rank 13→11、class 30484 unknown 5→4 / rank 7→7 (残 4 子は不消費
  probe-level WIN {aj030, ai048, aj049, aj050} のまま)、class 30118
  unknown 52→51 / rank 21→17、witnesses 16371/20421/34908 byte-static。

## 2. tamper battery T-EM1..T-EM6 (単翻訳 byte 反転・事前 sha 変化 assert 付き)

各テストは独立 scratch tree copy で対象 1 byte を反転し (反転前後の sha256
変化をまず assert)、script を実行、rc=1 fail-closed・出力非作成を確認
(EL 検証 lane の教訓「sed no-op 偽陰性」対策の事前 assert を全テストで
実施)。

| tag | 対象 (1 byte) | gate 文面 (最初に落ちた単一 gate) | rc | output |
|---|---|---|---|---|
| T-EM1 | EF kit raw `output/raw/ai001.p1.out` | `ABORT Part EF kit file sha drift: output/raw/ai001.p1.out` | 1 | なし |
| T-EM2 | EF `output/status.log` | `ABORT Part EF kit file sha drift: output/status.log` | 1 | なし |
| T-EM3 | BASE EL merged cache | `ABORT base cache (Part EL canonical) sha drift` | 1 | なし |
| T-EM4 | SCEN EM merged cache | `ABORT scenario cache sha drift` (drift sha を明示) | 1 | なし |
| T-EM5 | EM increments-manifest.json | `ABORT manifest sha drift` | 1 | なし |
| T-EM6 | EM scenario closure-classes.csv | `ABORT scenario closure-classes sha drift` | 1 | なし |

復元 control: 無反転の別 scratch tree で maker rc=0・increment byte
一致 (3c632661…)。root 側の正本 bytes は battery 前後で全 pin 不変
(decomp cd8bbf89… / merged b5be64e6… / manifest ac5649f8… / closure
93a68897…)。

## 3. honest 記録

1. **merger 初回呼び出し形式ミス**: subcommand (`merge`) を欠く CLI 形式で
   argparse rc=2 (usage error) となり、出力は既定 bytes のまま cmp 一致
   「に見えた」が、これは未実行の自明一致であり検証点とは数えず、正形式で
   3x を取り直して成立させた (rc 検証が誤採点を防いだ)。
2. **tamper 関数の echo 誤記 (`${$((…))}` bad substitution)**: T-EM4 の
   第 1 回実行で rc/出力行を採取できなかったため同テストの第 1 回は結果
   不採用とし、echo を修正して同条件で再実行した第 2 回のみを記録とした
   (第 1 回も投入 byte 列と走行条件は同じだが、証跡を落とした点で検証
   記録には使わない)。
3. **実行環境 reset 3 回**: (i) refresh 3x を単一 call の default 120s
   timeout で回した際に timeout 到達で kill され workspace ごと wipe →
   「root 再取得 + pin sweep + battery 再実行」で立て直し、以後は
   timeout 上限 300s + 長い run は 1 call 1 実行に分離した。(ii)(iii)
   call 間の自然 reset 計 2 回も同手順で回復。reset 前に得た maker/merger
   3x の測定は、再構築 tree 上で改めて 3x を実行して採り直した
   (refresh 3x / extractor 2x / tamper 6 + control はいずれも再構築後の
   tree での測定のみ記載)。
4. 本環境は g++ なし (C++ scrutiny gate は相変わらず外部環境専権)。
   並走 lane 成果 (K1327 PG(2,8) / K1328 T-Z18 公式実行) には不干渉。

## 4. 解釈ガード (不変)

- 本検証は Part EM の成果物が「出版 bytes から独立に再現できる」ことの
  第二環境確認のみ。verdict は 1 つも新たに消費しない。
- probe-level WIN 19 行 (incl. ai048)・EXHAUSTED 6 キー・b018・
  aj030/aj049/aj050 は NO cache のまま・nodes は bookkeeping。
- loss-only adoption は class の free 化・excluded 化を行わない
  (reaudit 機械導出の再現で確認)。
- **標準 11×11 空盤・19 central-reply roots・二石 root {49,60}/{59,60}・
  S2 {59,60}・class 30345 (残 26 unknown)・30484 (残 4)・30118 は
  すべて全時点 UNKNOWN のまま。**

## 5. resume notes

1. waves B-E は本 log で 2 環境検証済み (wave F の README/MANIFEST/完了log
   は本環境でも byte pin 照合のみで再実行対象外・run record と 14 pin を
   突合済み)。
2. 次の loss-only 積み上げは **class 30345 残 26 unknown の batch-41
   (rank 11) 宣言 + fail-closed maker** が計算量的に最優先 (EM 完了log
   resume (2) どおり)。
3. C++ scrutiny gate `9193f5b6…` (ai048 を含む 19 WIN 行・30484 残 4 子)
   は依然 g++ 環境の外部提供待ち。
4. Part EJ (batch-40・class 30118) は本検証時点でその後の wave 出版を
   確認できていないため・着手前に必ず最新 main で進捗を再確認
   (EM 出版による re-baseline cache head `b5be64e6…` 必須の規定は不変)。
