# 2026-11-17: ラダー決着8件の DRAT 監査完了に伴う knowledge 更新ドラフト (W34, omp)

対象: 候補A予算ラダー（`research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md`）で
SOLVER_UNSAT 決着した 8 d の DRAT 領収書。W28
（`research/log/2026-11-16-a2647-ladder-drat-receipts-omp.md`）が 4 件 VERIFIED・d=622 検証中で
打ち切った後、W33（`research/log/2026-11-16-a2647-ladder-drat-native-omp.md`）のネイティブ経路で
残りを埋め、**8/8 が drat-trim VERIFIED** になった状態を知識項目へ反映する差分案。

**本ログはドラフトであり、knowledge 項目もコードも編集していない。** 数値はすべて保存済み
JSON（`audit-drat-trim.json` / `solver.json` / `init.json` / `result.json`）と、その場で再計算した
ハッシュからの転記。推定には `[INFERENCE]` を付す。

## 1. 8 件の実読表

出力: `research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-d<D>-budget<B>/`
`seconds` は `audit-drat-trim.json` の `seconds`（チェッカ呼び出しの実測経過。stdout の
`c verification time` より 0.03〜0.5 秒大きい＝プロセス起動等の差）。

| d | 段 | verified | seconds | proof_sha256 | input_sha256 |
|---|---|---|---|---|---|
| 1292 | 3M | true | 0.242352 | `95dafdaa570519452db5bce806452b6a3d53d384c3ba49993b41aba63c529538` | `f144e4dcf1a358b159641989879815b39b59e57da99a40a4fa0dc52ce82937e8` |
| 977 | 3M | true | 144.588479 | `ef1219dff4f17455cc56500315f6aa91539f056d882b37114a654f8c657ef86e` | `3e1cbe1d7ffc5ad37c10389ef394d6866932c9446281b53b71e95085c2c89840` |
| 1040 | 3M | true | 223.534723 | `f79aa37821c806ecf29325ab2a7006b4932db4588bf44b78b6bb5d3eddc49836` | `5602843db350e6e6ae01d4ee2a59ba6bc99f554dd6b6d1a90b686fc74ab19440` |
| 914 | 3M | true | 212.290142 | `926f4e036268521a3f89562a6cd072c92094b5ea96757e3407bdd029c9f47074` | `b2d99061aaeb9d9cd3077d4fe8c3bfcb774d2e1a2618007eb07367c719c66ffa` |
| 622 | 3M | true | 576.327351 | `f15b5e44e577df7989c59151a7fdd33bb7f8886c8034b6b73f2113e3a7a7aa38` | `eadafdf44405a68b0fe9e8ecff7411c69b1588118fca8b19397dec2ab5ca1b7a` |
| 1258 | 10M | true | 1564.196035 | `943e374d6885c2ca87810cbe1482c54c3b443c9f3ab3d8543bdac8577302cc4f` | `c51d5cfbc7b0bd55d1a96f9f8822b9ef6453d03b43490f6d8d24ae8f8e2802c3` |
| 1266 | 10M | true | 1501.090970 | `17bdaabaf1fa11c1d5d2c202273b0cb108e804cdcc83f8bc30109f6ff12192dd` | `68ff0344de6cd6f08ac41e65af0a6243aca83f17c48e3efb8966286e37cae97a` |
| 820 | 20M | true | 8204.671140 | `0e92b79f8960c0830967994d0c518be0d9a0a2c49a8ed1c43dc9dc420a734d30` | `1c2dece33115f9d0c41625c3c0611a79525fb157ed42398ddfe63a0fe7c990e7` |

8 件の検証時間合計 **12,426.94 秒**（JSON `seconds` の単純和）。全件 `returncode: 0`,
`timed_out: false`, `checker_binary_sha256` = `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`
（W28 と同一バイナリ）, `checker_source_commit` = `2e3b2dc0…d9a985`。

### 1a. 証明の表現

- d=1292, 977, 1040, 914, 622, 1258, 1266: ASCII DRAT。`proof_lines` はそれぞれ
  3,514 / 1,056,572 / 1,069,706 / 1,408,769 / 3,801,225 / 8,666,047 / 7,800,374 行。
  解凍後バイト数は 52,300 / 110,846,598 / 110,180,521 / 168,211,108 / 501,762,222 /
  1,450,845,303 / 1,325,240,618 B（`gzip -l` 実測）。
- d=820: **binary-drat**（`proof_format: "binary-drat"`、`proof_lines: null`、
  `proof_bytes: 2367583553`、`proof_steps {added: 19610968, deleted: 19564515}`、
  `proof_gz_sha256: 1e37e59cad022cb939f666e14617144f0c6b1e04a1e57e92bb5d7e647d350154`）。
  drat-trim ログも `c turning on binary mode checking` で始まる。ASCII 版の 7 件とは
  形式・生成経路が違う。

### 1b. d=820 の来歴（ネイティブ）

- solver: `cadical-native` 3.0.1（libcadical `c60730422e758ef1cebe7aeddf2dda31c996bf04`）、
  shim `5d3fc38e…f67c7`（source）/ `e5afb8d5…74e0`（binary）、
  `solver_binary_sha256` `26a5daca…fde41`。
- `solver_status: SOLVER_UNSAT`、`solver_exit_code: 20`、`statistics.conflicts` **19,442,067**、
  `solve_seconds` **4,820.636161**、`wall_seconds` 4,820.895、`max_rss_kb` 98,272、
  `phase_hints` 3,966。
- 検証完了時刻: `audit-drat-trim.json` / `drat-trim.log` の mtime **2026-11-17 10:43:47 JST**。
- 領収書は 2 ディレクトリに存在し、**中身は同一**（実測で確認）:
  - `output/ladder-drat-native-d820-budget20000000/`（一次。`proof.drat`＝非圧縮 binary 2,367,583,553 B
    も保持、`run.log` / `phases.txt` / `input.cnf` あり）
  - `output/ladder-drat-d820-budget20000000/`（統合先。`proof.drat.gz` のみ）
  - `audit-drat-trim.json` はキー・値とも一致、`solver.json` は md5 一致、
    `drat-trim.log` は md5 一致、`proof.drat.gz` は SHA-256
    `1e37e59c…d350154` で一致、`input.cnf.gz` は
    `c056ea4dc13dc3dabdffc468ed7b27ae3fad1ee837c3297750c09ebe9cfebfa7` で一致。

### 1c. 本ドラフトで実行した再計算（JSON との照合）

- `input.cnf.gz` を解凍した SHA-256 が 8/8 で `audit-drat-trim.json` の `input_sha256` と一致。
  さらに 8/8 でラダー側 `ladder-d<D>-target1322-budget<B>/init.json` の `encoded_cnf_sha256`
  と一致（＝再実行 CNF はラダーと同一入力）。
- `proof.drat.gz` を解凍した SHA-256 が 8/8 で `proof_sha256` と一致
  （d=820 は binary 2,367,583,553 B のまま `0e92b79f…34d30` に一致）。
- `solver.json` の `proof_sha256` と `audit-drat-trim.json` の `proof_sha256` が 8 件すべて一致。

## 2. W28 ログとの照合

W28 の記述は**数値レベルで矛盾しない**。差は「d=622 が検証中、1258/1266/820 未着手」という
進行状況のみで、これは現在の状態で置き換わる。

- 4 件の VERIFIED（1292 / 977 / 1040 / 914）: W28 の check_seconds 0.24 / 144.59 / 223.53 /
  212.29 は JSON `seconds` 0.242352 / 144.588479 / 223.534723 / 212.290142 と一致。
  `proof_lines` 3,514 / 1,056,572 / 1,069,706 / 1,408,769、`proof_sha256` の先頭・末尾
  （95dafdaa…c529538 / ef1219df…57ef86e / f79aa378…dc49836 / 926f4e03…c9f4707）も一致。
- d=622: W28 は「solve 完了・検証中、`audit-drat-trim.json` 未生成」と書く。現在は存在し
  `verified: true`、`seconds` 576.327351、`proof_lines` 3,801,225、`proof_sha256`
  `f15b5e44…a7aa38`（W28 が引用した solver 側の値と同一）。矛盾ではなく進展。
- d=1258 / 1266 / 820: W28 は未着手。現在は VERIFIED（1564.196035 / 1501.090970 /
  8204.671140 秒）。W28 の所要見込み「1258/1266 は約 0.5〜1 時間規模」は実測 26 分・25 分で
  範囲内、「820 は 1 時間超」は実測 2 時間 17 分で範囲内。
- W28 の「入力 CNF はバイト一致」は 4 d での確認だったが、**今回 8 d すべてで
  `encoded_cnf_sha256` 一致を確認**した（§1c）。

**明記すべき非対称（矛盾ではないが、W28 の枠組みの外）**: d=820 は W28 の方式
（pysat Cadical195, ASCII proof）ではなく W33 のネイティブ方式で解かれた。したがって

1. conflicts はラダー／pysat 系と一致しない: ラダー `result.json` 13,294,778
   （pysat, 3,813.133 秒）に対し、ネイティブ再解は 19,442,067（4,820.636 秒）。
   一致するのは「入力 CNF のバイト」と「UNSAT という判定」だけである。
2. `output/ladder-drat-d820-budget20000000/` は**pysat の領収書ではない**。このディレクトリの
   `init.json`（mtime 2026-11-17 22:07）は `solver: Cadical195` / `python_sat: 1.9.dev21` と
   書くが、同居する `solver.json` は `cadical-native`、`audit-drat-trim.json` は binary-drat。
   `ladder_drat.py` は `solver.json` が存在すれば solve をスキップするため、ネイティブの
   `solver.json` を置いたディレクトリを pysat ドライバが後から開くと、この取り合わせが
   再現する。**統合時、このディレクトリを pysat 方式の領収書として説明してはならない。**

## 3. K0870 の差分案

対象: `research/knowledge/items/K0870-p2647-113-budget-ladder-3m-20m.md`
（title / kind / status / scope / evidence は変更しない。status は `computed` のまま。）

### 3a. 「限界」冒頭の第 1 箇条（現行 78–81 行目）

置換前:

```markdown
- **8 件の SOLVER_UNSAT はソルバの主張のみで、単体の DRAT 証明は保存されていない。**
  出力ディレクトリに proof は無く、`scope` も unaudited と明記する。
  領収書付きの UNSAT ではない（K0737 の問いと同種の未監査）。監査には該当 d を
  DRAT 付きで再実行する必要がある。
```

置換後:

```markdown
- **本ラダー自体の出力には proof が無い**（`ladder-d<D>-target1322-budget<B>/` は
  `init.json` / `input.cnf.gz` / `result.json` のみで、`scope` も unaudited と明記する）。
  ただし決着 8 件の SOLVER_UNSAT はすべて、同一入力・同一予算の再実行と drat-trim による
  独立検証で領収書化済みである（下記「追記（2026-11-17）」）。ラダーの生出力と領収書は
  別ディレクトリであり、前者は今も未監査のまま保持する。
```

### 3b. 末尾の追記ブロック（現行 89–94 行目）を丸ごと差し替え

置換前:

```markdown
- 追記（2026-11-16、統合時）: 上記の「DRAT 証明は保存されていない」は本ラダー自体の
  出力についての記述であり、その後の再実行（W28）で 8 件中 5 件
  （d=1292, 977, 1040, 914, 622）は DRAT 証明付きで再解され、drat-trim で
  VERIFIED となった（領収書は `output/ladder-drat-d<D>-budget<B>/`、
  記録は `research/log/2026-11-16-a2647-ladder-drat-receipts-omp.md`）。
  残り d=1258, 1266, 820 は未監査のままである。
```

置換後:

```markdown
- 追記（2026-11-17、W34 統合）: 決着 **8 件すべて**が DRAT 証明付きで再解され、
  drat-trim で **VERIFIED（8/8）**となった。領収書は
  `output/ladder-drat-d<D>-budget<B>/` の `solver.json` / `audit-drat-trim.json` /
  `drat-trim.log`（証明本体はバイナリのため未追跡）。d ごとの drat-trim 秒数:

  | d | 段 | 検証秒 | 証明形式 |
  |---|---|---|---|
  | 1292 | 3M | 0.24 | ASCII |
  | 977 | 3M | 144.59 | ASCII |
  | 1040 | 3M | 223.53 | ASCII |
  | 914 | 3M | 212.29 | ASCII |
  | 622 | 3M | 576.33 | ASCII |
  | 1258 | 10M | 1,564.20 | ASCII |
  | 1266 | 10M | 1,501.09 | ASCII |
  | 820 | 20M | 8,204.67 | binary（ネイティブ） |

  各再実行の `input.cnf.gz` はラダーの `init.json` の `encoded_cnf_sha256` と一致する
  （8/8 で実測照合）。したがって本ラダーの 8 件の SOLVER_UNSAT は、記録済みの
  入力同一性のもとで独立監査済みである。記録: W28
  `research/log/2026-11-16-a2647-ladder-drat-receipts-omp.md`（最初の 4 件と d=622）,
  W33 `research/log/2026-11-16-a2647-ladder-drat-native-omp.md`（ネイティブ経路の設計）,
  W34 `research/log/2026-11-17-w34-knowledge-update-draft-omp.md`（8/8 の集計）。
- 追記（2026-11-17）の限界 — **d=820 だけは pysat 方式ではない**。ネイティブ CaDiCaL 3.0.1
  （libcadical `c6073042`、証明をディスクへストリーム）で解き、binary DRAT
  （2,367,583,553 B、`proof_sha256` `0e92b79f…34d30`、added 19,610,968 / deleted 19,564,515）を
  drat-trim の binary モードで検証した。ASCII 版 7 件とは証明形式が異なり、conflicts も
  ラダー側の 13,294,778 ではなく 19,442,067（solve 4,820.64 秒）である。両者が共有するのは
  入力 CNF のバイト同一性と UNSAT 判定だけであり、conflicts の一致を領収書の根拠にしない。
  なお統合先 `output/ladder-drat-d820-budget20000000/` の `init.json` は pysat ドライバが
  後から書いたもので `solver: Cadical195` と表示するが、同居する `solver.json` /
  `audit-drat-trim.json` はネイティブ由来（binary-drat）である。このディレクトリを
  pysat 方式の領収書として引用しない。
- 追記（2026-11-17）で**動かないもの**: UNKNOWN 37 件は依然 UNSAT でも SAT でもなく、
  クラス (1,1,3) の判定は未了、A(2647) の範囲 1296 ≤ A ≤ 1322 は不変である。
  8 件の領収書は「決着した d の UNSAT が入力同一性つきで監査された」ことだけを意味し、
  非標本 14 d や 20M 超の予算への外挿を含意しない。
```

### 3c. artifacts への追加（任意だが推奨、現行 34–37 行目の直後に挿入）

```markdown
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-d820-budget20000000/audit-drat-trim.json
  role: data
  note: 8/8 完了を閉じた d=820 の drat-trim VERIFIED（8,204.7 秒、binary-drat 2,367,583,553 B）
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-native-d820-budget20000000/init.json
  role: data
  note: d=820 のネイティブ領収書の来歴（CNF 一致判定と参照 pysat 領収書、solver 同定）
- path: research/log/2026-11-17-w34-knowledge-update-draft-omp.md
  role: log
  note: 8 件の監査表・W28 との照合・限界の整理
```

既存 3 番目の artifact（`.../ladder-drat-d622-budget3000000/audit-drat-trim.json`）の
note「W28 の領収書の代表。d=622 の drat-trim VERIFIED（576.3 秒、証明 3,801,225 行）」は
現行 JSON（576.327351 秒、3,801,225 行）と一致するので**変更不要**。

`evidence:` 行（現行 38 行目）はラダー 45 実行の集計についての記述なので変更不要。
8/8 監査は本文の追記で担う。ただし統合担当の判断で
`evidence:` の末尾に「加えて決着 8 件は DRAT 領収書 8/8 VERIFIED（W34 ログ）」を足すのは可。

## 4. K0869 / K0706 の要否判断

### K0869 — 追記不要

- K0869 の scope は「size=1322 の形状クラス (0,0,1),(1,0,2),(0,1,2) の単体 CNF」で、
  明示的に (1,1,3) を除外している。本ラダーの領収書は (1,1,3) の **d 固定 CNF
  （クラス CNF ∧ B_d）** に対するもので、K0869 が検証した 3 クラスの CNF とは別物。
- K0869 の status `verified` は「その 3 クラスについて検査済み」の意味しか持たず、
  8/8 で変わる数値も変わらない。
- 逆に K0869 に (1,1,3) の進展を書き込むと、「(1,1,3) も監査が進んだ」＝上界 1322 の
  監査状態が動いたという誤読を招く。A(2647) の範囲は不変（K0706 の 1296 ≤ A ≤ 1322）。
  以上から**変更しない**のが正しい。クロスリンクも不要（K0870 側から K0869 への言及は
  現行の K0768 経由で足りている）。

### K0706 — 追記不要

- K0706 の根拠は「全 1323 d の CNF UNSAT ＋ 全 1323 d の DRAT を修正版検証器で
  1323/1323 VERIFIED」であり、本ラダーの 8 件（19 d の標本、別符号化の d 固定 CNF）より
  被覆が広い。8 件の領収書は K0706 の証拠を強めも弱めもしない。
- K0706 の限界節は既に「(1,1,3) は未解決（UNSAT なら A ≤ 1321、SAT なら A = 1322）」と
  書いており、8/8 でこの記述は変化しない（8 件は 19 d の部分標本でクラス判定ではない）。
- K0706 は命題 `A(2647) < 1325` の項目であり、ラダーの予算軸は K0870 が担う分担に
  なっている。同一命題の状態更新でも証拠追加でもないので追記しない。
  （任意で 1 行のクロスリンクを足すのは可だが、必須ではない。）

### 参考: K0768 — 追記不要

K0768 の本文（51–52 行目）は「d=1258,1266 が 10M で SOLVER_UNSAT に到達（K0870）」と
K0870 を参照するのみで、監査状態についての主張を含まない。8/8 で書き換える文がない。

## 5. 統合時の注意

1. **K 番号**: 本ドラフトは新規 K を作らないため再採番は不要。ただし remote main では
   前例として新規項目が再採番されている（W27 ドラフトの仮 K0726 → main の K0870、
   仮 K0725 → main の K0869）。統合前に remote main の
   `research/knowledge/items/` を確認し、K0870 の参照（K0768 の 2 箇所）が生きていることを
   確かめる。
2. **生成物**: `research/knowledge/generated/` と root `README.md` は派生物。編集せず、
   AGENTS.md の手順どおり正本 merge → 番号衝突解消 → 再生成の順で:
   ```sh
   uv sync --locked
   uv run --locked python tools/knowledge/check.py
   uv run --locked python -m unittest discover -s tools/knowledge/tests
   uv run --locked python tools/knowledge/build.py
   git diff --exit-code -- README.md research/knowledge/generated
   ```
3. **領収書の追跡**: 現時点で `ladder-drat-d1258-budget10000000/`,
   `ladder-drat-d1266-budget10000000/`, `ladder-drat-d820-budget20000000/`,
   `ladder-drat-native-d820-budget20000000/`, `ladder-drat-native-d1292-budget3000000/` は
   **未追跡**（W28 の 5 件は追跡済み）。artifact に path を書く以上、少なくとも
   `init.json` / `solver.json` / `audit-drat-trim.json` / `drat-trim.log` を追跡対象にすること。
   `proof.drat.gz`（d=820 で 1.32 GB）と `input.cnf.gz`、`proof.drat`、`input.cnf`、
   `phases.txt`、`native-result.json`、`run.log` は追跡しない（SHA-256 が JSON にあり
   バイト再生成可能）。`output/native-solve`（ビルド済み shim）も追跡しない。
4. **d=820 の記述**: §2 の非対称を必ず反映する。`ladder-drat-d820-budget20000000/init.json`
   を根拠に「pysat で再解した」と書いてはならない。一次領収書は
   `ladder-drat-native-d820-budget20000000/` 側。
5. **数値の丸め**: 本文で 1,564.20 等と書く場合、原値は JSON の `seconds`
   （1564.196035）と `solver.json` の `solve_seconds`（1258 は 2,366.898667、
   1266 は 1,612.557232、820 は 4,820.636161）を区別して扱う。検証秒と solve 秒を
   混同しない。

（完）
