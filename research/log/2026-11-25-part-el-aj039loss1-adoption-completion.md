# Part EL 完了: aj039loss1 (Part EK 30M 再probe の fresh exact-LOSS 1行) loss-only canonical adoption + reaudit 完了 (2026-11-25)

単一オーナー Part EL・publish-then-execute。Part EK 30M 再probe kit
(class 30484 target・aj030/aj039 を 15M honest-EXHAUSTED 履歴の先の
30M 条件で fresh probe・two-pass fresh-cold node-exact・MISMATCH 0)
の産物のうち、**(15M, 30M] で解決した fresh exact-LOSS 行 aj039
1行のみ** (key (1152922606282735616, 65536)・legal 88・s5_index
897668・nodes 16,549,916/order 0) を canonical exact-S5 chain cache
に採用し、reaudit (refresh + delta extractor) まで完了した。

| wave | 内容 | commit |
|---|---|---|
| A | 対抗宣言走査クリーン確定後の単一オーナー宣言 `research/log/2026-11-25-part-el-aj039loss1-adoption-declaration.md` | `11ac123f` |
| B | kit: maker `910ede30…` (EI-maker fork・EK 42-file kit pin 対応・単一行化) + pinned union merger byte-clone `90711961…`。maker pre-dry 3x byte-identical・tamper T-EL1/EL2/EL3 (raw sha / status.log / BASE cache 各改変) 全て rc=1 fail-closed・復旧 byte-identical | `405dcc17` |
| C | outputs 6 files: increment 1,254B `7838b081…` (1行) / manifest `34439f4d…` (schema ek-aj039loss1-increments-manifest-v1) / merged chain head `cf08e181…` **6,713行 WIN 158 / LOSS 6,555** / merge-audit ×3 同一 sha `0ab05a15…`。merger 3x byte-identical | `56bcc871` |
| D | refresh fork `c0debd18…` (EI refresh `1bcf1972…` の 3箇所変更: docstring/CACHE path/sha pin)。3回 byte-identical (~62s/回)。outputs: refresh-summary `4579a021…` / closure-classes `880e1c37…` / per-root-coverage `bafc7b66…` (probe-worklist.csv 3,721,201B は不出版・regen pin `ed289920…`) | `648ef1b0` / `9df5a474` |
| E | delta extractor `compare_deltas_el_adoption.py` `220348fa…` + 機械 decomp `02103ac1…`。pre-dry 3x byte-identical・tamper T-EL4/EL5/EL6 (scenario cache / manifest / closure-classes 1バイト改変) 全て rc=1 fail-closed・復旧 byte-identical | `3f613fc0` |
| F | README.md run record 確定 (7,021B) + MANIFEST-sha256.txt (14 entries) + 本完了log | (本 commit) |

## 出版経路の正直な記録

- 実行環境の自動リセットが本セッション中に複数回発生した。
  (1) wave B〜D 検証中の background 起動 (nohup+disown) pre-dry が
  リセットで殺され `/tmp` 側 log を喪失した。1回は症状が奇妙で
  (両scratch dir 作成済み・stderr 空・rc=1・数秒で終了)、pull から
  push までの哪の段階の state か特定できなかったが、直後の同一構成
  foreground 再実行で全 gate PASS・以後すべて再現したため、実行
  環境リセット時の中途 state 破壊と結論づけた。(2) wave E push
  完了直後 (README/MANIFEST 作成着手時) にリセットが発生し作業
  ミラー `/home/user/kr` 全体が消滅した (EI 完了log に記録したのと
  同一の既知制約)。ただし wave E までの成果物はこの時点で全文
  出版済みだったため、wave F (README run record・MANIFEST・完了log)
  は**出版バイトのみ**から再構成した: main HEAD `2c74f1c6` の
  raw CDN から EL dir の全 12 published files + README stub を
  fetch し全 pin を再照合 (14/14 一致) のうえ MANIFEST 14 entry を
  author した。事前に nohup 由来の不安定さをなるべく排除するため、
  公式 extractor run は単一 bash call 内 foreground 実行 (~2-3分) に
  切り替え、以後の再現は全てこの形で行った。
- ハンドオフ (compaction summary) の測定値メモに
  「fully stable 803 rows」とあったが、直接 diff では **完全 stable
  804 rows + rank-churn-only 2 rows + class 30484 自身の変更 (rank
  9→7・unknown 6→5)** が正しく (803+2+1 = 806 ≠ 807 rows で旧記載は
  1行の行方が合わない)、extractor pin を 804 に訂正してから pre-dry
  に入った。pre-dry は 3 回とも byte-identical・fail なし。
- 並走 (hourly) の別環境レーンが waves B-D の second-environment
  verification log を出版した (`73ca3fe0`・`research/log/2026-11-25-part-el-aj039loss1-waves-bcd-second-environment-verification.md`):
  新規 clone からの maker 3x / merger 3x / refresh 3x byte-identical・
  tamper T-EL1..4 (協調的な two-pass RAW_SHAS rewire を含む) が
  kit-manifest pin 層で捕捉され fail-closed・clean control PASS。
  本 Part の全成果物は 2 独立環境で再現検証済みとなる。

## 採用結果 (honest label・verdict は aj039 の 1 LOSS行のみを消費)

- 採用 1行 = Part EK 30M 再probe の aj039 fresh exact-LOSS
  (two-pass fresh-cold node-exact @30M/order 0・MISMATCH 0・
  16,549,916 nodes/pass・honest EXHAUSTED 15M 履歴を超えた
  (15M, 30M] で解決 = 同一条件再probe ではない・Part EH batch-39
  の 30M WIN aj049/aj050 も 15M EXHAUSTED aj030 も不消費)。
- merged canonical
  `output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache`
  (279,854B) sha256 `cf08e181…` = **BASE (Part EI `73482be0…`
  6,712行・WIN 158 / LOSS 6,554) + fresh 1行 = 6,713行・WIN 158 /
  LOSS 6,555** (3回 merge 同一 bytes・merge-audit ×3 同一 sha
  `0ab05a15…`・quarantine hits 0・BASE 重複 0)。
- **不消費の明示**: probe-level WIN 行 aj030 (15,284,699・WIN-HALT)
  は scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権のまま
  本 Part では 1行も消費せず NO cache。batch-39 盤面の probe-level
  WIN aj049/aj050 も同様に NO cache。claim-reserved dual-class
  batch-38 キー {ai044, ai048} は Part EF in-flight single-owner
  のまま一切触れていない (manifest の claim_reserved_pairs は
  採用対象外の明示用)。

## reaudit 機械導出の確定値 (extractor fail-closed 検証・全 byte 再現)

- **class 30484**: unknown **6→5**・rank **9→7**・groups_served 4
  static・**NOT freed・NOT excluded**。54-child Board 境界を独立
  integer-geometry で再生成 (non-s5 child 0・update8 receipt child
  0・quarantine child 0・BASE known-loss child 48)。残 5子の s5 index
  は機械ピン {892576 aj030 不消費WIN, 900354 ai044 reserved,
  900718 ai048 reserved, 902511 aj049 不消費WIN, 902512 aj050
  不消費WIN}。採用 aj039 (s5 897668) は境界内側の唯一の採用行で
  update8 凍結 baseline requirement の外側。
- **class 30118**: secondary dual-class owner・**byte-static**
  (aj039 は 56-child Board 境界の外。unknown 52 static)。class
  16371 も byte-static。class **20421 / 34908**: rank-churn-only
  (8→9 / 7→8・unknown static)。
- closure表 (807行): left/entered 空・**fully stable 804 + rank
  churn 2行** (groups_served churn 0)・unknown_now 変更は class
  30484 のみ (Board 境界の own-adopted 1行と一致)。
- update8: 完全 byte-static (resolved 259 / remaining 31,600 /
  groups_free_now 131・newly_resolved []・win_hit_groups []・全
  per_root_remaining 不变)。class_status: excluded 390 /
  excluded_now 23 / free_now 39 / unknown 34,497 で完全 static
  (Board 検証 39/39・reject 0 両側)。
- metrics (bookkeeping・決して verdict ではない): joint greedy
  36,505 static (unique_groups 2,115 static)・worklist
  64,366→64,365・known_universe 891→892・cache_in_universe
  868→869・root24 individual greedy 2,782→2,781 (free 12/12・
  uncovered 107/107 不变 = 純 re-selection)・root27 119/119・
  **free/uncovered は全 19 root で完全同一 (= 何も free 化していない)**。
- extractor は毎回 BASE (EI) refresh `1bcf1972…` と SCEN (EL)
  refresh `c0debd18…` の両 fork を scratch で実行し、8 output 全て
  出版 pin と byte-identical であることを gate する (EL reaudit
  outputs が出版バイトのみから誰でも再生成可能なことの機械保証)。

## 解釈ガード

- 採用 1行は fresh (BASE 不在・quarantine 不在・同一条件
  再probe でない)・two-pass fresh-cold node-exact @30M の honest
  label のみ
- probe-level WIN行 (aj030・aj049・aj050) は本 Part では 1行も
  消費しない (いずれも NO cache)。EXHAUSTED 15M 履歴の同一条件
  (15M) での再probe は禁止のまま
- loss-only adoption は class を free化も excluded化もしない
  (class 30484 は残 5子のため unknown・reaudit の機械導出で確定)
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- **11×11 空盤は UNKNOWN のまま。root verdict・coverage claim は
  本dir のどこにも無い**

## 次の実行可能選択肢 (class 30484 残 5子)

(a) scrutiny owner C++ gate (`9193f5b6…`) による probe-level WIN
行 {aj030 (30M), aj049 (30M), aj050 (30M)} の第二実装検証 Part
(WIN 採用は同 gate 専権)。本環境に g++ は無く、外部 C++ 環境
での実施が必要。(b) Part EF 完了による claim-reserved {ai044,
ai048} の解決 (単一オーナー Part EF)。この 2系統の完了が
class 30484 (rank 7) を 0 unknown に落とす最短経緯で、その後
Board 検証による free 化判定が reaudit に回る。最終選定は次 Part
の宣言が fail-closed maker で行う。
