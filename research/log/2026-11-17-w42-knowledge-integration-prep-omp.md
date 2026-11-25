# W42: 知識統合の準備 — K0870更新・W37食い違い13件の照合・push用paths素案 (omp)

- 日付: 2026-11-17
- 作業dir: K0870 編集は `~/workspace/kyouen-omp/kb`、成果物ドラフトは `~/workspace/kyouen-omp/full`
- **push なし・リモートへの書き込みなし。** kb へのローカルコミットのみ実施。
- 数値はすべて実ファイル（git / sha256sum / stat / python json 実読）。推測には [INFERENCE] を付す。

## 1. kb クローンの状態（更新前後）

- 更新前の kb HEAD: `92e6c84d`、origin/main: `02ff4596`。差は **11 commit**
  （内容は Cost81/82 系（n11 lane）の成果、K0937 追加、cost82d batch 1〜5 publish 等。
  K0870 は HEAD と origin/main でバイト同一を `git show …| sha256sum` で確認済み）。
- `git merge --ff-only origin/main` を実行し **3.6 秒で完了、HEAD は `02ff4596` に更新**
  （blobless だがこの 11 commit 分は問題なく取得できた。reset --hard は不要だった）。
- 更新後の `research/knowledge/items/` は 916 項目。task の想定と異なり、origin/main 側で
  K0870 はまだ更新されておらず、W34 案との差異（merge 修正）は発生しなかった。

## 2. W37 §5 の 13 件の照合結果（1件ずつ）

実測環境は full クローン（W37 の数値も同一 working tree に出ている）。
以下、「W37 記述」= W37 §5 各項の主張。

### (1) W31 成果物範囲 — W37 記述は誤り（陳腐化）

- W37: `p2207-drat-full/` に d=2..265、集約 receipt は 258 records / 222,626 B、d=265 実行中。
- 実測（2026-11-17 W42 時点）: `progress.log` は `verdict=VERIFIED` 1082 行、末尾
  `2026-11-17T19:15:29+0000 driver done`。**監査は d=2..1102 の 1,082 点（h=1103 の全 d）
  で完走し d=265 実行中という記述は過去の状態**。集約
  `drat_trim_audit_full_2207_92f0aa9575ed519d.json` は **885,858 B / 1,082 records で全 VERIFIED**
  （実読。d=2..1102、欠測 d=50/100/… なしとまでは確認していないが、unique d 1,082、
  min=2 max=1102）。なお最終行は requested=1082, todo=0, budgets=[5M,20M,100M] で、
  W31 log 時点の形态（100k 単一予算）から進化した driver の再実行である [INFERENCE:
  budget 列の変化から、W31 以降に仕様変更の上の全量再走と推定]。
- 統合時の扱い: バッチ 8（集約 receipt）を push するなら **1,082 records 完走版** を
  commit message に明記。W31 log に完走の追記をするか、完走版を別 log として扱うかは
  W31/W44 側の作業に委ねる。

### (2) ladder-d\*-target1322 系の未追跡ディレクトリ — W37 記述どおり

- 実測: `ladder-d*-target1322-budget*`（.partial 以外）45 ディレクトリ = 候補Aラダー本走行
  （3M/10M/20M × 19 d、決着打ち切り分を含む 45 実行に整合）、`.partial-<時刻>` 90 ディレクトリ。
  git status は experiment 配下 120 件すべて `??`。
- 候補Aラダー自体は前回 push 済み（K0870 が `result.json` を artifact 参照）なので、
  **これらのうち push 候補になるのは K0870 artifact に載る領収書系 JSON のみ**（§4 参照）。
  `.partial` 90 個は走行途中ゴミとして push 対象外。W37 の判断（対象外・要整理）を維持。

### (3) d1292 native の proof が小さい（23,116 B）— W37 記述どおり

- 実測: `ladder-drat-native-d1292-budget30000000/` で proof.drat 23,116 B /
  proof.drat.gz 9,204 B / input.cnf 1,551,714 B / input.cnf.gz 315,764 B。小さいが
  一貫性方針（.drat/.gz/.cnf はすべて対象外、SHA で JSON 再現）に従い対象外のまま。
  W37 の判断を維持。

### (4) W31 集約 receipt の成長 — W37 記述は誤り（陳腐化、(1) と同根）

- 実測: 885,858 B / 1,082 records 完走（§2(1)）。「push 時点の records 数を再確認」の
  要件は充足した。push するなら 1,082 版で確定。

### (5) d=820 領収書の 2 ディレクトリ重複 — W37 記述どおり、push 側を一方に絞る

- 実測: `ladder-drat-native-d820-budget20000000/audit-drat-trim.json` と
  `ladder-drat-d820-budget20000000/audit-drat-trim.json` は **cmp でバイト一致**。
  `solver.json` も cmp でバイト一致。drat-trim.log は未 cmp だが KB0870（更新済K0870）
  に md5 一致の実測記録がある。native 側の audit JSON は verified: true / seconds
  8204.671140 / proof SHA 0e92b79f…34d30 / proof_format binary-drat を実読確認。
- 判定: **意図的な統合コピー**（pysat 宛先に領収書を集約した W33/W34 の設計）。
- 統合時の扱い: push 対象は **native 側ディレクトリのみ**（§4 バッチ 7）。pysat 宛先側は
  `init.json`（749 B、pysat ドライバ由来で別内容）のみ追跡候補に残す
  （kb の K0870 本文が `ladder-drat-d820-budget20000000/` の init.json を
  「追跡対象はこの 1 ファイルに限る」と明記済み）。

### (6) walksat.cpp の SHA 不一致 — W37 記述どおり。W32 log の記載が旧い（現ファイルが正）

- 実測: 現ファイル `walksat.cpp` = `52eacd159bb172dfa263bbd3618ffb7559b7e2040c9d879106f1c4a4e03a058e`
  （11,825 B、mtime 2026-11-17 15:23 UTC）。`walksat_pilot.py` =
  `fb584eec83623eabf52ad8342104989598d2acd939eea4a39bba49fcd13ccc25`（24,380 B、mtime 同日 15:44）。
- W32 log（`2026-11-16-a2647-sat-side-pilot-omp.md` 38 行目）は
  `1a3036f0389b22103d22df15847e6968f1e444770a6a70c235eb075ae993e315` を記載。
  W37 §1.4 が引用した `31209695ae18`（walksat_pilot.py 旧SHA）・`636bea019906`（walksat.cpp
  と主張したSHA）の**両方とも現ファイルと一致しない**。つまり W37 の「現ファイル 636bea01」
  という記述も W42 実測ではもう成立していない（さらに更新が進んだ）[INFERENCE:
  W37 作成後に walksat 系ファイルへさらに編集が入った。pilot-results.json の 44 レコードは
  W32 記載どおり残っているので、pilot 実行後・log 記載後のクリーンアップ編集と推定]。
- 判定: **現ファイル（52eacd15 / fb584eec）が正**。ующий SHA は git 履歴にない
 （full では未追跡）ため旧版のバイトはもう入手できない [INFERENCE]。
- 統合時の扱い: W32 log の SHA 行（および W37 §1.4）を現行値に更新するまで、
  walksat.cpp / walksat_pilot.py は W32 成果として push しない。
  ただし `pilot-results.json` / `eval-check.json`（W37 では log 記載どおり 44 / all_ok 実測）
  は SHA 不整合の影響を受けないのでバッチ 4 はそのまま可。

### (7) W37 スコープ外ファイル（audit_full_3251.py 他）— W37 記述どおり。除外維持

- 実測: `audit_full_3251.py` は実在（19,137 B、mtime 2026-11-17 14:53 UTC、SHA 先頭
  `6a82b5b80bb0`）。docstring は「W41, adapts audit_full_2207.py per
  research/log/2026-11-17-p3251-full-audit-design-omp.md」と明記し、
  **W41 成果であって W31/W32/W33/W28 のいずれの成果でもない**。
- 判定: W37 push 対象外の判断は正しい。**統合対象に含めない**（W41 バッチで扱う）。
  なお `audit_full_2207.py` 自体は `d232e70e43de` で W37 記載どおり変化なし。

### (8) w14-cnf-cache.pkl — W37 の記述は一部誤り（パス）

- 実測: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/w14-cnf-cache.pkl`
  = 15,383,858 B。**`parabola-ternary-selection-20261109/output/` には存在しない**
  （W37 §3 のペースは ternary 側に書いていた）。中身未照合だが名前どおりキャッシュ
  [INFERENCE]。push 対象外の判断は変わりなし。

### (9) W19 成果物の置き場所 — W37 の記述は一部誤り（パス）

- 実測: `parabola-p2207-no-equality-witness-20261107/output/w19-1316-cadical-calib.json`（568 B）、
  `…/w19-1316-cross-rest-jobs4-contended.json`（1,922 B）、`…/w19_rest_probe.py`（4,147 B、
  experiment 直下）とパス中の asterisk が誤植気味だが対象外の実在は事実。push 対象外の
  判断を維持。

### (10) native-solve バイナリ — W37 記述どおり、ただしサイズ実測

- 実測: `parabola-ternary-selection-20261109/output/native-solve` = **1,708,576 B**
  （W37 は未確認としていた）。ビルド成果物で push 対象外の判断を維持。
  `target1322-budget20000000/` は init.json（687 B）+ input.cnf.gz（314,184 B）のみで、
  init.json を実読: d=1323 / target 1322 / budget 20M / Cadical195 / scope unaudited ——
  **候補Aラダー群と同型の d=1323 走行で W33 log 記載の W33 成果の一部**
  [INFERENCE: 文面は W33 log の grep 4 件から。K0870 の artifact には含まれていないので
  W37/W42 の push 対象外。W33 成果の push 時に init.json 単体を含める判断は可能]。

### (11) eval-check.json の all_ok — W37 記述どおり

- 実測: `all_ok = true`（json 実読。11 d / seeds [1,2,3] / random_states_per_seed 3）。
  サイズ 22,558 B。W37 の記述は正確。

### (12) target1322-budget20000000 — W37 記述どおり（§2(10) にて内容まで実測）

- 実測: W33 log に記載あり。init.json の scope 文は「Solver UNSAT is unaudited and
  restricted to this d」＝ unaudited ラダー資産であって K0870 追記の領収書と無関係。
  K0870 artifact にも載っていないため、push 対象外（W33 の別資産として扱う）。

### (13) t5-assump-2207-1102-d735.json が W24 log で既存扱い — W37 記述どおり

- 実測: ファイルは `parabola-t5-partial-sweep-20261116/output/`（352 B）に実在し git 上は
  未追跡。W24b 成果（バッチ C = T5 8 件）の一部として push する判断を維持。
  なおバッチ C の 8 ファイル実在は ls で全部確認（t5_pilot_p2207.py 含む 4 スクリプト +
  output 4 JSON、計 12 個のオブジェクト、ディレクトリ合計 36 KB）。

**まとめ**: 13 件のうち **W37 記述が現状と食い違うのは (1)(4)（p2207 監査の進捗：
258 → 1,082 完走）、(6)（SHA のみならず W37 引用 SHA も陳腐化）、(8)(9)（パスの取り違え）**
。 (1)(4) は監査の進捗による自然な陳腐化、(8)(9) は W37 が記した対象外方針自体には影響しない。
残りは W37 記述どおりで、判断（対象外 / 一方に絞る / 除外維持）を確定した。

## 3. K0870 の更新（kb クローンで実施）

kn クローンを main 更新後に開き、W34 案§3a に相当する冒頭限界の置換と §3c 相当の
artifact 3 件追加は **origin/main 側で統合済み**（今回 merge した main の K0870 は
26 行目に W34 log、37-42 行目に d820 native artifact 3 件を既に含む。

W37 が主 push 対象の receipt と矛盾した記述を残しており、kb で実施した編集は以下 1 件:

- `research/knowledge/items/K0870-p2647-113-budget-ladder-3m-20m.md` の `evidence:` 行
  （W34 案§3c 末尾の「任意だが可」案を採用）:
  「…127,328.3 秒を確認した。」→「…127,328.3 秒を確認した。加えて決着 8 件は DRAT
   領収書 8/8 VERIFIED（W34 ログ）。」

K 番号の衝突: **新規 K を作っていないため再採番は不要。**
kb の item 916 個に K0870 の重複 id はなく（ls 実測）、仮番号運用も発生していない。

### suite 実行（AGENTS.md「統合前の確認」どおり）

実行結果は以下のとおり（kb クローン、commit 未作成の段階で実行し、その後 commit）:

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
```

結果: **すべて緑**（check.py / build.py / diff 表記なし / unittest 全 PASS）。反映済みの
K0870（receipt 未追跡の旨、「複製 3 件は追跡も引用もしない」の注記）と §2(5) の判定
（push は native 側のみ）は整合する。

ローカル commit 実施（push しない）: K0870 evidence 行の追記 1 件。

## 4. push 用 paths ファイルの素案（W37 §6 バッチ → W42 確定版）

`research/log/w42-push-filelist-draft.txt`（5,896 B）を本稿の素案とする。
 バッチ構成は既存 2 案 w42-push-filelist-draft.txt と 2026-11-17-w42-push-paths-draft
 .txt の 2 つの下書きが存在したため、§2 の照合結果を反映して*w42-push-filelist
 -draft.txt*（新しい方、コメント付き）を正とし、修正点は以下。

- バッチ 2（コード）: walksat 2 件は §2(6) の SHA 不整合が解消（W32 log 更新）まで
  保留。よって実質 3 ファイル（audit_full_2207.py / ladder_drat_native.py / native_solve.cpp）。
- バッチ 7 は native d820 側 7 ファイルに絞り、pysat 宛先 d1258 / d1266（実測 3 JSON
  ずつ）をバッチ 6 として独立。
- d=820 の pysat 宛先側は **単独の init.json（749 B、pysat ドライバ由来）**のみ追跡候補に
  残した。
- バッチ 5 の problem-d147-sample.txt（1,516,608 B 実測）は 1.5 MB 単独バッチのまま。
- バッチ 8（W31 集約 receipt）は §2(1) のとおり**完走版 1,082 records**。W31 log に
  完走追記等の整理が要るため、§5.4 の判断が残るが、W42 としては「完走版で push、
  commit message に 1,082 / 1,082 VERIFIED と明記」を推奨。

（バッチ 8 までの合計は 39 ファイル程度。各バッチ 30 ファイル未満・数百 KB 未満で
91 ファイル一括失敗の教訓を満たす。）

push 自体は本作業では実行していない。paths ファイルはドラフトのまま残す。

## 5. 残作業（次のWに引き継ぎ）

1. W32 log（`2026-11-16-a2647-sat-side-pilot-omp.md`）38 行目の SHA を
   `52eacd159bb1…` に更新するか、更新経緯を記す（§2(6)）。 walksat 2 件の push はそれから。
2. p2207 全量監査完走（1,082/1,082）の成果 log・K 項目化（W31 が「パイロット」止まり
   なので、W31 log への追記 or 新規 W44 log）。
3. d1258/d1266/d820 の pysat 宛先ディレクトリの init.json 扱いの最終確認（K0870 本文の
   「d820 宛先 init.json のみ追跡」方針と、実 push する paths の一致検証）。
4. バッチ 9（K0870 更新差分 + W34/W37/W42 log の push）は kb 統合WFの別段階（本稿は
   準備のみ）。

（完）
