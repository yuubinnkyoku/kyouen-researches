# Part CN declaration: batch-28 (class 5343) drive-5 — remaining 23 fileless keys aa032..aa054, WIN-CONTINUE

- 規約: publish-then-execute（本宣言をprobe実行前に出版する）。単一オーナー宣言。
- observed HEAD-before-push: `35cc3702a8904f7a9ab6d10d47ce8a56c5dcc522`（push直前に再取得した最新main。対抗・先行するdrive-5宣言は、research/log の2026-11-23ファイル一覧をこのHEADで機械確認し、存在しないことを確認済み）。
- 非接触確認: Part CG takeover（aa006/aa007 thirdimpl・宣言 `d5e9acc2` 18:01Z）は宣言後35分未満でまだoutputs出版なし → takeover規約の時間条件を満たさないため本Partでは触れない。Part CI batch-29（closure class 2251・scaffold `c6ae987a`）は宣言側セッション所有のため非接触。Part CK drive-4（aa010..aa031・完了 `85d26a2c`）は完結済み。

## 目標

batch-28 (class 5343) の54キー中、Part CB drive-1（aa001/aa002）、Part CH前段のdrive-2（aa003..aa007）、Part CJ drive-3（aa008/aa009）、Part CK drive-4（aa010..aa031）で probed 31 となった残り23キー **aa032..aa054**（s5_index 199717..199739 のbatch内最高s5帯・legal 64..96・ membership 2..4）を、同一のpinned protocolで完走する。

## 事前登録protocol（Part CK drive-4と同一・変更点のみ明記）

1. **探査機**: 公刊pinned runner `scripts/runbatch.sh`（sha256 `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`、byte-clone）。2-pass fresh-cold、budget 15,000,000、`replay,`行の比較対象fields（budget,result,nodes・wall_s除外・raw key/lo/hi一致）が2-passで完全一致することが完走条件。mismatch rc=42 = HARD-STOP。
2. **WIN-CONTINUE設計（Part CE先例・Part CK実績）**: WIN行（result 1・2-pass node-exact）はhonest WIN labelとして記録し、orchestration層はrc=45後も継続する。runner内蔵stop rules（mismatch rc=42 / P1/P2 fail rc=43/44 / WIN rc=45）は不変で、**orchestration層のみ**rc=45を打ち消して次キーへ進む（runner自体は1 WINでrc=45を返す）。EXHAUSTED（result 0）はhonest UNKNOWN・同条件での再probeはしない（COMPLETED exhaustion行のno-15M-re-search規約・file-based completeness guardが再実行を防止する設計どおり）。
3. **session-local orchestration**: `scripts/drive5_local_step.sh`（sha256 `e2ceb7fa278a81307fafae58d975f0cc5f1daa0ec85adcb5ad11c99ba6704f76`・Part CKの `drive4_local_step.sh`（`ea0db83e`）と同一設計）: 未完了キーを先頭2つ選び、worker 2並列（1 worker 1キー）で `timeout 260 bash scripts/runbatch.sh <key>` を実行。**変更点1箇所**: worker timeout 285s→260s（本hostの外側shell呼び出し上限290sに対し、inner timeout側が先に発火して正常returnすることで、外側timeoutによる環境リセットがevidenceファイル書込後に巻き戻る事故構造を排除するため・Part CKの伝統的285sからの機能等価縮小）。truncated passはpublished completeness guardが次invocationでfresh-cold再実行（15M EXHAUSTED級はpass約60-70s→p1+p2が260s窓に収まるか、2 invocation構成になる）。
4. **val-gate（probe実行前・A scaffold出版に同梱）**: 公刊pins 12 byte-clone（`at2m` 2件 budget 2,000,000 / `first-15m` nodes 3,651,923 / `second-15m` nodes 5,040,200 の各input.csv・published-baseline.out・cd2-host.out）+ 本host fresh `.ck-host.out` 4件。fresh runの比較fields（wall_s除外）がpublished-baselineとnode-exact一致を必須とする（4/4でなければABORT）。
   - **宣言前探査の開示**: 宣言push前にtoolchain確認として `at2m-s5-1152921504606851072-536870946` を1回実行した（nodes 2,000,000・result 0・budget 2,000,000でpublished-baselineとnode-exact一致・wall 9s vs published 8s。batch-28のキーは未実行）。これはscript動作確認であり、いかなるbatch-28/29キーにも触れていない。
5. **kit構成**: input 55 byte-clone（batch-keys.json sha256 `af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5`・54キーすべてに変更なし）、output/raw 68 byte-clone（Part CK出版のaa001..aa031・truncated 6件込み）、output/status.log 61-line byte-clone（sha256 `598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8`・drive-4 seed）、scripts 8（7 byte-clone + session-local 1）。
6. **監査**: 完走/誠実打ち切り後に公刊 `row_audit_batch28_win_halt.py`（sha `96867282…`・byte-clone）を3回実行してbyte一致を確認。tamper battery 4種（有効性assertモデル・Part CK T1'設計）をclean control込みで実施し、検出を確認後にbaseline復元をcmp検証。
7. **出版plan**: A scaffold（scripts + input + val-gate 16 + seed output/raw 68 + status.log）→ B outputs（drive-5新規raw + 更新status.log + row-audit json）→ C README + MANIFEST-sha256（全ファイルpinned）→ 完了log。すべてfetch-back byte照合。

## 判定規約（不変）

- verdict不消費: WIN行はhonest WIN label（採用判断はscrutiny owner C++第二実装gate `9193f5b6…` のまま・本レーンは代行しない）。LOSS行（result 2）はadoption候補のみ（採用は別adoption Part・pinned fail-closed merger `90711961…` 経由のみ）。EXHAUSTED行はhonest UNKNOWN（同条件再probeなし・予算引き上げは新宣言条件）。fragmentキーはevidenceでない（complete single passはbookkeepingのみ）。filelessキーはUNPROBED。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・class 5343（54キーすべて・aa032..aa054を含む）はどの時点でもUNKNOWNのまま**。nodes数・wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張はしない。
- 誠実打ち切り: session時間制約で中断する場合、完了済みキーのみをB outputsとして出版し、残りはfileless UNPROBEDとして正直記録する。
